# NeQOS release history

This page records release-specific additions, corrections and compatibility notes. The repository [README](../README.md) always links to the most recent release.

## Current release

[v0.5.0](v0.5.0/README.md) is the current NeQOS release. Pre-built executable distributions are available from the [v0.5.0 release](https://github.com/QuantumInternet-it/NeQOS/releases/tag/v0.5.0).

## v0.5.0

### Changes from v0.4.0

- Operator User Guide and public protocol cookbook integrated with the API site.
- Delegated device leases for nested foreground workflows.
- Reusable acquisition, timing, raw-stream, polarization compensation and tomography/fidelity building blocks.

See the [v0.5.0 release README](v0.5.0/README.md) for distribution details, license requirements, launch commands and documentation links.

## v0.4.0

### Added

- Standalone macOS Apple Silicon (`arm64`) NodeEngine distribution.
- Standalone Windows 11 (`x86_64`) DeviceOS distribution.
- Network configurations and open protocol-pack material for software evaluation.
- A Fake-device configuration for an end-to-end runtime smoke test.

### Compatibility

- NodeEngine is supplied for macOS Apple Silicon (`arm64`).
- DeviceOS is supplied for Windows 11 (`x86_64`).
- Hardware-dependent operation requires an equivalent device installation and, where applicable, the corresponding vendor software.

See the [v0.4.0 release README](v0.4.0/README.md) for the executable layout, license requirement and run instructions.
