"""Open handler used only to test an external Python-package import."""

import humanize


async def ExternalPythonPackageDependencyHumanizeStage(ctx, params):
    """Format an integer through the externally installed ``humanize`` package."""
    value = int(params["value"])
    formatted_value = humanize.intcomma(value)
    ctx.set("externalPythonPackageDependency.formattedValue", formatted_value)
    print(
        f"[ExternalPythonPackageDependency] humanize import succeeded: {formatted_value}",
        flush=True,
    )
    return "advance"


HANDLERS = {
    "ExternalPythonPackageDependencyHumanizeStage": ExternalPythonPackageDependencyHumanizeStage,
}
