# NeQOS LLM Authoring Instructions

Apply these instructions when generating or extending an Open meta-protocol library. Read them together with the Reserved and Open libraries supplied by the user's NodeEngine distribution. This guide accompanies NeQOS 0.5.0; verify the contracts and formats against the supplied release before generating files.

## 1. Establish the Available Context

- Inspect `NodeEnginePack/ReservedMetaProtocols/` for Built-in contracts and `NodeEnginePack/OpenMetaProtocols/` for editable examples.
- Report the file paths actually read, the target NeQOS release, and sources you cannot access. Do not claim to have read an entire archive or folder if the interface only exposes part of it.
- Search manifests and protocol descriptions first, then read the complete relevant `protocol.json` files, including `sharedParams`, `inputSchema`, `outputSchema`, `resourceRequests` and stages. Read the relevant Open manifests, handlers and run inputs.
- Use the matching public NodeEngine handler and DeviceOS API documentation when needed. If a necessary API contract is unavailable, request it instead of inventing a signature.
- Treat the supplied release contracts as authoritative. Documentation from another release or remembered examples must not override them.
- Treat example device IDs, timings and physical values as examples, not as settings for the user's bench.

`ReservedMetaProtocols` is already the distributed Built-in capability catalog. Do not create another hand-maintained catalog. Only Built-in contracts explicitly marked `"exported": true` may be invoked by an Open protocol. Children defined in the loaded Open library do not need this protected-only field.

## 2. Compose Existing Behavior First

1. Search existing exported Built-in protocols and existing Open definitions before creating new behavior. Explain which contracts satisfy each requested operation and what, if anything, is missing.
2. Prefer declarative composition through `SubmitMicroProtocolStage` and `WaitMicroProtocolStage`. Use the matching `protocolKey` for submission and waiting, pass declared child inputs through `sharedParamOverrides`, and import only paths declared by the child's `outputSchema`.
3. Reuse existing Open children within the generated library. Follow the manifest rules for the library actually loaded; do not assume a protocol in another example library becomes available automatically. Identify any Open definition you propose to include and register it explicitly.
4. Do not copy protected implementations or import internal Reserved services to bypass a public contract. Compose exported protocols through their public interfaces.
5. Avoid duplicated setup, acquisition, timing, loading, calibration and scientific analysis. Reuse a child with different inputs when that expresses the requested behavior.
6. Do not produce long repeated stage lists when a reusable child plus justified runtime iteration can express them. Do not add wrappers that only rename an existing protocol without serving the user's workflow.
7. If a required reusable primitive is absent, describe the missing contract. Do not silently implement a protected workflow in a new Open handler.

## 3. Use Local Handlers Where Needed

Local Python handlers are appropriate for runtime branching, bounded iteration, convergence decisions, aggregation of child results or new domain-specific behavior not provided by existing contracts. Explain why declarative composition is insufficient before adding one. New scientific analysis must be explicitly requested and its assumptions documented; do not invent calculations to fill a gap.

- Keep reusable logic in one place rather than duplicating it across handlers.
- Document the handler's inputs, decisions, produced values and reason for existing in Python docstrings.
- Follow the public `StageContext` and `StageResult` APIs demonstrated in the matching Open examples and handler reference. Do not guess whether a call is synchronous or awaited.
- In runtime composition, retain child runtime identifiers, check failures, wait for completion and consume declared results. Do not treat submission as completion or suppress child failures.
- Register callable stages in `HANDLERS`. A file listed in a protocol's `handlerFiles` registers only handlers used by that protocol. Shared Open handlers belong in `sharedHandlerFiles`; declare each handler file once and avoid collisions with compiled names.
- Use finite timeouts and explicit termination conditions for repeated work. A deliberately unbounded monitor requires a parent that owns its termination.

## 4. Respect Device and Acquisition Ownership

