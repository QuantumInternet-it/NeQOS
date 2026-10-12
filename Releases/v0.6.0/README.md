# NeQOS — Neapolitan / Networked Quantum Operating System v0.6.0

NeQOS coordinates quantum-network devices through meta-protocols composed from reusable micro-protocols. **NodeEngine** orchestrates experiments; **DeviceOS** hosts a DeviceEngine and a hardware driver beside each device. Version 0.6.0 adds browser-based operation and separates the laboratory inventory from the experiment network.

## Release status and downloads

Release preparation is in progress. Software-only regression and simulated operator checks do not establish hardware correctness. Packaged-build and laboratory regression remain release checks; this README does not certify a completed Windows or macOS deployment. The 0.6.0 documentation is currently marked as development documentation.

Use the executable assets attached to the [NeQOS Releases page](https://github.com/QuantumInternet-it/NeQOS/releases) when the 0.6.0 release is published. Check each asset's component, operating system and architecture; do not substitute a 0.5.0 archive. Extract the **entire `.dist` directory**, not just the executable. NodeEngine's browser assets, protocol contracts and runtime dependencies must remain with it. Open libraries and Open drivers remain editable external source content.

## Changes from v0.5.0

### Browser operator interface

NodeEngine can serve an authenticated browser interface with three workspaces: **Network & devices**, **Library**, and **Execution**. The interface displays port-to-port optical/readout topology, device health and leases, supports parameter forms and drag-and-drop protocol sequences, and shows nested protocol/stage progression. NodeEngine resolves and validates the plan and its resources before admission; the browser does not guess device leases.

While a run or its cleanup is active, operators can observe the current run and devices or abort. Editing/submitting new plans, changing networks and browsing previous runs are blocked. Planned steps and child protocols continue normally. Abort waits for cleanup and leaves the queue paused until an explicit operator decision. Closing the browser does not stop NodeEngine or the experiment.

When idle, the experiment timeline supports saved revisions, parameter inspection and reuse, grouped published outputs and artifact downloads. Browser submission is limited to protocols supported by the operator planner, not every protocol visible in the catalog. See the [browser guide](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/browser-interface.html) for coverage and controls. Grafana configuration provides dashboard links; embedded live metrics are not included.

### Laboratory inventory and experiment activation

A stable `inventory-1` JSON file describes device identities, endpoints, driver configuration and boot settings. An `experiment-1` JSON file references that inventory and describes optical links, bindings and experiment operating settings. DeviceOS processes can remain running while NodeEngine validates and activates a different experiment when the system is idle.

Activation applies device settings through NodeEngine and commits the new topology only after successful completion. A failed activation retains the previous topology and records configuration drift; it is not an automatic rollback of hardware writes. A successful re-activation is required before starting another experiment. After a NodeEngine restart, re-validate and activate the intended experiment.

### Explicit optical and electrical wiring

Topology resolution follows declared device roles and link lineage, including passive `FiberSplitter` devices, analyzer H/V ports, detector channels and TimeTagger inputs. Detector-to-TimeTagger pairing is inferred only when the link/port mapping is unambiguous. Explicit `healthGuards` remain accepted but must agree with that mapping.

A detector need not be declared for an unguarded TimeTagger acquisition. A `required` latch guard needs an enabled, unambiguously mapped detector and the corresponding resources. Passive splitters have no DeviceOS, telemetry or lease. The GUI depicts declared wiring; it does not verify physical cables.

### Live execution and compact archives

The live execution graph uses bounded in-memory projections instead of repeatedly reading scientific manifests. Historical runs use indexed/cached archive reads, with large legacy JSON parsed outside the NodeEngine event loop. Operator history, saved experiments and queue records are stored in SQLite.

New operational manifests use schema `0.2`: compact previews reference full inputs, stage evidence, exports and lifecycle files. Scientific `result.json` outputs and declared export keys remain the scientific contract. See the [results guide](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/results.html) for file layout, archive handling and backups.

## Compatibility and upgrade notes

- Deploy matching 0.6.0 NodeEngine and DeviceOS builds. The Open Device Driver API is **0.6.0**; update external drivers and their registry declarations together.
- The canonical detector type is `Photec` and the explicit guard channel field is `snspdChannel`. `Photek`, `DetectorHealth` and `detectorHealthChannel` are rejected, not compatibility aliases. If a device ID was renamed, update its DeviceOS launch command and all network/run references.
- The single-file `--configFile` workflow remains available for networks using the current conventions. Inventory operation uses `--inventoryFile`, optionally with `--networkFile`; do not combine it with `--configFile` on NodeEngine.
- Run-plan schema remains `0.4`. Earlier archived runs remain readable and are not rewritten. Tools that read full values directly from manifests must follow the new `fullInputsFile`/`exportsFile` references when present.
- `--serve` and `--metaProtocolRun` are alternative modes. The standalone read-only viewer is not a live operator service and cannot launch experiments.
- Abort invokes registered cleanup; it does not undo completed steps or restore previously overwritten calibration tables. Review `persist` and factory-reset settings in the chosen experiment. Successful execution is not a physical acceptance certificate.

Back up network configurations, run inputs, calibration files and operator data before upgrading. Use binaries, contracts, examples and documentation from the same release. Install vendor runtimes only on the DeviceOS hosts that need them.

## License

NodeEngine and DeviceOS require a valid NeQOS license. Pass its path with `--licenseFile`; do not publish credentials or redistribute a personal activation file. Evaluation access: [info@quantuminternet.it](mailto:info@quantuminternet.it).

## Start on Windows

Run these commands from the corresponding extracted `.dist` directory. Paths and IDs below are placeholders: replace them with your inventory, experiment, license and selected node/device. Real startup can initialize hardware; these are not simulation commands.

First check each executable without connecting equipment:

```bat
.\DeviceOS.exe --version
.\DeviceOS.exe --help
```

```bat
.\NodeEngine.exe --version
.\NodeEngine.exe --help
```

Both must report `0.6.0`. Start one DeviceOS per enabled active device on its hardware host, using the same inventory:

```bat
.\DeviceOS.exe --configFile "C:\NeQOSConfig\lab-inventory.json" --deviceId YOUR_DEVICE_ID --licenseFile "C:\NeQOSConfig\license.json"
```

### Browser operation

Start NodeEngine once, then load, validate and activate the experiment in **Network & devices**:

```bat
.\NodeEngine.exe --inventoryFile "C:\NeQOSConfig\lab-inventory.json" --nodeId YOUR_NODE_ID --licenseFile "C:\NeQOSConfig\license.json" --serve --operatorPort 8766 --operatorData "C:\NeQOSData\OperatorData"
```

Open `http://127.0.0.1:8766` and enter the token printed in the NodeEngine terminal. Keep that process running. Do not start a second NodeEngine to attach a browser to an existing CLI run.

### Command-line operation

Alternatively, activate an experiment and run its plan without a browser:

```bat
.\NodeEngine.exe --inventoryFile "C:\NeQOSConfig\lab-inventory.json" --networkFile "C:\NeQOSConfig\experiment.json" --nodeId YOUR_NODE_ID --licenseFile "C:\NeQOSConfig\license.json" --metaProtocolRun "C:\NeQOSConfig\input.json" --waitProtocol
```

Passing `--networkFile` authorizes startup activation, including its recorded warnings. Review the configuration before launch. For a hardware-free first run, use the [Fake-device quickstart](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/quickstart.html) instead.

## macOS and remote operation

For a macOS NodeEngine archive, use its supplied launcher (for example `./NodeEngine.bin`) instead of `.\NodeEngine.exe`, with macOS paths and the same arguments. Check `--version` and `--help` first. DeviceOS can run on separate instrument PCs; configure reachable device endpoints and the required vendor runtimes on those hosts.

The browser need not run on the NodeEngine PC. The operator service binds to loopback, so access from another computer uses an SSH tunnel, not a direct connection to the laboratory host's HTTP port. Follow the [remote browser instructions](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/running.html#use-a-browser-on-another-computer); keep the documented authentication and origin checks enabled.

## Documentation

- [0.6.0 User Guide](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/index.html): installation, first runs and experimental recipes.
- [Inventory and network configuration](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/network.html).
- [Browser operator guide](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/browser-interface.html).
- [Protocol catalog](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/protocols/index.html) and [results guide](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/results.html).
- [NodeEngine API](https://quantuminternet-it.github.io/NeQOS/v0.6.0/api/NodeEngine/index.html).
- [DeviceOS API](https://quantuminternet-it.github.io/NeQOS/v0.6.0/api/DeviceOS/index.html), [Open driver contract](https://quantuminternet-it.github.io/NeQOS/v0.6.0/api/DeviceOS/DriverContract.html) and [driver authoring guide](https://quantuminternet-it.github.io/NeQOS/v0.6.0/user-guide/writing-hardware-driver.html).

These links select version 0.6.0 explicitly. The documentation root follows the stable release independently of this README; preparing this file does not publish binaries or promote the documentation to stable.
