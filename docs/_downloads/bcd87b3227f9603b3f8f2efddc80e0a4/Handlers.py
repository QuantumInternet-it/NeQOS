"""Sweep handlers for the FAKE-COMPOSED-SWEEP-BRANCH meta-protocol."""

from NodeEnginePack.NodeEngineAuxiliary import StageResult


def _positiveInt(value, fieldName):
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{fieldName} must be an integer.") from exc
    if parsed < 1:
        raise ValueError(f"{fieldName} must be >= 1.")
    return parsed


async def FakeComposedSweepSubmitStage(ctx, params):
    """Submit all leaf runs from one parent stage, producing S01/N01..Nxx."""
    templateId = str(params.get("templateId") or "").strip()
    if not templateId:
        return StageResult(decision="fail", reason="Missing templateId for test sweep.")
    try:
        count = _positiveInt(params.get("count", 0), "count")
        valueStart = int(params.get("valueStart", 0))
    except ValueError as exc:
        return StageResult(decision="fail", reason=str(exc))
    childRuns = []
    for iteration in range(1, count + 1):
        childRuns.append(ctx.submit_microprotocol(templateId, sharedParamOverrides={"iteration": iteration, "value": valueStart + iteration - 1, "fakeDeviceId": params.get("fakeDeviceId"), "fakeTaskDurationSec": params.get("fakeTaskDurationSec")}))
    ctx.set("test.childRuns", childRuns)
    ctx.set("test.expectedCount", count)
    return StageResult(decision="advance")


async def FakeComposedSweepWaitStage(ctx, params):
    """Wait for all leaf runs and aggregate their exported values in order."""
    childRuns = list(ctx.get("test.childRuns") or [])
    expectedCount = int(ctx.get("test.expectedCount") or 0)
    if not childRuns or len(childRuns) != expectedCount:
        return StageResult(decision="fail", reason="Test sweep has no complete child-run list.")
    for runtimeId in childRuns:
        if ctx.microprotocol_failed(runtimeId):
            return StageResult(decision="fail", reason=f"Leaf child {runtimeId!r} failed.")
    if not all(ctx.microprotocol_succeeded(runtimeId) for runtimeId in childRuns):
        return StageResult(decision="requeue", delaySec=float(params.get("pollDelaySec", 0.01)))
    values = []
    for runtimeId in childRuns:
        child = ctx.nodeEngine.microProtocolInstances.get(runtimeId)
        exports = dict(getattr(child, "metadata", {}).get("exports") or {})
        leaf = dict(dict(exports.get("test") or {}).get("leaf") or {})
        if "iteration" not in leaf or "value" not in leaf:
            return StageResult(decision="fail", reason=f"Leaf child {runtimeId!r} did not export test.leaf.")
        values.append(leaf)
    ctx.set("test.sweep", {"childRunIds": childRuns, "count": len(values), "values": values})
    return StageResult(decision="advance")


HANDLERS = {
    "FakeComposedSweepSubmitStage": FakeComposedSweepSubmitStage,
    "FakeComposedSweepWaitStage": FakeComposedSweepWaitStage,
}
