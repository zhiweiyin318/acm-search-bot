# ACM AI Search Bot

This project implements a simple AI Search Bot prototype for ACM.

You can use common language to get or list the resources on the managed cluster from the Hub cluster.

## Demo

![demo GIF "how to search resources on the managed cluster"](./.github/demo.gif)

## How to run

### Requirements 

* Install and start ollama on your host.

* Set your model in the model.py file for ollama.

* Set the KUBECONFIG env
  ```bash
  export KUBECONFIG=<your hub cluster kubeconfig>
  ```

* Only support to get the specified resource by default. Need to override the test image if support to list the resources.
The steps to override the images:
  1. pause the mce:
    ```bash
    oc annotate mce multiclusterengine pause=true
    ```
  2. Replace the `agent-addon-image` to `quay.io/zhiweiyin/test:viewlist` in the ocm-controller deployment in the multicluster-engine ns.
    
### Run
```bash
    python3 -m venv venv
    source env/bin/activate
    pip install -r requirements.txt
    python3 search.py
```

## TODO

* support to get the pod log
    ```
    * get the logs of pod klusterlet-78c767d9d5-24ssk in the open-cluster-management-agent namespace on the cluster1
    ```

* support to get the field of a resource
    ```
    * get the conditon of klusterlets klusterlet on the cluster1
    ```
* support label selector, CEL
    ```
    * get the clusterclaims on the cluster1 with the label open-cluster-management.io/spoke-only=
    ```

* support to search resources on the Hub cluster
    
* save chat history, for example 
    ```
    * log in to cluster1
    * list the pods on open-cluster-management-agent namespace
    * get the depolyment 
    * log out
    * log in to cluster2
    * get the pod on open-cluster-management namespace
    ```

* more complex tasks
    ```
    * get the logs of pods in open-cluster-management-agent namespace with the label app=klusterlet
    * get the CrashLoopbackoff pods in the open-cluster-management-agent-addon namespace
    ```

* use the cluster-proxy and serviceAccount as the backend

* containerized the ollama with a small model and the search bot service.

* deploy the search bot as an addon on the ACM.

* integrate the bot into clusteradm in the OCM community.
