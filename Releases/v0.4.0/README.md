# NeQOS — Neapolitan / Networked Quantum Operating System v0.4.0

This release provides executable distributions of the distributed runtime used
to operate quantum-network services through dynamic composition of
micro-protocols.

## Download

Download the pre-built archives for this release from the
[NeQOS Releases page](https://github.com/QuantumInternet-it/NeQOS/releases).

## Release contents

| Distribution | Platform | Runtime role |
| --- | --- | --- |
| `Win-x86_64-NodeEngine.dist.zip` | Windows 11 (`x86_64`) | Network-level orchestration and meta-protocol execution. |
| `MacOS-arm64-NodeEngine.dist.zip` | macOS Apple Silicon (`arm64`) | Network-level orchestration and meta-protocol execution. |
| `Win-x86_64-DeviceOS.dist.zip` | Windows 11 (`x86_64`) | Device-local task admission, scheduling and driver execution. |

Each archive contains a `.dist` directory. Keep this directory intact after
extraction: the executable uses the adjacent runtime libraries and supplied
configuration material.

## License

NodeEngine and DeviceOS require a valid NeQOS license at startup. Supply the
path explicitly through `--licenseFile`, as shown in the examples below. The
paths used here are placeholders: replace them with the locations of your own
license files. To request an evaluation license, contact
[info@quantuminternet.it](mailto:info@quantuminternet.it).

## Developer documentation

For DeviceOS driver interfaces and NodeEngine extension contracts, see the
[NeQOS Developer API](https://quantuminternet-it.github.io/NeQOS/). The
reference documents exported tasks, readable signals, public microprotocol
templates, open meta-protocol packs, and their handler contracts. It is updated
independently of the executable archives.

## Windows 11

Download and extract the Windows archives. Open **Command Prompt** (`cmd.exe`,
also known as the MS-DOS prompt), then change to the corresponding `.dist`
directory. You may also use PowerShell; the commands below work in both.

### NodeEngine

```bat
cd NodeEngine.dist
NodeEngine.exe --help
```

### DeviceOS

```bat
cd DeviceOS.dist
DeviceOS.exe --help
```

## macOS

NodeEngine is provided for Apple Silicon (`arm64`). Download and extract the
archive, then open **Terminal** and change to the `NodeEngine.dist` directory.
Make the executable executable before first use:

```bash
cd NodeEngine.dist
chmod +x NodeEngine.bin
./NodeEngine.bin --help
```

## Fake-device smoke test

The supplied `config/networkFakeNodeEngine.json` defines one `Fake` device
with identifier `FAKE-PRODUCER-01`. It is a minimal end-to-end test of the
protected `FAKE-SIMPLE-001` micro-protocol: NodeEngine submits two abstract
tasks to a DeviceEngine, which executes them through the bundled Fake driver.

The configuration uses `127.0.0.1`; therefore, a local smoke test runs both
processes on the same Windows 11 host. Open two Command Prompt windows. In the
first, start DeviceOS:


```bat
cd DeviceOS.dist
DeviceOS.exe --configFile .\config\networkFakeNodeEngine.json --nodeId FAKE-NODE --deviceId FAKE-PRODUCER-01 --licenseFile C:\path\to\license-DeviceOS.json
```

### NodeEngine on Windows 11

In the second window, start NodeEngine and wait for the protocol result:

```bat
cd NodeEngine.dist
NodeEngine.exe --configFile .\config\networkFakeNodeEngine.json --nodeId FAKE-NODE --protocolId FAKE-SIMPLE-001 --waitProtocol --licenseFile C:\path\to\license-NodeEngine.json
```

### NodeEngine on macOS (two-host test)

To run NodeEngine on macOS, first copy the same configuration to both hosts,
set `host` to the LAN address of the macOS host, and set `deviceEngine.ip` to
the LAN address of the Windows host running DeviceOS. The two copies must be
identical. Start DeviceOS on Windows as above, then open Terminal on macOS and
run:

```bash
cd NodeEngine.dist
chmod +x NodeEngine.bin
./NodeEngine.bin --configFile ./config/networkFakeNodeEngine.json --nodeId FAKE-NODE --protocolId FAKE-SIMPLE-001 --waitProtocol --licenseFile /path/to/license-NodeEngine.json
```