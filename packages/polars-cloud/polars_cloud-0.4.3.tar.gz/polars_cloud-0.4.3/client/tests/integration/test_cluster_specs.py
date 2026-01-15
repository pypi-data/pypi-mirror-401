# mypy: disable-error-code="no-untyped-def"


import boto3
import pytest
from polars_cloud import ComputeContext

from .conftest import ComputeContextSpecsInput  # noqa: TID252


@pytest.mark.parametrize(
    "proxy_compute", [ComputeContextSpecsInput(cpus=2, memory=2)], indirect=True
)
def test_standard_instance_specs(proxy_compute: ComputeContext) -> None:
    ec2 = boto3.client("ec2")
    filters = [
        {"Name": "tag:PolarsClusterId", "Values": [str(proxy_compute._compute_id)]},
    ]
    response = ec2.describe_instances(Filters=filters)
    instance_types = set()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_types.add(instance["InstanceType"])
    assert len(instance_types) == 1

    response = ec2.describe_instance_types(InstanceTypes=list(instance_types))
    for instance_type in response["InstanceTypes"]:
        assert instance_type["VCpuInfo"]["DefaultVCpus"] >= 2
        assert instance_type["MemoryInfo"]["SizeInMiB"] >= 2048


# @pytest.mark.parametrize(
#     "proxy_compute",
#     [ComputeContextSpecsInput(cpus=2, memory=2,
#                               big_instance_multiplier=2, cluster_size=2)],
#     indirect=True,
# )
# def test_big_instance_specs(proxy_compute: ComputeContext) -> None:
#     ec2 = boto3.client("ec2")
#     filters = [
#         {"Name": "tag:PolarsClusterId", "Values": [str(proxy_compute._compute_id)]},
#     ]
#     response = ec2.describe_instances(Filters=filters)
#     instance_types = []
#     for reservation in response["Reservations"]:
#         for instance in reservation["Instances"]:
#             instance_types.append(instance["InstanceType"])
#     assert len(instance_types) == 2
#
#     response = ec2.describe_instance_types(InstanceTypes=instance_types)
#     assert len(response["InstanceTypes"]) == 2
#     sorted(response["InstanceTypes"], key=lambda x: x["VCpuInfo"]["DefaultVCpus"])
#
#     assert response["InstanceTypes"][0]["VCpuInfo"]["DefaultVCpus"] >= 2
#     assert response["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"] >= 2048
#
#     assert response["InstanceTypes"][1]["VCpuInfo"]["DefaultVCpus"] >= 2
#     assert response["InstanceTypes"][1]["MemoryInfo"]["SizeInMiB"] >= 4096


@pytest.mark.parametrize(
    "proxy_compute", [ComputeContextSpecsInput(instance_type="t3.micro")], indirect=True
)
def test_standard_instance_type(proxy_compute: ComputeContext) -> None:
    ec2 = boto3.client("ec2")
    filters = [
        {"Name": "tag:PolarsClusterId", "Values": [str(proxy_compute._compute_id)]},
    ]
    response = ec2.describe_instances(Filters=filters)
    instance_types = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_types.append(instance["InstanceType"])
    assert len(instance_types) == 1
    assert instance_types[0] == "t3.micro"


# @pytest.mark.parametrize(
#     "proxy_compute",
#     [
#         ComputeContextSpecsInput(
#             instance_type="t3.micro", big_instance_type="t3.small", cluster_size=2
#         )
#     ],
#     indirect=True,
# )
# def test_big_instance_type(proxy_compute: ComputeContext) -> None:
#     ec2 = boto3.client("ec2")
#     filters = [
#         {"Name": "tag:PolarsClusterId", "Values": [str(proxy_compute._compute_id)]},
#     ]
#     response = ec2.describe_instances(Filters=filters)
#     instance_types = []
#     for reservation in response["Reservations"]:
#         for instance in reservation["Instances"]:
#             instance_types.append(instance["InstanceType"])
#     assert len(instance_types) == 2
#     assert "t3.small" in instance_types
#     assert "t3.micro" in instance_types
