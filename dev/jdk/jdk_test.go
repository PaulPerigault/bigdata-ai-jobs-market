package main

import (
	"archive/zip"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

func javaName() string {
	if runtime.GOOS == "windows" {
		return "java.exe"
	}
	return "java"
}

// zipBytes builds an archive in a temporary file and returns its path, digest and size.
func zipBytes(t *testing.T, names ...string) (string, string, int64) {
	t.Helper()
	path := filepath.Join(t.TempDir(), "a.zip")
	f, err := os.Create(path)
	if err != nil {
		t.Fatal(err)
	}
	zw := zip.NewWriter(f)
	for _, n := range names {
		w, err := zw.Create(n)
		if err != nil {
			t.Fatal(err)
		}
		_, _ = w.Write([]byte("x"))
	}
	if err := zw.Close(); err != nil {
		t.Fatal(err)
	}
	if err := f.Close(); err != nil {
		t.Fatal(err)
	}
	b, _ := os.ReadFile(path)
	sum := sha256.Sum256(b)
	return path, hex.EncodeToString(sum[:]), int64(len(b))
}

func copyFetch(src string) func(pin, string) error {
	return func(p pin, dest string) error {
		b, err := os.ReadFile(src)
		if err != nil {
			return err
		}
		return save(strings.NewReader(string(b)), dest, p)
	}
}

func newResolver(t *testing.T, home string, fetch func(pin, string) error, p pin) resolver {
	t.Helper()
	return resolver{
		home: home, cache: filepath.Join(t.TempDir(), "jdk"), pin: p, hasPin: true,
		major: func(string) (int, error) { return 17, nil }, fetch: fetch, log: func(string) {},
	}
}

func TestResolveKeepsAValidEnvironmentJDK(t *testing.T) {
	r := newResolver(t, "/opt/jdk17", func(pin, string) error { return errors.New("must not download") }, pin{})
	got, err := r.resolve()
	if err != nil || got != "/opt/jdk17" {
		t.Fatalf("got %q, %v", got, err)
	}
}

func TestResolveRejectsUnsupportedEnvironmentJDK(t *testing.T) {
	r := newResolver(t, "/opt/jdk22", func(pin, string) error { return errors.New("offline") }, pin{})
	r.major = func(string) (int, error) { return 22, nil }
	if _, err := r.resolve(); err == nil {
		t.Fatal("Java 22 must not be accepted and the failed download must surface")
	}
}

func TestResolveDownloadsVerifiesExtractsAndReuses(t *testing.T) {
	path, sum, size := zipBytes(t, "jdk-17.0.21+9/bin/"+javaName())
	p := pin{SHA256: sum, Size: size, Zip: true}
	calls := 0
	fetch := func(p pin, dest string) error { calls++; return copyFetch(path)(p, dest) }
	r := newResolver(t, "", fetch, p)
	first, err := r.resolve()
	if err != nil || !strings.Contains(first, "jdk-17.0.21+9") {
		t.Fatalf("got %q, %v", first, err)
	}
	second, err := r.resolve()
	if err != nil || second != first || calls != 1 {
		t.Fatalf("cache not reused: %q %v calls=%d", second, err, calls)
	}
}

func TestResolveRefusesAWrongDigest(t *testing.T) {
	path, _, size := zipBytes(t, "jdk/bin/"+javaName())
	r := newResolver(t, "", copyFetch(path), pin{SHA256: strings.Repeat("0", 64), Size: size, Zip: true})
	if _, err := r.resolve(); err == nil || !strings.Contains(err.Error(), "SHA-256 mismatch") {
		t.Fatalf("want a digest mismatch, got %v", err)
	}
	if h := findHome(r.cache); h != "" {
		t.Fatalf("nothing may be extracted after a mismatch, found %s", h)
	}
}

func TestSaveRefusesMoreThanThePinnedSize(t *testing.T) {
	err := save(strings.NewReader("0123456789"), filepath.Join(t.TempDir(), "x"), pin{Size: 4, SHA256: "00"})
	if err == nil || !strings.Contains(err.Error(), "larger") {
		t.Fatalf("got %v", err)
	}
}

func TestExtractRefusesPathTraversal(t *testing.T) {
	path, _, _ := zipBytes(t, "../escape.txt")
	dir := filepath.Join(t.TempDir(), "out")
	if err := extractZip(path, dir); err == nil {
		t.Fatal("a path outside the target must be refused")
	}
}

func TestJavaMajorParsing(t *testing.T) {
	for in, want := range map[string]int{`version "17.0.21"`: 17, `version "1.8.0_402"`: 8, `version "22.0.2"`: 22, `version "11"`: 11} {
		m := versionRe.FindStringSubmatch(in)
		if m == nil {
			t.Fatalf("no match for %s", in)
		}
		if got := parseMajor(m[1], m[2]); got != want {
			t.Errorf("%s: got %d, want %d", in, got, want)
		}
	}
}
