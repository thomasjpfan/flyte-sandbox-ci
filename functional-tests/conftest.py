import os
from pathlib import Path
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config

import pytest


@pytest.fixture(scope="session")
def remote() -> FlyteRemote:
    return FlyteRemote(
        Config.for_sandbox(),
        default_project="flytesnacks",
        default_domain="development",
    )


@pytest.fixture(scope="session")
def workflows_dir() -> Path:
    return Path(__file__).parent / "workflows"


@pytest.fixture(scope="session")
def config_path() -> str:
    sandbox_path = Path(__file__).parent / "sandbox-yaml.yaml"
    return os.fspath(sandbox_path.resolve())
