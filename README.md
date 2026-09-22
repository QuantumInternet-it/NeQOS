# NeQOS — Neapolitan / Networked Quantum Operating System

NeQOS is a distributed operating system for quantum networks. It realizes
network services as meta-protocols dynamically composed at run time from
reusable micro-protocols, while coordinating device-local execution across
heterogeneous quantum-classical resources.

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

## Release material

The [v0.4.0 release](Releases/v0.4.0/) provides standalone NodeEngine and
DeviceOS distributions, configurations, and example protocol material for
software evaluation. The release instructions describe the supplied artifacts
and their use on the supported platforms.

## References

### Theoretical foundations

1. A. S. Cacciapuoti and M. Caleffi, [*A Quantum Internet Protocol Suite
   Beyond Layering*](https://arxiv.org/abs/2602.19998), *IEEE Transactions on
   Network Science and Engineering* **13**, 9170-9187 (2026).
2. M. Caleffi and A. S. Cacciapuoti, [*Quantum Internet Architecture:
   Unlocking Quantum-Native Routing via Quantum
   Addressing*](https://arxiv.org/abs/2507.19655), *IEEE Transactions on
   Communications* **74**, 3577-3599 (2026).
3. A. S. Cacciapuoti *et al.*, [*Quantum-Native Architectural Tenets and
   Philosophy for the Quantum
   Internet*](https://datatracker.ietf.org/doc/draft-cacciapuoti-qirg-quantum-native-architecture/),
   IETF Internet-Draft, work in progress (2026).

### Related work

3. M. Caleffi, L. d'Avossa and A. S. Cacciapuoti, [*Engineering Quantum
   Links: Noise and Quantum-State-Degradation Metrics over Metropolitan Fiber
   Network*](https://arxiv.org/abs/2609.11359), arXiv:2609.11359 (2026).
4. L. d'Avossa, D. Salvoni, A. S. Cacciapuoti and M. Caleffi, [*Entanglement
   Meets Reality: A Network Engineering Assessment and Forecast of Rackable
   Entanglement Sources*](https://arxiv.org/abs/2609.11387), arXiv:2609.11387
   (2026).
