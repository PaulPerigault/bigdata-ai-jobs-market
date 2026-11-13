# tools/ (template)

Pinned development tools: `golangci-lint`, `govulncheck`, `gitleaks`, `lefthook`, `task`. Replace `__MODULE__` in `go.mod`, keep `go.sum`, run `go mod tidy` then check **every** tool:

```text
go tool -modfile=tools/go.mod lefthook version
go tool -modfile=tools/go.mod task --version
go tool -modfile=tools/go.mod gitleaks version
go tool -modfile=tools/go.mod govulncheck -version
go tool -modfile=tools/go.mod golangci-lint --version
```

`github.com/go-json-experiment/json` is pinned at v1.27.2: the 2025 pseudo-version that `go get -tool` picked fails to compile `lefthook` with Go 1.27 (`json.SkipFunc` undefined). Verified on Go 1.27.4, 2026-11-12. Infrastructure variant: add `go get -tool github.com/terraform-linters/tflint@<version>`.
