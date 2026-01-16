r'''
# `kubernetes_service`

Refer to the Terraform Registry for docs: [`kubernetes_service`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service).
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


class Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service kubernetes_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["ServiceMetadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["ServiceSpec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service kubernetes_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#metadata Service#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#spec Service#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#timeouts Service#timeouts}
        :param wait_for_load_balancer: Terraform will wait for the load balancer to have at least 1 endpoint before considering the resource created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#wait_for_load_balancer Service#wait_for_load_balancer}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd008ce3bf3e1676fb7c7c3450a677661030ea72a9841944d417ab1f8b5b6da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceConfig(
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
        '''Generates CDKTF code for importing a Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Service to import.
        :param import_from_id: The id of the existing Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a696767454137e1e7b13e4d4934f71f723d16bbf7d51b71611f05e059086d408)
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
        :param annotations: An unstructured key value map stored with the service that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#annotations Service#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#generate_name Service#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the service. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#labels Service#labels}
        :param name: Name of the service, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#name Service#name}
        :param namespace: Namespace defines the space within which name of the service must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#namespace Service#namespace}
        '''
        value = ServiceMetadata(
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
        port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceSpecPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        publish_not_ready_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_config: typing.Optional[typing.Union["ServiceSpecSessionAffinityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocate_load_balancer_node_ports: Defines if ``NodePorts`` will be automatically allocated for services with type ``LoadBalancer``. It may be set to ``false`` if the cluster load-balancer does not rely on ``NodePorts``. If the caller requests specific ``NodePorts`` (by specifying a value), those requests will be respected, regardless of this field. This field may only be set for services with type ``LoadBalancer``. Default is ``true``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-nodeport-allocation Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#allocate_load_balancer_node_ports Service#allocate_load_balancer_node_ports}
        :param cluster_ip: The IP address of the service. It is usually assigned randomly by the master. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise, creation of the service will fail. ``None`` can be specified for headless services when proxying is not required. Ignored if type is ``ExternalName``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#cluster_ip Service#cluster_ip}
        :param cluster_ips: List of IP addresses assigned to this service, and are usually assigned randomly. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise creation of the service will fail. If this field is not specified, it will be initialized from the ``clusterIP`` field. If this field is specified, clients must ensure that ``clusterIPs[0]`` and ``clusterIP`` have the same value. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#cluster_ips Service#cluster_ips}
        :param external_ips: A list of IP addresses for which nodes in the cluster will also accept traffic for this service. These IPs are not managed by Kubernetes. The user is responsible for ensuring that traffic arrives at a node with this IP. A common example is external load-balancers that are not part of the Kubernetes system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_ips Service#external_ips}
        :param external_name: The external reference that kubedns or equivalent will return as a CNAME record for this service. No proxying will be involved. Must be a valid DNS name and requires ``type`` to be ``ExternalName``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_name Service#external_name}
        :param external_traffic_policy: Denotes if this Service desires to route external traffic to node-local or cluster-wide endpoints. ``Local`` preserves the client source IP and avoids a second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced traffic spreading. ``Cluster`` obscures the client source IP and may cause a second hop to another node, but should have good overall load-spreading. More info: https://kubernetes.io/docs/tutorials/services/source-ip/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_traffic_policy Service#external_traffic_policy}
        :param health_check_node_port: Specifies the Healthcheck NodePort for the service. Only effects when type is set to ``LoadBalancer`` and external_traffic_policy is set to ``Local``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#health_check_node_port Service#health_check_node_port}
        :param internal_traffic_policy: Specifies if the cluster internal traffic should be routed to all endpoints or node-local endpoints only. ``Cluster`` routes internal traffic to a Service to all endpoints. ``Local`` routes traffic to node-local endpoints only, traffic is dropped if no node-local endpoints are ready. The default value is ``Cluster``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#internal_traffic_policy Service#internal_traffic_policy}
        :param ip_families: IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this service. This field is usually assigned automatically based on cluster configuration and the ipFamilyPolicy field. If this field is specified manually, the requested family is available in the cluster, and ipFamilyPolicy allows it, it will be used; otherwise creation of the service will fail. This field is conditionally mutable: it allows for adding or removing a secondary IP family, but it does not allow changing the primary IP family of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#ip_families Service#ip_families}
        :param ip_family_policy: IPFamilyPolicy represents the dual-stack-ness requested or required by this Service. If there is no value provided, then this field will be set to SingleStack. Services can be 'SingleStack' (a single IP family), 'PreferDualStack' (two IP families on dual-stack configured clusters or a single IP family on single-stack clusters), or 'RequireDualStack' (two IP families on dual-stack configured clusters, otherwise fail). The ipFamilies and clusterIPs fields depend on the value of this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#ip_family_policy Service#ip_family_policy}
        :param load_balancer_class: The class of the load balancer implementation this Service belongs to. If specified, the value of this field must be a label-style identifier, with an optional prefix. This field can only be set when the Service type is ``LoadBalancer``. If not set, the default load balancer implementation is used. This field can only be set when creating or updating a Service to type ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_class Service#load_balancer_class}
        :param load_balancer_ip: Only applies to ``type = LoadBalancer``. LoadBalancer will get created with the IP specified in this field. This feature depends on whether the underlying cloud-provider supports specifying this field when a load balancer is created. This field will be ignored if the cloud-provider does not support the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_ip Service#load_balancer_ip}
        :param load_balancer_source_ranges: If specified and supported by the platform, this will restrict traffic through the cloud-provider load-balancer will be restricted to the specified client IPs. This field will be ignored if the cloud-provider does not support the feature. More info: http://kubernetes.io/docs/user-guide/services-firewalls Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_source_ranges Service#load_balancer_source_ranges}
        :param port: port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#port Service#port}
        :param publish_not_ready_addresses: When set to true, indicates that DNS implementations must publish the ``notReadyAddresses`` of subsets for the Endpoints associated with the Service. The default value is ``false``. The primary use case for setting this field is to use a StatefulSet's Headless Service to propagate ``SRV`` records for its Pods without respect to their readiness for purpose of peer discovery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#publish_not_ready_addresses Service#publish_not_ready_addresses}
        :param selector: Route service traffic to pods with label keys and values matching this selector. Only applies to types ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#selector Service#selector}
        :param session_affinity: Used to maintain session affinity. Supports ``ClientIP`` and ``None``. Defaults to ``None``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#session_affinity Service#session_affinity}
        :param session_affinity_config: session_affinity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#session_affinity_config Service#session_affinity_config}
        :param type: Determines how the service is exposed. Defaults to ``ClusterIP``. Valid options are ``ExternalName``, ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. ``ExternalName`` maps to the specified ``external_name``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#type Service#type}
        '''
        value = ServiceSpec(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#create Service#create}.
        '''
        value = ServiceTimeouts(create=create)

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
    def metadata(self) -> "ServiceMetadataOutputReference":
        return typing.cast("ServiceMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "ServiceSpecOutputReference":
        return typing.cast("ServiceSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "ServiceStatusList":
        return typing.cast("ServiceStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServiceTimeoutsOutputReference":
        return typing.cast("ServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["ServiceMetadata"]:
        return typing.cast(typing.Optional["ServiceMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["ServiceSpec"]:
        return typing.cast(typing.Optional["ServiceSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8f17e7261e16afc04cc163778440580134d52467613e83eb7c797d237e87cab1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c698fa72cc9dab13715a178498c5a5464dc33712e24cae0de0c51c64263c2ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForLoadBalancer", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceConfig",
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
class ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["ServiceMetadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["ServiceSpec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#metadata Service#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#spec Service#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#timeouts Service#timeouts}
        :param wait_for_load_balancer: Terraform will wait for the load balancer to have at least 1 endpoint before considering the resource created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#wait_for_load_balancer Service#wait_for_load_balancer}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = ServiceMetadata(**metadata)
        if isinstance(spec, dict):
            spec = ServiceSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = ServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba11ba943e603fa66c1ce5ee16e709bc80fa32b1495f40c86a8180c82e77446c)
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
    def metadata(self) -> "ServiceMetadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#metadata Service#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("ServiceMetadata", result)

    @builtins.property
    def spec(self) -> "ServiceSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#spec Service#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("ServiceSpec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#id Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#timeouts Service#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServiceTimeouts"], result)

    @builtins.property
    def wait_for_load_balancer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Terraform will wait for the load balancer to have at least 1 endpoint before considering the resource created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#wait_for_load_balancer Service#wait_for_load_balancer}
        '''
        result = self._values.get("wait_for_load_balancer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class ServiceMetadata:
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
        :param annotations: An unstructured key value map stored with the service that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#annotations Service#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#generate_name Service#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the service. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#labels Service#labels}
        :param name: Name of the service, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#name Service#name}
        :param namespace: Namespace defines the space within which name of the service must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#namespace Service#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030fa05aa2dbce94b3c89f8f5393694a52c244bdb487944a20a24c12fd7e1937)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#annotations Service#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        '''Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided.

        This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#generate_name Service#generate_name}
        '''
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the service.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the service, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within which name of the service must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#namespace Service#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df400b5c531735276c42b78e9c85e10d73488a0b6c2755ce90744b3d7e027d20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0efab969de4fef3f53a4a21e98e369c3dd22060e4694fd8936a892f7cdaf7497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generateName")
    def generate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateName"))

    @generate_name.setter
    def generate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7a7b3dc7174a682965eb66fefcd3c4bcd4708d83f74b1804c34e306401aa94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a3b19495eef4ba76ebd2dfef77386b0ad113bc53a1465bcf32a9bd5226a786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d9f3d44fffea9e247772fcdd6758d364e4ec045fc4e896299763b9414b1b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6114dd91e26f30f91e517fa016b20063ed4afa400e7af779af6a554fecc43964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceMetadata]:
        return typing.cast(typing.Optional[ServiceMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceMetadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077ede6a7a5b1da676735323e71c99d21046d6c6cecf11cb3c27c916f624920f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpec",
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
class ServiceSpec:
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
        port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceSpecPort", typing.Dict[builtins.str, typing.Any]]]]] = None,
        publish_not_ready_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        session_affinity_config: typing.Optional[typing.Union["ServiceSpecSessionAffinityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocate_load_balancer_node_ports: Defines if ``NodePorts`` will be automatically allocated for services with type ``LoadBalancer``. It may be set to ``false`` if the cluster load-balancer does not rely on ``NodePorts``. If the caller requests specific ``NodePorts`` (by specifying a value), those requests will be respected, regardless of this field. This field may only be set for services with type ``LoadBalancer``. Default is ``true``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-nodeport-allocation Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#allocate_load_balancer_node_ports Service#allocate_load_balancer_node_ports}
        :param cluster_ip: The IP address of the service. It is usually assigned randomly by the master. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise, creation of the service will fail. ``None`` can be specified for headless services when proxying is not required. Ignored if type is ``ExternalName``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#cluster_ip Service#cluster_ip}
        :param cluster_ips: List of IP addresses assigned to this service, and are usually assigned randomly. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise creation of the service will fail. If this field is not specified, it will be initialized from the ``clusterIP`` field. If this field is specified, clients must ensure that ``clusterIPs[0]`` and ``clusterIP`` have the same value. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#cluster_ips Service#cluster_ips}
        :param external_ips: A list of IP addresses for which nodes in the cluster will also accept traffic for this service. These IPs are not managed by Kubernetes. The user is responsible for ensuring that traffic arrives at a node with this IP. A common example is external load-balancers that are not part of the Kubernetes system. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_ips Service#external_ips}
        :param external_name: The external reference that kubedns or equivalent will return as a CNAME record for this service. No proxying will be involved. Must be a valid DNS name and requires ``type`` to be ``ExternalName``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_name Service#external_name}
        :param external_traffic_policy: Denotes if this Service desires to route external traffic to node-local or cluster-wide endpoints. ``Local`` preserves the client source IP and avoids a second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced traffic spreading. ``Cluster`` obscures the client source IP and may cause a second hop to another node, but should have good overall load-spreading. More info: https://kubernetes.io/docs/tutorials/services/source-ip/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_traffic_policy Service#external_traffic_policy}
        :param health_check_node_port: Specifies the Healthcheck NodePort for the service. Only effects when type is set to ``LoadBalancer`` and external_traffic_policy is set to ``Local``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#health_check_node_port Service#health_check_node_port}
        :param internal_traffic_policy: Specifies if the cluster internal traffic should be routed to all endpoints or node-local endpoints only. ``Cluster`` routes internal traffic to a Service to all endpoints. ``Local`` routes traffic to node-local endpoints only, traffic is dropped if no node-local endpoints are ready. The default value is ``Cluster``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#internal_traffic_policy Service#internal_traffic_policy}
        :param ip_families: IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this service. This field is usually assigned automatically based on cluster configuration and the ipFamilyPolicy field. If this field is specified manually, the requested family is available in the cluster, and ipFamilyPolicy allows it, it will be used; otherwise creation of the service will fail. This field is conditionally mutable: it allows for adding or removing a secondary IP family, but it does not allow changing the primary IP family of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#ip_families Service#ip_families}
        :param ip_family_policy: IPFamilyPolicy represents the dual-stack-ness requested or required by this Service. If there is no value provided, then this field will be set to SingleStack. Services can be 'SingleStack' (a single IP family), 'PreferDualStack' (two IP families on dual-stack configured clusters or a single IP family on single-stack clusters), or 'RequireDualStack' (two IP families on dual-stack configured clusters, otherwise fail). The ipFamilies and clusterIPs fields depend on the value of this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#ip_family_policy Service#ip_family_policy}
        :param load_balancer_class: The class of the load balancer implementation this Service belongs to. If specified, the value of this field must be a label-style identifier, with an optional prefix. This field can only be set when the Service type is ``LoadBalancer``. If not set, the default load balancer implementation is used. This field can only be set when creating or updating a Service to type ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_class Service#load_balancer_class}
        :param load_balancer_ip: Only applies to ``type = LoadBalancer``. LoadBalancer will get created with the IP specified in this field. This feature depends on whether the underlying cloud-provider supports specifying this field when a load balancer is created. This field will be ignored if the cloud-provider does not support the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_ip Service#load_balancer_ip}
        :param load_balancer_source_ranges: If specified and supported by the platform, this will restrict traffic through the cloud-provider load-balancer will be restricted to the specified client IPs. This field will be ignored if the cloud-provider does not support the feature. More info: http://kubernetes.io/docs/user-guide/services-firewalls Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_source_ranges Service#load_balancer_source_ranges}
        :param port: port block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#port Service#port}
        :param publish_not_ready_addresses: When set to true, indicates that DNS implementations must publish the ``notReadyAddresses`` of subsets for the Endpoints associated with the Service. The default value is ``false``. The primary use case for setting this field is to use a StatefulSet's Headless Service to propagate ``SRV`` records for its Pods without respect to their readiness for purpose of peer discovery. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#publish_not_ready_addresses Service#publish_not_ready_addresses}
        :param selector: Route service traffic to pods with label keys and values matching this selector. Only applies to types ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#selector Service#selector}
        :param session_affinity: Used to maintain session affinity. Supports ``ClientIP`` and ``None``. Defaults to ``None``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#session_affinity Service#session_affinity}
        :param session_affinity_config: session_affinity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#session_affinity_config Service#session_affinity_config}
        :param type: Determines how the service is exposed. Defaults to ``ClusterIP``. Valid options are ``ExternalName``, ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. ``ExternalName`` maps to the specified ``external_name``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#type Service#type}
        '''
        if isinstance(session_affinity_config, dict):
            session_affinity_config = ServiceSpecSessionAffinityConfig(**session_affinity_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc8e29de680350ab23df99e1d77eafbd6203186a180ecf959a50f497b86889b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#allocate_load_balancer_node_ports Service#allocate_load_balancer_node_ports}
        '''
        result = self._values.get("allocate_load_balancer_node_ports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cluster_ip(self) -> typing.Optional[builtins.str]:
        '''The IP address of the service.

        It is usually assigned randomly by the master. If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise, creation of the service will fail. ``None`` can be specified for headless services when proxying is not required. Ignored if type is ``ExternalName``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#cluster_ip Service#cluster_ip}
        '''
        result = self._values.get("cluster_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IP addresses assigned to this service, and are usually assigned randomly.

        If an address is specified manually and is not in use by others, it will be allocated to the service; otherwise creation of the service will fail. If this field is not specified, it will be initialized from the ``clusterIP`` field. If this field is specified, clients must ensure that ``clusterIPs[0]`` and ``clusterIP`` have the same value. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#cluster_ips Service#cluster_ips}
        '''
        result = self._values.get("cluster_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IP addresses for which nodes in the cluster will also accept traffic for this service.

        These IPs are not managed by Kubernetes. The user is responsible for ensuring that traffic arrives at a node with this IP.  A common example is external load-balancers that are not part of the Kubernetes system.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_ips Service#external_ips}
        '''
        result = self._values.get("external_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_name(self) -> typing.Optional[builtins.str]:
        '''The external reference that kubedns or equivalent will return as a CNAME record for this service.

        No proxying will be involved. Must be a valid DNS name and requires ``type`` to be ``ExternalName``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_name Service#external_name}
        '''
        result = self._values.get("external_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_traffic_policy(self) -> typing.Optional[builtins.str]:
        '''Denotes if this Service desires to route external traffic to node-local or cluster-wide endpoints.

        ``Local`` preserves the client source IP and avoids a second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced traffic spreading. ``Cluster`` obscures the client source IP and may cause a second hop to another node, but should have good overall load-spreading. More info: https://kubernetes.io/docs/tutorials/services/source-ip/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#external_traffic_policy Service#external_traffic_policy}
        '''
        result = self._values.get("external_traffic_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_node_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the Healthcheck NodePort for the service.

        Only effects when type is set to ``LoadBalancer`` and external_traffic_policy is set to ``Local``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#health_check_node_port Service#health_check_node_port}
        '''
        result = self._values.get("health_check_node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def internal_traffic_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies if the cluster internal traffic should be routed to all endpoints or node-local endpoints only.

        ``Cluster`` routes internal traffic to a Service to all endpoints. ``Local`` routes traffic to node-local endpoints only, traffic is dropped if no node-local endpoints are ready. The default value is ``Cluster``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#internal_traffic_policy Service#internal_traffic_policy}
        '''
        result = self._values.get("internal_traffic_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_families(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IPFamilies is a list of IP families (e.g. IPv4, IPv6) assigned to this service. This field is usually assigned automatically based on cluster configuration and the ipFamilyPolicy field. If this field is specified manually, the requested family is available in the cluster, and ipFamilyPolicy allows it, it will be used; otherwise creation of the service will fail. This field is conditionally mutable: it allows for adding or removing a secondary IP family, but it does not allow changing the primary IP family of the Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#ip_families Service#ip_families}
        '''
        result = self._values.get("ip_families")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_family_policy(self) -> typing.Optional[builtins.str]:
        '''IPFamilyPolicy represents the dual-stack-ness requested or required by this Service.

        If there is no value provided, then this field will be set to SingleStack. Services can be 'SingleStack' (a single IP family), 'PreferDualStack' (two IP families on dual-stack configured clusters or a single IP family on single-stack clusters), or 'RequireDualStack' (two IP families on dual-stack configured clusters, otherwise fail). The ipFamilies and clusterIPs fields depend on the value of this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#ip_family_policy Service#ip_family_policy}
        '''
        result = self._values.get("ip_family_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_class(self) -> typing.Optional[builtins.str]:
        '''The class of the load balancer implementation this Service belongs to.

        If specified, the value of this field must be a label-style identifier, with an optional prefix. This field can only be set when the Service type is ``LoadBalancer``. If not set, the default load balancer implementation is used. This field can only be set when creating or updating a Service to type ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancer-class

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_class Service#load_balancer_class}
        '''
        result = self._values.get("load_balancer_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_ip(self) -> typing.Optional[builtins.str]:
        '''Only applies to ``type = LoadBalancer``.

        LoadBalancer will get created with the IP specified in this field. This feature depends on whether the underlying cloud-provider supports specifying this field when a load balancer is created. This field will be ignored if the cloud-provider does not support the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_ip Service#load_balancer_ip}
        '''
        result = self._values.get("load_balancer_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_source_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If specified and supported by the platform, this will restrict traffic through the cloud-provider load-balancer will be restricted to the specified client IPs.

        This field will be ignored if the cloud-provider does not support the feature. More info: http://kubernetes.io/docs/user-guide/services-firewalls

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#load_balancer_source_ranges Service#load_balancer_source_ranges}
        '''
        result = self._values.get("load_balancer_source_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def port(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceSpecPort"]]]:
        '''port block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#port Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceSpecPort"]]], result)

    @builtins.property
    def publish_not_ready_addresses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, indicates that DNS implementations must publish the ``notReadyAddresses`` of subsets for the Endpoints associated with the Service.

        The default value is ``false``. The primary use case for setting this field is to use a StatefulSet's Headless Service to propagate ``SRV`` records for its Pods without respect to their readiness for purpose of peer discovery.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#publish_not_ready_addresses Service#publish_not_ready_addresses}
        '''
        result = self._values.get("publish_not_ready_addresses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selector(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Route service traffic to pods with label keys and values matching this selector.

        Only applies to types ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. More info: https://kubernetes.io/docs/concepts/services-networking/service/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#selector Service#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Used to maintain session affinity. Supports ``ClientIP`` and ``None``. Defaults to ``None``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#session_affinity Service#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity_config(
        self,
    ) -> typing.Optional["ServiceSpecSessionAffinityConfig"]:
        '''session_affinity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#session_affinity_config Service#session_affinity_config}
        '''
        result = self._values.get("session_affinity_config")
        return typing.cast(typing.Optional["ServiceSpecSessionAffinityConfig"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Determines how the service is exposed.

        Defaults to ``ClusterIP``. Valid options are ``ExternalName``, ``ClusterIP``, ``NodePort``, and ``LoadBalancer``. ``ExternalName`` maps to the specified ``external_name``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#type Service#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa30d40e000dcf38d7b5f2a45beb1a0e8311605649a5fff128432f234596d543)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPort")
    def put_port(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceSpecPort", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e11f4a066b96c9587e356af83798ae7e22d04e9b95243fe62fd8e5e1b33b224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPort", [value]))

    @jsii.member(jsii_name="putSessionAffinityConfig")
    def put_session_affinity_config(
        self,
        *,
        client_ip: typing.Optional[typing.Union["ServiceSpecSessionAffinityConfigClientIp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip: client_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#client_ip Service#client_ip}
        '''
        value = ServiceSpecSessionAffinityConfig(client_ip=client_ip)

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
    def port(self) -> "ServiceSpecPortList":
        return typing.cast("ServiceSpecPortList", jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityConfig")
    def session_affinity_config(
        self,
    ) -> "ServiceSpecSessionAffinityConfigOutputReference":
        return typing.cast("ServiceSpecSessionAffinityConfigOutputReference", jsii.get(self, "sessionAffinityConfig"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceSpecPort"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceSpecPort"]]], jsii.get(self, "portInput"))

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
    ) -> typing.Optional["ServiceSpecSessionAffinityConfig"]:
        return typing.cast(typing.Optional["ServiceSpecSessionAffinityConfig"], jsii.get(self, "sessionAffinityConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__11ec216fb649a605bcf9eef8afd954914842c9e5f852e8e17da903660e10c58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocateLoadBalancerNodePorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIp")
    def cluster_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIp"))

    @cluster_ip.setter
    def cluster_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4571a7a23933440891babd691f66c89853320abb9af15d1b81f9e75df710884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIps")
    def cluster_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterIps"))

    @cluster_ips.setter
    def cluster_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d493d6c65eeb045c1fa18638556076d8a9e42c4dfd807cf63c011e17a829039b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalIps")
    def external_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalIps"))

    @external_ips.setter
    def external_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b312af3e801d83c3044dcf1db126dba39ee0510c8ff502bedd265c81a67786d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalName")
    def external_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalName"))

    @external_name.setter
    def external_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a0b9b9ddc58b461b41bd953c002c0bccb922a9fec39c837ce7c7721d91098a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalTrafficPolicy")
    def external_traffic_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalTrafficPolicy"))

    @external_traffic_policy.setter
    def external_traffic_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915affc6d7baf640cafb742e96b7e7a2cd17cf66aadf99de4f715a44a4403df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalTrafficPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckNodePort")
    def health_check_node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckNodePort"))

    @health_check_node_port.setter
    def health_check_node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7648b06b0429bc87d87d2773365dad99aba684cfcd5d8168e07c2f538ae59c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckNodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalTrafficPolicy")
    def internal_traffic_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalTrafficPolicy"))

    @internal_traffic_policy.setter
    def internal_traffic_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d014e943da791c1c7652e8ccfe865725d5e69ff2f0fd0c33a899e15d9939b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalTrafficPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipFamilies")
    def ip_families(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipFamilies"))

    @ip_families.setter
    def ip_families(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cf2b2578cdff993f80f0985a0c650ce04fb188ae339b2ca2654a44c32a36d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFamilies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipFamilyPolicy")
    def ip_family_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipFamilyPolicy"))

    @ip_family_policy.setter
    def ip_family_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7cea9197838d6d7e3f204ec75f97a09631614d4e5ed599e3bcdce9d5134b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFamilyPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerClass")
    def load_balancer_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerClass"))

    @load_balancer_class.setter
    def load_balancer_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79a8b5478df37ed6c7562a850f9c95c89000e5626df8fe1c244ca195e8fde23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerIp")
    def load_balancer_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerIp"))

    @load_balancer_ip.setter
    def load_balancer_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d891655cf222711a78d515313a16f748cf86d8a4091de5919172948d62e00b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSourceRanges")
    def load_balancer_source_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loadBalancerSourceRanges"))

    @load_balancer_source_ranges.setter
    def load_balancer_source_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66cf87f896278051ca4ed10f9609c8db4859b056a448ab243afb9be509440d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a733f2feb2d2e1467b8267287ad40b0c4a33ec4aeaed50f322a333947900b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishNotReadyAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f80d5c40b5220cd865dc9a0d796ad8025b9b5202b2aca16d8d1946d711c7b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2481a60c25504ff1c4c3e7fdf305bba580f88c3587477e7f2ceb0645d75d23fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fb9680bd95ff5d74f22bcc5791aa8a0cf1dff7f48efb29e8040219fad21c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceSpec]:
        return typing.cast(typing.Optional[ServiceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553fcdf282a2243ae565ddaf709866b21edb44a44d2a30e2609f984bd85ffeb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecPort",
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
class ServiceSpecPort:
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
        :param port: The port that will be exposed by this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#port Service#port}
        :param app_protocol: The application protocol for this port. This field follows standard Kubernetes label syntax. Un-prefixed names are reserved for IANA standard service names (as per RFC-6335 and http://www.iana.org/assignments/service-names). Non-standard protocols should use prefixed names such as mycompany.com/my-custom-protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#app_protocol Service#app_protocol}
        :param name: The name of this port within the service. All ports within the service must have unique names. Optional if only one ServicePort is defined on this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#name Service#name}
        :param node_port: The port on each node on which this service is exposed when ``type`` is ``NodePort`` or ``LoadBalancer``. Usually assigned by the system. If specified, it will be allocated to the service if unused or else creation of the service will fail. Default is to auto-allocate a port if the ``type`` of this service requires one. More info: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#node_port Service#node_port}
        :param protocol: The IP protocol for this port. Supports ``TCP`` and ``UDP``. Default is ``TCP``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#protocol Service#protocol}
        :param target_port: Number or name of the port to access on the pods targeted by the service. Number must be in the range 1 to 65535. This field is ignored for services with ``cluster_ip = "None"``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#target_port Service#target_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67a5030308d9544d162ca4c79fb7477901c5fa62712c0dfd8de7f1b76117810)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#port Service#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def app_protocol(self) -> typing.Optional[builtins.str]:
        '''The application protocol for this port.

        This field follows standard Kubernetes label syntax. Un-prefixed names are reserved for IANA standard service names (as per RFC-6335 and http://www.iana.org/assignments/service-names). Non-standard protocols should use prefixed names such as mycompany.com/my-custom-protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#app_protocol Service#app_protocol}
        '''
        result = self._values.get("app_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this port within the service.

        All ports within the service must have unique names. Optional if only one ServicePort is defined on this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_port(self) -> typing.Optional[jsii.Number]:
        '''The port on each node on which this service is exposed when ``type`` is ``NodePort`` or ``LoadBalancer``.

        Usually assigned by the system. If specified, it will be allocated to the service if unused or else creation of the service will fail. Default is to auto-allocate a port if the ``type`` of this service requires one. More info: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#node_port Service#node_port}
        '''
        result = self._values.get("node_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The IP protocol for this port. Supports ``TCP`` and ``UDP``. Default is ``TCP``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#protocol Service#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_port(self) -> typing.Optional[builtins.str]:
        '''Number or name of the port to access on the pods targeted by the service.

        Number must be in the range 1 to 65535. This field is ignored for services with ``cluster_ip = "None"``. More info: https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#target_port Service#target_port}
        '''
        result = self._values.get("target_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceSpecPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceSpecPortList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecPortList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef85948dbac68520f5612cda6c1866279874444be1de74c2a20222adb66b99e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceSpecPortOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b0dcf8d67f3ba63b8612fad5aac2b6e594f56e801d8020a5e4d0f57aac17bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceSpecPortOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2623b192f1884d960eef2933de275eba860c49045ec1c00c71bd2a2997ce616)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cbc83933b318d44523453b96e105e1680f3fa93535a4f4e0d58ec439177f2bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f781cb529a10d9711a9e76d8e0b8916b01436f18b5592d25b9629ee272850ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceSpecPort]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceSpecPort]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceSpecPort]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fe910720dfb320486cc7cfb6e5fec24d223e6d83349eec87e5b3e81489f491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceSpecPortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecPortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c6016a37888dd2f2efd15b5ef1b51928d2c6bf8dadfbe0e61fa8129f0546753)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8681a9e70d8175c13389df67dbda2a288c5f412d09b50427fb41f1db1896225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1a199733e588673c24da46c2a98296b58383d146099ad60e44e5a94269e274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePort")
    def node_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodePort"))

    @node_port.setter
    def node_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcfd308fd588d1f37e6c83b6f6fcad3ec8749fc267b9b2276c4699a111b277e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6d197e0b9d7bbf41799befb0417f0c754e10ce00949a95207b5d65409d17fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2638766c43654431eba5836f0d02dcb07beae167420adde04661431fc921aa4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPort")
    def target_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPort"))

    @target_port.setter
    def target_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78be54363a21c69981694bb96c9123f96785a9efe8de192a116c3575dad9b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceSpecPort]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceSpecPort]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceSpecPort]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a33bf2995cad5067e49734b9e3b5708b57d75b5c19df12fa57b9bd5b0b7e312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecSessionAffinityConfig",
    jsii_struct_bases=[],
    name_mapping={"client_ip": "clientIp"},
)
class ServiceSpecSessionAffinityConfig:
    def __init__(
        self,
        *,
        client_ip: typing.Optional[typing.Union["ServiceSpecSessionAffinityConfigClientIp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip: client_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#client_ip Service#client_ip}
        '''
        if isinstance(client_ip, dict):
            client_ip = ServiceSpecSessionAffinityConfigClientIp(**client_ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d1806113c03976d5e93a9d9467d191d6753b5da638e75ea579511589244d95)
            check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_ip is not None:
            self._values["client_ip"] = client_ip

    @builtins.property
    def client_ip(self) -> typing.Optional["ServiceSpecSessionAffinityConfigClientIp"]:
        '''client_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#client_ip Service#client_ip}
        '''
        result = self._values.get("client_ip")
        return typing.cast(typing.Optional["ServiceSpecSessionAffinityConfigClientIp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceSpecSessionAffinityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecSessionAffinityConfigClientIp",
    jsii_struct_bases=[],
    name_mapping={"timeout_seconds": "timeoutSeconds"},
)
class ServiceSpecSessionAffinityConfigClientIp:
    def __init__(self, *, timeout_seconds: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param timeout_seconds: Specifies the seconds of ``ClientIP`` type session sticky time. The value must be > 0 and <= 86400(for 1 day) if ``ServiceAffinity`` == ``ClientIP``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#timeout_seconds Service#timeout_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9854793f986542982d4512859b0bcf5a2794912c15af30e8a5d14171c204ad)
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies the seconds of ``ClientIP`` type session sticky time.

        The value must be > 0 and <= 86400(for 1 day) if ``ServiceAffinity`` == ``ClientIP``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#timeout_seconds Service#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceSpecSessionAffinityConfigClientIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceSpecSessionAffinityConfigClientIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecSessionAffinityConfigClientIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26292440eaf19843b43c9146cead0990f17cad3dda03c40fe5a9a38237f0b95f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60fdd96289a22f209f0c135738b65ef3a3093f6ce2c0e4eb7556475e9eb597b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceSpecSessionAffinityConfigClientIp]:
        return typing.cast(typing.Optional[ServiceSpecSessionAffinityConfigClientIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceSpecSessionAffinityConfigClientIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7483bf2c215d965ea20b754df658a8439fc3c7303f091717b09025a1140b6d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceSpecSessionAffinityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceSpecSessionAffinityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__311ceef974ad26a6fa6d26fbba14834cc2bcf09ca4a463d0034578922a6c3c04)
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
        :param timeout_seconds: Specifies the seconds of ``ClientIP`` type session sticky time. The value must be > 0 and <= 86400(for 1 day) if ``ServiceAffinity`` == ``ClientIP``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#timeout_seconds Service#timeout_seconds}
        '''
        value = ServiceSpecSessionAffinityConfigClientIp(
            timeout_seconds=timeout_seconds
        )

        return typing.cast(None, jsii.invoke(self, "putClientIp", [value]))

    @jsii.member(jsii_name="resetClientIp")
    def reset_client_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIp", []))

    @builtins.property
    @jsii.member(jsii_name="clientIp")
    def client_ip(self) -> ServiceSpecSessionAffinityConfigClientIpOutputReference:
        return typing.cast(ServiceSpecSessionAffinityConfigClientIpOutputReference, jsii.get(self, "clientIp"))

    @builtins.property
    @jsii.member(jsii_name="clientIpInput")
    def client_ip_input(
        self,
    ) -> typing.Optional[ServiceSpecSessionAffinityConfigClientIp]:
        return typing.cast(typing.Optional[ServiceSpecSessionAffinityConfigClientIp], jsii.get(self, "clientIpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceSpecSessionAffinityConfig]:
        return typing.cast(typing.Optional[ServiceSpecSessionAffinityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceSpecSessionAffinityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bbe855fd5768f90c2bf6f26f7d2bb421aa88edeb438c259142f5d83b0db714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5791686b897478784055103a091c5760513cf8f2ab435681ba57adb191077267)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33771711bf9730dca02fa806748e3e7069d990c2c3e38ea008441bd5254d7d61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911f74d9c504e1ace9c5c1e7544407179cbdc5c810dcc1ece6c7c6d1d6068d23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25dab095c595561e1bc2de5d207b2c29130f320e2142d014be96694553159420)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3c86ce43b43b3efd27186cc963b38c468ae3f0d63ae40dcafeb45fe079e0bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceStatusLoadBalancer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceStatusLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusLoadBalancerIngress",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceStatusLoadBalancerIngress:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceStatusLoadBalancerIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceStatusLoadBalancerIngressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusLoadBalancerIngressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__505fdcd6d0570c41d1bda713dc18c7a5576ba596f55948e935ba0f17dc7e91c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceStatusLoadBalancerIngressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4e06495c66f2dd349578d6ed97b9c8980a28e6cb5162aba06f5e96a2d519f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceStatusLoadBalancerIngressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abfa691807f2abe79e91fa21f358c67fc253007a183c7521fbbf6329bd64fc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d777237ca5f637a6f37df2a3c48cef604a0ff62578e5f535aff9502350beb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf3418ae9a10b206ede0adb251b38b666318db1344190e6b83fc9b254b484b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceStatusLoadBalancerIngressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusLoadBalancerIngressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64c214219b366a79bb1ccec3615e8042d6514a45b63b71fd0ad51392420c56fb)
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
    def internal_value(self) -> typing.Optional[ServiceStatusLoadBalancerIngress]:
        return typing.cast(typing.Optional[ServiceStatusLoadBalancerIngress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceStatusLoadBalancerIngress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58940de3d4f0ca536253cbc958dbb27d5724cfbf69a718ad178b4539eb89348e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceStatusLoadBalancerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusLoadBalancerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8d281b7386cb34778be4bafd7ebeb3f7637ccfd779a9a0d23356b289c7bdf57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceStatusLoadBalancerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2cf202975b335d00cc529d3f1d0494e5f7a666629f95fb38e5903efb3c8e7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceStatusLoadBalancerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75a34d7bf17f20c06947bec2d9e4b0ae34303c3779096e9c5f92ac973b15092)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e14a8cc0039ab75ed2b26dbbd2eedc5307db532e30e858ca3c5dbf3dcac832)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4f97328378174e793c4de2d4575dd39b99daa32a22a9ecf3751c9dbb408184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceStatusLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01314599fb73d23c9ff19ad7d53090a897c8b5088b8bde27b47f09ad625cb43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> ServiceStatusLoadBalancerIngressList:
        return typing.cast(ServiceStatusLoadBalancerIngressList, jsii.get(self, "ingress"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceStatusLoadBalancer]:
        return typing.cast(typing.Optional[ServiceStatusLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceStatusLoadBalancer]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e760c462b8fb232ca39df187cbb0242aadbaa926773d1dec8bba01746b452aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__147b810e8cfe807e80ca762717d6c0a73a8b42c87ede3fb58e34e0cd4353f540)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> ServiceStatusLoadBalancerList:
        return typing.cast(ServiceStatusLoadBalancerList, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceStatus]:
        return typing.cast(typing.Optional[ServiceStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59fdb21bbbf916d158077a6dc8accebe25e23397a459d822b7f20251358c6e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.service.ServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class ServiceTimeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#create Service#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d32d76fc4347f5818ed9a8d5b9e1fd55b87ed8af792c73936311711145a52ee)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/service#create Service#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.service.ServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__705696646197183107f950f5ff0874985e87761eb11c4d13cb35a7d76253d62b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3c7b512daae8fbcf420fec35fd1129f7389ece2dc439a048c00b86bd8eb413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0e644a61fabd49c950f23ff5020b41e93feaf636d5bbc1e76f91ba940c34e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Service",
    "ServiceConfig",
    "ServiceMetadata",
    "ServiceMetadataOutputReference",
    "ServiceSpec",
    "ServiceSpecOutputReference",
    "ServiceSpecPort",
    "ServiceSpecPortList",
    "ServiceSpecPortOutputReference",
    "ServiceSpecSessionAffinityConfig",
    "ServiceSpecSessionAffinityConfigClientIp",
    "ServiceSpecSessionAffinityConfigClientIpOutputReference",
    "ServiceSpecSessionAffinityConfigOutputReference",
    "ServiceStatus",
    "ServiceStatusList",
    "ServiceStatusLoadBalancer",
    "ServiceStatusLoadBalancerIngress",
    "ServiceStatusLoadBalancerIngressList",
    "ServiceStatusLoadBalancerIngressOutputReference",
    "ServiceStatusLoadBalancerList",
    "ServiceStatusLoadBalancerOutputReference",
    "ServiceStatusOutputReference",
    "ServiceTimeouts",
    "ServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9cd008ce3bf3e1676fb7c7c3450a677661030ea72a9841944d417ab1f8b5b6da(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[ServiceMetadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[ServiceSpec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a696767454137e1e7b13e4d4934f71f723d16bbf7d51b71611f05e059086d408(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f17e7261e16afc04cc163778440580134d52467613e83eb7c797d237e87cab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c698fa72cc9dab13715a178498c5a5464dc33712e24cae0de0c51c64263c2ec3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba11ba943e603fa66c1ce5ee16e709bc80fa32b1495f40c86a8180c82e77446c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[ServiceMetadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[ServiceSpec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030fa05aa2dbce94b3c89f8f5393694a52c244bdb487944a20a24c12fd7e1937(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    generate_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df400b5c531735276c42b78e9c85e10d73488a0b6c2755ce90744b3d7e027d20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efab969de4fef3f53a4a21e98e369c3dd22060e4694fd8936a892f7cdaf7497(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7a7b3dc7174a682965eb66fefcd3c4bcd4708d83f74b1804c34e306401aa94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a3b19495eef4ba76ebd2dfef77386b0ad113bc53a1465bcf32a9bd5226a786(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d9f3d44fffea9e247772fcdd6758d364e4ec045fc4e896299763b9414b1b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6114dd91e26f30f91e517fa016b20063ed4afa400e7af779af6a554fecc43964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077ede6a7a5b1da676735323e71c99d21046d6c6cecf11cb3c27c916f624920f(
    value: typing.Optional[ServiceMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc8e29de680350ab23df99e1d77eafbd6203186a180ecf959a50f497b86889b(
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
    port: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceSpecPort, typing.Dict[builtins.str, typing.Any]]]]] = None,
    publish_not_ready_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    session_affinity_config: typing.Optional[typing.Union[ServiceSpecSessionAffinityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa30d40e000dcf38d7b5f2a45beb1a0e8311605649a5fff128432f234596d543(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e11f4a066b96c9587e356af83798ae7e22d04e9b95243fe62fd8e5e1b33b224(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceSpecPort, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ec216fb649a605bcf9eef8afd954914842c9e5f852e8e17da903660e10c58d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4571a7a23933440891babd691f66c89853320abb9af15d1b81f9e75df710884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d493d6c65eeb045c1fa18638556076d8a9e42c4dfd807cf63c011e17a829039b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b312af3e801d83c3044dcf1db126dba39ee0510c8ff502bedd265c81a67786d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a0b9b9ddc58b461b41bd953c002c0bccb922a9fec39c837ce7c7721d91098a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915affc6d7baf640cafb742e96b7e7a2cd17cf66aadf99de4f715a44a4403df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7648b06b0429bc87d87d2773365dad99aba684cfcd5d8168e07c2f538ae59c63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d014e943da791c1c7652e8ccfe865725d5e69ff2f0fd0c33a899e15d9939b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cf2b2578cdff993f80f0985a0c650ce04fb188ae339b2ca2654a44c32a36d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7cea9197838d6d7e3f204ec75f97a09631614d4e5ed599e3bcdce9d5134b20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79a8b5478df37ed6c7562a850f9c95c89000e5626df8fe1c244ca195e8fde23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d891655cf222711a78d515313a16f748cf86d8a4091de5919172948d62e00b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66cf87f896278051ca4ed10f9609c8db4859b056a448ab243afb9be509440d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a733f2feb2d2e1467b8267287ad40b0c4a33ec4aeaed50f322a333947900b53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f80d5c40b5220cd865dc9a0d796ad8025b9b5202b2aca16d8d1946d711c7b3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2481a60c25504ff1c4c3e7fdf305bba580f88c3587477e7f2ceb0645d75d23fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fb9680bd95ff5d74f22bcc5791aa8a0cf1dff7f48efb29e8040219fad21c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553fcdf282a2243ae565ddaf709866b21edb44a44d2a30e2609f984bd85ffeb1(
    value: typing.Optional[ServiceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67a5030308d9544d162ca4c79fb7477901c5fa62712c0dfd8de7f1b76117810(
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

def _typecheckingstub__4ef85948dbac68520f5612cda6c1866279874444be1de74c2a20222adb66b99e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b0dcf8d67f3ba63b8612fad5aac2b6e594f56e801d8020a5e4d0f57aac17bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2623b192f1884d960eef2933de275eba860c49045ec1c00c71bd2a2997ce616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbc83933b318d44523453b96e105e1680f3fa93535a4f4e0d58ec439177f2bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f781cb529a10d9711a9e76d8e0b8916b01436f18b5592d25b9629ee272850ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fe910720dfb320486cc7cfb6e5fec24d223e6d83349eec87e5b3e81489f491(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceSpecPort]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6016a37888dd2f2efd15b5ef1b51928d2c6bf8dadfbe0e61fa8129f0546753(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8681a9e70d8175c13389df67dbda2a288c5f412d09b50427fb41f1db1896225(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1a199733e588673c24da46c2a98296b58383d146099ad60e44e5a94269e274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfd308fd588d1f37e6c83b6f6fcad3ec8749fc267b9b2276c4699a111b277e0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6d197e0b9d7bbf41799befb0417f0c754e10ce00949a95207b5d65409d17fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2638766c43654431eba5836f0d02dcb07beae167420adde04661431fc921aa4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78be54363a21c69981694bb96c9123f96785a9efe8de192a116c3575dad9b64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a33bf2995cad5067e49734b9e3b5708b57d75b5c19df12fa57b9bd5b0b7e312(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceSpecPort]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d1806113c03976d5e93a9d9467d191d6753b5da638e75ea579511589244d95(
    *,
    client_ip: typing.Optional[typing.Union[ServiceSpecSessionAffinityConfigClientIp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9854793f986542982d4512859b0bcf5a2794912c15af30e8a5d14171c204ad(
    *,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26292440eaf19843b43c9146cead0990f17cad3dda03c40fe5a9a38237f0b95f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fdd96289a22f209f0c135738b65ef3a3093f6ce2c0e4eb7556475e9eb597b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7483bf2c215d965ea20b754df658a8439fc3c7303f091717b09025a1140b6d2a(
    value: typing.Optional[ServiceSpecSessionAffinityConfigClientIp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311ceef974ad26a6fa6d26fbba14834cc2bcf09ca4a463d0034578922a6c3c04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bbe855fd5768f90c2bf6f26f7d2bb421aa88edeb438c259142f5d83b0db714(
    value: typing.Optional[ServiceSpecSessionAffinityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5791686b897478784055103a091c5760513cf8f2ab435681ba57adb191077267(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33771711bf9730dca02fa806748e3e7069d990c2c3e38ea008441bd5254d7d61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911f74d9c504e1ace9c5c1e7544407179cbdc5c810dcc1ece6c7c6d1d6068d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dab095c595561e1bc2de5d207b2c29130f320e2142d014be96694553159420(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c86ce43b43b3efd27186cc963b38c468ae3f0d63ae40dcafeb45fe079e0bee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505fdcd6d0570c41d1bda713dc18c7a5576ba596f55948e935ba0f17dc7e91c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4e06495c66f2dd349578d6ed97b9c8980a28e6cb5162aba06f5e96a2d519f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abfa691807f2abe79e91fa21f358c67fc253007a183c7521fbbf6329bd64fc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d777237ca5f637a6f37df2a3c48cef604a0ff62578e5f535aff9502350beb1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf3418ae9a10b206ede0adb251b38b666318db1344190e6b83fc9b254b484b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c214219b366a79bb1ccec3615e8042d6514a45b63b71fd0ad51392420c56fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58940de3d4f0ca536253cbc958dbb27d5724cfbf69a718ad178b4539eb89348e(
    value: typing.Optional[ServiceStatusLoadBalancerIngress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d281b7386cb34778be4bafd7ebeb3f7637ccfd779a9a0d23356b289c7bdf57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2cf202975b335d00cc529d3f1d0494e5f7a666629f95fb38e5903efb3c8e7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75a34d7bf17f20c06947bec2d9e4b0ae34303c3779096e9c5f92ac973b15092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e14a8cc0039ab75ed2b26dbbd2eedc5307db532e30e858ca3c5dbf3dcac832(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4f97328378174e793c4de2d4575dd39b99daa32a22a9ecf3751c9dbb408184(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01314599fb73d23c9ff19ad7d53090a897c8b5088b8bde27b47f09ad625cb43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e760c462b8fb232ca39df187cbb0242aadbaa926773d1dec8bba01746b452aa4(
    value: typing.Optional[ServiceStatusLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147b810e8cfe807e80ca762717d6c0a73a8b42c87ede3fb58e34e0cd4353f540(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59fdb21bbbf916d158077a6dc8accebe25e23397a459d822b7f20251358c6e1(
    value: typing.Optional[ServiceStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d32d76fc4347f5818ed9a8d5b9e1fd55b87ed8af792c73936311711145a52ee(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705696646197183107f950f5ff0874985e87761eb11c4d13cb35a7d76253d62b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3c7b512daae8fbcf420fec35fd1129f7389ece2dc439a048c00b86bd8eb413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0e644a61fabd49c950f23ff5020b41e93feaf636d5bbc1e76f91ba940c34e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
