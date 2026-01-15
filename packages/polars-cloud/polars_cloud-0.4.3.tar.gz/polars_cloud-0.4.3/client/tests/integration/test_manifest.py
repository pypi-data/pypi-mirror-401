# mypy: disable-error-code="no-untyped-def"
import random
import string

import pytest
from polars_cloud import ComputeContext, Workspace
from polars_cloud.polars_cloud import NotFoundError


def test_register_and_start(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    ctx_from_name.start(wait=True)
    assert ctx_from_name.instance_type == "t3.micro"
    ctx_from_name.stop()


def test_register_upsert(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    ctx2 = ComputeContext(workspace=workspace, instance_type="t3.small")
    ctx2.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    assert ctx_from_name.instance_type == "t3.small"


def test_register_and_unregister(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    ctx_from_name.unregister()

    with pytest.raises(NotFoundError):
        ctx_from_name = ComputeContext(workspace=workspace, name=name)
