r'''
# `kubernetes_horizontal_pod_autoscaler`

Refer to the Terraform Registry for docs: [`kubernetes_horizontal_pod_autoscaler`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler).
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


class HorizontalPodAutoscaler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscaler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler kubernetes_horizontal_pod_autoscaler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["HorizontalPodAutoscalerMetadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["HorizontalPodAutoscalerSpec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler kubernetes_horizontal_pod_autoscaler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metadata HorizontalPodAutoscaler#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#spec HorizontalPodAutoscaler#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#id HorizontalPodAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3204788aa482b9bc5577cc97d383bea14289372d47f3c887866c1364b1db3b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HorizontalPodAutoscalerConfig(
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
        '''Generates CDKTF code for importing a HorizontalPodAutoscaler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HorizontalPodAutoscaler to import.
        :param import_from_id: The id of the existing HorizontalPodAutoscaler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HorizontalPodAutoscaler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de6ca68e79c8c1dcf44a0eb4594e25f4f2bf8c3b527ba97c72b9fb9c5bd4cf1)
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
        :param annotations: An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#annotations HorizontalPodAutoscaler#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#generate_name HorizontalPodAutoscaler#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#labels HorizontalPodAutoscaler#labels}
        :param name: Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param namespace: Namespace defines the space within which name of the horizontal pod autoscaler must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#namespace HorizontalPodAutoscaler#namespace}
        '''
        value = HorizontalPodAutoscalerMetadata(
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
        max_replicas: jsii.Number,
        scale_target_ref: typing.Union["HorizontalPodAutoscalerSpecScaleTargetRef", typing.Dict[builtins.str, typing.Any]],
        behavior: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replicas: Upper limit for the number of pods that can be set by the autoscaler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#max_replicas HorizontalPodAutoscaler#max_replicas}
        :param scale_target_ref: scale_target_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_target_ref HorizontalPodAutoscaler#scale_target_ref}
        :param behavior: behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#behavior HorizontalPodAutoscaler#behavior}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param min_replicas: Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#min_replicas HorizontalPodAutoscaler#min_replicas}
        :param target_cpu_utilization_percentage: Target average CPU utilization (represented as a percentage of requested CPU) over all the pods. If not specified the default autoscaling policy will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target_cpu_utilization_percentage HorizontalPodAutoscaler#target_cpu_utilization_percentage}
        '''
        value = HorizontalPodAutoscalerSpec(
            max_replicas=max_replicas,
            scale_target_ref=scale_target_ref,
            behavior=behavior,
            metric=metric,
            min_replicas=min_replicas,
            target_cpu_utilization_percentage=target_cpu_utilization_percentage,
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
    def metadata(self) -> "HorizontalPodAutoscalerMetadataOutputReference":
        return typing.cast("HorizontalPodAutoscalerMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "HorizontalPodAutoscalerSpecOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["HorizontalPodAutoscalerMetadata"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["HorizontalPodAutoscalerSpec"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e36b78af617bbf9e9bd52282790de4f842b3bc9ec6261b82ecc9450287adee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerConfig",
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
class HorizontalPodAutoscalerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["HorizontalPodAutoscalerMetadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["HorizontalPodAutoscalerSpec", typing.Dict[builtins.str, typing.Any]],
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
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metadata HorizontalPodAutoscaler#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#spec HorizontalPodAutoscaler#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#id HorizontalPodAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = HorizontalPodAutoscalerMetadata(**metadata)
        if isinstance(spec, dict):
            spec = HorizontalPodAutoscalerSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaecd39a76273a9a9ef0d14852a138b61f2d4d288344528367fcfc7a716bac61)
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
    def metadata(self) -> "HorizontalPodAutoscalerMetadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metadata HorizontalPodAutoscaler#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("HorizontalPodAutoscalerMetadata", result)

    @builtins.property
    def spec(self) -> "HorizontalPodAutoscalerSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#spec HorizontalPodAutoscaler#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("HorizontalPodAutoscalerSpec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#id HorizontalPodAutoscaler#id}.

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
        return "HorizontalPodAutoscalerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class HorizontalPodAutoscalerMetadata:
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
        :param annotations: An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#annotations HorizontalPodAutoscaler#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#generate_name HorizontalPodAutoscaler#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#labels HorizontalPodAutoscaler#labels}
        :param name: Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param namespace: Namespace defines the space within which name of the horizontal pod autoscaler must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#namespace HorizontalPodAutoscaler#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb05b59494172fefa288638491a766f92427844c79776a339ab5d36f7ec15d16)
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
        '''An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#annotations HorizontalPodAutoscaler#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        '''Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided.

        This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#generate_name HorizontalPodAutoscaler#generate_name}
        '''
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#labels HorizontalPodAutoscaler#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within which name of the horizontal pod autoscaler must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#namespace HorizontalPodAutoscaler#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8664126bd102d4ed5164a706eb4d6267e943d6c3c7601bd351db399ddd9b21bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d266c152449de007cdba89247720a8e5774bbe2806a55e419a51909c562c1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generateName")
    def generate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateName"))

    @generate_name.setter
    def generate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a67fe3f5d046a606c76b09dcd4ef9f7e6cee9b8f626a25c0244bcc753a72a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e385dd60d79895434d755a72083db2b52acaad4ccf421b124fcad3a0c10bb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71fcf61effa8155c798d6e9ffc823dd4db637c43e7bfdab682f3db703d94514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c0a076f34fcc4def3d8d85f58718652ababe1485accbb84597f9523b5939a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerMetadata]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082460acb0ed973b97e305f362cb1ef237810b0a300316b735f4977b9ee22b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "max_replicas": "maxReplicas",
        "scale_target_ref": "scaleTargetRef",
        "behavior": "behavior",
        "metric": "metric",
        "min_replicas": "minReplicas",
        "target_cpu_utilization_percentage": "targetCpuUtilizationPercentage",
    },
)
class HorizontalPodAutoscalerSpec:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        scale_target_ref: typing.Union["HorizontalPodAutoscalerSpecScaleTargetRef", typing.Dict[builtins.str, typing.Any]],
        behavior: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replicas: Upper limit for the number of pods that can be set by the autoscaler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#max_replicas HorizontalPodAutoscaler#max_replicas}
        :param scale_target_ref: scale_target_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_target_ref HorizontalPodAutoscaler#scale_target_ref}
        :param behavior: behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#behavior HorizontalPodAutoscaler#behavior}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param min_replicas: Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#min_replicas HorizontalPodAutoscaler#min_replicas}
        :param target_cpu_utilization_percentage: Target average CPU utilization (represented as a percentage of requested CPU) over all the pods. If not specified the default autoscaling policy will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target_cpu_utilization_percentage HorizontalPodAutoscaler#target_cpu_utilization_percentage}
        '''
        if isinstance(scale_target_ref, dict):
            scale_target_ref = HorizontalPodAutoscalerSpecScaleTargetRef(**scale_target_ref)
        if isinstance(behavior, dict):
            behavior = HorizontalPodAutoscalerSpecBehavior(**behavior)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62bde2b2a07d13a5e4d92fb302c1de1571b1df5f60bde7ed05303b358b1461ab)
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument scale_target_ref", value=scale_target_ref, expected_type=type_hints["scale_target_ref"])
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument min_replicas", value=min_replicas, expected_type=type_hints["min_replicas"])
            check_type(argname="argument target_cpu_utilization_percentage", value=target_cpu_utilization_percentage, expected_type=type_hints["target_cpu_utilization_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_replicas": max_replicas,
            "scale_target_ref": scale_target_ref,
        }
        if behavior is not None:
            self._values["behavior"] = behavior
        if metric is not None:
            self._values["metric"] = metric
        if min_replicas is not None:
            self._values["min_replicas"] = min_replicas
        if target_cpu_utilization_percentage is not None:
            self._values["target_cpu_utilization_percentage"] = target_cpu_utilization_percentage

    @builtins.property
    def max_replicas(self) -> jsii.Number:
        '''Upper limit for the number of pods that can be set by the autoscaler.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#max_replicas HorizontalPodAutoscaler#max_replicas}
        '''
        result = self._values.get("max_replicas")
        assert result is not None, "Required property 'max_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_target_ref(self) -> "HorizontalPodAutoscalerSpecScaleTargetRef":
        '''scale_target_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_target_ref HorizontalPodAutoscaler#scale_target_ref}
        '''
        result = self._values.get("scale_target_ref")
        assert result is not None, "Required property 'scale_target_ref' is missing"
        return typing.cast("HorizontalPodAutoscalerSpecScaleTargetRef", result)

    @builtins.property
    def behavior(self) -> typing.Optional["HorizontalPodAutoscalerSpecBehavior"]:
        '''behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#behavior HorizontalPodAutoscaler#behavior}
        '''
        result = self._values.get("behavior")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecBehavior"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetric"]]], result)

    @builtins.property
    def min_replicas(self) -> typing.Optional[jsii.Number]:
        '''Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#min_replicas HorizontalPodAutoscaler#min_replicas}
        '''
        result = self._values.get("min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
        '''Target average CPU utilization (represented as a percentage of requested CPU) over all the pods.

        If not specified the default autoscaling policy will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target_cpu_utilization_percentage HorizontalPodAutoscaler#target_cpu_utilization_percentage}
        '''
        result = self._values.get("target_cpu_utilization_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehavior",
    jsii_struct_bases=[],
    name_mapping={"scale_down": "scaleDown", "scale_up": "scaleUp"},
)
class HorizontalPodAutoscalerSpecBehavior:
    def __init__(
        self,
        *,
        scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleDown", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleUp", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scale_down: scale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_down HorizontalPodAutoscaler#scale_down}
        :param scale_up: scale_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_up HorizontalPodAutoscaler#scale_up}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b705fd022c11550441c44d382c38b7762785aec5558d167da6edd48292bb57a7)
            check_type(argname="argument scale_down", value=scale_down, expected_type=type_hints["scale_down"])
            check_type(argname="argument scale_up", value=scale_up, expected_type=type_hints["scale_up"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scale_down is not None:
            self._values["scale_down"] = scale_down
        if scale_up is not None:
            self._values["scale_up"] = scale_up

    @builtins.property
    def scale_down(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDown"]]]:
        '''scale_down block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_down HorizontalPodAutoscaler#scale_down}
        '''
        result = self._values.get("scale_down")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDown"]]], result)

    @builtins.property
    def scale_up(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUp"]]]:
        '''scale_up block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_up HorizontalPodAutoscaler#scale_up}
        '''
        result = self._values.get("scale_up")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUp"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8a7d48c3603b61ba517eb241db34718fbbc6195dd2d01e957c3ee4b9fb4009b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScaleDown")
    def put_scale_down(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleDown", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a39270634d1c4875e18c4de9b5d84cc489107b048ea8f715a370c0d6f725848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScaleDown", [value]))

    @jsii.member(jsii_name="putScaleUp")
    def put_scale_up(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleUp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ded5df46797812a244c0fc5a712851be60dcab61f44ea6b959bcc415716e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScaleUp", [value]))

    @jsii.member(jsii_name="resetScaleDown")
    def reset_scale_down(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDown", []))

    @jsii.member(jsii_name="resetScaleUp")
    def reset_scale_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleUp", []))

    @builtins.property
    @jsii.member(jsii_name="scaleDown")
    def scale_down(self) -> "HorizontalPodAutoscalerSpecBehaviorScaleDownList":
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleDownList", jsii.get(self, "scaleDown"))

    @builtins.property
    @jsii.member(jsii_name="scaleUp")
    def scale_up(self) -> "HorizontalPodAutoscalerSpecBehaviorScaleUpList":
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleUpList", jsii.get(self, "scaleUp"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownInput")
    def scale_down_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDown"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDown"]]], jsii.get(self, "scaleDownInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUpInput")
    def scale_up_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUp"]]], jsii.get(self, "scaleUpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerSpecBehavior]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecBehavior], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecBehavior],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be9f4e1bb3d049b06e8c2ffc7a79e33cab54c3bc45fbeac1e6bc482c3069200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleDown",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "select_policy": "selectPolicy",
        "stabilization_window_seconds": "stabilizationWindowSeconds",
    },
)
class HorizontalPodAutoscalerSpecBehaviorScaleDown:
    def __init__(
        self,
        *,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy", typing.Dict[builtins.str, typing.Any]]]],
        select_policy: typing.Optional[builtins.str] = None,
        stabilization_window_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#policy HorizontalPodAutoscaler#policy}
        :param select_policy: Used to specify which policy should be used. If not set, the default value Max is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#select_policy HorizontalPodAutoscaler#select_policy}
        :param stabilization_window_seconds: Number of seconds for which past recommendations should be considered while scaling up or scaling down. This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#stabilization_window_seconds HorizontalPodAutoscaler#stabilization_window_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e444e3f8a4902017601e4d30298e81a138c43865f56f1f40bf811c43354ed7fb)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument select_policy", value=select_policy, expected_type=type_hints["select_policy"])
            check_type(argname="argument stabilization_window_seconds", value=stabilization_window_seconds, expected_type=type_hints["stabilization_window_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
        }
        if select_policy is not None:
            self._values["select_policy"] = select_policy
        if stabilization_window_seconds is not None:
            self._values["stabilization_window_seconds"] = stabilization_window_seconds

    @builtins.property
    def policy(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#policy HorizontalPodAutoscaler#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy"]], result)

    @builtins.property
    def select_policy(self) -> typing.Optional[builtins.str]:
        '''Used to specify which policy should be used. If not set, the default value Max is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#select_policy HorizontalPodAutoscaler#select_policy}
        '''
        result = self._values.get("select_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stabilization_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds for which past recommendations should be considered while scaling up or scaling down.

        This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#stabilization_window_seconds HorizontalPodAutoscaler#stabilization_window_seconds}
        '''
        result = self._values.get("stabilization_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecBehaviorScaleDown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecBehaviorScaleDownList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleDownList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b046d49c063b4bedc41f444dede05b35b24c7d27e6c228b76aa87c8946d2cdc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecBehaviorScaleDownOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a024a0ae1bc62fdb972053e1752ea376024c75b830b0154c8734db97639a57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleDownOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31edc5cf760faf3ce2be35ededf01be17da6f2cfc3c79ab9d1df81c98ddb9a34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1ff8796bda9d5489961a1952bcd818033384c959098af77fe17891fd8431fae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f38e05b8b2771501e35bd435649e6332c258463acbc4ee409e214c72733cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDown]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDown]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDown]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff3eb4b81c20a26686733ead1850cd4a260d99dd6d049bb4c70029943fe066f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecBehaviorScaleDownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleDownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a3555a60aeb23d4d170e1d04c0e9718809789780a0014a82b2f7e1a5325ca0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d16265201f2e9c9556c143701441ef92c2d95604bcf8d0317e9fc843fc648f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicy", [value]))

    @jsii.member(jsii_name="resetSelectPolicy")
    def reset_select_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectPolicy", []))

    @jsii.member(jsii_name="resetStabilizationWindowSeconds")
    def reset_stabilization_window_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStabilizationWindowSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> "HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyList":
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy"]]], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="selectPolicyInput")
    def select_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSecondsInput")
    def stabilization_window_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stabilizationWindowSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectPolicy")
    def select_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectPolicy"))

    @select_policy.setter
    def select_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8222ce0bd57665056b01f819c1c4f21d581a26f29c21555e00a76bcd54337c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSeconds")
    def stabilization_window_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stabilizationWindowSeconds"))

    @stabilization_window_seconds.setter
    def stabilization_window_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67413f56a81dfbb60da7f8d314440f3a8055c6de7452f704b16b94a219a3efeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stabilizationWindowSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDown]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDown]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDown]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fc2efdb9a400b030685264d753cd7e8b1aa0c816885866b86919737aad1353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy",
    jsii_struct_bases=[],
    name_mapping={"period_seconds": "periodSeconds", "type": "type", "value": "value"},
)
class HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy:
    def __init__(
        self,
        *,
        period_seconds: jsii.Number,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param period_seconds: Period specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#period_seconds HorizontalPodAutoscaler#period_seconds}
        :param type: Type is used to specify the scaling policy: Percent or Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param value: Value contains the amount of change which is permitted by the policy. It must be greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff03bdd24b570a82c0921bb9760e754bf8c68d3906fd8611b5b50e6d9c90706)
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "period_seconds": period_seconds,
            "type": type,
            "value": value,
        }

    @builtins.property
    def period_seconds(self) -> jsii.Number:
        '''Period specifies the window of time for which the policy should hold true.

        PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#period_seconds HorizontalPodAutoscaler#period_seconds}
        '''
        result = self._values.get("period_seconds")
        assert result is not None, "Required property 'period_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type is used to specify the scaling policy: Percent or Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Value contains the amount of change which is permitted by the policy. It must be greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15a2f5ba9e19727b3ec610ab7c35670f5a7807b0867f79d7c8641a6ce9965857)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd2ce3df568eb5d13ab8c16be060acb6f45277700c03afd46d87a4cd09a8e56)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0014cfc18989e9b5b263f0ba7e793643982ca255b5bd9246d86e746d1312a4b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f82f984eaf071992fd147f08093e40748eaea71be4d18046961aaf8269b1d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c87d66a57a6f832a89091bd2469c3748487d74701127b327cefd78103c6afd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b853fb09d4fb7b1b495bd7650ba4c8973fd4e84cf39a86c08671470e3929dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4b370120324fa673beca3e83f0469740bde06a04f7b6efbc5980ac066b5c08f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5929d2970ae2d1789ba3f2c64f0c8f49fea0013efcab03a1719c8cd42612dfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36235b0967bd873d7dc43d63fea5f17fc58e73a18ceba6acdce9dfa55f4b0364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6412a1b4523bc8d5fc2d02f81ba5b60db4e70e3a81ccac92b013bf2559555de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de11af1b236491f4ce28349d84f7516f9da6f056ce79334db4733cf8adbaa778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleUp",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "select_policy": "selectPolicy",
        "stabilization_window_seconds": "stabilizationWindowSeconds",
    },
)
class HorizontalPodAutoscalerSpecBehaviorScaleUp:
    def __init__(
        self,
        *,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy", typing.Dict[builtins.str, typing.Any]]]],
        select_policy: typing.Optional[builtins.str] = None,
        stabilization_window_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#policy HorizontalPodAutoscaler#policy}
        :param select_policy: Used to specify which policy should be used. If not set, the default value Max is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#select_policy HorizontalPodAutoscaler#select_policy}
        :param stabilization_window_seconds: Number of seconds for which past recommendations should be considered while scaling up or scaling down. This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#stabilization_window_seconds HorizontalPodAutoscaler#stabilization_window_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283eeca41622ed7cb30bd54d274a383882bed39abf147f3f1b75ef743f98bd45)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument select_policy", value=select_policy, expected_type=type_hints["select_policy"])
            check_type(argname="argument stabilization_window_seconds", value=stabilization_window_seconds, expected_type=type_hints["stabilization_window_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
        }
        if select_policy is not None:
            self._values["select_policy"] = select_policy
        if stabilization_window_seconds is not None:
            self._values["stabilization_window_seconds"] = stabilization_window_seconds

    @builtins.property
    def policy(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#policy HorizontalPodAutoscaler#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy"]], result)

    @builtins.property
    def select_policy(self) -> typing.Optional[builtins.str]:
        '''Used to specify which policy should be used. If not set, the default value Max is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#select_policy HorizontalPodAutoscaler#select_policy}
        '''
        result = self._values.get("select_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stabilization_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds for which past recommendations should be considered while scaling up or scaling down.

        This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#stabilization_window_seconds HorizontalPodAutoscaler#stabilization_window_seconds}
        '''
        result = self._values.get("stabilization_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecBehaviorScaleUp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecBehaviorScaleUpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleUpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0cee265d653504aa1e7c98347b76e00bc3a540c08e0f1058b32ae5c33111ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecBehaviorScaleUpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbe85d58fa7d3cb384bed66eedb4d07cb22bea96da303ec5fff9b7d5825a838)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleUpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ecbf6562fd526ed675b51412e4c39800fd66c67e888d2d819612a765a6c4b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9128f268976a75af683bb6b77842b5015baf9753ec6cda16a664648a0932928f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3d3ce3672353e2cac3ce3484e97e04072181309eabbd0386380ca473b74d432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7242d24e005e7076953de6966ee56069a887a6b100a2f7ceb64db00e3b00d395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecBehaviorScaleUpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleUpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1e07ea75e58231a09bcec705a0b763c28e87c8a53b5895a0e46de56d307658b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07c37fc24f3a3083553eba142eba886af24543d0192b6521643ea52ca5ea6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicy", [value]))

    @jsii.member(jsii_name="resetSelectPolicy")
    def reset_select_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectPolicy", []))

    @jsii.member(jsii_name="resetStabilizationWindowSeconds")
    def reset_stabilization_window_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStabilizationWindowSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> "HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyList":
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy"]]], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="selectPolicyInput")
    def select_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSecondsInput")
    def stabilization_window_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stabilizationWindowSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectPolicy")
    def select_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectPolicy"))

    @select_policy.setter
    def select_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16971a746d8a47a5242087ab932b1e354d85d3b12a5f6a7927617f9cc7dc1ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSeconds")
    def stabilization_window_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stabilizationWindowSeconds"))

    @stabilization_window_seconds.setter
    def stabilization_window_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0381cb1085db24a56d2688a2b7789d21de6411e3d0efcf7b4a2e49d050f0d38d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stabilizationWindowSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b117f26cb3c7d55bca40c9ef1ea3f6be2dc0be27838b6c10edeba876bd7f2976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy",
    jsii_struct_bases=[],
    name_mapping={"period_seconds": "periodSeconds", "type": "type", "value": "value"},
)
class HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy:
    def __init__(
        self,
        *,
        period_seconds: jsii.Number,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param period_seconds: Period specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#period_seconds HorizontalPodAutoscaler#period_seconds}
        :param type: Type is used to specify the scaling policy: Percent or Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param value: Value contains the amount of change which is permitted by the policy. It must be greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6199baf49f01ffe26a71f36ecd6eab4482383a561c9de555e01a6192d1b96e3a)
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "period_seconds": period_seconds,
            "type": type,
            "value": value,
        }

    @builtins.property
    def period_seconds(self) -> jsii.Number:
        '''Period specifies the window of time for which the policy should hold true.

        PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#period_seconds HorizontalPodAutoscaler#period_seconds}
        '''
        result = self._values.get("period_seconds")
        assert result is not None, "Required property 'period_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type is used to specify the scaling policy: Percent or Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Value contains the amount of change which is permitted by the policy. It must be greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29a68288f3504a8e39e641e65a67ded6e2fe5ec01323a8003b97c44a1ba4877b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0851477bad5ce785d20e48d5245f6cddd976a9c23772bd5fa28c78146e58ce8b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3860e41242fb6d618d3df5f678da7175c242cb86ead7db19b31ee5ba0f8cf3f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7dfb80e2539a8cc64fff21a01c0a3b08fda2a81a39a6cf16a40f6667bef240a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b06c13c2d1394d58545417187dea82ea35a9e635d1e8acddb42a67072be1223c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a0014291a4d67f6aa45fdc3dec020d985f5a8e8f40ede5daa0ef1d57fe6807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bebc596acfa5303d1c2bcca9fe742adeff377c39f1407f1ef43014b948818bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efc4a4ebe5fef7914190e4e9b92aaf5cdb2ced71e7ddab2ac2dc76e914f40ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb92815fd0df002ce3c437455a32622649a07ee3a1eff4c2b4af98c88d9b230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72436c8cda53bcdd05471fceedac11c834d096d66224ee0104615fb5b4154481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e2d03046adad3006c011faddb7ef4a020b0b969d92b1620a35146c562412a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetric",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "container_resource": "containerResource",
        "external": "external",
        "object": "object",
        "pods": "pods",
        "resource": "resource",
    },
)
class HorizontalPodAutoscalerSpecMetric:
    def __init__(
        self,
        *,
        type: builtins.str,
        container_resource: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricContainerResource", typing.Dict[builtins.str, typing.Any]]] = None,
        external: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricExternal", typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricObject", typing.Dict[builtins.str, typing.Any]]] = None,
        pods: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricPods", typing.Dict[builtins.str, typing.Any]]] = None,
        resource: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: type is the type of metric source. It should be one of "ContainerResource", "External", "Object", "Pods" or "Resource", each mapping to a matching field in the object. Note: "ContainerResource" type is available on when the feature-gate HPAContainerMetrics is enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param container_resource: container_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#container_resource HorizontalPodAutoscaler#container_resource}
        :param external: external block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#external HorizontalPodAutoscaler#external}
        :param object: object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#object HorizontalPodAutoscaler#object}
        :param pods: pods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#pods HorizontalPodAutoscaler#pods}
        :param resource: resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#resource HorizontalPodAutoscaler#resource}
        '''
        if isinstance(container_resource, dict):
            container_resource = HorizontalPodAutoscalerSpecMetricContainerResource(**container_resource)
        if isinstance(external, dict):
            external = HorizontalPodAutoscalerSpecMetricExternal(**external)
        if isinstance(object, dict):
            object = HorizontalPodAutoscalerSpecMetricObject(**object)
        if isinstance(pods, dict):
            pods = HorizontalPodAutoscalerSpecMetricPods(**pods)
        if isinstance(resource, dict):
            resource = HorizontalPodAutoscalerSpecMetricResource(**resource)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ea7c526d002af5d1720f234dac3bf9a563a3b6c823f85c51912c8fd6424b6c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument container_resource", value=container_resource, expected_type=type_hints["container_resource"])
            check_type(argname="argument external", value=external, expected_type=type_hints["external"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument pods", value=pods, expected_type=type_hints["pods"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if container_resource is not None:
            self._values["container_resource"] = container_resource
        if external is not None:
            self._values["external"] = external
        if object is not None:
            self._values["object"] = object
        if pods is not None:
            self._values["pods"] = pods
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def type(self) -> builtins.str:
        '''type is the type of metric source.

        It should be one of "ContainerResource", "External", "Object", "Pods" or "Resource", each mapping to a matching field in the object. Note: "ContainerResource" type is available on when the feature-gate HPAContainerMetrics is enabled

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resource(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricContainerResource"]:
        '''container_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#container_resource HorizontalPodAutoscaler#container_resource}
        '''
        result = self._values.get("container_resource")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricContainerResource"], result)

    @builtins.property
    def external(self) -> typing.Optional["HorizontalPodAutoscalerSpecMetricExternal"]:
        '''external block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#external HorizontalPodAutoscaler#external}
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricExternal"], result)

    @builtins.property
    def object(self) -> typing.Optional["HorizontalPodAutoscalerSpecMetricObject"]:
        '''object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#object HorizontalPodAutoscaler#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricObject"], result)

    @builtins.property
    def pods(self) -> typing.Optional["HorizontalPodAutoscalerSpecMetricPods"]:
        '''pods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#pods HorizontalPodAutoscaler#pods}
        '''
        result = self._values.get("pods")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricPods"], result)

    @builtins.property
    def resource(self) -> typing.Optional["HorizontalPodAutoscalerSpecMetricResource"]:
        '''resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#resource HorizontalPodAutoscaler#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricResource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricContainerResource",
    jsii_struct_bases=[],
    name_mapping={"container": "container", "name": "name", "target": "target"},
)
class HorizontalPodAutoscalerSpecMetricContainerResource:
    def __init__(
        self,
        *,
        container: builtins.str,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricContainerResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: name of the container in the pods of the scaling target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#container HorizontalPodAutoscaler#container}
        :param name: name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerSpecMetricContainerResourceTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400dcf91f0f393a8e8441cf8b23d47dc595f67f658e0a57d013c0bb9026f4f45)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
            "name": name,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def container(self) -> builtins.str:
        '''name of the container in the pods of the scaling target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#container HorizontalPodAutoscaler#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''name of the resource in question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricContainerResourceTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricContainerResourceTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricContainerResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricContainerResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricContainerResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c33639843e8c48551422fc990856cdf7bb4b321a48a47eb7875683c7ff96993)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        value_ = HorizontalPodAutoscalerSpecMetricContainerResourceTarget(
            type=type,
            average_utilization=average_utilization,
            average_value=average_value,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerSpecMetricContainerResourceTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricContainerResourceTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricContainerResourceTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricContainerResourceTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fc5c5baf705fd4659743e041b19846dd9a2c2ae4a7833fd7eb36368864f4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bba7337708bbc327b7368cbb1ca49e3690336ab493e519af4d9ea1ce832f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4483cf90a5aada764ebc2f0fd74947ec18bd52214769740ff8292ccc9c9df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricContainerResourceTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerSpecMetricContainerResourceTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff61eb4be2f006f4ae5a95d1ff8da76f006cd3ac57eec973bef75b14ad0cb97e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument average_utilization", value=average_utilization, expected_type=type_hints["average_utilization"])
            check_type(argname="argument average_value", value=average_value, expected_type=type_hints["average_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if average_utilization is not None:
            self._values["average_utilization"] = average_utilization
        if average_value is not None:
            self._values["average_value"] = average_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''type represents whether the metric type is Utilization, Value, or AverageValue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricContainerResourceTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricContainerResourceTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricContainerResourceTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bcdb550ad8cd67e68665190d8493c30bbf08551a9584a1f710c72179291a0df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAverageUtilization")
    def reset_average_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageUtilization", []))

    @jsii.member(jsii_name="resetAverageValue")
    def reset_average_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="averageUtilizationInput")
    def average_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="averageValueInput")
    def average_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "averageValueInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="averageUtilization")
    def average_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageUtilization"))

    @average_utilization.setter
    def average_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07fddc4094f1001a512961ad86133d56d20a8d63ec027851483c521ab61e0d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f821a150896c39201cb4c61dbdc318609a0f99b84cbe2e8c03d26728daebc9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9025b76345448e3319b2d41ed99a0006ba1d5c11dd17dc30857d60b66ae9f3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15670a4f36120a7c0faaf62663bb64d787f0e43b3eccf5a15949ce1ef44e8058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResourceTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResourceTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResourceTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a580dcc9a5137f866523a72297e6303546019c8d29f6712cbf2893e5d8d96e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternal",
    jsii_struct_bases=[],
    name_mapping={"metric": "metric", "target": "target"},
)
class HorizontalPodAutoscalerSpecMetricExternal:
    def __init__(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerSpecMetricExternalMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricExternalTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerSpecMetricExternalMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerSpecMetricExternalTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1455207f926c576a3a149cd04d67740384f37c4bb602dc980ad215888ce1669d)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerSpecMetricExternalMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerSpecMetricExternalMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricExternalTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricExternalTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricExternal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerSpecMetricExternalMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricExternalMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61e7cd6b5d81827846a8f256c7ffcf73192cc1dff4624e10a06054fb84ed953)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if selector is not None:
            self._values["selector"] = selector

    @builtins.property
    def name(self) -> builtins.str:
        '''name is the name of the given metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricExternalMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricExternalMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricExternalMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricExternalMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__640fea169ffea647778831d98e27ccabc59f1e6fe9a64d62cd056301b189d134)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricExternalMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5aff0f5c5f82f8c462510226342946efa6b85c532ec478975e0d0a735e3c610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerSpecMetricExternalMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricExternalMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricExternalMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10f5dff15a226d6f2e8d11636c22366a29c12f31c999da502488ae526c51f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricExternalMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricExternalMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricExternalMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179767f4070bd10122e5d9c3e85cd6a05718a1482413f8caca6a4091c2a4ef95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerSpecMetricExternalMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_expressions HorizontalPodAutoscaler#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_labels HorizontalPodAutoscaler#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8aac30bc0f94ffc035f2b259df121117a5034cdee46ba0dddf5045355f9e6f)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_labels", value=match_labels, expected_type=type_hints["match_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_labels is not None:
            self._values["match_labels"] = match_labels

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_expressions HorizontalPodAutoscaler#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_labels HorizontalPodAutoscaler#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricExternalMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricExternalMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d31d2903d642ef33e70b1af0e21f69b19c2b47687d93e18def813c1dab1577b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0c973f659db8b15bf0e9585fc09e0504e8094d275f73d85dd787b960b2fd2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricExternalMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce0d18f4df97086c2862c45b46f184095e6360361ece4d6a972d6ef1075c7b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb14693386e1351de4960c9de2ae0a0ef8814a8b2e41acc3d882a9d729018206)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da22eba6997d2ce5c85c26c0516a1366ba9cda8196870fb27ee72fa8920a89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54408b82fc1871abc3d557e199cc573abe20981e87331b675985c64539db2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#key HorizontalPodAutoscaler#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#operator HorizontalPodAutoscaler#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#values HorizontalPodAutoscaler#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eee6d55b98ea1253baf6ad25168d4cb1b892972ec927937babc614652bb52bf)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#key HorizontalPodAutoscaler#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#operator HorizontalPodAutoscaler#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#values HorizontalPodAutoscaler#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5315cacb69d542161d81ddbfe80e97bbcbbf273d00f86da3bb4e2a10ded78e70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafd6f8edc146fcba183680aba24fb6ecc067781ca38b9a98dcdf1287128e6d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00f19b88fc30be5d1fa66f41a26573037213edd2bbc0dba5895a8cf66563870)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1498aefb47ffde29615f11623b1e945344270741e11987be51468ee7d5747215)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98739ec27f3b41534538669f3abde54cfd6df4af4a70e4fbe38590a473458a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f171b7673524e917952fca35d9ae5cfa8372261e31d75a01dad030290561c817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0836c61261d1cf351e1a0850859bb648454b8c15b2d4d2072af10ff4ead9d9a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c16ecc736256a60856e5ad6947c8b36f190963b1db085dd335dfdbc889bf8bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241ee111f390d1efaec2084de5a93971a50ecff9163452ca9f56cc39727e68cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47f0c49613fda9fb49f90cc5c60e48d497f09e661501ed49b204f4dcb0f22d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0761c585bb938abdb87b66fa03a297c47ebff1096d97952d02fb7c47f2dd4e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricExternalMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3c0a63555433179190a75cc27697e3745c349761b01c168a05fad755cd48308)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408152b775458e10d356618b5e81958e5037761a7963bc16b727af3e6e27b50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchExpressions", [value]))

    @jsii.member(jsii_name="resetMatchExpressions")
    def reset_match_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchExpressions", []))

    @jsii.member(jsii_name="resetMatchLabels")
    def reset_match_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabels", []))

    @builtins.property
    @jsii.member(jsii_name="matchExpressions")
    def match_expressions(
        self,
    ) -> HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelsInput")
    def match_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "matchLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabels")
    def match_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "matchLabels"))

    @match_labels.setter
    def match_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbc2a6c7b994e7acb340b2092c9358dd627aba6218dcbcc9b6517f177f77e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35d9e519058dbf402703c2288f77aa7c4607761ab749cabdb2e80c88521e600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricExternalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8968140552c301cb87bac0fcdaa877228f8dc6dd5aa8046197b40825bad5b779)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        value = HorizontalPodAutoscalerSpecMetricExternalMetric(
            name=name, selector=selector
        )

        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        value_ = HorizontalPodAutoscalerSpecMetricExternalTarget(
            type=type,
            average_utilization=average_utilization,
            average_value=average_value,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerSpecMetricExternalMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricExternalMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerSpecMetricExternalTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricExternalTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricExternalMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricExternalMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricExternalTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricExternalTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricExternal]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricExternal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricExternal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95862d239439e91e87a50aa3f243ed0f1d0275819c0767730159484080bbbbfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerSpecMetricExternalTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bde13e4c04cc3927468d1c30d407f4e362a4a694225291e66905f626186be0)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument average_utilization", value=average_utilization, expected_type=type_hints["average_utilization"])
            check_type(argname="argument average_value", value=average_value, expected_type=type_hints["average_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if average_utilization is not None:
            self._values["average_utilization"] = average_utilization
        if average_value is not None:
            self._values["average_value"] = average_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''type represents whether the metric type is Utilization, Value, or AverageValue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricExternalTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricExternalTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricExternalTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1166772c671f3ee6b217a947e404e98275d6e39f2798e1c139161dc3216f9208)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAverageUtilization")
    def reset_average_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageUtilization", []))

    @jsii.member(jsii_name="resetAverageValue")
    def reset_average_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="averageUtilizationInput")
    def average_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="averageValueInput")
    def average_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "averageValueInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="averageUtilization")
    def average_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageUtilization"))

    @average_utilization.setter
    def average_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d093612bcaf33bf91cdf3a42c05991e8d6482a1ce95d3597554abe615e436e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c989a7fabd50fe0a67a2b0e166e4708f982d400e62cc24bc47536ab15089bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64af7c6620d30cfd718a80064488f9f2a009a0750d06a0fcbfb45f2fd16c0c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5baffc4898e3de7d9dd51aa44f9e359e80a1b1d1517f13f5166ac8b7175bad6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricExternalTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricExternalTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricExternalTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8cb216240a64ac33cc493697b8d10ec1346f02c75203923a8e2088cf8b0d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e92918650cb0c03d54f997e1d05eea5666e2fe7491254cc02af88ff767cee112)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e40a8cbc79052b82f194021c7e46970606ef5c08878056ba84f15cb7228966)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8541816f56304dbd0205cc06a0b4c581ea591d33355e4cedc7b6d0c475d7e577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92038f94e8ece79cce2654be7969dcb6abe88c18086f702965cbcfb24212c577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b082e13ca5b09eb48725b34b60f42c2ecffa242823d19a295026a0103f2b22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bcd0a5ff3e5d45040d21a0daa2dfb83cbdc45db9253221c6755d1187ed4b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObject",
    jsii_struct_bases=[],
    name_mapping={
        "described_object": "describedObject",
        "metric": "metric",
        "target": "target",
    },
)
class HorizontalPodAutoscalerSpecMetricObject:
    def __init__(
        self,
        *,
        described_object: typing.Union["HorizontalPodAutoscalerSpecMetricObjectDescribedObject", typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union["HorizontalPodAutoscalerSpecMetricObjectMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricObjectTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param described_object: described_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#described_object HorizontalPodAutoscaler#described_object}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        if isinstance(described_object, dict):
            described_object = HorizontalPodAutoscalerSpecMetricObjectDescribedObject(**described_object)
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerSpecMetricObjectMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerSpecMetricObjectTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc162bbf92942238f0ceaff6e825128bef680ec884cff10584475de0d22f139)
            check_type(argname="argument described_object", value=described_object, expected_type=type_hints["described_object"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "described_object": described_object,
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def described_object(
        self,
    ) -> "HorizontalPodAutoscalerSpecMetricObjectDescribedObject":
        '''described_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#described_object HorizontalPodAutoscaler#described_object}
        '''
        result = self._values.get("described_object")
        assert result is not None, "Required property 'described_object' is missing"
        return typing.cast("HorizontalPodAutoscalerSpecMetricObjectDescribedObject", result)

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerSpecMetricObjectMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerSpecMetricObjectMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricObjectTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricObjectTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectDescribedObject",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "kind": "kind", "name": "name"},
)
class HorizontalPodAutoscalerSpecMetricObjectDescribedObject:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#api_version HorizontalPodAutoscaler#api_version}
        :param kind: Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#kind HorizontalPodAutoscaler#kind}
        :param name: Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934171abd418c21f6ed422668bdf2425eaf8ff5ad7a5bd210dae1cab7d3a6ae3)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_version": api_version,
            "kind": kind,
            "name": name,
        }

    @builtins.property
    def api_version(self) -> builtins.str:
        '''API version of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#api_version HorizontalPodAutoscaler#api_version}
        '''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#kind HorizontalPodAutoscaler#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricObjectDescribedObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricObjectDescribedObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectDescribedObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa584c54961cf28759bbf3203eceacf8ccc66204f47e3d0645732024e9f79a79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2242c6433e722f8f2b427bb01dbef432cecd13d14a17398e489e805a6e54d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6e1b14ab5636547fa91d2f24e6647850e85bbd3bb85cf342df05ed40520520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379981bbfcc1568c8b9b6d84aa3143b9bdec90ea8e9067c0cd206226c1394fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObjectDescribedObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObjectDescribedObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricObjectDescribedObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96021d0c69b928de78dd3b7d93e8627daf9db3b697bb7944e5c65a00ef6162da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerSpecMetricObjectMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricObjectMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2757e6f7d5494c18ae403859c8c55c58e1c4549d1c5b0ca783e02ecc335c43)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if selector is not None:
            self._values["selector"] = selector

    @builtins.property
    def name(self) -> builtins.str:
        '''name is the name of the given metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricObjectMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricObjectMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricObjectMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricObjectMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__faa7a50eef8dbbd303755bf17751c62b771114bfc5e781d000b3916fc1f0fe9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricObjectMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49514718b1311799ae2f045e53e8d5f03b539564fc8228ad67257a4960675c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerSpecMetricObjectMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricObjectMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricObjectMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc069ba028ef3d59ebda973cc018599cc96626bb4019265ff455a9c99f7a999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObjectMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObjectMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricObjectMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444043f9e3fe26cf65af82ea40dd14c273d6fdb0394a9e9f3057acda335cb521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerSpecMetricObjectMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_expressions HorizontalPodAutoscaler#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_labels HorizontalPodAutoscaler#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eedfbbc21776905cf3c5a47d7e7c865d872cf78312c0ae0e7909ee07deb715a)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_labels", value=match_labels, expected_type=type_hints["match_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_labels is not None:
            self._values["match_labels"] = match_labels

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_expressions HorizontalPodAutoscaler#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_labels HorizontalPodAutoscaler#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricObjectMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricObjectMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a5543fbb2fb92ec7992332b40a2c6d78ac1d7a90686cf87dac6590237ad7be4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6532dfc131db7fa7cf9a1a0edf3f7e196944ab3651ff1ccaef5e04d8b6da773)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricObjectMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01e87e99b1d2f5ab8840f10d933ecbdfe3cdb1e8d58a9dec01f5945d29f311b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b51d87febcdede346c93a3e49265cbc0b06be522cdb84d1a99555e48d230f100)
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
            type_hints = typing.get_type_hints(_typecheckingstub__694829f178a3c737d7efaa55bc227037add28903d5a037871a729b2f20cac8b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f39438d3429f6c4e3ca197a38eba4ea97aa001295e9c8d919311163d4ce421d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#key HorizontalPodAutoscaler#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#operator HorizontalPodAutoscaler#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#values HorizontalPodAutoscaler#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cc0175608419aaa6c3921066f14c6918e91afb587bf7104925303388186057)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#key HorizontalPodAutoscaler#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#operator HorizontalPodAutoscaler#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#values HorizontalPodAutoscaler#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17c6d61c2e51d945f34d983eb2d01dbe4302d25994137579e16858ee8cd4268b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb41e68f649bad3de334b0fd6006d4a40361427fa8f5e7fc56eec7ae6ef55861)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84a3177e429657cdfa2deaee9891ae8b5deaba5c54e237d9ee6d4cabb1ede85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45dbf6a896d716c8f3ae5ef524caa24496b31e71c0bfd182da7301e7a14924ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeebdf8009d393f9f11e9b42fff56f8f16ef23698898a0afb75ea4660f74ecb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b04e86dc1f46e05da98392cc4c940f88c62c263eed3d332256f8557427be37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__016744d8b0ccdb135c61c05d25fab529dac15b73791113d693933e7baba992a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__04ae1c34aaed9aa566ab398357f3c71ab4798d7577829ee3fe6a6ff10ec1251e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3536bfe601fcfbd16ec96e841da009a78e4dcd645e600a1d7bd6f5d863c36c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacaba02f14fb878361faa7a576e55dfb080e556bf966d47c21ad36cc9ed085e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8197f72fdc38b15d23b21c278c6829cde2ee56e9534ea37281ba690bc46e43ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricObjectMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__505d270df4390281069baacb7d91d8ffe7a1ba8df72029d1d271c35a6127dcad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd810b9768340e6f833ed681849731386f1ee3579521498e3f83f7c21d46291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchExpressions", [value]))

    @jsii.member(jsii_name="resetMatchExpressions")
    def reset_match_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchExpressions", []))

    @jsii.member(jsii_name="resetMatchLabels")
    def reset_match_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabels", []))

    @builtins.property
    @jsii.member(jsii_name="matchExpressions")
    def match_expressions(
        self,
    ) -> HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelsInput")
    def match_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "matchLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabels")
    def match_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "matchLabels"))

    @match_labels.setter
    def match_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc87d57cfc423d915d784cbcf1e62d295c8c44aaf7b0a20026de28fc835ba185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7442f62eb00f1c157a90617b0d02912c17bf92b79e81b9af75205c2853761623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63d05f6161120da6586d14ded76e6c0d59968264b23c808af0aaf81819bed31e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDescribedObject")
    def put_described_object(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#api_version HorizontalPodAutoscaler#api_version}
        :param kind: Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#kind HorizontalPodAutoscaler#kind}
        :param name: Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        value = HorizontalPodAutoscalerSpecMetricObjectDescribedObject(
            api_version=api_version, kind=kind, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putDescribedObject", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        value = HorizontalPodAutoscalerSpecMetricObjectMetric(
            name=name, selector=selector
        )

        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        value_ = HorizontalPodAutoscalerSpecMetricObjectTarget(
            type=type,
            average_utilization=average_utilization,
            average_value=average_value,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="describedObject")
    def described_object(
        self,
    ) -> HorizontalPodAutoscalerSpecMetricObjectDescribedObjectOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricObjectDescribedObjectOutputReference, jsii.get(self, "describedObject"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerSpecMetricObjectMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricObjectMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "HorizontalPodAutoscalerSpecMetricObjectTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricObjectTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="describedObjectInput")
    def described_object_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObjectDescribedObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObjectDescribedObject], jsii.get(self, "describedObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObjectMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObjectMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricObjectTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricObjectTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46ec48a453c63774522c92cd94e38ba1d6cf5244cbc5307fb8f5a98fc8cd625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerSpecMetricObjectTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978fce1aa0e6f26a723ba5cd3722805c0f952623bfb7c3c8df0502a3f771a8ca)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument average_utilization", value=average_utilization, expected_type=type_hints["average_utilization"])
            check_type(argname="argument average_value", value=average_value, expected_type=type_hints["average_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if average_utilization is not None:
            self._values["average_utilization"] = average_utilization
        if average_value is not None:
            self._values["average_value"] = average_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''type represents whether the metric type is Utilization, Value, or AverageValue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricObjectTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricObjectTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricObjectTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63164e681d1f2520b68df21a92bd8c46e610e9d61d7a562510cb6ded1ba9c736)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAverageUtilization")
    def reset_average_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageUtilization", []))

    @jsii.member(jsii_name="resetAverageValue")
    def reset_average_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="averageUtilizationInput")
    def average_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="averageValueInput")
    def average_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "averageValueInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="averageUtilization")
    def average_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageUtilization"))

    @average_utilization.setter
    def average_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf29c4d9bb9670bf58ea61f62fb9a6cf966274ab9143dc38408e65cfc617d1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e8f160a24dfa049dece8a335c02f9ad50db07f300954db30ca6c6f3fdf8ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9e2ab24f2d5528da3c0387adedda84fbc0ccf2e9540c9f109ee5f0472f6120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c962375c56a95b65c41d24a500e052598c81260a19924daf7bf20b8602329f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObjectTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObjectTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricObjectTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605abe70bf262c453ec1e964e3b17f1a594955a932e99e09294b154c194db599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10d2bae0b8be83844f240a46fc066e53531ee9fc5b74d1bd63c08429152621c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainerResource")
    def put_container_resource(
        self,
        *,
        container: builtins.str,
        name: builtins.str,
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricContainerResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: name of the container in the pods of the scaling target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#container HorizontalPodAutoscaler#container}
        :param name: name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        value = HorizontalPodAutoscalerSpecMetricContainerResource(
            container=container, name=name, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResource", [value]))

    @jsii.member(jsii_name="putExternal")
    def put_external(
        self,
        *,
        metric: typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetric, typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricExternalTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        value = HorizontalPodAutoscalerSpecMetricExternal(metric=metric, target=target)

        return typing.cast(None, jsii.invoke(self, "putExternal", [value]))

    @jsii.member(jsii_name="putObject")
    def put_object(
        self,
        *,
        described_object: typing.Union[HorizontalPodAutoscalerSpecMetricObjectDescribedObject, typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetric, typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricObjectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param described_object: described_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#described_object HorizontalPodAutoscaler#described_object}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        value = HorizontalPodAutoscalerSpecMetricObject(
            described_object=described_object, metric=metric, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putObject", [value]))

    @jsii.member(jsii_name="putPods")
    def put_pods(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerSpecMetricPodsMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricPodsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        value = HorizontalPodAutoscalerSpecMetricPods(metric=metric, target=target)

        return typing.cast(None, jsii.invoke(self, "putPods", [value]))

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        *,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        value = HorizontalPodAutoscalerSpecMetricResource(name=name, target=target)

        return typing.cast(None, jsii.invoke(self, "putResource", [value]))

    @jsii.member(jsii_name="resetContainerResource")
    def reset_container_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerResource", []))

    @jsii.member(jsii_name="resetExternal")
    def reset_external(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternal", []))

    @jsii.member(jsii_name="resetObject")
    def reset_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObject", []))

    @jsii.member(jsii_name="resetPods")
    def reset_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPods", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="containerResource")
    def container_resource(
        self,
    ) -> HorizontalPodAutoscalerSpecMetricContainerResourceOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricContainerResourceOutputReference, jsii.get(self, "containerResource"))

    @builtins.property
    @jsii.member(jsii_name="external")
    def external(self) -> HorizontalPodAutoscalerSpecMetricExternalOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricExternalOutputReference, jsii.get(self, "external"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> HorizontalPodAutoscalerSpecMetricObjectOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricObjectOutputReference, jsii.get(self, "object"))

    @builtins.property
    @jsii.member(jsii_name="pods")
    def pods(self) -> "HorizontalPodAutoscalerSpecMetricPodsOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricPodsOutputReference", jsii.get(self, "pods"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "HorizontalPodAutoscalerSpecMetricResourceOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricResourceOutputReference", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="containerResourceInput")
    def container_resource_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResource], jsii.get(self, "containerResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="externalInput")
    def external_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricExternal]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricExternal], jsii.get(self, "externalInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[HorizontalPodAutoscalerSpecMetricObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricObject], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="podsInput")
    def pods_input(self) -> typing.Optional["HorizontalPodAutoscalerSpecMetricPods"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricPods"], jsii.get(self, "podsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricResource"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricResource"], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e76f5f959e538735676ec91fc9e0db58c1ecb0f58ab3f8499dc539d2281b4d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83095bfc3b2b7b7965149a9c6d179a25c13ed9b17dfe94e50bc6e8fde643390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPods",
    jsii_struct_bases=[],
    name_mapping={"metric": "metric", "target": "target"},
)
class HorizontalPodAutoscalerSpecMetricPods:
    def __init__(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerSpecMetricPodsMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricPodsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerSpecMetricPodsMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerSpecMetricPodsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f43532e83a7287c974125dcb1a6e52b31cad43cf198bd3ca8fd3f91a3b20a67)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerSpecMetricPodsMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#metric HorizontalPodAutoscaler#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerSpecMetricPodsMetric", result)

    @builtins.property
    def target(self) -> typing.Optional["HorizontalPodAutoscalerSpecMetricPodsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricPodsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricPods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerSpecMetricPodsMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricPodsMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce11faab1c0a982586e382c066c81472ef30cd6f3cb7b03fb501676ced0e0c20)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if selector is not None:
            self._values["selector"] = selector

    @builtins.property
    def name(self) -> builtins.str:
        '''name is the name of the given metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricPodsMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricPodsMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricPodsMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricPodsMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d458c71d0111fdc775cb55d229caf19cf923e4a21ff1fd3068ae45b9d624ac2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricPodsMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b96756aa28cfe6346b1b499bc5ec93d0a5130a13893e6f9023ae3ba621e364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerSpecMetricPodsMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricPodsMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricPodsMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973ac1f5c511f1a87e29f6cc227e4103c85ffcff7ff12422b68cd7eaf7b5122c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricPodsMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricPodsMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricPodsMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc167c025a3e8ee79bb8da9f7890355d4cdaa6d7a6dc23b67f01800c9659e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerSpecMetricPodsMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_expressions HorizontalPodAutoscaler#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_labels HorizontalPodAutoscaler#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ad2cff6fc367fd9211f5301ba28e16de5cddb099e7860c0459b0fd4ca65ac5)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_labels", value=match_labels, expected_type=type_hints["match_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_labels is not None:
            self._values["match_labels"] = match_labels

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_expressions HorizontalPodAutoscaler#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#match_labels HorizontalPodAutoscaler#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricPodsMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricPodsMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__107b0554e60671156d7771af8a1df69bdf799ab8f5b1bf0a777640dbde5b764d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85ac496810921b0d5b56d2c017a9a84092f0b63d1f20b93790cb8cf83d176e4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricPodsMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d27635d572cc03e584cf5eca49c399b97f2e25267a0c52e592e93be1540ad5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7a481ec21f4d2ddc94e7b7393014476a958d32a36c9dde21e3e1de404010bde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f66b11c361629f1194d9f0464abe27365fda6eca9645171088901a21a1451e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d939cf57c142cf96f94699820fe783dc41ef5b2930b02e60d71d7feacf627f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#key HorizontalPodAutoscaler#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#operator HorizontalPodAutoscaler#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#values HorizontalPodAutoscaler#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29cd4a477439fa05c3c9f496d17feb18d56021cd25b5bcd9788abf449937a6d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#key HorizontalPodAutoscaler#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#operator HorizontalPodAutoscaler#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#values HorizontalPodAutoscaler#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e625487492df595c683add16da23b6a96eec93a542f24b64b3f1e441558bf969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cff6563f041aef683fef43a5d2817638821d58d2ea3fe62f11a8a1d72932c14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c80c2420a1fd899acc51d89a9bd3096f03375cf4d2fca9ddfc73e2927f31bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de418159736f805fa6e65a0b9b45b2918a4f42995b898a9db4058f8d9e124881)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ef423ed8caaa926ac5636370fc0e4b241166a8692664ca210da40173f56e402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46bb41e1fa483515027a2010e83d962cb003f6ff628912d16b77ecc26df0f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baf8b6c5533310fadd0c268e617ae142c0eae733014e2afd1e2f8a707d931031)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ebbd2fc71d808ed7250b071e0299665aa1c4d2c33264228c2baa9ab7db2490b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1022960c9d9b6db0c5eef3008ea733e83bdb1bbef76929528f7f36601ab746ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab8b630d4ff59bf2dda239ef5782fe42bd69d319b91a40c18057d67d4c1af03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed39e54d4aaec95c79cd2e29d1b447d57cfec1afaf709f49a20a38b3c1ab3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricPodsMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc7ae826977c187d8ca4fe53321c93d2b2865c1795a79960222e7257bacf928)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6eb0aae0264510e71b189928231c713a05ddd41f1cf39077a61156cc907d449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchExpressions", [value]))

    @jsii.member(jsii_name="resetMatchExpressions")
    def reset_match_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchExpressions", []))

    @jsii.member(jsii_name="resetMatchLabels")
    def reset_match_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabels", []))

    @builtins.property
    @jsii.member(jsii_name="matchExpressions")
    def match_expressions(
        self,
    ) -> HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelsInput")
    def match_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "matchLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabels")
    def match_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "matchLabels"))

    @match_labels.setter
    def match_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beef4caccd4cd6821a6d9e10553953628f9ba969fdde56473fb779448fc6eb91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31124ae5929b0d268b4990ec6110eb58d22a7262684af76c0805d27d94089ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecMetricPodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02f512f616754585a1043d737e3b77130e98dd75d78d62d8e31625c584e7f13a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#selector HorizontalPodAutoscaler#selector}
        '''
        value = HorizontalPodAutoscalerSpecMetricPodsMetric(
            name=name, selector=selector
        )

        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        value_ = HorizontalPodAutoscalerSpecMetricPodsTarget(
            type=type,
            average_utilization=average_utilization,
            average_value=average_value,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerSpecMetricPodsMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecMetricPodsMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "HorizontalPodAutoscalerSpecMetricPodsTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricPodsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricPodsMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricPodsMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricPodsTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricPodsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerSpecMetricPods]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricPods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricPods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839fd8360be4b6c9587dcdbdc44ea397ab8b99b8fdac13755a0ad17a3ba6ea69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerSpecMetricPodsTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1551ead0f16b18b53162a0e86cacd7ebf359b5cdbca41c511c1ecf43a095a73f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument average_utilization", value=average_utilization, expected_type=type_hints["average_utilization"])
            check_type(argname="argument average_value", value=average_value, expected_type=type_hints["average_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if average_utilization is not None:
            self._values["average_utilization"] = average_utilization
        if average_value is not None:
            self._values["average_value"] = average_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''type represents whether the metric type is Utilization, Value, or AverageValue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricPodsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricPodsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricPodsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e65d63e7e9e4cc53ac397a6be36ca967a9122a26cde200bb50fc97eadc757c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAverageUtilization")
    def reset_average_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageUtilization", []))

    @jsii.member(jsii_name="resetAverageValue")
    def reset_average_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="averageUtilizationInput")
    def average_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="averageValueInput")
    def average_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "averageValueInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="averageUtilization")
    def average_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageUtilization"))

    @average_utilization.setter
    def average_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f205110b5489f270e0296d33cbb8d51eff53a382f76797435e28bbde7d7aa6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9644862928599a7e6eab369b99f692fab5db0c1c8e5068a8c2ee826953e71ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3503b0747e171e7aa506ba966a06e0913375d2ef90203ec817d52ea6c514c087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3ca3895e733a673dcbba761cc5814a5c62ef580aa5e3a96d9d7494ef77da2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricPodsTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricPodsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricPodsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740b1ed410370b5968999521a90f745dec4d5b7474ac80748f2d90e7c2485f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricResource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "target": "target"},
)
class HorizontalPodAutoscalerSpecMetricResource:
    def __init__(
        self,
        *,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerSpecMetricResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerSpecMetricResourceTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1aed86b2aff3d5d1dd97e6389156d76e1a38fef3faa49bbfffb3639d0b0f911)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def name(self) -> builtins.str:
        '''name is the name of the resource in question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricResourceTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#target HorizontalPodAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricResourceTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68371d847355e7798e794b04030d480088b5452ad6c3d95019a853c8e3e2b3eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        value_ = HorizontalPodAutoscalerSpecMetricResourceTarget(
            type=type,
            average_utilization=average_utilization,
            average_value=average_value,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerSpecMetricResourceTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecMetricResourceTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecMetricResourceTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecMetricResourceTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28bdc74c443ac99186328f91a153d606e204166621e98f9bef8e680bd740cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db211e20778339a67d394c7c6468a89e23a4e717a2ce28fbbf858b83136adc4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricResourceTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerSpecMetricResourceTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe5e8ced2c30bd5f5b95005066658eff1eff0239478f65ec4bea5ab6508b5e5)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument average_utilization", value=average_utilization, expected_type=type_hints["average_utilization"])
            check_type(argname="argument average_value", value=average_value, expected_type=type_hints["average_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if average_utilization is not None:
            self._values["average_utilization"] = average_utilization
        if average_value is not None:
            self._values["average_value"] = average_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''type represents whether the metric type is Utilization, Value, or AverageValue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#type HorizontalPodAutoscaler#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_utilization HorizontalPodAutoscaler#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#average_value HorizontalPodAutoscaler#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#value HorizontalPodAutoscaler#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecMetricResourceTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecMetricResourceTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecMetricResourceTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c97882dab74377b398a7c6188e751ae7281447706a8c6e147e546c4c4de98f2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAverageUtilization")
    def reset_average_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageUtilization", []))

    @jsii.member(jsii_name="resetAverageValue")
    def reset_average_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="averageUtilizationInput")
    def average_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="averageValueInput")
    def average_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "averageValueInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="averageUtilization")
    def average_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageUtilization"))

    @average_utilization.setter
    def average_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1f0030cb3f41ee9663d833fbd8675d93f6831ea7333fdf9757dbaf5be0386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7679bc0348dce1a88107931e667bd54fa52a457bfeeb16eca914ec2493185ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8befa572748fedbcdf3660002e3cace47ae45b36e4571d07bf10522f7eacb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab84ab8a58692b8ec41bbf54ec987af36d311c91387f927a9f7b8a569539051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecMetricResourceTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecMetricResourceTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecMetricResourceTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d7b7fe17593c120262f49c99b8d077c1c1d21f365fd64adfcfeb9e936f1f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e261021721d934f8bafd40e79ff0f89635fdf7cbd37c0dd8f6058438e31ee4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBehavior")
    def put_behavior(
        self,
        *,
        scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]]] = None,
        scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scale_down: scale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_down HorizontalPodAutoscaler#scale_down}
        :param scale_up: scale_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#scale_up HorizontalPodAutoscaler#scale_up}
        '''
        value = HorizontalPodAutoscalerSpecBehavior(
            scale_down=scale_down, scale_up=scale_up
        )

        return typing.cast(None, jsii.invoke(self, "putBehavior", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42b8dd8018639d46a0da647c0034cf7c3f50fc3ab7416dddd39736bdaa75995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putScaleTargetRef")
    def put_scale_target_ref(
        self,
        *,
        kind: builtins.str,
        name: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#kind HorizontalPodAutoscaler#kind}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#api_version HorizontalPodAutoscaler#api_version}
        '''
        value = HorizontalPodAutoscalerSpecScaleTargetRef(
            kind=kind, name=name, api_version=api_version
        )

        return typing.cast(None, jsii.invoke(self, "putScaleTargetRef", [value]))

    @jsii.member(jsii_name="resetBehavior")
    def reset_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBehavior", []))

    @jsii.member(jsii_name="resetMetric")
    def reset_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetric", []))

    @jsii.member(jsii_name="resetMinReplicas")
    def reset_min_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReplicas", []))

    @jsii.member(jsii_name="resetTargetCpuUtilizationPercentage")
    def reset_target_cpu_utilization_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCpuUtilizationPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> HorizontalPodAutoscalerSpecBehaviorOutputReference:
        return typing.cast(HorizontalPodAutoscalerSpecBehaviorOutputReference, jsii.get(self, "behavior"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerSpecMetricList:
        return typing.cast(HorizontalPodAutoscalerSpecMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleTargetRef")
    def scale_target_ref(
        self,
    ) -> "HorizontalPodAutoscalerSpecScaleTargetRefOutputReference":
        return typing.cast("HorizontalPodAutoscalerSpecScaleTargetRefOutputReference", jsii.get(self, "scaleTargetRef"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[HorizontalPodAutoscalerSpecBehavior]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecBehavior], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetric]]], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleTargetRefInput")
    def scale_target_ref_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerSpecScaleTargetRef"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerSpecScaleTargetRef"], jsii.get(self, "scaleTargetRefInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilizationPercentageInput")
    def target_cpu_utilization_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetCpuUtilizationPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3121ff98a5d3ed8f23cd3c0d7f2afe37e3b3e2568a7fee1dc9c996b86cc411c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72fdeae21cfd226069f720754b99f5edb6b78c02af64ad065d2e7f2fd425e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilizationPercentage")
    def target_cpu_utilization_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetCpuUtilizationPercentage"))

    @target_cpu_utilization_percentage.setter
    def target_cpu_utilization_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64efa9001192a1767726cc5e2e36fc2d9a56aaed26c9376c3f26930b4a9fea2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCpuUtilizationPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerSpec]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de556c2b0d148087ec1caa3f0b61d70c6d5a647c2ac04b2acb574c7a23bbf783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecScaleTargetRef",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "name": "name", "api_version": "apiVersion"},
)
class HorizontalPodAutoscalerSpecScaleTargetRef:
    def __init__(
        self,
        *,
        kind: builtins.str,
        name: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#kind HorizontalPodAutoscaler#kind}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#api_version HorizontalPodAutoscaler#api_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e105f18d4edcac2c9c86ff0d735aba9faa40eb8096000dd3884805223e5ad6)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
            "name": name,
        }
        if api_version is not None:
            self._values["api_version"] = api_version

    @builtins.property
    def kind(self) -> builtins.str:
        '''Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#kind HorizontalPodAutoscaler#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#name HorizontalPodAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''API version of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler#api_version HorizontalPodAutoscaler#api_version}
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerSpecScaleTargetRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerSpecScaleTargetRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscaler.HorizontalPodAutoscalerSpecScaleTargetRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c310d86364862d43ac79872289d033f91fcfe7abbaf1cdb559cca02e52234a4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c0c95a2016fba367072815bbec0b497ceb89d5ae53e3c9b6e4d9cabbdb2c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b531629610ed214bf8e9d772c8f302aac9485c96a3ef7afe9e74e48a697295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9490e8e5f52920a51ad9dc34b24e9d690ad19e68fcbcd902f1be204c5bb008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerSpecScaleTargetRef]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerSpecScaleTargetRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerSpecScaleTargetRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167465f10c51a9eee57aa206950fd36ee3e37a4d13b5998b71e99d542af6f8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HorizontalPodAutoscaler",
    "HorizontalPodAutoscalerConfig",
    "HorizontalPodAutoscalerMetadata",
    "HorizontalPodAutoscalerMetadataOutputReference",
    "HorizontalPodAutoscalerSpec",
    "HorizontalPodAutoscalerSpecBehavior",
    "HorizontalPodAutoscalerSpecBehaviorOutputReference",
    "HorizontalPodAutoscalerSpecBehaviorScaleDown",
    "HorizontalPodAutoscalerSpecBehaviorScaleDownList",
    "HorizontalPodAutoscalerSpecBehaviorScaleDownOutputReference",
    "HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy",
    "HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyList",
    "HorizontalPodAutoscalerSpecBehaviorScaleDownPolicyOutputReference",
    "HorizontalPodAutoscalerSpecBehaviorScaleUp",
    "HorizontalPodAutoscalerSpecBehaviorScaleUpList",
    "HorizontalPodAutoscalerSpecBehaviorScaleUpOutputReference",
    "HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy",
    "HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyList",
    "HorizontalPodAutoscalerSpecBehaviorScaleUpPolicyOutputReference",
    "HorizontalPodAutoscalerSpecMetric",
    "HorizontalPodAutoscalerSpecMetricContainerResource",
    "HorizontalPodAutoscalerSpecMetricContainerResourceOutputReference",
    "HorizontalPodAutoscalerSpecMetricContainerResourceTarget",
    "HorizontalPodAutoscalerSpecMetricContainerResourceTargetOutputReference",
    "HorizontalPodAutoscalerSpecMetricExternal",
    "HorizontalPodAutoscalerSpecMetricExternalMetric",
    "HorizontalPodAutoscalerSpecMetricExternalMetricOutputReference",
    "HorizontalPodAutoscalerSpecMetricExternalMetricSelector",
    "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorList",
    "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerSpecMetricExternalMetricSelectorOutputReference",
    "HorizontalPodAutoscalerSpecMetricExternalOutputReference",
    "HorizontalPodAutoscalerSpecMetricExternalTarget",
    "HorizontalPodAutoscalerSpecMetricExternalTargetOutputReference",
    "HorizontalPodAutoscalerSpecMetricList",
    "HorizontalPodAutoscalerSpecMetricObject",
    "HorizontalPodAutoscalerSpecMetricObjectDescribedObject",
    "HorizontalPodAutoscalerSpecMetricObjectDescribedObjectOutputReference",
    "HorizontalPodAutoscalerSpecMetricObjectMetric",
    "HorizontalPodAutoscalerSpecMetricObjectMetricOutputReference",
    "HorizontalPodAutoscalerSpecMetricObjectMetricSelector",
    "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorList",
    "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerSpecMetricObjectMetricSelectorOutputReference",
    "HorizontalPodAutoscalerSpecMetricObjectOutputReference",
    "HorizontalPodAutoscalerSpecMetricObjectTarget",
    "HorizontalPodAutoscalerSpecMetricObjectTargetOutputReference",
    "HorizontalPodAutoscalerSpecMetricOutputReference",
    "HorizontalPodAutoscalerSpecMetricPods",
    "HorizontalPodAutoscalerSpecMetricPodsMetric",
    "HorizontalPodAutoscalerSpecMetricPodsMetricOutputReference",
    "HorizontalPodAutoscalerSpecMetricPodsMetricSelector",
    "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorList",
    "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerSpecMetricPodsMetricSelectorOutputReference",
    "HorizontalPodAutoscalerSpecMetricPodsOutputReference",
    "HorizontalPodAutoscalerSpecMetricPodsTarget",
    "HorizontalPodAutoscalerSpecMetricPodsTargetOutputReference",
    "HorizontalPodAutoscalerSpecMetricResource",
    "HorizontalPodAutoscalerSpecMetricResourceOutputReference",
    "HorizontalPodAutoscalerSpecMetricResourceTarget",
    "HorizontalPodAutoscalerSpecMetricResourceTargetOutputReference",
    "HorizontalPodAutoscalerSpecOutputReference",
    "HorizontalPodAutoscalerSpecScaleTargetRef",
    "HorizontalPodAutoscalerSpecScaleTargetRefOutputReference",
]

publication.publish()

def _typecheckingstub__f3204788aa482b9bc5577cc97d383bea14289372d47f3c887866c1364b1db3b6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[HorizontalPodAutoscalerMetadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[HorizontalPodAutoscalerSpec, typing.Dict[builtins.str, typing.Any]],
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

def _typecheckingstub__5de6ca68e79c8c1dcf44a0eb4594e25f4f2bf8c3b527ba97c72b9fb9c5bd4cf1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e36b78af617bbf9e9bd52282790de4f842b3bc9ec6261b82ecc9450287adee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaecd39a76273a9a9ef0d14852a138b61f2d4d288344528367fcfc7a716bac61(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[HorizontalPodAutoscalerMetadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[HorizontalPodAutoscalerSpec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb05b59494172fefa288638491a766f92427844c79776a339ab5d36f7ec15d16(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    generate_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8664126bd102d4ed5164a706eb4d6267e943d6c3c7601bd351db399ddd9b21bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d266c152449de007cdba89247720a8e5774bbe2806a55e419a51909c562c1f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a67fe3f5d046a606c76b09dcd4ef9f7e6cee9b8f626a25c0244bcc753a72a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e385dd60d79895434d755a72083db2b52acaad4ccf421b124fcad3a0c10bb72(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71fcf61effa8155c798d6e9ffc823dd4db637c43e7bfdab682f3db703d94514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c0a076f34fcc4def3d8d85f58718652ababe1485accbb84597f9523b5939a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082460acb0ed973b97e305f362cb1ef237810b0a300316b735f4977b9ee22b98(
    value: typing.Optional[HorizontalPodAutoscalerMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bde2b2a07d13a5e4d92fb302c1de1571b1df5f60bde7ed05303b358b1461ab(
    *,
    max_replicas: jsii.Number,
    scale_target_ref: typing.Union[HorizontalPodAutoscalerSpecScaleTargetRef, typing.Dict[builtins.str, typing.Any]],
    behavior: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecBehavior, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    min_replicas: typing.Optional[jsii.Number] = None,
    target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b705fd022c11550441c44d382c38b7762785aec5558d167da6edd48292bb57a7(
    *,
    scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a7d48c3603b61ba517eb241db34718fbbc6195dd2d01e957c3ee4b9fb4009b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a39270634d1c4875e18c4de9b5d84cc489107b048ea8f715a370c0d6f725848(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ded5df46797812a244c0fc5a712851be60dcab61f44ea6b959bcc415716e06(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be9f4e1bb3d049b06e8c2ffc7a79e33cab54c3bc45fbeac1e6bc482c3069200(
    value: typing.Optional[HorizontalPodAutoscalerSpecBehavior],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e444e3f8a4902017601e4d30298e81a138c43865f56f1f40bf811c43354ed7fb(
    *,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy, typing.Dict[builtins.str, typing.Any]]]],
    select_policy: typing.Optional[builtins.str] = None,
    stabilization_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b046d49c063b4bedc41f444dede05b35b24c7d27e6c228b76aa87c8946d2cdc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a024a0ae1bc62fdb972053e1752ea376024c75b830b0154c8734db97639a57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31edc5cf760faf3ce2be35ededf01be17da6f2cfc3c79ab9d1df81c98ddb9a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ff8796bda9d5489961a1952bcd818033384c959098af77fe17891fd8431fae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f38e05b8b2771501e35bd435649e6332c258463acbc4ee409e214c72733cf2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff3eb4b81c20a26686733ead1850cd4a260d99dd6d049bb4c70029943fe066f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDown]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3555a60aeb23d4d170e1d04c0e9718809789780a0014a82b2f7e1a5325ca0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d16265201f2e9c9556c143701441ef92c2d95604bcf8d0317e9fc843fc648f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8222ce0bd57665056b01f819c1c4f21d581a26f29c21555e00a76bcd54337c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67413f56a81dfbb60da7f8d314440f3a8055c6de7452f704b16b94a219a3efeb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fc2efdb9a400b030685264d753cd7e8b1aa0c816885866b86919737aad1353(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDown]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff03bdd24b570a82c0921bb9760e754bf8c68d3906fd8611b5b50e6d9c90706(
    *,
    period_seconds: jsii.Number,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a2f5ba9e19727b3ec610ab7c35670f5a7807b0867f79d7c8641a6ce9965857(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd2ce3df568eb5d13ab8c16be060acb6f45277700c03afd46d87a4cd09a8e56(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0014cfc18989e9b5b263f0ba7e793643982ca255b5bd9246d86e746d1312a4b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f82f984eaf071992fd147f08093e40748eaea71be4d18046961aaf8269b1d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c87d66a57a6f832a89091bd2469c3748487d74701127b327cefd78103c6afd8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b853fb09d4fb7b1b495bd7650ba4c8973fd4e84cf39a86c08671470e3929dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b370120324fa673beca3e83f0469740bde06a04f7b6efbc5980ac066b5c08f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5929d2970ae2d1789ba3f2c64f0c8f49fea0013efcab03a1719c8cd42612dfbd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36235b0967bd873d7dc43d63fea5f17fc58e73a18ceba6acdce9dfa55f4b0364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6412a1b4523bc8d5fc2d02f81ba5b60db4e70e3a81ccac92b013bf2559555de3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de11af1b236491f4ce28349d84f7516f9da6f056ce79334db4733cf8adbaa778(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleDownPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283eeca41622ed7cb30bd54d274a383882bed39abf147f3f1b75ef743f98bd45(
    *,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy, typing.Dict[builtins.str, typing.Any]]]],
    select_policy: typing.Optional[builtins.str] = None,
    stabilization_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0cee265d653504aa1e7c98347b76e00bc3a540c08e0f1058b32ae5c33111ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbe85d58fa7d3cb384bed66eedb4d07cb22bea96da303ec5fff9b7d5825a838(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ecbf6562fd526ed675b51412e4c39800fd66c67e888d2d819612a765a6c4b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9128f268976a75af683bb6b77842b5015baf9753ec6cda16a664648a0932928f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d3ce3672353e2cac3ce3484e97e04072181309eabbd0386380ca473b74d432(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7242d24e005e7076953de6966ee56069a887a6b100a2f7ceb64db00e3b00d395(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e07ea75e58231a09bcec705a0b763c28e87c8a53b5895a0e46de56d307658b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07c37fc24f3a3083553eba142eba886af24543d0192b6521643ea52ca5ea6c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16971a746d8a47a5242087ab932b1e354d85d3b12a5f6a7927617f9cc7dc1ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0381cb1085db24a56d2688a2b7789d21de6411e3d0efcf7b4a2e49d050f0d38d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b117f26cb3c7d55bca40c9ef1ea3f6be2dc0be27838b6c10edeba876bd7f2976(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6199baf49f01ffe26a71f36ecd6eab4482383a561c9de555e01a6192d1b96e3a(
    *,
    period_seconds: jsii.Number,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a68288f3504a8e39e641e65a67ded6e2fe5ec01323a8003b97c44a1ba4877b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0851477bad5ce785d20e48d5245f6cddd976a9c23772bd5fa28c78146e58ce8b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3860e41242fb6d618d3df5f678da7175c242cb86ead7db19b31ee5ba0f8cf3f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dfb80e2539a8cc64fff21a01c0a3b08fda2a81a39a6cf16a40f6667bef240a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06c13c2d1394d58545417187dea82ea35a9e635d1e8acddb42a67072be1223c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a0014291a4d67f6aa45fdc3dec020d985f5a8e8f40ede5daa0ef1d57fe6807(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebc596acfa5303d1c2bcca9fe742adeff377c39f1407f1ef43014b948818bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efc4a4ebe5fef7914190e4e9b92aaf5cdb2ced71e7ddab2ac2dc76e914f40ba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb92815fd0df002ce3c437455a32622649a07ee3a1eff4c2b4af98c88d9b230(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72436c8cda53bcdd05471fceedac11c834d096d66224ee0104615fb5b4154481(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e2d03046adad3006c011faddb7ef4a020b0b969d92b1620a35146c562412a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecBehaviorScaleUpPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ea7c526d002af5d1720f234dac3bf9a563a3b6c823f85c51912c8fd6424b6c(
    *,
    type: builtins.str,
    container_resource: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricContainerResource, typing.Dict[builtins.str, typing.Any]]] = None,
    external: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricExternal, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricObject, typing.Dict[builtins.str, typing.Any]]] = None,
    pods: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricPods, typing.Dict[builtins.str, typing.Any]]] = None,
    resource: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricResource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400dcf91f0f393a8e8441cf8b23d47dc595f67f658e0a57d013c0bb9026f4f45(
    *,
    container: builtins.str,
    name: builtins.str,
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricContainerResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c33639843e8c48551422fc990856cdf7bb4b321a48a47eb7875683c7ff96993(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fc5c5baf705fd4659743e041b19846dd9a2c2ae4a7833fd7eb36368864f4bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bba7337708bbc327b7368cbb1ca49e3690336ab493e519af4d9ea1ce832f94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4483cf90a5aada764ebc2f0fd74947ec18bd52214769740ff8292ccc9c9df5(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff61eb4be2f006f4ae5a95d1ff8da76f006cd3ac57eec973bef75b14ad0cb97e(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcdb550ad8cd67e68665190d8493c30bbf08551a9584a1f710c72179291a0df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fddc4094f1001a512961ad86133d56d20a8d63ec027851483c521ab61e0d5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f821a150896c39201cb4c61dbdc318609a0f99b84cbe2e8c03d26728daebc9e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9025b76345448e3319b2d41ed99a0006ba1d5c11dd17dc30857d60b66ae9f3fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15670a4f36120a7c0faaf62663bb64d787f0e43b3eccf5a15949ce1ef44e8058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a580dcc9a5137f866523a72297e6303546019c8d29f6712cbf2893e5d8d96e(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricContainerResourceTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1455207f926c576a3a149cd04d67740384f37c4bb602dc980ad215888ce1669d(
    *,
    metric: typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricExternalTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61e7cd6b5d81827846a8f256c7ffcf73192cc1dff4624e10a06054fb84ed953(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640fea169ffea647778831d98e27ccabc59f1e6fe9a64d62cd056301b189d134(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aff0f5c5f82f8c462510226342946efa6b85c532ec478975e0d0a735e3c610(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10f5dff15a226d6f2e8d11636c22366a29c12f31c999da502488ae526c51f42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179767f4070bd10122e5d9c3e85cd6a05718a1482413f8caca6a4091c2a4ef95(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricExternalMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8aac30bc0f94ffc035f2b259df121117a5034cdee46ba0dddf5045355f9e6f(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d31d2903d642ef33e70b1af0e21f69b19c2b47687d93e18def813c1dab1577b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0c973f659db8b15bf0e9585fc09e0504e8094d275f73d85dd787b960b2fd2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce0d18f4df97086c2862c45b46f184095e6360361ece4d6a972d6ef1075c7b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb14693386e1351de4960c9de2ae0a0ef8814a8b2e41acc3d882a9d729018206(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da22eba6997d2ce5c85c26c0516a1366ba9cda8196870fb27ee72fa8920a89d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54408b82fc1871abc3d557e199cc573abe20981e87331b675985c64539db2bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eee6d55b98ea1253baf6ad25168d4cb1b892972ec927937babc614652bb52bf(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5315cacb69d542161d81ddbfe80e97bbcbbf273d00f86da3bb4e2a10ded78e70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafd6f8edc146fcba183680aba24fb6ecc067781ca38b9a98dcdf1287128e6d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00f19b88fc30be5d1fa66f41a26573037213edd2bbc0dba5895a8cf66563870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1498aefb47ffde29615f11623b1e945344270741e11987be51468ee7d5747215(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98739ec27f3b41534538669f3abde54cfd6df4af4a70e4fbe38590a473458a0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f171b7673524e917952fca35d9ae5cfa8372261e31d75a01dad030290561c817(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0836c61261d1cf351e1a0850859bb648454b8c15b2d4d2072af10ff4ead9d9a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16ecc736256a60856e5ad6947c8b36f190963b1db085dd335dfdbc889bf8bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241ee111f390d1efaec2084de5a93971a50ecff9163452ca9f56cc39727e68cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47f0c49613fda9fb49f90cc5c60e48d497f09e661501ed49b204f4dcb0f22d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0761c585bb938abdb87b66fa03a297c47ebff1096d97952d02fb7c47f2dd4e2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c0a63555433179190a75cc27697e3745c349761b01c168a05fad755cd48308(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408152b775458e10d356618b5e81958e5037761a7963bc16b727af3e6e27b50c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbc2a6c7b994e7acb340b2092c9358dd627aba6218dcbcc9b6517f177f77e33(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35d9e519058dbf402703c2288f77aa7c4607761ab749cabdb2e80c88521e600(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricExternalMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8968140552c301cb87bac0fcdaa877228f8dc6dd5aa8046197b40825bad5b779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95862d239439e91e87a50aa3f243ed0f1d0275819c0767730159484080bbbbfd(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricExternal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bde13e4c04cc3927468d1c30d407f4e362a4a694225291e66905f626186be0(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1166772c671f3ee6b217a947e404e98275d6e39f2798e1c139161dc3216f9208(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d093612bcaf33bf91cdf3a42c05991e8d6482a1ce95d3597554abe615e436e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c989a7fabd50fe0a67a2b0e166e4708f982d400e62cc24bc47536ab15089bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64af7c6620d30cfd718a80064488f9f2a009a0750d06a0fcbfb45f2fd16c0c96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5baffc4898e3de7d9dd51aa44f9e359e80a1b1d1517f13f5166ac8b7175bad6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8cb216240a64ac33cc493697b8d10ec1346f02c75203923a8e2088cf8b0d23(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricExternalTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92918650cb0c03d54f997e1d05eea5666e2fe7491254cc02af88ff767cee112(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e40a8cbc79052b82f194021c7e46970606ef5c08878056ba84f15cb7228966(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8541816f56304dbd0205cc06a0b4c581ea591d33355e4cedc7b6d0c475d7e577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92038f94e8ece79cce2654be7969dcb6abe88c18086f702965cbcfb24212c577(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b082e13ca5b09eb48725b34b60f42c2ecffa242823d19a295026a0103f2b22a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bcd0a5ff3e5d45040d21a0daa2dfb83cbdc45db9253221c6755d1187ed4b2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc162bbf92942238f0ceaff6e825128bef680ec884cff10584475de0d22f139(
    *,
    described_object: typing.Union[HorizontalPodAutoscalerSpecMetricObjectDescribedObject, typing.Dict[builtins.str, typing.Any]],
    metric: typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricObjectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934171abd418c21f6ed422668bdf2425eaf8ff5ad7a5bd210dae1cab7d3a6ae3(
    *,
    api_version: builtins.str,
    kind: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa584c54961cf28759bbf3203eceacf8ccc66204f47e3d0645732024e9f79a79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2242c6433e722f8f2b427bb01dbef432cecd13d14a17398e489e805a6e54d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6e1b14ab5636547fa91d2f24e6647850e85bbd3bb85cf342df05ed40520520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379981bbfcc1568c8b9b6d84aa3143b9bdec90ea8e9067c0cd206226c1394fb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96021d0c69b928de78dd3b7d93e8627daf9db3b697bb7944e5c65a00ef6162da(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricObjectDescribedObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2757e6f7d5494c18ae403859c8c55c58e1c4549d1c5b0ca783e02ecc335c43(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa7a50eef8dbbd303755bf17751c62b771114bfc5e781d000b3916fc1f0fe9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49514718b1311799ae2f045e53e8d5f03b539564fc8228ad67257a4960675c7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc069ba028ef3d59ebda973cc018599cc96626bb4019265ff455a9c99f7a999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444043f9e3fe26cf65af82ea40dd14c273d6fdb0394a9e9f3057acda335cb521(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricObjectMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eedfbbc21776905cf3c5a47d7e7c865d872cf78312c0ae0e7909ee07deb715a(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5543fbb2fb92ec7992332b40a2c6d78ac1d7a90686cf87dac6590237ad7be4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6532dfc131db7fa7cf9a1a0edf3f7e196944ab3651ff1ccaef5e04d8b6da773(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01e87e99b1d2f5ab8840f10d933ecbdfe3cdb1e8d58a9dec01f5945d29f311b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51d87febcdede346c93a3e49265cbc0b06be522cdb84d1a99555e48d230f100(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694829f178a3c737d7efaa55bc227037add28903d5a037871a729b2f20cac8b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f39438d3429f6c4e3ca197a38eba4ea97aa001295e9c8d919311163d4ce421d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cc0175608419aaa6c3921066f14c6918e91afb587bf7104925303388186057(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c6d61c2e51d945f34d983eb2d01dbe4302d25994137579e16858ee8cd4268b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb41e68f649bad3de334b0fd6006d4a40361427fa8f5e7fc56eec7ae6ef55861(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84a3177e429657cdfa2deaee9891ae8b5deaba5c54e237d9ee6d4cabb1ede85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dbf6a896d716c8f3ae5ef524caa24496b31e71c0bfd182da7301e7a14924ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeebdf8009d393f9f11e9b42fff56f8f16ef23698898a0afb75ea4660f74ecb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b04e86dc1f46e05da98392cc4c940f88c62c263eed3d332256f8557427be37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016744d8b0ccdb135c61c05d25fab529dac15b73791113d693933e7baba992a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ae1c34aaed9aa566ab398357f3c71ab4798d7577829ee3fe6a6ff10ec1251e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3536bfe601fcfbd16ec96e841da009a78e4dcd645e600a1d7bd6f5d863c36c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacaba02f14fb878361faa7a576e55dfb080e556bf966d47c21ad36cc9ed085e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8197f72fdc38b15d23b21c278c6829cde2ee56e9534ea37281ba690bc46e43ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505d270df4390281069baacb7d91d8ffe7a1ba8df72029d1d271c35a6127dcad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd810b9768340e6f833ed681849731386f1ee3579521498e3f83f7c21d46291(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc87d57cfc423d915d784cbcf1e62d295c8c44aaf7b0a20026de28fc835ba185(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7442f62eb00f1c157a90617b0d02912c17bf92b79e81b9af75205c2853761623(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricObjectMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d05f6161120da6586d14ded76e6c0d59968264b23c808af0aaf81819bed31e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46ec48a453c63774522c92cd94e38ba1d6cf5244cbc5307fb8f5a98fc8cd625(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978fce1aa0e6f26a723ba5cd3722805c0f952623bfb7c3c8df0502a3f771a8ca(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63164e681d1f2520b68df21a92bd8c46e610e9d61d7a562510cb6ded1ba9c736(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf29c4d9bb9670bf58ea61f62fb9a6cf966274ab9143dc38408e65cfc617d1c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e8f160a24dfa049dece8a335c02f9ad50db07f300954db30ca6c6f3fdf8ba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9e2ab24f2d5528da3c0387adedda84fbc0ccf2e9540c9f109ee5f0472f6120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c962375c56a95b65c41d24a500e052598c81260a19924daf7bf20b8602329f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605abe70bf262c453ec1e964e3b17f1a594955a932e99e09294b154c194db599(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricObjectTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10d2bae0b8be83844f240a46fc066e53531ee9fc5b74d1bd63c08429152621c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e76f5f959e538735676ec91fc9e0db58c1ecb0f58ab3f8499dc539d2281b4d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83095bfc3b2b7b7965149a9c6d179a25c13ed9b17dfe94e50bc6e8fde643390(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f43532e83a7287c974125dcb1a6e52b31cad43cf198bd3ca8fd3f91a3b20a67(
    *,
    metric: typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricPodsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce11faab1c0a982586e382c066c81472ef30cd6f3cb7b03fb501676ced0e0c20(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d458c71d0111fdc775cb55d229caf19cf923e4a21ff1fd3068ae45b9d624ac2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b96756aa28cfe6346b1b499bc5ec93d0a5130a13893e6f9023ae3ba621e364(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973ac1f5c511f1a87e29f6cc227e4103c85ffcff7ff12422b68cd7eaf7b5122c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc167c025a3e8ee79bb8da9f7890355d4cdaa6d7a6dc23b67f01800c9659e20(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricPodsMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ad2cff6fc367fd9211f5301ba28e16de5cddb099e7860c0459b0fd4ca65ac5(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107b0554e60671156d7771af8a1df69bdf799ab8f5b1bf0a777640dbde5b764d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85ac496810921b0d5b56d2c017a9a84092f0b63d1f20b93790cb8cf83d176e4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d27635d572cc03e584cf5eca49c399b97f2e25267a0c52e592e93be1540ad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a481ec21f4d2ddc94e7b7393014476a958d32a36c9dde21e3e1de404010bde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66b11c361629f1194d9f0464abe27365fda6eca9645171088901a21a1451e88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d939cf57c142cf96f94699820fe783dc41ef5b2930b02e60d71d7feacf627f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29cd4a477439fa05c3c9f496d17feb18d56021cd25b5bcd9788abf449937a6d(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e625487492df595c683add16da23b6a96eec93a542f24b64b3f1e441558bf969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cff6563f041aef683fef43a5d2817638821d58d2ea3fe62f11a8a1d72932c14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c80c2420a1fd899acc51d89a9bd3096f03375cf4d2fca9ddfc73e2927f31bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de418159736f805fa6e65a0b9b45b2918a4f42995b898a9db4058f8d9e124881(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef423ed8caaa926ac5636370fc0e4b241166a8692664ca210da40173f56e402(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46bb41e1fa483515027a2010e83d962cb003f6ff628912d16b77ecc26df0f96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf8b6c5533310fadd0c268e617ae142c0eae733014e2afd1e2f8a707d931031(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebbd2fc71d808ed7250b071e0299665aa1c4d2c33264228c2baa9ab7db2490b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1022960c9d9b6db0c5eef3008ea733e83bdb1bbef76929528f7f36601ab746ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab8b630d4ff59bf2dda239ef5782fe42bd69d319b91a40c18057d67d4c1af03(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed39e54d4aaec95c79cd2e29d1b447d57cfec1afaf709f49a20a38b3c1ab3de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc7ae826977c187d8ca4fe53321c93d2b2865c1795a79960222e7257bacf928(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6eb0aae0264510e71b189928231c713a05ddd41f1cf39077a61156cc907d449(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beef4caccd4cd6821a6d9e10553953628f9ba969fdde56473fb779448fc6eb91(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31124ae5929b0d268b4990ec6110eb58d22a7262684af76c0805d27d94089ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerSpecMetricPodsMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f512f616754585a1043d737e3b77130e98dd75d78d62d8e31625c584e7f13a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839fd8360be4b6c9587dcdbdc44ea397ab8b99b8fdac13755a0ad17a3ba6ea69(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricPods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1551ead0f16b18b53162a0e86cacd7ebf359b5cdbca41c511c1ecf43a095a73f(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e65d63e7e9e4cc53ac397a6be36ca967a9122a26cde200bb50fc97eadc757c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f205110b5489f270e0296d33cbb8d51eff53a382f76797435e28bbde7d7aa6ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9644862928599a7e6eab369b99f692fab5db0c1c8e5068a8c2ee826953e71ba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3503b0747e171e7aa506ba966a06e0913375d2ef90203ec817d52ea6c514c087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3ca3895e733a673dcbba761cc5814a5c62ef580aa5e3a96d9d7494ef77da2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b1ed410370b5968999521a90f745dec4d5b7474ac80748f2d90e7c2485f18(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricPodsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aed86b2aff3d5d1dd97e6389156d76e1a38fef3faa49bbfffb3639d0b0f911(
    *,
    name: builtins.str,
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerSpecMetricResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68371d847355e7798e794b04030d480088b5452ad6c3d95019a853c8e3e2b3eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28bdc74c443ac99186328f91a153d606e204166621e98f9bef8e680bd740cc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db211e20778339a67d394c7c6468a89e23a4e717a2ce28fbbf858b83136adc4f(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe5e8ced2c30bd5f5b95005066658eff1eff0239478f65ec4bea5ab6508b5e5(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97882dab74377b398a7c6188e751ae7281447706a8c6e147e546c4c4de98f2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb1f0030cb3f41ee9663d833fbd8675d93f6831ea7333fdf9757dbaf5be0386(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7679bc0348dce1a88107931e667bd54fa52a457bfeeb16eca914ec2493185ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8befa572748fedbcdf3660002e3cace47ae45b36e4571d07bf10522f7eacb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab84ab8a58692b8ec41bbf54ec987af36d311c91387f927a9f7b8a569539051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d7b7fe17593c120262f49c99b8d077c1c1d21f365fd64adfcfeb9e936f1f37(
    value: typing.Optional[HorizontalPodAutoscalerSpecMetricResourceTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e261021721d934f8bafd40e79ff0f89635fdf7cbd37c0dd8f6058438e31ee4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42b8dd8018639d46a0da647c0034cf7c3f50fc3ab7416dddd39736bdaa75995(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerSpecMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3121ff98a5d3ed8f23cd3c0d7f2afe37e3b3e2568a7fee1dc9c996b86cc411c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72fdeae21cfd226069f720754b99f5edb6b78c02af64ad065d2e7f2fd425e45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64efa9001192a1767726cc5e2e36fc2d9a56aaed26c9376c3f26930b4a9fea2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de556c2b0d148087ec1caa3f0b61d70c6d5a647c2ac04b2acb574c7a23bbf783(
    value: typing.Optional[HorizontalPodAutoscalerSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e105f18d4edcac2c9c86ff0d735aba9faa40eb8096000dd3884805223e5ad6(
    *,
    kind: builtins.str,
    name: builtins.str,
    api_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c310d86364862d43ac79872289d033f91fcfe7abbaf1cdb559cca02e52234a4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c0c95a2016fba367072815bbec0b497ceb89d5ae53e3c9b6e4d9cabbdb2c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b531629610ed214bf8e9d772c8f302aac9485c96a3ef7afe9e74e48a697295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9490e8e5f52920a51ad9dc34b24e9d690ad19e68fcbcd902f1be204c5bb008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167465f10c51a9eee57aa206950fd36ee3e37a4d13b5998b71e99d542af6f8fd(
    value: typing.Optional[HorizontalPodAutoscalerSpecScaleTargetRef],
) -> None:
    """Type checking stubs"""
    pass
