# NeQOS LLM authoring instructions

Apply these instructions when generating or extending an Open library. Read them together with the built-in catalog (`ReservedMetaProtocols/`) and Open example libraries (`OpenMetaProtocols/`) supplied by the user's NodeEngine distribution. This guide accompanies NeQOS 0.6.0; verify the contracts and formats against the supplied release before generating files.

## 1. Establish the available context

- Inspect `NodeEnginePack/ReservedMetaProtocols/` for built-in contracts and `NodeEnginePack/OpenMetaProtocols/` for editable examples.
- Report the paths actually read, the target release and sources you cannot access. An upload alone does not establish that an entire archive is readable.
- Search manifests and descriptions first, then read complete relevant definitions: `sharedParams`, `inputSchema`, `outputSchema`, `resourceRequests`, stages and the built-in `exported` flag. Read the relevant Open manifests, handlers and run plans.
- Use the matching stage-handler, `StageContext`/`StageResult` and DeviceOS task-surface references. Request a missing API contract rather than inventing a signature.
- Treat the supplied release as authoritative. Example IDs, timing and physical values require review for the user's testbed.

The built-in catalog is the only index of built-in protocols. Only definitions marked `"exported": true` are public built-in protocols callable by an Open library. That flag is unrelated to result exports. Open definitions do not declare it. Use the current shipped examples cited by the documentation, not remembered examples from another release.

## 2. Compose existing behavior first

1. Identify public built-in protocols and existing Open definitions that satisfy the requested operations, then describe any missing contract.
2. Prefer `SubmitMicroProtocolStage` followed by `WaitMicroProtocolStage` with the same `protocolKey`. Pass only declared child inputs through `sharedParamOverrides`; import declared outputs or existing dictionary fields under a declared object export.
3. Register every included Open child in the loaded library. Definitions from another example library do not become available automatically.
4. Compose public built-in interfaces rather than copying their handler code or importing internal NodeEngine services.
5. Reuse setup, acquisition, timing, loading, calibration and scientific analysis. Add a wrapper only when it serves an actual parent contract or execution requirement.
6. Use a justified runtime loop instead of repeating long stage lists. New scientific analysis requires the user's request and documented assumptions.

## 3. Use local handlers where needed

Local handlers support runtime branching, bounded iteration, convergence decisions and aggregation. Explain why declared composition is insufficient before adding one. Document inputs, decisions, produced values and failure conditions in Python docstrings.

- Register callable stages in `HANDLERS`. A protocol's `handlerFiles` registers only handlers used by that protocol. Reusable handlers belong in `sharedHandlerFiles`; declare each file once and avoid built-in stage-handler names such as `PublishResultStage`.
- `ctx.submit_microprotocol`, child state checks, `ctx.child_output`, `ctx.get` and `ctx.set` are synchronous. Await device operations and `ctx.abort_microprotocol`.
- Store child runtime IDs in the scratchpad before returning; re-entry must not submit the same child again. Check failure/abort and unknown IDs, wait for `COMPLETED`, then read declared values through `ctx.child_output`.
- Return `StageResult` with `advance`, `repeat`, `requeue`, `complete` or `fail`. `requeue` returns to scheduling at the same stage; `repeat` runs it again inside the current execution. Include `reason` for failure and a non-negative `delaySec` when polling. Publish all required outputs before an early `complete`.
- Define explicit loop termination and an actual elapsed-time guard when needed. A declared catalog `timeoutSec` alone is not an enforced deadline for a handler-backed run. A deliberately unbounded monitor requires a parent that owns termination.

## 4. Respect devices, acquisition and leases

- Prefer public configuration and acquisition protocols to direct device operations. For a small uncovered task, use `RunSingleTaskStage` or `ctx.run_task` with declared resources and advertised inputs.
- Time Tagger acquisition through `CreateMeasurement`, `ActivateMeasurements` and `StartMeasurement` belongs to the built-in acquisition implementation. Open handlers compose the public acquisition contract for count rates, coincidences, correlations or raw streams.
- Select `latchGuard` from the experiment's intended detector-health policy, not merely to pass validation. Ask when it is unresolved.
- Sequential measurements are not a simultaneous acquisition window. Report a missing simultaneous-acquisition contract instead of relabelling sequential data.
- Every device-operating child declares its resources. Omit `resourceRequests` to retain the child declaration; an explicit list replaces it, and `[]` grants no device access.
- A lease root retains external ownership while a foreground child uses a delegated lease. The active turn means only that runtime instance may operate the device; its parent can poll but cannot issue competing operations. Siblings serialize and delegated background work is forbidden.
- Default `requeue` retains owned/delegated leases. `releaseResources=True` intentionally yields them and breaks uninterrupted exclusivity; use it only for a deliberate cooperative boundary.
- Register idempotent terminal restoration before opening reversible device state. On the normal path, verify restoration and clear the exact registration. Successful completion does not automatically execute pending cleanup.

