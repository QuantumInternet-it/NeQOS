"""Local editable handlers for the FAKE-HANDLER teaching protocol."""


async def FakePrepareStage(ctx, params):
    deviceId = str(params["deviceId"])
    gain = float(params.get("gain", 4.2))
    durationSec = float(params.get("durationSec", 1.0))
    await ctx.run_task(deviceId, "SetGainTask", {"value": gain})
    await ctx.run_task(
        deviceId,
        "ForegroundShortTask",
        {
            "durationSec": durationSec,
            "tickSec": float(params.get("tickSec", 0.5)),
        },
    )
    ctx.set("handler.deviceId", deviceId)
    ctx.set("handler.gain", gain)
    ctx.set("handler.durationSec", durationSec)
    return "advance"


async def FakeRepeatShortCheckStage(ctx, params):
    reply = await ctx.run_task(
        str(params["deviceId"]),
        "ForegroundShortTask",
        {
            "durationSec": float(params.get("durationSec", 1.0)),
            "tickSec": float(params.get("tickSec", 0.5)),
        },
    )
    iteration = int(ctx.get("iteration", 0)) + 1
    ctx.set("iteration", iteration)
    ctx.set("handler.iterations", iteration)
    ctx.set("handler.status", str(reply.get("status") or "UNKNOWN"))
    return "repeat" if iteration < int(params.get("maxIterations", 2)) else "advance"


HANDLERS = {
    "FakePrepareStage": FakePrepareStage,
    "FakeRepeatShortCheckStage": FakeRepeatShortCheckStage,
}
