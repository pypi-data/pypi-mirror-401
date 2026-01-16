r'''
# `data_kubernetes_persistent_volume_v1`

Refer to the Terraform Registry for docs: [`data_kubernetes_persistent_volume_v1`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1).
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


class DataKubernetesPersistentVolumeV1(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1 kubernetes_persistent_volume_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["DataKubernetesPersistentVolumeV1Metadata", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1Spec", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1 kubernetes_persistent_volume_v1} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#metadata DataKubernetesPersistentVolumeV1#metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#id DataKubernetesPersistentVolumeV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#spec DataKubernetesPersistentVolumeV1#spec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9ffaf6cb94dce91e6459fcbba68ba3d5f7cb5d565e378d4ccf2116f33e49a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataKubernetesPersistentVolumeV1Config(
            metadata=metadata,
            id=id,
            spec=spec,
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
        '''Generates CDKTF code for importing a DataKubernetesPersistentVolumeV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataKubernetesPersistentVolumeV1 to import.
        :param import_from_id: The id of the existing DataKubernetesPersistentVolumeV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataKubernetesPersistentVolumeV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1545bd34be77b630804ae9731919ef969728efaa37466e9734907d41356486f5)
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
        :param annotations: An unstructured key value map stored with the persistent volume that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#annotations DataKubernetesPersistentVolumeV1#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the persistent volume. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#labels DataKubernetesPersistentVolumeV1#labels}
        :param name: Name of the persistent volume, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        value = DataKubernetesPersistentVolumeV1Metadata(
            annotations=annotations, labels=labels, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1Spec", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1725a422ef86afb5301d76e51007a3ba6e36b45ededf99d83a57198f94c43840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

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
    def metadata(self) -> "DataKubernetesPersistentVolumeV1MetadataOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "DataKubernetesPersistentVolumeV1SpecList":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecList", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1Metadata"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1Spec"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1Spec"]]], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6483c21e2760d3269825500f39cd0b3477e7a8a762d00736ae77a65332ba7cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1Config",
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
        "id": "id",
        "spec": "spec",
    },
)
class DataKubernetesPersistentVolumeV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["DataKubernetesPersistentVolumeV1Metadata", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1Spec", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#metadata DataKubernetesPersistentVolumeV1#metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#id DataKubernetesPersistentVolumeV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#spec DataKubernetesPersistentVolumeV1#spec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = DataKubernetesPersistentVolumeV1Metadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b201aff73105553daeef85d16c39b40f44eb9508bf652eab540a9fc332d10c28)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if id is not None:
            self._values["id"] = id
        if spec is not None:
            self._values["spec"] = spec

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
    def metadata(self) -> "DataKubernetesPersistentVolumeV1Metadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#metadata DataKubernetesPersistentVolumeV1#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("DataKubernetesPersistentVolumeV1Metadata", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#id DataKubernetesPersistentVolumeV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1Spec"]]]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#spec DataKubernetesPersistentVolumeV1#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1Spec"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1Metadata",
    jsii_struct_bases=[],
    name_mapping={"annotations": "annotations", "labels": "labels", "name": "name"},
)
class DataKubernetesPersistentVolumeV1Metadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the persistent volume that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#annotations DataKubernetesPersistentVolumeV1#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the persistent volume. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#labels DataKubernetesPersistentVolumeV1#labels}
        :param name: Name of the persistent volume, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a34e5b63d39d3bedd73559d9d4936156123fef99042a05acc76afa464dfc21b)
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
        '''An unstructured key value map stored with the persistent volume that may be used to store arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#annotations DataKubernetesPersistentVolumeV1#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the persistent volume.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#labels DataKubernetesPersistentVolumeV1#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the persistent volume, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed075b8191e8388fd399eafeb4f69c919b8724d768574f7442397b8a9511795)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f95016b039c12d1f51aa71a6dc454ec49921f96b7296e8a0b2f06de9e8c009e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168d7cdd09c238ebfac189fc572bfbe14d8dc7bb5413cb92c9876a21ecadf4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53951c75a7c18aa19aaf15b7fd9d6956468ffea84a07158137aaea4fce7b496c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1Metadata]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1Metadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71bacf809bb13bf8e466c45ad175c09e1e7606d4c5bdc9314b00e17c4429800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1Spec",
    jsii_struct_bases=[],
    name_mapping={
        "access_modes": "accessModes",
        "capacity": "capacity",
        "persistent_volume_source": "persistentVolumeSource",
        "claim_ref": "claimRef",
        "mount_options": "mountOptions",
        "node_affinity": "nodeAffinity",
        "persistent_volume_reclaim_policy": "persistentVolumeReclaimPolicy",
        "storage_class_name": "storageClassName",
        "volume_mode": "volumeMode",
    },
)
class DataKubernetesPersistentVolumeV1Spec:
    def __init__(
        self,
        *,
        access_modes: typing.Sequence[builtins.str],
        capacity: typing.Mapping[builtins.str, builtins.str],
        persistent_volume_source: typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource", typing.Dict[builtins.str, typing.Any]],
        claim_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecClaimRef", typing.Dict[builtins.str, typing.Any]]] = None,
        mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        node_affinity: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecNodeAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        persistent_volume_reclaim_policy: typing.Optional[builtins.str] = None,
        storage_class_name: typing.Optional[builtins.str] = None,
        volume_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_modes: Contains all ways the volume can be mounted. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#access_modes DataKubernetesPersistentVolumeV1#access_modes}
        :param capacity: A description of the persistent volume's resources and capacity. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#capacity DataKubernetesPersistentVolumeV1#capacity}
        :param persistent_volume_source: persistent_volume_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#persistent_volume_source DataKubernetesPersistentVolumeV1#persistent_volume_source}
        :param claim_ref: claim_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#claim_ref DataKubernetesPersistentVolumeV1#claim_ref}
        :param mount_options: A list of mount options, e.g. ["ro", "soft"]. Not validated - mount will simply fail if one is invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#mount_options DataKubernetesPersistentVolumeV1#mount_options}
        :param node_affinity: node_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_affinity DataKubernetesPersistentVolumeV1#node_affinity}
        :param persistent_volume_reclaim_policy: What happens to a persistent volume when released from its claim. Valid options are Retain (default) and Recycle. Recycling must be supported by the volume plugin underlying this persistent volume. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#reclaiming Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#persistent_volume_reclaim_policy DataKubernetesPersistentVolumeV1#persistent_volume_reclaim_policy}
        :param storage_class_name: A description of the persistent volume's class. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#storage_class_name DataKubernetesPersistentVolumeV1#storage_class_name}
        :param volume_mode: Defines if a volume is intended to be used with a formatted filesystem. or to remain in raw block state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_mode DataKubernetesPersistentVolumeV1#volume_mode}
        '''
        if isinstance(persistent_volume_source, dict):
            persistent_volume_source = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource(**persistent_volume_source)
        if isinstance(claim_ref, dict):
            claim_ref = DataKubernetesPersistentVolumeV1SpecClaimRef(**claim_ref)
        if isinstance(node_affinity, dict):
            node_affinity = DataKubernetesPersistentVolumeV1SpecNodeAffinity(**node_affinity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f9741d4180b052d476cc5a4fb76d434d76a261a85f89912ecbdcd12eb50517)
            check_type(argname="argument access_modes", value=access_modes, expected_type=type_hints["access_modes"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument persistent_volume_source", value=persistent_volume_source, expected_type=type_hints["persistent_volume_source"])
            check_type(argname="argument claim_ref", value=claim_ref, expected_type=type_hints["claim_ref"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument node_affinity", value=node_affinity, expected_type=type_hints["node_affinity"])
            check_type(argname="argument persistent_volume_reclaim_policy", value=persistent_volume_reclaim_policy, expected_type=type_hints["persistent_volume_reclaim_policy"])
            check_type(argname="argument storage_class_name", value=storage_class_name, expected_type=type_hints["storage_class_name"])
            check_type(argname="argument volume_mode", value=volume_mode, expected_type=type_hints["volume_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_modes": access_modes,
            "capacity": capacity,
            "persistent_volume_source": persistent_volume_source,
        }
        if claim_ref is not None:
            self._values["claim_ref"] = claim_ref
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if node_affinity is not None:
            self._values["node_affinity"] = node_affinity
        if persistent_volume_reclaim_policy is not None:
            self._values["persistent_volume_reclaim_policy"] = persistent_volume_reclaim_policy
        if storage_class_name is not None:
            self._values["storage_class_name"] = storage_class_name
        if volume_mode is not None:
            self._values["volume_mode"] = volume_mode

    @builtins.property
    def access_modes(self) -> typing.List[builtins.str]:
        '''Contains all ways the volume can be mounted. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#access_modes DataKubernetesPersistentVolumeV1#access_modes}
        '''
        result = self._values.get("access_modes")
        assert result is not None, "Required property 'access_modes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def capacity(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''A description of the persistent volume's resources and capacity. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#capacity DataKubernetesPersistentVolumeV1#capacity}
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def persistent_volume_source(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource":
        '''persistent_volume_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#persistent_volume_source DataKubernetesPersistentVolumeV1#persistent_volume_source}
        '''
        result = self._values.get("persistent_volume_source")
        assert result is not None, "Required property 'persistent_volume_source' is missing"
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource", result)

    @builtins.property
    def claim_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecClaimRef"]:
        '''claim_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#claim_ref DataKubernetesPersistentVolumeV1#claim_ref}
        '''
        result = self._values.get("claim_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecClaimRef"], result)

    @builtins.property
    def mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of mount options, e.g. ["ro", "soft"]. Not validated - mount will simply fail if one is invalid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#mount_options DataKubernetesPersistentVolumeV1#mount_options}
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def node_affinity(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecNodeAffinity"]:
        '''node_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_affinity DataKubernetesPersistentVolumeV1#node_affinity}
        '''
        result = self._values.get("node_affinity")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecNodeAffinity"], result)

    @builtins.property
    def persistent_volume_reclaim_policy(self) -> typing.Optional[builtins.str]:
        '''What happens to a persistent volume when released from its claim.

        Valid options are Retain (default) and Recycle. Recycling must be supported by the volume plugin underlying this persistent volume. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#reclaiming

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#persistent_volume_reclaim_policy DataKubernetesPersistentVolumeV1#persistent_volume_reclaim_policy}
        '''
        result = self._values.get("persistent_volume_reclaim_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_class_name(self) -> typing.Optional[builtins.str]:
        '''A description of the persistent volume's class. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#storage_class_name DataKubernetesPersistentVolumeV1#storage_class_name}
        '''
        result = self._values.get("storage_class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_mode(self) -> typing.Optional[builtins.str]:
        '''Defines if a volume is intended to be used with a formatted filesystem.

        or to remain in raw block state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_mode DataKubernetesPersistentVolumeV1#volume_mode}
        '''
        result = self._values.get("volume_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1Spec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecClaimRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecClaimRef:
    def __init__(
        self,
        *,
        name: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the PersistentVolumeClaim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: The namespace of the PersistentVolumeClaim. Uses 'default' namespace if none is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30ea2ab52ed466346c9ae5acd52bf7c5c5ecfc40370ea0623896cef9b68e369)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the PersistentVolumeClaim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the PersistentVolumeClaim. Uses 'default' namespace if none is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecClaimRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecClaimRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecClaimRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57565dec968d139d95bdc509eb108849c118099b20387e2a1eb65567a82692a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2623d708d1a2355c4b01ddb0127fbff7ea74ada28f815e7d014808b54a26369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3541486920026c73bd49688ad968527d2f76eddd5bdbd445845318fa8ea76b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecClaimRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecClaimRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecClaimRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2713f6c2ce4fa4fe183aef98dd298cad2b8c57d9e782c4816d52588be824471c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e64bffde9043c93b58ac9a862855e31988f8d3d5c7a65aa64903ac2063a4b1b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataKubernetesPersistentVolumeV1SpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec77bf34026facb2ddc734629b5b503518e824d04487fa3c0c02e757cd0090c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataKubernetesPersistentVolumeV1SpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad3150bf1180d01ca8783a5db901611621d91cee86f51f40d8f5227f2062d7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a113ed275519eecf684312b0c144f059d2a4f540d318c569b607559ff8af275)
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
            type_hints = typing.get_type_hints(_typecheckingstub__045a509b219d948f16677ee65b1a58963ca4ee09d1dff977b8faeeb77fafb50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1Spec]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1Spec]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1Spec]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a29d7f26db8f6f7d08dd5e0d05a980d50afd8ccb92e37838334158ae5bbdde4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinity",
    jsii_struct_bases=[],
    name_mapping={"required": "required"},
)
class DataKubernetesPersistentVolumeV1SpecNodeAffinity:
    def __init__(
        self,
        *,
        required: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param required: required block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#required DataKubernetesPersistentVolumeV1#required}
        '''
        if isinstance(required, dict):
            required = DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired(**required)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84feb2bd0dd4a0039c3b88fd143c944af37f68b8b5b15fd6e24dcc2eb4afc1bc)
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def required(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired"]:
        '''required block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#required DataKubernetesPersistentVolumeV1#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecNodeAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecNodeAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abbf759135a4cd85c80d93f8ae3a1caf62d3fcb50c6db4893779c9c1644d335a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequired")
    def put_required(
        self,
        *,
        node_selector_term: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param node_selector_term: node_selector_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_selector_term DataKubernetesPersistentVolumeV1#node_selector_term}
        '''
        value = DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired(
            node_selector_term=node_selector_term
        )

        return typing.cast(None, jsii.invoke(self, "putRequired", [value]))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredOutputReference", jsii.get(self, "required"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired"], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinity]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1dc2df57a2a63098b0ac22f052f660531e52a66d1722454c7e71e47df3d1168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired",
    jsii_struct_bases=[],
    name_mapping={"node_selector_term": "nodeSelectorTerm"},
)
class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired:
    def __init__(
        self,
        *,
        node_selector_term: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param node_selector_term: node_selector_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_selector_term DataKubernetesPersistentVolumeV1#node_selector_term}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f2e8e1e9b93047ac9e62c842f016cf62ef317c951b31548c725b5153715209)
            check_type(argname="argument node_selector_term", value=node_selector_term, expected_type=type_hints["node_selector_term"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_selector_term": node_selector_term,
        }

    @builtins.property
    def node_selector_term(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm"]]:
        '''node_selector_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_selector_term DataKubernetesPersistentVolumeV1#node_selector_term}
        '''
        result = self._values.get("node_selector_term")
        assert result is not None, "Required property 'node_selector_term' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_fields": "matchFields",
    },
)
class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#match_expressions DataKubernetesPersistentVolumeV1#match_expressions}
        :param match_fields: match_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#match_fields DataKubernetesPersistentVolumeV1#match_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119915a20c24a51ec3c06e5b8b86d98927bc84005f8df50071ce2897985a9ea0)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_fields", value=match_fields, expected_type=type_hints["match_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_fields is not None:
            self._values["match_fields"] = match_fields

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#match_expressions DataKubernetesPersistentVolumeV1#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions"]]], result)

    @builtins.property
    def match_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields"]]]:
        '''match_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#match_fields DataKubernetesPersistentVolumeV1#match_fields}
        '''
        result = self._values.get("match_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5934052119272406687894391833dc80e9507e453798ff1d112b296f3898e49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7545b6463c29ceb0a104bda4f9b2a0f89f431f2093cd61d72f59be98d96026d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08b1e55d806307e2f8037e41d124865074943aa64b73d14332f9ad0cb0e4380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4406da5391b94ddb17101b42f59af491a05a0db80f76dfd5aa3077ed0eaba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7d81ef7aadf6020454fc0fcfd513b69ca5766cac49ccd0aa0061d8b7bfbd57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f910779aa267549e92521dc6ea6a94b8fe68a71fa6445ea57ca4f724be3454d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#key DataKubernetesPersistentVolumeV1#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists``, ``DoesNotExist``, ``Gt``, and ``Lt``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#operator DataKubernetesPersistentVolumeV1#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#values DataKubernetesPersistentVolumeV1#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba328d9664d34c29b31be02c99f7fe36341b7a12539928440c35e6104225ee1)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "operator": operator,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> builtins.str:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#key DataKubernetesPersistentVolumeV1#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists``, ``DoesNotExist``, ``Gt``, and ``Lt``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#operator DataKubernetesPersistentVolumeV1#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#values DataKubernetesPersistentVolumeV1#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f318299747cc704553383de0e58de86a05f5483e8e516f7fbb01f63a459e0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de49aeb62b0d696d108551288fdac4c15ac6bae88bcf07c293f407e6281848ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef0f213af551aae758e708fd74f99d2f3a49647276bbe79d18cb47f4abfac24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60c5f0e0d01379117a9c91f1c20e396a2689d9526ede41efe6c731131cb2779)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1723c5e87abfc8a1625348af8c6239194b9fda17ac99dc9c618a57de23752c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc266cecfa139bdee5b67356f4e4cb233c82e3e317fb99142af80951306f27b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7db808498ec8cd7fa943aa470e98763556227df80636cf587baeca52ffdc47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a7c0b5e35c9096be00acae829346208c60c0b39330525cb77bf00311c1c59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5f345dd5dd8170bc86be7e589f1e76359acd5b0c95cb244b025be8e36cd9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33508e3025c768a9c32655ab151786fb8af77e051eb8779b796e35c3d0a3ef6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04b878c17446b23a157fda9d3d550b2a8d2eef251a766b6b31b7cf552f012b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#key DataKubernetesPersistentVolumeV1#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists``, ``DoesNotExist``, ``Gt``, and ``Lt``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#operator DataKubernetesPersistentVolumeV1#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#values DataKubernetesPersistentVolumeV1#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cf172f4ab65bd19d48f6b3b8e472401468617d7487196fb49f236eece4682e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "operator": operator,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> builtins.str:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#key DataKubernetesPersistentVolumeV1#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists``, ``DoesNotExist``, ``Gt``, and ``Lt``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#operator DataKubernetesPersistentVolumeV1#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#values DataKubernetesPersistentVolumeV1#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e96360cd543594b732760a3f5cf4f038e07f2c92eabf8e088eb29b181a5e798)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9080a4a5565c9467c32cb6fab1de044999e8b564bde7667b6f56cfe23c00b51f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc8d9efb4bdc06d73760b7433392ab51fe151152bddb71779abe97355ca434d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff691d4fd9c7b8a264b61d002c0f2497670648089c05d4cc69cce05db68dcbac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed866aa9ea02c7371224f53004ed71fb026c60012f41f033f2eccea2bc86b248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b3550aab0e21b8dd89f2f4f8449a486d98ef4ba910d535fa131f999d38aa43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74ea658e20b1a811493ff45f60b64be90253cbdd30e0ec4b8911b9f72227d8cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e3f16c734f54d6b6490a77950c272fdcaa573432072bf0fad5a983613d5e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43317251f8e37fe92cbc141ba3852d5891757976be707e44905e83a4b52a9342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47235d3631baae964168e2039f10475ff7b0457e37f20a0f0fd3bc21c6974ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff64b25e1f7980bdbd064266ad081861bf9a7c5570b062ebff1c7a89e5634f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__085bb2ca3e2b3e53774b50b9ea7df01384b98e0d8ac6a5d4e7195a620e6c3ad8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31a738f54182db9d00a3d4f80a03d7ac5a8b8e2d9ee8e97c129807fa235e9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchExpressions", [value]))

    @jsii.member(jsii_name="putMatchFields")
    def put_match_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca75dc97884bf6f4120f54a1e0803fb95bd7a7b52a8a49111db76e2d3bab723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchFields", [value]))

    @jsii.member(jsii_name="resetMatchExpressions")
    def reset_match_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchExpressions", []))

    @jsii.member(jsii_name="resetMatchFields")
    def reset_match_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchFields", []))

    @builtins.property
    @jsii.member(jsii_name="matchExpressions")
    def match_expressions(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsList:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchFields")
    def match_fields(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsList:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsList, jsii.get(self, "matchFields"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchFieldsInput")
    def match_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]], jsii.get(self, "matchFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99db347dfd0bb9d30ed0d515174471e426dc8b3ab1249fe89f5a7cafd973b77d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cfee2878babfde321371352588ca87610f765303db7812c117a157220a84d67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeSelectorTerm")
    def put_node_selector_term(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851199addd78519421382111ad153d782933bf84f049a29315a9ba4aed8d5f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeSelectorTerm", [value]))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorTerm")
    def node_selector_term(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermList:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermList, jsii.get(self, "nodeSelectorTerm"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorTermInput")
    def node_selector_term_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]], jsii.get(self, "nodeSelectorTermInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b664a6c419dbb47088c352747ac2d52eca90a21209c40bf9dada3f77d57870f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79342100c548f4f057653f5c8cf6b35a861f66cf6c2ac4008b4394b672d78de0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClaimRef")
    def put_claim_ref(
        self,
        *,
        name: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the PersistentVolumeClaim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: The namespace of the PersistentVolumeClaim. Uses 'default' namespace if none is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecClaimRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putClaimRef", [value]))

    @jsii.member(jsii_name="putNodeAffinity")
    def put_node_affinity(
        self,
        *,
        required: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param required: required block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#required DataKubernetesPersistentVolumeV1#required}
        '''
        value = DataKubernetesPersistentVolumeV1SpecNodeAffinity(required=required)

        return typing.cast(None, jsii.invoke(self, "putNodeAffinity", [value]))

    @jsii.member(jsii_name="putPersistentVolumeSource")
    def put_persistent_volume_source(
        self,
        *,
        aws_elastic_block_store: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_disk: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_file: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile", typing.Dict[builtins.str, typing.Any]]] = None,
        ceph_fs: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs", typing.Dict[builtins.str, typing.Any]]] = None,
        cinder: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder", typing.Dict[builtins.str, typing.Any]]] = None,
        csi: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi", typing.Dict[builtins.str, typing.Any]]] = None,
        fc: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc", typing.Dict[builtins.str, typing.Any]]] = None,
        flex_volume: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        flocker: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_persistent_disk: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        glusterfs: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs", typing.Dict[builtins.str, typing.Any]]] = None,
        host_path: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath", typing.Dict[builtins.str, typing.Any]]] = None,
        iscsi: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi", typing.Dict[builtins.str, typing.Any]]] = None,
        local: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        photon_persistent_disk: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        quobyte: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte", typing.Dict[builtins.str, typing.Any]]] = None,
        rbd: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd", typing.Dict[builtins.str, typing.Any]]] = None,
        vsphere_volume: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_elastic_block_store: aws_elastic_block_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#aws_elastic_block_store DataKubernetesPersistentVolumeV1#aws_elastic_block_store}
        :param azure_disk: azure_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#azure_disk DataKubernetesPersistentVolumeV1#azure_disk}
        :param azure_file: azure_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#azure_file DataKubernetesPersistentVolumeV1#azure_file}
        :param ceph_fs: ceph_fs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#ceph_fs DataKubernetesPersistentVolumeV1#ceph_fs}
        :param cinder: cinder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#cinder DataKubernetesPersistentVolumeV1#cinder}
        :param csi: csi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#csi DataKubernetesPersistentVolumeV1#csi}
        :param fc: fc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fc DataKubernetesPersistentVolumeV1#fc}
        :param flex_volume: flex_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#flex_volume DataKubernetesPersistentVolumeV1#flex_volume}
        :param flocker: flocker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#flocker DataKubernetesPersistentVolumeV1#flocker}
        :param gce_persistent_disk: gce_persistent_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#gce_persistent_disk DataKubernetesPersistentVolumeV1#gce_persistent_disk}
        :param glusterfs: glusterfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#glusterfs DataKubernetesPersistentVolumeV1#glusterfs}
        :param host_path: host_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#host_path DataKubernetesPersistentVolumeV1#host_path}
        :param iscsi: iscsi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iscsi DataKubernetesPersistentVolumeV1#iscsi}
        :param local: local block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#local DataKubernetesPersistentVolumeV1#local}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#nfs DataKubernetesPersistentVolumeV1#nfs}
        :param photon_persistent_disk: photon_persistent_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#photon_persistent_disk DataKubernetesPersistentVolumeV1#photon_persistent_disk}
        :param quobyte: quobyte block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#quobyte DataKubernetesPersistentVolumeV1#quobyte}
        :param rbd: rbd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd DataKubernetesPersistentVolumeV1#rbd}
        :param vsphere_volume: vsphere_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#vsphere_volume DataKubernetesPersistentVolumeV1#vsphere_volume}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource(
            aws_elastic_block_store=aws_elastic_block_store,
            azure_disk=azure_disk,
            azure_file=azure_file,
            ceph_fs=ceph_fs,
            cinder=cinder,
            csi=csi,
            fc=fc,
            flex_volume=flex_volume,
            flocker=flocker,
            gce_persistent_disk=gce_persistent_disk,
            glusterfs=glusterfs,
            host_path=host_path,
            iscsi=iscsi,
            local=local,
            nfs=nfs,
            photon_persistent_disk=photon_persistent_disk,
            quobyte=quobyte,
            rbd=rbd,
            vsphere_volume=vsphere_volume,
        )

        return typing.cast(None, jsii.invoke(self, "putPersistentVolumeSource", [value]))

    @jsii.member(jsii_name="resetClaimRef")
    def reset_claim_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClaimRef", []))

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @jsii.member(jsii_name="resetNodeAffinity")
    def reset_node_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAffinity", []))

    @jsii.member(jsii_name="resetPersistentVolumeReclaimPolicy")
    def reset_persistent_volume_reclaim_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistentVolumeReclaimPolicy", []))

    @jsii.member(jsii_name="resetStorageClassName")
    def reset_storage_class_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClassName", []))

    @jsii.member(jsii_name="resetVolumeMode")
    def reset_volume_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMode", []))

    @builtins.property
    @jsii.member(jsii_name="claimRef")
    def claim_ref(self) -> DataKubernetesPersistentVolumeV1SpecClaimRefOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecClaimRefOutputReference, jsii.get(self, "claimRef"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinity")
    def node_affinity(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecNodeAffinityOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecNodeAffinityOutputReference, jsii.get(self, "nodeAffinity"))

    @builtins.property
    @jsii.member(jsii_name="persistentVolumeSource")
    def persistent_volume_source(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceOutputReference", jsii.get(self, "persistentVolumeSource"))

    @builtins.property
    @jsii.member(jsii_name="accessModesInput")
    def access_modes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessModesInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="claimRefInput")
    def claim_ref_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecClaimRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecClaimRef], jsii.get(self, "claimRefInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityInput")
    def node_affinity_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinity]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinity], jsii.get(self, "nodeAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="persistentVolumeReclaimPolicyInput")
    def persistent_volume_reclaim_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "persistentVolumeReclaimPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="persistentVolumeSourceInput")
    def persistent_volume_source_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource"], jsii.get(self, "persistentVolumeSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassNameInput")
    def storage_class_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassNameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeModeInput")
    def volume_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="accessModes")
    def access_modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessModes"))

    @access_modes.setter
    def access_modes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0d2b198e880a425488869c578c18ed087e2dffe947e9c11eaa9e7580a815d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessModes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7163b4bee673417c0b29906d215243f5dcfd98efe934d935e7447823325e82fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88b5fe491d189f9094f2f58b1eaa58323cd8f98d5fa64341d1f982e3d4a46c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="persistentVolumeReclaimPolicy")
    def persistent_volume_reclaim_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "persistentVolumeReclaimPolicy"))

    @persistent_volume_reclaim_policy.setter
    def persistent_volume_reclaim_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686926aaaa1f69ef6830f232be6cafd22b205f25fdf5d3c8eab7d326bf8fc6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "persistentVolumeReclaimPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClassName")
    def storage_class_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClassName"))

    @storage_class_name.setter
    def storage_class_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c382f8d605b979e61d427a26e06ffa6fb7f7bdff9d00a89e8a45f53595e7728a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClassName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeMode")
    def volume_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeMode"))

    @volume_mode.setter
    def volume_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a60c57ebd7785a6b6c9df7319ea1ef38d2583d2240417ef1ab781b761d13cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1Spec]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1Spec]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1Spec]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76fa1b56cda1fe864d656e7bd7c34b66d8839db94e3a0836d4704ee5c31dcb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource",
    jsii_struct_bases=[],
    name_mapping={
        "aws_elastic_block_store": "awsElasticBlockStore",
        "azure_disk": "azureDisk",
        "azure_file": "azureFile",
        "ceph_fs": "cephFs",
        "cinder": "cinder",
        "csi": "csi",
        "fc": "fc",
        "flex_volume": "flexVolume",
        "flocker": "flocker",
        "gce_persistent_disk": "gcePersistentDisk",
        "glusterfs": "glusterfs",
        "host_path": "hostPath",
        "iscsi": "iscsi",
        "local": "local",
        "nfs": "nfs",
        "photon_persistent_disk": "photonPersistentDisk",
        "quobyte": "quobyte",
        "rbd": "rbd",
        "vsphere_volume": "vsphereVolume",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource:
    def __init__(
        self,
        *,
        aws_elastic_block_store: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_disk: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_file: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile", typing.Dict[builtins.str, typing.Any]]] = None,
        ceph_fs: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs", typing.Dict[builtins.str, typing.Any]]] = None,
        cinder: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder", typing.Dict[builtins.str, typing.Any]]] = None,
        csi: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi", typing.Dict[builtins.str, typing.Any]]] = None,
        fc: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc", typing.Dict[builtins.str, typing.Any]]] = None,
        flex_volume: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        flocker: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_persistent_disk: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        glusterfs: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs", typing.Dict[builtins.str, typing.Any]]] = None,
        host_path: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath", typing.Dict[builtins.str, typing.Any]]] = None,
        iscsi: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi", typing.Dict[builtins.str, typing.Any]]] = None,
        local: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        photon_persistent_disk: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        quobyte: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte", typing.Dict[builtins.str, typing.Any]]] = None,
        rbd: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd", typing.Dict[builtins.str, typing.Any]]] = None,
        vsphere_volume: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_elastic_block_store: aws_elastic_block_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#aws_elastic_block_store DataKubernetesPersistentVolumeV1#aws_elastic_block_store}
        :param azure_disk: azure_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#azure_disk DataKubernetesPersistentVolumeV1#azure_disk}
        :param azure_file: azure_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#azure_file DataKubernetesPersistentVolumeV1#azure_file}
        :param ceph_fs: ceph_fs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#ceph_fs DataKubernetesPersistentVolumeV1#ceph_fs}
        :param cinder: cinder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#cinder DataKubernetesPersistentVolumeV1#cinder}
        :param csi: csi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#csi DataKubernetesPersistentVolumeV1#csi}
        :param fc: fc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fc DataKubernetesPersistentVolumeV1#fc}
        :param flex_volume: flex_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#flex_volume DataKubernetesPersistentVolumeV1#flex_volume}
        :param flocker: flocker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#flocker DataKubernetesPersistentVolumeV1#flocker}
        :param gce_persistent_disk: gce_persistent_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#gce_persistent_disk DataKubernetesPersistentVolumeV1#gce_persistent_disk}
        :param glusterfs: glusterfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#glusterfs DataKubernetesPersistentVolumeV1#glusterfs}
        :param host_path: host_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#host_path DataKubernetesPersistentVolumeV1#host_path}
        :param iscsi: iscsi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iscsi DataKubernetesPersistentVolumeV1#iscsi}
        :param local: local block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#local DataKubernetesPersistentVolumeV1#local}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#nfs DataKubernetesPersistentVolumeV1#nfs}
        :param photon_persistent_disk: photon_persistent_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#photon_persistent_disk DataKubernetesPersistentVolumeV1#photon_persistent_disk}
        :param quobyte: quobyte block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#quobyte DataKubernetesPersistentVolumeV1#quobyte}
        :param rbd: rbd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd DataKubernetesPersistentVolumeV1#rbd}
        :param vsphere_volume: vsphere_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#vsphere_volume DataKubernetesPersistentVolumeV1#vsphere_volume}
        '''
        if isinstance(aws_elastic_block_store, dict):
            aws_elastic_block_store = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore(**aws_elastic_block_store)
        if isinstance(azure_disk, dict):
            azure_disk = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk(**azure_disk)
        if isinstance(azure_file, dict):
            azure_file = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile(**azure_file)
        if isinstance(ceph_fs, dict):
            ceph_fs = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs(**ceph_fs)
        if isinstance(cinder, dict):
            cinder = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder(**cinder)
        if isinstance(csi, dict):
            csi = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi(**csi)
        if isinstance(fc, dict):
            fc = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc(**fc)
        if isinstance(flex_volume, dict):
            flex_volume = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume(**flex_volume)
        if isinstance(flocker, dict):
            flocker = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker(**flocker)
        if isinstance(gce_persistent_disk, dict):
            gce_persistent_disk = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk(**gce_persistent_disk)
        if isinstance(glusterfs, dict):
            glusterfs = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs(**glusterfs)
        if isinstance(host_path, dict):
            host_path = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath(**host_path)
        if isinstance(iscsi, dict):
            iscsi = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi(**iscsi)
        if isinstance(local, dict):
            local = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal(**local)
        if isinstance(nfs, dict):
            nfs = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs(**nfs)
        if isinstance(photon_persistent_disk, dict):
            photon_persistent_disk = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk(**photon_persistent_disk)
        if isinstance(quobyte, dict):
            quobyte = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte(**quobyte)
        if isinstance(rbd, dict):
            rbd = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd(**rbd)
        if isinstance(vsphere_volume, dict):
            vsphere_volume = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume(**vsphere_volume)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113976244ca2fe5a798509c5f9621655003ae601e6cd7a292165dac63090f031)
            check_type(argname="argument aws_elastic_block_store", value=aws_elastic_block_store, expected_type=type_hints["aws_elastic_block_store"])
            check_type(argname="argument azure_disk", value=azure_disk, expected_type=type_hints["azure_disk"])
            check_type(argname="argument azure_file", value=azure_file, expected_type=type_hints["azure_file"])
            check_type(argname="argument ceph_fs", value=ceph_fs, expected_type=type_hints["ceph_fs"])
            check_type(argname="argument cinder", value=cinder, expected_type=type_hints["cinder"])
            check_type(argname="argument csi", value=csi, expected_type=type_hints["csi"])
            check_type(argname="argument fc", value=fc, expected_type=type_hints["fc"])
            check_type(argname="argument flex_volume", value=flex_volume, expected_type=type_hints["flex_volume"])
            check_type(argname="argument flocker", value=flocker, expected_type=type_hints["flocker"])
            check_type(argname="argument gce_persistent_disk", value=gce_persistent_disk, expected_type=type_hints["gce_persistent_disk"])
            check_type(argname="argument glusterfs", value=glusterfs, expected_type=type_hints["glusterfs"])
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
            check_type(argname="argument iscsi", value=iscsi, expected_type=type_hints["iscsi"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            check_type(argname="argument photon_persistent_disk", value=photon_persistent_disk, expected_type=type_hints["photon_persistent_disk"])
            check_type(argname="argument quobyte", value=quobyte, expected_type=type_hints["quobyte"])
            check_type(argname="argument rbd", value=rbd, expected_type=type_hints["rbd"])
            check_type(argname="argument vsphere_volume", value=vsphere_volume, expected_type=type_hints["vsphere_volume"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_elastic_block_store is not None:
            self._values["aws_elastic_block_store"] = aws_elastic_block_store
        if azure_disk is not None:
            self._values["azure_disk"] = azure_disk
        if azure_file is not None:
            self._values["azure_file"] = azure_file
        if ceph_fs is not None:
            self._values["ceph_fs"] = ceph_fs
        if cinder is not None:
            self._values["cinder"] = cinder
        if csi is not None:
            self._values["csi"] = csi
        if fc is not None:
            self._values["fc"] = fc
        if flex_volume is not None:
            self._values["flex_volume"] = flex_volume
        if flocker is not None:
            self._values["flocker"] = flocker
        if gce_persistent_disk is not None:
            self._values["gce_persistent_disk"] = gce_persistent_disk
        if glusterfs is not None:
            self._values["glusterfs"] = glusterfs
        if host_path is not None:
            self._values["host_path"] = host_path
        if iscsi is not None:
            self._values["iscsi"] = iscsi
        if local is not None:
            self._values["local"] = local
        if nfs is not None:
            self._values["nfs"] = nfs
        if photon_persistent_disk is not None:
            self._values["photon_persistent_disk"] = photon_persistent_disk
        if quobyte is not None:
            self._values["quobyte"] = quobyte
        if rbd is not None:
            self._values["rbd"] = rbd
        if vsphere_volume is not None:
            self._values["vsphere_volume"] = vsphere_volume

    @builtins.property
    def aws_elastic_block_store(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore"]:
        '''aws_elastic_block_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#aws_elastic_block_store DataKubernetesPersistentVolumeV1#aws_elastic_block_store}
        '''
        result = self._values.get("aws_elastic_block_store")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore"], result)

    @builtins.property
    def azure_disk(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk"]:
        '''azure_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#azure_disk DataKubernetesPersistentVolumeV1#azure_disk}
        '''
        result = self._values.get("azure_disk")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk"], result)

    @builtins.property
    def azure_file(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile"]:
        '''azure_file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#azure_file DataKubernetesPersistentVolumeV1#azure_file}
        '''
        result = self._values.get("azure_file")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile"], result)

    @builtins.property
    def ceph_fs(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs"]:
        '''ceph_fs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#ceph_fs DataKubernetesPersistentVolumeV1#ceph_fs}
        '''
        result = self._values.get("ceph_fs")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs"], result)

    @builtins.property
    def cinder(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder"]:
        '''cinder block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#cinder DataKubernetesPersistentVolumeV1#cinder}
        '''
        result = self._values.get("cinder")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder"], result)

    @builtins.property
    def csi(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi"]:
        '''csi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#csi DataKubernetesPersistentVolumeV1#csi}
        '''
        result = self._values.get("csi")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi"], result)

    @builtins.property
    def fc(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc"]:
        '''fc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fc DataKubernetesPersistentVolumeV1#fc}
        '''
        result = self._values.get("fc")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc"], result)

    @builtins.property
    def flex_volume(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume"]:
        '''flex_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#flex_volume DataKubernetesPersistentVolumeV1#flex_volume}
        '''
        result = self._values.get("flex_volume")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume"], result)

    @builtins.property
    def flocker(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker"]:
        '''flocker block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#flocker DataKubernetesPersistentVolumeV1#flocker}
        '''
        result = self._values.get("flocker")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker"], result)

    @builtins.property
    def gce_persistent_disk(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk"]:
        '''gce_persistent_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#gce_persistent_disk DataKubernetesPersistentVolumeV1#gce_persistent_disk}
        '''
        result = self._values.get("gce_persistent_disk")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk"], result)

    @builtins.property
    def glusterfs(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs"]:
        '''glusterfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#glusterfs DataKubernetesPersistentVolumeV1#glusterfs}
        '''
        result = self._values.get("glusterfs")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs"], result)

    @builtins.property
    def host_path(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath"]:
        '''host_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#host_path DataKubernetesPersistentVolumeV1#host_path}
        '''
        result = self._values.get("host_path")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath"], result)

    @builtins.property
    def iscsi(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi"]:
        '''iscsi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iscsi DataKubernetesPersistentVolumeV1#iscsi}
        '''
        result = self._values.get("iscsi")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi"], result)

    @builtins.property
    def local(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal"]:
        '''local block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#local DataKubernetesPersistentVolumeV1#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal"], result)

    @builtins.property
    def nfs(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#nfs DataKubernetesPersistentVolumeV1#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs"], result)

    @builtins.property
    def photon_persistent_disk(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk"]:
        '''photon_persistent_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#photon_persistent_disk DataKubernetesPersistentVolumeV1#photon_persistent_disk}
        '''
        result = self._values.get("photon_persistent_disk")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk"], result)

    @builtins.property
    def quobyte(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte"]:
        '''quobyte block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#quobyte DataKubernetesPersistentVolumeV1#quobyte}
        '''
        result = self._values.get("quobyte")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte"], result)

    @builtins.property
    def rbd(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd"]:
        '''rbd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd DataKubernetesPersistentVolumeV1#rbd}
        '''
        result = self._values.get("rbd")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd"], result)

    @builtins.property
    def vsphere_volume(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume"]:
        '''vsphere_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#vsphere_volume DataKubernetesPersistentVolumeV1#vsphere_volume}
        '''
        result = self._values.get("vsphere_volume")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore",
    jsii_struct_bases=[],
    name_mapping={
        "volume_id": "volumeId",
        "fs_type": "fsType",
        "partition": "partition",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore:
    def __init__(
        self,
        *,
        volume_id: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        partition: typing.Optional[jsii.Number] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param volume_id: Unique ID of the persistent disk resource in AWS (Amazon EBS volume). More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_id DataKubernetesPersistentVolumeV1#volume_id}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param partition: The partition in the volume that you want to mount. If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#partition DataKubernetesPersistentVolumeV1#partition}
        :param read_only: Whether to set the read-only property in VolumeMounts to "true". If omitted, the default is "false". More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d84f1cee603d1e9964f9438dde61fad35f9a9ebe9848410a13516ab6e566425)
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "volume_id": volume_id,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if partition is not None:
            self._values["partition"] = partition
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def volume_id(self) -> builtins.str:
        '''Unique ID of the persistent disk resource in AWS (Amazon EBS volume). More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_id DataKubernetesPersistentVolumeV1#volume_id}
        '''
        result = self._values.get("volume_id")
        assert result is not None, "Required property 'volume_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type of the volume that you want to mount.

        Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[jsii.Number]:
        '''The partition in the volume that you want to mount.

        If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#partition DataKubernetesPersistentVolumeV1#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to set the read-only property in VolumeMounts to "true". If omitted, the default is "false". More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4481c3bc6efda3a18a6e5114da4138675ff4041eb5ae9077e63f93917e7b185f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeIdInput")
    def volume_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d797ed10c0825e6c157829c96b37376934c73df8307d932c84a842a631313658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4460db22a20acc259e05e6ca666cc74a1fdb9892cfd115cd5e776d29fb934d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1b744e5fd526a4a344ef1353f418588e6971254212425011fe8bda58174bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeId"))

    @volume_id.setter
    def volume_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26817bd5a8b2322db5df3f20b12a7ae9e0cbaae4fd4fc45c77d813c0ca1d3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6ad61a1aafc60119ed65ce6b73ce3323e8ffc23d1ec76cd5b949a9cf3a3611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk",
    jsii_struct_bases=[],
    name_mapping={
        "caching_mode": "cachingMode",
        "data_disk_uri": "dataDiskUri",
        "disk_name": "diskName",
        "fs_type": "fsType",
        "kind": "kind",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk:
    def __init__(
        self,
        *,
        caching_mode: builtins.str,
        data_disk_uri: builtins.str,
        disk_name: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param caching_mode: Host Caching mode: None, Read Only, Read Write. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#caching_mode DataKubernetesPersistentVolumeV1#caching_mode}
        :param data_disk_uri: The URI the data disk in the blob storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#data_disk_uri DataKubernetesPersistentVolumeV1#data_disk_uri}
        :param disk_name: The Name of the data disk in the blob storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#disk_name DataKubernetesPersistentVolumeV1#disk_name}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param kind: The type for the data disk. Expected values: Shared, Dedicated, Managed. Defaults to Shared. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#kind DataKubernetesPersistentVolumeV1#kind}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98db2c5e57788f811028512f8f7dc68a1b3ee2ba8b44180b6ec11b3108e9daf2)
            check_type(argname="argument caching_mode", value=caching_mode, expected_type=type_hints["caching_mode"])
            check_type(argname="argument data_disk_uri", value=data_disk_uri, expected_type=type_hints["data_disk_uri"])
            check_type(argname="argument disk_name", value=disk_name, expected_type=type_hints["disk_name"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "caching_mode": caching_mode,
            "data_disk_uri": data_disk_uri,
            "disk_name": disk_name,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if kind is not None:
            self._values["kind"] = kind
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def caching_mode(self) -> builtins.str:
        '''Host Caching mode: None, Read Only, Read Write.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#caching_mode DataKubernetesPersistentVolumeV1#caching_mode}
        '''
        result = self._values.get("caching_mode")
        assert result is not None, "Required property 'caching_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_disk_uri(self) -> builtins.str:
        '''The URI the data disk in the blob storage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#data_disk_uri DataKubernetesPersistentVolumeV1#data_disk_uri}
        '''
        result = self._values.get("data_disk_uri")
        assert result is not None, "Required property 'data_disk_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_name(self) -> builtins.str:
        '''The Name of the data disk in the blob storage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#disk_name DataKubernetesPersistentVolumeV1#disk_name}
        '''
        result = self._values.get("disk_name")
        assert result is not None, "Required property 'disk_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''The type for the data disk. Expected values: Shared, Dedicated, Managed. Defaults to Shared.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#kind DataKubernetesPersistentVolumeV1#kind}
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf682a19c605f0c89fc3e75616752ce4910c93b4325d47fd57553ff5e6bdf51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="cachingModeInput")
    def caching_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskUriInput")
    def data_disk_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDiskUriInput"))

    @builtins.property
    @jsii.member(jsii_name="diskNameInput")
    def disk_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="cachingMode")
    def caching_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachingMode"))

    @caching_mode.setter
    def caching_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607d0982d2631b71198640cd3584b9faa0fd9dbeff7be2dd501cd1cf5623b1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskUri")
    def data_disk_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskUri"))

    @data_disk_uri.setter
    def data_disk_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6464728969dba38444c2692b9fe5c4f068e7eb1aae9a4bbebecf970855ae3c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskName")
    def disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskName"))

    @disk_name.setter
    def disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac88c7b0da31b6a6fe4a9e215d5031b56f709fbd72231240ec1b7d53dd95cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b567e1e4c60b0e3cefe58a4754f096942a4526729488a0edf8c3dd9c41f4f7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e632a528d070082b7a218f656fdc2f1b81f2a4daf51201b8699d2778fdb9b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cd8aa80fc894b1295de26e3a41fca90d098881edc38558d54d1254d3d729f95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a217a6b7c3929cea21179233fe69b3d72e74f0dea55c8737bd88cca7e5b1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "share_name": "shareName",
        "read_only": "readOnly",
        "secret_namespace": "secretNamespace",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        share_name: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_name: The name of secret that contains Azure Storage Account Name and Key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_name DataKubernetesPersistentVolumeV1#secret_name}
        :param share_name: Share Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#share_name DataKubernetesPersistentVolumeV1#share_name}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_namespace: The namespace of the secret that contains Azure Storage Account Name and Key. For Kubernetes up to 1.18.x the default is the same as the Pod. For Kubernetes 1.19.x and later the default is "default" namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_namespace DataKubernetesPersistentVolumeV1#secret_namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca89969e183b084ed94395577675b9d82bd43f819f2fee9cb21ee09c367315ff)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument secret_namespace", value=secret_namespace, expected_type=type_hints["secret_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
            "share_name": share_name,
        }
        if read_only is not None:
            self._values["read_only"] = read_only
        if secret_namespace is not None:
            self._values["secret_namespace"] = secret_namespace

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''The name of secret that contains Azure Storage Account Name and Key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_name DataKubernetesPersistentVolumeV1#secret_name}
        '''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def share_name(self) -> builtins.str:
        '''Share Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#share_name DataKubernetesPersistentVolumeV1#share_name}
        '''
        result = self._values.get("share_name")
        assert result is not None, "Required property 'share_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the secret that contains Azure Storage Account Name and Key.

        For Kubernetes up to 1.18.x the default is the same as the Pod. For Kubernetes 1.19.x and later the default is "default" namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_namespace DataKubernetesPersistentVolumeV1#secret_namespace}
        '''
        result = self._values.get("secret_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bff3ebb9d101b1eff9a17f051259b25329cf3eafcfa2ff7eee19aa64ad7b147a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSecretNamespace")
    def reset_secret_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNamespaceInput")
    def secret_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="shareNameInput")
    def share_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__55bd178cc4bf6e5ceeabdf6b0966c235a12a66d7280b46112a0229f2fb78960b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b600c7783878e6bf226408abe59ef5d52dcf6bfe8aabd966077d6f06b9b4822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretNamespace")
    def secret_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretNamespace"))

    @secret_namespace.setter
    def secret_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbb915c150ecff69d69c9a567abe5e9a41d093a4ff7dc2afe049366a34d85d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18dac20213c3d7c18d5a90b736a9239a63c7a6cd9184904ac5b1cc51dee667df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb1cec703cb54cd084098fbf7afa767605ca3677fdc36d303ec81f7ba3a8a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs",
    jsii_struct_bases=[],
    name_mapping={
        "monitors": "monitors",
        "path": "path",
        "read_only": "readOnly",
        "secret_file": "secretFile",
        "secret_ref": "secretRef",
        "user": "user",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs:
    def __init__(
        self,
        *,
        monitors: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_file: typing.Optional[builtins.str] = None,
        secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param monitors: Monitors is a collection of Ceph monitors. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#monitors DataKubernetesPersistentVolumeV1#monitors}
        :param path: Used as the mounted root, rather than the full Ceph tree, default is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to ``false`` (read/write). More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_file: The path to key ring for User, default is ``/etc/ceph/user.secret``. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_file DataKubernetesPersistentVolumeV1#secret_file}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        :param user: User is the rados user name, default is admin. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#user DataKubernetesPersistentVolumeV1#user}
        '''
        if isinstance(secret_ref, dict):
            secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef(**secret_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21574e500eeefa0024fd86c1ea36f6c302cac859cbafab86a2efccf65b296ab6)
            check_type(argname="argument monitors", value=monitors, expected_type=type_hints["monitors"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument secret_file", value=secret_file, expected_type=type_hints["secret_file"])
            check_type(argname="argument secret_ref", value=secret_ref, expected_type=type_hints["secret_ref"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitors": monitors,
        }
        if path is not None:
            self._values["path"] = path
        if read_only is not None:
            self._values["read_only"] = read_only
        if secret_file is not None:
            self._values["secret_file"] = secret_file
        if secret_ref is not None:
            self._values["secret_ref"] = secret_ref
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def monitors(self) -> typing.List[builtins.str]:
        '''Monitors is a collection of Ceph monitors. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#monitors DataKubernetesPersistentVolumeV1#monitors}
        '''
        result = self._values.get("monitors")
        assert result is not None, "Required property 'monitors' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Used as the mounted root, rather than the full Ceph tree, default is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to ``false`` (read/write). More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_file(self) -> typing.Optional[builtins.str]:
        '''The path to key ring for User, default is ``/etc/ceph/user.secret``. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_file DataKubernetesPersistentVolumeV1#secret_file}
        '''
        result = self._values.get("secret_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef"]:
        '''secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        result = self._values.get("secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef"], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''User is the rados user name, default is admin. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#user DataKubernetesPersistentVolumeV1#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79cecb907445c48d9ed655112de946f02b933a03fa104089c33b22f014c4333a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretRef")
    def put_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putSecretRef", [value]))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSecretFile")
    def reset_secret_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretFile", []))

    @jsii.member(jsii_name="resetSecretRef")
    def reset_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretRef", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="secretRef")
    def secret_ref(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRefOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRefOutputReference", jsii.get(self, "secretRef"))

    @builtins.property
    @jsii.member(jsii_name="monitorsInput")
    def monitors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monitorsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretFileInput")
    def secret_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretFileInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRefInput")
    def secret_ref_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef"], jsii.get(self, "secretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="monitors")
    def monitors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monitors"))

    @monitors.setter
    def monitors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4dae5f600d4cf1d3265c5c1e243878edada09a22b541630f0307f050677583a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5a05691a3849b70232b1fffd609931b3a8e3f0297dd34f8e3fad0bf4273cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__bb83ea9bf2ae4179d87142f3c0ace9b8230bb461a04caeccc291344929f15a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretFile")
    def secret_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretFile"))

    @secret_file.setter
    def secret_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfea857a268de465d880d71e4027bcaf6227eead88824402f51d0da29f0bacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1aff64bbb369d4d289bfc6d27f162e4df12bfe7baf4c2edd44837e73edb11b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35ff2767acaf1119de5bf958fc2c7ad45cd7c0d83b5a33aefbb3fbd54523734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108018c8d38866dbeaffc621529725d815e64d1e2fd886bfe1f0a3a2600219eb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a96bcf878fc410e85497703fa5589c05b8da8143533f93173ca490dcf6ef6adb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__98b6400e6805a31c8377fb3a3de64cc489d543cca2f666ad2a293859f35c217d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e367b40f90d0a51966be45c9072837e3926e84ec201193612606a2fefc44e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e111ed8b118e039d9d185028baf3309de13807d534d26824a2440d6203782500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder",
    jsii_struct_bases=[],
    name_mapping={
        "volume_id": "volumeId",
        "fs_type": "fsType",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder:
    def __init__(
        self,
        *,
        volume_id: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param volume_id: Volume ID used to identify the volume in Cinder. More info: https://examples.k8s.io/mysql-cinder-pd/README.md. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_id DataKubernetesPersistentVolumeV1#volume_id}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://examples.k8s.io/mysql-cinder-pd/README.md Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). More info: https://examples.k8s.io/mysql-cinder-pd/README.md. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762417192d9ab1938214e0a567ffaea5d88a588c4da896d37aba7657de6f6ae2)
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "volume_id": volume_id,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def volume_id(self) -> builtins.str:
        '''Volume ID used to identify the volume in Cinder. More info: https://examples.k8s.io/mysql-cinder-pd/README.md.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_id DataKubernetesPersistentVolumeV1#volume_id}
        '''
        result = self._values.get("volume_id")
        assert result is not None, "Required property 'volume_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://examples.k8s.io/mysql-cinder-pd/README.md

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). More info: https://examples.k8s.io/mysql-cinder-pd/README.md.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d270519917ff4625bf6210cd564924a23272f6d3063f04700d2393a0d1534afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeIdInput")
    def volume_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ee3675e6ff8a896808aed126746c74a5bbcfc3f452f35eedd94f1bd94e7c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c4f7978828126c397030c29614f9f0751cc3f85db384a289b485bdbd09132629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeId"))

    @volume_id.setter
    def volume_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26bffd4b078ccb837dc55280c9b2c5edd712c0f061342c89d880ec2e773e1f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7f94f467864f1d364cbaf9c3d6ccab745797803a5776ffa964823349138bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi",
    jsii_struct_bases=[],
    name_mapping={
        "driver": "driver",
        "volume_handle": "volumeHandle",
        "controller_expand_secret_ref": "controllerExpandSecretRef",
        "controller_publish_secret_ref": "controllerPublishSecretRef",
        "fs_type": "fsType",
        "node_publish_secret_ref": "nodePublishSecretRef",
        "node_stage_secret_ref": "nodeStageSecretRef",
        "read_only": "readOnly",
        "volume_attributes": "volumeAttributes",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi:
    def __init__(
        self,
        *,
        driver: builtins.str,
        volume_handle: builtins.str,
        controller_expand_secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
        controller_publish_secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
        fs_type: typing.Optional[builtins.str] = None,
        node_publish_secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
        node_stage_secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver: the name of the volume driver to use. More info: https://kubernetes.io/docs/concepts/storage/volumes/#csi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#driver DataKubernetesPersistentVolumeV1#driver}
        :param volume_handle: A string value that uniquely identifies the volume. More info: https://kubernetes.io/docs/concepts/storage/volumes/#csi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_handle DataKubernetesPersistentVolumeV1#volume_handle}
        :param controller_expand_secret_ref: controller_expand_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#controller_expand_secret_ref DataKubernetesPersistentVolumeV1#controller_expand_secret_ref}
        :param controller_publish_secret_ref: controller_publish_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#controller_publish_secret_ref DataKubernetesPersistentVolumeV1#controller_publish_secret_ref}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param node_publish_secret_ref: node_publish_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_publish_secret_ref DataKubernetesPersistentVolumeV1#node_publish_secret_ref}
        :param node_stage_secret_ref: node_stage_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_stage_secret_ref DataKubernetesPersistentVolumeV1#node_stage_secret_ref}
        :param read_only: Whether to set the read-only property in VolumeMounts to "true". If omitted, the default is "false". More info: https://kubernetes.io/docs/concepts/storage/volumes#csi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param volume_attributes: Attributes of the volume to publish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_attributes DataKubernetesPersistentVolumeV1#volume_attributes}
        '''
        if isinstance(controller_expand_secret_ref, dict):
            controller_expand_secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef(**controller_expand_secret_ref)
        if isinstance(controller_publish_secret_ref, dict):
            controller_publish_secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef(**controller_publish_secret_ref)
        if isinstance(node_publish_secret_ref, dict):
            node_publish_secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef(**node_publish_secret_ref)
        if isinstance(node_stage_secret_ref, dict):
            node_stage_secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef(**node_stage_secret_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85cabe6ef938771e07bf1fcf90608f1c665462dbbafef6c63e5adc6e5f85108)
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument volume_handle", value=volume_handle, expected_type=type_hints["volume_handle"])
            check_type(argname="argument controller_expand_secret_ref", value=controller_expand_secret_ref, expected_type=type_hints["controller_expand_secret_ref"])
            check_type(argname="argument controller_publish_secret_ref", value=controller_publish_secret_ref, expected_type=type_hints["controller_publish_secret_ref"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument node_publish_secret_ref", value=node_publish_secret_ref, expected_type=type_hints["node_publish_secret_ref"])
            check_type(argname="argument node_stage_secret_ref", value=node_stage_secret_ref, expected_type=type_hints["node_stage_secret_ref"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument volume_attributes", value=volume_attributes, expected_type=type_hints["volume_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver": driver,
            "volume_handle": volume_handle,
        }
        if controller_expand_secret_ref is not None:
            self._values["controller_expand_secret_ref"] = controller_expand_secret_ref
        if controller_publish_secret_ref is not None:
            self._values["controller_publish_secret_ref"] = controller_publish_secret_ref
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if node_publish_secret_ref is not None:
            self._values["node_publish_secret_ref"] = node_publish_secret_ref
        if node_stage_secret_ref is not None:
            self._values["node_stage_secret_ref"] = node_stage_secret_ref
        if read_only is not None:
            self._values["read_only"] = read_only
        if volume_attributes is not None:
            self._values["volume_attributes"] = volume_attributes

    @builtins.property
    def driver(self) -> builtins.str:
        '''the name of the volume driver to use. More info: https://kubernetes.io/docs/concepts/storage/volumes/#csi.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#driver DataKubernetesPersistentVolumeV1#driver}
        '''
        result = self._values.get("driver")
        assert result is not None, "Required property 'driver' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_handle(self) -> builtins.str:
        '''A string value that uniquely identifies the volume. More info: https://kubernetes.io/docs/concepts/storage/volumes/#csi.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_handle DataKubernetesPersistentVolumeV1#volume_handle}
        '''
        result = self._values.get("volume_handle")
        assert result is not None, "Required property 'volume_handle' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def controller_expand_secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef"]:
        '''controller_expand_secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#controller_expand_secret_ref DataKubernetesPersistentVolumeV1#controller_expand_secret_ref}
        '''
        result = self._values.get("controller_expand_secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef"], result)

    @builtins.property
    def controller_publish_secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef"]:
        '''controller_publish_secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#controller_publish_secret_ref DataKubernetesPersistentVolumeV1#controller_publish_secret_ref}
        '''
        result = self._values.get("controller_publish_secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef"], result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_publish_secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef"]:
        '''node_publish_secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_publish_secret_ref DataKubernetesPersistentVolumeV1#node_publish_secret_ref}
        '''
        result = self._values.get("node_publish_secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef"], result)

    @builtins.property
    def node_stage_secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef"]:
        '''node_stage_secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_stage_secret_ref DataKubernetesPersistentVolumeV1#node_stage_secret_ref}
        '''
        result = self._values.get("node_stage_secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef"], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to set the read-only property in VolumeMounts to "true". If omitted, the default is "false". More info: https://kubernetes.io/docs/concepts/storage/volumes#csi.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def volume_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Attributes of the volume to publish.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_attributes DataKubernetesPersistentVolumeV1#volume_attributes}
        '''
        result = self._values.get("volume_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc099719380e72cbdeeab2015eaf4d7ba305efbd4c7ea3f6c6dcb7224672becd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24e1c50b466c632565ccdeafe41a4ce577408e6fe9cfbb6a10d75bba058b22e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fa16e0cb7cb6f26c1ea97e1a5c548416c3a44628e125fec45aa3793f0383cd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6381259433490a0c0626efda5ef883f4b4fba4f951257f250ca381fbfd39a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2526198a23b4053a5900082a940fa062477d8678ad2450df3a83146cb085c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92de899c7ccec6485649ccced6735e39ac3a21c61d0aac855c7fdb41285d51ad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ccbebcfdb9d191a7478fcb1bcac8c6463e1f78f3ed65de440e9a67eaf191806)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c0b5e476a34d3226a0d524be2331f62d0339aeda1a4f37780a7f674e2550c47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415889eb5c7b226dfcd45ff765518075b95b5c8e403550ab7d8f3a051b303d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7604551e89c0e2a049793375e3f1cf81caa432f86dc403980d10506eda8c5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fd09f8bbff57d161f1a15dbb1ae42d718d8f330b47abb6856d4d278f8ce04f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6077184a5d5c2be081ef2d44358a2b5a004b6fbafebd4ff880e5966580e3c11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__10268b4c21cd8ba27954cb4e084fdc43382fd7bec25fa37998f0ae5be4359a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea97c015565da84bc625a461efc1ba0d1fabb5897e0edfce458382adc7b1848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d565630d7aa18a935928cfd63110847cd8654f9e46f1c55fb6a542eefbf55c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0711a4e1d4885bf8aacbcb2b04a8eed22df7a14f5d9a292a34e32a34616b755b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2110fab5345e61f2f8ab12f3bdd74f987ddda56a727392a5475b82acbbb142cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__95941b05d74a7cb7354ad29422988934efb4477070ddb81fdd3d71eb2365ef06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce5300888a88062e96a0592a5e17eb7cff53858cefaf5b92ee5066e1b2ea74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36562f58a51a30e902cfb5ee377a2c9fa3949f6b7fce067eda6d612415c41e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6407951d4efb2d74d262802f4c47530ce6b7de5eda7ddf43f78dfbaba7cf45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putControllerExpandSecretRef")
    def put_controller_expand_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putControllerExpandSecretRef", [value]))

    @jsii.member(jsii_name="putControllerPublishSecretRef")
    def put_controller_publish_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putControllerPublishSecretRef", [value]))

    @jsii.member(jsii_name="putNodePublishSecretRef")
    def put_node_publish_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putNodePublishSecretRef", [value]))

    @jsii.member(jsii_name="putNodeStageSecretRef")
    def put_node_stage_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putNodeStageSecretRef", [value]))

    @jsii.member(jsii_name="resetControllerExpandSecretRef")
    def reset_controller_expand_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControllerExpandSecretRef", []))

    @jsii.member(jsii_name="resetControllerPublishSecretRef")
    def reset_controller_publish_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControllerPublishSecretRef", []))

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetNodePublishSecretRef")
    def reset_node_publish_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublishSecretRef", []))

    @jsii.member(jsii_name="resetNodeStageSecretRef")
    def reset_node_stage_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeStageSecretRef", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetVolumeAttributes")
    def reset_volume_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="controllerExpandSecretRef")
    def controller_expand_secret_ref(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRefOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRefOutputReference, jsii.get(self, "controllerExpandSecretRef"))

    @builtins.property
    @jsii.member(jsii_name="controllerPublishSecretRef")
    def controller_publish_secret_ref(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRefOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRefOutputReference, jsii.get(self, "controllerPublishSecretRef"))

    @builtins.property
    @jsii.member(jsii_name="nodePublishSecretRef")
    def node_publish_secret_ref(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRefOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRefOutputReference, jsii.get(self, "nodePublishSecretRef"))

    @builtins.property
    @jsii.member(jsii_name="nodeStageSecretRef")
    def node_stage_secret_ref(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRefOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRefOutputReference, jsii.get(self, "nodeStageSecretRef"))

    @builtins.property
    @jsii.member(jsii_name="controllerExpandSecretRefInput")
    def controller_expand_secret_ref_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef], jsii.get(self, "controllerExpandSecretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="controllerPublishSecretRefInput")
    def controller_publish_secret_ref_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef], jsii.get(self, "controllerPublishSecretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="driverInput")
    def driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInput"))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublishSecretRefInput")
    def node_publish_secret_ref_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef], jsii.get(self, "nodePublishSecretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeStageSecretRefInput")
    def node_stage_secret_ref_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef], jsii.get(self, "nodeStageSecretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeAttributesInput")
    def volume_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "volumeAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeHandleInput")
    def volume_handle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeHandleInput"))

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driver"))

    @driver.setter
    def driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e484a17e46cc553e7995aaf99d10573666ba377e10cb6a392bbabdafa7c9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7b161854bd546fec9fc4282bfee9a49da0ae5ed852d83f5cdc21fabcad6cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c4f2618f0e93594359a64554f500e54051b2fb08b3f7da967da1e49f2d7a3b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeAttributes")
    def volume_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "volumeAttributes"))

    @volume_attributes.setter
    def volume_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92860d484a4a27a16d0d8fca41e430f2b184df5dc32cb621d42009b8653a1bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeHandle")
    def volume_handle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeHandle"))

    @volume_handle.setter
    def volume_handle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daafb6b00e9c28f06004aa93b97d5d9c6d38a7d37f76b90392d108fc314d62e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeHandle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55951abdcb788a47a83fb6426af24f633491044a70e4705b582396b19ef31641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc",
    jsii_struct_bases=[],
    name_mapping={
        "lun": "lun",
        "target_ww_ns": "targetWwNs",
        "fs_type": "fsType",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc:
    def __init__(
        self,
        *,
        lun: jsii.Number,
        target_ww_ns: typing.Sequence[builtins.str],
        fs_type: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param lun: FC target lun number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#lun DataKubernetesPersistentVolumeV1#lun}
        :param target_ww_ns: FC target worldwide names (WWNs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#target_ww_ns DataKubernetesPersistentVolumeV1#target_ww_ns}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1072eeef6ed822c30347f081d0cf3ce6087dc4252d2be80e450aa5d29e27bbc2)
            check_type(argname="argument lun", value=lun, expected_type=type_hints["lun"])
            check_type(argname="argument target_ww_ns", value=target_ww_ns, expected_type=type_hints["target_ww_ns"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lun": lun,
            "target_ww_ns": target_ww_ns,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def lun(self) -> jsii.Number:
        '''FC target lun number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#lun DataKubernetesPersistentVolumeV1#lun}
        '''
        result = self._values.get("lun")
        assert result is not None, "Required property 'lun' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def target_ww_ns(self) -> typing.List[builtins.str]:
        '''FC target worldwide names (WWNs).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#target_ww_ns DataKubernetesPersistentVolumeV1#target_ww_ns}
        '''
        result = self._values.get("target_ww_ns")
        assert result is not None, "Required property 'target_ww_ns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7fdeedbbab3cf9b5737ac9169ace89dd5736011ec8cc436c21a0023be92683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lunInput")
    def lun_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lunInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetWwNsInput")
    def target_ww_ns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetWwNsInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc0b7710e8f342683747a6c4b7d6170ec47f4fb25dc0e03e11bd7ebf0c83d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lun")
    def lun(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lun"))

    @lun.setter
    def lun(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab8e36de22cf495a57dbd5774409967f906c9defcad22a0a6f0a14b0be05fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lun", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b3005a6eeb4d1a005bd814dc6cf620994efaf6494757c6e53547a82d7e90d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetWwNs")
    def target_ww_ns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetWwNs"))

    @target_ww_ns.setter
    def target_ww_ns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e43dcf1078933f8c67fa292c465c73b1dff3082646a99e15d67181f619ba193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetWwNs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5910cc248ab4f97fe4e5b5539c09c127ad49eb38833df1b6e90d3299e66ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume",
    jsii_struct_bases=[],
    name_mapping={
        "driver": "driver",
        "fs_type": "fsType",
        "options": "options",
        "read_only": "readOnly",
        "secret_ref": "secretRef",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume:
    def __init__(
        self,
        *,
        driver: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param driver: Driver is the name of the driver to use for this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#driver DataKubernetesPersistentVolumeV1#driver}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem depends on FlexVolume script. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param options: Extra command options if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#options DataKubernetesPersistentVolumeV1#options}
        :param read_only: Whether to force the ReadOnly setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        if isinstance(secret_ref, dict):
            secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef(**secret_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7255398244458af6d67f628503e7b703e761c72122ad8bb717ce0b51df62c0f3)
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument secret_ref", value=secret_ref, expected_type=type_hints["secret_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver": driver,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if options is not None:
            self._values["options"] = options
        if read_only is not None:
            self._values["read_only"] = read_only
        if secret_ref is not None:
            self._values["secret_ref"] = secret_ref

    @builtins.property
    def driver(self) -> builtins.str:
        '''Driver is the name of the driver to use for this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#driver DataKubernetesPersistentVolumeV1#driver}
        '''
        result = self._values.get("driver")
        assert result is not None, "Required property 'driver' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem depends on FlexVolume script.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Extra command options if any.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#options DataKubernetesPersistentVolumeV1#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the ReadOnly setting in VolumeMounts. Defaults to false (read/write).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef"]:
        '''secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        result = self._values.get("secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c5ac88e040f87ea970a5132c8dcaa0dccc926b351d1b47a3c4351130ce8e20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretRef")
    def put_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putSecretRef", [value]))

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSecretRef")
    def reset_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretRef", []))

    @builtins.property
    @jsii.member(jsii_name="secretRef")
    def secret_ref(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRefOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRefOutputReference", jsii.get(self, "secretRef"))

    @builtins.property
    @jsii.member(jsii_name="driverInput")
    def driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInput"))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRefInput")
    def secret_ref_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef"], jsii.get(self, "secretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driver"))

    @driver.setter
    def driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4df2c919ad472d35c8b8f64ddc7e8cad1f490447a2d4ad37fd6bd15d1ae251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd67c99349a9dd8d6969f77ad77bcef8973454aaef7866b83cbafdb1f910373e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ff8d8d8847d25e22dcf954ed2d081d8df5d7a7e0dcbcaae865ff1eb7d36b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__653490b1d54e8d81dc6273b86d05ba938ce2ea4a1306422dd6a622e754dd8cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77df88b4d374230fe3956a4bb8171306d95712ac3bfeba26868c72fc3e3a33ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e956ec00d98d676117b691dcc01b800af283e2dc0450733e59b983af64602f7c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1ce8dee0d9ab99b8e56915636dd350f547085b115840017c3ff1f07d4991580)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec20b3c4570c3e23f7ca784575488e4d4d884ecef2ccba298c3f8c4bbdde6a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95b93b83996c07178772a2297b3ac3d0069805ac469bbb2a06fa4c0a1482731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d02538fe0a64ba0ce52b9ee9396e92f0fb95b756c33ec76ccbe12ee406277b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker",
    jsii_struct_bases=[],
    name_mapping={"dataset_name": "datasetName", "dataset_uuid": "datasetUuid"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker:
    def __init__(
        self,
        *,
        dataset_name: typing.Optional[builtins.str] = None,
        dataset_uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_name: Name of the dataset stored as metadata -> name on the dataset for Flocker should be considered as deprecated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#dataset_name DataKubernetesPersistentVolumeV1#dataset_name}
        :param dataset_uuid: UUID of the dataset. This is unique identifier of a Flocker dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#dataset_uuid DataKubernetesPersistentVolumeV1#dataset_uuid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241135ff2bb5ad6f59a42b4dd5a4b1f660a197bd421bf8a03554cad184dabe47)
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument dataset_uuid", value=dataset_uuid, expected_type=type_hints["dataset_uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if dataset_uuid is not None:
            self._values["dataset_uuid"] = dataset_uuid

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''Name of the dataset stored as metadata -> name on the dataset for Flocker should be considered as deprecated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#dataset_name DataKubernetesPersistentVolumeV1#dataset_name}
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataset_uuid(self) -> typing.Optional[builtins.str]:
        '''UUID of the dataset. This is unique identifier of a Flocker dataset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#dataset_uuid DataKubernetesPersistentVolumeV1#dataset_uuid}
        '''
        result = self._values.get("dataset_uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlockerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlockerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a080c95a88976cbadbf46a2200ef9b571d4d3268fbd61bb94960d5aa982ce6a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetName")
    def reset_dataset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetName", []))

    @jsii.member(jsii_name="resetDatasetUuid")
    def reset_dataset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetUuid", []))

    @builtins.property
    @jsii.member(jsii_name="datasetNameInput")
    def dataset_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetUuidInput")
    def dataset_uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetUuidInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetName")
    def dataset_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetName"))

    @dataset_name.setter
    def dataset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd7f05d49b356c4decd7431a3664bfe470717da31d8baf059641ec4dadaf5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datasetUuid")
    def dataset_uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetUuid"))

    @dataset_uuid.setter
    def dataset_uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88b9669cb416633613416311e1c79256d350ccf935c5f0d6edf473be2e81838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetUuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d307c877bddbb5d36f0e6798832e97f14257f11b999f73a03c5acd1ac7b3e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk",
    jsii_struct_bases=[],
    name_mapping={
        "pd_name": "pdName",
        "fs_type": "fsType",
        "partition": "partition",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk:
    def __init__(
        self,
        *,
        pd_name: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        partition: typing.Optional[jsii.Number] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pd_name: Unique name of the PD resource in GCE. Used to identify the disk in GCE. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#pd_name DataKubernetesPersistentVolumeV1#pd_name}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param partition: The partition in the volume that you want to mount. If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty). More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#partition DataKubernetesPersistentVolumeV1#partition}
        :param read_only: Whether to force the ReadOnly setting in VolumeMounts. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61629f288bf6e5ec05f93f237c1b0565e1c2d2ec867c0d97f38af3485c69be7)
            check_type(argname="argument pd_name", value=pd_name, expected_type=type_hints["pd_name"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pd_name": pd_name,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if partition is not None:
            self._values["partition"] = partition
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def pd_name(self) -> builtins.str:
        '''Unique name of the PD resource in GCE. Used to identify the disk in GCE. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#pd_name DataKubernetesPersistentVolumeV1#pd_name}
        '''
        result = self._values.get("pd_name")
        assert result is not None, "Required property 'pd_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type of the volume that you want to mount.

        Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[jsii.Number]:
        '''The partition in the volume that you want to mount.

        If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty). More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#partition DataKubernetesPersistentVolumeV1#partition}
        '''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the ReadOnly setting in VolumeMounts. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29f61d216dd662dbe04358f33fc85a887f262725ef9c3f275355afe6df3feff5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="pdNameInput")
    def pd_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pdNameInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c97a8efbec18d5af69d4c725f130a3ef49ace30c420ceda5ce12d46ec9cbb05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68fc75b4a03bdf7f61a53da7e259649fe7a29d705c2a1a92f3cbe80a81a0bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pdName")
    def pd_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pdName"))

    @pd_name.setter
    def pd_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d65aa3c74ceba7bf70ac97788f2cae5999f78f4cfab44bf7ceff4c5f25f2487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pdName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__bc6d52ec253230d19f5a990fd2a487c1b279d75724fd101952a7f19e10a1109c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7bc15f6e343b9c5ff581f49396554b6ab68b8b068ee0b90218ef6c1cd8ca6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints_name": "endpointsName",
        "path": "path",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs:
    def __init__(
        self,
        *,
        endpoints_name: builtins.str,
        path: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpoints_name: The endpoint name that details Glusterfs topology. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#endpoints_name DataKubernetesPersistentVolumeV1#endpoints_name}
        :param path: The Glusterfs volume path. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param read_only: Whether to force the Glusterfs volume to be mounted with read-only permissions. Defaults to false. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1541fce0f18550517d68cba9135421a31f2ed753c42c2b9264c0a2b689f46181)
            check_type(argname="argument endpoints_name", value=endpoints_name, expected_type=type_hints["endpoints_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints_name": endpoints_name,
            "path": path,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def endpoints_name(self) -> builtins.str:
        '''The endpoint name that details Glusterfs topology. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#endpoints_name DataKubernetesPersistentVolumeV1#endpoints_name}
        '''
        result = self._values.get("endpoints_name")
        assert result is not None, "Required property 'endpoints_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The Glusterfs volume path. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the Glusterfs volume to be mounted with read-only permissions. Defaults to false. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5affc8d4403e62a6bbd03149966da9fef908ad112ab992d5d6512ce434d697a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="endpointsNameInput")
    def endpoints_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsName")
    def endpoints_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointsName"))

    @endpoints_name.setter
    def endpoints_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0f22a59e831560fc7346a571951c58dddf23ff7bf56626d57c1956f5db2332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d4d900335869d10358ed92fac0251460b7a08e8d1c0fd6693ed278aee627fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1e79ada5d676b5e99c406fecc38e3c09466f5b8cec61fed9e12bbf1862b9dff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446d41d552ad146a5de9d618249f6d4e169dc260f709259c320b5a396661f2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "type": "type"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Path of the directory on the host. More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param type: Type for HostPath volume. Allowed values are "" (default), DirectoryOrCreate, Directory, FileOrCreate, File, Socket, CharDevice and BlockDevice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#type DataKubernetesPersistentVolumeV1#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfd95af06aa4a13b9c5d09e4e946a49cc62375767b6aa0333a9d83f2026f61e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path of the directory on the host. More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type for HostPath volume. Allowed values are "" (default), DirectoryOrCreate, Directory, FileOrCreate, File, Socket, CharDevice and BlockDevice.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#type DataKubernetesPersistentVolumeV1#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c32d2bf3e6f66f420bfaef475125a8f1550dfaeafe9378eb5e26166a5fb574a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9f6d704e30118d3ffcc085a1ea6c6a64be0502956b5c9ca65347e8a9dad26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3ea191affc8af59f194550817b22e4e2acc096084c6e93dceca790b50cc6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1abc781e3d008dbaec8612b21da0560db05834b094332312185f082aece4341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi",
    jsii_struct_bases=[],
    name_mapping={
        "iqn": "iqn",
        "target_portal": "targetPortal",
        "fs_type": "fsType",
        "iscsi_interface": "iscsiInterface",
        "lun": "lun",
        "read_only": "readOnly",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi:
    def __init__(
        self,
        *,
        iqn: builtins.str,
        target_portal: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        iscsi_interface: typing.Optional[builtins.str] = None,
        lun: typing.Optional[jsii.Number] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param iqn: Target iSCSI Qualified Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iqn DataKubernetesPersistentVolumeV1#iqn}
        :param target_portal: iSCSI target portal. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#target_portal DataKubernetesPersistentVolumeV1#target_portal}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param iscsi_interface: iSCSI interface name that uses an iSCSI transport. Defaults to 'default' (tcp). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iscsi_interface DataKubernetesPersistentVolumeV1#iscsi_interface}
        :param lun: iSCSI target lun number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#lun DataKubernetesPersistentVolumeV1#lun}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da9cf096e164f4eb98d40ad163ff5f8dda14bd73bdc9c0bc7d175db1828cd09)
            check_type(argname="argument iqn", value=iqn, expected_type=type_hints["iqn"])
            check_type(argname="argument target_portal", value=target_portal, expected_type=type_hints["target_portal"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument iscsi_interface", value=iscsi_interface, expected_type=type_hints["iscsi_interface"])
            check_type(argname="argument lun", value=lun, expected_type=type_hints["lun"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iqn": iqn,
            "target_portal": target_portal,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if iscsi_interface is not None:
            self._values["iscsi_interface"] = iscsi_interface
        if lun is not None:
            self._values["lun"] = lun
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def iqn(self) -> builtins.str:
        '''Target iSCSI Qualified Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iqn DataKubernetesPersistentVolumeV1#iqn}
        '''
        result = self._values.get("iqn")
        assert result is not None, "Required property 'iqn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_portal(self) -> builtins.str:
        '''iSCSI target portal.

        The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#target_portal DataKubernetesPersistentVolumeV1#target_portal}
        '''
        result = self._values.get("target_portal")
        assert result is not None, "Required property 'target_portal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type of the volume that you want to mount.

        Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iscsi_interface(self) -> typing.Optional[builtins.str]:
        '''iSCSI interface name that uses an iSCSI transport. Defaults to 'default' (tcp).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iscsi_interface DataKubernetesPersistentVolumeV1#iscsi_interface}
        '''
        result = self._values.get("iscsi_interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lun(self) -> typing.Optional[jsii.Number]:
        '''iSCSI target lun number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#lun DataKubernetesPersistentVolumeV1#lun}
        '''
        result = self._values.get("lun")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18b92a8f8bf1a28c25d7e3fb2905e25ea51ae8705777c55c79a98e9fea30f927)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetIscsiInterface")
    def reset_iscsi_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIscsiInterface", []))

    @jsii.member(jsii_name="resetLun")
    def reset_lun(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLun", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="iqnInput")
    def iqn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iqnInput"))

    @builtins.property
    @jsii.member(jsii_name="iscsiInterfaceInput")
    def iscsi_interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iscsiInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="lunInput")
    def lun_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lunInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPortalInput")
    def target_portal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPortalInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bdd042570b06f5010e5eb182f56fbdf1a7b96fae7a80317e69dde309e6c90a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iqn")
    def iqn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iqn"))

    @iqn.setter
    def iqn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8810f708dc057afc4ce3a8f0456339cff726bec6ea4b6335d7aba566d3477308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iqn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iscsiInterface")
    def iscsi_interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iscsiInterface"))

    @iscsi_interface.setter
    def iscsi_interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab9aa856115cf61b1ceaf96b740db9fd8f4c192e2aa3e84d9ca92e32835b8b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iscsiInterface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lun")
    def lun(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lun"))

    @lun.setter
    def lun(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4433697239e27173d53ee83ce9cd21e3ba920e3ec9fadfcb74c0d04e34967749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lun", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5c0c80051e1d14926dfe5d3239d9d3eb6bad523989bda589580a8b0724ad55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPortal")
    def target_portal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPortal"))

    @target_portal.setter
    def target_portal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131c3750a4d73dd861a8a90d5e2e91f4ae7215094142afd0c66530b53fda7083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPortal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fe99944dbd0b9d47ee485594cd193061ea688ead86555fcdbe3a5db8f3e2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal:
    def __init__(self, *, path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param path: Path of the directory on the host. More info: https://kubernetes.io/docs/concepts/storage/volumes#local. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65828e0e0f43df08e690982b7c21714add6ab55c3474e9f9d3dff4eb4783d604)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path of the directory on the host. More info: https://kubernetes.io/docs/concepts/storage/volumes#local.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c605afb2a44a1eca17e27d68bb27473c3ba448af9ce6340e4a19a38e289611)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfeeec763ce4322c1493b1bb9c8f6124d9079c731d2e48a8258eae3a0e094bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d3ee946a183172d4ceee9f40a07644f2df1d7b37ed9dcc7ff6f5b213700e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "server": "server", "read_only": "readOnly"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs:
    def __init__(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param server: Server is the hostname or IP address of the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#server DataKubernetesPersistentVolumeV1#server}
        :param read_only: Whether to force the NFS export to be mounted with read-only permissions. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132053ff7a234b35f793ad8c39c887a84f86d5b6fb236954f4d2d0dcd31295ef)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "server": server,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def path(self) -> builtins.str:
        '''Path that is exported by the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Server is the hostname or IP address of the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#server DataKubernetesPersistentVolumeV1#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the NFS export to be mounted with read-only permissions. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f35675634ec45a4234872e03b08489ab4b7d68b69aeb3eaa4bf618f844ac34d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64593791276c651e6f503043b53e4e621529504a5e28225c2a2f1eec3694e994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ad0f12735220504b093d57faedf3e4fb88c0b0abd1c5bea2cdbec071f51f1e4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10151930eb5ca30f66c061dc4428795990540a0faebb5540c8240d1353ea9f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d50d230acc72e0bd39d04e638c370c43e6d50a008ea9903f8953f5656f41e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f02bc26af73927534bc16682ff7c910b45a4ce70045f92c82974a52b6538fde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsElasticBlockStore")
    def put_aws_elastic_block_store(
        self,
        *,
        volume_id: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        partition: typing.Optional[jsii.Number] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param volume_id: Unique ID of the persistent disk resource in AWS (Amazon EBS volume). More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_id DataKubernetesPersistentVolumeV1#volume_id}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param partition: The partition in the volume that you want to mount. If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#partition DataKubernetesPersistentVolumeV1#partition}
        :param read_only: Whether to set the read-only property in VolumeMounts to "true". If omitted, the default is "false". More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore(
            volume_id=volume_id,
            fs_type=fs_type,
            partition=partition,
            read_only=read_only,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsElasticBlockStore", [value]))

    @jsii.member(jsii_name="putAzureDisk")
    def put_azure_disk(
        self,
        *,
        caching_mode: builtins.str,
        data_disk_uri: builtins.str,
        disk_name: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param caching_mode: Host Caching mode: None, Read Only, Read Write. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#caching_mode DataKubernetesPersistentVolumeV1#caching_mode}
        :param data_disk_uri: The URI the data disk in the blob storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#data_disk_uri DataKubernetesPersistentVolumeV1#data_disk_uri}
        :param disk_name: The Name of the data disk in the blob storage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#disk_name DataKubernetesPersistentVolumeV1#disk_name}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param kind: The type for the data disk. Expected values: Shared, Dedicated, Managed. Defaults to Shared. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#kind DataKubernetesPersistentVolumeV1#kind}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk(
            caching_mode=caching_mode,
            data_disk_uri=data_disk_uri,
            disk_name=disk_name,
            fs_type=fs_type,
            kind=kind,
            read_only=read_only,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureDisk", [value]))

    @jsii.member(jsii_name="putAzureFile")
    def put_azure_file(
        self,
        *,
        secret_name: builtins.str,
        share_name: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_name: The name of secret that contains Azure Storage Account Name and Key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_name DataKubernetesPersistentVolumeV1#secret_name}
        :param share_name: Share Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#share_name DataKubernetesPersistentVolumeV1#share_name}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_namespace: The namespace of the secret that contains Azure Storage Account Name and Key. For Kubernetes up to 1.18.x the default is the same as the Pod. For Kubernetes 1.19.x and later the default is "default" namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_namespace DataKubernetesPersistentVolumeV1#secret_namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile(
            secret_name=secret_name,
            share_name=share_name,
            read_only=read_only,
            secret_namespace=secret_namespace,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureFile", [value]))

    @jsii.member(jsii_name="putCephFs")
    def put_ceph_fs(
        self,
        *,
        monitors: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_file: typing.Optional[builtins.str] = None,
        secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param monitors: Monitors is a collection of Ceph monitors. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#monitors DataKubernetesPersistentVolumeV1#monitors}
        :param path: Used as the mounted root, rather than the full Ceph tree, default is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to ``false`` (read/write). More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_file: The path to key ring for User, default is ``/etc/ceph/user.secret``. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_file DataKubernetesPersistentVolumeV1#secret_file}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        :param user: User is the rados user name, default is admin. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#user DataKubernetesPersistentVolumeV1#user}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs(
            monitors=monitors,
            path=path,
            read_only=read_only,
            secret_file=secret_file,
            secret_ref=secret_ref,
            user=user,
        )

        return typing.cast(None, jsii.invoke(self, "putCephFs", [value]))

    @jsii.member(jsii_name="putCinder")
    def put_cinder(
        self,
        *,
        volume_id: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param volume_id: Volume ID used to identify the volume in Cinder. More info: https://examples.k8s.io/mysql-cinder-pd/README.md. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_id DataKubernetesPersistentVolumeV1#volume_id}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://examples.k8s.io/mysql-cinder-pd/README.md Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). More info: https://examples.k8s.io/mysql-cinder-pd/README.md. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder(
            volume_id=volume_id, fs_type=fs_type, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putCinder", [value]))

    @jsii.member(jsii_name="putCsi")
    def put_csi(
        self,
        *,
        driver: builtins.str,
        volume_handle: builtins.str,
        controller_expand_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
        controller_publish_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
        fs_type: typing.Optional[builtins.str] = None,
        node_publish_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
        node_stage_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver: the name of the volume driver to use. More info: https://kubernetes.io/docs/concepts/storage/volumes/#csi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#driver DataKubernetesPersistentVolumeV1#driver}
        :param volume_handle: A string value that uniquely identifies the volume. More info: https://kubernetes.io/docs/concepts/storage/volumes/#csi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_handle DataKubernetesPersistentVolumeV1#volume_handle}
        :param controller_expand_secret_ref: controller_expand_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#controller_expand_secret_ref DataKubernetesPersistentVolumeV1#controller_expand_secret_ref}
        :param controller_publish_secret_ref: controller_publish_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#controller_publish_secret_ref DataKubernetesPersistentVolumeV1#controller_publish_secret_ref}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param node_publish_secret_ref: node_publish_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_publish_secret_ref DataKubernetesPersistentVolumeV1#node_publish_secret_ref}
        :param node_stage_secret_ref: node_stage_secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#node_stage_secret_ref DataKubernetesPersistentVolumeV1#node_stage_secret_ref}
        :param read_only: Whether to set the read-only property in VolumeMounts to "true". If omitted, the default is "false". More info: https://kubernetes.io/docs/concepts/storage/volumes#csi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param volume_attributes: Attributes of the volume to publish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_attributes DataKubernetesPersistentVolumeV1#volume_attributes}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi(
            driver=driver,
            volume_handle=volume_handle,
            controller_expand_secret_ref=controller_expand_secret_ref,
            controller_publish_secret_ref=controller_publish_secret_ref,
            fs_type=fs_type,
            node_publish_secret_ref=node_publish_secret_ref,
            node_stage_secret_ref=node_stage_secret_ref,
            read_only=read_only,
            volume_attributes=volume_attributes,
        )

        return typing.cast(None, jsii.invoke(self, "putCsi", [value]))

    @jsii.member(jsii_name="putFc")
    def put_fc(
        self,
        *,
        lun: jsii.Number,
        target_ww_ns: typing.Sequence[builtins.str],
        fs_type: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param lun: FC target lun number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#lun DataKubernetesPersistentVolumeV1#lun}
        :param target_ww_ns: FC target worldwide names (WWNs). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#target_ww_ns DataKubernetesPersistentVolumeV1#target_ww_ns}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc(
            lun=lun, target_ww_ns=target_ww_ns, fs_type=fs_type, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putFc", [value]))

    @jsii.member(jsii_name="putFlexVolume")
    def put_flex_volume(
        self,
        *,
        driver: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param driver: Driver is the name of the driver to use for this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#driver DataKubernetesPersistentVolumeV1#driver}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem depends on FlexVolume script. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param options: Extra command options if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#options DataKubernetesPersistentVolumeV1#options}
        :param read_only: Whether to force the ReadOnly setting in VolumeMounts. Defaults to false (read/write). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume(
            driver=driver,
            fs_type=fs_type,
            options=options,
            read_only=read_only,
            secret_ref=secret_ref,
        )

        return typing.cast(None, jsii.invoke(self, "putFlexVolume", [value]))

    @jsii.member(jsii_name="putFlocker")
    def put_flocker(
        self,
        *,
        dataset_name: typing.Optional[builtins.str] = None,
        dataset_uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_name: Name of the dataset stored as metadata -> name on the dataset for Flocker should be considered as deprecated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#dataset_name DataKubernetesPersistentVolumeV1#dataset_name}
        :param dataset_uuid: UUID of the dataset. This is unique identifier of a Flocker dataset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#dataset_uuid DataKubernetesPersistentVolumeV1#dataset_uuid}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker(
            dataset_name=dataset_name, dataset_uuid=dataset_uuid
        )

        return typing.cast(None, jsii.invoke(self, "putFlocker", [value]))

    @jsii.member(jsii_name="putGcePersistentDisk")
    def put_gce_persistent_disk(
        self,
        *,
        pd_name: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        partition: typing.Optional[jsii.Number] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pd_name: Unique name of the PD resource in GCE. Used to identify the disk in GCE. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#pd_name DataKubernetesPersistentVolumeV1#pd_name}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param partition: The partition in the volume that you want to mount. If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty). More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#partition DataKubernetesPersistentVolumeV1#partition}
        :param read_only: Whether to force the ReadOnly setting in VolumeMounts. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk(
            pd_name=pd_name, fs_type=fs_type, partition=partition, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putGcePersistentDisk", [value]))

    @jsii.member(jsii_name="putGlusterfs")
    def put_glusterfs(
        self,
        *,
        endpoints_name: builtins.str,
        path: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpoints_name: The endpoint name that details Glusterfs topology. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#endpoints_name DataKubernetesPersistentVolumeV1#endpoints_name}
        :param path: The Glusterfs volume path. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param read_only: Whether to force the Glusterfs volume to be mounted with read-only permissions. Defaults to false. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs(
            endpoints_name=endpoints_name, path=path, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putGlusterfs", [value]))

    @jsii.member(jsii_name="putHostPath")
    def put_host_path(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Path of the directory on the host. More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param type: Type for HostPath volume. Allowed values are "" (default), DirectoryOrCreate, Directory, FileOrCreate, File, Socket, CharDevice and BlockDevice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#type DataKubernetesPersistentVolumeV1#type}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath(
            path=path, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putHostPath", [value]))

    @jsii.member(jsii_name="putIscsi")
    def put_iscsi(
        self,
        *,
        iqn: builtins.str,
        target_portal: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        iscsi_interface: typing.Optional[builtins.str] = None,
        lun: typing.Optional[jsii.Number] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param iqn: Target iSCSI Qualified Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iqn DataKubernetesPersistentVolumeV1#iqn}
        :param target_portal: iSCSI target portal. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#target_portal DataKubernetesPersistentVolumeV1#target_portal}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param iscsi_interface: iSCSI interface name that uses an iSCSI transport. Defaults to 'default' (tcp). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#iscsi_interface DataKubernetesPersistentVolumeV1#iscsi_interface}
        :param lun: iSCSI target lun number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#lun DataKubernetesPersistentVolumeV1#lun}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi(
            iqn=iqn,
            target_portal=target_portal,
            fs_type=fs_type,
            iscsi_interface=iscsi_interface,
            lun=lun,
            read_only=read_only,
        )

        return typing.cast(None, jsii.invoke(self, "putIscsi", [value]))

    @jsii.member(jsii_name="putLocal")
    def put_local(self, *, path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param path: Path of the directory on the host. More info: https://kubernetes.io/docs/concepts/storage/volumes#local. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal(
            path=path
        )

        return typing.cast(None, jsii.invoke(self, "putLocal", [value]))

    @jsii.member(jsii_name="putNfs")
    def put_nfs(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#path DataKubernetesPersistentVolumeV1#path}
        :param server: Server is the hostname or IP address of the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#server DataKubernetesPersistentVolumeV1#server}
        :param read_only: Whether to force the NFS export to be mounted with read-only permissions. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs(
            path=path, server=server, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putPhotonPersistentDisk")
    def put_photon_persistent_disk(
        self,
        *,
        pd_id: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pd_id: ID that identifies Photon Controller persistent disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#pd_id DataKubernetesPersistentVolumeV1#pd_id}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk(
            pd_id=pd_id, fs_type=fs_type
        )

        return typing.cast(None, jsii.invoke(self, "putPhotonPersistentDisk", [value]))

    @jsii.member(jsii_name="putQuobyte")
    def put_quobyte(
        self,
        *,
        registry: builtins.str,
        volume: builtins.str,
        group: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param registry: Registry represents a single or multiple Quobyte Registry services specified as a string as host:port pair (multiple entries are separated with commas) which acts as the central registry for volumes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#registry DataKubernetesPersistentVolumeV1#registry}
        :param volume: Volume is a string that references an already created Quobyte volume by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume DataKubernetesPersistentVolumeV1#volume}
        :param group: Group to map volume access to Default is no group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#group DataKubernetesPersistentVolumeV1#group}
        :param read_only: Whether to force the Quobyte volume to be mounted with read-only permissions. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param user: User to map volume access to Defaults to serivceaccount user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#user DataKubernetesPersistentVolumeV1#user}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte(
            registry=registry,
            volume=volume,
            group=group,
            read_only=read_only,
            user=user,
        )

        return typing.cast(None, jsii.invoke(self, "putQuobyte", [value]))

    @jsii.member(jsii_name="putRbd")
    def put_rbd(
        self,
        *,
        ceph_monitors: typing.Sequence[builtins.str],
        rbd_image: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        keyring: typing.Optional[builtins.str] = None,
        rados_user: typing.Optional[builtins.str] = None,
        rbd_pool: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ceph_monitors: A collection of Ceph monitors. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#ceph_monitors DataKubernetesPersistentVolumeV1#ceph_monitors}
        :param rbd_image: The rados image name. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd_image DataKubernetesPersistentVolumeV1#rbd_image}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#rbd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param keyring: Keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#keyring DataKubernetesPersistentVolumeV1#keyring}
        :param rados_user: The rados user name. Default is admin. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rados_user DataKubernetesPersistentVolumeV1#rados_user}
        :param rbd_pool: The rados pool name. Default is rbd. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd_pool DataKubernetesPersistentVolumeV1#rbd_pool}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd(
            ceph_monitors=ceph_monitors,
            rbd_image=rbd_image,
            fs_type=fs_type,
            keyring=keyring,
            rados_user=rados_user,
            rbd_pool=rbd_pool,
            read_only=read_only,
            secret_ref=secret_ref,
        )

        return typing.cast(None, jsii.invoke(self, "putRbd", [value]))

    @jsii.member(jsii_name="putVsphereVolume")
    def put_vsphere_volume(
        self,
        *,
        volume_path: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param volume_path: Path that identifies vSphere volume vmdk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_path DataKubernetesPersistentVolumeV1#volume_path}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume(
            volume_path=volume_path, fs_type=fs_type
        )

        return typing.cast(None, jsii.invoke(self, "putVsphereVolume", [value]))

    @jsii.member(jsii_name="resetAwsElasticBlockStore")
    def reset_aws_elastic_block_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsElasticBlockStore", []))

    @jsii.member(jsii_name="resetAzureDisk")
    def reset_azure_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureDisk", []))

    @jsii.member(jsii_name="resetAzureFile")
    def reset_azure_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureFile", []))

    @jsii.member(jsii_name="resetCephFs")
    def reset_ceph_fs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCephFs", []))

    @jsii.member(jsii_name="resetCinder")
    def reset_cinder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCinder", []))

    @jsii.member(jsii_name="resetCsi")
    def reset_csi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsi", []))

    @jsii.member(jsii_name="resetFc")
    def reset_fc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFc", []))

    @jsii.member(jsii_name="resetFlexVolume")
    def reset_flex_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexVolume", []))

    @jsii.member(jsii_name="resetFlocker")
    def reset_flocker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlocker", []))

    @jsii.member(jsii_name="resetGcePersistentDisk")
    def reset_gce_persistent_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcePersistentDisk", []))

    @jsii.member(jsii_name="resetGlusterfs")
    def reset_glusterfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlusterfs", []))

    @jsii.member(jsii_name="resetHostPath")
    def reset_host_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPath", []))

    @jsii.member(jsii_name="resetIscsi")
    def reset_iscsi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIscsi", []))

    @jsii.member(jsii_name="resetLocal")
    def reset_local(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocal", []))

    @jsii.member(jsii_name="resetNfs")
    def reset_nfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfs", []))

    @jsii.member(jsii_name="resetPhotonPersistentDisk")
    def reset_photon_persistent_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhotonPersistentDisk", []))

    @jsii.member(jsii_name="resetQuobyte")
    def reset_quobyte(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuobyte", []))

    @jsii.member(jsii_name="resetRbd")
    def reset_rbd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRbd", []))

    @jsii.member(jsii_name="resetVsphereVolume")
    def reset_vsphere_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsphereVolume", []))

    @builtins.property
    @jsii.member(jsii_name="awsElasticBlockStore")
    def aws_elastic_block_store(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStoreOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStoreOutputReference, jsii.get(self, "awsElasticBlockStore"))

    @builtins.property
    @jsii.member(jsii_name="azureDisk")
    def azure_disk(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDiskOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDiskOutputReference, jsii.get(self, "azureDisk"))

    @builtins.property
    @jsii.member(jsii_name="azureFile")
    def azure_file(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFileOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFileOutputReference, jsii.get(self, "azureFile"))

    @builtins.property
    @jsii.member(jsii_name="cephFs")
    def ceph_fs(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsOutputReference, jsii.get(self, "cephFs"))

    @builtins.property
    @jsii.member(jsii_name="cinder")
    def cinder(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinderOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinderOutputReference, jsii.get(self, "cinder"))

    @builtins.property
    @jsii.member(jsii_name="csi")
    def csi(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiOutputReference, jsii.get(self, "csi"))

    @builtins.property
    @jsii.member(jsii_name="fc")
    def fc(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFcOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFcOutputReference, jsii.get(self, "fc"))

    @builtins.property
    @jsii.member(jsii_name="flexVolume")
    def flex_volume(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeOutputReference, jsii.get(self, "flexVolume"))

    @builtins.property
    @jsii.member(jsii_name="flocker")
    def flocker(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlockerOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlockerOutputReference, jsii.get(self, "flocker"))

    @builtins.property
    @jsii.member(jsii_name="gcePersistentDisk")
    def gce_persistent_disk(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDiskOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDiskOutputReference, jsii.get(self, "gcePersistentDisk"))

    @builtins.property
    @jsii.member(jsii_name="glusterfs")
    def glusterfs(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfsOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfsOutputReference, jsii.get(self, "glusterfs"))

    @builtins.property
    @jsii.member(jsii_name="hostPath")
    def host_path(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPathOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPathOutputReference, jsii.get(self, "hostPath"))

    @builtins.property
    @jsii.member(jsii_name="iscsi")
    def iscsi(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsiOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsiOutputReference, jsii.get(self, "iscsi"))

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocalOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocalOutputReference, jsii.get(self, "local"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(
        self,
    ) -> DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfsOutputReference:
        return typing.cast(DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="photonPersistentDisk")
    def photon_persistent_disk(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDiskOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDiskOutputReference", jsii.get(self, "photonPersistentDisk"))

    @builtins.property
    @jsii.member(jsii_name="quobyte")
    def quobyte(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyteOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyteOutputReference", jsii.get(self, "quobyte"))

    @builtins.property
    @jsii.member(jsii_name="rbd")
    def rbd(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdOutputReference", jsii.get(self, "rbd"))

    @builtins.property
    @jsii.member(jsii_name="vsphereVolume")
    def vsphere_volume(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolumeOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolumeOutputReference", jsii.get(self, "vsphereVolume"))

    @builtins.property
    @jsii.member(jsii_name="awsElasticBlockStoreInput")
    def aws_elastic_block_store_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore], jsii.get(self, "awsElasticBlockStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="azureDiskInput")
    def azure_disk_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk], jsii.get(self, "azureDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFileInput")
    def azure_file_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile], jsii.get(self, "azureFileInput"))

    @builtins.property
    @jsii.member(jsii_name="cephFsInput")
    def ceph_fs_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs], jsii.get(self, "cephFsInput"))

    @builtins.property
    @jsii.member(jsii_name="cinderInput")
    def cinder_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder], jsii.get(self, "cinderInput"))

    @builtins.property
    @jsii.member(jsii_name="csiInput")
    def csi_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi], jsii.get(self, "csiInput"))

    @builtins.property
    @jsii.member(jsii_name="fcInput")
    def fc_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc], jsii.get(self, "fcInput"))

    @builtins.property
    @jsii.member(jsii_name="flexVolumeInput")
    def flex_volume_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume], jsii.get(self, "flexVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="flockerInput")
    def flocker_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker], jsii.get(self, "flockerInput"))

    @builtins.property
    @jsii.member(jsii_name="gcePersistentDiskInput")
    def gce_persistent_disk_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk], jsii.get(self, "gcePersistentDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="glusterfsInput")
    def glusterfs_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs], jsii.get(self, "glusterfsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPathInput")
    def host_path_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath], jsii.get(self, "hostPathInput"))

    @builtins.property
    @jsii.member(jsii_name="iscsiInput")
    def iscsi_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi], jsii.get(self, "iscsiInput"))

    @builtins.property
    @jsii.member(jsii_name="localInput")
    def local_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal], jsii.get(self, "localInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="photonPersistentDiskInput")
    def photon_persistent_disk_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk"], jsii.get(self, "photonPersistentDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="quobyteInput")
    def quobyte_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte"], jsii.get(self, "quobyteInput"))

    @builtins.property
    @jsii.member(jsii_name="rbdInput")
    def rbd_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd"], jsii.get(self, "rbdInput"))

    @builtins.property
    @jsii.member(jsii_name="vsphereVolumeInput")
    def vsphere_volume_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume"], jsii.get(self, "vsphereVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac340614a27dbb7a93dcb021302b48dce5b8a40beb7a6c4932fabf4e6d6c3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk",
    jsii_struct_bases=[],
    name_mapping={"pd_id": "pdId", "fs_type": "fsType"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk:
    def __init__(
        self,
        *,
        pd_id: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pd_id: ID that identifies Photon Controller persistent disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#pd_id DataKubernetesPersistentVolumeV1#pd_id}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f67052ff63203c7fa4ae94c24e9486cd0f37bc5c31847db9de98523cc7d8994)
            check_type(argname="argument pd_id", value=pd_id, expected_type=type_hints["pd_id"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pd_id": pd_id,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type

    @builtins.property
    def pd_id(self) -> builtins.str:
        '''ID that identifies Photon Controller persistent disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#pd_id DataKubernetesPersistentVolumeV1#pd_id}
        '''
        result = self._values.get("pd_id")
        assert result is not None, "Required property 'pd_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6be27d3988cb2904664fca67af9241df9094a1774cba5f32a3e7ff18f949b7e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="pdIdInput")
    def pd_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pdIdInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48019b13d2fdb5ada57fe319d075f6d9b4b1308fddf3b7990b4ed6f0e3522cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pdId")
    def pd_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pdId"))

    @pd_id.setter
    def pd_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a94453fef26e52533cf03d68cae2fb6518bda4b35df95da2610b07e968f8e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pdId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fa1da91d7aae82983a4f2c21bd39fdb7f2d97c303a126e6c52079c7f934940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte",
    jsii_struct_bases=[],
    name_mapping={
        "registry": "registry",
        "volume": "volume",
        "group": "group",
        "read_only": "readOnly",
        "user": "user",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte:
    def __init__(
        self,
        *,
        registry: builtins.str,
        volume: builtins.str,
        group: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param registry: Registry represents a single or multiple Quobyte Registry services specified as a string as host:port pair (multiple entries are separated with commas) which acts as the central registry for volumes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#registry DataKubernetesPersistentVolumeV1#registry}
        :param volume: Volume is a string that references an already created Quobyte volume by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume DataKubernetesPersistentVolumeV1#volume}
        :param group: Group to map volume access to Default is no group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#group DataKubernetesPersistentVolumeV1#group}
        :param read_only: Whether to force the Quobyte volume to be mounted with read-only permissions. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param user: User to map volume access to Defaults to serivceaccount user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#user DataKubernetesPersistentVolumeV1#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb38965a1220d0cca97da4cfb0efcff00a02dae3b7ed60645ec9779543de4e3)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "registry": registry,
            "volume": volume,
        }
        if group is not None:
            self._values["group"] = group
        if read_only is not None:
            self._values["read_only"] = read_only
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def registry(self) -> builtins.str:
        '''Registry represents a single or multiple Quobyte Registry services specified as a string as host:port pair (multiple entries are separated with commas) which acts as the central registry for volumes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#registry DataKubernetesPersistentVolumeV1#registry}
        '''
        result = self._values.get("registry")
        assert result is not None, "Required property 'registry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume(self) -> builtins.str:
        '''Volume is a string that references an already created Quobyte volume by name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume DataKubernetesPersistentVolumeV1#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Group to map volume access to Default is no group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#group DataKubernetesPersistentVolumeV1#group}
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the Quobyte volume to be mounted with read-only permissions. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''User to map volume access to Defaults to serivceaccount user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#user DataKubernetesPersistentVolumeV1#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__466ab7e5050bf929696b329f11c41d99188e6fd5295346856370bb5e6fda74b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="registryInput")
    def registry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f8d88c069f64f4b9c25a8ebca33edee9336c13cf9c43a4701c95bedc364d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__8dacaa9a8a0903205e7683c5f5ff5259ace2fa86aff61d24f54da7a0d926beb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f762d82aff49c708a66282a78a26d09786fbb7b27a8e6dce7b72808437751509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beefa9cc9b8f33fafd43c82ef7b253dc6220bdcce7e37a2dcc9876ea60a07dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volume"))

    @volume.setter
    def volume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86509090784fae12b08b034337fa384c0187e02cb693909777c2c2ee464f0dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be9162c6edd0832aae93cc789d263bfe59af2a79a8eff5589638bc5b9905677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd",
    jsii_struct_bases=[],
    name_mapping={
        "ceph_monitors": "cephMonitors",
        "rbd_image": "rbdImage",
        "fs_type": "fsType",
        "keyring": "keyring",
        "rados_user": "radosUser",
        "rbd_pool": "rbdPool",
        "read_only": "readOnly",
        "secret_ref": "secretRef",
    },
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd:
    def __init__(
        self,
        *,
        ceph_monitors: typing.Sequence[builtins.str],
        rbd_image: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
        keyring: typing.Optional[builtins.str] = None,
        rados_user: typing.Optional[builtins.str] = None,
        rbd_pool: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_ref: typing.Optional[typing.Union["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ceph_monitors: A collection of Ceph monitors. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#ceph_monitors DataKubernetesPersistentVolumeV1#ceph_monitors}
        :param rbd_image: The rados image name. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd_image DataKubernetesPersistentVolumeV1#rbd_image}
        :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#rbd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        :param keyring: Keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#keyring DataKubernetesPersistentVolumeV1#keyring}
        :param rados_user: The rados user name. Default is admin. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rados_user DataKubernetesPersistentVolumeV1#rados_user}
        :param rbd_pool: The rados pool name. Default is rbd. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd_pool DataKubernetesPersistentVolumeV1#rbd_pool}
        :param read_only: Whether to force the read-only setting in VolumeMounts. Defaults to false. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        if isinstance(secret_ref, dict):
            secret_ref = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef(**secret_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7348ba12c0ea9b812c243dcf917bd59bf6435b8030a538b3101ca9051d0e5130)
            check_type(argname="argument ceph_monitors", value=ceph_monitors, expected_type=type_hints["ceph_monitors"])
            check_type(argname="argument rbd_image", value=rbd_image, expected_type=type_hints["rbd_image"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument keyring", value=keyring, expected_type=type_hints["keyring"])
            check_type(argname="argument rados_user", value=rados_user, expected_type=type_hints["rados_user"])
            check_type(argname="argument rbd_pool", value=rbd_pool, expected_type=type_hints["rbd_pool"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument secret_ref", value=secret_ref, expected_type=type_hints["secret_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ceph_monitors": ceph_monitors,
            "rbd_image": rbd_image,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if keyring is not None:
            self._values["keyring"] = keyring
        if rados_user is not None:
            self._values["rados_user"] = rados_user
        if rbd_pool is not None:
            self._values["rbd_pool"] = rbd_pool
        if read_only is not None:
            self._values["read_only"] = read_only
        if secret_ref is not None:
            self._values["secret_ref"] = secret_ref

    @builtins.property
    def ceph_monitors(self) -> typing.List[builtins.str]:
        '''A collection of Ceph monitors. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#ceph_monitors DataKubernetesPersistentVolumeV1#ceph_monitors}
        '''
        result = self._values.get("ceph_monitors")
        assert result is not None, "Required property 'ceph_monitors' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def rbd_image(self) -> builtins.str:
        '''The rados image name. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd_image DataKubernetesPersistentVolumeV1#rbd_image}
        '''
        result = self._values.get("rbd_image")
        assert result is not None, "Required property 'rbd_image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type of the volume that you want to mount.

        Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#rbd

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keyring(self) -> typing.Optional[builtins.str]:
        '''Keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#keyring DataKubernetesPersistentVolumeV1#keyring}
        '''
        result = self._values.get("keyring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rados_user(self) -> typing.Optional[builtins.str]:
        '''The rados user name. Default is admin. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rados_user DataKubernetesPersistentVolumeV1#rados_user}
        '''
        result = self._values.get("rados_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rbd_pool(self) -> typing.Optional[builtins.str]:
        '''The rados pool name. Default is rbd. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#rbd_pool DataKubernetesPersistentVolumeV1#rbd_pool}
        '''
        result = self._values.get("rbd_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force the read-only setting in VolumeMounts. Defaults to false. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#read_only DataKubernetesPersistentVolumeV1#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_ref(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef"]:
        '''secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#secret_ref DataKubernetesPersistentVolumeV1#secret_ref}
        '''
        result = self._values.get("secret_ref")
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a71718d00f500aca2096c7726544e2d2618d78ae8d64aca2a210e202c6235708)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretRef")
    def put_secret_ref(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        value = DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef(
            name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putSecretRef", [value]))

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetKeyring")
    def reset_keyring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyring", []))

    @jsii.member(jsii_name="resetRadosUser")
    def reset_rados_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRadosUser", []))

    @jsii.member(jsii_name="resetRbdPool")
    def reset_rbd_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRbdPool", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSecretRef")
    def reset_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretRef", []))

    @builtins.property
    @jsii.member(jsii_name="secretRef")
    def secret_ref(
        self,
    ) -> "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRefOutputReference":
        return typing.cast("DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRefOutputReference", jsii.get(self, "secretRef"))

    @builtins.property
    @jsii.member(jsii_name="cephMonitorsInput")
    def ceph_monitors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cephMonitorsInput"))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyringInput")
    def keyring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyringInput"))

    @builtins.property
    @jsii.member(jsii_name="radosUserInput")
    def rados_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "radosUserInput"))

    @builtins.property
    @jsii.member(jsii_name="rbdImageInput")
    def rbd_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rbdImageInput"))

    @builtins.property
    @jsii.member(jsii_name="rbdPoolInput")
    def rbd_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rbdPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRefInput")
    def secret_ref_input(
        self,
    ) -> typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef"]:
        return typing.cast(typing.Optional["DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef"], jsii.get(self, "secretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="cephMonitors")
    def ceph_monitors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cephMonitors"))

    @ceph_monitors.setter
    def ceph_monitors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8aa4c921d9d7c8fe2a3933b8b3310b31a12f97dc51a49b4b083b35d494cd571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cephMonitors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c5f398366fa7792a5c815d98067e2f0b5ee2c86cb2e698b345a141ba2afcff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyring")
    def keyring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyring"))

    @keyring.setter
    def keyring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec00fb4a5c750ea0d770b8bcef23ee02b914b8b1a4fb8ede7234d005e2e7bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="radosUser")
    def rados_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "radosUser"))

    @rados_user.setter
    def rados_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839a792c3ac0646ab8cd7a2c2fa7f33ca50bbf0ff4271e31d46cd8317e86be38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "radosUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rbdImage")
    def rbd_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rbdImage"))

    @rbd_image.setter
    def rbd_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b025c5433aaf4335144ec9581f587bdf36e79ce92721e9be42f684aee3329392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rbdImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rbdPool")
    def rbd_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rbdPool"))

    @rbd_pool.setter
    def rbd_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9702eb9fe20cdede17bd0ae148900c9e1b2f0e9b9cf43ba65fb3bab38b9b6c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rbdPool", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9c472670073d335a309f54a7eac69f3754f8c1959673e0f1b77a64a35b3141d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724729284948a2aedf626fc37656848b54f946e95bcbf1590a16afc3dde5d151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        :param namespace: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d36a19a54faa909d32ae97da09627cadeae6ad6c65ee2d597a4319305dc1e8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#name DataKubernetesPersistentVolumeV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#namespace DataKubernetesPersistentVolumeV1#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__374fbac5be799075d48f8aacfcd107346bb6db41fe3159ec36ba33085398e2e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1db1875e1a59b28571613f1a34bf36c6f34ab0faf28e64442fb5e8b19c994589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae41f75612b93c7207eeb7ae17cecb19c77ccd8a70db99eaf7368669e9dbddc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62215320e89864f6d050a55e62f27d6f969ff9e2f3f87827eb30722754d3e676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume",
    jsii_struct_bases=[],
    name_mapping={"volume_path": "volumePath", "fs_type": "fsType"},
)
class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume:
    def __init__(
        self,
        *,
        volume_path: builtins.str,
        fs_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param volume_path: Path that identifies vSphere volume vmdk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_path DataKubernetesPersistentVolumeV1#volume_path}
        :param fs_type: Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd86bd32e5a70ff3324c9ecc2ad928b21c54187387768279869aa5fd4d597576)
            check_type(argname="argument volume_path", value=volume_path, expected_type=type_hints["volume_path"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "volume_path": volume_path,
        }
        if fs_type is not None:
            self._values["fs_type"] = fs_type

    @builtins.property
    def volume_path(self) -> builtins.str:
        '''Path that identifies vSphere volume vmdk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#volume_path DataKubernetesPersistentVolumeV1#volume_path}
        '''
        result = self._values.get("volume_path")
        assert result is not None, "Required property 'volume_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Filesystem type to mount.

        Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/data-sources/persistent_volume_v1#fs_type DataKubernetesPersistentVolumeV1#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.dataKubernetesPersistentVolumeV1.DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be9b9567bc8f389a8c354b98d896d48acc02d5573d4a6dc577ca1d21f71dd814)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumePathInput")
    def volume_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumePathInput"))

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ace705aacd552af3304e8e0b56f303d287b08ee5d0d6a88aab19dc1eafe5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumePath")
    def volume_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumePath"))

    @volume_path.setter
    def volume_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0febdccd780dcb12040bd843e87565b0ac9fc8ae85353144b3cb30d8fd604739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume]:
        return typing.cast(typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22ce9d5b750b5613c596a5da94c33d6e24b6eea6b4273d5a504fbf7b3e5e828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataKubernetesPersistentVolumeV1",
    "DataKubernetesPersistentVolumeV1Config",
    "DataKubernetesPersistentVolumeV1Metadata",
    "DataKubernetesPersistentVolumeV1MetadataOutputReference",
    "DataKubernetesPersistentVolumeV1Spec",
    "DataKubernetesPersistentVolumeV1SpecClaimRef",
    "DataKubernetesPersistentVolumeV1SpecClaimRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecList",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinity",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityOutputReference",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermList",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsList",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressionsOutputReference",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsList",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFieldsOutputReference",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermOutputReference",
    "DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredOutputReference",
    "DataKubernetesPersistentVolumeV1SpecOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStoreOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDiskOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFileOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinderOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFcOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlockerOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDiskOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfsOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPathOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsiOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocalOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfsOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDiskOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyteOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRefOutputReference",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume",
    "DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolumeOutputReference",
]

publication.publish()

def _typecheckingstub__1c9ffaf6cb94dce91e6459fcbba68ba3d5f7cb5d565e378d4ccf2116f33e49a6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[DataKubernetesPersistentVolumeV1Metadata, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1Spec, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__1545bd34be77b630804ae9731919ef969728efaa37466e9734907d41356486f5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1725a422ef86afb5301d76e51007a3ba6e36b45ededf99d83a57198f94c43840(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1Spec, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6483c21e2760d3269825500f39cd0b3477e7a8a762d00736ae77a65332ba7cd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b201aff73105553daeef85d16c39b40f44eb9508bf652eab540a9fc332d10c28(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[DataKubernetesPersistentVolumeV1Metadata, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1Spec, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a34e5b63d39d3bedd73559d9d4936156123fef99042a05acc76afa464dfc21b(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed075b8191e8388fd399eafeb4f69c919b8724d768574f7442397b8a9511795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f95016b039c12d1f51aa71a6dc454ec49921f96b7296e8a0b2f06de9e8c009e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168d7cdd09c238ebfac189fc572bfbe14d8dc7bb5413cb92c9876a21ecadf4d6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53951c75a7c18aa19aaf15b7fd9d6956468ffea84a07158137aaea4fce7b496c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71bacf809bb13bf8e466c45ad175c09e1e7606d4c5bdc9314b00e17c4429800(
    value: typing.Optional[DataKubernetesPersistentVolumeV1Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f9741d4180b052d476cc5a4fb76d434d76a261a85f89912ecbdcd12eb50517(
    *,
    access_modes: typing.Sequence[builtins.str],
    capacity: typing.Mapping[builtins.str, builtins.str],
    persistent_volume_source: typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource, typing.Dict[builtins.str, typing.Any]],
    claim_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecClaimRef, typing.Dict[builtins.str, typing.Any]]] = None,
    mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    node_affinity: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    persistent_volume_reclaim_policy: typing.Optional[builtins.str] = None,
    storage_class_name: typing.Optional[builtins.str] = None,
    volume_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30ea2ab52ed466346c9ae5acd52bf7c5c5ecfc40370ea0623896cef9b68e369(
    *,
    name: builtins.str,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57565dec968d139d95bdc509eb108849c118099b20387e2a1eb65567a82692a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2623d708d1a2355c4b01ddb0127fbff7ea74ada28f815e7d014808b54a26369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3541486920026c73bd49688ad968527d2f76eddd5bdbd445845318fa8ea76b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2713f6c2ce4fa4fe183aef98dd298cad2b8c57d9e782c4816d52588be824471c(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecClaimRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64bffde9043c93b58ac9a862855e31988f8d3d5c7a65aa64903ac2063a4b1b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec77bf34026facb2ddc734629b5b503518e824d04487fa3c0c02e757cd0090c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad3150bf1180d01ca8783a5db901611621d91cee86f51f40d8f5227f2062d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a113ed275519eecf684312b0c144f059d2a4f540d318c569b607559ff8af275(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045a509b219d948f16677ee65b1a58963ca4ee09d1dff977b8faeeb77fafb50a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a29d7f26db8f6f7d08dd5e0d05a980d50afd8ccb92e37838334158ae5bbdde4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1Spec]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84feb2bd0dd4a0039c3b88fd143c944af37f68b8b5b15fd6e24dcc2eb4afc1bc(
    *,
    required: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbf759135a4cd85c80d93f8ae3a1caf62d3fcb50c6db4893779c9c1644d335a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dc2df57a2a63098b0ac22f052f660531e52a66d1722454c7e71e47df3d1168(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f2e8e1e9b93047ac9e62c842f016cf62ef317c951b31548c725b5153715209(
    *,
    node_selector_term: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119915a20c24a51ec3c06e5b8b86d98927bc84005f8df50071ce2897985a9ea0(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5934052119272406687894391833dc80e9507e453798ff1d112b296f3898e49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7545b6463c29ceb0a104bda4f9b2a0f89f431f2093cd61d72f59be98d96026d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08b1e55d806307e2f8037e41d124865074943aa64b73d14332f9ad0cb0e4380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4406da5391b94ddb17101b42f59af491a05a0db80f76dfd5aa3077ed0eaba8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d81ef7aadf6020454fc0fcfd513b69ca5766cac49ccd0aa0061d8b7bfbd57e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f910779aa267549e92521dc6ea6a94b8fe68a71fa6445ea57ca4f724be3454d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba328d9664d34c29b31be02c99f7fe36341b7a12539928440c35e6104225ee1(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f318299747cc704553383de0e58de86a05f5483e8e516f7fbb01f63a459e0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de49aeb62b0d696d108551288fdac4c15ac6bae88bcf07c293f407e6281848ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef0f213af551aae758e708fd74f99d2f3a49647276bbe79d18cb47f4abfac24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60c5f0e0d01379117a9c91f1c20e396a2689d9526ede41efe6c731131cb2779(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1723c5e87abfc8a1625348af8c6239194b9fda17ac99dc9c618a57de23752c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc266cecfa139bdee5b67356f4e4cb233c82e3e317fb99142af80951306f27b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7db808498ec8cd7fa943aa470e98763556227df80636cf587baeca52ffdc47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a7c0b5e35c9096be00acae829346208c60c0b39330525cb77bf00311c1c59c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5f345dd5dd8170bc86be7e589f1e76359acd5b0c95cb244b025be8e36cd9e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33508e3025c768a9c32655ab151786fb8af77e051eb8779b796e35c3d0a3ef6f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04b878c17446b23a157fda9d3d550b2a8d2eef251a766b6b31b7cf552f012b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cf172f4ab65bd19d48f6b3b8e472401468617d7487196fb49f236eece4682e(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e96360cd543594b732760a3f5cf4f038e07f2c92eabf8e088eb29b181a5e798(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9080a4a5565c9467c32cb6fab1de044999e8b564bde7667b6f56cfe23c00b51f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc8d9efb4bdc06d73760b7433392ab51fe151152bddb71779abe97355ca434d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff691d4fd9c7b8a264b61d002c0f2497670648089c05d4cc69cce05db68dcbac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed866aa9ea02c7371224f53004ed71fb026c60012f41f033f2eccea2bc86b248(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b3550aab0e21b8dd89f2f4f8449a486d98ef4ba910d535fa131f999d38aa43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ea658e20b1a811493ff45f60b64be90253cbdd30e0ec4b8911b9f72227d8cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e3f16c734f54d6b6490a77950c272fdcaa573432072bf0fad5a983613d5e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43317251f8e37fe92cbc141ba3852d5891757976be707e44905e83a4b52a9342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47235d3631baae964168e2039f10475ff7b0457e37f20a0f0fd3bc21c6974ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff64b25e1f7980bdbd064266ad081861bf9a7c5570b062ebff1c7a89e5634f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085bb2ca3e2b3e53774b50b9ea7df01384b98e0d8ac6a5d4e7195a620e6c3ad8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31a738f54182db9d00a3d4f80a03d7ac5a8b8e2d9ee8e97c129807fa235e9f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca75dc97884bf6f4120f54a1e0803fb95bd7a7b52a8a49111db76e2d3bab723(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTermMatchFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99db347dfd0bb9d30ed0d515174471e426dc8b3ab1249fe89f5a7cafd973b77d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfee2878babfde321371352588ca87610f765303db7812c117a157220a84d67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851199addd78519421382111ad153d782933bf84f049a29315a9ba4aed8d5f00(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequiredNodeSelectorTerm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b664a6c419dbb47088c352747ac2d52eca90a21209c40bf9dada3f77d57870f2(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecNodeAffinityRequired],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79342100c548f4f057653f5c8cf6b35a861f66cf6c2ac4008b4394b672d78de0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0d2b198e880a425488869c578c18ed087e2dffe947e9c11eaa9e7580a815d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7163b4bee673417c0b29906d215243f5dcfd98efe934d935e7447823325e82fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88b5fe491d189f9094f2f58b1eaa58323cd8f98d5fa64341d1f982e3d4a46c7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686926aaaa1f69ef6830f232be6cafd22b205f25fdf5d3c8eab7d326bf8fc6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c382f8d605b979e61d427a26e06ffa6fb7f7bdff9d00a89e8a45f53595e7728a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a60c57ebd7785a6b6c9df7319ea1ef38d2583d2240417ef1ab781b761d13cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76fa1b56cda1fe864d656e7bd7c34b66d8839db94e3a0836d4704ee5c31dcb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataKubernetesPersistentVolumeV1Spec]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113976244ca2fe5a798509c5f9621655003ae601e6cd7a292165dac63090f031(
    *,
    aws_elastic_block_store: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_disk: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_file: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile, typing.Dict[builtins.str, typing.Any]]] = None,
    ceph_fs: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs, typing.Dict[builtins.str, typing.Any]]] = None,
    cinder: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder, typing.Dict[builtins.str, typing.Any]]] = None,
    csi: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi, typing.Dict[builtins.str, typing.Any]]] = None,
    fc: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc, typing.Dict[builtins.str, typing.Any]]] = None,
    flex_volume: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    flocker: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker, typing.Dict[builtins.str, typing.Any]]] = None,
    gce_persistent_disk: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    glusterfs: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs, typing.Dict[builtins.str, typing.Any]]] = None,
    host_path: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath, typing.Dict[builtins.str, typing.Any]]] = None,
    iscsi: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi, typing.Dict[builtins.str, typing.Any]]] = None,
    local: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    photon_persistent_disk: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    quobyte: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte, typing.Dict[builtins.str, typing.Any]]] = None,
    rbd: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd, typing.Dict[builtins.str, typing.Any]]] = None,
    vsphere_volume: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d84f1cee603d1e9964f9438dde61fad35f9a9ebe9848410a13516ab6e566425(
    *,
    volume_id: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    partition: typing.Optional[jsii.Number] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4481c3bc6efda3a18a6e5114da4138675ff4041eb5ae9077e63f93917e7b185f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d797ed10c0825e6c157829c96b37376934c73df8307d932c84a842a631313658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4460db22a20acc259e05e6ca666cc74a1fdb9892cfd115cd5e776d29fb934d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1b744e5fd526a4a344ef1353f418588e6971254212425011fe8bda58174bad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26817bd5a8b2322db5df3f20b12a7ae9e0cbaae4fd4fc45c77d813c0ca1d3e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6ad61a1aafc60119ed65ce6b73ce3323e8ffc23d1ec76cd5b949a9cf3a3611(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAwsElasticBlockStore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98db2c5e57788f811028512f8f7dc68a1b3ee2ba8b44180b6ec11b3108e9daf2(
    *,
    caching_mode: builtins.str,
    data_disk_uri: builtins.str,
    disk_name: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf682a19c605f0c89fc3e75616752ce4910c93b4325d47fd57553ff5e6bdf51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607d0982d2631b71198640cd3584b9faa0fd9dbeff7be2dd501cd1cf5623b1c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6464728969dba38444c2692b9fe5c4f068e7eb1aae9a4bbebecf970855ae3c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac88c7b0da31b6a6fe4a9e215d5031b56f709fbd72231240ec1b7d53dd95cc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b567e1e4c60b0e3cefe58a4754f096942a4526729488a0edf8c3dd9c41f4f7d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e632a528d070082b7a218f656fdc2f1b81f2a4daf51201b8699d2778fdb9b1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8aa80fc894b1295de26e3a41fca90d098881edc38558d54d1254d3d729f95f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a217a6b7c3929cea21179233fe69b3d72e74f0dea55c8737bd88cca7e5b1b8(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca89969e183b084ed94395577675b9d82bd43f819f2fee9cb21ee09c367315ff(
    *,
    secret_name: builtins.str,
    share_name: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff3ebb9d101b1eff9a17f051259b25329cf3eafcfa2ff7eee19aa64ad7b147a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bd178cc4bf6e5ceeabdf6b0966c235a12a66d7280b46112a0229f2fb78960b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b600c7783878e6bf226408abe59ef5d52dcf6bfe8aabd966077d6f06b9b4822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbb915c150ecff69d69c9a567abe5e9a41d093a4ff7dc2afe049366a34d85d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dac20213c3d7c18d5a90b736a9239a63c7a6cd9184904ac5b1cc51dee667df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb1cec703cb54cd084098fbf7afa767605ca3677fdc36d303ec81f7ba3a8a87(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceAzureFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21574e500eeefa0024fd86c1ea36f6c302cac859cbafab86a2efccf65b296ab6(
    *,
    monitors: typing.Sequence[builtins.str],
    path: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_file: typing.Optional[builtins.str] = None,
    secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cecb907445c48d9ed655112de946f02b933a03fa104089c33b22f014c4333a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4dae5f600d4cf1d3265c5c1e243878edada09a22b541630f0307f050677583a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5a05691a3849b70232b1fffd609931b3a8e3f0297dd34f8e3fad0bf4273cce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb83ea9bf2ae4179d87142f3c0ace9b8230bb461a04caeccc291344929f15a88(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfea857a268de465d880d71e4027bcaf6227eead88824402f51d0da29f0bacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aff64bbb369d4d289bfc6d27f162e4df12bfe7baf4c2edd44837e73edb11b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35ff2767acaf1119de5bf958fc2c7ad45cd7c0d83b5a33aefbb3fbd54523734(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108018c8d38866dbeaffc621529725d815e64d1e2fd886bfe1f0a3a2600219eb(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96bcf878fc410e85497703fa5589c05b8da8143533f93173ca490dcf6ef6adb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b6400e6805a31c8377fb3a3de64cc489d543cca2f666ad2a293859f35c217d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e367b40f90d0a51966be45c9072837e3926e84ec201193612606a2fefc44e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e111ed8b118e039d9d185028baf3309de13807d534d26824a2440d6203782500(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCephFsSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762417192d9ab1938214e0a567ffaea5d88a588c4da896d37aba7657de6f6ae2(
    *,
    volume_id: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d270519917ff4625bf6210cd564924a23272f6d3063f04700d2393a0d1534afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ee3675e6ff8a896808aed126746c74a5bbcfc3f452f35eedd94f1bd94e7c9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f7978828126c397030c29614f9f0751cc3f85db384a289b485bdbd09132629(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bffd4b078ccb837dc55280c9b2c5edd712c0f061342c89d880ec2e773e1f1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7f94f467864f1d364cbaf9c3d6ccab745797803a5776ffa964823349138bc8(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCinder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85cabe6ef938771e07bf1fcf90608f1c665462dbbafef6c63e5adc6e5f85108(
    *,
    driver: builtins.str,
    volume_handle: builtins.str,
    controller_expand_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
    controller_publish_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
    fs_type: typing.Optional[builtins.str] = None,
    node_publish_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
    node_stage_secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc099719380e72cbdeeab2015eaf4d7ba305efbd4c7ea3f6c6dcb7224672becd(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e1c50b466c632565ccdeafe41a4ce577408e6fe9cfbb6a10d75bba058b22e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa16e0cb7cb6f26c1ea97e1a5c548416c3a44628e125fec45aa3793f0383cd72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6381259433490a0c0626efda5ef883f4b4fba4f951257f250ca381fbfd39a28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2526198a23b4053a5900082a940fa062477d8678ad2450df3a83146cb085c16(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerExpandSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92de899c7ccec6485649ccced6735e39ac3a21c61d0aac855c7fdb41285d51ad(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccbebcfdb9d191a7478fcb1bcac8c6463e1f78f3ed65de440e9a67eaf191806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b5e476a34d3226a0d524be2331f62d0339aeda1a4f37780a7f674e2550c47a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415889eb5c7b226dfcd45ff765518075b95b5c8e403550ab7d8f3a051b303d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7604551e89c0e2a049793375e3f1cf81caa432f86dc403980d10506eda8c5e0(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiControllerPublishSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fd09f8bbff57d161f1a15dbb1ae42d718d8f330b47abb6856d4d278f8ce04f(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6077184a5d5c2be081ef2d44358a2b5a004b6fbafebd4ff880e5966580e3c11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10268b4c21cd8ba27954cb4e084fdc43382fd7bec25fa37998f0ae5be4359a16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea97c015565da84bc625a461efc1ba0d1fabb5897e0edfce458382adc7b1848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d565630d7aa18a935928cfd63110847cd8654f9e46f1c55fb6a542eefbf55c92(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodePublishSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0711a4e1d4885bf8aacbcb2b04a8eed22df7a14f5d9a292a34e32a34616b755b(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2110fab5345e61f2f8ab12f3bdd74f987ddda56a727392a5475b82acbbb142cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95941b05d74a7cb7354ad29422988934efb4477070ddb81fdd3d71eb2365ef06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce5300888a88062e96a0592a5e17eb7cff53858cefaf5b92ee5066e1b2ea74e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36562f58a51a30e902cfb5ee377a2c9fa3949f6b7fce067eda6d612415c41e1f(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsiNodeStageSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6407951d4efb2d74d262802f4c47530ce6b7de5eda7ddf43f78dfbaba7cf45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e484a17e46cc553e7995aaf99d10573666ba377e10cb6a392bbabdafa7c9e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7b161854bd546fec9fc4282bfee9a49da0ae5ed852d83f5cdc21fabcad6cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f2618f0e93594359a64554f500e54051b2fb08b3f7da967da1e49f2d7a3b20(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92860d484a4a27a16d0d8fca41e430f2b184df5dc32cb621d42009b8653a1bee(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daafb6b00e9c28f06004aa93b97d5d9c6d38a7d37f76b90392d108fc314d62e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55951abdcb788a47a83fb6426af24f633491044a70e4705b582396b19ef31641(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceCsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1072eeef6ed822c30347f081d0cf3ce6087dc4252d2be80e450aa5d29e27bbc2(
    *,
    lun: jsii.Number,
    target_ww_ns: typing.Sequence[builtins.str],
    fs_type: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7fdeedbbab3cf9b5737ac9169ace89dd5736011ec8cc436c21a0023be92683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc0b7710e8f342683747a6c4b7d6170ec47f4fb25dc0e03e11bd7ebf0c83d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab8e36de22cf495a57dbd5774409967f906c9defcad22a0a6f0a14b0be05fdf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b3005a6eeb4d1a005bd814dc6cf620994efaf6494757c6e53547a82d7e90d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e43dcf1078933f8c67fa292c465c73b1dff3082646a99e15d67181f619ba193(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5910cc248ab4f97fe4e5b5539c09c127ad49eb38833df1b6e90d3299e66ec7(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7255398244458af6d67f628503e7b703e761c72122ad8bb717ce0b51df62c0f3(
    *,
    driver: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c5ac88e040f87ea970a5132c8dcaa0dccc926b351d1b47a3c4351130ce8e20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4df2c919ad472d35c8b8f64ddc7e8cad1f490447a2d4ad37fd6bd15d1ae251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd67c99349a9dd8d6969f77ad77bcef8973454aaef7866b83cbafdb1f910373e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ff8d8d8847d25e22dcf954ed2d081d8df5d7a7e0dcbcaae865ff1eb7d36b33(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653490b1d54e8d81dc6273b86d05ba938ce2ea4a1306422dd6a622e754dd8cc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77df88b4d374230fe3956a4bb8171306d95712ac3bfeba26868c72fc3e3a33ec(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e956ec00d98d676117b691dcc01b800af283e2dc0450733e59b983af64602f7c(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ce8dee0d9ab99b8e56915636dd350f547085b115840017c3ff1f07d4991580(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec20b3c4570c3e23f7ca784575488e4d4d884ecef2ccba298c3f8c4bbdde6a00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95b93b83996c07178772a2297b3ac3d0069805ac469bbb2a06fa4c0a1482731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d02538fe0a64ba0ce52b9ee9396e92f0fb95b756c33ec76ccbe12ee406277b(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlexVolumeSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241135ff2bb5ad6f59a42b4dd5a4b1f660a197bd421bf8a03554cad184dabe47(
    *,
    dataset_name: typing.Optional[builtins.str] = None,
    dataset_uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a080c95a88976cbadbf46a2200ef9b571d4d3268fbd61bb94960d5aa982ce6a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd7f05d49b356c4decd7431a3664bfe470717da31d8baf059641ec4dadaf5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88b9669cb416633613416311e1c79256d350ccf935c5f0d6edf473be2e81838(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d307c877bddbb5d36f0e6798832e97f14257f11b999f73a03c5acd1ac7b3e5d(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceFlocker],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61629f288bf6e5ec05f93f237c1b0565e1c2d2ec867c0d97f38af3485c69be7(
    *,
    pd_name: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    partition: typing.Optional[jsii.Number] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f61d216dd662dbe04358f33fc85a887f262725ef9c3f275355afe6df3feff5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c97a8efbec18d5af69d4c725f130a3ef49ace30c420ceda5ce12d46ec9cbb05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68fc75b4a03bdf7f61a53da7e259649fe7a29d705c2a1a92f3cbe80a81a0bac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d65aa3c74ceba7bf70ac97788f2cae5999f78f4cfab44bf7ceff4c5f25f2487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6d52ec253230d19f5a990fd2a487c1b279d75724fd101952a7f19e10a1109c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7bc15f6e343b9c5ff581f49396554b6ab68b8b068ee0b90218ef6c1cd8ca6c(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGcePersistentDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1541fce0f18550517d68cba9135421a31f2ed753c42c2b9264c0a2b689f46181(
    *,
    endpoints_name: builtins.str,
    path: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5affc8d4403e62a6bbd03149966da9fef908ad112ab992d5d6512ce434d697a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0f22a59e831560fc7346a571951c58dddf23ff7bf56626d57c1956f5db2332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d4d900335869d10358ed92fac0251460b7a08e8d1c0fd6693ed278aee627fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e79ada5d676b5e99c406fecc38e3c09466f5b8cec61fed9e12bbf1862b9dff2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446d41d552ad146a5de9d618249f6d4e169dc260f709259c320b5a396661f2e6(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceGlusterfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfd95af06aa4a13b9c5d09e4e946a49cc62375767b6aa0333a9d83f2026f61e(
    *,
    path: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c32d2bf3e6f66f420bfaef475125a8f1550dfaeafe9378eb5e26166a5fb574a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9f6d704e30118d3ffcc085a1ea6c6a64be0502956b5c9ca65347e8a9dad26e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3ea191affc8af59f194550817b22e4e2acc096084c6e93dceca790b50cc6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1abc781e3d008dbaec8612b21da0560db05834b094332312185f082aece4341(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceHostPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da9cf096e164f4eb98d40ad163ff5f8dda14bd73bdc9c0bc7d175db1828cd09(
    *,
    iqn: builtins.str,
    target_portal: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    iscsi_interface: typing.Optional[builtins.str] = None,
    lun: typing.Optional[jsii.Number] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b92a8f8bf1a28c25d7e3fb2905e25ea51ae8705777c55c79a98e9fea30f927(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdd042570b06f5010e5eb182f56fbdf1a7b96fae7a80317e69dde309e6c90a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8810f708dc057afc4ce3a8f0456339cff726bec6ea4b6335d7aba566d3477308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab9aa856115cf61b1ceaf96b740db9fd8f4c192e2aa3e84d9ca92e32835b8b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4433697239e27173d53ee83ce9cd21e3ba920e3ec9fadfcb74c0d04e34967749(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5c0c80051e1d14926dfe5d3239d9d3eb6bad523989bda589580a8b0724ad55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131c3750a4d73dd861a8a90d5e2e91f4ae7215094142afd0c66530b53fda7083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fe99944dbd0b9d47ee485594cd193061ea688ead86555fcdbe3a5db8f3e2d1(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceIscsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65828e0e0f43df08e690982b7c21714add6ab55c3474e9f9d3dff4eb4783d604(
    *,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c605afb2a44a1eca17e27d68bb27473c3ba448af9ce6340e4a19a38e289611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfeeec763ce4322c1493b1bb9c8f6124d9079c731d2e48a8258eae3a0e094bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d3ee946a183172d4ceee9f40a07644f2df1d7b37ed9dcc7ff6f5b213700e95(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceLocal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132053ff7a234b35f793ad8c39c887a84f86d5b6fb236954f4d2d0dcd31295ef(
    *,
    path: builtins.str,
    server: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f35675634ec45a4234872e03b08489ab4b7d68b69aeb3eaa4bf618f844ac34d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64593791276c651e6f503043b53e4e621529504a5e28225c2a2f1eec3694e994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0f12735220504b093d57faedf3e4fb88c0b0abd1c5bea2cdbec071f51f1e4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10151930eb5ca30f66c061dc4428795990540a0faebb5540c8240d1353ea9f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d50d230acc72e0bd39d04e638c370c43e6d50a008ea9903f8953f5656f41e4d(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f02bc26af73927534bc16682ff7c910b45a4ce70045f92c82974a52b6538fde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac340614a27dbb7a93dcb021302b48dce5b8a40beb7a6c4932fabf4e6d6c3fa(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f67052ff63203c7fa4ae94c24e9486cd0f37bc5c31847db9de98523cc7d8994(
    *,
    pd_id: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be27d3988cb2904664fca67af9241df9094a1774cba5f32a3e7ff18f949b7e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48019b13d2fdb5ada57fe319d075f6d9b4b1308fddf3b7990b4ed6f0e3522cef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a94453fef26e52533cf03d68cae2fb6518bda4b35df95da2610b07e968f8e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fa1da91d7aae82983a4f2c21bd39fdb7f2d97c303a126e6c52079c7f934940(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourcePhotonPersistentDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb38965a1220d0cca97da4cfb0efcff00a02dae3b7ed60645ec9779543de4e3(
    *,
    registry: builtins.str,
    volume: builtins.str,
    group: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466ab7e5050bf929696b329f11c41d99188e6fd5295346856370bb5e6fda74b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f8d88c069f64f4b9c25a8ebca33edee9336c13cf9c43a4701c95bedc364d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dacaa9a8a0903205e7683c5f5ff5259ace2fa86aff61d24f54da7a0d926beb9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f762d82aff49c708a66282a78a26d09786fbb7b27a8e6dce7b72808437751509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beefa9cc9b8f33fafd43c82ef7b253dc6220bdcce7e37a2dcc9876ea60a07dfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86509090784fae12b08b034337fa384c0187e02cb693909777c2c2ee464f0dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be9162c6edd0832aae93cc789d263bfe59af2a79a8eff5589638bc5b9905677(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceQuobyte],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7348ba12c0ea9b812c243dcf917bd59bf6435b8030a538b3101ca9051d0e5130(
    *,
    ceph_monitors: typing.Sequence[builtins.str],
    rbd_image: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
    keyring: typing.Optional[builtins.str] = None,
    rados_user: typing.Optional[builtins.str] = None,
    rbd_pool: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_ref: typing.Optional[typing.Union[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71718d00f500aca2096c7726544e2d2618d78ae8d64aca2a210e202c6235708(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8aa4c921d9d7c8fe2a3933b8b3310b31a12f97dc51a49b4b083b35d494cd571(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c5f398366fa7792a5c815d98067e2f0b5ee2c86cb2e698b345a141ba2afcff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec00fb4a5c750ea0d770b8bcef23ee02b914b8b1a4fb8ede7234d005e2e7bd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839a792c3ac0646ab8cd7a2c2fa7f33ca50bbf0ff4271e31d46cd8317e86be38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b025c5433aaf4335144ec9581f587bdf36e79ce92721e9be42f684aee3329392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9702eb9fe20cdede17bd0ae148900c9e1b2f0e9b9cf43ba65fb3bab38b9b6c6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c472670073d335a309f54a7eac69f3754f8c1959673e0f1b77a64a35b3141d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724729284948a2aedf626fc37656848b54f946e95bcbf1590a16afc3dde5d151(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbd],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d36a19a54faa909d32ae97da09627cadeae6ad6c65ee2d597a4319305dc1e8(
    *,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374fbac5be799075d48f8aacfcd107346bb6db41fe3159ec36ba33085398e2e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db1875e1a59b28571613f1a34bf36c6f34ab0faf28e64442fb5e8b19c994589(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae41f75612b93c7207eeb7ae17cecb19c77ccd8a70db99eaf7368669e9dbddc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62215320e89864f6d050a55e62f27d6f969ff9e2f3f87827eb30722754d3e676(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceRbdSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd86bd32e5a70ff3324c9ecc2ad928b21c54187387768279869aa5fd4d597576(
    *,
    volume_path: builtins.str,
    fs_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9b9567bc8f389a8c354b98d896d48acc02d5573d4a6dc577ca1d21f71dd814(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ace705aacd552af3304e8e0b56f303d287b08ee5d0d6a88aab19dc1eafe5b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0febdccd780dcb12040bd843e87565b0ac9fc8ae85353144b3cb30d8fd604739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22ce9d5b750b5613c596a5da94c33d6e24b6eea6b4273d5a504fbf7b3e5e828(
    value: typing.Optional[DataKubernetesPersistentVolumeV1SpecPersistentVolumeSourceVsphereVolume],
) -> None:
    """Type checking stubs"""
    pass
