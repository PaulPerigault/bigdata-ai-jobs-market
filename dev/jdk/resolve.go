package main

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strconv"
)

// pin is one Temurin archive: where it comes from, its digest and size, how it is packed.
type pin struct {
	URL    string
	SHA256 string
	Size   int64
	Zip    bool
}

const release = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.21%2B9/"

// pins holds Eclipse Temurin 17.0.21+9 (hotspot, jdk). Digests are the ones the Adoptium API
// published on 2026-11-13. Refresh URL, digest and size together.
var pins = map[string]pin{
	"windows/amd64": {release + "OpenJDK17U-jdk_x64_windows_hotspot_17.0.21_9.zip",
		"98518ecf554465057ee5509462631deeee374bc368c12a411d225cd29381f84b", 191117380, true},
	"linux/amd64": {release + "OpenJDK17U-jdk_x64_linux_hotspot_17.0.21_9.tar.gz",
		"8b9b611d917e3dfd8419d3566b5949226f69b052fed7e109c1368add1dfe8711", 193594705, false},
	"linux/arm64": {release + "OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.21_9.tar.gz",
		"3e4eca7ead088f080af1476007decf010a240a1eb4e1e78c54fa32fbcc347084", 192336814, false},
	"darwin/amd64": {release + "OpenJDK17U-jdk_x64_mac_hotspot_17.0.21_9.tar.gz",
		"868f5c672b3389fdbe48e44f94ae170f01668b1401360944fc7159d7cc9772cc", 180879475, false},
	"darwin/arm64": {release + "OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.21_9.tar.gz",
		"78b08c7f5a0598242d5719c022e19479cb4a3aa45c37c19726a757a469ed1c15", 186192554, false},
}

// resolver carries every dependency, so tests run without network or JVM.
type resolver struct {
	home   string
	cache  string
	pin    pin
	hasPin bool
	major  func(home string) (int, error)
	fetch  func(p pin, dest string) error
	log    func(string)
}

func supported(m int) bool { return m == 11 || m == 17 }

func (r resolver) usable(home string) bool {
	if home == "" {
		return false
	}
	m, err := r.major(home)
	return err == nil && supported(m)
}

func (r resolver) resolve() (string, error) {
	if r.usable(r.home) {
		return r.home, nil
	}
	if h := findHome(r.cache); h != "" && r.usable(h) {
		return h, nil
	}
	if !r.hasPin {
		return "", fmt.Errorf("no JDK 11 or 17 in JAVA_HOME and no pinned archive for %s/%s", runtime.GOOS, runtime.GOARCH)
	}
	r.log("downloading the pinned Temurin 17 into " + r.cache)
	if err := r.install(); err != nil {
		return "", err
	}
	h := findHome(r.cache)
	if h == "" || !r.usable(h) {
		return "", errors.New("the extracted archive holds no usable JDK")
	}
	return h, nil
}

func (r resolver) install() error {
	if err := os.MkdirAll(r.cache, 0o750); err != nil {
		return err
	}
	archive := filepath.Join(r.cache, "download.tmp")
	defer func() { _ = os.Remove(archive) }()
	if err := r.fetch(r.pin, archive); err != nil {
		return err
	}
	stage, err := os.MkdirTemp(r.cache, "stage-")
	if err != nil {
		return err
	}
	defer func() { _ = os.RemoveAll(stage) }()
	if err := extract(archive, stage, r.pin.Zip); err != nil {
		return err
	}
	final := filepath.Join(r.cache, "temurin-17")
	_ = os.RemoveAll(final)
	return os.Rename(stage, final)
}

// findHome returns the directory under root that holds bin/java (macOS: Contents/Home), or "".
func findHome(root string) string {
	exe := "java"
	if runtime.GOOS == "windows" {
		exe = "java.exe"
	}
	for _, depth := range []string{"*", "*/*", "*/*/*"} {
		hits, _ := filepath.Glob(filepath.Join(root, "temurin-17", depth, "bin", exe))
		if len(hits) > 0 {
			return filepath.Dir(filepath.Dir(hits[0]))
		}
	}
	return ""
}

var versionRe = regexp.MustCompile(`version "(\d+)(?:\.(\d+))?`)

// javaMajor runs `<home>/bin/java -version` and returns the major version (1.8 gives 8).
func javaMajor(home string) (int, error) {
	exe := filepath.Join(home, "bin", "java")
	out, err := exec.Command(exe, "-version").CombinedOutput() // #nosec G204 -- path from JAVA_HOME or our cache
	if err != nil {
		return 0, err
	}
	m := versionRe.FindSubmatch(out)
	if m == nil {
		return 0, errors.New("cannot read the Java version")
	}
	return parseMajor(string(m[1]), string(m[2])), nil
}

// parseMajor turns the first two version groups into a major number: "1","8" is Java 8.
func parseMajor(first, second string) int {
	major, _ := strconv.Atoi(first)
	if major == 1 && second != "" {
		major, _ = strconv.Atoi(second)
	}
	return major
}
