import os
import json
import time
import urllib3

from typing import  Annotated
from uuid import uuid4
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

def get_resources(
        resource: str,
        name: str,
        namespace: str,
        cluster: str
) -> str:
    """
    Get Kubernetes resources on the managed cluster.

    Args:
        resource: the name of the Kubernetes resource you want to get or list
        name: the instance name of the kubernetes resource you want to get, will list all instances of the resource if the name is empty
        namespace: the namespace where the resource is in, could be empty for All namespaces
        cluster: the managed cluster where you want to get or list the resource from
    """

    # Validate required inputs
    if not resource:
        raise ValueError("the resource cannot be empty ")
    if not cluster:
        raise ValueError("the cluster cannot be empty ")

    # Generate a random name for the ManagedClusterView CR
    cr_name = f"search-bot-{uuid4().hex[:5]}"

    # Define the ManagedClusterView CR
    cr_body = {
        "apiVersion": "view.open-cluster-management.io/v1beta1",
        "kind": "ManagedClusterView",
        "metadata": {
            "name": cr_name,
            "namespace": cluster
        },
        "spec": {
            "scope": {
                "resource": resource,
                "name": name,
                "namespace": namespace
            }
        }
    }

    # Load kubeconfig from environment variable
    kubeconfig_path = os.getenv("KUBECONFIG")
    if not kubeconfig_path:
        raise ValueError("KUBECONFIG environment variable not set")
    config.load_kube_config(kubeconfig_path)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    api = client.CustomObjectsApi()

    # Create the ManagedClusterView CR
    try:
        api.create_namespaced_custom_object(
            group="view.open-cluster-management.io",
            version="v1beta1",
            namespace=cluster,
            plural="managedclusterviews",
            body=cr_body
        )
    except ApiException as e:
        raise ValueError("failed to get resource: ", str(e))

    # Wait for the status to be populated
    result = {}
    max_wait_seconds = 10
    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        try:
            cr = api.get_namespaced_custom_object(
                group="view.open-cluster-management.io",
                version="v1beta1",
                namespace=cluster,
                plural="managedclusterviews",
                name=cr_name
            )
            current_status = cr.get("status", {})
            if current_status.get("conditions"):
                result = current_status.get("result", {})
                break
            time.sleep(2)
        except ApiException as e:
            if e.status == 404:
                time.sleep(2)
                continue
            else:
                raise ValueError("failed to get resource: ", str(e))

    # Clean up the created CR
    try:
        api.delete_namespaced_custom_object(
            group="view.open-cluster-management.io",
            version="v1beta1",
            namespace=cluster,
            plural="managedclusterviews",
            name=cr_name
        )
    except ApiException as e:
        raise ValueError("failed to delete mcv: ", str(e))

    return json.dumps(result,indent=2,sort_keys=True)



@tool
def get_resources_tool(
        resource: Annotated[str, "the resource is the name of kubernetes resource you want to get or list"],
        name: Annotated[str, "The name is the instance name of the kubernetes resource you want to get, will list all instances of the resource if the name is empty "],
        namespace: Annotated[str, "The namespace where the resource is in"],
        cluster: Annotated[str, "The managed cluster where you want to get or list the resource from"]
):
    """Get the list of resources from the provided resource, name, namespace, cluster"""
    return get_resources(resource, name, namespace, cluster)


search_tools = [get_resources_tool]

search_tools_node = ToolNode(search_tools)
