import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktn-provider-kubernetes",
    "version": "12.2.0",
    "description": "Prebuilt kubernetes Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktn-io/cdktn-provider-kubernetes.git",
    "long_description_content_type": "text/markdown",
    "author": "CDK Terrain Maintainers",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktn-io/cdktn-provider-kubernetes.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktn_provider_kubernetes",
        "cdktn_provider_kubernetes._jsii",
        "cdktn_provider_kubernetes.annotations",
        "cdktn_provider_kubernetes.api_service",
        "cdktn_provider_kubernetes.api_service_v1",
        "cdktn_provider_kubernetes.certificate_signing_request",
        "cdktn_provider_kubernetes.certificate_signing_request_v1",
        "cdktn_provider_kubernetes.cluster_role",
        "cdktn_provider_kubernetes.cluster_role_binding",
        "cdktn_provider_kubernetes.cluster_role_binding_v1",
        "cdktn_provider_kubernetes.cluster_role_v1",
        "cdktn_provider_kubernetes.config_map",
        "cdktn_provider_kubernetes.config_map_v1",
        "cdktn_provider_kubernetes.config_map_v1_data",
        "cdktn_provider_kubernetes.cron_job",
        "cdktn_provider_kubernetes.cron_job_v1",
        "cdktn_provider_kubernetes.csi_driver",
        "cdktn_provider_kubernetes.csi_driver_v1",
        "cdktn_provider_kubernetes.daemon_set_v1",
        "cdktn_provider_kubernetes.daemonset",
        "cdktn_provider_kubernetes.data_kubernetes_all_namespaces",
        "cdktn_provider_kubernetes.data_kubernetes_config_map",
        "cdktn_provider_kubernetes.data_kubernetes_config_map_v1",
        "cdktn_provider_kubernetes.data_kubernetes_endpoints_v1",
        "cdktn_provider_kubernetes.data_kubernetes_ingress",
        "cdktn_provider_kubernetes.data_kubernetes_ingress_v1",
        "cdktn_provider_kubernetes.data_kubernetes_mutating_webhook_configuration_v1",
        "cdktn_provider_kubernetes.data_kubernetes_namespace",
        "cdktn_provider_kubernetes.data_kubernetes_namespace_v1",
        "cdktn_provider_kubernetes.data_kubernetes_nodes",
        "cdktn_provider_kubernetes.data_kubernetes_persistent_volume_claim",
        "cdktn_provider_kubernetes.data_kubernetes_persistent_volume_claim_v1",
        "cdktn_provider_kubernetes.data_kubernetes_persistent_volume_v1",
        "cdktn_provider_kubernetes.data_kubernetes_pod",
        "cdktn_provider_kubernetes.data_kubernetes_pod_v1",
        "cdktn_provider_kubernetes.data_kubernetes_resource",
        "cdktn_provider_kubernetes.data_kubernetes_resources",
        "cdktn_provider_kubernetes.data_kubernetes_secret",
        "cdktn_provider_kubernetes.data_kubernetes_secret_v1",
        "cdktn_provider_kubernetes.data_kubernetes_server_version",
        "cdktn_provider_kubernetes.data_kubernetes_service",
        "cdktn_provider_kubernetes.data_kubernetes_service_account",
        "cdktn_provider_kubernetes.data_kubernetes_service_account_v1",
        "cdktn_provider_kubernetes.data_kubernetes_service_v1",
        "cdktn_provider_kubernetes.data_kubernetes_storage_class",
        "cdktn_provider_kubernetes.data_kubernetes_storage_class_v1",
        "cdktn_provider_kubernetes.default_service_account",
        "cdktn_provider_kubernetes.default_service_account_v1",
        "cdktn_provider_kubernetes.deployment",
        "cdktn_provider_kubernetes.deployment_v1",
        "cdktn_provider_kubernetes.endpoint_slice_v1",
        "cdktn_provider_kubernetes.endpoints",
        "cdktn_provider_kubernetes.endpoints_v1",
        "cdktn_provider_kubernetes.env",
        "cdktn_provider_kubernetes.horizontal_pod_autoscaler",
        "cdktn_provider_kubernetes.horizontal_pod_autoscaler_v1",
        "cdktn_provider_kubernetes.horizontal_pod_autoscaler_v2",
        "cdktn_provider_kubernetes.horizontal_pod_autoscaler_v2_beta2",
        "cdktn_provider_kubernetes.ingress",
        "cdktn_provider_kubernetes.ingress_class",
        "cdktn_provider_kubernetes.ingress_class_v1",
        "cdktn_provider_kubernetes.ingress_v1",
        "cdktn_provider_kubernetes.job",
        "cdktn_provider_kubernetes.job_v1",
        "cdktn_provider_kubernetes.labels",
        "cdktn_provider_kubernetes.limit_range",
        "cdktn_provider_kubernetes.limit_range_v1",
        "cdktn_provider_kubernetes.manifest",
        "cdktn_provider_kubernetes.mutating_webhook_configuration",
        "cdktn_provider_kubernetes.mutating_webhook_configuration_v1",
        "cdktn_provider_kubernetes.namespace",
        "cdktn_provider_kubernetes.namespace_v1",
        "cdktn_provider_kubernetes.network_policy",
        "cdktn_provider_kubernetes.network_policy_v1",
        "cdktn_provider_kubernetes.node_taint",
        "cdktn_provider_kubernetes.persistent_volume",
        "cdktn_provider_kubernetes.persistent_volume_claim",
        "cdktn_provider_kubernetes.persistent_volume_claim_v1",
        "cdktn_provider_kubernetes.persistent_volume_v1",
        "cdktn_provider_kubernetes.pod",
        "cdktn_provider_kubernetes.pod_disruption_budget",
        "cdktn_provider_kubernetes.pod_disruption_budget_v1",
        "cdktn_provider_kubernetes.pod_security_policy",
        "cdktn_provider_kubernetes.pod_security_policy_v1_beta1",
        "cdktn_provider_kubernetes.pod_v1",
        "cdktn_provider_kubernetes.priority_class",
        "cdktn_provider_kubernetes.priority_class_v1",
        "cdktn_provider_kubernetes.provider",
        "cdktn_provider_kubernetes.replication_controller",
        "cdktn_provider_kubernetes.replication_controller_v1",
        "cdktn_provider_kubernetes.resource_quota",
        "cdktn_provider_kubernetes.resource_quota_v1",
        "cdktn_provider_kubernetes.role",
        "cdktn_provider_kubernetes.role_binding",
        "cdktn_provider_kubernetes.role_binding_v1",
        "cdktn_provider_kubernetes.role_v1",
        "cdktn_provider_kubernetes.runtime_class_v1",
        "cdktn_provider_kubernetes.secret",
        "cdktn_provider_kubernetes.secret_v1",
        "cdktn_provider_kubernetes.secret_v1_data",
        "cdktn_provider_kubernetes.service",
        "cdktn_provider_kubernetes.service_account",
        "cdktn_provider_kubernetes.service_account_v1",
        "cdktn_provider_kubernetes.service_v1",
        "cdktn_provider_kubernetes.stateful_set",
        "cdktn_provider_kubernetes.stateful_set_v1",
        "cdktn_provider_kubernetes.storage_class",
        "cdktn_provider_kubernetes.storage_class_v1",
        "cdktn_provider_kubernetes.token_request_v1",
        "cdktn_provider_kubernetes.validating_webhook_configuration",
        "cdktn_provider_kubernetes.validating_webhook_configuration_v1"
    ],
    "package_data": {
        "cdktn_provider_kubernetes._jsii": [
            "provider-kubernetes@12.2.0.jsii.tgz"
        ],
        "cdktn_provider_kubernetes": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "cdktf>=0.21.0, <0.22.0",
        "constructs>=10.4.2, <11.0.0",
        "jsii>=1.119.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