- Prefer exported device configuration and acquisition protocols over direct task calls. For a small uncovered device operation, use the documented `RunSingleTaskStage` or `ctx.run_task` interface with declared resources and advertised task inputs.
- Do not call TimeTagger acquisition tasks such as `CreateMeasurement`, `ActivateMeasurements` or `StartMeasurement` directly from an Open handler. Compose the appropriate exported acquisition contract for count rates, coincidences, correlations or raw streams.
- Preserve acquisition guard semantics from the chosen contract. Do not select `latchGuard: disabled` merely to make an input pass validation. Ask for the intended policy when it is unresolved.
- Sequential child measurements do not represent a simultaneous acquisition window. If simultaneity is required and no public contract provides it, report that missing capability.
- Declare resources for each protocol that operates devices, including delegated children. Use parameterized resource declarations supported by the release. Do not override a child's resources to an empty list when it needs hardware.
- The runtime manages ancestor/child leases and the active device turn. A parent may poll a delegated child but cannot operate that device while the child is active. Do not invent manual ownership or an `inherit`/`acquire` catalog switch.
- Compose existing state restoration workflows. If a new handler changes reversible device state across invocations, use the documented terminal cleanup API and clear the cleanup only after normal restoration succeeds.

## 5. Define Inputs and Results Precisely

- Put configurable experiment values in `sharedParams`, describe and constrain them in `inputSchema`, and supply experiment-specific overrides in the run's `input.json`. Keep device identities, topology, paths and channels out of Python literals.
- Follow the release's actual schema semantics for required fields, defaults, nullability and nested fields. Do not assume this schema supports every JSON Schema keyword.
- Define caller-meaningful `outputSchema` exports before stages. Every successful completion must publish all declared exports, normally through `PublishResultStage`.
- Map child exports through declared imports and publish the parent's declared result. Do not reach into private child scratchpad fields or scrape operational artifacts as a result API.
- Preserve the distinction: `run-manifest.json` says how the run executed; `result.json` says what it produced.
- Preserve nested statuses when handling task replies: the outer status describes the NodeEngine-to-DeviceOS operation, while the task result can describe the driver/hardware outcome. Follow the documented success checks for the selected task.

## 6. Generate a Portable Library

Create the user's library separately from the shipped Reserved contracts and Open examples. Do not edit shipped contracts to make generated inputs valid.

```text
MyLibrary/
  manifest.json
  MetaProtocolsDef/
    MY-ROOT/
      protocol.json
      Handlers.py       # only when needed
  MetaProtocolsRun/
    my-root/
      input.json
  network.json          # only if the user requests a new network example
```

For NeQOS 0.5.0, the library manifest has `schemaVersion: "0.5"` and a `libraryId`. Each `metaProtocols` entry declares a `protocolId`, `definitionFile` and optional `handlerFiles`; each definition file contains exactly that protocol. Definition and handler paths remain relative and inside the library. Do not add undeclared manifest fields.

The run input has a different schema version: `"0.4"`. It declares `metaProtocolLibrary` with the same `libraryId` and a `folder` resolved relative to the input file, and an ordered `steps` list. With the layout above, `folder` is `"../.."`. Do not use the manifest schema version as the run-input version. Check these formats against the supplied release.

Format JSON with indentation and one object property per line. Register all included Open children, use unique protocol and handler identifiers, and provide a minimal run input with explicitly documented unresolved values. Do not fabricate a bench configuration if the user's network file already supplies it.

## 7. Work in This Order

1. Confirm available sources and identify missing experiment information.
2. Present a concise composition plan naming exact existing contracts, effective child inputs, imported outputs, resources, timeouts and final results. Explain any necessary new handler.
3. Generate the library files and a minimal run input.
4. Check JSON parsing, manifest paths and IDs, handler registration, schema constraints, shared references, resource declarations and child import/export mappings. Parse Python syntax without importing or executing handlers during this review.
5. State which checks ran, their outcomes and any checks that remain unperformed. Do not report runtime validation from syntax checks alone.
6. Provide the exact launch command using the executable and arguments documented for the supplied distribution. Label it as execution: starting NodeEngine can invoke hardware. Keep authoring and static checks separate from running an experiment.

Do not invent a standalone validator, CLI switch or dry-run mode. If runtime checking is only available by loading or running NodeEngine, explain that limitation. Do not execute the generated experiment as part of an authoring request.

## 8. Final Review

- Every Built-in child is explicitly exported; every Open child is registered in the loaded library.
- Child inputs use the actual contract, and every imported output path is declared by that child.
- New code serves a documented need and does not duplicate an available workflow.
- Devices and guard policies are explicit; delegated ownership and restoration are respected.
- Successful publication includes all declared results, with operational provenance kept in the manifest.
- The deliverable includes all required files, a minimal run input, evidence of checks and clearly stated unresolved inputs.
