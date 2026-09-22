# NeQOS — Neapolitan / Networked Quantum Operating System v0.4.0

This release provides executable distributions of the distributed runtime used
to operate quantum-network services through dynamic composition of
micro-protocols.

## Release contents

| Distribution | Platform | Runtime role |
| --- | --- | --- |
| `MacOS-arm64/NodeEngine.dist.zip` | macOS Apple Silicon (`arm64`) | Network-level orchestration and meta-protocol execution. |
| `Win-x86_64/DeviceOS.dist.zip` | Windows 11 (`x86_64`) | Device-local task admission, scheduling and driver execution. |

Each archive contains a `.dist` directory. Keep this directory intact after
extraction: the executable uses the adjacent runtime libraries and supplied
configuration material.

## License

NodeEngine and DeviceOS require a valid NeQOS license at startup. Supply its
path explicitly through `--licenseFile`, as shown in the examples below. To
request an evaluation license, contact
[info@quantuminternet.it](mailto:info@quantuminternet.it).

## Running the executables

For example, after extracting the macOS distribution:

```bash
cd NodeEngine.dist
chmod +x NodeEngine.bin
./NodeEngine.bin --help
```

After extracting the Windows distribution:

```bat
cd DeviceOS.dist
DeviceOS.exe --help
```

Hardware-dependent operation requires an equivalent device installation and
its associated vendor software.

## Fake-device example

`config/networkFakeNodeEngine.json` defines one `Fake` device with the
identifier `FAKE-PRODUCER-01`. It is a minimal end-to-end example for the
protected `FAKE-SIMPLE-001` micro-protocol: NodeEngine submits two abstract
tasks to a DeviceEngine, which realizes them through the supplied Fake driver.

For a local smoke test, start DeviceOS first:

```bat
cd DeviceOS.dist
DeviceOS.exe --configFile .\config\networkFakeNodeEngine.json --nodeId FAKE-NODE --deviceId FAKE-PRODUCER-01 --licenseFile .\config\license.json
```

Then start NodeEngine and wait for the protocol result:

```bash
cd NodeEngine.dist
chmod +x NodeEngine.bin
./NodeEngine.bin --configFile ./config/networkFakeNodeEngine.json --nodeId FAKE-NODE --protocolId FAKE-SIMPLE-001 --waitProtocol --licenseFile ./config/license.json
```

The supplied file uses `127.0.0.1`. For a two-host execution, copy the same
file to both hosts, set `host` to the LAN address of the NodeEngine host, and
set `deviceEngine.ip` to the LAN address of the Windows host running DeviceOS.
The two copies must be identical.
