"""Leaf-value handler for the FAKE-COMPOSED-SWEEP fake-device protocol."""

from NodeEnginePack.NodeEngineAuxiliary import StageResult


async def FakeComposedSweepProduceValueStage(ctx, params):
    """Produce a deterministic leaf export without communicating with hardware."""
    try:
        iteration = int(params.get("iteration", 0))
    except (TypeError, ValueError):
        return StageResult(decision="fail", reason="iteration must be an integer.")
    if iteration < 1:
        return StageResult(decision="fail", reason="iteration must be >= 1.")
    ctx.set("test.leaf", {"iteration": iteration, "value": params.get("value")})
    return StageResult(decision="advance")


HANDLERS = {"FakeComposedSweepProduceValueStage": FakeComposedSweepProduceValueStage}
