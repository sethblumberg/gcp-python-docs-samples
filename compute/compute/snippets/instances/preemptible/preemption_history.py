#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa


# This file is automatically generated. Please do not modify it directly.
# Find the relevant recipe file in the samples/recipes or samples/ingredients
# directory and apply your changes there.


# [START compute_preemptible_history]
import datetime
from typing import List, Tuple

from google.cloud import compute_v1
from google.cloud.compute_v1.services.zone_operations import pagers


def list_zone_operations(
    project_id: str, zone: str, filter: str = ""
) -> pagers.ListPager:
    """
    List all recent operations the happened in given zone in a project. Optionally filter those
    operations by providing a filter. More about using the filter can be found here:
    https://cloud.google.com/compute/docs/reference/rest/v1/zoneOperations/list
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        filter: filter string to be used for this listing operation.
    Returns:
        List of preemption operations in given zone.
    """
    operation_client = compute_v1.ZoneOperationsClient()
    request = compute_v1.ListZoneOperationsRequest()
    request.project = project_id
    request.zone = zone
    request.filter = filter

    return operation_client.list(request)


def preemption_history(
    project_id: str, zone: str, instance_name: str = None
) -> List[Tuple[str, datetime.datetime]]:
    """
    Get a list of preemption operations from given zone in a project. Optionally limit
    the results to instance name.
    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        instance_name: name of the virtual machine to look for.
    Returns:
        List of preemption operations in given zone.
    """
    if instance_name:
        filter = (
            f'operationType="compute.instances.preempted" '
            f"AND targetLink:instances/{instance_name}"
        )
    else:
        filter = 'operationType="compute.instances.preempted"'

    history = []

    for operation in list_zone_operations(project_id, zone, filter):
        this_instance_name = operation.target_link.rsplit("/", maxsplit=1)[1]
        if instance_name and this_instance_name == instance_name:
            # The filter used is not 100% accurate, it's `contains` not `equals`
            # So we need to check the name to make sure it's the one we want.
            moment = datetime.datetime.fromisoformat(operation.insert_time)
            history.append((instance_name, moment))

    return history


# [END compute_preemptible_history]