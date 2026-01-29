"""
Service location utilities for SCP applications.
"""
from kubernetes import client as kubernetes_client, config as kubernetes_config
from scp.app.sdk.scripts.user import get_env_variable

def studio_url(studio_id: str, private_routing: bool = True ) -> str|None:
    """
    Get the URL for a specific studio.

    Args:
        studio_id (str): The unique identifier for the studio.
        private_routing (bool): Whether to use private routing (ingress).

    Returns:
        str: The URL of the studio.
    """
    return locate_service(
        f"{studio_id}.studios",
        'studios',
        private_routing,
        port=443 if private_routing else 3333
    )


def voicebot_url() -> str:
    """
    Get the URL for the voicebot service.

    Returns:
        str: The URL of the voicebot service.
    """
    return locate_service(
        "service",
        "voicebot",
        private_routing=False,
        port=3000
    )


def locate_service(
    service: str,
    stack: str,
    private_routing: bool = True,
    port: int|None = None
) -> str:
    """
    Locate a service within the Kubernetes environment.

    Args:
        service (str): The name of the service to locate.
        stack (str|None): The stack the service belongs to.
        private_routing (bool): Whether to use private routing.
        port (int|None): The port number to access the service.

    Returns:
        str: The URL of the located service.
    """
    kubernetes_environment=get_env_variable('APP_STORE_KUBERNETES_ENVIRONMENT')
    if private_routing:
        return _get_ingress_for_service(f"{kubernetes_environment}-{stack}", service, port)
    port_suffix = f":{port}" if port is not None else ""
    return f"http://{service}.{kubernetes_environment}-{stack}.svc.cluster.local{port_suffix}"

def _get_ingress_for_service(namespace: str, service: str, port: int|None = None) -> str:
    """
    Get the ingress URL for a service in a specific namespace.

    Args:
        namespace (str): The Kubernetes namespace to search in.
        service (str): The name of the service to find.
        port (int|None): The port number of the service.
    """
    ingress_hosts = _list_namespaced_ingress_hosts_for_service_with_label(namespace, service, port)
    if not ingress_hosts:
        ingress_hosts = _list_namespaced_ingress_hosts_for_service(namespace, service, port)
    if not ingress_hosts:
        raise ValueError(
            f"No ingress found for service {service} in namespace {namespace} on port {port}"
        )
    return f"https://{ingress_hosts.pop()}"

def _list_namespaced_ingress_hosts_for_service_with_label(namespace: str, service: str, port: int|None = None)\
    -> list[str]:
    """
    List all ingress hosts for a specific service in a namespace,
    with ingress label app.kubernetes.io/name the service name

    Args:
        namespace (str): The Kubernetes namespace to search in.
        service (str): The name of the service to find.
        port (int|None): The port number of the service.
    """
    _load_kubernetes_config()
    result: list[str] = []
    with kubernetes_client.ApiClient() as api_client:
        api_instance = kubernetes_client.NetworkingV1Api(api_client)
        ingress_res = api_instance.list_namespaced_ingress(namespace, label_selector=f"app.kubernetes.io/name={service}") # type: ignore[attr-defined]
        for ingress_item in [i for i in ingress_res.items if i.spec.rules]:
            for ingress_rule in ingress_item.spec.rules:
                for path in ingress_rule.http.paths:
                    if path.backend.service.name==service:
                        if port is None or path.backend.service.port.number==port:
                            result.append(ingress_rule.host)
    return result

def _list_namespaced_ingress_hosts_for_service(namespace: str, service: str, port: int|None = None)\
    -> list[str]:
    """ 
    List all ingress hosts for a specific service in a namespace.

    Args:
        namespace (str): The Kubernetes namespace to search in.
        service (str): The name of the service to find.
        port (int|None): The port number of the service.
    """
    _load_kubernetes_config()
    result: list[str] = []
    with kubernetes_client.ApiClient() as api_client:
        api_instance = kubernetes_client.NetworkingV1Api(api_client)
        ingress_res = api_instance.list_namespaced_ingress(namespace) # type: ignore[attr-defined]
        for ingress_item in [i for i in ingress_res.items if i.spec.rules]:
            for ingress_rule in ingress_item.spec.rules:
                for path in ingress_rule.http.paths:
                    if path.backend.service.name==service:
                        if port is None or path.backend.service.port.number==port:
                            result.append(ingress_rule.host)
    return result

def _load_kubernetes_config() -> None:
    """
    Load the Kubernetes configuration.

    Attempts to load in-cluster configuration first; if that fails, it loads the kubeconfig file.
    (this is useful for local/minikube testing)
    """
    try:
        kubernetes_config.load_incluster_config()
    except kubernetes_config.ConfigException:
        kubernetes_config.load_kube_config()
