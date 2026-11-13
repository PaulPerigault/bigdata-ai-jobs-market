package main

import (
	"archive/tar"
	"archive/zip"
	"compress/gzip"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const downloadTimeout = 10 * time.Minute

// download fetches p.URL into dest, refuses more than p.Size bytes, and fails unless the SHA-256
// of what was written equals p.SHA256.
func download(p pin, dest string) error {
	ctx, cancel := context.WithTimeout(context.Background(), downloadTimeout)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, p.URL, nil)
	if err != nil {
		return err
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer func() { _ = resp.Body.Close() }()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("download: HTTP %d", resp.StatusCode)
	}
	return save(resp.Body, dest, p)
}

func save(src io.Reader, dest string, p pin) error {
	f, err := os.Create(dest) // #nosec G304 -- path built by the caller inside the cache
	if err != nil {
		return err
	}
	h := sha256.New()
	n, err := io.Copy(io.MultiWriter(f, h), io.LimitReader(src, p.Size+1))
	if cerr := f.Close(); err == nil {
		err = cerr
	}
	if err != nil {
		return err
	}
	if n > p.Size {
		return errors.New("download: larger than the pinned size")
	}
	if got := hex.EncodeToString(h.Sum(nil)); got != p.SHA256 {
		return fmt.Errorf("download: SHA-256 mismatch (got %s, want %s)", got, p.SHA256)
	}
	return nil
}

// extract unpacks a verified archive into dir, refusing any path that escapes it.
func extract(archive, dir string, isZip bool) error {
	if isZip {
		return extractZip(archive, dir)
	}
	return extractTarGz(archive, dir)
}

func inside(dir, name string) (string, error) {
	target := filepath.Join(dir, filepath.FromSlash(name))
	if target != dir && !strings.HasPrefix(target, dir+string(os.PathSeparator)) {
		return "", fmt.Errorf("unsafe path in archive: %s", name)
	}
	return target, nil
}

func extractZip(archive, dir string) error {
	zr, err := zip.OpenReader(archive)
	if err != nil {
		return err
	}
	defer func() { _ = zr.Close() }()
	for _, f := range zr.File {
		target, err := inside(dir, f.Name)
		if err != nil {
			return err
		}
		if f.FileInfo().IsDir() {
			if err := os.MkdirAll(target, 0o750); err != nil {
				return err
			}
			continue
		}
		rc, err := f.Open()
		if err != nil {
			return err
		}
		err = writeFile(target, rc, f.Mode())
		_ = rc.Close()
		if err != nil {
			return err
		}
	}
	return nil
}

func extractTarGz(archive, dir string) error {
	f, err := os.Open(archive) // #nosec G304 -- path built by the caller inside the cache
	if err != nil {
		return err
	}
	defer func() { _ = f.Close() }()
	gz, err := gzip.NewReader(f)
	if err != nil {
		return err
	}
	defer func() { _ = gz.Close() }()
	tr := tar.NewReader(gz)
	for {
		hdr, err := tr.Next()
		if errors.Is(err, io.EOF) {
			return nil
		}
		if err != nil {
			return err
		}
		if err := untar(tr, hdr, dir); err != nil {
			return err
		}
	}
}

func untar(tr *tar.Reader, hdr *tar.Header, dir string) error {
	target, err := inside(dir, hdr.Name)
	if err != nil {
		return err
	}
	switch hdr.Typeflag {
	case tar.TypeDir:
		return os.MkdirAll(target, 0o750)
	case tar.TypeReg:
		return writeFile(target, tr, os.FileMode(hdr.Mode))
	default: // links are skipped: nothing the JVM needs, and none can point outside the cache
		return nil
	}
}

func writeFile(target string, src io.Reader, mode os.FileMode) error {
	if err := os.MkdirAll(filepath.Dir(target), 0o750); err != nil {
		return err
	}
	out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, mode.Perm()|0o600) // #nosec G304 -- checked by inside
	if err != nil {
		return err
	}
	_, err = io.Copy(out, src) // #nosec G110 -- the archive is size-bounded and digest-checked
	if cerr := out.Close(); err == nil {
		err = cerr
	}
	return err
}
