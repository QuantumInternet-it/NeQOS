"""Local editable handlers for the FAKE-HANDLER teaching protocol."""

from NodeEnginePack.NodeEngineAuxiliary import StageResult


def _task_failure(reply):
    task_result = reply.get("result") or {}
    if reply.get("status") != "OK" or task_result.get("status", "OK") != "OK":
        return StageResult(decision="fail", reason=str(
            reply.get("errorMessage") or "Fake device task did not complete successfully."))
    return None


async def FakePrepareStage(ctx, params):
    deviceId = str(params["deviceId"])
    gain = float(params.get("gain", 4.2))
    durationSec = float(params.get("durationSec", 1.0))
    reply = await ctx.run_task(deviceId, "SetGainTask", {"value": gain})
    failure = _task_failure(reply)
    if failure is not None:
        return failure
    reply = await ctx.run_task(
        deviceId,
        "ForegroundShortTask",
        {
            "durationSec": durationSec,
            "tickSec": float(params.get("tickSec", 0.5)),
        },
    )
    failure = _task_failure(reply)
    if failure is not None:
        return failure
    ctx.set("handler.deviceId", deviceId)
    ctx.set("handler.gain", gain)
    ctx.set("handler.durationSec", durationSec)
    return StageResult(decision="advance")


async def FakeRepeatShortCheckStage(ctx, params):
    reply = await ctx.run_task(
        str(params["deviceId"]),
        "ForegroundShortTask",
        {
            "durationSec": float(params.get("durationSec", 1.0)),
            "tickSec": float(params.get("tickSec", 0.5)),
        },
    )
    failure = _task_failure(reply)
    if failure is not None:
        return failure
    iteration = int(ctx.get("iteration", 0)) + 1
    ctx.set("iteration", iteration)
    ctx.set("handler.iterations", iteration)
    ctx.set("handler.status", str(reply.get("status") or "UNKNOWN"))
    return StageResult(decision="repeat" if iteration < int(params.get("maxIterations", 2)) else "advance")


HANDLERS = {
    "FakePrepareStage": FakePrepareStage,
    "FakeRepeatShortCheckStage": FakeRepeatShortCheckStage,
}
