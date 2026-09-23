# NeQOS — Neapolitan / Networked Quantum Operating System

NeQOS is a distributed operating system for quantum networks. It realizes
network services as meta-protocols: run-time compositions of reusable
micro-protocols that coordinate device-local execution across heterogeneous
quantum-classical resources. This architectural treatment follows the
quantum-native protocol and architectural principles developed in
[1-3].

The system adopts a microkernel-inspired organization. The NodeEngine provides
network-level orchestration, resource binding, execution-state management and
telemetry aggregation; DeviceOS hosts a DeviceEngine co-located with each
device and exposes the corresponding abstract task surface.

## Extensibility

NeQOS is extensible at both architectural boundaries.

- At the network-service boundary, new micro-protocols and meta-protocols can
  extend the protocol catalog and compose existing network functionalities into
  new services.
- At the device boundary, hardware drivers map the declared device-task surface
  to vendor-specific device software, enabling additional quantum-classical
  hardware to be incorporated without changing network-service logic.

## Hardware support

The current DeviceOS distribution includes drivers for:

- NuCrypt [EPS1000W entangled-photon source](https://www.nucrypt.net/EPS-1000-W.html);
- NuCrypt [PA1000/PA2000 polarization controller](https://nucrypt.net/PA-1000.html);
- Thorlabs [MPC320 polarization controller](https://www.thorlabs.com/thorproduct.cfm?partnumber=MPC320);
- Thorlabs [DV1550AA variable optical attenuator](https://www.thorlabs.com/digital-variable-optical-attenuators-dvoas-sm-fiber-coupled);
- Swabian Instruments [Time Tagger](https://www.swabianinstruments.com/time-tagger/);
- Photec (Photon Technology) [SNSPD controller](https://www.cnphotec.com/en/product/snspd/snspd-system#product); and
- a Fake driver for software-only evaluation.

Additional hardware can be integrated through the public Device Driver API.

## Release material

Pre-built executable distributions are available from the
[NeQOS Releases page](https://github.com/QuantumInternet-it/NeQOS/releases).

The current release, [v0.4.0](https://github.com/QuantumInternet-it/NeQOS/releases),
provides standalone NodeEngine for Windows 11 (`x86_64`) and macOS Apple Silicon (`arm64`),
and DeviceOS for Windows 11 (`x86_64`). It also includes configurations and
example protocol material for software evaluation.

Download the software from
the [v0.4.0 release page](https://github.com/QuantumInternet-it/NeQOS/releases) and see the [v0.4.0 README](Releases/v0.4.0/README.md)
for installation and usage details.

The [release history](Releases/README.md) records version-specific additions, fixes and
compatibility notes.

## License and evaluation access

Running NodeEngine or DeviceOS requires a valid NeQOS license. Evaluation
licenses and access information can be requested at
[info@quantuminternet.it](mailto:info@quantuminternet.it).

## References

### Theoretical foundations

- **1.** A. S. Cacciapuoti and M. Caleffi, [*A Quantum Internet Protocol Suite
   Beyond Layering*](https://doi.org/10.1109/TNSE.2026.3679795), *IEEE Transactions on
   Network Science and Engineering* **13** vol. 13, pp. 9170-9187, 2026. Invited Paper.
- **2.** M. Caleffi and A. S. Cacciapuoti, [*Quantum Internet Architecture:
   Unlocking Quantum-Native Routing via Quantum
   Addressing*](https://doi.org/10.1109/TCOMM.2025.3650397), *IEEE Transactions on
   Communications* **74**, vol. 74, pp. 3577-3599, 2026. Invited paper.
- **3.** A. S. Cacciapuoti *et al.*, [*Quantum-Native Architectural Tenets and
   Philosophy for the Quantum
   Internet*](https://datatracker.ietf.org/doc/draft-cacciapuoti-qirg-quantum-native-architecture/),
   IETF Internet-Draft, work in progress (2026).

### Experimental quantum networking

- **4.** M. Caleffi, L. d'Avossa, I. I. Machuca Flores, M. Grillo, E. Montella and
   A. S. Cacciapuoti, [*Towards Quantum Networks: Characterizing Raman Noise
   over Metropolitan-scale Fiber
   Network*](https://ieeexplore.ieee.org/document/11627564/), *2026 IEEE
   International Conference on Smart Computing Workshops and Other Affiliated
   Events (SmartComp Companion)*, 109-113 (2026). *Invited paper.*
- **5.** L. d'Avossa, E. Montella, M. Grillo, A. S. Cacciapuoti and M. Caleffi,
   [*Optimization of C-Band Quantum Traffic Coexisting With O-Band Classical
   Traffic: Preliminary
   Results*](https://ieeexplore.ieee.org/document/11641122/), *2026 IEEE
   International Mediterranean Conference on Communications and Networking
   (MeditCom)*, 1-6 (2026).
- **6.** L. d'Avossa, A. S. Cacciapuoti and M. Caleffi, [*Interconnection of
   Quantum Networks at Urban scale: Analysis of Temporal Stability of
   Entangled Photon Sources*](https://arxiv.org/abs/2607.27906),
   arXiv:2607.27906 (2026).
- **7.** M. Caleffi, L. d'Avossa and A. S. Cacciapuoti, [*Engineering Quantum
   Links: Noise and Quantum-State-Degradation Metrics over Metropolitan Fiber
   Network*](https://arxiv.org/abs/2609.11359), arXiv:2609.11359 (2026).
- **8.** L. d'Avossa, D. Salvoni, A. S. Cacciapuoti and M. Caleffi, [*Entanglement
   Meets Reality: A Network Engineering Assessment and Forecast of Rackable
   Entanglement Sources*](https://arxiv.org/abs/2609.11387), arXiv:2609.11387
   (2026).
