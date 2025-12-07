# Development Guide

This doc explains how to build and run the Online Boutique source code locally using the `skaffold` command-line tool.

## Prerequisites

- [Docker for Desktop](https://www.docker.com/products/docker-desktop)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (can be installed via `gcloud components install kubectl` for Option 1 - GKE)
- [skaffold **2.0.2+**](https://skaffold.dev/docs/install/) (latest version recommended), a tool that builds and deploys Docker images in bulk.
- Clone the repository.
    ```sh
    git clone https://github.com/GoogleCloudPlatform/microservices-demo
    cd microservices-demo/
    ```
- [Kind](https://kind.sigs.k8s.io/)

## Local Cluster

1. Launch a local Kubernetes cluster with one of the following tools:

    - To launch **Docker for Desktop** (tested with Windows). Go to Preferences:
        - choose “Enable Kubernetes”,
        - set CPUs to at least 3, and Memory to at least 6.0 GiB
        - on the "Disk" tab, set at least 32 GB disk space

    - To launch a **Kind** cluster:

      ```shell
      kind create cluster
      ```

2. Run `kubectl get nodes` to verify you're connected to the respective control plane.

3. Run `skaffold run` (first time will be slow, it can take ~20 minutes).
   This will build and deploy the application. If you need to rebuild the images
   automatically as you refactor the code, run `skaffold dev` command.

4. Run `kubectl get pods` to verify the Pods are ready and running.

5. Run `kubectl port-forward deployment/frontend 8080:8080` to forward a port to the frontend service.

6. Run `kubectl port-forward service/grafana 3000:3000` to forward a port to grafana.

7. Run `kubectl port-forward service/mailhog 8025:8025` to forward a port to mailhog.

8. Navigate to `localhost:8080` to access the web frontend.

9. Navigate to `localhost:3000` to acces grafana.

10. Navigate to `localhost:8025` to acces mailhog.

## Cleanup

If you've deployed the application with `skaffold run` command, you can run
`skaffold delete` to clean up the deployed resources.
