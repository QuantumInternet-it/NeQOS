# NeQOS — Neapolitan / Networked Quantum Operating System v0.5.0

NeQOS coordinates quantum-network devices through reusable micro-protocols
and composed experimental workflows. **NodeEngine** orchestrates the network;
**DeviceOS** runs beside each device and executes its driver tasks.

## Changes from v0.4.0

### Guided setup and protocol cookbook

The operator manual now covers installation, network configuration, first
runs and experimental recipes alongside the API reference. A public protocol
cookbook lists required and optional inputs, defaults, outputs and examples.

### Nested workflows with delegated device leases

Foreground child protocols can use devices held by their parent workflow
without releasing its exclusive lease between operations. Run manifests record
lease ownership, active executors and cleanup/recovery evidence.

### Reusable measurement and polarization workflows

The Reserved catalog includes finite acquisitions with explicit latch-guard
policies, raw-stream recording and transfer, timing alignment, polarization
compensation, tomography reconstruction and fidelity estimation.

## Download

Download the executable archives attached to the
[v0.5.0 release](https://github.com/QuantumInternet-it/NeQOS/releases/tag/v0.5.0).
Choose the component, operating system and architecture indicated by each
asset.

## Release contents

| Distribution | Platform | Runtime role |
| --- | --- | --- |
| NodeEngine | Windows 11 (`x86_64`) | Network-level orchestration and meta-protocol execution. |
| NodeEngine | macOS Apple Silicon (`arm64`) | Network-level orchestration and meta-protocol execution. |
| DeviceOS | Windows 11 (`x86_64`) | Device-local task admission, scheduling and driver execution. |

Use the corresponding archive attached to the release; filenames can include
the platform and version.

Extract the **entire `.dist` directory** and keep its executable, libraries,
contracts and examples together. Do not copy only the executable. Install
device-specific vendor runtimes on the DeviceOS host that needs them.

## License

NodeEngine and DeviceOS require a valid NeQOS license at startup. Supply its
path explicitly with `--licenseFile`. Replace the placeholder license paths
in the examples with your own. To request an evaluation license, contact
[info@quantuminternet.it](mailto:info@quantuminternet.it).

## Start here: User Guide

The [NeQOS User Guide](https://quantuminternet-it.github.io/NeQOS/user-guide/index.html)
provides step-by-step instructions:

1. [Install the software](https://quantuminternet-it.github.io/NeQOS/user-guide/installation.html):
   distributions, licenses, vendor runtimes and per-PC data directories.
2. [Describe your bench](https://quantuminternet-it.github.io/NeQOS/user-guide/network.html):
   device identities, endpoints, link roles, detector channels and health guards.
3. [Run a hardware-free example](https://quantuminternet-it.github.io/NeQOS/user-guide/quickstart.html).
4. [Run and customize a protocol](https://quantuminternet-it.github.io/NeQOS/user-guide/running.html).
5. [Use experimental recipes](https://quantuminternet-it.github.io/NeQOS/user-guide/recipes.html)
   and the [public protocol cookbook](https://quantuminternet-it.github.io/NeQOS/user-guide/protocols/index.html),
   including required and optional inputs, defaults, outputs and available examples.
6. [Find results and troubleshoot failures](https://quantuminternet-it.github.io/NeQOS/user-guide/results.html).

## Developer API

- [NodeEngine API](https://quantuminternet-it.github.io/NeQOS/api/NodeEngine/index.html):
  protocol contracts, composition, Open packs and handler interfaces.
- [DeviceOS API](https://quantuminternet-it.github.io/NeQOS/api/DeviceOS/index.html):
  drivers, exported tasks, parameters, signals and runtime setup.

The online manual and API are updated independently of executable archives.
Check the documentation version and use matching binaries, contracts and
examples. The documentation may describe capabilities not present in an older
installed build; check that executable's `--version` and `--help`.

## Windows 11

Download and extract the Windows archives. Open **Command Prompt** (`cmd.exe`)
or **PowerShell**, then change to the appropriate `.dist` directory.
The commands below work in both shells.

### NodeEngine

```bat
cd NodeEngine.dist
.\NodeEngine.exe --version
.\NodeEngine.exe --help
```

### DeviceOS

```bat
cd DeviceOS.dist
.\DeviceOS.exe --version
.\DeviceOS.exe --help
```

An unsigned executable can be blocked before startup by Smart App Control or
another App Control policy. See the
[Windows startup guidance](https://quantuminternet-it.github.io/NeQOS/user-guide/installation.html#windows-unsigned-builds)
for the confirmed Smart App Control procedure and its security implications.

## macOS

NodeEngine is provided for Apple Silicon (`arm64`). Extract the archive, open
**Terminal** and change to the `NodeEngine.dist` directory. Set the executable
permission before first use:

```bash
cd NodeEngine.dist
chmod +x NodeEngine.bin
./NodeEngine.bin --version
./NodeEngine.bin --help
```
