r'''
# `kubernetes_service_v1`

Refer to the Terraform Registry for docs: [`kubernetes_service_v1`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ServiceV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1 kubernetes_service_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["ServiceV1Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["ServiceV1Spec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServiceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1 kubernetes_service_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#metadata ServiceV1#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#spec ServiceV1#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#id ServiceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#timeouts ServiceV1#timeouts}
        :param wait_for_load_balancer: Terraform will wait for the load balancer to have at least 1 endpoint before considering the resource created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#wait_for_load_balancer ServiceV1#wait_for_load_balancer}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd25b5bf030af8231b92b976a7f992f294b0f19cab615956ef90d02096ced18e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceV1Config(
            metadata=metadata,
            spec=spec,
            id=id,
            timeouts=timeouts,
            wait_for_load_balancer=wait_for_load_balancer,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ServiceV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceV1 to import.
        :param import_from_id: The id of the existing ServiceV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b3d32d7c038d1cc64564344267b770df921cf084da1dc66f077bd0abcebca1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        generate_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the service that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#annotations ServiceV1#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#generate_name ServiceV1#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the service. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#labels ServiceV1#labels}
        :param name: Name of the service, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#name ServiceV1#name}
        :param namespace: Namespace defines the space within which name of the service must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#namespace ServiceV1#namespace}
        '''
        value = ServiceV1Metadata(
            annotations=annotations,
            generate_name=generate_name,
            labels=labels,
            name=name,
            namespace=namespace,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        allocate_load_balancer_node_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_ip: typing.Optional[builtins.str] = None,
        cluster_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_traffic_policy: typing.Optional[builtins.str] = None,
        health_check_node_port: typing.Optional[jsii.Number] = None,
        internal_traffic_policy: typing.Optional[builtins.str] = None,
        ip_families: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_family_policy: typing.Optional[builtins.str] = None,
        load_balancer_class: typing.Optional[builtins.str] = None,
        load_balancer_ip: typing.Optional[builtins.str] = None,
        load_balancer_source_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceV1SpecPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        publish_not_ready_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_config: typing.Optional[typing.Union["ServiceV1SpecSessionAffinityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocate_load_balancer_node_ports: Defines if ``NodePorts`` will be automatically allocated for services with type ``LoadBalancer``. It may be set to ``false`` if the cluster load-balancer does not rely on ``NodePorts``. If the caller requests specific ``NodePorts`` (by specifying a value), those requests will be respected, regardless of this field. This field may only be set for services with type ``LoadBalancer``. Default is ``true``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-nodeport-allocation Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#allocate_load_balancer_node_ports ServiceV1#allocate_load_balancer_node_ports}
        :param cluster_ip: The IP address of the service. It is usually assigned randomly by the master. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise, creation of the service will fail. ``None`` can be specified for headless services when proxying is not required. Ignored if type is ``ExternalName``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#cluster_ip ServiceV1#cluster_ip}
        :param cluster_ips: List of IP addresses assigned to this service, and are usually assigned randomly. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise creation of the service will fail. If this field is not specified, it will be initialized from the ``clusterIP`` field. If this field is specified, clients must ensure that ``clusterIPs[0]`` and ``clusterIP`` have the same value. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#cluster_ips ServiceV1#cluster_ips}
        :param external_ips: A list of IP addresses for which nodes in the cluster will also accept traffic for this service. These IPs are not managed by Kubernetes. The user is responsible for ensuring that traffic arrives at a node with this IP. A common example is external load-balancers that are not part of the Kubernetes system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_ips ServiceV1#external_ips}
        :param external_name: The external reference that kubedns or equivalent will return as a CNAME record for this service. No proxying will be involved. Must be a valid DNS name and requires ``type`` to be ``ExternalName``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_name ServiceV1#external_name}
        :param external_traffic_policy: Denotes if this Service desires to route external traffic to node-local or cluster-wide endpoints. ``Local`` preserves the client source IP and avoids a second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced traffic spreading. ``Cluster`` obscures the client source IP and may cause a second hop to another node, but should have good overall load-spreading. More info: https://kubernetes.io/docs/tutorials/services/source-ip/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_traffic_policy ServiceV1#external_traffic_policy}
        :param health_check_node_port: Specifies the Healthcheck NodePort for the service. Only effects when type is set to ``LoadBalancer`` and external_traffic_policy is set to ``Local``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#health_check_node_port ServiceV1#health_check_node_port}
        :param internal_traffic_policy: Specifies if the cluster internal traffic should be routed to all endpoints or node-local endpoints only. ``Cluster`` routes internal traffic to a Service to all endpoints. ``Local`` routes traffic to node-local endpoints only, traffic is dropped if no node-local endpoints are ready. The default value is ``Cluster``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#internal_traffic_policy ServiceV1#internal_traffic_policy}
        :param ip_families: IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this service. This field is usually assigned automatically based on cluster configuration and the ipFamilyPolicy field. If this field is specified manually, the requested family is available in the cluster, and ipFamilyPolicy allows it, it will be used; otherwise creation of the service will fail. This field is conditionally mutable: it allows for adding or removing a secondary IP family, but it does not allow changing the primary IP family of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#ip_families ServiceV1#ip_families}
        :param ip_family_policy: IPFamilyPolicy represents the dual-stack-ness requested or required by this Service. If there is no value provided, then this field will be set to SingleStack. Services can be 'SingleStack' (a single IP family), 'PreferDualStack' (two IP families on dual-stack configured clusters or a single IP family on single-stack clusters), or 'RequireDualStack' (two IP families on dual-stack configured clusters, otherwise fail). The ipFamilies and clusterIPs fields depend on the value of this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#ip_family_policy ServiceV1#ip_family_policy}
        :param load_balancer_class: The class of the load balancer implementation this Service belongs to. If specified, the value of this field must be a label-style identifier, with an optional prefix. This field can only be set when the Service type is ``LoadBalancer``. If not set, the default load balancer implementation is used. This field can only be set when creating or updating a Service to type ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_class ServiceV1#load_balancer_class}
        :param load_balancer_ip: Only applies to ``type = LoadBalancer``. LoadBalancer will get created with the IP specified in this field. This feature depends on whether the underlying cloud-provider supports specifying this field when a load balancer is created. This field will be ignored if the cloud-provider does not support the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_ip ServiceV1#load_balancer_ip}
        :param load_balancer_source_ranges: If specified and supported by the platform, this will restrict traffic through the cloud-provider load-balancer will be restricted to the specified client IPs. This field will be ignored if the cloud-provider does not support the feature. More info: http://kubernetes.io/docs/user-guide/services-firewalls Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_source_ranges ServiceV1#load_balancer_source_ranges}
        :param port: port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#port ServiceV1#port}
        :param publish_not_ready_addresses: When set to true, indicates that DNS implementations must publish the ``notReadyAddresses`` of subsets for the Endpoints associated with the Service. The default value is ``false``. The primary use case for setting this field is to use a StatefulSet's Headless Service to propagate ``SRV`` records for its Pods without respect to their readiness for purpose of peer discovery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#publish_not_ready_addresses ServiceV1#publish_not_ready_addresses}
        :param selector: Route service traffic to pods with label keys and values matching this selector. Only applies to types ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#selector ServiceV1#selector}
        :param session_affinity: Used to maintain session affinity. Supports ``ClientIP`` and ``None``. Defaults to ``None``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#session_affinity ServiceV1#session_affinity}
        :param session_affinity_config: session_affinity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#session_affinity_config ServiceV1#session_affinity_config}
        :param type: Determines how the service is exposed. Defaults to ``ClusterIP``. Valid options are ``ExternalName``, ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. ``ExternalName`` maps to the specified ``external_name``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#type ServiceV1#type}
        '''
        value = ServiceV1Spec(
            allocate_load_balancer_node_ports=allocate_load_balancer_node_ports,
            cluster_ip=cluster_ip,
            cluster_ips=cluster_ips,
            external_ips=external_ips,
            external_name=external_name,
            external_traffic_policy=external_traffic_policy,
            health_check_node_port=health_check_node_port,
            internal_traffic_policy=internal_traffic_policy,
            ip_families=ip_families,
            ip_family_policy=ip_family_policy,
            load_balancer_class=load_balancer_class,
            load_balancer_ip=load_balancer_ip,
            load_balancer_source_ranges=load_balancer_source_ranges,
            port=port,
            publish_not_ready_addresses=publish_not_ready_addresses,
            selector=selector,
            session_affinity=session_affinity,
            session_affinity_config=session_affinity_config,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#create ServiceV1#create}.
        '''
        value = ServiceV1Timeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWaitForLoadBalancer")
    def reset_wait_for_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForLoadBalancer", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "ServiceV1MetadataOutputReference":
        return typing.cast("ServiceV1MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "ServiceV1SpecOutputReference":
        return typing.cast("ServiceV1SpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "ServiceV1StatusList":
        return typing.cast("ServiceV1StatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServiceV1TimeoutsOutputReference":
        return typing.cast("ServiceV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["ServiceV1Metadata"]:
        return typing.cast(typing.Optional["ServiceV1Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["ServiceV1Spec"]:
        return typing.cast(typing.Optional["ServiceV1Spec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForLoadBalancerInput")
    def wait_for_load_balancer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForLoadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220df1537103c6d6ad5fefab4772872db1ea5b69081f92b59805e15b396c1c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForLoadBalancer")
    def wait_for_load_balancer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForLoadBalancer"))

    @wait_for_load_balancer.setter
    def wait_for_load_balancer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4582786322dde4c8a1732d85a5ff03c7b65afb77c2933b2f5873c651ce3782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForLoadBalancer", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "metadata": "metadata",
        "spec": "spec",
        "id": "id",
        "timeouts": "timeouts",
        "wait_for_load_balancer": "waitForLoadBalancer",
    },
)
class ServiceV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Union["ServiceV1Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["ServiceV1Spec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServiceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#metadata ServiceV1#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#spec ServiceV1#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#id ServiceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#timeouts ServiceV1#timeouts}
        :param wait_for_load_balancer: Terraform will wait for the load balancer to have at least 1 endpoint before considering the resource created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#wait_for_load_balancer ServiceV1#wait_for_load_balancer}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = ServiceV1Metadata(**metadata)
        if isinstance(spec, dict):
            spec = ServiceV1Spec(**spec)
        if isinstance(timeouts, dict):
            timeouts = ServiceV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2434a51f0d3891964eaa18e3df29abb22c7ecb1dc3c81917b48a0dc98581fc9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument wait_for_load_balancer", value=wait_for_load_balancer, expected_type=type_hints["wait_for_load_balancer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata": metadata,
            "spec": spec,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if wait_for_load_balancer is not None:
            self._values["wait_for_load_balancer"] = wait_for_load_balancer

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def metadata(self) -> "ServiceV1Metadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#metadata ServiceV1#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("ServiceV1Metadata", result)

    @builtins.property
    def spec(self) -> "ServiceV1Spec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#spec ServiceV1#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("ServiceV1Spec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#id ServiceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServiceV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#timeouts ServiceV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServiceV1Timeouts"], result)

    @builtins.property
    def wait_for_load_balancer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Terraform will wait for the load balancer to have at least 1 endpoint before considering the resource created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#wait_for_load_balancer ServiceV1#wait_for_load_balancer}
        '''
        result = self._values.get("wait_for_load_balancer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1Metadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class ServiceV1Metadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        generate_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the service that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#annotations ServiceV1#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#generate_name ServiceV1#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the service. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#labels ServiceV1#labels}
        :param name: Name of the service, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#name ServiceV1#name}
        :param namespace: Namespace defines the space within which name of the service must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#namespace ServiceV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b999aebc92d9053c6cce2f9605bb607a0d48dae7ae47015683dd19d3674c3faa)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument generate_name", value=generate_name, expected_type=type_hints["generate_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if generate_name is not None:
            self._values["generate_name"] = generate_name
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An unstructured key value map stored with the service that may be used to store arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#annotations ServiceV1#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        '''Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided.

        This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#generate_name ServiceV1#generate_name}
        '''
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the service.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#labels ServiceV1#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the service, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#name ServiceV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within which name of the service must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#namespace ServiceV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1MetadataOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c891424df43c2772f1a226f7b26444e464041bb6fa53bebfa7789a31f487740)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetGenerateName")
    def reset_generate_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerateName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="resourceVersion")
    def resource_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceVersion"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="generateNameInput")
    def generate_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278ffc45a99b3c47e209ea81565eb4a79301ca3466a17431542207c8602bdc52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generateName")
    def generate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateName"))

    @generate_name.setter
    def generate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea202fa16c5efb4ac087cd8ec549d363ed4520f3d38d4e31516371b2d1133907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9606d085aad03e2b625b2b333bc98696465b111da729fe5a3920d9d4b31b9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d51b1332c9df6fffa7fcd8a7bddd1e552bb890db406b6c0d22b4bee7a079d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc23532b529a03f27fc7b718fb24b75c8665e32eddf0223d1ba2f147182e4904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceV1Metadata]:
        return typing.cast(typing.Optional[ServiceV1Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceV1Metadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fe3ef01387a6617c2ab3d169a76e85f403e1eda5d51de228d6a8272e3f276c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1Spec",
    jsii_struct_bases=[],
    name_mapping={
        "allocate_load_balancer_node_ports": "allocateLoadBalancerNodePorts",
        "cluster_ip": "clusterIp",
        "cluster_ips": "clusterIps",
        "external_ips": "externalIps",
        "external_name": "externalName",
        "external_traffic_policy": "externalTrafficPolicy",
        "health_check_node_port": "healthCheckNodePort",
        "internal_traffic_policy": "internalTrafficPolicy",
        "ip_families": "ipFamilies",
        "ip_family_policy": "ipFamilyPolicy",
        "load_balancer_class": "loadBalancerClass",
        "load_balancer_ip": "loadBalancerIp",
        "load_balancer_source_ranges": "loadBalancerSourceRanges",
        "port": "port",
        "publish_not_ready_addresses": "publishNotReadyAddresses",
        "selector": "selector",
        "session_affinity": "sessionAffinity",
        "session_affinity_config": "sessionAffinityConfig",
        "type": "type",
    },
)
class ServiceV1Spec:
    def __init__(
        self,
        *,
        allocate_load_balancer_node_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_ip: typing.Optional[builtins.str] = None,
        cluster_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_traffic_policy: typing.Optional[builtins.str] = None,
        health_check_node_port: typing.Optional[jsii.Number] = None,
        internal_traffic_policy: typing.Optional[builtins.str] = None,
        ip_families: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_family_policy: typing.Optional[builtins.str] = None,
        load_balancer_class: typing.Optional[builtins.str] = None,
        load_balancer_ip: typing.Optional[builtins.str] = None,
        load_balancer_source_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceV1SpecPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        publish_not_ready_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_config: typing.Optional[typing.Union["ServiceV1SpecSessionAffinityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocate_load_balancer_node_ports: Defines if ``NodePorts`` will be automatically allocated for services with type ``LoadBalancer``. It may be set to ``false`` if the cluster load-balancer does not rely on ``NodePorts``. If the caller requests specific ``NodePorts`` (by specifying a value), those requests will be respected, regardless of this field. This field may only be set for services with type ``LoadBalancer``. Default is ``true``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-nodeport-allocation Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#allocate_load_balancer_node_ports ServiceV1#allocate_load_balancer_node_ports}
        :param cluster_ip: The IP address of the service. It is usually assigned randomly by the master. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise, creation of the service will fail. ``None`` can be specified for headless services when proxying is not required. Ignored if type is ``ExternalName``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#cluster_ip ServiceV1#cluster_ip}
        :param cluster_ips: List of IP addresses assigned to this service, and are usually assigned randomly. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise creation of the service will fail. If this field is not specified, it will be initialized from the ``clusterIP`` field. If this field is specified, clients must ensure that ``clusterIPs[0]`` and ``clusterIP`` have the same value. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#cluster_ips ServiceV1#cluster_ips}
        :param external_ips: A list of IP addresses for which nodes in the cluster will also accept traffic for this service. These IPs are not managed by Kubernetes. The user is responsible for ensuring that traffic arrives at a node with this IP. A common example is external load-balancers that are not part of the Kubernetes system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_ips ServiceV1#external_ips}
        :param external_name: The external reference that kubedns or equivalent will return as a CNAME record for this service. No proxying will be involved. Must be a valid DNS name and requires ``type`` to be ``ExternalName``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_name ServiceV1#external_name}
        :param external_traffic_policy: Denotes if this Service desires to route external traffic to node-local or cluster-wide endpoints. ``Local`` preserves the client source IP and avoids a second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced traffic spreading. ``Cluster`` obscures the client source IP and may cause a second hop to another node, but should have good overall load-spreading. More info: https://kubernetes.io/docs/tutorials/services/source-ip/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_traffic_policy ServiceV1#external_traffic_policy}
        :param health_check_node_port: Specifies the Healthcheck NodePort for the service. Only effects when type is set to ``LoadBalancer`` and external_traffic_policy is set to ``Local``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#health_check_node_port ServiceV1#health_check_node_port}
        :param internal_traffic_policy: Specifies if the cluster internal traffic should be routed to all endpoints or node-local endpoints only. ``Cluster`` routes internal traffic to a Service to all endpoints. ``Local`` routes traffic to node-local endpoints only, traffic is dropped if no node-local endpoints are ready. The default value is ``Cluster``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#internal_traffic_policy ServiceV1#internal_traffic_policy}
        :param ip_families: IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this service. This field is usually assigned automatically based on cluster configuration and the ipFamilyPolicy field. If this field is specified manually, the requested family is available in the cluster, and ipFamilyPolicy allows it, it will be used; otherwise creation of the service will fail. This field is conditionally mutable: it allows for adding or removing a secondary IP family, but it does not allow changing the primary IP family of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#ip_families ServiceV1#ip_families}
        :param ip_family_policy: IPFamilyPolicy represents the dual-stack-ness requested or required by this Service. If there is no value provided, then this field will be set to SingleStack. Services can be 'SingleStack' (a single IP family), 'PreferDualStack' (two IP families on dual-stack configured clusters or a single IP family on single-stack clusters), or 'RequireDualStack' (two IP families on dual-stack configured clusters, otherwise fail). The ipFamilies and clusterIPs fields depend on the value of this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#ip_family_policy ServiceV1#ip_family_policy}
        :param load_balancer_class: The class of the load balancer implementation this Service belongs to. If specified, the value of this field must be a label-style identifier, with an optional prefix. This field can only be set when the Service type is ``LoadBalancer``. If not set, the default load balancer implementation is used. This field can only be set when creating or updating a Service to type ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_class ServiceV1#load_balancer_class}
        :param load_balancer_ip: Only applies to ``type = LoadBalancer``. LoadBalancer will get created with the IP specified in this field. This feature depends on whether the underlying cloud-provider supports specifying this field when a load balancer is created. This field will be ignored if the cloud-provider does not support the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_ip ServiceV1#load_balancer_ip}
        :param load_balancer_source_ranges: If specified and supported by the platform, this will restrict traffic through the cloud-provider load-balancer will be restricted to the specified client IPs. This field will be ignored if the cloud-provider does not support the feature. More info: http://kubernetes.io/docs/user-guide/services-firewalls Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_source_ranges ServiceV1#load_balancer_source_ranges}
        :param port: port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#port ServiceV1#port}
        :param publish_not_ready_addresses: When set to true, indicates that DNS implementations must publish the ``notReadyAddresses`` of subsets for the Endpoints associated with the Service. The default value is ``false``. The primary use case for setting this field is to use a StatefulSet's Headless Service to propagate ``SRV`` records for its Pods without respect to their readiness for purpose of peer discovery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#publish_not_ready_addresses ServiceV1#publish_not_ready_addresses}
        :param selector: Route service traffic to pods with label keys and values matching this selector. Only applies to types ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#selector ServiceV1#selector}
        :param session_affinity: Used to maintain session affinity. Supports ``ClientIP`` and ``None``. Defaults to ``None``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#session_affinity ServiceV1#session_affinity}
        :param session_affinity_config: session_affinity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#session_affinity_config ServiceV1#session_affinity_config}
        :param type: Determines how the service is exposed. Defaults to ``ClusterIP``. Valid options are ``ExternalName``, ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. ``ExternalName`` maps to the specified ``external_name``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#type ServiceV1#type}
        '''
        if isinstance(session_affinity_config, dict):
            session_affinity_config = ServiceV1SpecSessionAffinityConfig(**session_affinity_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c08e6559c669a32a313c2a252105320fb247b9628140759f119a52c2f53f9b1)
            check_type(argname="argument allocate_load_balancer_node_ports", value=allocate_load_balancer_node_ports, expected_type=type_hints["allocate_load_balancer_node_ports"])
            check_type(argname="argument cluster_ip", value=cluster_ip, expected_type=type_hints["cluster_ip"])
            check_type(argname="argument cluster_ips", value=cluster_ips, expected_type=type_hints["cluster_ips"])
            check_type(argname="argument external_ips", value=external_ips, expected_type=type_hints["external_ips"])
            check_type(argname="argument external_name", value=external_name, expected_type=type_hints["external_name"])
            check_type(argname="argument external_traffic_policy", value=external_traffic_policy, expected_type=type_hints["external_traffic_policy"])
            check_type(argname="argument health_check_node_port", value=health_check_node_port, expected_type=type_hints["health_check_node_port"])
            check_type(argname="argument internal_traffic_policy", value=internal_traffic_policy, expected_type=type_hints["internal_traffic_policy"])
            check_type(argname="argument ip_families", value=ip_families, expected_type=type_hints["ip_families"])
            check_type(argname="argument ip_family_policy", value=ip_family_policy, expected_type=type_hints["ip_family_policy"])
            check_type(argname="argument load_balancer_class", value=load_balancer_class, expected_type=type_hints["load_balancer_class"])
            check_type(argname="argument load_balancer_ip", value=load_balancer_ip, expected_type=type_hints["load_balancer_ip"])
            check_type(argname="argument load_balancer_source_ranges", value=load_balancer_source_ranges, expected_type=type_hints["load_balancer_source_ranges"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument publish_not_ready_addresses", value=publish_not_ready_addresses, expected_type=type_hints["publish_not_ready_addresses"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument session_affinity_config", value=session_affinity_config, expected_type=type_hints["session_affinity_config"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocate_load_balancer_node_ports is not None:
            self._values["allocate_load_balancer_node_ports"] = allocate_load_balancer_node_ports
        if cluster_ip is not None:
            self._values["cluster_ip"] = cluster_ip
        if cluster_ips is not None:
            self._values["cluster_ips"] = cluster_ips
        if external_ips is not None:
            self._values["external_ips"] = external_ips
        if external_name is not None:
            self._values["external_name"] = external_name
        if external_traffic_policy is not None:
            self._values["external_traffic_policy"] = external_traffic_policy
        if health_check_node_port is not None:
            self._values["health_check_node_port"] = health_check_node_port
        if internal_traffic_policy is not None:
            self._values["internal_traffic_policy"] = internal_traffic_policy
        if ip_families is not None:
            self._values["ip_families"] = ip_families
        if ip_family_policy is not None:
            self._values["ip_family_policy"] = ip_family_policy
        if load_balancer_class is not None:
            self._values["load_balancer_class"] = load_balancer_class
        if load_balancer_ip is not None:
            self._values["load_balancer_ip"] = load_balancer_ip
        if load_balancer_source_ranges is not None:
            self._values["load_balancer_source_ranges"] = load_balancer_source_ranges
        if port is not None:
            self._values["port"] = port
        if publish_not_ready_addresses is not None:
            self._values["publish_not_ready_addresses"] = publish_not_ready_addresses
        if selector is not None:
            self._values["selector"] = selector
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if session_affinity_config is not None:
            self._values["session_affinity_config"] = session_affinity_config
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def allocate_load_balancer_node_ports(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if ``NodePorts`` will be automatically allocated for services with type ``LoadBalancer``.

        It may be set to ``false`` if the cluster load-balancer does not rely on ``NodePorts``.  If the caller requests specific ``NodePorts`` (by specifying a value), those requests will be respected, regardless of this field. This field may only be set for services with type ``LoadBalancer``. Default is ``true``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-nodeport-allocation

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#allocate_load_balancer_node_ports ServiceV1#allocate_load_balancer_node_ports}
        '''
        result = self._values.get("allocate_load_balancer_node_ports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cluster_ip(self) -> typing.Optional[builtins.str]:
        '''The IP address of the service.

        It is usually assigned randomly by the master. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise, creation of the service will fail. ``None`` can be specified for headless services when proxying is not required. Ignored if type is ``ExternalName``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#cluster_ip ServiceV1#cluster_ip}
        '''
        result = self._values.get("cluster_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IP addresses assigned to this service, and are usually assigned randomly.

        If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise creation of the service will fail. If this field is not specified, it will be initialized from the ``clusterIP`` field. If this field is specified, clients must ensure that ``clusterIPs[0]`` and ``clusterIP`` have the same value. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#cluster_ips ServiceV1#cluster_ips}
        '''
        result = self._values.get("cluster_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IP addresses for which nodes in the cluster will also accept traffic for this service.

        These IPs are not managed by Kubernetes. The user is responsible for ensuring that traffic arrives at a node with this IP.  A common example is external load-balancers that are not part of the Kubernetes system.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_ips ServiceV1#external_ips}
        '''
        result = self._values.get("external_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_name(self) -> typing.Optional[builtins.str]:
        '''The external reference that kubedns or equivalent will return as a CNAME record for this service.

        No proxying will be involved. Must be a valid DNS name and requires ``type`` to be ``ExternalName``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_name ServiceV1#external_name}
        '''
        result = self._values.get("external_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_traffic_policy(self) -> typing.Optional[builtins.str]:
        '''Denotes if this Service desires to route external traffic to node-local or cluster-wide endpoints.

        ``Local`` preserves the client source IP and avoids a second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced traffic spreading. ``Cluster`` obscures the client source IP and may cause a second hop to another node, but should have good overall load-spreading. More info: https://kubernetes.io/docs/tutorials/services/source-ip/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#external_traffic_policy ServiceV1#external_traffic_policy}
        '''
        result = self._values.get("external_traffic_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_node_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the Healthcheck NodePort for the service.

        Only effects when type is set to ``LoadBalancer`` and external_traffic_policy is set to ``Local``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#health_check_node_port ServiceV1#health_check_node_port}
        '''
        result = self._values.get("health_check_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def internal_traffic_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies if the cluster internal traffic should be routed to all endpoints or node-local endpoints only.

        ``Cluster`` routes internal traffic to a Service to all endpoints. ``Local`` routes traffic to node-local endpoints only, traffic is dropped if no node-local endpoints are ready. The default value is ``Cluster``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#internal_traffic_policy ServiceV1#internal_traffic_policy}
        '''
        result = self._values.get("internal_traffic_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_families(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this service. This field is usually assigned automatically based on cluster configuration and the ipFamilyPolicy field. If this field is specified manually, the requested family is available in the cluster, and ipFamilyPolicy allows it, it will be used; otherwise creation of the service will fail. This field is conditionally mutable: it allows for adding or removing a secondary IP family, but it does not allow changing the primary IP family of the Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#ip_families ServiceV1#ip_families}
        '''
        result = self._values.get("ip_families")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_family_policy(self) -> typing.Optional[builtins.str]:
        '''IPFamilyPolicy represents the dual-stack-ness requested or required by this Service.

        If there is no value provided, then this field will be set to SingleStack. Services can be 'SingleStack' (a single IP family), 'PreferDualStack' (two IP families on dual-stack configured clusters or a single IP family on single-stack clusters), or 'RequireDualStack' (two IP families on dual-stack configured clusters, otherwise fail). The ipFamilies and clusterIPs fields depend on the value of this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#ip_family_policy ServiceV1#ip_family_policy}
        '''
        result = self._values.get("ip_family_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_class(self) -> typing.Optional[builtins.str]:
        '''The class of the load balancer implementation this Service belongs to.

        If specified, the value of this field must be a label-style identifier, with an optional prefix. This field can only be set when the Service type is ``LoadBalancer``. If not set, the default load balancer implementation is used. This field can only be set when creating or updating a Service to type ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_class ServiceV1#load_balancer_class}
        '''
        result = self._values.get("load_balancer_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_ip(self) -> typing.Optional[builtins.str]:
        '''Only applies to ``type = LoadBalancer``.

        LoadBalancer will get created with the IP specified in this field. This feature depends on whether the underlying cloud-provider supports specifying this field when a load balancer is created. This field will be ignored if the cloud-provider does not support the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_ip ServiceV1#load_balancer_ip}
        '''
        result = self._values.get("load_balancer_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_source_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified and supported by the platform, this will restrict traffic through the cloud-provider load-balancer will be restricted to the specified client IPs.

        This field will be ignored if the cloud-provider does not support the feature. More info: http://kubernetes.io/docs/user-guide/services-firewalls

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#load_balancer_source_ranges ServiceV1#load_balancer_source_ranges}
        '''
        result = self._values.get("load_balancer_source_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def port(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceV1SpecPort"]]]:
        '''port block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#port ServiceV1#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceV1SpecPort"]]], result)

    @builtins.property
    def publish_not_ready_addresses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, indicates that DNS implementations must publish the ``notReadyAddresses`` of subsets for the Endpoints associated with the Service.

        The default value is ``false``. The primary use case for setting this field is to use a StatefulSet's Headless Service to propagate ``SRV`` records for its Pods without respect to their readiness for purpose of peer discovery.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#publish_not_ready_addresses ServiceV1#publish_not_ready_addresses}
        '''
        result = self._values.get("publish_not_ready_addresses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selector(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Route service traffic to pods with label keys and values matching this selector.

        Only applies to types ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#selector ServiceV1#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Used to maintain session affinity. Supports ``ClientIP`` and ``None``. Defaults to ``None``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#session_affinity ServiceV1#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity_config(
        self,
    ) -> typing.Optional["ServiceV1SpecSessionAffinityConfig"]:
        '''session_affinity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#session_affinity_config ServiceV1#session_affinity_config}
        '''
        result = self._values.get("session_affinity_config")
        return typing.cast(typing.Optional["ServiceV1SpecSessionAffinityConfig"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Determines how the service is exposed.

        Defaults to ``ClusterIP``. Valid options are ``ExternalName``, ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. ``ExternalName`` maps to the specified ``external_name``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#type ServiceV1#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1Spec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1SpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ceedad0bd9e6ce21137cce3c5a8062fdcd04666a40a0c47aba25f2e5c777ca8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPort")
    def put_port(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceV1SpecPort", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f72698e3ee4b25244a891218d39e76a4164177a1329cfed05e32a29cfabb560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPort", [value]))

    @jsii.member(jsii_name="putSessionAffinityConfig")
    def put_session_affinity_config(
        self,
        *,
        client_ip: typing.Optional[typing.Union["ServiceV1SpecSessionAffinityConfigClientIp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip: client_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#client_ip ServiceV1#client_ip}
        '''
        value = ServiceV1SpecSessionAffinityConfig(client_ip=client_ip)

        return typing.cast(None, jsii.invoke(self, "putSessionAffinityConfig", [value]))

    @jsii.member(jsii_name="resetAllocateLoadBalancerNodePorts")
    def reset_allocate_load_balancer_node_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocateLoadBalancerNodePorts", []))

    @jsii.member(jsii_name="resetClusterIp")
    def reset_cluster_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIp", []))

    @jsii.member(jsii_name="resetClusterIps")
    def reset_cluster_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIps", []))

    @jsii.member(jsii_name="resetExternalIps")
    def reset_external_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIps", []))

    @jsii.member(jsii_name="resetExternalName")
    def reset_external_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalName", []))

    @jsii.member(jsii_name="resetExternalTrafficPolicy")
    def reset_external_traffic_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalTrafficPolicy", []))

    @jsii.member(jsii_name="resetHealthCheckNodePort")
    def reset_health_check_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckNodePort", []))

    @jsii.member(jsii_name="resetInternalTrafficPolicy")
    def reset_internal_traffic_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalTrafficPolicy", []))

    @jsii.member(jsii_name="resetIpFamilies")
    def reset_ip_families(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFamilies", []))

    @jsii.member(jsii_name="resetIpFamilyPolicy")
    def reset_ip_family_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFamilyPolicy", []))

    @jsii.member(jsii_name="resetLoadBalancerClass")
    def reset_load_balancer_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerClass", []))

    @jsii.member(jsii_name="resetLoadBalancerIp")
    def reset_load_balancer_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerIp", []))

    @jsii.member(jsii_name="resetLoadBalancerSourceRanges")
    def reset_load_balancer_source_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerSourceRanges", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPublishNotReadyAddresses")
    def reset_publish_not_ready_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishNotReadyAddresses", []))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetSessionAffinityConfig")
    def reset_session_affinity_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinityConfig", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> "ServiceV1SpecPortList":
        return typing.cast("ServiceV1SpecPortList", jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityConfig")
    def session_affinity_config(
        self,
    ) -> "ServiceV1SpecSessionAffinityConfigOutputReference":
        return typing.cast("ServiceV1SpecSessionAffinityConfigOutputReference", jsii.get(self, "sessionAffinityConfig"))

    @builtins.property
    @jsii.member(jsii_name="allocateLoadBalancerNodePortsInput")
    def allocate_load_balancer_node_ports_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allocateLoadBalancerNodePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpInput")
    def cluster_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIpInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpsInput")
    def cluster_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusterIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIpsInput")
    def external_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNameInput")
    def external_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNameInput"))

    @builtins.property
    @jsii.member(jsii_name="externalTrafficPolicyInput")
    def external_traffic_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalTrafficPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckNodePortInput")
    def health_check_node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckNodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="internalTrafficPolicyInput")
    def internal_traffic_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internalTrafficPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFamiliesInput")
    def ip_families_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipFamiliesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFamilyPolicyInput")
    def ip_family_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipFamilyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerClassInput")
    def load_balancer_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerClassInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerIpInput")
    def load_balancer_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerIpInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSourceRangesInput")
    def load_balancer_source_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loadBalancerSourceRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceV1SpecPort"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceV1SpecPort"]]], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="publishNotReadyAddressesInput")
    def publish_not_ready_addresses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishNotReadyAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityConfigInput")
    def session_affinity_config_input(
        self,
    ) -> typing.Optional["ServiceV1SpecSessionAffinityConfig"]:
        return typing.cast(typing.Optional["ServiceV1SpecSessionAffinityConfig"], jsii.get(self, "sessionAffinityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="allocateLoadBalancerNodePorts")
    def allocate_load_balancer_node_ports(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allocateLoadBalancerNodePorts"))

    @allocate_load_balancer_node_ports.setter
    def allocate_load_balancer_node_ports(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b3a4f43b915d509ec73450fb7cd9f9765b09e53c42a9ad7940fcf7026af7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocateLoadBalancerNodePorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIp")
    def cluster_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIp"))

    @cluster_ip.setter
    def cluster_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49414e9d030c37b71d376384551ff8327eda937f3717031b249ba37a95a55bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIps")
    def cluster_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterIps"))

    @cluster_ips.setter
    def cluster_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff74915daa373580bb906174f7b87153ea4bd7ccc6fd801286cc6c7b21b0c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalIps")
    def external_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalIps"))

    @external_ips.setter
    def external_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de8374d54217757181c1ec1ead1e0cc16cfc1ed27d9fd933125bbd466b41fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalName")
    def external_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalName"))

    @external_name.setter
    def external_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c885aa41c69e98a41d0eb16e494c445464df1bd689461c2eccc114b59287296f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalTrafficPolicy")
    def external_traffic_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalTrafficPolicy"))

    @external_traffic_policy.setter
    def external_traffic_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09e3c724e250f6268a1f605d5c9b64c30b7b40c52eb8aeef439f7d848831674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalTrafficPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckNodePort")
    def health_check_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckNodePort"))

    @health_check_node_port.setter
    def health_check_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a89027695a3b77981e290ca9e7483d263c6d91c85fa4e3aaea7ca18cb3d982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalTrafficPolicy")
    def internal_traffic_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalTrafficPolicy"))

    @internal_traffic_policy.setter
    def internal_traffic_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc0ad85a4ccc4bd6a77d5bc779a577e1679307ad5fc0dbc9efcb3bccf232614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalTrafficPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipFamilies")
    def ip_families(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipFamilies"))

    @ip_families.setter
    def ip_families(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28480eb425d6f9b317f93712ad7334ec1713c4f35e24c451290e51cc9b9eff17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFamilies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipFamilyPolicy")
    def ip_family_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipFamilyPolicy"))

    @ip_family_policy.setter
    def ip_family_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640239701c2b6f63f6f4bef5e79b4d482c3afcd0a0cd75b22ce4037e731866bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFamilyPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerClass")
    def load_balancer_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerClass"))

    @load_balancer_class.setter
    def load_balancer_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762027c2e283b6950d1d5e6ae30975bb07c05263fbe41fda60b9fc87ce7ba387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerIp")
    def load_balancer_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerIp"))

    @load_balancer_ip.setter
    def load_balancer_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8e45d5f7a700170956202f1d8dafae8ba4c53a428cd22fd6b3d8a34d6c632e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSourceRanges")
    def load_balancer_source_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loadBalancerSourceRanges"))

    @load_balancer_source_ranges.setter
    def load_balancer_source_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41ec5c0ddeb77f52b3818c16b03ec1576cc440a53cbab65a0b5cefb1f15ebf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerSourceRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishNotReadyAddresses")
    def publish_not_ready_addresses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishNotReadyAddresses"))

    @publish_not_ready_addresses.setter
    def publish_not_ready_addresses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b7b89b0228adfeaf82660046ccbd69a1e78af16859e71a62e96bbcb4f1dcb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishNotReadyAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c5b5aee1a068bf502b98c7a7a5ab3d119947369c0a0f142e7cc265cc7cd710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5cf3fc6de38897df783d12bb63628d0f33b507e7a8f8b8c6ab46da17aca2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a646512eb1e1de3774ea1903e59cd98995f1be7135ecb83c6e9c2b3715da92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceV1Spec]:
        return typing.cast(typing.Optional[ServiceV1Spec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceV1Spec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5eaa030f6fa1f16c9344517ce4cbfef53bcb7ff04012d252c5619c33da659e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecPort",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "app_protocol": "appProtocol",
        "name": "name",
        "node_port": "nodePort",
        "protocol": "protocol",
        "target_port": "targetPort",
    },
)
class ServiceV1SpecPort:
    def __init__(
        self,
        *,
        port: jsii.Number,
        app_protocol: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        node_port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        target_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: The port that will be exposed by this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#port ServiceV1#port}
        :param app_protocol: The application protocol for this port. This field follows standard Kubernetes label syntax. Un-prefixed names are reserved for IANA standard service names (as per RFC-6335 and http://www.iana.org/assignments/service-names). Non-standard protocols should use prefixed names such as mycompany.com/my-custom-protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#app_protocol ServiceV1#app_protocol}
        :param name: The name of this port within the service. All ports within the service must have unique names. Optional if only one ServicePort is defined on this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#name ServiceV1#name}
        :param node_port: The port on each node on which this service is exposed when ``type`` is ``NodePort`` or ``LoadBalancer``. Usually assigned by the system. If specified, it will be allocated to the service if unused or else creation of the service will fail. Default is to auto-allocate a port if the ``type`` of this service requires one. More info: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#node_port ServiceV1#node_port}
        :param protocol: The IP protocol for this port. Supports ``TCP`` and ``UDP``. Default is ``TCP``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#protocol ServiceV1#protocol}
        :param target_port: Number or name of the port to access on the pods targeted by the service. Number must be in the range 1 to 65535. This field is ignored for services with ``cluster_ip = "None"``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#target_port ServiceV1#target_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6034e310b0a934c7a10bb731ab836ba2f21e95308f3044986edc40f705b0444)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument app_protocol", value=app_protocol, expected_type=type_hints["app_protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_port", value=node_port, expected_type=type_hints["node_port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
        }
        if app_protocol is not None:
            self._values["app_protocol"] = app_protocol
        if name is not None:
            self._values["name"] = name
        if node_port is not None:
            self._values["node_port"] = node_port
        if protocol is not None:
            self._values["protocol"] = protocol
        if target_port is not None:
            self._values["target_port"] = target_port

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port that will be exposed by this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#port ServiceV1#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def app_protocol(self) -> typing.Optional[builtins.str]:
        '''The application protocol for this port.

        This field follows standard Kubernetes label syntax. Un-prefixed names are reserved for IANA standard service names (as per RFC-6335 and http://www.iana.org/assignments/service-names). Non-standard protocols should use prefixed names such as mycompany.com/my-custom-protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#app_protocol ServiceV1#app_protocol}
        '''
        result = self._values.get("app_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this port within the service.

        All ports within the service must have unique names. Optional if only one ServicePort is defined on this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#name ServiceV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_port(self) -> typing.Optional[jsii.Number]:
        '''The port on each node on which this service is exposed when ``type`` is ``NodePort`` or ``LoadBalancer``.

        Usually assigned by the system. If specified, it will be allocated to the service if unused or else creation of the service will fail. Default is to auto-allocate a port if the ``type`` of this service requires one. More info: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#node_port ServiceV1#node_port}
        '''
        result = self._values.get("node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The IP protocol for this port. Supports ``TCP`` and ``UDP``. Default is ``TCP``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#protocol ServiceV1#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_port(self) -> typing.Optional[builtins.str]:
        '''Number or name of the port to access on the pods targeted by the service.

        Number must be in the range 1 to 65535. This field is ignored for services with ``cluster_ip = "None"``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#target_port ServiceV1#target_port}
        '''
        result = self._values.get("target_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1SpecPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1SpecPortList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecPortList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a88fc6c49ddaf3d3ef0567c44d2e7df54de54b7290487b1ed79002bf130ea54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceV1SpecPortOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db7bfadb0fe15433a429e732b2e484f773e341c102f471b1ee52a9b00cbded0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceV1SpecPortOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb35ffd284a6963f38dbdee285fed03f1b331a3b2e7fb02d44c8deeb6c1913e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61de6fe607b52f573f31655e8a52765f09de0335a74cc5f7d016705d398e21c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26b3f11dcf0fa5ff9a6156a2e4de8520add74e07116190fe7f3017f2e28c533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceV1SpecPort]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceV1SpecPort]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceV1SpecPort]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5d0d26a8ffe6f489628b67e13d08442c3f7d5322780b6647b6ba3f4d43fc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceV1SpecPortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecPortOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b73e83f2c854df7f5fd6691a26cb191e14c7cccb389f5682ecbbc7ff365a2d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAppProtocol")
    def reset_app_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppProtocol", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNodePort")
    def reset_node_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetTargetPort")
    def reset_target_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPort", []))

    @builtins.property
    @jsii.member(jsii_name="appProtocolInput")
    def app_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePortInput")
    def node_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodePortInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPortInput")
    def target_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPortInput"))

    @builtins.property
    @jsii.member(jsii_name="appProtocol")
    def app_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appProtocol"))

    @app_protocol.setter
    def app_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5396face1dacd159402a5f08e6a7a28b2586b0b71fd8742cdba8518af9ad128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228030f79412d26b5280a0958ac5b955bb6be350fb5a281cc0c02cdbf371332b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePort")
    def node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodePort"))

    @node_port.setter
    def node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74242269ca08f08268f1c7da61970347f15eddaaee4a410654fe571f2e9c5dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f865ed8b3f522f46d8c6ab945b091cd7c24d4b480f3677938dfce43532e9f980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd73f865716d5c04aefe09dc954ec81d7fe98c32cba21b60ddb651482b39f73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPort")
    def target_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPort"))

    @target_port.setter
    def target_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0959522591f84cda19e914de82203fe9923643295da6e6ae6504d43d231ee64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1SpecPort]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1SpecPort]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1SpecPort]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53a77fcd86af9e862888558eb2ae55ca6f24f4984213c8aa8ce1a9ce864fe38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecSessionAffinityConfig",
    jsii_struct_bases=[],
    name_mapping={"client_ip": "clientIp"},
)
class ServiceV1SpecSessionAffinityConfig:
    def __init__(
        self,
        *,
        client_ip: typing.Optional[typing.Union["ServiceV1SpecSessionAffinityConfigClientIp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip: client_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#client_ip ServiceV1#client_ip}
        '''
        if isinstance(client_ip, dict):
            client_ip = ServiceV1SpecSessionAffinityConfigClientIp(**client_ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e47f7eda546afb9426b1226198cc1157294fabdf50b52b396ed367a555d59db)
            check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_ip is not None:
            self._values["client_ip"] = client_ip

    @builtins.property
    def client_ip(
        self,
    ) -> typing.Optional["ServiceV1SpecSessionAffinityConfigClientIp"]:
        '''client_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#client_ip ServiceV1#client_ip}
        '''
        result = self._values.get("client_ip")
        return typing.cast(typing.Optional["ServiceV1SpecSessionAffinityConfigClientIp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1SpecSessionAffinityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecSessionAffinityConfigClientIp",
    jsii_struct_bases=[],
    name_mapping={"timeout_seconds": "timeoutSeconds"},
)
class ServiceV1SpecSessionAffinityConfigClientIp:
    def __init__(self, *, timeout_seconds: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param timeout_seconds: Specifies the seconds of ``ClientIP`` type session sticky time. The value must be > 0 and <= 86400(for 1 day) if ``ServiceAffinity`` == ``ClientIP``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#timeout_seconds ServiceV1#timeout_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4132d0b48a783dfd49907c91a76a082f78ed288fefb0d77d9b36c900ab4757f9)
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies the seconds of ``ClientIP`` type session sticky time.

        The value must be > 0 and <= 86400(for 1 day) if ``ServiceAffinity`` == ``ClientIP``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#timeout_seconds ServiceV1#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1SpecSessionAffinityConfigClientIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1SpecSessionAffinityConfigClientIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecSessionAffinityConfigClientIpOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4ffecffb42fecf73cd6eb9b2f896c8b6efee8775c419285657a8c49ba0c4bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60fecc1fc4bb52a44bdb116c7da2e734080cafc56d73e21b6fb1e8d7dbad23fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceV1SpecSessionAffinityConfigClientIp]:
        return typing.cast(typing.Optional[ServiceV1SpecSessionAffinityConfigClientIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceV1SpecSessionAffinityConfigClientIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc671dcf667cba2f0a092857e2bd5389bb366e0e4b94bd39a8c2f2e1fae4f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceV1SpecSessionAffinityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1SpecSessionAffinityConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce34a6d0b2f9870ade546c4c44125a303d527f9f186f4116ff9d6b9bde3021a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientIp")
    def put_client_ip(
        self,
        *,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param timeout_seconds: Specifies the seconds of ``ClientIP`` type session sticky time. The value must be > 0 and <= 86400(for 1 day) if ``ServiceAffinity`` == ``ClientIP``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#timeout_seconds ServiceV1#timeout_seconds}
        '''
        value = ServiceV1SpecSessionAffinityConfigClientIp(
            timeout_seconds=timeout_seconds
        )

        return typing.cast(None, jsii.invoke(self, "putClientIp", [value]))

    @jsii.member(jsii_name="resetClientIp")
    def reset_client_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIp", []))

    @builtins.property
    @jsii.member(jsii_name="clientIp")
    def client_ip(self) -> ServiceV1SpecSessionAffinityConfigClientIpOutputReference:
        return typing.cast(ServiceV1SpecSessionAffinityConfigClientIpOutputReference, jsii.get(self, "clientIp"))

    @builtins.property
    @jsii.member(jsii_name="clientIpInput")
    def client_ip_input(
        self,
    ) -> typing.Optional[ServiceV1SpecSessionAffinityConfigClientIp]:
        return typing.cast(typing.Optional[ServiceV1SpecSessionAffinityConfigClientIp], jsii.get(self, "clientIpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceV1SpecSessionAffinityConfig]:
        return typing.cast(typing.Optional[ServiceV1SpecSessionAffinityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceV1SpecSessionAffinityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b760d9b868daf797d8b598bed4dbfc3fcf865f3726e975a9fd3bb4328d367b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1Status",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceV1Status:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1Status(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1StatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c46f67afd2d5ba007968b8334bd965babd8add8bcb3242e32d3c2ff02c17f90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceV1StatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490a591a607b73f70cddb851e987208e0c717a24c0709a4379628445768eddcb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceV1StatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e65ca138038ce65963a5c57867a7afad81bc7f5ad22b4e1da01099c5db23831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c659a722792e4d754f20fe315ff1241938bc507d9d4abed35104fcff2e7d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc281df5c675d23fca807d077ace2b8e80aacc34f6eacf747e6d64debc31df86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceV1StatusLoadBalancer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1StatusLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusLoadBalancerIngress",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceV1StatusLoadBalancerIngress:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1StatusLoadBalancerIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1StatusLoadBalancerIngressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusLoadBalancerIngressList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1532644df8d85abf39ebdcf6dac6fb559954f8d6aa0377875f1486d47f55e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceV1StatusLoadBalancerIngressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435ac57b94efa8271d5916142783582bac6bcc17e2fe605ac76b9c4571ff8005)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceV1StatusLoadBalancerIngressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f311300928c202b6bc900db5ea2b17148a709f5f3c19e5fa5a2958b37e94411c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10547a55a6fcdac515b8448286560312ac4f34b30424bf9942d5512895e1d58b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51b061afafcb2e05535004f04f9c5a5d2f7d0b3ae0a989bcc23ce4c6185ff39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceV1StatusLoadBalancerIngressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusLoadBalancerIngressOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec63e56300ffe6897ea20e6a6a77339195c712c1deb7a330d5d0f54ab5731574)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceV1StatusLoadBalancerIngress]:
        return typing.cast(typing.Optional[ServiceV1StatusLoadBalancerIngress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceV1StatusLoadBalancerIngress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10446b31e7f3777c7904226e4bc30d9cf316fb54f64805d505386bbc59add5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceV1StatusLoadBalancerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusLoadBalancerList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022b79b1f31ea7c98b0d512c9baddad4112efdcb463b12b15086e05f6ea38017)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceV1StatusLoadBalancerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73994cee36bd3431a7b4dfef1aca42168dd8c7f3f97eaf6b4bb4e89db4a470bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceV1StatusLoadBalancerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0d3827cde134874502a81b0260b9e61f9943c87a812339837d4d41e8d8bc9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52dcab8a278a946a737e73045bce5b8c79f906627fa305faead4bdc51627421f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece32bd0136a7dd277712e4dd589090cbb144a5d63fdb153371f8c7a4f588395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceV1StatusLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusLoadBalancerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__870b2e378555ff332f43def77772a7e2a8a6e545aeb9312e3cd0a7a4f2bf303d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> ServiceV1StatusLoadBalancerIngressList:
        return typing.cast(ServiceV1StatusLoadBalancerIngressList, jsii.get(self, "ingress"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceV1StatusLoadBalancer]:
        return typing.cast(typing.Optional[ServiceV1StatusLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceV1StatusLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a691ffa07381161c1354163200fee3d2395bb5ffd8be6e162424caf64ad53172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceV1StatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1StatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821ddea5933d0e4c93516fcb846a821f85417de8fd99a652b81ef5a88354508f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> ServiceV1StatusLoadBalancerList:
        return typing.cast(ServiceV1StatusLoadBalancerList, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceV1Status]:
        return typing.cast(typing.Optional[ServiceV1Status], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceV1Status]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec793d6c657feb20687f2819c6e83ed3bd227adca7532849af4b07f455bd552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class ServiceV1Timeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#create ServiceV1#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecfb921f488e0e74f85a788f7a246a9b2431bf0241c58aed59c451d350874df)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service_v1#create ServiceV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.serviceV1.ServiceV1TimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d88988a3cc296530e4505e440f274ad9c1776c95c084335ccb80c1555f1a1d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7dfa1e88d86021337ee03dfc36de23b7c3244df370fd8e47b5ed0a16d7620e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66822ec4f7307f3ca65947ac333f9ea96e1d496f0886d67fc4682e7805b983e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceV1",
    "ServiceV1Config",
    "ServiceV1Metadata",
    "ServiceV1MetadataOutputReference",
    "ServiceV1Spec",
    "ServiceV1SpecOutputReference",
    "ServiceV1SpecPort",
    "ServiceV1SpecPortList",
    "ServiceV1SpecPortOutputReference",
    "ServiceV1SpecSessionAffinityConfig",
    "ServiceV1SpecSessionAffinityConfigClientIp",
    "ServiceV1SpecSessionAffinityConfigClientIpOutputReference",
    "ServiceV1SpecSessionAffinityConfigOutputReference",
    "ServiceV1Status",
    "ServiceV1StatusList",
    "ServiceV1StatusLoadBalancer",
    "ServiceV1StatusLoadBalancerIngress",
    "ServiceV1StatusLoadBalancerIngressList",
    "ServiceV1StatusLoadBalancerIngressOutputReference",
    "ServiceV1StatusLoadBalancerList",
    "ServiceV1StatusLoadBalancerOutputReference",
    "ServiceV1StatusOutputReference",
    "ServiceV1Timeouts",
    "ServiceV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fd25b5bf030af8231b92b976a7f992f294b0f19cab615956ef90d02096ced18e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[ServiceV1Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[ServiceV1Spec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServiceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b3d32d7c038d1cc64564344267b770df921cf084da1dc66f077bd0abcebca1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220df1537103c6d6ad5fefab4772872db1ea5b69081f92b59805e15b396c1c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4582786322dde4c8a1732d85a5ff03c7b65afb77c2933b2f5873c651ce3782(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2434a51f0d3891964eaa18e3df29abb22c7ecb1dc3c81917b48a0dc98581fc9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[ServiceV1Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[ServiceV1Spec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServiceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b999aebc92d9053c6cce2f9605bb607a0d48dae7ae47015683dd19d3674c3faa(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    generate_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c891424df43c2772f1a226f7b26444e464041bb6fa53bebfa7789a31f487740(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278ffc45a99b3c47e209ea81565eb4a79301ca3466a17431542207c8602bdc52(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea202fa16c5efb4ac087cd8ec549d363ed4520f3d38d4e31516371b2d1133907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9606d085aad03e2b625b2b333bc98696465b111da729fe5a3920d9d4b31b9fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d51b1332c9df6fffa7fcd8a7bddd1e552bb890db406b6c0d22b4bee7a079d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc23532b529a03f27fc7b718fb24b75c8665e32eddf0223d1ba2f147182e4904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fe3ef01387a6617c2ab3d169a76e85f403e1eda5d51de228d6a8272e3f276c(
    value: typing.Optional[ServiceV1Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c08e6559c669a32a313c2a252105320fb247b9628140759f119a52c2f53f9b1(
    *,
    allocate_load_balancer_node_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cluster_ip: typing.Optional[builtins.str] = None,
    cluster_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_traffic_policy: typing.Optional[builtins.str] = None,
    health_check_node_port: typing.Optional[jsii.Number] = None,
    internal_traffic_policy: typing.Optional[builtins.str] = None,
    ip_families: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_family_policy: typing.Optional[builtins.str] = None,
    load_balancer_class: typing.Optional[builtins.str] = None,
    load_balancer_ip: typing.Optional[builtins.str] = None,
    load_balancer_source_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceV1SpecPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    publish_not_ready_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_config: typing.Optional[typing.Union[ServiceV1SpecSessionAffinityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ceedad0bd9e6ce21137cce3c5a8062fdcd04666a40a0c47aba25f2e5c777ca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f72698e3ee4b25244a891218d39e76a4164177a1329cfed05e32a29cfabb560(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceV1SpecPort, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b3a4f43b915d509ec73450fb7cd9f9765b09e53c42a9ad7940fcf7026af7ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49414e9d030c37b71d376384551ff8327eda937f3717031b249ba37a95a55bcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff74915daa373580bb906174f7b87153ea4bd7ccc6fd801286cc6c7b21b0c7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de8374d54217757181c1ec1ead1e0cc16cfc1ed27d9fd933125bbd466b41fed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c885aa41c69e98a41d0eb16e494c445464df1bd689461c2eccc114b59287296f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09e3c724e250f6268a1f605d5c9b64c30b7b40c52eb8aeef439f7d848831674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a89027695a3b77981e290ca9e7483d263c6d91c85fa4e3aaea7ca18cb3d982(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc0ad85a4ccc4bd6a77d5bc779a577e1679307ad5fc0dbc9efcb3bccf232614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28480eb425d6f9b317f93712ad7334ec1713c4f35e24c451290e51cc9b9eff17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640239701c2b6f63f6f4bef5e79b4d482c3afcd0a0cd75b22ce4037e731866bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762027c2e283b6950d1d5e6ae30975bb07c05263fbe41fda60b9fc87ce7ba387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8e45d5f7a700170956202f1d8dafae8ba4c53a428cd22fd6b3d8a34d6c632e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41ec5c0ddeb77f52b3818c16b03ec1576cc440a53cbab65a0b5cefb1f15ebf1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b7b89b0228adfeaf82660046ccbd69a1e78af16859e71a62e96bbcb4f1dcb8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c5b5aee1a068bf502b98c7a7a5ab3d119947369c0a0f142e7cc265cc7cd710(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5cf3fc6de38897df783d12bb63628d0f33b507e7a8f8b8c6ab46da17aca2d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a646512eb1e1de3774ea1903e59cd98995f1be7135ecb83c6e9c2b3715da92b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5eaa030f6fa1f16c9344517ce4cbfef53bcb7ff04012d252c5619c33da659e(
    value: typing.Optional[ServiceV1Spec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6034e310b0a934c7a10bb731ab836ba2f21e95308f3044986edc40f705b0444(
    *,
    port: jsii.Number,
    app_protocol: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    node_port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    target_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a88fc6c49ddaf3d3ef0567c44d2e7df54de54b7290487b1ed79002bf130ea54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db7bfadb0fe15433a429e732b2e484f773e341c102f471b1ee52a9b00cbded0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb35ffd284a6963f38dbdee285fed03f1b331a3b2e7fb02d44c8deeb6c1913e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61de6fe607b52f573f31655e8a52765f09de0335a74cc5f7d016705d398e21c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26b3f11dcf0fa5ff9a6156a2e4de8520add74e07116190fe7f3017f2e28c533(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5d0d26a8ffe6f489628b67e13d08442c3f7d5322780b6647b6ba3f4d43fc86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceV1SpecPort]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b73e83f2c854df7f5fd6691a26cb191e14c7cccb389f5682ecbbc7ff365a2d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5396face1dacd159402a5f08e6a7a28b2586b0b71fd8742cdba8518af9ad128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228030f79412d26b5280a0958ac5b955bb6be350fb5a281cc0c02cdbf371332b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74242269ca08f08268f1c7da61970347f15eddaaee4a410654fe571f2e9c5dfa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f865ed8b3f522f46d8c6ab945b091cd7c24d4b480f3677938dfce43532e9f980(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd73f865716d5c04aefe09dc954ec81d7fe98c32cba21b60ddb651482b39f73e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0959522591f84cda19e914de82203fe9923643295da6e6ae6504d43d231ee64f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53a77fcd86af9e862888558eb2ae55ca6f24f4984213c8aa8ce1a9ce864fe38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1SpecPort]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e47f7eda546afb9426b1226198cc1157294fabdf50b52b396ed367a555d59db(
    *,
    client_ip: typing.Optional[typing.Union[ServiceV1SpecSessionAffinityConfigClientIp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4132d0b48a783dfd49907c91a76a082f78ed288fefb0d77d9b36c900ab4757f9(
    *,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4ffecffb42fecf73cd6eb9b2f896c8b6efee8775c419285657a8c49ba0c4bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fecc1fc4bb52a44bdb116c7da2e734080cafc56d73e21b6fb1e8d7dbad23fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc671dcf667cba2f0a092857e2bd5389bb366e0e4b94bd39a8c2f2e1fae4f22(
    value: typing.Optional[ServiceV1SpecSessionAffinityConfigClientIp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce34a6d0b2f9870ade546c4c44125a303d527f9f186f4116ff9d6b9bde3021a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b760d9b868daf797d8b598bed4dbfc3fcf865f3726e975a9fd3bb4328d367b(
    value: typing.Optional[ServiceV1SpecSessionAffinityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c46f67afd2d5ba007968b8334bd965babd8add8bcb3242e32d3c2ff02c17f90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490a591a607b73f70cddb851e987208e0c717a24c0709a4379628445768eddcb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e65ca138038ce65963a5c57867a7afad81bc7f5ad22b4e1da01099c5db23831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c659a722792e4d754f20fe315ff1241938bc507d9d4abed35104fcff2e7d5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc281df5c675d23fca807d077ace2b8e80aacc34f6eacf747e6d64debc31df86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1532644df8d85abf39ebdcf6dac6fb559954f8d6aa0377875f1486d47f55e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435ac57b94efa8271d5916142783582bac6bcc17e2fe605ac76b9c4571ff8005(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f311300928c202b6bc900db5ea2b17148a709f5f3c19e5fa5a2958b37e94411c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10547a55a6fcdac515b8448286560312ac4f34b30424bf9942d5512895e1d58b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51b061afafcb2e05535004f04f9c5a5d2f7d0b3ae0a989bcc23ce4c6185ff39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec63e56300ffe6897ea20e6a6a77339195c712c1deb7a330d5d0f54ab5731574(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10446b31e7f3777c7904226e4bc30d9cf316fb54f64805d505386bbc59add5c(
    value: typing.Optional[ServiceV1StatusLoadBalancerIngress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022b79b1f31ea7c98b0d512c9baddad4112efdcb463b12b15086e05f6ea38017(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73994cee36bd3431a7b4dfef1aca42168dd8c7f3f97eaf6b4bb4e89db4a470bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0d3827cde134874502a81b0260b9e61f9943c87a812339837d4d41e8d8bc9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dcab8a278a946a737e73045bce5b8c79f906627fa305faead4bdc51627421f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece32bd0136a7dd277712e4dd589090cbb144a5d63fdb153371f8c7a4f588395(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870b2e378555ff332f43def77772a7e2a8a6e545aeb9312e3cd0a7a4f2bf303d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a691ffa07381161c1354163200fee3d2395bb5ffd8be6e162424caf64ad53172(
    value: typing.Optional[ServiceV1StatusLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821ddea5933d0e4c93516fcb846a821f85417de8fd99a652b81ef5a88354508f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec793d6c657feb20687f2819c6e83ed3bd227adca7532849af4b07f455bd552(
    value: typing.Optional[ServiceV1Status],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecfb921f488e0e74f85a788f7a246a9b2431bf0241c58aed59c451d350874df(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d88988a3cc296530e4505e440f274ad9c1776c95c084335ccb80c1555f1a1d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7dfa1e88d86021337ee03dfc36de23b7c3244df370fd8e47b5ed0a16d7620e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66822ec4f7307f3ca65947ac333f9ea96e1d496f0886d67fc4682e7805b983e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
