import re
from datetime import timedelta
from functools import partial
from subprocess import run

from flytekit import WorkflowExecutionPhase

_run = partial(run, check=True, capture_output=True, text=True)


def test_hello_world(workflows_dir, remote, config_path):
    """Check simple hello world example.

    1. Run hello_world.py
    2. Checks output is i + 1
    """
    result = _run(
        [
            "union",
            "--config",
            config_path,
            "run",
            "--remote",
            "hello_world.py",
            "main",
            "--i",
            "10",
        ],
        cwd=workflows_dir,
    )
    match = re.search(r"executions/(\w+)", result.stdout)

    execution_id = match.group(1)
    ex1 = remote.fetch_execution(name=execution_id)
    ex1 = remote.wait(ex1, poll_interval=timedelta(seconds=1))
    assert ex1.closure.phase == WorkflowExecutionPhase.SUCCEEDED
    assert ex1.outputs["o0"] == 11
