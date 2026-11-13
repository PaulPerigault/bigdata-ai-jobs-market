// Command jdk prints a JAVA_HOME that PySpark 3.5 can use (Java 11 or 17), one line on stdout.
//
// Order: a valid JAVA_HOME already in the environment, then the cache `.tools/jdk` (ignored by Git),
// then a download of the pinned Eclipse Temurin 17 archive, checked against its pinned SHA-256
// before anything is extracted. Nothing is downloaded without a digest. See docs/adr/0005.
package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
)

const cacheDir = ".tools/jdk"

func main() {
	root, err := os.Getwd()
	if err != nil {
		fail(err)
	}
	pin, ok := pins[runtime.GOOS+"/"+runtime.GOARCH]
	env := resolver{
		home:   os.Getenv("JAVA_HOME"),
		cache:  filepath.Join(root, filepath.FromSlash(cacheDir)),
		pin:    pin,
		hasPin: ok,
		major:  javaMajor,
		fetch:  download,
		log:    func(s string) { fmt.Fprintln(os.Stderr, "jdk:", s) },
	}
	home, err := env.resolve()
	if err != nil {
		fail(err)
	}
	fmt.Println(home)
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "jdk:", err)
	os.Exit(1)
}
