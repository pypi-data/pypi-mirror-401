r'''
# `kubernetes_horizontal_pod_autoscaler_v2beta2`

Refer to the Terraform Registry for docs: [`kubernetes_horizontal_pod_autoscaler_v2beta2`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2).
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


class HorizontalPodAutoscalerV2Beta2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2 kubernetes_horizontal_pod_autoscaler_v2beta2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["HorizontalPodAutoscalerV2Beta2Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["HorizontalPodAutoscalerV2Beta2Spec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2 kubernetes_horizontal_pod_autoscaler_v2beta2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metadata HorizontalPodAutoscalerV2Beta2#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#spec HorizontalPodAutoscalerV2Beta2#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#id HorizontalPodAutoscalerV2Beta2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7efb896ce085b01bbc12085c8a0b1faa6583fc1b68c94ea1e643c2fd538c1b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HorizontalPodAutoscalerV2Beta2Config(
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
        '''Generates CDKTF code for importing a HorizontalPodAutoscalerV2Beta2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HorizontalPodAutoscalerV2Beta2 to import.
        :param import_from_id: The id of the existing HorizontalPodAutoscalerV2Beta2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HorizontalPodAutoscalerV2Beta2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1760332d80aca29397a6af3e3fe8bdd897f944b04699755da43b6237e22b0b)
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
        :param annotations: An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#annotations HorizontalPodAutoscalerV2Beta2#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#generate_name HorizontalPodAutoscalerV2Beta2#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#labels HorizontalPodAutoscalerV2Beta2#labels}
        :param name: Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param namespace: Namespace defines the space within which name of the horizontal pod autoscaler must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#namespace HorizontalPodAutoscalerV2Beta2#namespace}
        '''
        value = HorizontalPodAutoscalerV2Beta2Metadata(
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
        scale_target_ref: typing.Union["HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef", typing.Dict[builtins.str, typing.Any]],
        behavior: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replicas: Upper limit for the number of pods that can be set by the autoscaler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#max_replicas HorizontalPodAutoscalerV2Beta2#max_replicas}
        :param scale_target_ref: scale_target_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_target_ref HorizontalPodAutoscalerV2Beta2#scale_target_ref}
        :param behavior: behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#behavior HorizontalPodAutoscalerV2Beta2#behavior}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param min_replicas: Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#min_replicas HorizontalPodAutoscalerV2Beta2#min_replicas}
        :param target_cpu_utilization_percentage: Target average CPU utilization (represented as a percentage of requested CPU) over all the pods. If not specified the default autoscaling policy will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target_cpu_utilization_percentage HorizontalPodAutoscalerV2Beta2#target_cpu_utilization_percentage}
        '''
        value = HorizontalPodAutoscalerV2Beta2Spec(
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
    def metadata(self) -> "HorizontalPodAutoscalerV2Beta2MetadataOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "HorizontalPodAutoscalerV2Beta2SpecOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2Metadata"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["HorizontalPodAutoscalerV2Beta2Spec"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2Spec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7c58fa181441acdcf4b6e16936fa862e4277fd27b7615b8414b88801fa999f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2Config",
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
class HorizontalPodAutoscalerV2Beta2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["HorizontalPodAutoscalerV2Beta2Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["HorizontalPodAutoscalerV2Beta2Spec", typing.Dict[builtins.str, typing.Any]],
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
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metadata HorizontalPodAutoscalerV2Beta2#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#spec HorizontalPodAutoscalerV2Beta2#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#id HorizontalPodAutoscalerV2Beta2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = HorizontalPodAutoscalerV2Beta2Metadata(**metadata)
        if isinstance(spec, dict):
            spec = HorizontalPodAutoscalerV2Beta2Spec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020a4c310b48daebe732779860f9d1e953abe33635a6d44a7e0fed12c56d93d2)
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
    def metadata(self) -> "HorizontalPodAutoscalerV2Beta2Metadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metadata HorizontalPodAutoscalerV2Beta2#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2Metadata", result)

    @builtins.property
    def spec(self) -> "HorizontalPodAutoscalerV2Beta2Spec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#spec HorizontalPodAutoscalerV2Beta2#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2Spec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#id HorizontalPodAutoscalerV2Beta2#id}.

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
        return "HorizontalPodAutoscalerV2Beta2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2Metadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class HorizontalPodAutoscalerV2Beta2Metadata:
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
        :param annotations: An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#annotations HorizontalPodAutoscalerV2Beta2#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#generate_name HorizontalPodAutoscalerV2Beta2#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#labels HorizontalPodAutoscalerV2Beta2#labels}
        :param name: Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param namespace: Namespace defines the space within which name of the horizontal pod autoscaler must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#namespace HorizontalPodAutoscalerV2Beta2#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d8d4badc03438aade768ff3e18209cb9f305dc364ab83a9b3260d93a4b1318)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#annotations HorizontalPodAutoscalerV2Beta2#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        '''Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided.

        This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#generate_name HorizontalPodAutoscalerV2Beta2#generate_name}
        '''
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#labels HorizontalPodAutoscalerV2Beta2#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within which name of the horizontal pod autoscaler must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#namespace HorizontalPodAutoscalerV2Beta2#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41e8fa5e81febf2a050769c3559aceb4d3f35cdcf67e6df029702327429089ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc2dcc6af7b79edd5c98ca81d1dd2f9457c188ccc6f62ecd2d94b7da4b8bb1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generateName")
    def generate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateName"))

    @generate_name.setter
    def generate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb59e97833eacd8b3ff1daa089c577072b125b959c631ec8f29c7b8431b23950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd6922ab06c96c7d7a60442d9a6b35380c8e8fac37ca3d2970903fb37508428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f6d87914a7a4c03ea114e7707740b1aec57b7b7b82e46666fc358f980c0bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26957d4424a40e5a24bb2b9f6d477e5e8f399fb211d50e2cc574389185a506a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerV2Beta2Metadata]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2Metadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d3eb55fc9735e29a04d883e01b2adb8080ab6dd7f79f88d681ccef1bbbb75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2Spec",
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
class HorizontalPodAutoscalerV2Beta2Spec:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        scale_target_ref: typing.Union["HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef", typing.Dict[builtins.str, typing.Any]],
        behavior: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replicas: Upper limit for the number of pods that can be set by the autoscaler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#max_replicas HorizontalPodAutoscalerV2Beta2#max_replicas}
        :param scale_target_ref: scale_target_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_target_ref HorizontalPodAutoscalerV2Beta2#scale_target_ref}
        :param behavior: behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#behavior HorizontalPodAutoscalerV2Beta2#behavior}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param min_replicas: Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#min_replicas HorizontalPodAutoscalerV2Beta2#min_replicas}
        :param target_cpu_utilization_percentage: Target average CPU utilization (represented as a percentage of requested CPU) over all the pods. If not specified the default autoscaling policy will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target_cpu_utilization_percentage HorizontalPodAutoscalerV2Beta2#target_cpu_utilization_percentage}
        '''
        if isinstance(scale_target_ref, dict):
            scale_target_ref = HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef(**scale_target_ref)
        if isinstance(behavior, dict):
            behavior = HorizontalPodAutoscalerV2Beta2SpecBehavior(**behavior)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6993d2b2c23c5111443dce34a89451890f0f94fe32cc929c7b1feb502f49587b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#max_replicas HorizontalPodAutoscalerV2Beta2#max_replicas}
        '''
        result = self._values.get("max_replicas")
        assert result is not None, "Required property 'max_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_target_ref(self) -> "HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef":
        '''scale_target_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_target_ref HorizontalPodAutoscalerV2Beta2#scale_target_ref}
        '''
        result = self._values.get("scale_target_ref")
        assert result is not None, "Required property 'scale_target_ref' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef", result)

    @builtins.property
    def behavior(self) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecBehavior"]:
        '''behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#behavior HorizontalPodAutoscalerV2Beta2#behavior}
        '''
        result = self._values.get("behavior")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecBehavior"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetric"]]], result)

    @builtins.property
    def min_replicas(self) -> typing.Optional[jsii.Number]:
        '''Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#min_replicas HorizontalPodAutoscalerV2Beta2#min_replicas}
        '''
        result = self._values.get("min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
        '''Target average CPU utilization (represented as a percentage of requested CPU) over all the pods.

        If not specified the default autoscaling policy will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target_cpu_utilization_percentage HorizontalPodAutoscalerV2Beta2#target_cpu_utilization_percentage}
        '''
        result = self._values.get("target_cpu_utilization_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2Spec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehavior",
    jsii_struct_bases=[],
    name_mapping={"scale_down": "scaleDown", "scale_up": "scaleUp"},
)
class HorizontalPodAutoscalerV2Beta2SpecBehavior:
    def __init__(
        self,
        *,
        scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scale_down: scale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_down HorizontalPodAutoscalerV2Beta2#scale_down}
        :param scale_up: scale_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_up HorizontalPodAutoscalerV2Beta2#scale_up}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ed5ddb6578ca32f355e7194721a673e096cd2db911aa6986c465cea34b02c3)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown"]]]:
        '''scale_down block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_down HorizontalPodAutoscalerV2Beta2#scale_down}
        '''
        result = self._values.get("scale_down")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown"]]], result)

    @builtins.property
    def scale_up(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp"]]]:
        '''scale_up block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_up HorizontalPodAutoscalerV2Beta2#scale_up}
        '''
        result = self._values.get("scale_up")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95dd083da1127bd3aef7985b0df56529c7739c4bce855b00797c786bdf3a4c38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScaleDown")
    def put_scale_down(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f0aebc832f5d0ecac335013d2b8f55155cfec10c1ccaca87d7b3d90646bd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScaleDown", [value]))

    @jsii.member(jsii_name="putScaleUp")
    def put_scale_up(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fdd099721eb4b92599face2934609a644200a1fcef6e91d2ff45239bef7a61)
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
    def scale_down(self) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownList", jsii.get(self, "scaleDown"))

    @builtins.property
    @jsii.member(jsii_name="scaleUp")
    def scale_up(self) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpList", jsii.get(self, "scaleUp"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownInput")
    def scale_down_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown"]]], jsii.get(self, "scaleDownInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUpInput")
    def scale_up_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp"]]], jsii.get(self, "scaleUpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecBehavior]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecBehavior], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecBehavior],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c7ec2484915bd9e11460270ba5ddd4a5b4915bbc56d911bf02600472a8c487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "select_policy": "selectPolicy",
        "stabilization_window_seconds": "stabilizationWindowSeconds",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown:
    def __init__(
        self,
        *,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy", typing.Dict[builtins.str, typing.Any]]]],
        select_policy: typing.Optional[builtins.str] = None,
        stabilization_window_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#policy HorizontalPodAutoscalerV2Beta2#policy}
        :param select_policy: Used to specify which policy should be used. If not set, the default value Max is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#select_policy HorizontalPodAutoscalerV2Beta2#select_policy}
        :param stabilization_window_seconds: Number of seconds for which past recommendations should be considered while scaling up or scaling down. This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#stabilization_window_seconds HorizontalPodAutoscalerV2Beta2#stabilization_window_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0c548ef1a0e5b98b9cdb0b84d6d796adcc6185d19452b61d6a3935589567d9)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#policy HorizontalPodAutoscalerV2Beta2#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy"]], result)

    @builtins.property
    def select_policy(self) -> typing.Optional[builtins.str]:
        '''Used to specify which policy should be used. If not set, the default value Max is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#select_policy HorizontalPodAutoscalerV2Beta2#select_policy}
        '''
        result = self._values.get("select_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stabilization_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds for which past recommendations should be considered while scaling up or scaling down.

        This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#stabilization_window_seconds HorizontalPodAutoscalerV2Beta2#stabilization_window_seconds}
        '''
        result = self._values.get("stabilization_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efe13766164151fe2a7e54142e5b6db293196316ea7f0aad894ba0a8a6db97ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b952aa4192599e0906d88231346bc2652fb7cb96f531c81012b319a35ba154f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58627c09f5a52545023e00bf1de05e3e30d165d094c179ebd2c0678b15168a18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0491721a17b639067a996b83d54f630e11419105136cbf0c097149bec37d6375)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2227100e9fed31aed82e7b9d8332c2aeb09f84cb8df88b9ffd25ee09ec3d9f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731c70d073a4aa93d36afd3e32b711c214e613c6aecf72ff971df59415f0004f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__558fcc7eb93badf4670899ec44b4d35dc2d4473dc6e7ef21585c0cf47e29ecd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b53687d16111f56ced26495e45727a742a6031b4c73a956f5edbc7b2aaef9c)
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
    def policy(self) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy"]]], jsii.get(self, "policyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b70575688112ff3fb92f9b95edaedf2d022f8e5035c0dee6449e70bbb48a6890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSeconds")
    def stabilization_window_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stabilizationWindowSeconds"))

    @stabilization_window_seconds.setter
    def stabilization_window_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e000b95e7d57050562b72949063d83c8b723f6f9b7a89f88f5011d8fd897a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stabilizationWindowSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd50b5f2448c96eff9f29ab5d9af1485aa77a669335da9d2461a1897c695c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy",
    jsii_struct_bases=[],
    name_mapping={"period_seconds": "periodSeconds", "type": "type", "value": "value"},
)
class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy:
    def __init__(
        self,
        *,
        period_seconds: jsii.Number,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param period_seconds: Period specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#period_seconds HorizontalPodAutoscalerV2Beta2#period_seconds}
        :param type: Type is used to specify the scaling policy: Percent or Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param value: Value contains the amount of change which is permitted by the policy. It must be greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1391ab97209bfc620b90407ef99f6c4d1ea4a5d8a4114c730b24095f8bdee39d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#period_seconds HorizontalPodAutoscalerV2Beta2#period_seconds}
        '''
        result = self._values.get("period_seconds")
        assert result is not None, "Required property 'period_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type is used to specify the scaling policy: Percent or Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Value contains the amount of change which is permitted by the policy. It must be greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37082af92551cf4c8f0e6b5168cbaae300f9c9e6d4b745b44b4176f810f59d26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e9a1dd0412ceefb954bbb7c7249279cd1a79a6799326d98521e429bd681fe3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67813a26f67acd16866f1f9e71d526ddf8947904d44fd4503087ed842fd5653)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54273a71f1be2ac4d1bd6f99005400ee7e35386249de11a73f75152c8e52b344)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70afd23f039db962861ea802822ad4a1ff58a6adbb21b63f082bbb7540003a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536b6c5ddbb434a5d8cfbd293770c158c879df788d77d8c7fe7654c5cd901d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a852064f919694e7a6a00e125fb55d5d2de33aeed1d0d3de51b3da17b6cb1712)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d4ef02e41ae909a1c11dd2380bcace06063b3cd3dd1bbc0c3fdfea62083df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c0d1e967dbf921809f8ff2c9a7930c53d9aaffbce6d1e3cc89da32489fe422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17d629edd2d84bdf31a9d8af3bed88707c322ea3b30a966e67af38ce8125a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de39642650f316d2c2b8f904010fb411b7d03bb4fed93554b9a0fb45c5b077f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "select_policy": "selectPolicy",
        "stabilization_window_seconds": "stabilizationWindowSeconds",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp:
    def __init__(
        self,
        *,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy", typing.Dict[builtins.str, typing.Any]]]],
        select_policy: typing.Optional[builtins.str] = None,
        stabilization_window_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#policy HorizontalPodAutoscalerV2Beta2#policy}
        :param select_policy: Used to specify which policy should be used. If not set, the default value Max is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#select_policy HorizontalPodAutoscalerV2Beta2#select_policy}
        :param stabilization_window_seconds: Number of seconds for which past recommendations should be considered while scaling up or scaling down. This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#stabilization_window_seconds HorizontalPodAutoscalerV2Beta2#stabilization_window_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5c15822532a323bdef942eb8acaed64c96379e862f46904c4909ad9b323277)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#policy HorizontalPodAutoscalerV2Beta2#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy"]], result)

    @builtins.property
    def select_policy(self) -> typing.Optional[builtins.str]:
        '''Used to specify which policy should be used. If not set, the default value Max is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#select_policy HorizontalPodAutoscalerV2Beta2#select_policy}
        '''
        result = self._values.get("select_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stabilization_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds for which past recommendations should be considered while scaling up or scaling down.

        This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#stabilization_window_seconds HorizontalPodAutoscalerV2Beta2#stabilization_window_seconds}
        '''
        result = self._values.get("stabilization_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deae2d7ba6bec9bc4d152ae1d1e37f47530c6735ef5d0db99ba1c0f526508d03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7381207b5f8ac58a9e696f28628236fac962f63f926a8e82f9f5a9195279995)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a946c61ff03658bbe756c0a4bb0e0c1fa406b86614185e363ba1f6081e3f8a2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b56025aaef68cc4dd31c6e64c30d1967292c7d532cb9ef01ae7fa4ac5184002)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e65445488574f3086d0441f9da2f7af61e92073797a2ae45f7ca0bb1731265f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a12462d273c8ef60b4eef9f093c64d08b3158b2c6d4a7b391c1216c5ce86850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ea0bac7f697c938a48f2c306980b77fe1bd5cd0c107a3c115be5a1dfc8fe40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8eaed5bbf380efef1000fc51b9deb1747f8b077e97d195e8711ba777cd04b4)
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
    def policy(self) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy"]]], jsii.get(self, "policyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fa62022b21c38dedd4fc141604375dd8bf0242251c27f73489e5c17fa880aac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSeconds")
    def stabilization_window_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stabilizationWindowSeconds"))

    @stabilization_window_seconds.setter
    def stabilization_window_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b2a399de0356f2f7503364da72d2771bff0fbff9ecf09f7d898bf2b9ad1b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stabilizationWindowSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f49c705778335937c964ae9043176d2c2046d7dd0e9028474baaa735f4266e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy",
    jsii_struct_bases=[],
    name_mapping={"period_seconds": "periodSeconds", "type": "type", "value": "value"},
)
class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy:
    def __init__(
        self,
        *,
        period_seconds: jsii.Number,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param period_seconds: Period specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#period_seconds HorizontalPodAutoscalerV2Beta2#period_seconds}
        :param type: Type is used to specify the scaling policy: Percent or Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param value: Value contains the amount of change which is permitted by the policy. It must be greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f260e7fc0c6454618ba4b15387ed76c7d2606702d79385eb7ac41a4d406b073)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#period_seconds HorizontalPodAutoscalerV2Beta2#period_seconds}
        '''
        result = self._values.get("period_seconds")
        assert result is not None, "Required property 'period_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type is used to specify the scaling policy: Percent or Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Value contains the amount of change which is permitted by the policy. It must be greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f647bc78de9f18d8cb1e3bba163c66d4d23bf22553cd9dfc5ef82bd41c8b41b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49476af2584617cf6075317597cfa5ad73739bd30b1bd50aead37dd421c42fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4477b795f76bf54dde6b70596cb995b6742bb5c5461fb50456035fc1c8129cf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0626f46a878e39cc30dafe264ee178df27672dbb413656a0cce7beb4972436f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__feab2ba404e1ce73297ed8d37d72d22bddba70283ac51220b5b46955a9e7bb70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620f7cd133c0a3b54c1a81e4a0dc6f97e798fd21111e470e2041c885e26fe8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92f0e2febb382ae5576fbf40826544a27e87bb81161dd3268de1d9a11576a6de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d90cdf1327ce08722cad4c8f5d2824b1a126ff46eef265c1e395922b80b4bd94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3149a27b68e3b939afae7ae290073534da80163a6fdfe0604f7516ba8ce92b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d534a8416bc6c7da797f9e7e6433502fc4b99123aa70dd6a739242a7f61c2aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add4a0168065167487c19aee9ce039e171259abd6f8db97fb1b35b96afda54a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetric",
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
class HorizontalPodAutoscalerV2Beta2SpecMetric:
    def __init__(
        self,
        *,
        type: builtins.str,
        container_resource: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource", typing.Dict[builtins.str, typing.Any]]] = None,
        external: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricExternal", typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObject", typing.Dict[builtins.str, typing.Any]]] = None,
        pods: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPods", typing.Dict[builtins.str, typing.Any]]] = None,
        resource: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: type is the type of metric source. It should be one of "ContainerResource", "External", "Object", "Pods" or "Resource", each mapping to a matching field in the object. Note: "ContainerResource" type is available on when the feature-gate HPAContainerMetrics is enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param container_resource: container_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#container_resource HorizontalPodAutoscalerV2Beta2#container_resource}
        :param external: external block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#external HorizontalPodAutoscalerV2Beta2#external}
        :param object: object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#object HorizontalPodAutoscalerV2Beta2#object}
        :param pods: pods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#pods HorizontalPodAutoscalerV2Beta2#pods}
        :param resource: resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#resource HorizontalPodAutoscalerV2Beta2#resource}
        '''
        if isinstance(container_resource, dict):
            container_resource = HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource(**container_resource)
        if isinstance(external, dict):
            external = HorizontalPodAutoscalerV2Beta2SpecMetricExternal(**external)
        if isinstance(object, dict):
            object = HorizontalPodAutoscalerV2Beta2SpecMetricObject(**object)
        if isinstance(pods, dict):
            pods = HorizontalPodAutoscalerV2Beta2SpecMetricPods(**pods)
        if isinstance(resource, dict):
            resource = HorizontalPodAutoscalerV2Beta2SpecMetricResource(**resource)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e44976d61d0e1ddb6f2c5e6041b5d288233e42566bd37bbdc9f1ab2af185622)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resource(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource"]:
        '''container_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#container_resource HorizontalPodAutoscalerV2Beta2#container_resource}
        '''
        result = self._values.get("container_resource")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource"], result)

    @builtins.property
    def external(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricExternal"]:
        '''external block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#external HorizontalPodAutoscalerV2Beta2#external}
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricExternal"], result)

    @builtins.property
    def object(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricObject"]:
        '''object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#object HorizontalPodAutoscalerV2Beta2#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricObject"], result)

    @builtins.property
    def pods(self) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPods"]:
        '''pods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#pods HorizontalPodAutoscalerV2Beta2#pods}
        '''
        result = self._values.get("pods")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPods"], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResource"]:
        '''resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#resource HorizontalPodAutoscalerV2Beta2#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource",
    jsii_struct_bases=[],
    name_mapping={"container": "container", "name": "name", "target": "target"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource:
    def __init__(
        self,
        *,
        container: builtins.str,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: name of the container in the pods of the scaling target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#container HorizontalPodAutoscalerV2Beta2#container}
        :param name: name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aec61a7fbf088392198b9d4f97b4217fd530eb80fea42de7e35d6117fb972e2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#container HorizontalPodAutoscalerV2Beta2#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''name of the resource in question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b93dada074c15a4d2515906647f7be0e04d036a21bdc9e268cba4d7d1713600)
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        value_ = HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget(
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
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTargetOutputReference", jsii.get(self, "target"))

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
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a0dbb7184d46e3b5e3ac1784100db030f8af17c70b19118a49b07752343737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9270d332606fe59f748498d56ddd84ad98fe504dffc9415eb085319ccf87bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691450b07f5e3867691788eca603bea9274155de8297007abe189d48c9496785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44ebf76c498bfc8ff289923a585620510c2407b20e65ebbe782bebf624b36dc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1984335f7f04d091ee5de5b8e7a62da8ada573530d219ef60f4fef2700b33b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d40167ae7c4142e7059329bba776b6841c3fc396f5cac23a4cb8c029013de0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ad8794fc2ad91e2106507a0185a7f0cda127f77481b06b1a79b68051c45f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e6b0bb32cae69b118083832ba89b28841d6cea15c04fa25fb82556dd226bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54903f0e5995986b99af26c9cd0ca73f4c67ad47c57d8982aee590224017942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef29201603d65012e5cc9732246b8b8ac7e0a4e6327f1f0b89453aa34ebf0e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternal",
    jsii_struct_bases=[],
    name_mapping={"metric": "metric", "target": "target"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricExternal:
    def __init__(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204a2b700a75b468d9a4820ed5cb7a6aab2d6bcd351f0a6fc36fe751a6e6bc8b)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricExternal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791927e591b856ec7d8bdb91da95cc77708d7c549e367e905a5e7e25b0e1ef8c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c212344476e17453ff6186e7ab26b8a8b2c7109d98b50b86ed5743223e617ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bebbbdbd3efeb805efb265a6782b71dd33908971ada2616a7a9a23d3ff590d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0231354f092d81a1f05efa897236b57f9cea9a380bea4c15e62b4b753686caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a8239570068b061a1722c6b45f3d37480703f6525e97efbd8adb6dbfb5d1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_expressions HorizontalPodAutoscalerV2Beta2#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_labels HorizontalPodAutoscalerV2Beta2#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c60788e22a2c62a576be5bfc01659cc28f03d96036f72b4fb2170f13f4f869)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_expressions HorizontalPodAutoscalerV2Beta2#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_labels HorizontalPodAutoscalerV2Beta2#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f2439e1c8216bcb3051dc4d65eed66e98278deac2cf77392656898f6fddcc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e380235db2a3098fb2c9963324898f3236545a73d2e8a82515620bd915c4161)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844b953c660e2d87dd39d912e54a6c94ab751b7fbca9dec299ea41d1900546a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f98f4d842dce0aa7cbeefede345c2ea6902429c2148217fa8a6a088b615f522)
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
            type_hints = typing.get_type_hints(_typecheckingstub__780b94cfa747e3eeb12a0d693dd1736426a01ee7d1d6b1e6713d1b3ff1ff5873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf943d93add3a06169b53394c3ae6a85e38cc2ab05222d86709a3556a8ab6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#key HorizontalPodAutoscalerV2Beta2#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#operator HorizontalPodAutoscalerV2Beta2#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#values HorizontalPodAutoscalerV2Beta2#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881b7f7a1104a4f26e0e7718c84d70e0bfdc44e7ba05c452685ab44fdf36ccc2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#key HorizontalPodAutoscalerV2Beta2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#operator HorizontalPodAutoscalerV2Beta2#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#values HorizontalPodAutoscalerV2Beta2#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1f76ad11d9cf91de65b06db65db4e68dbe45e4d02776ca7e69c87bc64636b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a5e931709f2e3937f64392e5124e604a223ffa9d6945dc06e9a8fef5484f6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e327249bf639e78c1762ea900114e8642a27df08d0518e8876e5a26d10911a46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20641f4a41fc84762af371fc0384e57f8b70140b8503990272cac6fcccab1756)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ba115b6de10a3ee2055f4c34dd4a93b30b8cb254724d385300cf06b614659a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d15c6ded7d3c9a5f2c5010b12ff3aac4daa69c0a1f448f905c4d658ad6d82f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__561fe0906405e458c8e84e421a0e5b8a94ec386d9e68fb37cc09f95cd2a951cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02fa06f91da87453a9a527f2962a1cfc6fc0e1d8076b615abfd8766a52eb76e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0d5ad7839c26b6493a185ba79c3cb0344f4aed06bb6c3dbcd0ac18c266c6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12e00fe0bc7e2f9833bb7568c9992d038bcd704751cbb53ae1f9a26c55db0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88326274806631e116b94900456e6d92e7463f630989630fe4a32389d499da6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32eb9c059e13e81eaf1800fd2578f3604bc2de3fd660297fcffa34a340f43686)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df079bad353c5686c93e2a5f9be65828ef11ce7dd488063bf2463c98365ec87)
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
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a41b5fdec9e0305b8b595ca7e8aef9f80091275aa8807a63ffc84029efdb5a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bab6993b1906d5c8a29b52a9998d0a7c6c55c4fc1c31b34ea996c808558341d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ee6a66f7adc183eb8a9a393255355ee8e994a9a8bfe362744bca90dc2138f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric(
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        value_ = HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget(
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
    def metric(
        self,
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricExternalTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricExternalTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternal]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986aa47c6677b597fd0b7e267d85a66a5571e736be6835969943f6ca2e48c3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642c4984df85d586ec63da14673a21e8b06414c5fe410cadb54aaf872f5fcd8e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricExternalTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricExternalTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad27825f967be445587955e8f64ebfd0ed19886ab3147e799ec3c3add99ddd08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff8f643946f7a73a21c6143da8de4e4f860895e312b21ca5b47bfd550e5f5712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c945fbdaddffe157454a1247cdddeaa9c76f9619ea98d2ab9b4c2d254fa1235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45778e344af7954e987f98445176dc21f7350f03f85ce5acd04a8c9f611a709a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5068488711ee3cabc303264c1e42a3b097bf7d126b7f6a93f96c8dee34d9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba2035aa14e6ffb5cc95ea7fb1a1577be55cd9688d949658e23cf5355a68c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d345315880793d874ad486ee9f53be1bd16b24abddc0b5112a242847d87b2722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34b81f4e1060be65eff79bedf16d2243ec8778881f51581c37574257804d847)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c542fb3757a932c7b43e2734dcfaf0efb386121141dac6c53283dcbe92b8d26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c53ed911a0413566df0c1bd985143371a05b990af492cca7a239aa4d99dabb21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e13a619add32669090bf20b5108b9a05b806af274a7f55dd6dd8bf53613f1675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc2285d25cd70ac1dbd89c0e53503df04c6e3723ae49eb12d78dfc429e79ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObject",
    jsii_struct_bases=[],
    name_mapping={
        "described_object": "describedObject",
        "metric": "metric",
        "target": "target",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricObject:
    def __init__(
        self,
        *,
        described_object: typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject", typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param described_object: described_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#described_object HorizontalPodAutoscalerV2Beta2#described_object}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        if isinstance(described_object, dict):
            described_object = HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject(**described_object)
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e612b14605990c6dbb997d3ba460e95d5ccbd7eda657bcdbd0594a11beeeb79)
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
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject":
        '''described_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#described_object HorizontalPodAutoscalerV2Beta2#described_object}
        '''
        result = self._values.get("described_object")
        assert result is not None, "Required property 'described_object' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject", result)

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "kind": "kind", "name": "name"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#api_version HorizontalPodAutoscalerV2Beta2#api_version}
        :param kind: Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#kind HorizontalPodAutoscalerV2Beta2#kind}
        :param name: Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e047be655c8b715a802a80f0a550a86bf28d15ca67d3e1e2a3fbafe3a55753f9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#api_version HorizontalPodAutoscalerV2Beta2#api_version}
        '''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#kind HorizontalPodAutoscalerV2Beta2#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb71ced805485b1f2a362910a3afe9b0e411e7b6fca35efffa5456d7a969162)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ead282309e42485f07baf82180438d379505a88b78a58c64da39dab068cf7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cdf39c88e80b1d2a81e1b33bad345783fa6aebc1e8fed60189087628025b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a095151479a110a167d33fb1d6603f070bc2b184cad9b5aefa7f78b68ea3a22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f8ebf34f578b11c72ff0f1adf979539c19350d54add85bd981f22f82bd50af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989068403256f4d9d89a1f8747e7e946cea8619099616fec1fb11f3647e1f32e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d245fc3e5e47583e916a04b88d1a47f9125f516bd85c1c167988b488b2b01de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dc52d7dcd28a2753974d49b926fb8769ad640ab15b3e416d8560ed770635a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb9baf5ae73b5ae0d8bc108cbb959341ca1decb1aa9e1648aa0457da7d7a499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084ae44ef9416dfedf5d01c02acb919da89918f97194d7396c80d99760ac4994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_expressions HorizontalPodAutoscalerV2Beta2#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_labels HorizontalPodAutoscalerV2Beta2#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d284d6f8ecf2dabb95f13838cab0883190930964d2ab8f552683c6f4b39319d)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_expressions HorizontalPodAutoscalerV2Beta2#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_labels HorizontalPodAutoscalerV2Beta2#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7293e21309dfd4a9fc2d99952fed4d33dc48ff26f2fb0b9d4e8527b8776fbb33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56a8e068628a4514b05936dea399107e1ce51b915c283db60c2ebdaf65bf6c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5385b84b414499a6e5acaeef0d4774c2894a94c366f1ed402082defaab1d6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c89a7721ecdcfcb6263d84063dfa993ae2173e7253ee430b2c6c537ddcf2b334)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c49d578c1ec1b8ca8d3d24b39d2dd4890b05db8bc150cf2907325915e413581f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b67af3a65dfa80ab7030a3823849285a0ab613dfa7e116bb224e4d8b4c55498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#key HorizontalPodAutoscalerV2Beta2#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#operator HorizontalPodAutoscalerV2Beta2#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#values HorizontalPodAutoscalerV2Beta2#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474501426e0f16c9b3352af94716ab03d5cfa0ec94bfff4e258e11b6d409c4a8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#key HorizontalPodAutoscalerV2Beta2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#operator HorizontalPodAutoscalerV2Beta2#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#values HorizontalPodAutoscalerV2Beta2#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__faf5321a9aa3dc4d9e694d8b7934d875771f3d1d1bb49d798ef2ea085bbce596)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10199523f6313cf622a2f3bd3ff4f4da587bac5ba3b5aa796d640aef3af13d36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf601b17fcd0f04032a1b96be39b3937ae92187594809a838d2e36dd7ff085c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0435100b20562fa5b79601828b56f2795a7ef9165e81bd1512bbff2b95a7dd83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb9907be7104dee4097bf3db5d9ec4ca6d93970197c7a8147209282129e6d526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a759423a5b5f07dd9dd20f333c9e9f6fe229896b66d824b4509ce236c77c8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5801a772324b5d7dcc05c9fbfdeb7c88a5ce59d00bfc6fd4c182e2b49a5b9ed8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b821716ad13c6936f7625f285bf5e41317e6d5cf98e6887591eceb34cd8139c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b9e6b71688c040f0f863370ff79cab63341a389a2adcb7cf10bdd4081a1ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c6489c5e8f6917f6fc2696732c7a6c5fbcb46eedbb0577fcb7883f77ea5e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590d8e1359a88de75ecf8164438ea161d0a1b229d2e99ee063d1c17b354a2ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c047a9c4d4494d99dbcb505f80f837c07450627a24ee267a4c4c7f77d9df9377)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92d231b9c893fdc382dde06526f5c088ef591779df98e1bf334637b3d0a36f2)
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
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__197a321f13c9752a82095c7426dd24eb148dbbf0c34bab29e10c9fe82b68d5fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d95c1ea94d8831b9606f38673ce05ce3203ac46d7ef0b5443dc288b7fb45a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e69b5317bbb3ed206836828a22b13f84102e9cacdd7bba882b488a5b8beeef7f)
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
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#api_version HorizontalPodAutoscalerV2Beta2#api_version}
        :param kind: Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#kind HorizontalPodAutoscalerV2Beta2#kind}
        :param name: Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject(
            api_version=api_version, kind=kind, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putDescribedObject", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric(
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        value_ = HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget(
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
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObjectOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObjectOutputReference, jsii.get(self, "describedObject"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(
        self,
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricObjectTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricObjectTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="describedObjectInput")
    def described_object_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject], jsii.get(self, "describedObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd1e4fbc1baa175f6b41d570282332197ba865712bdfbb41cc2e3089a28a69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d08f5987e8d9bc05a715dfd8fdc8aa1ba0f7a1a93902d9b6792d95c6342b56)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricObjectTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricObjectTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef4dc46c2300c35f2138a3856bd4f378862f02356b6b4ae937719db653232521)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a4dd8144f9895c403d8051f9987ec1040f7d3c2ca88407b30133db46d110469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be3f0e5ad8c77cb375b4fa44330f5d6a7b5c4b26f9e8340bd747054a0999da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3a8be35c82590d69ed659c6e8a2d87578a4dcdfe8025ee46d3e26c711fb58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b10dae64a6b130cbc6d86bd5780966508fc64deb423ef1cb42c35b78f16425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed9a004dc83e1091c6b695967f5c70579a4d0a05a10a4e75bc0f7469de9c096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebf36a345f0ab5ec1dde62c27606521804a7c9b4477033389adfc18d8417928a)
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
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: name of the container in the pods of the scaling target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#container HorizontalPodAutoscalerV2Beta2#container}
        :param name: name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource(
            container=container, name=name, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResource", [value]))

    @jsii.member(jsii_name="putExternal")
    def put_external(
        self,
        *,
        metric: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric, typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricExternal(
            metric=metric, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putExternal", [value]))

    @jsii.member(jsii_name="putObject")
    def put_object(
        self,
        *,
        described_object: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject, typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric, typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param described_object: described_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#described_object HorizontalPodAutoscalerV2Beta2#described_object}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricObject(
            described_object=described_object, metric=metric, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putObject", [value]))

    @jsii.member(jsii_name="putPods")
    def put_pods(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricPods(
            metric=metric, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putPods", [value]))

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        *,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricResource(
            name=name, target=target
        )

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
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceOutputReference, jsii.get(self, "containerResource"))

    @builtins.property
    @jsii.member(jsii_name="external")
    def external(
        self,
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricExternalOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricExternalOutputReference, jsii.get(self, "external"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> HorizontalPodAutoscalerV2Beta2SpecMetricObjectOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricObjectOutputReference, jsii.get(self, "object"))

    @builtins.property
    @jsii.member(jsii_name="pods")
    def pods(self) -> "HorizontalPodAutoscalerV2Beta2SpecMetricPodsOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricPodsOutputReference", jsii.get(self, "pods"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricResourceOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricResourceOutputReference", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="containerResourceInput")
    def container_resource_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource], jsii.get(self, "containerResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="externalInput")
    def external_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternal]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternal], jsii.get(self, "externalInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObject], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="podsInput")
    def pods_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPods"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPods"], jsii.get(self, "podsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResource"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResource"], jsii.get(self, "resourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__aa32461d55274b5744fef104344e4cc927daedc33c1ca5eb70fad39fbfc9f501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b43d6618a13af2870cd4e01ef3ce681ae4dafb6571d6e77af23a14490c585e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPods",
    jsii_struct_bases=[],
    name_mapping={"metric": "metric", "target": "target"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricPods:
    def __init__(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e295c10034e1a77b29c15437e4d97cec8056de792551b9e8d905f37fba1304c1)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#metric HorizontalPodAutoscalerV2Beta2#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricPods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc5767b474b65b29a9ac74e22414acd608e7bf1da53918c999d0a3edd649d11)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf357473e341a68db410acc184adab1a8ef957f6a617384f8cd46ec20be3716d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f24dcb1d831c8590afe58165eaebacc94f293575d8c0ea487ad78c2c5dd6f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703abff868149f60b449598b7cd3f7f8b1bad1747f07db89f223c744371bfbf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8c7c138875154d1c7657c82a3631ac5a7211759baa540fe7f400c35f809815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_expressions HorizontalPodAutoscalerV2Beta2#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_labels HorizontalPodAutoscalerV2Beta2#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976c820109307fe6527ef9003e8468dbfc642d28f6671d92c321c400cf412db0)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_expressions HorizontalPodAutoscalerV2Beta2#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#match_labels HorizontalPodAutoscalerV2Beta2#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c347464b2d5890eef3b00fc7f101e0f3b84de1b037e265fa51d53a28ca197983)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb334037e3fc081db989436dd240346433a4d2001329d92b49ab6ceed2f00b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e38ab186cedb7524293af3c66211a169342be89d592f9e94ee4ad319fa5182)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd1a8a7c81c39c00ddab729eab27c5511dc22d8a4bb865af4196db6bdcbcdef9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b025b77563ad0d8b1b00834a2f247732d59b7ef5b26a5b515da669402008a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97416c41bca84e16ae57301aa0218254bc1b767532ce2324d358509ef1f5b629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#key HorizontalPodAutoscalerV2Beta2#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#operator HorizontalPodAutoscalerV2Beta2#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#values HorizontalPodAutoscalerV2Beta2#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08b339a3dea24691e99884e56bceb823f0793e1138675a07f98389b44816329)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#key HorizontalPodAutoscalerV2Beta2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#operator HorizontalPodAutoscalerV2Beta2#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#values HorizontalPodAutoscalerV2Beta2#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beabe735ded7b02ce5a8a2c12952ac8cdedcc6955ac340008c037e7962ee29ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01afd78b6a63746c3a2202b329f3ab4591d5acc8e4d9865221d78a590622015d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dd26f787ece5aa8da8215795ac3851ba85c8782d26d9ce6a74da5f819f452a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aecc32a1e7b294079d396f4b977c028d12508a44b593254bd4c67ecc12a44fa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c83a9c7fe8e492a2bd1e204021c8fab10161582ed51f982bfb2c6292bab4251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85869936f663709be8b7689b4a980fb6453baf5fc6ba99cb8682add9d3cad8d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd8871cf08ca0a2c90fed33fd046c190cf0d56b7997cff9807e9a9bcbe6b68b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a81a4dd72f32a25a0b3aea8036c2a0c0f565f93407bd77aca61b2930b2117077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b40d43f05c23aa76b27a471dcc044c8cf044d21d900a8ea9e18e18daf46690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c34ec7231cc767144db6b03e3eae22a5b2ff146bd5c125e8920046a68ec099c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a37182dd53ca6ade18ba75307c871bf289d6b4b34d0fbcbea5bd3016588dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__806c5e2e2145eb7728dde8397b19865a5f0ad84e75036f5157925870b85343eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4d98accd8af26af825bfb5a3603fcfb58e2519b8ac6c57b6545e7892840e92)
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
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c5fc716dd179f86a63eb6a852e9113bee18b605da7932c5c7f46d7b043446675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa50e19bfa1be3192a5b5aff1e17133c0f0e00b4950e2b2998c7f7046a4bf6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__993cf8c3d84bcb80b57d32ef10306e39451e82e8492efbdf5e4ade04e0604554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#selector HorizontalPodAutoscalerV2Beta2#selector}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric(
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        value_ = HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget(
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
    def metric(
        self,
    ) -> HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricPodsTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricPodsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPods]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4257072aa57ba356bf15521aa612d00ffadcfee3e669882c680c6b3062376399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ed104156e221dae89f63502d5a8d2ef36ebd81ce9a6da72e71c0a1d238527e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricPodsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricPodsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3052d86216c52317319c22f357345753f5e75a3f3fabb84c1c5a84141cc0f74c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__553f590e9805a809eaccb755db172ff4d3ac985985e312437a34e828ba5af9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195f0fd0095cf1702f53eaa2206cbcd67c419a89325d850abe981757c98779d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5114ab6da44b47211f00b27f8302691893500a9dc32dc5c9d4c0c6d01bf49a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba60a87cd4bbb126934209469358e58cc48f0902a108dffa44297795853282e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15abdc368425965416e3cb450530365f959014d81733c5df5673a673dc3086a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricResource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "target": "target"},
)
class HorizontalPodAutoscalerV2Beta2SpecMetricResource:
    def __init__(
        self,
        *,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e37156819ed46a4e8db73ad035d93e2ec167cda3e98254a50e5cc84b376f61)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#target HorizontalPodAutoscalerV2Beta2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c04043da6fe695c28d1e880943ee0cd53e20871c54313fec65ecdbbd5173c8cf)
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        value_ = HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget(
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
    ) -> "HorizontalPodAutoscalerV2Beta2SpecMetricResourceTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecMetricResourceTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c9ef9286d27519641a94a9327f4af321406503985693c9d49adda3cf08cf98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6544df05aa06f6bf9324f52a2723f4f32d4275100aab015d553572d7bebce34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9dab9d9d9da0bfa06a75bde46e48787677bb043c9dabc2184c2c9c4b0896c4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#type HorizontalPodAutoscalerV2Beta2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_utilization HorizontalPodAutoscalerV2Beta2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#average_value HorizontalPodAutoscalerV2Beta2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#value HorizontalPodAutoscalerV2Beta2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecMetricResourceTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecMetricResourceTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac8919096f9bdcf48ea9137f854136fb4cd2a0f8dacc3b123a62918eff3c0952)
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
            type_hints = typing.get_type_hints(_typecheckingstub__216966b67960dae68f1b7e2b48977c7e5366744e93bf855e8e48302214295cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfacd4403187c31ad6fbae2349f207e5e6ebbeb01637dccb08d37663c3399d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d29f274f661ea5ee739b0fdb623f5f7a873f1317e34deb36447820a90d5461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0957c9f653f6e1ead311cbb7dc4b1e6957146679bdc796bbb798ca3bf4427944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c714921b1ecec73a891112b755ee25ecf9a77fec9b3155457d63081c69adf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2Beta2SpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8db93467321d53510cd54e8b2a2cefbe5de7bb4c96091723a290d9daa3f56a41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBehavior")
    def put_behavior(
        self,
        *,
        scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]]] = None,
        scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scale_down: scale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_down HorizontalPodAutoscalerV2Beta2#scale_down}
        :param scale_up: scale_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#scale_up HorizontalPodAutoscalerV2Beta2#scale_up}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecBehavior(
            scale_down=scale_down, scale_up=scale_up
        )

        return typing.cast(None, jsii.invoke(self, "putBehavior", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba4ac4d6fbe2b95fb1d3937c9f07d91a43848e5d9cab036776d36cbcc594c9b)
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
        :param kind: Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#kind HorizontalPodAutoscalerV2Beta2#kind}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#api_version HorizontalPodAutoscalerV2Beta2#api_version}
        '''
        value = HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef(
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
    def behavior(self) -> HorizontalPodAutoscalerV2Beta2SpecBehaviorOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecBehaviorOutputReference, jsii.get(self, "behavior"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerV2Beta2SpecMetricList:
        return typing.cast(HorizontalPodAutoscalerV2Beta2SpecMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleTargetRef")
    def scale_target_ref(
        self,
    ) -> "HorizontalPodAutoscalerV2Beta2SpecScaleTargetRefOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2Beta2SpecScaleTargetRefOutputReference", jsii.get(self, "scaleTargetRef"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecBehavior]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecBehavior], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetric]]], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleTargetRefInput")
    def scale_target_ref_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef"], jsii.get(self, "scaleTargetRefInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4823f4503091e2091f3374591a2e23281c2858684e8ddba0429e1dcbb66820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b6b537a84c3b8c194b38186f4c3f50975d0c0ff84c5686359eab8df64e3923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilizationPercentage")
    def target_cpu_utilization_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetCpuUtilizationPercentage"))

    @target_cpu_utilization_percentage.setter
    def target_cpu_utilization_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475994385a21cdd933aa38b3005b884e8f91c2f4082329666aeb0cd635acb9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCpuUtilizationPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerV2Beta2Spec]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2Spec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2Spec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed0a4bcd28ac2d9e00cf11a4785ed4c30fe4b07c920453c1d18bd4c8af05345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "name": "name", "api_version": "apiVersion"},
)
class HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef:
    def __init__(
        self,
        *,
        kind: builtins.str,
        name: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#kind HorizontalPodAutoscalerV2Beta2#kind}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#api_version HorizontalPodAutoscalerV2Beta2#api_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f472fa253e83e7ce259a677bfea94a846182a64f1ba2577ddf116f98be07b3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#kind HorizontalPodAutoscalerV2Beta2#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#name HorizontalPodAutoscalerV2Beta2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''API version of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2beta2#api_version HorizontalPodAutoscalerV2Beta2#api_version}
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2Beta2SpecScaleTargetRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2Beta2.HorizontalPodAutoscalerV2Beta2SpecScaleTargetRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c58a8d212c9b7acef75e2f59fe17cba048c95394bb940763195258adaf2f020)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3901ab3f95c0af1951944c4176f19fd75f0104705705204b923b1c770e597109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d83b87c0f0d19f0e6048e1a388dc9612e22704e05f399548255fa18b2f35f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc57546f550cbf52d93e22e20cd57ca0e8d3f89128aedd28d51d4fbfc787b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bcdc5c19bd4526da0ead86b360839974d820ea89ee00dba017d74e56220cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HorizontalPodAutoscalerV2Beta2",
    "HorizontalPodAutoscalerV2Beta2Config",
    "HorizontalPodAutoscalerV2Beta2Metadata",
    "HorizontalPodAutoscalerV2Beta2MetadataOutputReference",
    "HorizontalPodAutoscalerV2Beta2Spec",
    "HorizontalPodAutoscalerV2Beta2SpecBehavior",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownList",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyList",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicyOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpList",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyList",
    "HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicyOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetric",
    "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource",
    "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget",
    "HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTargetOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternal",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget",
    "HorizontalPodAutoscalerV2Beta2SpecMetricExternalTargetOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObject",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObjectOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget",
    "HorizontalPodAutoscalerV2Beta2SpecMetricObjectTargetOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPods",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget",
    "HorizontalPodAutoscalerV2Beta2SpecMetricPodsTargetOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricResource",
    "HorizontalPodAutoscalerV2Beta2SpecMetricResourceOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget",
    "HorizontalPodAutoscalerV2Beta2SpecMetricResourceTargetOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecOutputReference",
    "HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef",
    "HorizontalPodAutoscalerV2Beta2SpecScaleTargetRefOutputReference",
]

publication.publish()

def _typecheckingstub__f7efb896ce085b01bbc12085c8a0b1faa6583fc1b68c94ea1e643c2fd538c1b8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[HorizontalPodAutoscalerV2Beta2Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[HorizontalPodAutoscalerV2Beta2Spec, typing.Dict[builtins.str, typing.Any]],
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

def _typecheckingstub__5f1760332d80aca29397a6af3e3fe8bdd897f944b04699755da43b6237e22b0b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7c58fa181441acdcf4b6e16936fa862e4277fd27b7615b8414b88801fa999f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020a4c310b48daebe732779860f9d1e953abe33635a6d44a7e0fed12c56d93d2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[HorizontalPodAutoscalerV2Beta2Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[HorizontalPodAutoscalerV2Beta2Spec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d8d4badc03438aade768ff3e18209cb9f305dc364ab83a9b3260d93a4b1318(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    generate_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e8fa5e81febf2a050769c3559aceb4d3f35cdcf67e6df029702327429089ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2dcc6af7b79edd5c98ca81d1dd2f9457c188ccc6f62ecd2d94b7da4b8bb1a0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb59e97833eacd8b3ff1daa089c577072b125b959c631ec8f29c7b8431b23950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd6922ab06c96c7d7a60442d9a6b35380c8e8fac37ca3d2970903fb37508428(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f6d87914a7a4c03ea114e7707740b1aec57b7b7b82e46666fc358f980c0bdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26957d4424a40e5a24bb2b9f6d477e5e8f399fb211d50e2cc574389185a506a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d3eb55fc9735e29a04d883e01b2adb8080ab6dd7f79f88d681ccef1bbbb75c(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6993d2b2c23c5111443dce34a89451890f0f94fe32cc929c7b1feb502f49587b(
    *,
    max_replicas: jsii.Number,
    scale_target_ref: typing.Union[HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef, typing.Dict[builtins.str, typing.Any]],
    behavior: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehavior, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    min_replicas: typing.Optional[jsii.Number] = None,
    target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ed5ddb6578ca32f355e7194721a673e096cd2db911aa6986c465cea34b02c3(
    *,
    scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95dd083da1127bd3aef7985b0df56529c7739c4bce855b00797c786bdf3a4c38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f0aebc832f5d0ecac335013d2b8f55155cfec10c1ccaca87d7b3d90646bd5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fdd099721eb4b92599face2934609a644200a1fcef6e91d2ff45239bef7a61(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c7ec2484915bd9e11460270ba5ddd4a5b4915bbc56d911bf02600472a8c487(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecBehavior],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0c548ef1a0e5b98b9cdb0b84d6d796adcc6185d19452b61d6a3935589567d9(
    *,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy, typing.Dict[builtins.str, typing.Any]]]],
    select_policy: typing.Optional[builtins.str] = None,
    stabilization_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe13766164151fe2a7e54142e5b6db293196316ea7f0aad894ba0a8a6db97ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b952aa4192599e0906d88231346bc2652fb7cb96f531c81012b319a35ba154f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58627c09f5a52545023e00bf1de05e3e30d165d094c179ebd2c0678b15168a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0491721a17b639067a996b83d54f630e11419105136cbf0c097149bec37d6375(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2227100e9fed31aed82e7b9d8332c2aeb09f84cb8df88b9ffd25ee09ec3d9f60(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731c70d073a4aa93d36afd3e32b711c214e613c6aecf72ff971df59415f0004f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558fcc7eb93badf4670899ec44b4d35dc2d4473dc6e7ef21585c0cf47e29ecd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b53687d16111f56ced26495e45727a742a6031b4c73a956f5edbc7b2aaef9c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70575688112ff3fb92f9b95edaedf2d022f8e5035c0dee6449e70bbb48a6890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e000b95e7d57050562b72949063d83c8b723f6f9b7a89f88f5011d8fd897a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd50b5f2448c96eff9f29ab5d9af1485aa77a669335da9d2461a1897c695c43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDown]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1391ab97209bfc620b90407ef99f6c4d1ea4a5d8a4114c730b24095f8bdee39d(
    *,
    period_seconds: jsii.Number,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37082af92551cf4c8f0e6b5168cbaae300f9c9e6d4b745b44b4176f810f59d26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e9a1dd0412ceefb954bbb7c7249279cd1a79a6799326d98521e429bd681fe3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67813a26f67acd16866f1f9e71d526ddf8947904d44fd4503087ed842fd5653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54273a71f1be2ac4d1bd6f99005400ee7e35386249de11a73f75152c8e52b344(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70afd23f039db962861ea802822ad4a1ff58a6adbb21b63f082bbb7540003a67(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536b6c5ddbb434a5d8cfbd293770c158c879df788d77d8c7fe7654c5cd901d69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a852064f919694e7a6a00e125fb55d5d2de33aeed1d0d3de51b3da17b6cb1712(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d4ef02e41ae909a1c11dd2380bcace06063b3cd3dd1bbc0c3fdfea62083df3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c0d1e967dbf921809f8ff2c9a7930c53d9aaffbce6d1e3cc89da32489fe422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17d629edd2d84bdf31a9d8af3bed88707c322ea3b30a966e67af38ce8125a7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de39642650f316d2c2b8f904010fb411b7d03bb4fed93554b9a0fb45c5b077f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleDownPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5c15822532a323bdef942eb8acaed64c96379e862f46904c4909ad9b323277(
    *,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy, typing.Dict[builtins.str, typing.Any]]]],
    select_policy: typing.Optional[builtins.str] = None,
    stabilization_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deae2d7ba6bec9bc4d152ae1d1e37f47530c6735ef5d0db99ba1c0f526508d03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7381207b5f8ac58a9e696f28628236fac962f63f926a8e82f9f5a9195279995(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a946c61ff03658bbe756c0a4bb0e0c1fa406b86614185e363ba1f6081e3f8a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b56025aaef68cc4dd31c6e64c30d1967292c7d532cb9ef01ae7fa4ac5184002(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e65445488574f3086d0441f9da2f7af61e92073797a2ae45f7ca0bb1731265f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a12462d273c8ef60b4eef9f093c64d08b3158b2c6d4a7b391c1216c5ce86850(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ea0bac7f697c938a48f2c306980b77fe1bd5cd0c107a3c115be5a1dfc8fe40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8eaed5bbf380efef1000fc51b9deb1747f8b077e97d195e8711ba777cd04b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa62022b21c38dedd4fc141604375dd8bf0242251c27f73489e5c17fa880aac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b2a399de0356f2f7503364da72d2771bff0fbff9ecf09f7d898bf2b9ad1b6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f49c705778335937c964ae9043176d2c2046d7dd0e9028474baaa735f4266e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f260e7fc0c6454618ba4b15387ed76c7d2606702d79385eb7ac41a4d406b073(
    *,
    period_seconds: jsii.Number,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f647bc78de9f18d8cb1e3bba163c66d4d23bf22553cd9dfc5ef82bd41c8b41b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49476af2584617cf6075317597cfa5ad73739bd30b1bd50aead37dd421c42fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4477b795f76bf54dde6b70596cb995b6742bb5c5461fb50456035fc1c8129cf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0626f46a878e39cc30dafe264ee178df27672dbb413656a0cce7beb4972436f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feab2ba404e1ce73297ed8d37d72d22bddba70283ac51220b5b46955a9e7bb70(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620f7cd133c0a3b54c1a81e4a0dc6f97e798fd21111e470e2041c885e26fe8b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f0e2febb382ae5576fbf40826544a27e87bb81161dd3268de1d9a11576a6de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90cdf1327ce08722cad4c8f5d2824b1a126ff46eef265c1e395922b80b4bd94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3149a27b68e3b939afae7ae290073534da80163a6fdfe0604f7516ba8ce92b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d534a8416bc6c7da797f9e7e6433502fc4b99123aa70dd6a739242a7f61c2aab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add4a0168065167487c19aee9ce039e171259abd6f8db97fb1b35b96afda54a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecBehaviorScaleUpPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e44976d61d0e1ddb6f2c5e6041b5d288233e42566bd37bbdc9f1ab2af185622(
    *,
    type: builtins.str,
    container_resource: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource, typing.Dict[builtins.str, typing.Any]]] = None,
    external: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternal, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObject, typing.Dict[builtins.str, typing.Any]]] = None,
    pods: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPods, typing.Dict[builtins.str, typing.Any]]] = None,
    resource: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricResource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aec61a7fbf088392198b9d4f97b4217fd530eb80fea42de7e35d6117fb972e2(
    *,
    container: builtins.str,
    name: builtins.str,
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b93dada074c15a4d2515906647f7be0e04d036a21bdc9e268cba4d7d1713600(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a0dbb7184d46e3b5e3ac1784100db030f8af17c70b19118a49b07752343737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9270d332606fe59f748498d56ddd84ad98fe504dffc9415eb085319ccf87bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691450b07f5e3867691788eca603bea9274155de8297007abe189d48c9496785(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44ebf76c498bfc8ff289923a585620510c2407b20e65ebbe782bebf624b36dc(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1984335f7f04d091ee5de5b8e7a62da8ada573530d219ef60f4fef2700b33b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d40167ae7c4142e7059329bba776b6841c3fc396f5cac23a4cb8c029013de0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ad8794fc2ad91e2106507a0185a7f0cda127f77481b06b1a79b68051c45f3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e6b0bb32cae69b118083832ba89b28841d6cea15c04fa25fb82556dd226bfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54903f0e5995986b99af26c9cd0ca73f4c67ad47c57d8982aee590224017942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef29201603d65012e5cc9732246b8b8ac7e0a4e6327f1f0b89453aa34ebf0e6(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricContainerResourceTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204a2b700a75b468d9a4820ed5cb7a6aab2d6bcd351f0a6fc36fe751a6e6bc8b(
    *,
    metric: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791927e591b856ec7d8bdb91da95cc77708d7c549e367e905a5e7e25b0e1ef8c(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c212344476e17453ff6186e7ab26b8a8b2c7109d98b50b86ed5743223e617ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bebbbdbd3efeb805efb265a6782b71dd33908971ada2616a7a9a23d3ff590d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0231354f092d81a1f05efa897236b57f9cea9a380bea4c15e62b4b753686caf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a8239570068b061a1722c6b45f3d37480703f6525e97efbd8adb6dbfb5d1fa(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c60788e22a2c62a576be5bfc01659cc28f03d96036f72b4fb2170f13f4f869(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f2439e1c8216bcb3051dc4d65eed66e98278deac2cf77392656898f6fddcc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e380235db2a3098fb2c9963324898f3236545a73d2e8a82515620bd915c4161(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844b953c660e2d87dd39d912e54a6c94ab751b7fbca9dec299ea41d1900546a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f98f4d842dce0aa7cbeefede345c2ea6902429c2148217fa8a6a088b615f522(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780b94cfa747e3eeb12a0d693dd1736426a01ee7d1d6b1e6713d1b3ff1ff5873(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf943d93add3a06169b53394c3ae6a85e38cc2ab05222d86709a3556a8ab6fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881b7f7a1104a4f26e0e7718c84d70e0bfdc44e7ba05c452685ab44fdf36ccc2(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1f76ad11d9cf91de65b06db65db4e68dbe45e4d02776ca7e69c87bc64636b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a5e931709f2e3937f64392e5124e604a223ffa9d6945dc06e9a8fef5484f6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e327249bf639e78c1762ea900114e8642a27df08d0518e8876e5a26d10911a46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20641f4a41fc84762af371fc0384e57f8b70140b8503990272cac6fcccab1756(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ba115b6de10a3ee2055f4c34dd4a93b30b8cb254724d385300cf06b614659a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d15c6ded7d3c9a5f2c5010b12ff3aac4daa69c0a1f448f905c4d658ad6d82f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561fe0906405e458c8e84e421a0e5b8a94ec386d9e68fb37cc09f95cd2a951cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fa06f91da87453a9a527f2962a1cfc6fc0e1d8076b615abfd8766a52eb76e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0d5ad7839c26b6493a185ba79c3cb0344f4aed06bb6c3dbcd0ac18c266c6c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12e00fe0bc7e2f9833bb7568c9992d038bcd704751cbb53ae1f9a26c55db0eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88326274806631e116b94900456e6d92e7463f630989630fe4a32389d499da6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32eb9c059e13e81eaf1800fd2578f3604bc2de3fd660297fcffa34a340f43686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df079bad353c5686c93e2a5f9be65828ef11ce7dd488063bf2463c98365ec87(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41b5fdec9e0305b8b595ca7e8aef9f80091275aa8807a63ffc84029efdb5a0b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bab6993b1906d5c8a29b52a9998d0a7c6c55c4fc1c31b34ea996c808558341d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricExternalMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ee6a66f7adc183eb8a9a393255355ee8e994a9a8bfe362744bca90dc2138f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986aa47c6677b597fd0b7e267d85a66a5571e736be6835969943f6ca2e48c3a4(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642c4984df85d586ec63da14673a21e8b06414c5fe410cadb54aaf872f5fcd8e(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad27825f967be445587955e8f64ebfd0ed19886ab3147e799ec3c3add99ddd08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8f643946f7a73a21c6143da8de4e4f860895e312b21ca5b47bfd550e5f5712(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c945fbdaddffe157454a1247cdddeaa9c76f9619ea98d2ab9b4c2d254fa1235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45778e344af7954e987f98445176dc21f7350f03f85ce5acd04a8c9f611a709a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5068488711ee3cabc303264c1e42a3b097bf7d126b7f6a93f96c8dee34d9c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba2035aa14e6ffb5cc95ea7fb1a1577be55cd9688d949658e23cf5355a68c54(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricExternalTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d345315880793d874ad486ee9f53be1bd16b24abddc0b5112a242847d87b2722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34b81f4e1060be65eff79bedf16d2243ec8778881f51581c37574257804d847(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c542fb3757a932c7b43e2734dcfaf0efb386121141dac6c53283dcbe92b8d26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53ed911a0413566df0c1bd985143371a05b990af492cca7a239aa4d99dabb21(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13a619add32669090bf20b5108b9a05b806af274a7f55dd6dd8bf53613f1675(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc2285d25cd70ac1dbd89c0e53503df04c6e3723ae49eb12d78dfc429e79ccc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e612b14605990c6dbb997d3ba460e95d5ccbd7eda657bcdbd0594a11beeeb79(
    *,
    described_object: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject, typing.Dict[builtins.str, typing.Any]],
    metric: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e047be655c8b715a802a80f0a550a86bf28d15ca67d3e1e2a3fbafe3a55753f9(
    *,
    api_version: builtins.str,
    kind: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb71ced805485b1f2a362910a3afe9b0e411e7b6fca35efffa5456d7a969162(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ead282309e42485f07baf82180438d379505a88b78a58c64da39dab068cf7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cdf39c88e80b1d2a81e1b33bad345783fa6aebc1e8fed60189087628025b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a095151479a110a167d33fb1d6603f070bc2b184cad9b5aefa7f78b68ea3a22e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f8ebf34f578b11c72ff0f1adf979539c19350d54add85bd981f22f82bd50af(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectDescribedObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989068403256f4d9d89a1f8747e7e946cea8619099616fec1fb11f3647e1f32e(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d245fc3e5e47583e916a04b88d1a47f9125f516bd85c1c167988b488b2b01de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dc52d7dcd28a2753974d49b926fb8769ad640ab15b3e416d8560ed770635a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb9baf5ae73b5ae0d8bc108cbb959341ca1decb1aa9e1648aa0457da7d7a499(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084ae44ef9416dfedf5d01c02acb919da89918f97194d7396c80d99760ac4994(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d284d6f8ecf2dabb95f13838cab0883190930964d2ab8f552683c6f4b39319d(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7293e21309dfd4a9fc2d99952fed4d33dc48ff26f2fb0b9d4e8527b8776fbb33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56a8e068628a4514b05936dea399107e1ce51b915c283db60c2ebdaf65bf6c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5385b84b414499a6e5acaeef0d4774c2894a94c366f1ed402082defaab1d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89a7721ecdcfcb6263d84063dfa993ae2173e7253ee430b2c6c537ddcf2b334(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49d578c1ec1b8ca8d3d24b39d2dd4890b05db8bc150cf2907325915e413581f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b67af3a65dfa80ab7030a3823849285a0ab613dfa7e116bb224e4d8b4c55498(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474501426e0f16c9b3352af94716ab03d5cfa0ec94bfff4e258e11b6d409c4a8(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf5321a9aa3dc4d9e694d8b7934d875771f3d1d1bb49d798ef2ea085bbce596(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10199523f6313cf622a2f3bd3ff4f4da587bac5ba3b5aa796d640aef3af13d36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf601b17fcd0f04032a1b96be39b3937ae92187594809a838d2e36dd7ff085c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0435100b20562fa5b79601828b56f2795a7ef9165e81bd1512bbff2b95a7dd83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9907be7104dee4097bf3db5d9ec4ca6d93970197c7a8147209282129e6d526(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a759423a5b5f07dd9dd20f333c9e9f6fe229896b66d824b4509ce236c77c8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5801a772324b5d7dcc05c9fbfdeb7c88a5ce59d00bfc6fd4c182e2b49a5b9ed8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b821716ad13c6936f7625f285bf5e41317e6d5cf98e6887591eceb34cd8139c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b9e6b71688c040f0f863370ff79cab63341a389a2adcb7cf10bdd4081a1ece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c6489c5e8f6917f6fc2696732c7a6c5fbcb46eedbb0577fcb7883f77ea5e4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590d8e1359a88de75ecf8164438ea161d0a1b229d2e99ee063d1c17b354a2ace(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c047a9c4d4494d99dbcb505f80f837c07450627a24ee267a4c4c7f77d9df9377(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92d231b9c893fdc382dde06526f5c088ef591779df98e1bf334637b3d0a36f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197a321f13c9752a82095c7426dd24eb148dbbf0c34bab29e10c9fe82b68d5fe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d95c1ea94d8831b9606f38673ce05ce3203ac46d7ef0b5443dc288b7fb45a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricObjectMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69b5317bbb3ed206836828a22b13f84102e9cacdd7bba882b488a5b8beeef7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd1e4fbc1baa175f6b41d570282332197ba865712bdfbb41cc2e3089a28a69b(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d08f5987e8d9bc05a715dfd8fdc8aa1ba0f7a1a93902d9b6792d95c6342b56(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4dc46c2300c35f2138a3856bd4f378862f02356b6b4ae937719db653232521(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4dd8144f9895c403d8051f9987ec1040f7d3c2ca88407b30133db46d110469(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be3f0e5ad8c77cb375b4fa44330f5d6a7b5c4b26f9e8340bd747054a0999da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3a8be35c82590d69ed659c6e8a2d87578a4dcdfe8025ee46d3e26c711fb58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b10dae64a6b130cbc6d86bd5780966508fc64deb423ef1cb42c35b78f16425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed9a004dc83e1091c6b695967f5c70579a4d0a05a10a4e75bc0f7469de9c096(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricObjectTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf36a345f0ab5ec1dde62c27606521804a7c9b4477033389adfc18d8417928a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa32461d55274b5744fef104344e4cc927daedc33c1ca5eb70fad39fbfc9f501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b43d6618a13af2870cd4e01ef3ce681ae4dafb6571d6e77af23a14490c585e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e295c10034e1a77b29c15437e4d97cec8056de792551b9e8d905f37fba1304c1(
    *,
    metric: typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc5767b474b65b29a9ac74e22414acd608e7bf1da53918c999d0a3edd649d11(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf357473e341a68db410acc184adab1a8ef957f6a617384f8cd46ec20be3716d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f24dcb1d831c8590afe58165eaebacc94f293575d8c0ea487ad78c2c5dd6f2f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703abff868149f60b449598b7cd3f7f8b1bad1747f07db89f223c744371bfbf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8c7c138875154d1c7657c82a3631ac5a7211759baa540fe7f400c35f809815(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976c820109307fe6527ef9003e8468dbfc642d28f6671d92c321c400cf412db0(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c347464b2d5890eef3b00fc7f101e0f3b84de1b037e265fa51d53a28ca197983(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb334037e3fc081db989436dd240346433a4d2001329d92b49ab6ceed2f00b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e38ab186cedb7524293af3c66211a169342be89d592f9e94ee4ad319fa5182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1a8a7c81c39c00ddab729eab27c5511dc22d8a4bb865af4196db6bdcbcdef9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b025b77563ad0d8b1b00834a2f247732d59b7ef5b26a5b515da669402008a3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97416c41bca84e16ae57301aa0218254bc1b767532ce2324d358509ef1f5b629(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08b339a3dea24691e99884e56bceb823f0793e1138675a07f98389b44816329(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beabe735ded7b02ce5a8a2c12952ac8cdedcc6955ac340008c037e7962ee29ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01afd78b6a63746c3a2202b329f3ab4591d5acc8e4d9865221d78a590622015d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dd26f787ece5aa8da8215795ac3851ba85c8782d26d9ce6a74da5f819f452a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecc32a1e7b294079d396f4b977c028d12508a44b593254bd4c67ecc12a44fa5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c83a9c7fe8e492a2bd1e204021c8fab10161582ed51f982bfb2c6292bab4251(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85869936f663709be8b7689b4a980fb6453baf5fc6ba99cb8682add9d3cad8d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd8871cf08ca0a2c90fed33fd046c190cf0d56b7997cff9807e9a9bcbe6b68b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81a4dd72f32a25a0b3aea8036c2a0c0f565f93407bd77aca61b2930b2117077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b40d43f05c23aa76b27a471dcc044c8cf044d21d900a8ea9e18e18daf46690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c34ec7231cc767144db6b03e3eae22a5b2ff146bd5c125e8920046a68ec099c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a37182dd53ca6ade18ba75307c871bf289d6b4b34d0fbcbea5bd3016588dfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806c5e2e2145eb7728dde8397b19865a5f0ad84e75036f5157925870b85343eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4d98accd8af26af825bfb5a3603fcfb58e2519b8ac6c57b6545e7892840e92(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fc716dd179f86a63eb6a852e9113bee18b605da7932c5c7f46d7b043446675(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa50e19bfa1be3192a5b5aff1e17133c0f0e00b4950e2b2998c7f7046a4bf6a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2Beta2SpecMetricPodsMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993cf8c3d84bcb80b57d32ef10306e39451e82e8492efbdf5e4ade04e0604554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4257072aa57ba356bf15521aa612d00ffadcfee3e669882c680c6b3062376399(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ed104156e221dae89f63502d5a8d2ef36ebd81ce9a6da72e71c0a1d238527e(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3052d86216c52317319c22f357345753f5e75a3f3fabb84c1c5a84141cc0f74c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553f590e9805a809eaccb755db172ff4d3ac985985e312437a34e828ba5af9dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195f0fd0095cf1702f53eaa2206cbcd67c419a89325d850abe981757c98779d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5114ab6da44b47211f00b27f8302691893500a9dc32dc5c9d4c0c6d01bf49a61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba60a87cd4bbb126934209469358e58cc48f0902a108dffa44297795853282e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15abdc368425965416e3cb450530365f959014d81733c5df5673a673dc3086a4(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricPodsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e37156819ed46a4e8db73ad035d93e2ec167cda3e98254a50e5cc84b376f61(
    *,
    name: builtins.str,
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04043da6fe695c28d1e880943ee0cd53e20871c54313fec65ecdbbd5173c8cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c9ef9286d27519641a94a9327f4af321406503985693c9d49adda3cf08cf98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6544df05aa06f6bf9324f52a2723f4f32d4275100aab015d553572d7bebce34e(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9dab9d9d9da0bfa06a75bde46e48787677bb043c9dabc2184c2c9c4b0896c4(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8919096f9bdcf48ea9137f854136fb4cd2a0f8dacc3b123a62918eff3c0952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216966b67960dae68f1b7e2b48977c7e5366744e93bf855e8e48302214295cb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfacd4403187c31ad6fbae2349f207e5e6ebbeb01637dccb08d37663c3399d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d29f274f661ea5ee739b0fdb623f5f7a873f1317e34deb36447820a90d5461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0957c9f653f6e1ead311cbb7dc4b1e6957146679bdc796bbb798ca3bf4427944(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c714921b1ecec73a891112b755ee25ecf9a77fec9b3155457d63081c69adf25(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecMetricResourceTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db93467321d53510cd54e8b2a2cefbe5de7bb4c96091723a290d9daa3f56a41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba4ac4d6fbe2b95fb1d3937c9f07d91a43848e5d9cab036776d36cbcc594c9b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2Beta2SpecMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4823f4503091e2091f3374591a2e23281c2858684e8ddba0429e1dcbb66820(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b6b537a84c3b8c194b38186f4c3f50975d0c0ff84c5686359eab8df64e3923(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475994385a21cdd933aa38b3005b884e8f91c2f4082329666aeb0cd635acb9d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed0a4bcd28ac2d9e00cf11a4785ed4c30fe4b07c920453c1d18bd4c8af05345(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2Spec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f472fa253e83e7ce259a677bfea94a846182a64f1ba2577ddf116f98be07b3(
    *,
    kind: builtins.str,
    name: builtins.str,
    api_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c58a8d212c9b7acef75e2f59fe17cba048c95394bb940763195258adaf2f020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3901ab3f95c0af1951944c4176f19fd75f0104705705204b923b1c770e597109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d83b87c0f0d19f0e6048e1a388dc9612e22704e05f399548255fa18b2f35f61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc57546f550cbf52d93e22e20cd57ca0e8d3f89128aedd28d51d4fbfc787b23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bcdc5c19bd4526da0ead86b360839974d820ea89ee00dba017d74e56220cfc(
    value: typing.Optional[HorizontalPodAutoscalerV2Beta2SpecScaleTargetRef],
) -> None:
    """Type checking stubs"""
    pass
