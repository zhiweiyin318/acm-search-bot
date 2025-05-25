from model import get_model
from langchain_core.messages import SystemMessage,HumanMessage
from agents.parser import  system_message
from agents.acm_tools import get_resources

def test_search_parser():
    test_cases = [
        "get the pod mypod in the default namespace on the cluster cluster2",
        "get the namespace default on the cluster dev",
        "get the namespace open-cluster-management on local-cluster",
        "get all namespace on qe",
        "get the deployments in the system namespace on test",
        "get klusterlet on the cluster abc",
        "on the cluster abc, get all klusterlets",
        "get klusterlets klusterlet on the cluster product",
        "get configmaps in the open-cluster-management namespace from the dev",
        "get configmaps on dev",
        "get configmaps on cluster dev"
    ]

    model = get_model()
    for case in test_cases:
        result = model.invoke(
            [
                SystemMessage(content=system_message),
                HumanMessage(content=case)
            ]
        )
        print(f"Input: {case}")
        print(f"Output: {result.content}\n")



def test_get_resources():
    test_cases = [
        {"resource": "deployments", "name": "", "namespace": "", "cluster": "cluster1"}
    ]

    for case in test_cases:
        result = get_resources(case["resource"], case["name"], case["namespace"], case["cluster"])
        print(f"Input: {case}")
        print(f"Output: {result}\n")


if __name__ == "__main__":
    test_get_resources()