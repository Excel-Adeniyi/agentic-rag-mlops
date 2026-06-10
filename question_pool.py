SIMPLE_QUERIES = [
    {
        "query": "What command lists all running pods in Kubernetes?",
        "ground_truth": "kubectl get pods"
    },
    {
        "query": "How do I view logs for a Docker container?",
        "ground_truth": "docker logs <container-id>"
    },
    {
        "query": "What command checks the status of a Kubernetes deployment?",
        "ground_truth": "kubectl rollout status deployment/<deployment-name>"
    },
    {
        "query": "How do I stop a running Docker container?",
        "ground_truth": "docker stop <container-id>"
    },
    {
        "query": "What is the default port Jenkins runs on?",
        "ground_truth": "Port 8080"
    },
    {
        "query": "How do I list all Kubernetes namespaces?",
        "ground_truth": "kubectl get namespaces"
    },
    {
        "query": "What command pulls a Docker image from a registry?",
        "ground_truth": "docker pull <image-name>"
    },
    {
        "query": "How do I restart a Kubernetes deployment?",
        "ground_truth": "kubectl rollout restart deployment/<deployment-name>"
    },
    {
        "query": "What command shows all Docker images on my machine?",
        "ground_truth": "docker images"
    },
    {
        "query": "How do I delete a Kubernetes pod?",
        "ground_truth": "kubectl delete pod <pod-name>"
    },
]

SYMPTOM_QUERIES = [
    {
        "query": "My pod keeps crashing, what should I do?",
        "ground_truth": "Check logs using kubectl logs <pod-name> and inspect events using kubectl describe pod <pod-name> to identify the root cause"
    },
    {
        "query": "My Docker container exits immediately after starting, what is wrong?",
        "ground_truth": "Check container logs using docker logs <container-id> to identify the error causing the immediate exit"
    },
    {
        "query": "My Kubernetes deployment is not updating after I made changes, what should I do?",
        "ground_truth": "Use kubectl rollout restart deployment/<name> to force a new rollout or check rollout status with kubectl rollout status deployment/<name>"
    },
    {
        "query": "My Jenkins pipeline is failing but I do not know why, how do I investigate?",
        "ground_truth": "Check the Jenkins console output by clicking the build number and selecting Console Output to find the specific error"
    },
    {
        "query": "My Kubernetes pod is stuck in pending state, what should I do?",
        "ground_truth": "Use kubectl describe pod <pod-name> to check events and identify whether the issue is insufficient resources or scheduling constraints"
    },
    {
        "query": "I cannot connect to my Docker container from outside, what is wrong?",
        "ground_truth": "Check that the container port is correctly mapped to the host using docker ps and verify the port mapping with -p flag"
    },
    {
        "query": "My Kubernetes nodes are not ready, how do I investigate?",
        "ground_truth": "Use kubectl get nodes to check node status and kubectl describe node <node-name> to see events and conditions"
    },
    {
        "query": "My Docker image build is failing, what should I check?",
        "ground_truth": "Check the Dockerfile for syntax errors and verify all referenced files exist. Review the build output for the specific step that failed"
    },
    {
        "query": "My Jenkins build works locally but fails in the pipeline, what should I check?",
        "ground_truth": "Check environment variables and tool versions on the Jenkins agent using sh env in your pipeline to print all environment variables"
    },
    {
        "query": "My Kubernetes deployment has zero available pods, what is wrong?",
        "ground_truth": "Use kubectl get pods to check pod status and kubectl describe deployment <name> to check deployment conditions and events"
    },
]

COMPARATIVE_QUERIES = [
    {
        "query": "What is the difference between a namespace and a deployment in Kubernetes?",
        "ground_truth": "A namespace provides a scope for resource names and isolates resources between teams or projects. A deployment manages the desired state and rollout of application pods ensuring the correct number of replicas are running"
    },
    {
        "query": "What is the difference between a pod and a container in Kubernetes?",
        "ground_truth": "A container is a single running process. A pod is the smallest deployable unit in Kubernetes and can contain one or more containers that share network and storage resources"
    },
    {
        "query": "What is the difference between docker run and docker start?",
        "ground_truth": "docker run creates and starts a new container from an image. docker start restarts an existing stopped container without creating a new one"
    },
    {
        "query": "What is the difference between a Kubernetes deployment and a statefulset?",
        "ground_truth": "A deployment manages stateless applications where pods are interchangeable. A statefulset manages stateful applications where each pod has a persistent identity and stable storage"
    },
    {
        "query": "What is the difference between docker copy and docker volume?",
        "ground_truth": "docker copy transfers files between a container and the host at a specific point in time. A volume provides persistent shared storage that persists beyond the container lifecycle"
    },
    {
        "query": "What is the difference between a Jenkins declarative and scripted pipeline?",
        "ground_truth": "A declarative pipeline uses a structured predefined syntax that is easier to read and validate. A scripted pipeline uses Groovy code giving more flexibility but requiring more expertise"
    },
    {
        "query": "What is the difference between kubectl apply and kubectl create?",
        "ground_truth": "kubectl create creates a new resource and fails if it already exists. kubectl apply creates or updates a resource and is idempotent making it better for declarative configuration management"
    },
    {
        "query": "What is the difference between a Kubernetes service and an ingress?",
        "ground_truth": "A service exposes pods internally within the cluster or externally on a specific port. An ingress manages external HTTP and HTTPS routing to multiple services based on rules"
    },
    {
        "query": "What is the difference between docker compose and Kubernetes?",
        "ground_truth": "Docker Compose defines and runs multi-container applications on a single host for development. Kubernetes orchestrates containers across multiple nodes in production with scaling, self-healing and service discovery"
    },
    {
        "query": "What is the difference between a Jenkins stage and a step?",
        "ground_truth": "A stage groups related steps together and appears as a distinct block in the Jenkins UI. A step is an individual command or action within a stage such as running a shell command or checking out code"
    },
]

# Combined list for running full evaluation
ALL_QUERIES = SIMPLE_QUERIES + SYMPTOM_QUERIES + COMPARATIVE_QUERIES