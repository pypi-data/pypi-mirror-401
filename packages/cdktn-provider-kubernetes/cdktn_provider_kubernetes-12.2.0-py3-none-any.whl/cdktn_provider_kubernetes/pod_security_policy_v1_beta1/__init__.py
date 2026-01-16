r'''
# `kubernetes_pod_security_policy_v1beta1`

Refer to the Terraform Registry for docs: [`kubernetes_pod_security_policy_v1beta1`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1).
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


class PodSecurityPolicyV1Beta1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1 kubernetes_pod_security_policy_v1beta1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["PodSecurityPolicyV1Beta1Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["PodSecurityPolicyV1Beta1Spec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1 kubernetes_pod_security_policy_v1beta1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#metadata PodSecurityPolicyV1Beta1#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#spec PodSecurityPolicyV1Beta1#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#id PodSecurityPolicyV1Beta1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e02854aec8a5588213790b571c2d7ba4311e8cd4b48cc1d690042ffd2f1cd52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PodSecurityPolicyV1Beta1Config(
            metadata=metadata,
            spec=spec,
            id=id,
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
        '''Generates CDKTF code for importing a PodSecurityPolicyV1Beta1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PodSecurityPolicyV1Beta1 to import.
        :param import_from_id: The id of the existing PodSecurityPolicyV1Beta1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PodSecurityPolicyV1Beta1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31158a61ffa87bdaf1b9e545da5d52d5c0c23db0bf2ac4178e33c6a2d87a988b)
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
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the podsecuritypolicy that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#annotations PodSecurityPolicyV1Beta1#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the podsecuritypolicy. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#labels PodSecurityPolicyV1Beta1#labels}
        :param name: Name of the podsecuritypolicy, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#name PodSecurityPolicyV1Beta1#name}
        '''
        value = PodSecurityPolicyV1Beta1Metadata(
            annotations=annotations, labels=labels, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        fs_group: typing.Union["PodSecurityPolicyV1Beta1SpecFsGroup", typing.Dict[builtins.str, typing.Any]],
        run_as_user: typing.Union["PodSecurityPolicyV1Beta1SpecRunAsUser", typing.Dict[builtins.str, typing.Any]],
        supplemental_groups: typing.Union["PodSecurityPolicyV1Beta1SpecSupplementalGroups", typing.Dict[builtins.str, typing.Any]],
        allowed_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_flex_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_host_paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecAllowedHostPaths", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_proc_mount_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_add_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forbidden_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        host_ipc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_pid: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecHostPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_drop_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        run_as_group: typing.Optional[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        se_linux: typing.Optional[typing.Union["PodSecurityPolicyV1Beta1SpecSeLinux", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param fs_group: fs_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#fs_group PodSecurityPolicyV1Beta1#fs_group}
        :param run_as_user: run_as_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#run_as_user PodSecurityPolicyV1Beta1#run_as_user}
        :param supplemental_groups: supplemental_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#supplemental_groups PodSecurityPolicyV1Beta1#supplemental_groups}
        :param allowed_capabilities: allowedCapabilities is a list of capabilities that can be requested to add to the container. Capabilities in this field may be added at the pod author's discretion. You must not list a capability in both allowedCapabilities and requiredDropCapabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_capabilities PodSecurityPolicyV1Beta1#allowed_capabilities}
        :param allowed_flex_volumes: allowed_flex_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_flex_volumes PodSecurityPolicyV1Beta1#allowed_flex_volumes}
        :param allowed_host_paths: allowed_host_paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_host_paths PodSecurityPolicyV1Beta1#allowed_host_paths}
        :param allowed_proc_mount_types: AllowedProcMountTypes is an allowlist of allowed ProcMountTypes. Empty or nil indicates that only the DefaultProcMountType may be used. This requires the ProcMountType feature flag to be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_proc_mount_types PodSecurityPolicyV1Beta1#allowed_proc_mount_types}
        :param allowed_unsafe_sysctls: allowedUnsafeSysctls is a list of explicitly allowed unsafe sysctls, defaults to none. Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of allowed sysctls. Single * means all unsafe sysctls are allowed. Kubelet has to allowlist all allowed unsafe sysctls explicitly to avoid rejection. Examples: e.g. "foo/*" allows "foo/bar", "foo/baz", etc. e.g. "foo.*" allows "foo.bar", "foo.baz", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_unsafe_sysctls PodSecurityPolicyV1Beta1#allowed_unsafe_sysctls}
        :param allow_privilege_escalation: allowPrivilegeEscalation determines if a pod can request to allow privilege escalation. If unspecified, defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allow_privilege_escalation PodSecurityPolicyV1Beta1#allow_privilege_escalation}
        :param default_add_capabilities: defaultAddCapabilities is the default set of capabilities that will be added to the container unless the pod spec specifically drops the capability. You may not list a capability in both defaultAddCapabilities and requiredDropCapabilities. Capabilities added here are implicitly allowed, and need not be included in the allowedCapabilities list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#default_add_capabilities PodSecurityPolicyV1Beta1#default_add_capabilities}
        :param default_allow_privilege_escalation: defaultAllowPrivilegeEscalation controls the default setting for whether a process can gain more privileges than its parent process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#default_allow_privilege_escalation PodSecurityPolicyV1Beta1#default_allow_privilege_escalation}
        :param forbidden_sysctls: forbiddenSysctls is a list of explicitly forbidden sysctls, defaults to none. Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of forbidden sysctls. Single * means all sysctls are forbidden. Examples: e.g. "foo/*" forbids "foo/bar", "foo/baz", etc. e.g. "foo.*" forbids "foo.bar", "foo.baz", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#forbidden_sysctls PodSecurityPolicyV1Beta1#forbidden_sysctls}
        :param host_ipc: hostIPC determines if the policy allows the use of HostIPC in the pod spec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_ipc PodSecurityPolicyV1Beta1#host_ipc}
        :param host_network: hostNetwork determines if the policy allows the use of HostNetwork in the pod spec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_network PodSecurityPolicyV1Beta1#host_network}
        :param host_pid: hostPID determines if the policy allows the use of HostPID in the pod spec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_pid PodSecurityPolicyV1Beta1#host_pid}
        :param host_ports: host_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_ports PodSecurityPolicyV1Beta1#host_ports}
        :param privileged: privileged determines if a pod can request to be run as privileged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#privileged PodSecurityPolicyV1Beta1#privileged}
        :param read_only_root_filesystem: readOnlyRootFilesystem when set to true will force containers to run with a read only root file system. If the container specifically requests to run with a non-read only root file system the PSP should deny the pod. If set to false the container may run with a read only root file system if it wishes but it will not be forced to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#read_only_root_filesystem PodSecurityPolicyV1Beta1#read_only_root_filesystem}
        :param required_drop_capabilities: requiredDropCapabilities are the capabilities that will be dropped from the container. These are required to be dropped and cannot be added. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#required_drop_capabilities PodSecurityPolicyV1Beta1#required_drop_capabilities}
        :param run_as_group: run_as_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#run_as_group PodSecurityPolicyV1Beta1#run_as_group}
        :param se_linux: se_linux block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#se_linux PodSecurityPolicyV1Beta1#se_linux}
        :param volumes: volumes is an allowlist of volume plugins. Empty indicates that no volumes may be used. To allow all volumes you may use '*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#volumes PodSecurityPolicyV1Beta1#volumes}
        '''
        value = PodSecurityPolicyV1Beta1Spec(
            fs_group=fs_group,
            run_as_user=run_as_user,
            supplemental_groups=supplemental_groups,
            allowed_capabilities=allowed_capabilities,
            allowed_flex_volumes=allowed_flex_volumes,
            allowed_host_paths=allowed_host_paths,
            allowed_proc_mount_types=allowed_proc_mount_types,
            allowed_unsafe_sysctls=allowed_unsafe_sysctls,
            allow_privilege_escalation=allow_privilege_escalation,
            default_add_capabilities=default_add_capabilities,
            default_allow_privilege_escalation=default_allow_privilege_escalation,
            forbidden_sysctls=forbidden_sysctls,
            host_ipc=host_ipc,
            host_network=host_network,
            host_pid=host_pid,
            host_ports=host_ports,
            privileged=privileged,
            read_only_root_filesystem=read_only_root_filesystem,
            required_drop_capabilities=required_drop_capabilities,
            run_as_group=run_as_group,
            se_linux=se_linux,
            volumes=volumes,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    def metadata(self) -> "PodSecurityPolicyV1Beta1MetadataOutputReference":
        return typing.cast("PodSecurityPolicyV1Beta1MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "PodSecurityPolicyV1Beta1SpecOutputReference":
        return typing.cast("PodSecurityPolicyV1Beta1SpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["PodSecurityPolicyV1Beta1Metadata"]:
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["PodSecurityPolicyV1Beta1Spec"]:
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1Spec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3285b0fc10addff7575865f4f74736f276e5611fce8ee28153d59c07376a5e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1Config",
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
    },
)
class PodSecurityPolicyV1Beta1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["PodSecurityPolicyV1Beta1Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["PodSecurityPolicyV1Beta1Spec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#metadata PodSecurityPolicyV1Beta1#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#spec PodSecurityPolicyV1Beta1#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#id PodSecurityPolicyV1Beta1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = PodSecurityPolicyV1Beta1Metadata(**metadata)
        if isinstance(spec, dict):
            spec = PodSecurityPolicyV1Beta1Spec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f46ed709073b3ccfd76762b5b553fe7e44ab1b6cda4360690a59bf46728741)
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
    def metadata(self) -> "PodSecurityPolicyV1Beta1Metadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#metadata PodSecurityPolicyV1Beta1#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("PodSecurityPolicyV1Beta1Metadata", result)

    @builtins.property
    def spec(self) -> "PodSecurityPolicyV1Beta1Spec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#spec PodSecurityPolicyV1Beta1#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("PodSecurityPolicyV1Beta1Spec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#id PodSecurityPolicyV1Beta1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1Metadata",
    jsii_struct_bases=[],
    name_mapping={"annotations": "annotations", "labels": "labels", "name": "name"},
)
class PodSecurityPolicyV1Beta1Metadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the podsecuritypolicy that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#annotations PodSecurityPolicyV1Beta1#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the podsecuritypolicy. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#labels PodSecurityPolicyV1Beta1#labels}
        :param name: Name of the podsecuritypolicy, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#name PodSecurityPolicyV1Beta1#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fbe505cb19bd64a98a95dc42885883acea5b84e48c042659fef639f874ac8b)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An unstructured key value map stored with the podsecuritypolicy that may be used to store arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#annotations PodSecurityPolicyV1Beta1#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the podsecuritypolicy.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#labels PodSecurityPolicyV1Beta1#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the podsecuritypolicy, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#name PodSecurityPolicyV1Beta1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78569ea75bf9935f75cc5b16d7c070869de4566af61334d45431224b9efcd9b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ead0d67408d3aa58cc553e7834e7ae314287199d103ed41e58b20d107b31b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72dfad94f2e73b9ffe5a64d86bd84b92dd943961b9a72cfd457ded419d33299f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24beb3718fbe6977a37c49e1387e3d74241d4aec6af19579701478bfd6c17556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PodSecurityPolicyV1Beta1Metadata]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1Metadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a43972fe1240de997939e371be41b05d39de07ac9c616f9ef21df47e817ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1Spec",
    jsii_struct_bases=[],
    name_mapping={
        "fs_group": "fsGroup",
        "run_as_user": "runAsUser",
        "supplemental_groups": "supplementalGroups",
        "allowed_capabilities": "allowedCapabilities",
        "allowed_flex_volumes": "allowedFlexVolumes",
        "allowed_host_paths": "allowedHostPaths",
        "allowed_proc_mount_types": "allowedProcMountTypes",
        "allowed_unsafe_sysctls": "allowedUnsafeSysctls",
        "allow_privilege_escalation": "allowPrivilegeEscalation",
        "default_add_capabilities": "defaultAddCapabilities",
        "default_allow_privilege_escalation": "defaultAllowPrivilegeEscalation",
        "forbidden_sysctls": "forbiddenSysctls",
        "host_ipc": "hostIpc",
        "host_network": "hostNetwork",
        "host_pid": "hostPid",
        "host_ports": "hostPorts",
        "privileged": "privileged",
        "read_only_root_filesystem": "readOnlyRootFilesystem",
        "required_drop_capabilities": "requiredDropCapabilities",
        "run_as_group": "runAsGroup",
        "se_linux": "seLinux",
        "volumes": "volumes",
    },
)
class PodSecurityPolicyV1Beta1Spec:
    def __init__(
        self,
        *,
        fs_group: typing.Union["PodSecurityPolicyV1Beta1SpecFsGroup", typing.Dict[builtins.str, typing.Any]],
        run_as_user: typing.Union["PodSecurityPolicyV1Beta1SpecRunAsUser", typing.Dict[builtins.str, typing.Any]],
        supplemental_groups: typing.Union["PodSecurityPolicyV1Beta1SpecSupplementalGroups", typing.Dict[builtins.str, typing.Any]],
        allowed_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_flex_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_host_paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecAllowedHostPaths", typing.Dict[builtins.str, typing.Any]]]]] = None,
        allowed_proc_mount_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_add_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forbidden_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        host_ipc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_pid: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecHostPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_drop_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        run_as_group: typing.Optional[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        se_linux: typing.Optional[typing.Union["PodSecurityPolicyV1Beta1SpecSeLinux", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param fs_group: fs_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#fs_group PodSecurityPolicyV1Beta1#fs_group}
        :param run_as_user: run_as_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#run_as_user PodSecurityPolicyV1Beta1#run_as_user}
        :param supplemental_groups: supplemental_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#supplemental_groups PodSecurityPolicyV1Beta1#supplemental_groups}
        :param allowed_capabilities: allowedCapabilities is a list of capabilities that can be requested to add to the container. Capabilities in this field may be added at the pod author's discretion. You must not list a capability in both allowedCapabilities and requiredDropCapabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_capabilities PodSecurityPolicyV1Beta1#allowed_capabilities}
        :param allowed_flex_volumes: allowed_flex_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_flex_volumes PodSecurityPolicyV1Beta1#allowed_flex_volumes}
        :param allowed_host_paths: allowed_host_paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_host_paths PodSecurityPolicyV1Beta1#allowed_host_paths}
        :param allowed_proc_mount_types: AllowedProcMountTypes is an allowlist of allowed ProcMountTypes. Empty or nil indicates that only the DefaultProcMountType may be used. This requires the ProcMountType feature flag to be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_proc_mount_types PodSecurityPolicyV1Beta1#allowed_proc_mount_types}
        :param allowed_unsafe_sysctls: allowedUnsafeSysctls is a list of explicitly allowed unsafe sysctls, defaults to none. Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of allowed sysctls. Single * means all unsafe sysctls are allowed. Kubelet has to allowlist all allowed unsafe sysctls explicitly to avoid rejection. Examples: e.g. "foo/*" allows "foo/bar", "foo/baz", etc. e.g. "foo.*" allows "foo.bar", "foo.baz", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_unsafe_sysctls PodSecurityPolicyV1Beta1#allowed_unsafe_sysctls}
        :param allow_privilege_escalation: allowPrivilegeEscalation determines if a pod can request to allow privilege escalation. If unspecified, defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allow_privilege_escalation PodSecurityPolicyV1Beta1#allow_privilege_escalation}
        :param default_add_capabilities: defaultAddCapabilities is the default set of capabilities that will be added to the container unless the pod spec specifically drops the capability. You may not list a capability in both defaultAddCapabilities and requiredDropCapabilities. Capabilities added here are implicitly allowed, and need not be included in the allowedCapabilities list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#default_add_capabilities PodSecurityPolicyV1Beta1#default_add_capabilities}
        :param default_allow_privilege_escalation: defaultAllowPrivilegeEscalation controls the default setting for whether a process can gain more privileges than its parent process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#default_allow_privilege_escalation PodSecurityPolicyV1Beta1#default_allow_privilege_escalation}
        :param forbidden_sysctls: forbiddenSysctls is a list of explicitly forbidden sysctls, defaults to none. Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of forbidden sysctls. Single * means all sysctls are forbidden. Examples: e.g. "foo/*" forbids "foo/bar", "foo/baz", etc. e.g. "foo.*" forbids "foo.bar", "foo.baz", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#forbidden_sysctls PodSecurityPolicyV1Beta1#forbidden_sysctls}
        :param host_ipc: hostIPC determines if the policy allows the use of HostIPC in the pod spec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_ipc PodSecurityPolicyV1Beta1#host_ipc}
        :param host_network: hostNetwork determines if the policy allows the use of HostNetwork in the pod spec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_network PodSecurityPolicyV1Beta1#host_network}
        :param host_pid: hostPID determines if the policy allows the use of HostPID in the pod spec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_pid PodSecurityPolicyV1Beta1#host_pid}
        :param host_ports: host_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_ports PodSecurityPolicyV1Beta1#host_ports}
        :param privileged: privileged determines if a pod can request to be run as privileged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#privileged PodSecurityPolicyV1Beta1#privileged}
        :param read_only_root_filesystem: readOnlyRootFilesystem when set to true will force containers to run with a read only root file system. If the container specifically requests to run with a non-read only root file system the PSP should deny the pod. If set to false the container may run with a read only root file system if it wishes but it will not be forced to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#read_only_root_filesystem PodSecurityPolicyV1Beta1#read_only_root_filesystem}
        :param required_drop_capabilities: requiredDropCapabilities are the capabilities that will be dropped from the container. These are required to be dropped and cannot be added. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#required_drop_capabilities PodSecurityPolicyV1Beta1#required_drop_capabilities}
        :param run_as_group: run_as_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#run_as_group PodSecurityPolicyV1Beta1#run_as_group}
        :param se_linux: se_linux block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#se_linux PodSecurityPolicyV1Beta1#se_linux}
        :param volumes: volumes is an allowlist of volume plugins. Empty indicates that no volumes may be used. To allow all volumes you may use '*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#volumes PodSecurityPolicyV1Beta1#volumes}
        '''
        if isinstance(fs_group, dict):
            fs_group = PodSecurityPolicyV1Beta1SpecFsGroup(**fs_group)
        if isinstance(run_as_user, dict):
            run_as_user = PodSecurityPolicyV1Beta1SpecRunAsUser(**run_as_user)
        if isinstance(supplemental_groups, dict):
            supplemental_groups = PodSecurityPolicyV1Beta1SpecSupplementalGroups(**supplemental_groups)
        if isinstance(run_as_group, dict):
            run_as_group = PodSecurityPolicyV1Beta1SpecRunAsGroup(**run_as_group)
        if isinstance(se_linux, dict):
            se_linux = PodSecurityPolicyV1Beta1SpecSeLinux(**se_linux)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd1557da641c756ca1df9bcd67b39345639e49dded7d2352538b528994893fc)
            check_type(argname="argument fs_group", value=fs_group, expected_type=type_hints["fs_group"])
            check_type(argname="argument run_as_user", value=run_as_user, expected_type=type_hints["run_as_user"])
            check_type(argname="argument supplemental_groups", value=supplemental_groups, expected_type=type_hints["supplemental_groups"])
            check_type(argname="argument allowed_capabilities", value=allowed_capabilities, expected_type=type_hints["allowed_capabilities"])
            check_type(argname="argument allowed_flex_volumes", value=allowed_flex_volumes, expected_type=type_hints["allowed_flex_volumes"])
            check_type(argname="argument allowed_host_paths", value=allowed_host_paths, expected_type=type_hints["allowed_host_paths"])
            check_type(argname="argument allowed_proc_mount_types", value=allowed_proc_mount_types, expected_type=type_hints["allowed_proc_mount_types"])
            check_type(argname="argument allowed_unsafe_sysctls", value=allowed_unsafe_sysctls, expected_type=type_hints["allowed_unsafe_sysctls"])
            check_type(argname="argument allow_privilege_escalation", value=allow_privilege_escalation, expected_type=type_hints["allow_privilege_escalation"])
            check_type(argname="argument default_add_capabilities", value=default_add_capabilities, expected_type=type_hints["default_add_capabilities"])
            check_type(argname="argument default_allow_privilege_escalation", value=default_allow_privilege_escalation, expected_type=type_hints["default_allow_privilege_escalation"])
            check_type(argname="argument forbidden_sysctls", value=forbidden_sysctls, expected_type=type_hints["forbidden_sysctls"])
            check_type(argname="argument host_ipc", value=host_ipc, expected_type=type_hints["host_ipc"])
            check_type(argname="argument host_network", value=host_network, expected_type=type_hints["host_network"])
            check_type(argname="argument host_pid", value=host_pid, expected_type=type_hints["host_pid"])
            check_type(argname="argument host_ports", value=host_ports, expected_type=type_hints["host_ports"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument read_only_root_filesystem", value=read_only_root_filesystem, expected_type=type_hints["read_only_root_filesystem"])
            check_type(argname="argument required_drop_capabilities", value=required_drop_capabilities, expected_type=type_hints["required_drop_capabilities"])
            check_type(argname="argument run_as_group", value=run_as_group, expected_type=type_hints["run_as_group"])
            check_type(argname="argument se_linux", value=se_linux, expected_type=type_hints["se_linux"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fs_group": fs_group,
            "run_as_user": run_as_user,
            "supplemental_groups": supplemental_groups,
        }
        if allowed_capabilities is not None:
            self._values["allowed_capabilities"] = allowed_capabilities
        if allowed_flex_volumes is not None:
            self._values["allowed_flex_volumes"] = allowed_flex_volumes
        if allowed_host_paths is not None:
            self._values["allowed_host_paths"] = allowed_host_paths
        if allowed_proc_mount_types is not None:
            self._values["allowed_proc_mount_types"] = allowed_proc_mount_types
        if allowed_unsafe_sysctls is not None:
            self._values["allowed_unsafe_sysctls"] = allowed_unsafe_sysctls
        if allow_privilege_escalation is not None:
            self._values["allow_privilege_escalation"] = allow_privilege_escalation
        if default_add_capabilities is not None:
            self._values["default_add_capabilities"] = default_add_capabilities
        if default_allow_privilege_escalation is not None:
            self._values["default_allow_privilege_escalation"] = default_allow_privilege_escalation
        if forbidden_sysctls is not None:
            self._values["forbidden_sysctls"] = forbidden_sysctls
        if host_ipc is not None:
            self._values["host_ipc"] = host_ipc
        if host_network is not None:
            self._values["host_network"] = host_network
        if host_pid is not None:
            self._values["host_pid"] = host_pid
        if host_ports is not None:
            self._values["host_ports"] = host_ports
        if privileged is not None:
            self._values["privileged"] = privileged
        if read_only_root_filesystem is not None:
            self._values["read_only_root_filesystem"] = read_only_root_filesystem
        if required_drop_capabilities is not None:
            self._values["required_drop_capabilities"] = required_drop_capabilities
        if run_as_group is not None:
            self._values["run_as_group"] = run_as_group
        if se_linux is not None:
            self._values["se_linux"] = se_linux
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def fs_group(self) -> "PodSecurityPolicyV1Beta1SpecFsGroup":
        '''fs_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#fs_group PodSecurityPolicyV1Beta1#fs_group}
        '''
        result = self._values.get("fs_group")
        assert result is not None, "Required property 'fs_group' is missing"
        return typing.cast("PodSecurityPolicyV1Beta1SpecFsGroup", result)

    @builtins.property
    def run_as_user(self) -> "PodSecurityPolicyV1Beta1SpecRunAsUser":
        '''run_as_user block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#run_as_user PodSecurityPolicyV1Beta1#run_as_user}
        '''
        result = self._values.get("run_as_user")
        assert result is not None, "Required property 'run_as_user' is missing"
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsUser", result)

    @builtins.property
    def supplemental_groups(self) -> "PodSecurityPolicyV1Beta1SpecSupplementalGroups":
        '''supplemental_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#supplemental_groups PodSecurityPolicyV1Beta1#supplemental_groups}
        '''
        result = self._values.get("supplemental_groups")
        assert result is not None, "Required property 'supplemental_groups' is missing"
        return typing.cast("PodSecurityPolicyV1Beta1SpecSupplementalGroups", result)

    @builtins.property
    def allowed_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''allowedCapabilities is a list of capabilities that can be requested to add to the container.

        Capabilities in this field may be added at the pod author's discretion. You must not list a capability in both allowedCapabilities and requiredDropCapabilities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_capabilities PodSecurityPolicyV1Beta1#allowed_capabilities}
        '''
        result = self._values.get("allowed_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_flex_volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes"]]]:
        '''allowed_flex_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_flex_volumes PodSecurityPolicyV1Beta1#allowed_flex_volumes}
        '''
        result = self._values.get("allowed_flex_volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes"]]], result)

    @builtins.property
    def allowed_host_paths(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecAllowedHostPaths"]]]:
        '''allowed_host_paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_host_paths PodSecurityPolicyV1Beta1#allowed_host_paths}
        '''
        result = self._values.get("allowed_host_paths")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecAllowedHostPaths"]]], result)

    @builtins.property
    def allowed_proc_mount_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''AllowedProcMountTypes is an allowlist of allowed ProcMountTypes.

        Empty or nil indicates that only the DefaultProcMountType may be used. This requires the ProcMountType feature flag to be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_proc_mount_types PodSecurityPolicyV1Beta1#allowed_proc_mount_types}
        '''
        result = self._values.get("allowed_proc_mount_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_unsafe_sysctls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''allowedUnsafeSysctls is a list of explicitly allowed unsafe sysctls, defaults to none.

        Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of allowed sysctls. Single * means all unsafe sysctls are allowed. Kubelet has to allowlist all allowed unsafe sysctls explicitly to avoid rejection.

        Examples: e.g. "foo/*" allows "foo/bar", "foo/baz", etc. e.g. "foo.*" allows "foo.bar", "foo.baz", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allowed_unsafe_sysctls PodSecurityPolicyV1Beta1#allowed_unsafe_sysctls}
        '''
        result = self._values.get("allowed_unsafe_sysctls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_privilege_escalation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''allowPrivilegeEscalation determines if a pod can request to allow privilege escalation. If unspecified, defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#allow_privilege_escalation PodSecurityPolicyV1Beta1#allow_privilege_escalation}
        '''
        result = self._values.get("allow_privilege_escalation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_add_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''defaultAddCapabilities is the default set of capabilities that will be added to the container unless the pod spec specifically drops the capability.

        You may not list a capability in both defaultAddCapabilities and requiredDropCapabilities. Capabilities added here are implicitly allowed, and need not be included in the allowedCapabilities list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#default_add_capabilities PodSecurityPolicyV1Beta1#default_add_capabilities}
        '''
        result = self._values.get("default_add_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_allow_privilege_escalation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''defaultAllowPrivilegeEscalation controls the default setting for whether a process can gain more privileges than its parent process.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#default_allow_privilege_escalation PodSecurityPolicyV1Beta1#default_allow_privilege_escalation}
        '''
        result = self._values.get("default_allow_privilege_escalation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forbidden_sysctls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''forbiddenSysctls is a list of explicitly forbidden sysctls, defaults to none.

        Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of forbidden sysctls. Single * means all sysctls are forbidden.

        Examples: e.g. "foo/*" forbids "foo/bar", "foo/baz", etc. e.g. "foo.*" forbids "foo.bar", "foo.baz", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#forbidden_sysctls PodSecurityPolicyV1Beta1#forbidden_sysctls}
        '''
        result = self._values.get("forbidden_sysctls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def host_ipc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''hostIPC determines if the policy allows the use of HostIPC in the pod spec.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_ipc PodSecurityPolicyV1Beta1#host_ipc}
        '''
        result = self._values.get("host_ipc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''hostNetwork determines if the policy allows the use of HostNetwork in the pod spec.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_network PodSecurityPolicyV1Beta1#host_network}
        '''
        result = self._values.get("host_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_pid(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''hostPID determines if the policy allows the use of HostPID in the pod spec.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_pid PodSecurityPolicyV1Beta1#host_pid}
        '''
        result = self._values.get("host_pid")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecHostPorts"]]]:
        '''host_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#host_ports PodSecurityPolicyV1Beta1#host_ports}
        '''
        result = self._values.get("host_ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecHostPorts"]]], result)

    @builtins.property
    def privileged(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''privileged determines if a pod can request to be run as privileged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#privileged PodSecurityPolicyV1Beta1#privileged}
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def read_only_root_filesystem(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''readOnlyRootFilesystem when set to true will force containers to run with a read only root file system.

        If the container specifically requests to run with a non-read only root file system the PSP should deny the pod. If set to false the container may run with a read only root file system if it wishes but it will not be forced to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#read_only_root_filesystem PodSecurityPolicyV1Beta1#read_only_root_filesystem}
        '''
        result = self._values.get("read_only_root_filesystem")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_drop_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''requiredDropCapabilities are the capabilities that will be dropped from the container.

        These are required to be dropped and cannot be added.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#required_drop_capabilities PodSecurityPolicyV1Beta1#required_drop_capabilities}
        '''
        result = self._values.get("required_drop_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def run_as_group(self) -> typing.Optional["PodSecurityPolicyV1Beta1SpecRunAsGroup"]:
        '''run_as_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#run_as_group PodSecurityPolicyV1Beta1#run_as_group}
        '''
        result = self._values.get("run_as_group")
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1SpecRunAsGroup"], result)

    @builtins.property
    def se_linux(self) -> typing.Optional["PodSecurityPolicyV1Beta1SpecSeLinux"]:
        '''se_linux block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#se_linux PodSecurityPolicyV1Beta1#se_linux}
        '''
        result = self._values.get("se_linux")
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1SpecSeLinux"], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''volumes is an allowlist of volume plugins.

        Empty indicates that no volumes may be used. To allow all volumes you may use '*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#volumes PodSecurityPolicyV1Beta1#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1Spec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes",
    jsii_struct_bases=[],
    name_mapping={"driver": "driver"},
)
class PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes:
    def __init__(self, *, driver: builtins.str) -> None:
        '''
        :param driver: driver is the name of the Flexvolume driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#driver PodSecurityPolicyV1Beta1#driver}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742bd87d46cb3e8164811e2f053cc6125bf713618795de393df7526f9fde4839)
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver": driver,
        }

    @builtins.property
    def driver(self) -> builtins.str:
        '''driver is the name of the Flexvolume driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#driver PodSecurityPolicyV1Beta1#driver}
        '''
        result = self._values.get("driver")
        assert result is not None, "Required property 'driver' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08ac647ef51f3e9eb74392e3b294973e4ba5fe7d82011bc01a636104b11528b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570febd07fd3277f63d4a1722d41cbde0d52bfd72856d1faac0a7bf3b3b7ab80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cb9085c30d88be5c958d976135b04e8d6114fbbea38f04893208af57ed1ffa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdce35b4b8b0a0f17dbebf5c9190e8dbeca48866ca288d393d08223fc5c35dde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cdbdefb1d5b0c6043b4cb72f098ef872c741f7fd0bde69ac2658fc165489e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8453dbf178fb7d170349f1a2b821e8b52096d28a1e983b70c3435ff794496b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a8a44a671051bc353737a2dcafb8f6be198c844ea321db0d339cbfefeafdd19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="driverInput")
    def driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInput"))

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driver"))

    @driver.setter
    def driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd5bcd63d2b0dcc3785b4b3dba6696475ebd95a53b20c6b5ebc1a878b9cbba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a4f9050575ab982d997231cdba679119584adbc3048e78670e825af0103e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecAllowedHostPaths",
    jsii_struct_bases=[],
    name_mapping={"path_prefix": "pathPrefix", "read_only": "readOnly"},
)
class PodSecurityPolicyV1Beta1SpecAllowedHostPaths:
    def __init__(
        self,
        *,
        path_prefix: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path_prefix: pathPrefix is the path prefix that the host volume must match. It does not support ``*``. Trailing slashes are trimmed when validating the path prefix with a host path. Examples: ``/foo`` would allow ``/foo``, ``/foo/`` and ``/foo/bar`` ``/foo`` would not allow ``/food`` or ``/etc/foo`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#path_prefix PodSecurityPolicyV1Beta1#path_prefix}
        :param read_only: when set to true, will allow host volumes matching the pathPrefix only if all volume mounts are readOnly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#read_only PodSecurityPolicyV1Beta1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae20616aa7f21889b5e8c3488860cedab7ca894c75b27e7b37f7d1519137e53)
            check_type(argname="argument path_prefix", value=path_prefix, expected_type=type_hints["path_prefix"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_prefix": path_prefix,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def path_prefix(self) -> builtins.str:
        '''pathPrefix is the path prefix that the host volume must match.

        It does not support ``*``. Trailing slashes are trimmed when validating the path prefix with a host path.

        Examples: ``/foo`` would allow ``/foo``, ``/foo/`` and ``/foo/bar`` ``/foo`` would not allow ``/food`` or ``/etc/foo``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#path_prefix PodSecurityPolicyV1Beta1#path_prefix}
        '''
        result = self._values.get("path_prefix")
        assert result is not None, "Required property 'path_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''when set to true, will allow host volumes matching the pathPrefix only if all volume mounts are readOnly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#read_only PodSecurityPolicyV1Beta1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecAllowedHostPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecAllowedHostPathsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecAllowedHostPathsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f523862d2a2741db5c0b8fa7d8a75370064cbb9d5f22e835cde5e13d2ddab1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecAllowedHostPathsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a36400b8e60ee09bd78367debd66f6040505d332c9e2cebb6cd25f77536f5e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecAllowedHostPathsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37344dba1d587c98e9c61d19c78cb58a273a5d8aaefc4ff8dc492ba584324f53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5416063272529b69f6aebebe1ac0b7174bb68ed00250b34a24b004285dc1c84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcfc9c1a5215bf34347eac42d31c2221de02855dd8dd7f46f68668b1d3682705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccadb00ea812b895162e2b1dc01ea63146cb71bc79bd193b3f34e0e771c9b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecAllowedHostPathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecAllowedHostPathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__645a355e4e7b338c453efcb645e9e42c8e15033219e38fcd5bb45d8586cd706a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="pathPrefixInput")
    def path_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="pathPrefix")
    def path_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPrefix"))

    @path_prefix.setter
    def path_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1700424d23c32708c6bec1c0f2665bc70de21c65a88a86311632e0c8515573f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c6dee6a979c3b871841066ddb02487f3ac3779cdb594a8a9e34cf139c339ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedHostPaths]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedHostPaths]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f311619a89054c39b5230ded212d8c6083e428eb073643c7d47388144a0034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecFsGroup",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "range": "range"},
)
class PodSecurityPolicyV1Beta1SpecFsGroup:
    def __init__(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecFsGroupRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate what FSGroup is used in the SecurityContext. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c92348a98fd131f754a39cfb9ff7730586a791a90bfa0e80922d7a03ac142b)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if range is not None:
            self._values["range"] = range

    @builtins.property
    def rule(self) -> builtins.str:
        '''rule is the strategy that will dictate what FSGroup is used in the SecurityContext.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecFsGroupRange"]]]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecFsGroupRange"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecFsGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecFsGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecFsGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f42b0e2a2014434ed385193993744b3887599f313016ed0015714dd96347e2f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecFsGroupRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926f971b25f80b2c19f76031ed1468771d8763bcb4d915e36cbcb074130006ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "PodSecurityPolicyV1Beta1SpecFsGroupRangeList":
        return typing.cast("PodSecurityPolicyV1Beta1SpecFsGroupRangeList", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecFsGroupRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecFsGroupRange"]]], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb73e6b49fe0814b960bb37d0354b0306a2ffa4435bb6a2ae5a5e203b47fbb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PodSecurityPolicyV1Beta1SpecFsGroup]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1SpecFsGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1SpecFsGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95da8f3139648f3c6460870e713d4068bd27e8dcb861eaba94d317df9b99a5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecFsGroupRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class PodSecurityPolicyV1Beta1SpecFsGroupRange:
    def __init__(self, *, max: jsii.Number, min: jsii.Number) -> None:
        '''
        :param max: max is the end of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        :param min: min is the start of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5547a2d747dc72d7d2778fc93943b1718647fa95dc8eeb78e56d0f1b3906739)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "min": min,
        }

    @builtins.property
    def max(self) -> jsii.Number:
        '''max is the end of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        '''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min(self) -> jsii.Number:
        '''min is the start of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecFsGroupRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecFsGroupRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecFsGroupRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd3cfc54e7e9f31121bd747241d9e2af963abbf689efcc53d462a5f28a2346e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecFsGroupRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497965dcd020f6da20eef2ffee711ed1bbc75ba1d5823d5ba8d335e49288a3e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecFsGroupRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c73df86db96fbce6d9d6cddba6664e0322e52b948eac55ebc2876a01b9d9478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d52466baa2e136c1dc02f2690dd51751cdf6cde0b1676e0510290ccea8ff9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28259e86c1ca684e2450b23d42a236df72ad88734fa34e84757bad1a364f8201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecFsGroupRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecFsGroupRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecFsGroupRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5f59e369d4e1365c073725a0fb734971d3ccbe0528b4a1ae1489fc072fc287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecFsGroupRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecFsGroupRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28a264f6d926852432fe2ed545738af710219547712dd9d0cefb35d44cc01752)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4829fc645ffe4799f9daaa1c61ff311fe8ebb7bdc121e12b2bdca770b0980b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0832aacf91a2b5632097aac4a684bb01ef7a49f3f44ae7e7324a8eeaf50d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecFsGroupRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecFsGroupRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecFsGroupRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b688cab0755d75adbd1d66721bb5bbbdb015f5d073eb865a0b9833088a54c1a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecHostPorts",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class PodSecurityPolicyV1Beta1SpecHostPorts:
    def __init__(self, *, max: jsii.Number, min: jsii.Number) -> None:
        '''
        :param max: max is the end of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        :param min: min is the start of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea3abc3b0f174b668f4a6854b99a29ef8091367352738c2cc428cafde9a3158)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "min": min,
        }

    @builtins.property
    def max(self) -> jsii.Number:
        '''max is the end of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        '''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min(self) -> jsii.Number:
        '''min is the start of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecHostPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecHostPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecHostPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37f48108e74853aa7ead63a588f4f39490b8371a5ee73bfef6c76401043820ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecHostPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd22d9fcf3c8917ff688a435ef57227fd30c6ece8973c0882d32dcec95ae9ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecHostPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efaede7c86f9dbe5e6aeffb855f6a863af7fdd76ca6fed03ae3d589062476a95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__468ea1e12ab773e72b18522f8f8b28357d12d999dd164f02a2c5e212b0c2c3fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31816f6a9705ea5e3e3155d6e537852ac8ec7683bfe2f983c2a21f48e64cef38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecHostPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecHostPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecHostPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f14854a57aea674d232841e9bfd5c8191180a4924c5b345cfbf50b591bb6496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecHostPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecHostPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c10587497fae5f57274b5c935de4b29e4a50665c71632be352906d7c191c827b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66af9d52b3afbcbf4ec4ea2d8e8f9e3a0d0fd37bac35c346240fee8bf5c9930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516f65f98df0506757ea5ce06604bb6ec3649fecd1590b594e09df99ca3cf103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecHostPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecHostPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecHostPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a2f69afeb92af864a42579ce6b84e673fce970923c017b3e17e6bb9b2e1ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fb8312c6c52eadadfc06d58db59534759336184f145238a12aec43229ed917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedFlexVolumes")
    def put_allowed_flex_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8fb77de85645e641ca621d58c6a6b00eefb0aabd3e70fb2103e093550240d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedFlexVolumes", [value]))

    @jsii.member(jsii_name="putAllowedHostPaths")
    def put_allowed_host_paths(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecAllowedHostPaths, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33217c692f0de6b203b934f746681816ad5393521cbbf530620d67b76dee164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedHostPaths", [value]))

    @jsii.member(jsii_name="putFsGroup")
    def put_fs_group(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecFsGroupRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate what FSGroup is used in the SecurityContext. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        value = PodSecurityPolicyV1Beta1SpecFsGroup(rule=rule, range=range)

        return typing.cast(None, jsii.invoke(self, "putFsGroup", [value]))

    @jsii.member(jsii_name="putHostPorts")
    def put_host_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecHostPorts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e085be028d47de8b47ae09600a093762f6591b061c595073cab5fb293a450987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHostPorts", [value]))

    @jsii.member(jsii_name="putRunAsGroup")
    def put_run_as_group(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsGroupRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate the allowable RunAsGroup values that may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        value = PodSecurityPolicyV1Beta1SpecRunAsGroup(rule=rule, range=range)

        return typing.cast(None, jsii.invoke(self, "putRunAsGroup", [value]))

    @jsii.member(jsii_name="putRunAsUser")
    def put_run_as_user(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsUserRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate the allowable RunAsUser values that may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        value = PodSecurityPolicyV1Beta1SpecRunAsUser(rule=rule, range=range)

        return typing.cast(None, jsii.invoke(self, "putRunAsUser", [value]))

    @jsii.member(jsii_name="putSeLinux")
    def put_se_linux(
        self,
        *,
        rule: builtins.str,
        se_linux_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate the allowable labels that may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param se_linux_options: se_linux_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#se_linux_options PodSecurityPolicyV1Beta1#se_linux_options}
        '''
        value = PodSecurityPolicyV1Beta1SpecSeLinux(
            rule=rule, se_linux_options=se_linux_options
        )

        return typing.cast(None, jsii.invoke(self, "putSeLinux", [value]))

    @jsii.member(jsii_name="putSupplementalGroups")
    def put_supplemental_groups(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate what supplemental groups is used in the SecurityContext. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        value = PodSecurityPolicyV1Beta1SpecSupplementalGroups(rule=rule, range=range)

        return typing.cast(None, jsii.invoke(self, "putSupplementalGroups", [value]))

    @jsii.member(jsii_name="resetAllowedCapabilities")
    def reset_allowed_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedCapabilities", []))

    @jsii.member(jsii_name="resetAllowedFlexVolumes")
    def reset_allowed_flex_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedFlexVolumes", []))

    @jsii.member(jsii_name="resetAllowedHostPaths")
    def reset_allowed_host_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHostPaths", []))

    @jsii.member(jsii_name="resetAllowedProcMountTypes")
    def reset_allowed_proc_mount_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedProcMountTypes", []))

    @jsii.member(jsii_name="resetAllowedUnsafeSysctls")
    def reset_allowed_unsafe_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedUnsafeSysctls", []))

    @jsii.member(jsii_name="resetAllowPrivilegeEscalation")
    def reset_allow_privilege_escalation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowPrivilegeEscalation", []))

    @jsii.member(jsii_name="resetDefaultAddCapabilities")
    def reset_default_add_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAddCapabilities", []))

    @jsii.member(jsii_name="resetDefaultAllowPrivilegeEscalation")
    def reset_default_allow_privilege_escalation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAllowPrivilegeEscalation", []))

    @jsii.member(jsii_name="resetForbiddenSysctls")
    def reset_forbidden_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForbiddenSysctls", []))

    @jsii.member(jsii_name="resetHostIpc")
    def reset_host_ipc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostIpc", []))

    @jsii.member(jsii_name="resetHostNetwork")
    def reset_host_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostNetwork", []))

    @jsii.member(jsii_name="resetHostPid")
    def reset_host_pid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPid", []))

    @jsii.member(jsii_name="resetHostPorts")
    def reset_host_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPorts", []))

    @jsii.member(jsii_name="resetPrivileged")
    def reset_privileged(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivileged", []))

    @jsii.member(jsii_name="resetReadOnlyRootFilesystem")
    def reset_read_only_root_filesystem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnlyRootFilesystem", []))

    @jsii.member(jsii_name="resetRequiredDropCapabilities")
    def reset_required_drop_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredDropCapabilities", []))

    @jsii.member(jsii_name="resetRunAsGroup")
    def reset_run_as_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunAsGroup", []))

    @jsii.member(jsii_name="resetSeLinux")
    def reset_se_linux(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeLinux", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @builtins.property
    @jsii.member(jsii_name="allowedFlexVolumes")
    def allowed_flex_volumes(
        self,
    ) -> PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesList:
        return typing.cast(PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesList, jsii.get(self, "allowedFlexVolumes"))

    @builtins.property
    @jsii.member(jsii_name="allowedHostPaths")
    def allowed_host_paths(self) -> PodSecurityPolicyV1Beta1SpecAllowedHostPathsList:
        return typing.cast(PodSecurityPolicyV1Beta1SpecAllowedHostPathsList, jsii.get(self, "allowedHostPaths"))

    @builtins.property
    @jsii.member(jsii_name="fsGroup")
    def fs_group(self) -> PodSecurityPolicyV1Beta1SpecFsGroupOutputReference:
        return typing.cast(PodSecurityPolicyV1Beta1SpecFsGroupOutputReference, jsii.get(self, "fsGroup"))

    @builtins.property
    @jsii.member(jsii_name="hostPorts")
    def host_ports(self) -> PodSecurityPolicyV1Beta1SpecHostPortsList:
        return typing.cast(PodSecurityPolicyV1Beta1SpecHostPortsList, jsii.get(self, "hostPorts"))

    @builtins.property
    @jsii.member(jsii_name="runAsGroup")
    def run_as_group(self) -> "PodSecurityPolicyV1Beta1SpecRunAsGroupOutputReference":
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsGroupOutputReference", jsii.get(self, "runAsGroup"))

    @builtins.property
    @jsii.member(jsii_name="runAsUser")
    def run_as_user(self) -> "PodSecurityPolicyV1Beta1SpecRunAsUserOutputReference":
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsUserOutputReference", jsii.get(self, "runAsUser"))

    @builtins.property
    @jsii.member(jsii_name="seLinux")
    def se_linux(self) -> "PodSecurityPolicyV1Beta1SpecSeLinuxOutputReference":
        return typing.cast("PodSecurityPolicyV1Beta1SpecSeLinuxOutputReference", jsii.get(self, "seLinux"))

    @builtins.property
    @jsii.member(jsii_name="supplementalGroups")
    def supplemental_groups(
        self,
    ) -> "PodSecurityPolicyV1Beta1SpecSupplementalGroupsOutputReference":
        return typing.cast("PodSecurityPolicyV1Beta1SpecSupplementalGroupsOutputReference", jsii.get(self, "supplementalGroups"))

    @builtins.property
    @jsii.member(jsii_name="allowedCapabilitiesInput")
    def allowed_capabilities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCapabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedFlexVolumesInput")
    def allowed_flex_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]], jsii.get(self, "allowedFlexVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHostPathsInput")
    def allowed_host_paths_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]], jsii.get(self, "allowedHostPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedProcMountTypesInput")
    def allowed_proc_mount_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedProcMountTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctlsInput")
    def allowed_unsafe_sysctls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedUnsafeSysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowPrivilegeEscalationInput")
    def allow_privilege_escalation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowPrivilegeEscalationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAddCapabilitiesInput")
    def default_add_capabilities_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultAddCapabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAllowPrivilegeEscalationInput")
    def default_allow_privilege_escalation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultAllowPrivilegeEscalationInput"))

    @builtins.property
    @jsii.member(jsii_name="forbiddenSysctlsInput")
    def forbidden_sysctls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forbiddenSysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="fsGroupInput")
    def fs_group_input(self) -> typing.Optional[PodSecurityPolicyV1Beta1SpecFsGroup]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1SpecFsGroup], jsii.get(self, "fsGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="hostIpcInput")
    def host_ipc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hostIpcInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNetworkInput")
    def host_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hostNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPidInput")
    def host_pid_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hostPidInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPortsInput")
    def host_ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecHostPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecHostPorts]]], jsii.get(self, "hostPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedInput")
    def privileged_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privilegedInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyRootFilesystemInput")
    def read_only_root_filesystem_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyRootFilesystemInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredDropCapabilitiesInput")
    def required_drop_capabilities_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredDropCapabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="runAsGroupInput")
    def run_as_group_input(
        self,
    ) -> typing.Optional["PodSecurityPolicyV1Beta1SpecRunAsGroup"]:
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1SpecRunAsGroup"], jsii.get(self, "runAsGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="runAsUserInput")
    def run_as_user_input(
        self,
    ) -> typing.Optional["PodSecurityPolicyV1Beta1SpecRunAsUser"]:
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1SpecRunAsUser"], jsii.get(self, "runAsUserInput"))

    @builtins.property
    @jsii.member(jsii_name="seLinuxInput")
    def se_linux_input(self) -> typing.Optional["PodSecurityPolicyV1Beta1SpecSeLinux"]:
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1SpecSeLinux"], jsii.get(self, "seLinuxInput"))

    @builtins.property
    @jsii.member(jsii_name="supplementalGroupsInput")
    def supplemental_groups_input(
        self,
    ) -> typing.Optional["PodSecurityPolicyV1Beta1SpecSupplementalGroups"]:
        return typing.cast(typing.Optional["PodSecurityPolicyV1Beta1SpecSupplementalGroups"], jsii.get(self, "supplementalGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCapabilities")
    def allowed_capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCapabilities"))

    @allowed_capabilities.setter
    def allowed_capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fcfbb5847babfcec17dd37ebe961c58c50d23470b935ed5ce9390af4ad231e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCapabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedProcMountTypes")
    def allowed_proc_mount_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedProcMountTypes"))

    @allowed_proc_mount_types.setter
    def allowed_proc_mount_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83616ebfb88da99b1848a0c6a2beacdebdbfe4e0daddb4c99998ea0eb33248ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedProcMountTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctls")
    def allowed_unsafe_sysctls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedUnsafeSysctls"))

    @allowed_unsafe_sysctls.setter
    def allowed_unsafe_sysctls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09b1a69f8c24040c7b34fe7a9bf4c338a03336747fff3e69806d587134559f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUnsafeSysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowPrivilegeEscalation")
    def allow_privilege_escalation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowPrivilegeEscalation"))

    @allow_privilege_escalation.setter
    def allow_privilege_escalation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828ca5a0544ae69d320aafdcac49d35f6ea80a183c7df02da1e46cbacc47a348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPrivilegeEscalation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAddCapabilities")
    def default_add_capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultAddCapabilities"))

    @default_add_capabilities.setter
    def default_add_capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31afcc76942955d1b75dc78cdbf9aed4b172d53270e21af6c2fdfeedf95b2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAddCapabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAllowPrivilegeEscalation")
    def default_allow_privilege_escalation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultAllowPrivilegeEscalation"))

    @default_allow_privilege_escalation.setter
    def default_allow_privilege_escalation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a32f4ff52330634c2403c5556f8c47bf49ccb3caa0ed998b2692309f0a2c4ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAllowPrivilegeEscalation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forbiddenSysctls")
    def forbidden_sysctls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forbiddenSysctls"))

    @forbidden_sysctls.setter
    def forbidden_sysctls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac4023b3f3cd8b64a516fa1ca1209fe407f33aa57b942d862a949aabf1e7c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forbiddenSysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostIpc")
    def host_ipc(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hostIpc"))

    @host_ipc.setter
    def host_ipc(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e466d1b154ef802da9f1884c06521e440d8cf6cd7730c14d8cc7e0197b2c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostIpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostNetwork")
    def host_network(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hostNetwork"))

    @host_network.setter
    def host_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4b2793d3d11c872a16c29d27cfb08635d1c26b09e0d2068aa53a6c5fc2382c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostPid")
    def host_pid(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hostPid"))

    @host_pid.setter
    def host_pid(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1ddd5e270572830dde5341be66a3c887dc41a6fabb0f0eb1d8ea3933748b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostPid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privileged"))

    @privileged.setter
    def privileged(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ef2c20598c0dcdbeb12c83ab3b1fb5605bf813b37d123b0d7355694e51baae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privileged", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnlyRootFilesystem")
    def read_only_root_filesystem(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnlyRootFilesystem"))

    @read_only_root_filesystem.setter
    def read_only_root_filesystem(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0786f7a1cef3a67de4c1557a6f80dcd96513638bbc4d081358a616c4221574d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnlyRootFilesystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredDropCapabilities")
    def required_drop_capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredDropCapabilities"))

    @required_drop_capabilities.setter
    def required_drop_capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f1f1550026ad5e5f005b557788859e6a1737689a9fc672ca8f2cc2bf2a994e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredDropCapabilities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "volumes"))

    @volumes.setter
    def volumes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c67710c10e791a6d98fe8ab3af088a6dbb237bf78997b98bd120f638da39757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PodSecurityPolicyV1Beta1Spec]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1Spec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1Spec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb7781b4609500bca9870b98d90caff56bd2b5a1c83304817c6df7733885a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsGroup",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "range": "range"},
)
class PodSecurityPolicyV1Beta1SpecRunAsGroup:
    def __init__(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsGroupRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate the allowable RunAsGroup values that may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211822933d64833b106a0b23f3b3b44dcf993b229e0e577c06109c94e2d1dff7)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if range is not None:
            self._values["range"] = range

    @builtins.property
    def rule(self) -> builtins.str:
        '''rule is the strategy that will dictate the allowable RunAsGroup values that may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsGroupRange"]]]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsGroupRange"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecRunAsGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecRunAsGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eef94b494f73518b7dac7642bb2cc2f8c0471d8551fe9e0e9704f73a46be29d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsGroupRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4580fc9197ff0872a16bad29f23488e29fc18c0faee36f8cacce845b0728f96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "PodSecurityPolicyV1Beta1SpecRunAsGroupRangeList":
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsGroupRangeList", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsGroupRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsGroupRange"]]], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d4356fe9aa48279a021d19d637c387e51715cfd3fedbde9870c8257c16c2af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsGroup]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e9ea3078f6dc5fc5763c7b8f1e67fa00315905209ef4e1ed1506f3f084cd28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsGroupRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class PodSecurityPolicyV1Beta1SpecRunAsGroupRange:
    def __init__(self, *, max: jsii.Number, min: jsii.Number) -> None:
        '''
        :param max: max is the end of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        :param min: min is the start of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c39c442931a5b28dfc936b20c5bafd9539a8a5d977d60c3ae08da7bfc78b2e8)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "min": min,
        }

    @builtins.property
    def max(self) -> jsii.Number:
        '''max is the end of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        '''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min(self) -> jsii.Number:
        '''min is the start of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecRunAsGroupRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecRunAsGroupRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsGroupRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0c9e44e3b1abb06a537e5b0b0a0d95bdb0e946166737ece0e0894f58f7d51e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecRunAsGroupRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10f993fbfc52d405341746f8c3b318be8a6a27a70a07da51a93051a1cf278e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsGroupRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2633efaf289a6631fc14c343623cef3f00d219004766c09a7fb12ce6f79cf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a1543c085b477edfb9591c499b2a077d6ea6cd93fe83ee8b50c6d7f377051b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87f221ecd3a44487cc7f79fcc933b21048d24e95fab5af6d755515e03cb51ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsGroupRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsGroupRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsGroupRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30694973913de2d542c19f02a63ba31c38b62264c4b31455dc04a08c7fdaa3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecRunAsGroupRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsGroupRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a606d3819479cf1f418a4bac806d19e5dc17fab32135373e70346d3fe5b5b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3b6456efaf28253dd97e591f0efd8cd227885536cd21709b9283eef1480c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f94c525abc0fb60200094f937146bea5475a1fded380596b0d44d4991f72e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsGroupRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsGroupRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsGroupRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41a5c69688a34fe01e7280fcc046093d0a7034d7f39cd43027f556c1b40b0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsUser",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "range": "range"},
)
class PodSecurityPolicyV1Beta1SpecRunAsUser:
    def __init__(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsUserRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate the allowable RunAsUser values that may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf77d17bc478f2ed9d23911ca0e5ba70ca1038c3ab4bb35fa5ef5566b556363)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if range is not None:
            self._values["range"] = range

    @builtins.property
    def rule(self) -> builtins.str:
        '''rule is the strategy that will dictate the allowable RunAsUser values that may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsUserRange"]]]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsUserRange"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecRunAsUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecRunAsUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e44bda5d11750cdae903650efa5f185e5fc395fe29b9f309c27a3ab4f730dc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecRunAsUserRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b047594d78d02569fbd5cc3c9578eabf3dfe2f5acfe40bb9b673cb065add338b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "PodSecurityPolicyV1Beta1SpecRunAsUserRangeList":
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsUserRangeList", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsUserRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecRunAsUserRange"]]], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee1cdb42b763a095f316850f97dd580587169d6f13ad44cb9f70aef9374bc54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsUser]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ce4a8388e4d2aae9828ced089b1fd1cfee0bee11dd1085fd7c92f604c759db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsUserRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class PodSecurityPolicyV1Beta1SpecRunAsUserRange:
    def __init__(self, *, max: jsii.Number, min: jsii.Number) -> None:
        '''
        :param max: max is the end of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        :param min: min is the start of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa22b7de5c5cf8391f2021a57a8472e7ca55f266c43051d433c3a425d44ff82)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "min": min,
        }

    @builtins.property
    def max(self) -> jsii.Number:
        '''max is the end of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        '''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min(self) -> jsii.Number:
        '''min is the start of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecRunAsUserRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecRunAsUserRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsUserRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fed7aef6ab02a0d29cf5d934bdbe6f84947e7c1b2659016cf1effb983a4abce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecRunAsUserRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b8562deed966bc8afd2f803926ffe74bb3828efb807285e6061c76ef1784ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecRunAsUserRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4115986f1b8dc3759a8c2bfaae723f85a47a8311755bedddb771760a9b42699)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57d7a85029218e7497772a4cdca24fb2d1fa4257417413b6c912bd5283d1abf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c60fce5b56e7e8409ca984d0e5973ad19361d672dc433f7dd3c62534586700f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsUserRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsUserRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsUserRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87d778acbaa9030dfd4451803d032c0762fd324d774e0a89f01641134653c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecRunAsUserRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecRunAsUserRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df11ea0732dd21815616e09d8bbc0c457bed5aeabaa1131e5ada2ce74906a85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fe68570cc8d50aa1b404d881eeac8f6c892a46b98a4ecc752fc64a00b353f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0804b76bdeababca69738acc2f67d055cbb23c535121341404fbc4225b29fcd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsUserRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsUserRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsUserRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec6fe3099054f5b776f7aab62d3ff0be245ded93407a7609999b17d6d188bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSeLinux",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "se_linux_options": "seLinuxOptions"},
)
class PodSecurityPolicyV1Beta1SpecSeLinux:
    def __init__(
        self,
        *,
        rule: builtins.str,
        se_linux_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate the allowable labels that may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param se_linux_options: se_linux_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#se_linux_options PodSecurityPolicyV1Beta1#se_linux_options}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5081d96efca3117a41d6b7d4175a7a2db716b62c37d4395a82e4be61616d763)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument se_linux_options", value=se_linux_options, expected_type=type_hints["se_linux_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if se_linux_options is not None:
            self._values["se_linux_options"] = se_linux_options

    @builtins.property
    def rule(self) -> builtins.str:
        '''rule is the strategy that will dictate the allowable labels that may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def se_linux_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions"]]]:
        '''se_linux_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#se_linux_options PodSecurityPolicyV1Beta1#se_linux_options}
        '''
        result = self._values.get("se_linux_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecSeLinux(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecSeLinuxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSeLinuxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19e176b8e3f861d9bd0ac0d25e8c31716495356b5638fa9a4e149034e3c3419)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSeLinuxOptions")
    def put_se_linux_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc631b2ad2f28cebd6f8d4d1b1ed989f55d4b84bb520a1ffa358473cb7f48b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeLinuxOptions", [value]))

    @jsii.member(jsii_name="resetSeLinuxOptions")
    def reset_se_linux_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeLinuxOptions", []))

    @builtins.property
    @jsii.member(jsii_name="seLinuxOptions")
    def se_linux_options(
        self,
    ) -> "PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsList":
        return typing.cast("PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsList", jsii.get(self, "seLinuxOptions"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="seLinuxOptionsInput")
    def se_linux_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions"]]], jsii.get(self, "seLinuxOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dafc90ba586578b9c0c0683e74c09c93fb49298a94c79c4eca26e2714c80803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PodSecurityPolicyV1Beta1SpecSeLinux]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1SpecSeLinux], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1SpecSeLinux],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923d662cb07df29372519a3ebdeb29d573e1246533985832a287a9057a02ecdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions",
    jsii_struct_bases=[],
    name_mapping={"level": "level", "role": "role", "type": "type", "user": "user"},
)
class PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions:
    def __init__(
        self,
        *,
        level: builtins.str,
        role: builtins.str,
        type: builtins.str,
        user: builtins.str,
    ) -> None:
        '''
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#level PodSecurityPolicyV1Beta1#level}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#role PodSecurityPolicyV1Beta1#role}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#type PodSecurityPolicyV1Beta1#type}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#user PodSecurityPolicyV1Beta1#user}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662beefe0b5c677ac679aa2aea3ff1195e2589deb8bd70151c942eec769cba23)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "level": level,
            "role": role,
            "type": type,
            "user": user,
        }

    @builtins.property
    def level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#level PodSecurityPolicyV1Beta1#level}.'''
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#role PodSecurityPolicyV1Beta1#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#type PodSecurityPolicyV1Beta1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#user PodSecurityPolicyV1Beta1#user}.'''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__595276051905b21d41395c0d96e6aa861764628ac1a41197a8eb70e6265093cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1cfdbb4cc2de5d7298751ef855ba0e03cfed87e34864c458ab36a0bbf736fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48176dd269980055f1ec290986650cfb8834b1fb3605b1eba2b81acbd0130950)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7feb99b0340ad8f8763b15228e88ec8e88f6283ee5294d2cd9b2b3541e0f7e47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f18d4c6cea983e9b943d258a25b1cc80f1a5bf9efa86b6df346ccab5f291b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b1f63043f2af8d9f6a14732430d42172117336d6072473852bbd74126ff4d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7cfd2192b353038070042a70bfe2bb832493b2f4fdf9d06214e1774d0169177)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b319644c28c5e5845521662eb539f18c9507587593c4702aebc3dcaeda64bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e199b757192b2b00e809960c4366be23b62ea9bf5051187725d32c8adc49384f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b0c40d1e98514ffafb3d718c06ae051c22d4fff561c20161153510cd2da54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50eeabce5c4b0db71d776be5ab94a9274a7ec3d292aca33f5eba2ae9d932b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa04047e19248ff988044053574b3a997ec218a12ee2dd1b7f99683ee3adc8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSupplementalGroups",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "range": "range"},
)
class PodSecurityPolicyV1Beta1SpecSupplementalGroups:
    def __init__(
        self,
        *,
        rule: builtins.str,
        range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param rule: rule is the strategy that will dictate what supplemental groups is used in the SecurityContext. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        :param range: range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411301606243cd5f6c043514ecf91e9333c63bf388b967ed55933d3d881d8eb6)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if range is not None:
            self._values["range"] = range

    @builtins.property
    def rule(self) -> builtins.str:
        '''rule is the strategy that will dictate what supplemental groups is used in the SecurityContext.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#rule PodSecurityPolicyV1Beta1#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange"]]]:
        '''range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#range PodSecurityPolicyV1Beta1#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecSupplementalGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecSupplementalGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSupplementalGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__028717aa5c9c056f149368866a3d8afc05855463144b69a9910686f40c4abbcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6e95603889a525932c7009a0662b9c3403fc8f1b2ed152a1a7ef52ecab04d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeList":
        return typing.cast("PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeList", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange"]]], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759dd09ff3d570857e72611ff7e952bef973e97aac4b560935cf59be36540451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PodSecurityPolicyV1Beta1SpecSupplementalGroups]:
        return typing.cast(typing.Optional[PodSecurityPolicyV1Beta1SpecSupplementalGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PodSecurityPolicyV1Beta1SpecSupplementalGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1577b871836e9bcda6f4df0db71a1b252af7966dcd7be35bbbbe1f81501d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange:
    def __init__(self, *, max: jsii.Number, min: jsii.Number) -> None:
        '''
        :param max: max is the end of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        :param min: min is the start of the range, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34cfc469760e2dc99deb5664cfe9931d896e5bca62e1e221de1bac84a25f20a)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max": max,
            "min": min,
        }

    @builtins.property
    def max(self) -> jsii.Number:
        '''max is the end of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#max PodSecurityPolicyV1Beta1#max}
        '''
        result = self._values.get("max")
        assert result is not None, "Required property 'max' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min(self) -> jsii.Number:
        '''min is the start of the range, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/pod_security_policy_v1beta1#min PodSecurityPolicyV1Beta1#min}
        '''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d5b7638fb0dcdcf3490ee0b573fca89ade9ea4a119ce8ccb1f1730757e787df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd89ce90e6e5e015c3b2b4afca424fac67444ce6ca9ff9299c026979d5b7196)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8968d02b045077a5f97339692dc37f2b806c5640b27b8738d359b7593a7dc471)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3afae16bc75cbed8fe4fe71d7c748cb0fb8b73d9ff027d875aabe64176eef26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e43db9f3b9c6b8ac97998ccb86004a04b9a0d67dbbf3a3e5c6765b368e16a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cec699d26167db66c5af1bd1d03fdd08ba9c40c3a3e4eaaca53babc94319ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.podSecurityPolicyV1Beta1.PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6edf6319ae8d7ad05b31defc65f36f5f134470b66cc32f3409aa3835fa82d0f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae6e4a754f2a1a5f8fc43354b3eaff9bdcdb6e38b6c8a90a8cebc0bdea0aaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125939bf30387ef4a2bfb9db25ca96e547fa77ace6a779360a51d95e97d58014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f9e4e5316ec2240a74ba85b5e09f6817c6315f0d84859e51378a7feeea69f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PodSecurityPolicyV1Beta1",
    "PodSecurityPolicyV1Beta1Config",
    "PodSecurityPolicyV1Beta1Metadata",
    "PodSecurityPolicyV1Beta1MetadataOutputReference",
    "PodSecurityPolicyV1Beta1Spec",
    "PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes",
    "PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesList",
    "PodSecurityPolicyV1Beta1SpecAllowedFlexVolumesOutputReference",
    "PodSecurityPolicyV1Beta1SpecAllowedHostPaths",
    "PodSecurityPolicyV1Beta1SpecAllowedHostPathsList",
    "PodSecurityPolicyV1Beta1SpecAllowedHostPathsOutputReference",
    "PodSecurityPolicyV1Beta1SpecFsGroup",
    "PodSecurityPolicyV1Beta1SpecFsGroupOutputReference",
    "PodSecurityPolicyV1Beta1SpecFsGroupRange",
    "PodSecurityPolicyV1Beta1SpecFsGroupRangeList",
    "PodSecurityPolicyV1Beta1SpecFsGroupRangeOutputReference",
    "PodSecurityPolicyV1Beta1SpecHostPorts",
    "PodSecurityPolicyV1Beta1SpecHostPortsList",
    "PodSecurityPolicyV1Beta1SpecHostPortsOutputReference",
    "PodSecurityPolicyV1Beta1SpecOutputReference",
    "PodSecurityPolicyV1Beta1SpecRunAsGroup",
    "PodSecurityPolicyV1Beta1SpecRunAsGroupOutputReference",
    "PodSecurityPolicyV1Beta1SpecRunAsGroupRange",
    "PodSecurityPolicyV1Beta1SpecRunAsGroupRangeList",
    "PodSecurityPolicyV1Beta1SpecRunAsGroupRangeOutputReference",
    "PodSecurityPolicyV1Beta1SpecRunAsUser",
    "PodSecurityPolicyV1Beta1SpecRunAsUserOutputReference",
    "PodSecurityPolicyV1Beta1SpecRunAsUserRange",
    "PodSecurityPolicyV1Beta1SpecRunAsUserRangeList",
    "PodSecurityPolicyV1Beta1SpecRunAsUserRangeOutputReference",
    "PodSecurityPolicyV1Beta1SpecSeLinux",
    "PodSecurityPolicyV1Beta1SpecSeLinuxOutputReference",
    "PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions",
    "PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsList",
    "PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptionsOutputReference",
    "PodSecurityPolicyV1Beta1SpecSupplementalGroups",
    "PodSecurityPolicyV1Beta1SpecSupplementalGroupsOutputReference",
    "PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange",
    "PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeList",
    "PodSecurityPolicyV1Beta1SpecSupplementalGroupsRangeOutputReference",
]

publication.publish()

def _typecheckingstub__0e02854aec8a5588213790b571c2d7ba4311e8cd4b48cc1d690042ffd2f1cd52(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[PodSecurityPolicyV1Beta1Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[PodSecurityPolicyV1Beta1Spec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__31158a61ffa87bdaf1b9e545da5d52d5c0c23db0bf2ac4178e33c6a2d87a988b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3285b0fc10addff7575865f4f74736f276e5611fce8ee28153d59c07376a5e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f46ed709073b3ccfd76762b5b553fe7e44ab1b6cda4360690a59bf46728741(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[PodSecurityPolicyV1Beta1Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[PodSecurityPolicyV1Beta1Spec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fbe505cb19bd64a98a95dc42885883acea5b84e48c042659fef639f874ac8b(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78569ea75bf9935f75cc5b16d7c070869de4566af61334d45431224b9efcd9b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ead0d67408d3aa58cc553e7834e7ae314287199d103ed41e58b20d107b31b1d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dfad94f2e73b9ffe5a64d86bd84b92dd943961b9a72cfd457ded419d33299f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24beb3718fbe6977a37c49e1387e3d74241d4aec6af19579701478bfd6c17556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a43972fe1240de997939e371be41b05d39de07ac9c616f9ef21df47e817ff6(
    value: typing.Optional[PodSecurityPolicyV1Beta1Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd1557da641c756ca1df9bcd67b39345639e49dded7d2352538b528994893fc(
    *,
    fs_group: typing.Union[PodSecurityPolicyV1Beta1SpecFsGroup, typing.Dict[builtins.str, typing.Any]],
    run_as_user: typing.Union[PodSecurityPolicyV1Beta1SpecRunAsUser, typing.Dict[builtins.str, typing.Any]],
    supplemental_groups: typing.Union[PodSecurityPolicyV1Beta1SpecSupplementalGroups, typing.Dict[builtins.str, typing.Any]],
    allowed_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_flex_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_host_paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecAllowedHostPaths, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_proc_mount_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_add_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forbidden_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
    host_ipc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_pid: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecHostPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_drop_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    run_as_group: typing.Optional[typing.Union[PodSecurityPolicyV1Beta1SpecRunAsGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    se_linux: typing.Optional[typing.Union[PodSecurityPolicyV1Beta1SpecSeLinux, typing.Dict[builtins.str, typing.Any]]] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742bd87d46cb3e8164811e2f053cc6125bf713618795de393df7526f9fde4839(
    *,
    driver: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ac647ef51f3e9eb74392e3b294973e4ba5fe7d82011bc01a636104b11528b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570febd07fd3277f63d4a1722d41cbde0d52bfd72856d1faac0a7bf3b3b7ab80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cb9085c30d88be5c958d976135b04e8d6114fbbea38f04893208af57ed1ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdce35b4b8b0a0f17dbebf5c9190e8dbeca48866ca288d393d08223fc5c35dde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdbdefb1d5b0c6043b4cb72f098ef872c741f7fd0bde69ac2658fc165489e94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8453dbf178fb7d170349f1a2b821e8b52096d28a1e983b70c3435ff794496b7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8a44a671051bc353737a2dcafb8f6be198c844ea321db0d339cbfefeafdd19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd5bcd63d2b0dcc3785b4b3dba6696475ebd95a53b20c6b5ebc1a878b9cbba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a4f9050575ab982d997231cdba679119584adbc3048e78670e825af0103e3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae20616aa7f21889b5e8c3488860cedab7ca894c75b27e7b37f7d1519137e53(
    *,
    path_prefix: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f523862d2a2741db5c0b8fa7d8a75370064cbb9d5f22e835cde5e13d2ddab1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a36400b8e60ee09bd78367debd66f6040505d332c9e2cebb6cd25f77536f5e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37344dba1d587c98e9c61d19c78cb58a273a5d8aaefc4ff8dc492ba584324f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5416063272529b69f6aebebe1ac0b7174bb68ed00250b34a24b004285dc1c84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfc9c1a5215bf34347eac42d31c2221de02855dd8dd7f46f68668b1d3682705(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccadb00ea812b895162e2b1dc01ea63146cb71bc79bd193b3f34e0e771c9b96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecAllowedHostPaths]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645a355e4e7b338c453efcb645e9e42c8e15033219e38fcd5bb45d8586cd706a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1700424d23c32708c6bec1c0f2665bc70de21c65a88a86311632e0c8515573f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c6dee6a979c3b871841066ddb02487f3ac3779cdb594a8a9e34cf139c339ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f311619a89054c39b5230ded212d8c6083e428eb073643c7d47388144a0034(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecAllowedHostPaths]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c92348a98fd131f754a39cfb9ff7730586a791a90bfa0e80922d7a03ac142b(
    *,
    rule: builtins.str,
    range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecFsGroupRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42b0e2a2014434ed385193993744b3887599f313016ed0015714dd96347e2f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926f971b25f80b2c19f76031ed1468771d8763bcb4d915e36cbcb074130006ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecFsGroupRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb73e6b49fe0814b960bb37d0354b0306a2ffa4435bb6a2ae5a5e203b47fbb18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95da8f3139648f3c6460870e713d4068bd27e8dcb861eaba94d317df9b99a5aa(
    value: typing.Optional[PodSecurityPolicyV1Beta1SpecFsGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5547a2d747dc72d7d2778fc93943b1718647fa95dc8eeb78e56d0f1b3906739(
    *,
    max: jsii.Number,
    min: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd3cfc54e7e9f31121bd747241d9e2af963abbf689efcc53d462a5f28a2346e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497965dcd020f6da20eef2ffee711ed1bbc75ba1d5823d5ba8d335e49288a3e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c73df86db96fbce6d9d6cddba6664e0322e52b948eac55ebc2876a01b9d9478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d52466baa2e136c1dc02f2690dd51751cdf6cde0b1676e0510290ccea8ff9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28259e86c1ca684e2450b23d42a236df72ad88734fa34e84757bad1a364f8201(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5f59e369d4e1365c073725a0fb734971d3ccbe0528b4a1ae1489fc072fc287(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecFsGroupRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a264f6d926852432fe2ed545738af710219547712dd9d0cefb35d44cc01752(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4829fc645ffe4799f9daaa1c61ff311fe8ebb7bdc121e12b2bdca770b0980b0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0832aacf91a2b5632097aac4a684bb01ef7a49f3f44ae7e7324a8eeaf50d6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b688cab0755d75adbd1d66721bb5bbbdb015f5d073eb865a0b9833088a54c1a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecFsGroupRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea3abc3b0f174b668f4a6854b99a29ef8091367352738c2cc428cafde9a3158(
    *,
    max: jsii.Number,
    min: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f48108e74853aa7ead63a588f4f39490b8371a5ee73bfef6c76401043820ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd22d9fcf3c8917ff688a435ef57227fd30c6ece8973c0882d32dcec95ae9ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efaede7c86f9dbe5e6aeffb855f6a863af7fdd76ca6fed03ae3d589062476a95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468ea1e12ab773e72b18522f8f8b28357d12d999dd164f02a2c5e212b0c2c3fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31816f6a9705ea5e3e3155d6e537852ac8ec7683bfe2f983c2a21f48e64cef38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f14854a57aea674d232841e9bfd5c8191180a4924c5b345cfbf50b591bb6496(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecHostPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10587497fae5f57274b5c935de4b29e4a50665c71632be352906d7c191c827b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66af9d52b3afbcbf4ec4ea2d8e8f9e3a0d0fd37bac35c346240fee8bf5c9930(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516f65f98df0506757ea5ce06604bb6ec3649fecd1590b594e09df99ca3cf103(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a2f69afeb92af864a42579ce6b84e673fce970923c017b3e17e6bb9b2e1ca9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecHostPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fb8312c6c52eadadfc06d58db59534759336184f145238a12aec43229ed917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8fb77de85645e641ca621d58c6a6b00eefb0aabd3e70fb2103e093550240d4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecAllowedFlexVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33217c692f0de6b203b934f746681816ad5393521cbbf530620d67b76dee164(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecAllowedHostPaths, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e085be028d47de8b47ae09600a093762f6591b061c595073cab5fb293a450987(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecHostPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcfbb5847babfcec17dd37ebe961c58c50d23470b935ed5ce9390af4ad231e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83616ebfb88da99b1848a0c6a2beacdebdbfe4e0daddb4c99998ea0eb33248ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09b1a69f8c24040c7b34fe7a9bf4c338a03336747fff3e69806d587134559f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828ca5a0544ae69d320aafdcac49d35f6ea80a183c7df02da1e46cbacc47a348(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31afcc76942955d1b75dc78cdbf9aed4b172d53270e21af6c2fdfeedf95b2a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a32f4ff52330634c2403c5556f8c47bf49ccb3caa0ed998b2692309f0a2c4ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac4023b3f3cd8b64a516fa1ca1209fe407f33aa57b942d862a949aabf1e7c3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e466d1b154ef802da9f1884c06521e440d8cf6cd7730c14d8cc7e0197b2c01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4b2793d3d11c872a16c29d27cfb08635d1c26b09e0d2068aa53a6c5fc2382c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1ddd5e270572830dde5341be66a3c887dc41a6fabb0f0eb1d8ea3933748b87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ef2c20598c0dcdbeb12c83ab3b1fb5605bf813b37d123b0d7355694e51baae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0786f7a1cef3a67de4c1557a6f80dcd96513638bbc4d081358a616c4221574d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f1f1550026ad5e5f005b557788859e6a1737689a9fc672ca8f2cc2bf2a994e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c67710c10e791a6d98fe8ab3af088a6dbb237bf78997b98bd120f638da39757(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb7781b4609500bca9870b98d90caff56bd2b5a1c83304817c6df7733885a3b(
    value: typing.Optional[PodSecurityPolicyV1Beta1Spec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211822933d64833b106a0b23f3b3b44dcf993b229e0e577c06109c94e2d1dff7(
    *,
    rule: builtins.str,
    range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecRunAsGroupRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eef94b494f73518b7dac7642bb2cc2f8c0471d8551fe9e0e9704f73a46be29d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4580fc9197ff0872a16bad29f23488e29fc18c0faee36f8cacce845b0728f96d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecRunAsGroupRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d4356fe9aa48279a021d19d637c387e51715cfd3fedbde9870c8257c16c2af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e9ea3078f6dc5fc5763c7b8f1e67fa00315905209ef4e1ed1506f3f084cd28(
    value: typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c39c442931a5b28dfc936b20c5bafd9539a8a5d977d60c3ae08da7bfc78b2e8(
    *,
    max: jsii.Number,
    min: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c9e44e3b1abb06a537e5b0b0a0d95bdb0e946166737ece0e0894f58f7d51e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10f993fbfc52d405341746f8c3b318be8a6a27a70a07da51a93051a1cf278e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2633efaf289a6631fc14c343623cef3f00d219004766c09a7fb12ce6f79cf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a1543c085b477edfb9591c499b2a077d6ea6cd93fe83ee8b50c6d7f377051b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f221ecd3a44487cc7f79fcc933b21048d24e95fab5af6d755515e03cb51ecb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30694973913de2d542c19f02a63ba31c38b62264c4b31455dc04a08c7fdaa3c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsGroupRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a606d3819479cf1f418a4bac806d19e5dc17fab32135373e70346d3fe5b5b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3b6456efaf28253dd97e591f0efd8cd227885536cd21709b9283eef1480c36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f94c525abc0fb60200094f937146bea5475a1fded380596b0d44d4991f72e59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41a5c69688a34fe01e7280fcc046093d0a7034d7f39cd43027f556c1b40b0d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsGroupRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf77d17bc478f2ed9d23911ca0e5ba70ca1038c3ab4bb35fa5ef5566b556363(
    *,
    rule: builtins.str,
    range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecRunAsUserRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e44bda5d11750cdae903650efa5f185e5fc395fe29b9f309c27a3ab4f730dc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b047594d78d02569fbd5cc3c9578eabf3dfe2f5acfe40bb9b673cb065add338b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecRunAsUserRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee1cdb42b763a095f316850f97dd580587169d6f13ad44cb9f70aef9374bc54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ce4a8388e4d2aae9828ced089b1fd1cfee0bee11dd1085fd7c92f604c759db(
    value: typing.Optional[PodSecurityPolicyV1Beta1SpecRunAsUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa22b7de5c5cf8391f2021a57a8472e7ca55f266c43051d433c3a425d44ff82(
    *,
    max: jsii.Number,
    min: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fed7aef6ab02a0d29cf5d934bdbe6f84947e7c1b2659016cf1effb983a4abce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b8562deed966bc8afd2f803926ffe74bb3828efb807285e6061c76ef1784ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4115986f1b8dc3759a8c2bfaae723f85a47a8311755bedddb771760a9b42699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d7a85029218e7497772a4cdca24fb2d1fa4257417413b6c912bd5283d1abf4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60fce5b56e7e8409ca984d0e5973ad19361d672dc433f7dd3c62534586700f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87d778acbaa9030dfd4451803d032c0762fd324d774e0a89f01641134653c34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecRunAsUserRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df11ea0732dd21815616e09d8bbc0c457bed5aeabaa1131e5ada2ce74906a85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fe68570cc8d50aa1b404d881eeac8f6c892a46b98a4ecc752fc64a00b353f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0804b76bdeababca69738acc2f67d055cbb23c535121341404fbc4225b29fcd4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec6fe3099054f5b776f7aab62d3ff0be245ded93407a7609999b17d6d188bbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecRunAsUserRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5081d96efca3117a41d6b7d4175a7a2db716b62c37d4395a82e4be61616d763(
    *,
    rule: builtins.str,
    se_linux_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19e176b8e3f861d9bd0ac0d25e8c31716495356b5638fa9a4e149034e3c3419(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc631b2ad2f28cebd6f8d4d1b1ed989f55d4b84bb520a1ffa358473cb7f48b1c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dafc90ba586578b9c0c0683e74c09c93fb49298a94c79c4eca26e2714c80803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923d662cb07df29372519a3ebdeb29d573e1246533985832a287a9057a02ecdb(
    value: typing.Optional[PodSecurityPolicyV1Beta1SpecSeLinux],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662beefe0b5c677ac679aa2aea3ff1195e2589deb8bd70151c942eec769cba23(
    *,
    level: builtins.str,
    role: builtins.str,
    type: builtins.str,
    user: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595276051905b21d41395c0d96e6aa861764628ac1a41197a8eb70e6265093cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1cfdbb4cc2de5d7298751ef855ba0e03cfed87e34864c458ab36a0bbf736fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48176dd269980055f1ec290986650cfb8834b1fb3605b1eba2b81acbd0130950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7feb99b0340ad8f8763b15228e88ec8e88f6283ee5294d2cd9b2b3541e0f7e47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f18d4c6cea983e9b943d258a25b1cc80f1a5bf9efa86b6df346ccab5f291b37(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b1f63043f2af8d9f6a14732430d42172117336d6072473852bbd74126ff4d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cfd2192b353038070042a70bfe2bb832493b2f4fdf9d06214e1774d0169177(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b319644c28c5e5845521662eb539f18c9507587593c4702aebc3dcaeda64bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e199b757192b2b00e809960c4366be23b62ea9bf5051187725d32c8adc49384f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b0c40d1e98514ffafb3d718c06ae051c22d4fff561c20161153510cd2da54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50eeabce5c4b0db71d776be5ab94a9274a7ec3d292aca33f5eba2ae9d932b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa04047e19248ff988044053574b3a997ec218a12ee2dd1b7f99683ee3adc8c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSeLinuxSeLinuxOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411301606243cd5f6c043514ecf91e9333c63bf388b967ed55933d3d881d8eb6(
    *,
    rule: builtins.str,
    range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028717aa5c9c056f149368866a3d8afc05855463144b69a9910686f40c4abbcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6e95603889a525932c7009a0662b9c3403fc8f1b2ed152a1a7ef52ecab04d3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759dd09ff3d570857e72611ff7e952bef973e97aac4b560935cf59be36540451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1577b871836e9bcda6f4df0db71a1b252af7966dcd7be35bbbbe1f81501d35(
    value: typing.Optional[PodSecurityPolicyV1Beta1SpecSupplementalGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34cfc469760e2dc99deb5664cfe9931d896e5bca62e1e221de1bac84a25f20a(
    *,
    max: jsii.Number,
    min: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5b7638fb0dcdcf3490ee0b573fca89ade9ea4a119ce8ccb1f1730757e787df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd89ce90e6e5e015c3b2b4afca424fac67444ce6ca9ff9299c026979d5b7196(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8968d02b045077a5f97339692dc37f2b806c5640b27b8738d359b7593a7dc471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3afae16bc75cbed8fe4fe71d7c748cb0fb8b73d9ff027d875aabe64176eef26(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e43db9f3b9c6b8ac97998ccb86004a04b9a0d67dbbf3a3e5c6765b368e16a6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cec699d26167db66c5af1bd1d03fdd08ba9c40c3a3e4eaaca53babc94319ebf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6edf6319ae8d7ad05b31defc65f36f5f134470b66cc32f3409aa3835fa82d0f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae6e4a754f2a1a5f8fc43354b3eaff9bdcdb6e38b6c8a90a8cebc0bdea0aaad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125939bf30387ef4a2bfb9db25ca96e547fa77ace6a779360a51d95e97d58014(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f9e4e5316ec2240a74ba85b5e09f6817c6315f0d84859e51378a7feeea69f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PodSecurityPolicyV1Beta1SpecSupplementalGroupsRange]],
) -> None:
    """Type checking stubs"""
    pass
