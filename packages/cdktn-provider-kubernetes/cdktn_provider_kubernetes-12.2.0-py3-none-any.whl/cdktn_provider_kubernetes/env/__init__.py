r'''
# `kubernetes_env`

Refer to the Terraform Registry for docs: [`kubernetes_env`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env).
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


class Env(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.Env",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env kubernetes_env}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_version: builtins.str,
        env: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[builtins.str, typing.Any]]]],
        kind: builtins.str,
        metadata: typing.Union["EnvMetadata", typing.Dict[builtins.str, typing.Any]],
        container: typing.Optional[builtins.str] = None,
        field_manager: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        init_container: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env kubernetes_env} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_version: Resource API version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#api_version Env#api_version}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#env Env#env}
        :param kind: Resource Kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#kind Env#kind}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#metadata Env#metadata}
        :param container: Name of the container for which we are updating the environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#container Env#container}
        :param field_manager: Set the name of the field manager for the specified environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_manager Env#field_manager}
        :param force: Force overwriting environments that were created or edited outside of Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#force Env#force}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#id Env#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param init_container: Name of the initContainer for which we are updating the environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#init_container Env#init_container}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84fb29c4feae7e74f8bcb996478135d2e34b1cd2ccc4d254b97c73edab3e25b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EnvConfig(
            api_version=api_version,
            env=env,
            kind=kind,
            metadata=metadata,
            container=container,
            field_manager=field_manager,
            force=force,
            id=id,
            init_container=init_container,
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
        '''Generates CDKTF code for importing a Env resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Env to import.
        :param import_from_id: The id of the existing Env that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Env to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8985b36cc91d6ef09cc99ee44358152a4f27d678e63cdc0d1f24257b5d7ecf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9fdbdad0b48f604a93285fae29b81f91fd1baefc4c8032c6387696f26a79ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        name: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param namespace: The namespace of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#namespace Env#namespace}
        '''
        value = EnvMetadata(name=name, namespace=namespace)

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetFieldManager")
    def reset_field_manager(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldManager", []))

    @jsii.member(jsii_name="resetForce")
    def reset_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForce", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitContainer")
    def reset_init_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitContainer", []))

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
    @jsii.member(jsii_name="env")
    def env(self) -> "EnvEnvList":
        return typing.cast("EnvEnvList", jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "EnvMetadataOutputReference":
        return typing.cast("EnvMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnvEnv"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnvEnv"]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldManagerInput")
    def field_manager_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldManagerInput"))

    @builtins.property
    @jsii.member(jsii_name="forceInput")
    def force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initContainerInput")
    def init_container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["EnvMetadata"]:
        return typing.cast(typing.Optional["EnvMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c811333683417017b013fddd8af3433f77b250909a82fae1a488a7b1cafbb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0fd74e6d50018323e7b1f76f0b736c22c3855c04029564bc3f148675de1f1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldManager")
    def field_manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldManager"))

    @field_manager.setter
    def field_manager(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19ee4b6ad65e8bbe38a01275e51ab98527b8aceae0177ef6103098e3d7fbb0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldManager", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="force")
    def force(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "force"))

    @force.setter
    def force(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176bb5a47cf4e96834f1fddf95ff8c650984de02fb2c688481610a832559f1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "force", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ca82549fd2883e832ddddc54ed8f732a14844ba1adb43c4182e55ad0f77f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initContainer")
    def init_container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initContainer"))

    @init_container.setter
    def init_container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65084d54f541acb74fedde0217e150a09f02ee068e1c18df150e7759f8b57bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initContainer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2086ce3da64781b5a1c284031f2bbb2a0fbb91f157ce8455c65da33298ce87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_version": "apiVersion",
        "env": "env",
        "kind": "kind",
        "metadata": "metadata",
        "container": "container",
        "field_manager": "fieldManager",
        "force": "force",
        "id": "id",
        "init_container": "initContainer",
    },
)
class EnvConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_version: builtins.str,
        env: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[builtins.str, typing.Any]]]],
        kind: builtins.str,
        metadata: typing.Union["EnvMetadata", typing.Dict[builtins.str, typing.Any]],
        container: typing.Optional[builtins.str] = None,
        field_manager: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        init_container: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_version: Resource API version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#api_version Env#api_version}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#env Env#env}
        :param kind: Resource Kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#kind Env#kind}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#metadata Env#metadata}
        :param container: Name of the container for which we are updating the environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#container Env#container}
        :param field_manager: Set the name of the field manager for the specified environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_manager Env#field_manager}
        :param force: Force overwriting environments that were created or edited outside of Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#force Env#force}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#id Env#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param init_container: Name of the initContainer for which we are updating the environment variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#init_container Env#init_container}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = EnvMetadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a067aa3d45412cb1c24f892961e2a581fd0a09361d1110b783493b63a90d2a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument field_manager", value=field_manager, expected_type=type_hints["field_manager"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument init_container", value=init_container, expected_type=type_hints["init_container"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_version": api_version,
            "env": env,
            "kind": kind,
            "metadata": metadata,
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
        if container is not None:
            self._values["container"] = container
        if field_manager is not None:
            self._values["field_manager"] = field_manager
        if force is not None:
            self._values["force"] = force
        if id is not None:
            self._values["id"] = id
        if init_container is not None:
            self._values["init_container"] = init_container

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
    def api_version(self) -> builtins.str:
        '''Resource API version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#api_version Env#api_version}
        '''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def env(self) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnvEnv"]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#env Env#env}
        '''
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnvEnv"]], result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Resource Kind.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#kind Env#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> "EnvMetadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#metadata Env#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("EnvMetadata", result)

    @builtins.property
    def container(self) -> typing.Optional[builtins.str]:
        '''Name of the container for which we are updating the environment variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#container Env#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_manager(self) -> typing.Optional[builtins.str]:
        '''Set the name of the field manager for the specified environment variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_manager Env#field_manager}
        '''
        result = self._values.get("field_manager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force overwriting environments that were created or edited outside of Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#force Env#force}
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#id Env#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def init_container(self) -> typing.Optional[builtins.str]:
        '''Name of the initContainer for which we are updating the environment variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#init_container Env#init_container}
        '''
        result = self._values.get("init_container")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_from": "valueFrom"},
)
class EnvEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
        value_from: typing.Optional[typing.Union["EnvEnvValueFrom", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a C_IDENTIFIER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param value: Variable references $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#value Env#value}
        :param value_from: value_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#value_from Env#value_from}
        '''
        if isinstance(value_from, dict):
            value_from = EnvEnvValueFrom(**value_from)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6066256787dada6652b6fc185ca19a525378c3b5d0007830b7dfc53e08d59622)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument value_from", value=value_from, expected_type=type_hints["value_from"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value
        if value_from is not None:
            self._values["value_from"] = value_from

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the environment variable. Must be a C_IDENTIFIER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Variable references $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables.

        If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#value Env#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_from(self) -> typing.Optional["EnvEnvValueFrom"]:
        '''value_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#value_from Env#value_from}
        '''
        result = self._values.get("value_from")
        return typing.cast(typing.Optional["EnvEnvValueFrom"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__262d5fc70f67681181e28733fb6972bd8608dd78e0711888d5e2fb773a174875)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EnvEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735c41e94983468a114e518a85335cc54d3798a4e4ee019cbe0a7ad52058edf4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EnvEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1ca581887eb58436a15ba039777397c5e33c16e7865dbe15f830a294d1454e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85ebc1c4dfc86438fe01e70c5e30cbab3b03b2004d6983c730643013ca30bc85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f377b5ff4092948c3ec4e5e6b187d5338ad0ff456202a5b37e6880c2f77fdb57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ee7df2f6f9903ee144059dbab374a1a1fe9eb6b82a3f430a57dc20b8ac4255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EnvEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a3458d02532960c19c09339a4d2abf6b6dfe87986c0cbf94cfbafc12658cdee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueFrom")
    def put_value_from(
        self,
        *,
        config_map_key_ref: typing.Optional[typing.Union["EnvEnvValueFromConfigMapKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
        field_ref: typing.Optional[typing.Union["EnvEnvValueFromFieldRef", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_field_ref: typing.Optional[typing.Union["EnvEnvValueFromResourceFieldRef", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_key_ref: typing.Optional[typing.Union["EnvEnvValueFromSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_map_key_ref: config_map_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#config_map_key_ref Env#config_map_key_ref}
        :param field_ref: field_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_ref Env#field_ref}
        :param resource_field_ref: resource_field_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#resource_field_ref Env#resource_field_ref}
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#secret_key_ref Env#secret_key_ref}
        '''
        value = EnvEnvValueFrom(
            config_map_key_ref=config_map_key_ref,
            field_ref=field_ref,
            resource_field_ref=resource_field_ref,
            secret_key_ref=secret_key_ref,
        )

        return typing.cast(None, jsii.invoke(self, "putValueFrom", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValueFrom")
    def reset_value_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueFrom", []))

    @builtins.property
    @jsii.member(jsii_name="valueFrom")
    def value_from(self) -> "EnvEnvValueFromOutputReference":
        return typing.cast("EnvEnvValueFromOutputReference", jsii.get(self, "valueFrom"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueFromInput")
    def value_from_input(self) -> typing.Optional["EnvEnvValueFrom"]:
        return typing.cast(typing.Optional["EnvEnvValueFrom"], jsii.get(self, "valueFromInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e186693ca2ad1786721d530ae001d321bff0f707be6ea9cb798968296515cd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62200fb9237c8bb86fb1b925b51fb61d43da6ae88c82c45ecbc6e341710c538a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78d7c04ece400c44458c4d52f276722bee64297144876274d1897e65ac72ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFrom",
    jsii_struct_bases=[],
    name_mapping={
        "config_map_key_ref": "configMapKeyRef",
        "field_ref": "fieldRef",
        "resource_field_ref": "resourceFieldRef",
        "secret_key_ref": "secretKeyRef",
    },
)
class EnvEnvValueFrom:
    def __init__(
        self,
        *,
        config_map_key_ref: typing.Optional[typing.Union["EnvEnvValueFromConfigMapKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
        field_ref: typing.Optional[typing.Union["EnvEnvValueFromFieldRef", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_field_ref: typing.Optional[typing.Union["EnvEnvValueFromResourceFieldRef", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_key_ref: typing.Optional[typing.Union["EnvEnvValueFromSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_map_key_ref: config_map_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#config_map_key_ref Env#config_map_key_ref}
        :param field_ref: field_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_ref Env#field_ref}
        :param resource_field_ref: resource_field_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#resource_field_ref Env#resource_field_ref}
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#secret_key_ref Env#secret_key_ref}
        '''
        if isinstance(config_map_key_ref, dict):
            config_map_key_ref = EnvEnvValueFromConfigMapKeyRef(**config_map_key_ref)
        if isinstance(field_ref, dict):
            field_ref = EnvEnvValueFromFieldRef(**field_ref)
        if isinstance(resource_field_ref, dict):
            resource_field_ref = EnvEnvValueFromResourceFieldRef(**resource_field_ref)
        if isinstance(secret_key_ref, dict):
            secret_key_ref = EnvEnvValueFromSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2a1de59bf316db79fbb35b7013c6e2914c5154003fd3585c8cc06fb07f408f)
            check_type(argname="argument config_map_key_ref", value=config_map_key_ref, expected_type=type_hints["config_map_key_ref"])
            check_type(argname="argument field_ref", value=field_ref, expected_type=type_hints["field_ref"])
            check_type(argname="argument resource_field_ref", value=resource_field_ref, expected_type=type_hints["resource_field_ref"])
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map_key_ref is not None:
            self._values["config_map_key_ref"] = config_map_key_ref
        if field_ref is not None:
            self._values["field_ref"] = field_ref
        if resource_field_ref is not None:
            self._values["resource_field_ref"] = resource_field_ref
        if secret_key_ref is not None:
            self._values["secret_key_ref"] = secret_key_ref

    @builtins.property
    def config_map_key_ref(self) -> typing.Optional["EnvEnvValueFromConfigMapKeyRef"]:
        '''config_map_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#config_map_key_ref Env#config_map_key_ref}
        '''
        result = self._values.get("config_map_key_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromConfigMapKeyRef"], result)

    @builtins.property
    def field_ref(self) -> typing.Optional["EnvEnvValueFromFieldRef"]:
        '''field_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_ref Env#field_ref}
        '''
        result = self._values.get("field_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromFieldRef"], result)

    @builtins.property
    def resource_field_ref(self) -> typing.Optional["EnvEnvValueFromResourceFieldRef"]:
        '''resource_field_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#resource_field_ref Env#resource_field_ref}
        '''
        result = self._values.get("resource_field_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromResourceFieldRef"], result)

    @builtins.property
    def secret_key_ref(self) -> typing.Optional["EnvEnvValueFromSecretKeyRef"]:
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#secret_key_ref Env#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromSecretKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromConfigMapKeyRef",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class EnvEnvValueFromConfigMapKeyRef:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key to select. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#key Env#key}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param optional: Specify whether the ConfigMap or its key must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#optional Env#optional}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2913bc3988e9f89143e0c717c35781273d3f6a3e97e2a201fe41942e3e322f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The key to select.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#key Env#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify whether the ConfigMap or its key must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#optional Env#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromConfigMapKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromConfigMapKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromConfigMapKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8e8d0a9bcfd496f351b150e1474f4a16e5086df51105dd18e0d9af1565e8fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346ad575b673dd67e336256374512493afd647e18f22cef1465ec9cbf4547ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589d58a0d31300780143497736097be30f993380ea27101f689b7b95294fb41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83437f6633739326fb34ce783e4df2fc24734ed5035269a391d696da176bc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromConfigMapKeyRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromConfigMapKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnvEnvValueFromConfigMapKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c4b785a112a1aa617e0ef9e1ec2d7c725db9034505e4bf17a504c75d978249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromFieldRef",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "field_path": "fieldPath"},
)
class EnvEnvValueFromFieldRef:
    def __init__(
        self,
        *,
        api_version: typing.Optional[builtins.str] = None,
        field_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_version: Version of the schema the FieldPath is written in terms of, defaults to "v1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#api_version Env#api_version}
        :param field_path: Path of the field to select in the specified API version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_path Env#field_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bfae8c0bcf201912dc61fc7baaf215957a99d83b8bab5653a94f23ee6dffaa)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument field_path", value=field_path, expected_type=type_hints["field_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_version is not None:
            self._values["api_version"] = api_version
        if field_path is not None:
            self._values["field_path"] = field_path

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Version of the schema the FieldPath is written in terms of, defaults to "v1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#api_version Env#api_version}
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_path(self) -> typing.Optional[builtins.str]:
        '''Path of the field to select in the specified API version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_path Env#field_path}
        '''
        result = self._values.get("field_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromFieldRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromFieldRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromFieldRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0316cfeb69c68c927775733b6eb29de0692c3536b1f621c23cc5ebd4bf9d553e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetFieldPath")
    def reset_field_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldPath", []))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldPathInput")
    def field_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldPathInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1790518855f7c5b0bc395e27c372681868960867541f6ced87958e8f3c7670ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldPath")
    def field_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldPath"))

    @field_path.setter
    def field_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5379cbb8f95ebf878fa0761ac5a5d4b1baf807fbbe6dfb0ef789ef42fdf868c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromFieldRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromFieldRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EnvEnvValueFromFieldRef]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49349b3533d564e1476856767f74218aedf84d6198944a5a436f753d27b74f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EnvEnvValueFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b17b34b7e964d1f2d0909b2bcf6dd6f8e811ca31713a31a14070921198c31e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigMapKeyRef")
    def put_config_map_key_ref(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key to select. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#key Env#key}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param optional: Specify whether the ConfigMap or its key must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#optional Env#optional}
        '''
        value = EnvEnvValueFromConfigMapKeyRef(key=key, name=name, optional=optional)

        return typing.cast(None, jsii.invoke(self, "putConfigMapKeyRef", [value]))

    @jsii.member(jsii_name="putFieldRef")
    def put_field_ref(
        self,
        *,
        api_version: typing.Optional[builtins.str] = None,
        field_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_version: Version of the schema the FieldPath is written in terms of, defaults to "v1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#api_version Env#api_version}
        :param field_path: Path of the field to select in the specified API version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#field_path Env#field_path}
        '''
        value = EnvEnvValueFromFieldRef(api_version=api_version, field_path=field_path)

        return typing.cast(None, jsii.invoke(self, "putFieldRef", [value]))

    @jsii.member(jsii_name="putResourceFieldRef")
    def put_resource_field_ref(
        self,
        *,
        resource: builtins.str,
        container_name: typing.Optional[builtins.str] = None,
        divisor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource: Resource to select. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#resource Env#resource}
        :param container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#container_name Env#container_name}.
        :param divisor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#divisor Env#divisor}.
        '''
        value = EnvEnvValueFromResourceFieldRef(
            resource=resource, container_name=container_name, divisor=divisor
        )

        return typing.cast(None, jsii.invoke(self, "putResourceFieldRef", [value]))

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key of the secret to select from. Must be a valid secret key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#key Env#key}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param optional: Specify whether the Secret or its key must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#optional Env#optional}
        '''
        value = EnvEnvValueFromSecretKeyRef(key=key, name=name, optional=optional)

        return typing.cast(None, jsii.invoke(self, "putSecretKeyRef", [value]))

    @jsii.member(jsii_name="resetConfigMapKeyRef")
    def reset_config_map_key_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigMapKeyRef", []))

    @jsii.member(jsii_name="resetFieldRef")
    def reset_field_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldRef", []))

    @jsii.member(jsii_name="resetResourceFieldRef")
    def reset_resource_field_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceFieldRef", []))

    @jsii.member(jsii_name="resetSecretKeyRef")
    def reset_secret_key_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKeyRef", []))

    @builtins.property
    @jsii.member(jsii_name="configMapKeyRef")
    def config_map_key_ref(self) -> EnvEnvValueFromConfigMapKeyRefOutputReference:
        return typing.cast(EnvEnvValueFromConfigMapKeyRefOutputReference, jsii.get(self, "configMapKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="fieldRef")
    def field_ref(self) -> EnvEnvValueFromFieldRefOutputReference:
        return typing.cast(EnvEnvValueFromFieldRefOutputReference, jsii.get(self, "fieldRef"))

    @builtins.property
    @jsii.member(jsii_name="resourceFieldRef")
    def resource_field_ref(self) -> "EnvEnvValueFromResourceFieldRefOutputReference":
        return typing.cast("EnvEnvValueFromResourceFieldRefOutputReference", jsii.get(self, "resourceFieldRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRef")
    def secret_key_ref(self) -> "EnvEnvValueFromSecretKeyRefOutputReference":
        return typing.cast("EnvEnvValueFromSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="configMapKeyRefInput")
    def config_map_key_ref_input(
        self,
    ) -> typing.Optional[EnvEnvValueFromConfigMapKeyRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromConfigMapKeyRef], jsii.get(self, "configMapKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldRefInput")
    def field_ref_input(self) -> typing.Optional[EnvEnvValueFromFieldRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromFieldRef], jsii.get(self, "fieldRefInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceFieldRefInput")
    def resource_field_ref_input(
        self,
    ) -> typing.Optional["EnvEnvValueFromResourceFieldRef"]:
        return typing.cast(typing.Optional["EnvEnvValueFromResourceFieldRef"], jsii.get(self, "resourceFieldRefInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(self) -> typing.Optional["EnvEnvValueFromSecretKeyRef"]:
        return typing.cast(typing.Optional["EnvEnvValueFromSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFrom]:
        return typing.cast(typing.Optional[EnvEnvValueFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EnvEnvValueFrom]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ead5e21d528b750c80801d639bc3b332a2f4a82e9a5cfef95b337d9d665617b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromResourceFieldRef",
    jsii_struct_bases=[],
    name_mapping={
        "resource": "resource",
        "container_name": "containerName",
        "divisor": "divisor",
    },
)
class EnvEnvValueFromResourceFieldRef:
    def __init__(
        self,
        *,
        resource: builtins.str,
        container_name: typing.Optional[builtins.str] = None,
        divisor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource: Resource to select. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#resource Env#resource}
        :param container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#container_name Env#container_name}.
        :param divisor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#divisor Env#divisor}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9b011eb9327c2c65eb9d79628c9719812d05391866371bfcad1b69ce8b8f08)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument divisor", value=divisor, expected_type=type_hints["divisor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
        }
        if container_name is not None:
            self._values["container_name"] = container_name
        if divisor is not None:
            self._values["divisor"] = divisor

    @builtins.property
    def resource(self) -> builtins.str:
        '''Resource to select.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#resource Env#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#container_name Env#container_name}.'''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def divisor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#divisor Env#divisor}.'''
        result = self._values.get("divisor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromResourceFieldRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromResourceFieldRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromResourceFieldRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfe52768cc5333df69640798a170ce7ecf8ba8054b92ce77eb7c3a1558e8642f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerName")
    def reset_container_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerName", []))

    @jsii.member(jsii_name="resetDivisor")
    def reset_divisor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDivisor", []))

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="divisorInput")
    def divisor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "divisorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73fc5b4dacb21207b54dd414de0570038aad18d7074f151714efd5fd74a98d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="divisor")
    def divisor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "divisor"))

    @divisor.setter
    def divisor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c59b2008d0b84d82c5dc65f29d3fd852553061d0b3f89f5ca9b735a15469c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "divisor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a6fe312d5f7fb840adb0f2e5ed4c5854b21f6508308eb922398e7547dd1c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromResourceFieldRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromResourceFieldRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnvEnvValueFromResourceFieldRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04603edfc413309cc20303bb39c9ffe01fe88f5f80b2e2054ffcc49e539f2f8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class EnvEnvValueFromSecretKeyRef:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key of the secret to select from. Must be a valid secret key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#key Env#key}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param optional: Specify whether the Secret or its key must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#optional Env#optional}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67deec769f4a4fd53d7132b5e53fef1b3915d1a15fc41338b0d8052b075a1e12)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The key of the secret to select from. Must be a valid secret key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#key Env#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify whether the Secret or its key must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#optional Env#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvEnvValueFromSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1f5a4a3bf510296a15abbabaadafb6d8101366eb71e210ea0cacb66170d712)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e7c092a4551d52e5c2767e4f9970283c5d7cd494aa75e471d49f74d608fa14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23e187d1fe1148a79ef7a428817a7a12a3dedf85d115929240d55a2dc88d86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b139b43e6ab01ed097041733fc5ac69d342bfe95bbf7bcd137022ce1615038be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromSecretKeyRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnvEnvValueFromSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98982e9d9369d428fa50c4cc80c65a6019398aa62e1ddb71b5098edf4146b913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.env.EnvMetadata",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class EnvMetadata:
    def __init__(
        self,
        *,
        name: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        :param namespace: The namespace of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#namespace Env#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d280c28c760e4bf99330c80f2c1b1e787b8886209166a935fa11dec834e24353)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#name Env#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/env#namespace Env#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.env.EnvMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cd64552efdef76b4701e561208eb58eb0af3cc4b7400057572d14d4f36bd401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773ccf3118daa3eef48e8d40a7cdd0d3d1c618b0cabef036bad040fc5a6c1415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b6d5a7ecaccb8ca6520a467fa55494433b8c8ce1bc1b7071e073b9301b3c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvMetadata]:
        return typing.cast(typing.Optional[EnvMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EnvMetadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405539b281f10539ee3066fcd4e25fd43d3af3f3548975bc8ac928cf993bf91c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Env",
    "EnvConfig",
    "EnvEnv",
    "EnvEnvList",
    "EnvEnvOutputReference",
    "EnvEnvValueFrom",
    "EnvEnvValueFromConfigMapKeyRef",
    "EnvEnvValueFromConfigMapKeyRefOutputReference",
    "EnvEnvValueFromFieldRef",
    "EnvEnvValueFromFieldRefOutputReference",
    "EnvEnvValueFromOutputReference",
    "EnvEnvValueFromResourceFieldRef",
    "EnvEnvValueFromResourceFieldRefOutputReference",
    "EnvEnvValueFromSecretKeyRef",
    "EnvEnvValueFromSecretKeyRefOutputReference",
    "EnvMetadata",
    "EnvMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__c84fb29c4feae7e74f8bcb996478135d2e34b1cd2ccc4d254b97c73edab3e25b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_version: builtins.str,
    env: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvEnv, typing.Dict[builtins.str, typing.Any]]]],
    kind: builtins.str,
    metadata: typing.Union[EnvMetadata, typing.Dict[builtins.str, typing.Any]],
    container: typing.Optional[builtins.str] = None,
    field_manager: typing.Optional[builtins.str] = None,
    force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    init_container: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4b8985b36cc91d6ef09cc99ee44358152a4f27d678e63cdc0d1f24257b5d7ecf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9fdbdad0b48f604a93285fae29b81f91fd1baefc4c8032c6387696f26a79ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c811333683417017b013fddd8af3433f77b250909a82fae1a488a7b1cafbb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0fd74e6d50018323e7b1f76f0b736c22c3855c04029564bc3f148675de1f1c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19ee4b6ad65e8bbe38a01275e51ab98527b8aceae0177ef6103098e3d7fbb0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176bb5a47cf4e96834f1fddf95ff8c650984de02fb2c688481610a832559f1d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ca82549fd2883e832ddddc54ed8f732a14844ba1adb43c4182e55ad0f77f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65084d54f541acb74fedde0217e150a09f02ee068e1c18df150e7759f8b57bf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2086ce3da64781b5a1c284031f2bbb2a0fbb91f157ce8455c65da33298ce87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a067aa3d45412cb1c24f892961e2a581fd0a09361d1110b783493b63a90d2a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_version: builtins.str,
    env: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvEnv, typing.Dict[builtins.str, typing.Any]]]],
    kind: builtins.str,
    metadata: typing.Union[EnvMetadata, typing.Dict[builtins.str, typing.Any]],
    container: typing.Optional[builtins.str] = None,
    field_manager: typing.Optional[builtins.str] = None,
    force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    init_container: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6066256787dada6652b6fc185ca19a525378c3b5d0007830b7dfc53e08d59622(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
    value_from: typing.Optional[typing.Union[EnvEnvValueFrom, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262d5fc70f67681181e28733fb6972bd8608dd78e0711888d5e2fb773a174875(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735c41e94983468a114e518a85335cc54d3798a4e4ee019cbe0a7ad52058edf4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1ca581887eb58436a15ba039777397c5e33c16e7865dbe15f830a294d1454e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ebc1c4dfc86438fe01e70c5e30cbab3b03b2004d6983c730643013ca30bc85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f377b5ff4092948c3ec4e5e6b187d5338ad0ff456202a5b37e6880c2f77fdb57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ee7df2f6f9903ee144059dbab374a1a1fe9eb6b82a3f430a57dc20b8ac4255(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3458d02532960c19c09339a4d2abf6b6dfe87986c0cbf94cfbafc12658cdee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e186693ca2ad1786721d530ae001d321bff0f707be6ea9cb798968296515cd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62200fb9237c8bb86fb1b925b51fb61d43da6ae88c82c45ecbc6e341710c538a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78d7c04ece400c44458c4d52f276722bee64297144876274d1897e65ac72ab8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2a1de59bf316db79fbb35b7013c6e2914c5154003fd3585c8cc06fb07f408f(
    *,
    config_map_key_ref: typing.Optional[typing.Union[EnvEnvValueFromConfigMapKeyRef, typing.Dict[builtins.str, typing.Any]]] = None,
    field_ref: typing.Optional[typing.Union[EnvEnvValueFromFieldRef, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_field_ref: typing.Optional[typing.Union[EnvEnvValueFromResourceFieldRef, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_key_ref: typing.Optional[typing.Union[EnvEnvValueFromSecretKeyRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2913bc3988e9f89143e0c717c35781273d3f6a3e97e2a201fe41942e3e322f(
    *,
    key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8e8d0a9bcfd496f351b150e1474f4a16e5086df51105dd18e0d9af1565e8fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346ad575b673dd67e336256374512493afd647e18f22cef1465ec9cbf4547ff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589d58a0d31300780143497736097be30f993380ea27101f689b7b95294fb41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83437f6633739326fb34ce783e4df2fc24734ed5035269a391d696da176bc82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c4b785a112a1aa617e0ef9e1ec2d7c725db9034505e4bf17a504c75d978249(
    value: typing.Optional[EnvEnvValueFromConfigMapKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bfae8c0bcf201912dc61fc7baaf215957a99d83b8bab5653a94f23ee6dffaa(
    *,
    api_version: typing.Optional[builtins.str] = None,
    field_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0316cfeb69c68c927775733b6eb29de0692c3536b1f621c23cc5ebd4bf9d553e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1790518855f7c5b0bc395e27c372681868960867541f6ced87958e8f3c7670ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5379cbb8f95ebf878fa0761ac5a5d4b1baf807fbbe6dfb0ef789ef42fdf868c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49349b3533d564e1476856767f74218aedf84d6198944a5a436f753d27b74f85(
    value: typing.Optional[EnvEnvValueFromFieldRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b17b34b7e964d1f2d0909b2bcf6dd6f8e811ca31713a31a14070921198c31e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ead5e21d528b750c80801d639bc3b332a2f4a82e9a5cfef95b337d9d665617b(
    value: typing.Optional[EnvEnvValueFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9b011eb9327c2c65eb9d79628c9719812d05391866371bfcad1b69ce8b8f08(
    *,
    resource: builtins.str,
    container_name: typing.Optional[builtins.str] = None,
    divisor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe52768cc5333df69640798a170ce7ecf8ba8054b92ce77eb7c3a1558e8642f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73fc5b4dacb21207b54dd414de0570038aad18d7074f151714efd5fd74a98d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c59b2008d0b84d82c5dc65f29d3fd852553061d0b3f89f5ca9b735a15469c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a6fe312d5f7fb840adb0f2e5ed4c5854b21f6508308eb922398e7547dd1c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04603edfc413309cc20303bb39c9ffe01fe88f5f80b2e2054ffcc49e539f2f8f(
    value: typing.Optional[EnvEnvValueFromResourceFieldRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67deec769f4a4fd53d7132b5e53fef1b3915d1a15fc41338b0d8052b075a1e12(
    *,
    key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1f5a4a3bf510296a15abbabaadafb6d8101366eb71e210ea0cacb66170d712(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e7c092a4551d52e5c2767e4f9970283c5d7cd494aa75e471d49f74d608fa14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23e187d1fe1148a79ef7a428817a7a12a3dedf85d115929240d55a2dc88d86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b139b43e6ab01ed097041733fc5ac69d342bfe95bbf7bcd137022ce1615038be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98982e9d9369d428fa50c4cc80c65a6019398aa62e1ddb71b5098edf4146b913(
    value: typing.Optional[EnvEnvValueFromSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d280c28c760e4bf99330c80f2c1b1e787b8886209166a935fa11dec834e24353(
    *,
    name: builtins.str,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd64552efdef76b4701e561208eb58eb0af3cc4b7400057572d14d4f36bd401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773ccf3118daa3eef48e8d40a7cdd0d3d1c618b0cabef036bad040fc5a6c1415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b6d5a7ecaccb8ca6520a467fa55494433b8c8ce1bc1b7071e073b9301b3c42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405539b281f10539ee3066fcd4e25fd43d3af3f3548975bc8ac928cf993bf91c(
    value: typing.Optional[EnvMetadata],
) -> None:
    """Type checking stubs"""
    pass