## 5. Define inputs and results precisely

- Put configurable values and defaults in `sharedParams`; describe and constrain them in `inputSchema`. Its parameter names match `sharedParams` exactly. Supply testbed-specific overrides in the run plan and resolve devices/channels from the network where the chosen contract supports it.
- Input and output schemas use version `"0.1"`. Supported types are `string`, `integer`, `number`, `boolean`, `array` and `object`; booleans are not integers. Each specification has `type` and `description`.
- `required: true` means the effective value after defaults/overrides must be non-null. Defaults are not schema fields. Nested objects merge recursively; lists/scalars are replaced. Required descendants apply when their parent object is non-null. Handler-specific conditional requirements still apply.
- Supported constraints include `minimum`, `exclusiveMinimum`, `maximum`, `enum`, string lengths, array sizes/items and object properties. Explicit object properties reject unknown fields. Follow the supplied release instead of adding unsupported JSON Schema keywords.
- Publish every declared output key after successful completion, normally with `PublishResultStage`. A key can contain null/empty data if its contract permits that; this is not an optional missing export. Add neither per-output `presence` nor `effects`/`group` metadata. `summary` complements the protocol's `description`.
- Keep scratchpad state private. Use declared child imports and `ctx.child_output`; read `outputs` in `result.json`. Operational provenance and restoration evidence belong in `run-manifest.json`, not the library `manifest.json`.
- Check the normalized outer reply status and any task-specific inner status before consuming device data. `RunSingleTaskStage` checks only the outer status by default.

Whole-value `"$shared.<path>"` references preserve JSON types; they are not interpolation or expressions. NodeEngine resolves shared references in effective stage parameters. Composition/publication/cleanup handlers also resolve `"$scratch.<path>"` at execution; a custom handler uses `ctx.get` for scratch data rather than assuming automatic scratch-reference resolution.

## 6. Generate a portable library

Keep the user's library separate from shipped built-in contracts and Open examples:

```text
MyLibrary/
  manifest.json
  MetaProtocolsDef/
    MY-PARENT/
      protocol.json
      Handlers.py
  MetaProtocolsRun/
    my-parent/
      input.json
  network.json
```

The manifest has `schemaVersion: "0.5"`, a `libraryId` and non-empty `metaProtocols`. Allowed optional fields are `description`, `domain`, `function` and `sharedHandlerFiles`. Each protocol entry contains `protocolId`, `definitionFile` and optional `handlerFiles`. Paths are relative, inside the library, and refer to existing JSON/Python files. For example, shared handlers can be declared as `"sharedHandlerFiles": ["Handlers.py"]`; that file must exist and its registered handlers must be used by the library.

The run plan uses `schemaVersion: "0.4"`, `metaProtocolLibrary` with the same `libraryId` and a `folder` resolved relative to the input file, plus an ordered `steps` list. In the layout above, the folder is `"../.."`. Manifest, run-plan and input/output schema versions are distinct. Use one JSON property per line and unique protocol/handler identifiers. Include a network example only when requested; preserve the user's verified network instead of inventing hardware values.

A step may have a unique `stepId` starting with a letter and then letters/digits/underscore/hyphen. Use `"$steps.<stepId>.<declaredExportPath>"` as an entire JSON value to import an earlier successfully completed step's declared output. Dictionary fields under declared object exports are accessible; array indexing, interpolation, expressions, self/forward references and missing-value fallback are unsupported. References can occur recursively in shared/common/stage overrides and resource entries. Preflight validates literal fields and source declarations; resolved destination inputs are validated again before submission. Top-level steps have independent leases.

## 7. Work in this order

1. Confirm sources and missing experiment information.
2. Present a concise composition: exact child IDs, effective inputs, imported outputs, resources, termination, actual timeout guards and final results. Explain necessary new handlers.
3. Generate the library and minimal run plan.
4. Check JSON syntax, paths/IDs, registrations, schema constraints, references, resources and child import/export mappings. Parse Python without executing handlers during this review.
5. Report checks performed, outcomes and unperformed checks. Syntax validation alone is not a runtime or hardware test.
6. Provide the launch command for the supplied distribution. Starting NodeEngine can initialize hardware; authoring and offline checks are not authorization to execute the experiment.

Use only existing documented validators and switches. Ask for the relevant runtime validation path if the supplied release does not provide an offline checker for the required behavior.

## 8. Final review

- Every built-in child is public and every Open child is registered in the loaded library.
- Inputs and imported paths match real contracts, including conditional requirements.
- New code serves a documented need and reuses existing operations.
- Physical values, detector-health policies, delegated leases and restoration are explicit.
- Successful publication contains every declared result; `run-manifest.json` records operational provenance.
- Deliver all necessary files, a minimal input, evidence of checks and unresolved values. No hardware run occurs as part of authoring.
