r'''
# `kubernetes_horizontal_pod_autoscaler_v2`

Refer to the Terraform Registry for docs: [`kubernetes_horizontal_pod_autoscaler_v2`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2).
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


class HorizontalPodAutoscalerV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2 kubernetes_horizontal_pod_autoscaler_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["HorizontalPodAutoscalerV2Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["HorizontalPodAutoscalerV2Spec", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2 kubernetes_horizontal_pod_autoscaler_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metadata HorizontalPodAutoscalerV2#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#spec HorizontalPodAutoscalerV2#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#id HorizontalPodAutoscalerV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca48c85652b0edbd246a5dba3f8e43c5eb451c350c25afac190238bf0b33dec7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HorizontalPodAutoscalerV2Config(
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
        '''Generates CDKTF code for importing a HorizontalPodAutoscalerV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HorizontalPodAutoscalerV2 to import.
        :param import_from_id: The id of the existing HorizontalPodAutoscalerV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HorizontalPodAutoscalerV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d42e70f1923c0a62f6650747298cfba09b949bacd462c06aa6127a66f48245c)
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
        :param annotations: An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#annotations HorizontalPodAutoscalerV2#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#generate_name HorizontalPodAutoscalerV2#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#labels HorizontalPodAutoscalerV2#labels}
        :param name: Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param namespace: Namespace defines the space within which name of the horizontal pod autoscaler must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#namespace HorizontalPodAutoscalerV2#namespace}
        '''
        value = HorizontalPodAutoscalerV2Metadata(
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
        scale_target_ref: typing.Union["HorizontalPodAutoscalerV2SpecScaleTargetRef", typing.Dict[builtins.str, typing.Any]],
        behavior: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replicas: Upper limit for the number of pods that can be set by the autoscaler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#max_replicas HorizontalPodAutoscalerV2#max_replicas}
        :param scale_target_ref: scale_target_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_target_ref HorizontalPodAutoscalerV2#scale_target_ref}
        :param behavior: behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#behavior HorizontalPodAutoscalerV2#behavior}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param min_replicas: Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#min_replicas HorizontalPodAutoscalerV2#min_replicas}
        :param target_cpu_utilization_percentage: Target average CPU utilization (represented as a percentage of requested CPU) over all the pods. If not specified the default autoscaling policy will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target_cpu_utilization_percentage HorizontalPodAutoscalerV2#target_cpu_utilization_percentage}
        '''
        value = HorizontalPodAutoscalerV2Spec(
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
    def metadata(self) -> "HorizontalPodAutoscalerV2MetadataOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "HorizontalPodAutoscalerV2SpecOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["HorizontalPodAutoscalerV2Metadata"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["HorizontalPodAutoscalerV2Spec"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2Spec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370ca6cfba557891cc14f42e9a1d47864dfde1bfaf3aedfedc7e59a878fdcc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2Config",
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
class HorizontalPodAutoscalerV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["HorizontalPodAutoscalerV2Metadata", typing.Dict[builtins.str, typing.Any]],
        spec: typing.Union["HorizontalPodAutoscalerV2Spec", typing.Dict[builtins.str, typing.Any]],
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
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metadata HorizontalPodAutoscalerV2#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#spec HorizontalPodAutoscalerV2#spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#id HorizontalPodAutoscalerV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = HorizontalPodAutoscalerV2Metadata(**metadata)
        if isinstance(spec, dict):
            spec = HorizontalPodAutoscalerV2Spec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0699a9669997722cf7347a1a85f3ccc6aa66e164b641808330c3a10ffcffff49)
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
    def metadata(self) -> "HorizontalPodAutoscalerV2Metadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metadata HorizontalPodAutoscalerV2#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Metadata", result)

    @builtins.property
    def spec(self) -> "HorizontalPodAutoscalerV2Spec":
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#spec HorizontalPodAutoscalerV2#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("HorizontalPodAutoscalerV2Spec", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#id HorizontalPodAutoscalerV2#id}.

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
        return "HorizontalPodAutoscalerV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2Metadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class HorizontalPodAutoscalerV2Metadata:
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
        :param annotations: An unstructured key value map stored with the horizontal pod autoscaler that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#annotations HorizontalPodAutoscalerV2#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#generate_name HorizontalPodAutoscalerV2#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#labels HorizontalPodAutoscalerV2#labels}
        :param name: Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param namespace: Namespace defines the space within which name of the horizontal pod autoscaler must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#namespace HorizontalPodAutoscalerV2#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e804b38c9b8d5046b9617012f73c7e2ff9d9e63136c95590ba87de6ecc9e3a9d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#annotations HorizontalPodAutoscalerV2#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        '''Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided.

        This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#generate_name HorizontalPodAutoscalerV2#generate_name}
        '''
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the horizontal pod autoscaler.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#labels HorizontalPodAutoscalerV2#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the horizontal pod autoscaler, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within which name of the horizontal pod autoscaler must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#namespace HorizontalPodAutoscalerV2#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49d4737b0229a6a7c43f84fc0e37a0eeb30df7bc22cfebc11a8a845c5d32ab3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5190936fb844d9dd1c240c34eb8344f437a43e458319a679381ba0998c6397a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generateName")
    def generate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateName"))

    @generate_name.setter
    def generate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12b9de274310b51a3ccf7bcd29964a3fddb7197e3bf88eea8f91fed69ed1b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666f9c4741dd18f718022e7ff0fe781e93888eeb9d0585a239896eeddc78cd57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded1c66e28404a0689d6a71c561d181d59b52b706b3ef48ac3ef320f09a9814b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279122ed751921a193acfc81faefe2b11e19726c7409d063cc8bce5c3b51cf18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerV2Metadata]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Metadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ffe169f416797db34aa63f592f994e40820fbfe48885eef8c141dba72387ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2Spec",
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
class HorizontalPodAutoscalerV2Spec:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        scale_target_ref: typing.Union["HorizontalPodAutoscalerV2SpecScaleTargetRef", typing.Dict[builtins.str, typing.Any]],
        behavior: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replicas: Upper limit for the number of pods that can be set by the autoscaler. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#max_replicas HorizontalPodAutoscalerV2#max_replicas}
        :param scale_target_ref: scale_target_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_target_ref HorizontalPodAutoscalerV2#scale_target_ref}
        :param behavior: behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#behavior HorizontalPodAutoscalerV2#behavior}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param min_replicas: Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#min_replicas HorizontalPodAutoscalerV2#min_replicas}
        :param target_cpu_utilization_percentage: Target average CPU utilization (represented as a percentage of requested CPU) over all the pods. If not specified the default autoscaling policy will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target_cpu_utilization_percentage HorizontalPodAutoscalerV2#target_cpu_utilization_percentage}
        '''
        if isinstance(scale_target_ref, dict):
            scale_target_ref = HorizontalPodAutoscalerV2SpecScaleTargetRef(**scale_target_ref)
        if isinstance(behavior, dict):
            behavior = HorizontalPodAutoscalerV2SpecBehavior(**behavior)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53448432822054c7d1a8ac05527a3ac3536549a7cbd5422c21d08e220d2a4de9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#max_replicas HorizontalPodAutoscalerV2#max_replicas}
        '''
        result = self._values.get("max_replicas")
        assert result is not None, "Required property 'max_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_target_ref(self) -> "HorizontalPodAutoscalerV2SpecScaleTargetRef":
        '''scale_target_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_target_ref HorizontalPodAutoscalerV2#scale_target_ref}
        '''
        result = self._values.get("scale_target_ref")
        assert result is not None, "Required property 'scale_target_ref' is missing"
        return typing.cast("HorizontalPodAutoscalerV2SpecScaleTargetRef", result)

    @builtins.property
    def behavior(self) -> typing.Optional["HorizontalPodAutoscalerV2SpecBehavior"]:
        '''behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#behavior HorizontalPodAutoscalerV2#behavior}
        '''
        result = self._values.get("behavior")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecBehavior"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetric"]]], result)

    @builtins.property
    def min_replicas(self) -> typing.Optional[jsii.Number]:
        '''Lower limit for the number of pods that can be set by the autoscaler, defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#min_replicas HorizontalPodAutoscalerV2#min_replicas}
        '''
        result = self._values.get("min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
        '''Target average CPU utilization (represented as a percentage of requested CPU) over all the pods.

        If not specified the default autoscaling policy will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target_cpu_utilization_percentage HorizontalPodAutoscalerV2#target_cpu_utilization_percentage}
        '''
        result = self._values.get("target_cpu_utilization_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2Spec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehavior",
    jsii_struct_bases=[],
    name_mapping={"scale_down": "scaleDown", "scale_up": "scaleUp"},
)
class HorizontalPodAutoscalerV2SpecBehavior:
    def __init__(
        self,
        *,
        scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleDown", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleUp", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scale_down: scale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_down HorizontalPodAutoscalerV2#scale_down}
        :param scale_up: scale_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_up HorizontalPodAutoscalerV2#scale_up}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9de99c691e74bb45630f65ea493f60a753936456e78484b7631adcb1e4cdaa7)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDown"]]]:
        '''scale_down block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_down HorizontalPodAutoscalerV2#scale_down}
        '''
        result = self._values.get("scale_down")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDown"]]], result)

    @builtins.property
    def scale_up(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUp"]]]:
        '''scale_up block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_up HorizontalPodAutoscalerV2#scale_up}
        '''
        result = self._values.get("scale_up")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUp"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8357c370f0fb7c5b0c500f4c11ebdaabf907c1cda640bacbd79a73769f8b7408)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScaleDown")
    def put_scale_down(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleDown", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d87466512b0e7bb5766492c7e4cb4cbc27ac123a8195e2f98b64ec004894354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScaleDown", [value]))

    @jsii.member(jsii_name="putScaleUp")
    def put_scale_up(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleUp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417ea81779205076b930d85e05187b0c1e1503bd254f18cb3ca8a9d3c31a7e2a)
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
    def scale_down(self) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleDownList":
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleDownList", jsii.get(self, "scaleDown"))

    @builtins.property
    @jsii.member(jsii_name="scaleUp")
    def scale_up(self) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleUpList":
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleUpList", jsii.get(self, "scaleUp"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownInput")
    def scale_down_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDown"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDown"]]], jsii.get(self, "scaleDownInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUpInput")
    def scale_up_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUp"]]], jsii.get(self, "scaleUpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerV2SpecBehavior]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecBehavior], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecBehavior],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363a714a9691c47bb7fb7e2fc7582d74f24a013c65ec911cf42a12d24af2ef1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleDown",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "select_policy": "selectPolicy",
        "stabilization_window_seconds": "stabilizationWindowSeconds",
    },
)
class HorizontalPodAutoscalerV2SpecBehaviorScaleDown:
    def __init__(
        self,
        *,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy", typing.Dict[builtins.str, typing.Any]]]],
        select_policy: typing.Optional[builtins.str] = None,
        stabilization_window_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#policy HorizontalPodAutoscalerV2#policy}
        :param select_policy: Used to specify which policy should be used. If not set, the default value Max is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#select_policy HorizontalPodAutoscalerV2#select_policy}
        :param stabilization_window_seconds: Number of seconds for which past recommendations should be considered while scaling up or scaling down. This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#stabilization_window_seconds HorizontalPodAutoscalerV2#stabilization_window_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560a39252b6878a4cbc18ed8b688cba3a6d1a662456b92abd93e72f9d596940b)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#policy HorizontalPodAutoscalerV2#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy"]], result)

    @builtins.property
    def select_policy(self) -> typing.Optional[builtins.str]:
        '''Used to specify which policy should be used. If not set, the default value Max is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#select_policy HorizontalPodAutoscalerV2#select_policy}
        '''
        result = self._values.get("select_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stabilization_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds for which past recommendations should be considered while scaling up or scaling down.

        This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#stabilization_window_seconds HorizontalPodAutoscalerV2#stabilization_window_seconds}
        '''
        result = self._values.get("stabilization_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecBehaviorScaleDown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecBehaviorScaleDownList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleDownList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__177708a2f7e2aa29fd69bac9cad8126ad01d7bafb19706a567167397011ff57d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleDownOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c354cf2f418b3c9812d7924f652ee62e12d4965025410db6d20463f1c474b84a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleDownOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17e4ca652926bc81d92ce615c015e10cbb5aec4ffac559e0da1b3d55ad2acf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40fb23cdeff98b32e7027f5f3a82e10e5593d464bd5649c57475f6c0880d609a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__933e66480256a4cbaf4c384865bcad389adf1356eed6c45e1899f83b19ab5a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDown]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDown]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDown]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7be231b96136f1aaf8026c2871dcacb107db7cdc45ebcea4c00672f9e31adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecBehaviorScaleDownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleDownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cb496cdfe59598da2ac946519c26ee8a3ab319a794018239268df24f132e9d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5f2fc376c3f30e2f22a42709de0b273425143caa84be46aa8422ba717b87ad)
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
    def policy(self) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyList":
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy"]]], jsii.get(self, "policyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__95be4c2a8d542b6e5a70e70699f223303c4cd7a420fdcb78145ed040c5a82f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSeconds")
    def stabilization_window_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stabilizationWindowSeconds"))

    @stabilization_window_seconds.setter
    def stabilization_window_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d8512d1cb186853bccf9b6b785f9a7a8432e2650c808146b438f4bdf38544d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stabilizationWindowSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDown]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDown]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDown]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b47dee7c7459dc421d58496b2c24a04a8cf659ba95eecc9c03fd565d0d8df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy",
    jsii_struct_bases=[],
    name_mapping={"period_seconds": "periodSeconds", "type": "type", "value": "value"},
)
class HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy:
    def __init__(
        self,
        *,
        period_seconds: jsii.Number,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param period_seconds: Period specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#period_seconds HorizontalPodAutoscalerV2#period_seconds}
        :param type: Type is used to specify the scaling policy: Percent or Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param value: Value contains the amount of change which is permitted by the policy. It must be greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac8f6c4a066d54a7ebb2022e182b1b8ffa2936b9278bd838dfb2fc8d8387a60)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#period_seconds HorizontalPodAutoscalerV2#period_seconds}
        '''
        result = self._values.get("period_seconds")
        assert result is not None, "Required property 'period_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type is used to specify the scaling policy: Percent or Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Value contains the amount of change which is permitted by the policy. It must be greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87d1d31357f5251e5002410f8c0d0cfcd34671b76a4ac7c87d17455451f469d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd62f564657e908b1b8758cf698917d7dd52d3af426b72c790074880c5a2deb3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5097127f3a98415ef40313d08d7b8c4e865ecd02bed9dca4b6a73e327bc71c19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f8cd9bf61f3e7c7a4cbb3b736f66ae81cf69e0cce9f8bf136065bbca2ac1998)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55f618b67befffac4fe200fbca6649028ec3b6346055f524c25870b21ffede1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57daa751d801d5a5943d243b7cfd0452a636268250abc29f4fe1191851a5a1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae8299a81dc0e6425f27dfe699a81006dbf14a156ca6c43d295160d73e66285e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bafea09da2367d8efa8f9d9c79e43778ab976c899a118d007aff59bd8dd5210c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defba12509aeabb4b1b66b1d09f10eaf9c98fb4e79c92036199c6d29ac0cb34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5ad568b70de9007c9afb89187261ba7d22f8382ac3566086ef4052fca76cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d801d648a698f5de70e125a892f4cd73f242a9744254c87c946a284a47e4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleUp",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "select_policy": "selectPolicy",
        "stabilization_window_seconds": "stabilizationWindowSeconds",
    },
)
class HorizontalPodAutoscalerV2SpecBehaviorScaleUp:
    def __init__(
        self,
        *,
        policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy", typing.Dict[builtins.str, typing.Any]]]],
        select_policy: typing.Optional[builtins.str] = None,
        stabilization_window_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#policy HorizontalPodAutoscalerV2#policy}
        :param select_policy: Used to specify which policy should be used. If not set, the default value Max is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#select_policy HorizontalPodAutoscalerV2#select_policy}
        :param stabilization_window_seconds: Number of seconds for which past recommendations should be considered while scaling up or scaling down. This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#stabilization_window_seconds HorizontalPodAutoscalerV2#stabilization_window_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867ad4b041cb0f817c0292be78d980c433905abf5bb61ee31a9e335028685aee)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy"]]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#policy HorizontalPodAutoscalerV2#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy"]], result)

    @builtins.property
    def select_policy(self) -> typing.Optional[builtins.str]:
        '''Used to specify which policy should be used. If not set, the default value Max is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#select_policy HorizontalPodAutoscalerV2#select_policy}
        '''
        result = self._values.get("select_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stabilization_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds for which past recommendations should be considered while scaling up or scaling down.

        This value must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#stabilization_window_seconds HorizontalPodAutoscalerV2#stabilization_window_seconds}
        '''
        result = self._values.get("stabilization_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecBehaviorScaleUp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecBehaviorScaleUpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleUpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55be2cf60442696143a428b244217392a9ed31444cba1f778458495b7d6a49c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleUpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be52f0c7cfdf85de8a47fced85c60fa611e81e900b7e10663f1519dea2e99c9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleUpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d358afac2dc436c47a32df71b44192f004b6f8133b2b72df34416b777b5c8c5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a26a3f9e1802c31032204f338f6a6511a56855687f303a83bb995179198eaf5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f500d7c980b2b9eb5d0e8ce99b9b068a78c3798bf39183edf8c34ebe9788212b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e1b529052b712af8307938d398454a8e967e95344fc9367bbd0d87911d0261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecBehaviorScaleUpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleUpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a2418aee35471981e81288bebf85352b690f619615620b1f4f3b9e271f94b3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicy")
    def put_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e805da76c4c54fc509e8ff4b6e26d0b835abfb6d3c0f07d15f373a6683622411)
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
    def policy(self) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyList":
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyList", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy"]]], jsii.get(self, "policyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f53418a1d7a5d4f719d1f92571526000192d65929bb7d6455b723f036971e140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stabilizationWindowSeconds")
    def stabilization_window_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stabilizationWindowSeconds"))

    @stabilization_window_seconds.setter
    def stabilization_window_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475c281696c121bdf4aac83e34f42e6ef427215d6bb14f0b43015319c2dd6583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stabilizationWindowSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3182150bce6a8948a5012ed8ef3551a45904c60e82a5bdf0ef0567cdab417056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy",
    jsii_struct_bases=[],
    name_mapping={"period_seconds": "periodSeconds", "type": "type", "value": "value"},
)
class HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy:
    def __init__(
        self,
        *,
        period_seconds: jsii.Number,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param period_seconds: Period specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#period_seconds HorizontalPodAutoscalerV2#period_seconds}
        :param type: Type is used to specify the scaling policy: Percent or Pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param value: Value contains the amount of change which is permitted by the policy. It must be greater than zero. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2544109ff0b0e2bfce45b551a610391be43003a80d1cbb022a150b7f5b0200f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#period_seconds HorizontalPodAutoscalerV2#period_seconds}
        '''
        result = self._values.get("period_seconds")
        assert result is not None, "Required property 'period_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type is used to specify the scaling policy: Percent or Pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Value contains the amount of change which is permitted by the policy. It must be greater than zero.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82018e7296d3587a8818e1ece0f54e370e269c17932e767dc9a4dcf842e10559)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a704fa8df2a43690b87d48fb77058ab3c9e8b6686b300e9c43372e3c346b53f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de57ab37d13b26157dbe037fb7f6575a5cd609560cc04ea81c9522e89ccab318)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4d0ff0b9b6d522b732bab2713722b2b669b2b19804c85554b26bd4557dd975a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__253598d85380e1f9319e8c444cd4008bc9c16eddf14fa87c9e3b0176b2aced7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1973ab8671f997efefc8976ffac8c765b3bf6897e3d721389db34aad85d3771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c40d489f6ac79e48a43004ee26184c6205f179e3c73d1c2823aceb254ed6c599)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f52cbff36c304064a3d16577342f7c93b501f802fa4f083d7120b4469d9ef6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5567fa75cb139d23215aa216d54665dd5f7d9cdfa8287a2a0a4df2b553ed6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07750549581aed268c6c1c06152c47eaf90e319c6c36b170d2eacbf2c5690f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240b26db47c2dfe6b87fa4a44647a0b9fa4f10916e39d30767da79d22105c844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetric",
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
class HorizontalPodAutoscalerV2SpecMetric:
    def __init__(
        self,
        *,
        type: builtins.str,
        container_resource: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricContainerResource", typing.Dict[builtins.str, typing.Any]]] = None,
        external: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricExternal", typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricObject", typing.Dict[builtins.str, typing.Any]]] = None,
        pods: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricPods", typing.Dict[builtins.str, typing.Any]]] = None,
        resource: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: type is the type of metric source. It should be one of "ContainerResource", "External", "Object", "Pods" or "Resource", each mapping to a matching field in the object. Note: "ContainerResource" type is available on when the feature-gate HPAContainerMetrics is enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param container_resource: container_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#container_resource HorizontalPodAutoscalerV2#container_resource}
        :param external: external block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#external HorizontalPodAutoscalerV2#external}
        :param object: object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#object HorizontalPodAutoscalerV2#object}
        :param pods: pods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#pods HorizontalPodAutoscalerV2#pods}
        :param resource: resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#resource HorizontalPodAutoscalerV2#resource}
        '''
        if isinstance(container_resource, dict):
            container_resource = HorizontalPodAutoscalerV2SpecMetricContainerResource(**container_resource)
        if isinstance(external, dict):
            external = HorizontalPodAutoscalerV2SpecMetricExternal(**external)
        if isinstance(object, dict):
            object = HorizontalPodAutoscalerV2SpecMetricObject(**object)
        if isinstance(pods, dict):
            pods = HorizontalPodAutoscalerV2SpecMetricPods(**pods)
        if isinstance(resource, dict):
            resource = HorizontalPodAutoscalerV2SpecMetricResource(**resource)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11541fce4ca0f4007735c91afa5ab6fdd143414298835dad8b1d971e2ac5c017)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resource(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricContainerResource"]:
        '''container_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#container_resource HorizontalPodAutoscalerV2#container_resource}
        '''
        result = self._values.get("container_resource")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricContainerResource"], result)

    @builtins.property
    def external(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricExternal"]:
        '''external block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#external HorizontalPodAutoscalerV2#external}
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricExternal"], result)

    @builtins.property
    def object(self) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricObject"]:
        '''object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#object HorizontalPodAutoscalerV2#object}
        '''
        result = self._values.get("object")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricObject"], result)

    @builtins.property
    def pods(self) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricPods"]:
        '''pods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#pods HorizontalPodAutoscalerV2#pods}
        '''
        result = self._values.get("pods")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricPods"], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricResource"]:
        '''resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#resource HorizontalPodAutoscalerV2#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricResource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricContainerResource",
    jsii_struct_bases=[],
    name_mapping={"container": "container", "name": "name", "target": "target"},
)
class HorizontalPodAutoscalerV2SpecMetricContainerResource:
    def __init__(
        self,
        *,
        container: builtins.str,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: name of the container in the pods of the scaling target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#container HorizontalPodAutoscalerV2#container}
        :param name: name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b279c073ebcf864b35712bccbebbddbc891fc7fa70029a92076061235c9f548)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#container HorizontalPodAutoscalerV2#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''name of the resource in question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricContainerResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricContainerResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricContainerResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8d52b40b81983655dbec0c192dfde75e1b9ed655328eec723e725940c57900)
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        value_ = HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget(
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
    ) -> "HorizontalPodAutoscalerV2SpecMetricContainerResourceTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricContainerResourceTargetOutputReference", jsii.get(self, "target"))

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
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28a8951456de4aa232c8b92513e49edf5bc43e182cf5d3bbb6131c9e68f9ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cae113e83c08ad55cab33bda053328ce341dae5d631e6ab0b544e00178ffa26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b100fa8df1c88c81001fbcf7dfd5036bb141ab759487f223f1f1a8b727282fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31403485a571ee5683e345ccdc6d657547f560e002841830664dd2ea13552a1b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricContainerResourceTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricContainerResourceTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbddf33aa389cd132fc2556c9fd522f788e4d9fe3098f98df416d4d5669a4cd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__904a46895dc76997d8c73754ef6f3ae01c321711b8bb7083f4e88c63bf1c45b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be80620ea575ada9d09ea4e8f91579fc00546b3ff07a8b2fecd1a373ecd2b890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c7254fe14ca5f02afab5590cb89cc2e12014a6d720ce9b2ff0ee36530399e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6b0d3148e82c211ac193f39c5f7d2d628585eaa6ec9a4e0a7b968ef20e1777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58fd3f826d3d103db2dc1912f209e478e81ef7506ad0e8a6fb069ebd1076d2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternal",
    jsii_struct_bases=[],
    name_mapping={"metric": "metric", "target": "target"},
)
class HorizontalPodAutoscalerV2SpecMetricExternal:
    def __init__(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerV2SpecMetricExternalMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricExternalTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerV2SpecMetricExternalMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2SpecMetricExternalTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5430af7d5441640dd380c519ad9d877c3ce078b66ccc6fd39e342fb233edacc)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerV2SpecMetricExternalMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricExternalMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricExternalTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricExternalTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricExternal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerV2SpecMetricExternalMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1915398b2ab5666cff3906b612c36a063dd73b0b062b7cfcac48cd91a138bf8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricExternalMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricExternalMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6d0b4750d6b92b331e1d4747c6d3567ec670bb367a2e5f774eced8744f9ead4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3c88d8e1803fad7df82bd93987de449a8628d6854fd54f630b736e9aa741b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(
        self,
    ) -> "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb13abb2bbf91de9cbed618d978e2a3f81c0677d890f174e5cd4c89343dc9689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52776e601a141365d799a41fb69ea51f88ef1e60a0a2347e700632d85c2a6164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_expressions HorizontalPodAutoscalerV2#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_labels HorizontalPodAutoscalerV2#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49bcb887ca2b04255627b4cc0e549db96e876a32d5f14d60e411cd9abf615ae)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_expressions HorizontalPodAutoscalerV2#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_labels HorizontalPodAutoscalerV2#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b63af2401ebcf114fee5d708d752c3d2c8054cc24ddcf7537d2f0e9d4fc4c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693da123493c04a50d17e9a9dfec7b30269a9a67d715b6f818e479d5fa69456c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3355a951e6f1c31621f51b05ece8fcb49c7bd1632e37a8b3f69a6c28cacb23d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21d82729db1bf6c74d72bf2f51333b7fe6ce12c3545c6acb0be3ee0a3dfd1c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17f116bffa91ac53771d91e93b47cf54c1d762001942e8139061f6ca8528a671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03c235fe91bd3d93e4f4dd7e11491f51baa9a8d9dce003ad66bb2eb926ec3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#key HorizontalPodAutoscalerV2#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#operator HorizontalPodAutoscalerV2#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#values HorizontalPodAutoscalerV2#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3528e48b34844426a1b0c5e14501d8d412dce7f5c9b485b88142f010894f841)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#key HorizontalPodAutoscalerV2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#operator HorizontalPodAutoscalerV2#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#values HorizontalPodAutoscalerV2#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0628a841d061c76f904fa0ef2280a47ad35ca5e29da8a1334f0b505ab1e422bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8863dcd0b075468bdd25f92f0f6ca942345b3846d2410c62c70448356ebbec3a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28cd6891ef346a6bd4c6fab24a1fd7bb2af5c97c5d4a6daf55f53e5ec99f55a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e418b3d6ff390c1289754784ec3b5966f6057eae81d6d690461643f2609bd90a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0469e96602ed4cca00d45df973c1c1849ce4a818612fd4eb684c7d97b6578fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1781435e300367891f85c9554f5041c06c723f9d108e7a56896163e2c4568bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__daaab170fccfec7ca35dd82a938f9a8146667adb9d6410ba8b923c27b6bca192)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7920be8300e592a212183abcbb95abbe21bcdd702f4e618eeeddda23a9e7dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7552966729cb4cacd102cb6f3342d6f5deb88405f038deca6951e25652c1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd5ecf0b1b7d1f94d3e815accf3ab858510223bfacc4bb090771b939398adee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac10bf19521b1f079786c130bcb3eb533420bc879ae3eabb3a515ac80c3651bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3972cce5a700682b51571dd1c246bf23b653a9e82e2f176daf85040839c8f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba60dd43a993cba35a60c60babb7d396a6b057c5808d01a8ee1001a2508574f)
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
    ) -> HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5f032b37be2b656f01b9afbc3d7c575785ed7c6a47cc570479c898d5dd701372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cef5f02cb50a175fdac01b2c2a8d9e6c75029f4bd9086897c04bc2a7c2c484d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricExternalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef0020ce3391cb04479e85ae62d566df29aee6cec867ad14ab2ed70b7b59e7fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricExternalMetric(
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        value_ = HorizontalPodAutoscalerV2SpecMetricExternalTarget(
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
    ) -> HorizontalPodAutoscalerV2SpecMetricExternalMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricExternalMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerV2SpecMetricExternalTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricExternalTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricExternalTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricExternalTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternal]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e04620fd1bf17606c4db9164708bc0189081d39a9ace4498ab9bbde976a099e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2SpecMetricExternalTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e486c6375dc8bb0e0c62c6c262c183500460d7564787b69ec899ebe3f58d2c14)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricExternalTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricExternalTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricExternalTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9718a0fbfc5230d94ce0ee19a16319dddb79d31e9de8640d6c9325bef156e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b04e44ed8145763759bb09f623223f509435ff7997f840ffd75d935a1c2bafed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7f214d4f57fc6356d4a7fa49ab6ece2afa8aab3a1af03abb1a00eda9b0f30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261489838fda38cfb6e7adc59e00b27a64301217609c45bc83f263a3b75ac765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7234af5d47e50c3db26626e1a687aee41665f32e50b2e3d917275f055d1f2790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed39a06952ea06a6e2e40de229b11995939c48033123ac3ad0da5308cc818038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed4df5d518532ba6b1119c492637ec10933e0bb5b16ab4b681bc04130589b654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d466cead42da16aa52e8a9efff979513124b6518e2aecdfa808b780d812cb039)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bcc66f78d05bc872700f881387e95c02856592bed2c1d27fd4684ab7cd8b4d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f5416bdef88eb8597407a5e9245aadf343618abe733aaa12bb9b3c07379b242)
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
            type_hints = typing.get_type_hints(_typecheckingstub__154bf85a64dede4c4ff8c2161df7f94e0a00ec8866ec94d26928e3f8340824fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c742b49224da0c4fb4ae7ea517d8b9733ac9f9e630949ec25b6d2b80ebdaaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObject",
    jsii_struct_bases=[],
    name_mapping={
        "described_object": "describedObject",
        "metric": "metric",
        "target": "target",
    },
)
class HorizontalPodAutoscalerV2SpecMetricObject:
    def __init__(
        self,
        *,
        described_object: typing.Union["HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject", typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union["HorizontalPodAutoscalerV2SpecMetricObjectMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricObjectTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param described_object: described_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#described_object HorizontalPodAutoscalerV2#described_object}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        if isinstance(described_object, dict):
            described_object = HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject(**described_object)
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerV2SpecMetricObjectMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2SpecMetricObjectTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290602cfc1c8fa2608f0896e0e86b75e64fc5d1c8739ffcc43db6d6f1ad7fdb3)
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
    ) -> "HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject":
        '''described_object block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#described_object HorizontalPodAutoscalerV2#described_object}
        '''
        result = self._values.get("described_object")
        assert result is not None, "Required property 'described_object' is missing"
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject", result)

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerV2SpecMetricObjectMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricObjectMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricObjectTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricObjectTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "kind": "kind", "name": "name"},
)
class HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#api_version HorizontalPodAutoscalerV2#api_version}
        :param kind: Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#kind HorizontalPodAutoscalerV2#kind}
        :param name: Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d073760a6c110cdc3ce23276e9c247aba0e4b0b3feb03b81cacd912c064c5330)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#api_version HorizontalPodAutoscalerV2#api_version}
        '''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#kind HorizontalPodAutoscalerV2#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricObjectDescribedObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectDescribedObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebb3645f22f4631ce4453f020fdfce12b82ca9b96493e59b25c4fb7fbf749799)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8aea386114b6a30f63fe282f476e942641dffad29a55feaf7ea987e17ce587a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3308b24f356ebab31720ccc41e327534078eece2c3f81d92e432917e5c3529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853954ee31186f8b7dcb27241f032e97c93ac1d2b1b0244da74e200cfab234f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6cbf56e1a09b95e7ad7728201b8e7ebd22c18fb37cf7fc0249861057a576be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerV2SpecMetricObjectMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2833d58cc9b3c4262918aabb5328e52b6b7274513ba343c59d35ec1f0d2cd2fd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricObjectMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricObjectMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b0df442ba7f03cceee2cebb9961ba376edca2b4d698d8f4f99245ab2c082032)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c028a135f32015ca9877da19623808843a2e170dd3c46e4caee9169a7013871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__254bd69627c93856231a92077d908d29474a133fe3a757414cee6557337b8b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba0a57c96301fd3cf82096deeed97fb23a4e20386adb9848225f279b9d6f1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_expressions HorizontalPodAutoscalerV2#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_labels HorizontalPodAutoscalerV2#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5edf623c1493e8b444bd08998b67ac921bba9d524d7ac65b88e484cd4bc9753)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_expressions HorizontalPodAutoscalerV2#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_labels HorizontalPodAutoscalerV2#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a8d5362f3fe282d877f381eeb640d303cfc6b78b0ea3de25bd09d447e965e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c091b41305ebedd385749e44435bb6b94bdbd5d400153a865498f2149b3858)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a8740988ed342f275c74f2da4cd988df50b6320b4c7d4e67c5dbd8834694d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aa51888b5b718655b62c238398dee941286883fda3853adf657a715e16625fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e1d354db4e93586bcf8cf9b366368964c98f6b10a60e3a9b90ab9946ef64c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb26a9ef58a5b9b782c08265a121ad098b9c26fba792437dd50e1a8e4757d0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#key HorizontalPodAutoscalerV2#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#operator HorizontalPodAutoscalerV2#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#values HorizontalPodAutoscalerV2#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f453a07f169600cac1d2d9344525bdb7dd97417ba21993f542f0cc17b46742e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#key HorizontalPodAutoscalerV2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#operator HorizontalPodAutoscalerV2#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#values HorizontalPodAutoscalerV2#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fb9c8adce2b7d16c6ddb9ff16eb76bb821316e6e9cee8a7b4a453f7ca5fb0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5c26d3ad591ab335886ebcfd26fbc9e5d1404ed336ff554bc277cf3f78137c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fd439dcca09b6caa7555d6917cda2b4112c5373e6634f2f8942bb43e94cb6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__348bb77c3201b899dae8dc3d99b45fb0fe40e6965cdadd1a1c9cf345de63b035)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b555daa3651ed61deaa366e5ff962a98f2d207ef3fd4e01c98af3aae9539184c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7ec4377b97e40cdc5b9c382ca652d6822b0063e023eaa3806c4e179099322b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__482eb0aa9444c5b33676fe2b3fc136769f2bcd9970c867192aa50892c8e733a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cee8fbba70aceef41e5c8f915b272986a9a03cfdc35b8f184278713717429597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b549b5900ba49818fdb43c57b8e15834b3ad25f7abbc33c355d91efc37b0b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ecdb2e87d2aa89a6e8c569fc0eb176e5afb0885660da33fca95d6632a0d63a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dd2fcd9108ff23983d94d0d56c5d8c88a9a078874b9a2c0a378b8648aa936e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f28a8887c65b7ecd6bdbf43a3725620113a7fbc8c0c448965c8006a2f1db2a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c755ad7e3bd875c786ae69b1ee34066a56671c02cf4a6060536d8e3573a589)
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
    ) -> HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f5aedebdce3ea67e33a34b91de61ccedd79f999a16f9e23df7ab082ad6bfdccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fdb67bd1d2a4cc0c473523e1b2e30927505b7b2dfc3e1ac1cdc7d079f233adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricObjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39979d4c356c05d7898eb862c71fc2deccf10cfd344cb27609a02d37b0dcf402)
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
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#api_version HorizontalPodAutoscalerV2#api_version}
        :param kind: Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#kind HorizontalPodAutoscalerV2#kind}
        :param name: Name of the referent; More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject(
            api_version=api_version, kind=kind, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putDescribedObject", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricObjectMetric(
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        value_ = HorizontalPodAutoscalerV2SpecMetricObjectTarget(
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
    ) -> HorizontalPodAutoscalerV2SpecMetricObjectDescribedObjectOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricObjectDescribedObjectOutputReference, jsii.get(self, "describedObject"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerV2SpecMetricObjectMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricObjectMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "HorizontalPodAutoscalerV2SpecMetricObjectTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricObjectTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="describedObjectInput")
    def described_object_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject], jsii.get(self, "describedObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricObjectTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricObjectTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5702369113a0607f26deab3aa5a15efa9113c70bc8192e099effe06cace34f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2SpecMetricObjectTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03a07fcef95f1169945c0045b41357f6da342ef3e046bf14aa278c928b6059b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricObjectTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricObjectTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricObjectTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56fca8fbee23a21aa6b474783b3eb873078d48e7f43023bbf554677fdcad0e33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b738c390cf6411a8ebd54956a2b41131d7f39171eb082da1bcacf8d430a2d099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78bac05dd829a3e2fb9ae4a788a93304885e2f99f6f8b9ed00b847fa8e3ed06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a584be3227f5fd3d7283788e9b9955441e3844564f364a6ccfe4aeefde9a3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f031620c25fcfb11254d27320d66a66134ad4cf225948a2c8445ef0961efc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2d4785f8a4cbbbb338bea8f47bff88dac5f6d2ce9d03e581c0aaca49fd5f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8f5fbbc318c5a7167620a5882575e253a7e72afe63c8c4e58bb1a01489affa)
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
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: name of the container in the pods of the scaling target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#container HorizontalPodAutoscalerV2#container}
        :param name: name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricContainerResource(
            container=container, name=name, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResource", [value]))

    @jsii.member(jsii_name="putExternal")
    def put_external(
        self,
        *,
        metric: typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetric, typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricExternal(
            metric=metric, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putExternal", [value]))

    @jsii.member(jsii_name="putObject")
    def put_object(
        self,
        *,
        described_object: typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject, typing.Dict[builtins.str, typing.Any]],
        metric: typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetric, typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param described_object: described_object block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#described_object HorizontalPodAutoscalerV2#described_object}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricObject(
            described_object=described_object, metric=metric, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putObject", [value]))

    @jsii.member(jsii_name="putPods")
    def put_pods(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricPods(metric=metric, target=target)

        return typing.cast(None, jsii.invoke(self, "putPods", [value]))

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        *,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricResource(name=name, target=target)

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
    ) -> HorizontalPodAutoscalerV2SpecMetricContainerResourceOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricContainerResourceOutputReference, jsii.get(self, "containerResource"))

    @builtins.property
    @jsii.member(jsii_name="external")
    def external(self) -> HorizontalPodAutoscalerV2SpecMetricExternalOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricExternalOutputReference, jsii.get(self, "external"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> HorizontalPodAutoscalerV2SpecMetricObjectOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricObjectOutputReference, jsii.get(self, "object"))

    @builtins.property
    @jsii.member(jsii_name="pods")
    def pods(self) -> "HorizontalPodAutoscalerV2SpecMetricPodsOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricPodsOutputReference", jsii.get(self, "pods"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "HorizontalPodAutoscalerV2SpecMetricResourceOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricResourceOutputReference", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="containerResourceInput")
    def container_resource_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResource], jsii.get(self, "containerResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="externalInput")
    def external_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternal]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternal], jsii.get(self, "externalInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricObject]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricObject], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="podsInput")
    def pods_input(self) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricPods"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricPods"], jsii.get(self, "podsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricResource"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricResource"], jsii.get(self, "resourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__57fed5eb4aeb9e12962041cae4733ff5e7471a45408258768d600a5608abd528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0d6de17e7c9be922301f6f9da5effab1e08a1666d18f77d83f04881bd918d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPods",
    jsii_struct_bases=[],
    name_mapping={"metric": "metric", "target": "target"},
)
class HorizontalPodAutoscalerV2SpecMetricPods:
    def __init__(
        self,
        *,
        metric: typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsMetric", typing.Dict[builtins.str, typing.Any]],
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        if isinstance(metric, dict):
            metric = HorizontalPodAutoscalerV2SpecMetricPodsMetric(**metric)
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2SpecMetricPodsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6097c199f8e113950dd31f2d5a4b081b002ac6c088370f72cd5f12113d5edacf)
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric": metric,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric(self) -> "HorizontalPodAutoscalerV2SpecMetricPodsMetric":
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#metric HorizontalPodAutoscalerV2#metric}
        '''
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricPodsMetric", result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricPodsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricPodsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricPods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetric",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "selector": "selector"},
)
class HorizontalPodAutoscalerV2SpecMetricPodsMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8aa03199a788dd1a60a4d9fbf07cefaee5d9b8ee8b6ced9136d5d61bbfeef51)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector"]]]:
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricPodsMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricPodsMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__433d9c11afa1d5a3b82735f1011df973da2f478a36358d726a7903fab2ed6ef0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00260b3fdd619c64317cf2bab304b42231c1cb95485cda6e40ab0d76d8c4e54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorList":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorList", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector"]]], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914bc1a0bf657d255999a4ca25b88e2f245d401325130f9e51acd8f66fcdb4b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe136cc9e2d76f5ae5d8a1c8dd8b97c5a3125b2e8c27e41a67c7bdb5376cb301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_expressions HorizontalPodAutoscalerV2#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_labels HorizontalPodAutoscalerV2#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1202b3b64152bec4e73a0676cc851a851017bff442c109a4b0158da8a7380c)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_expressions HorizontalPodAutoscalerV2#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#match_labels HorizontalPodAutoscalerV2#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52dd7eed894c2d6ea630fb37cda8bff5253283541562c83199d6261e0a8c7ba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef731f95d4432b293ca45ceaac5e0aa34ea560b00433f8f2f8a2a41f281aeae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0db14e8206a8865592592fda53a4348b18d223d5585fffc13b0876590c6e83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f190d80376bf0fc87e67f9057abd837f8b9b0d82bb3ebf8a557c3da32111e935)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a529ad9fc676815cf71a124257909d19903539565f368325e77ee85d148f7592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e5622d0be7db52ab8b1cb969df82f3e768702e01e10e36235096b9033eda6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#key HorizontalPodAutoscalerV2#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#operator HorizontalPodAutoscalerV2#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#values HorizontalPodAutoscalerV2#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a428edf8eeb7ea6e1b08b05140a9b37e1557d0faf6de6809c4b644b854e935d2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#key HorizontalPodAutoscalerV2#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#operator HorizontalPodAutoscalerV2#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#values HorizontalPodAutoscalerV2#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17d5a90fcadbb2490358ad4736864b5f442214f2dd62f5640603955f9b9f277)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c78d23e3750990162bc9330f6e4169bb2815291c742d0223312650431852f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb46d8f637420a76f780f9026525b38cf22bb71bd9906b634dbe185bc0bea1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f00506c3aa534c3e59993ebd538b44aace1ba672d64e5a02eeb7032e98f0d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f91460707fd1247f954d885734346dfb11e6bf87e60871f03aa3d8215fee269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e584958a71d1318771940f04a175db493614d972089684902cca1e400e2521d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7e7c5a41cb7cf7246fbe3563fdf23d6cbbd632c960b598f3730f1635ed65f76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d50990d892a89c171a0ca359448eea2a2953efe3521d0c65ff00823fab69ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c863e7e956b9c00128f56c123c519a33f1b491621502458f718c2be96cb52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d813708279bfb1477f08d24e63063dcf0fabd2f63e00f3b7c144c50f71349a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518c8835b76a76fa61728c059b8e056120543649e6fd7ecd1e1fbf8eef66d5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c1e66d8d828575d1b91ae23630e08afcd4d04d3841f15154adaebba48d086d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae5af4c782d4f86d192c0b9e5f0814c3c09998990e495e20055370631a2e716)
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
    ) -> HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsList:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ccaf594abca20680d7afc2fa2d5262eeff424ba80d491264dcde89a220167465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25765abf477c499449665d4820f56ab61af61897fae3b2c09a29157c93297c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecMetricPodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d624ee41da699f952686220e2640a074d18c97713fbbd54d8af96c3705a129)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        *,
        name: builtins.str,
        selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the given metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#selector HorizontalPodAutoscalerV2#selector}
        '''
        value = HorizontalPodAutoscalerV2SpecMetricPodsMetric(
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        value_ = HorizontalPodAutoscalerV2SpecMetricPodsTarget(
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
    def metric(self) -> HorizontalPodAutoscalerV2SpecMetricPodsMetricOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricPodsMetricOutputReference, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "HorizontalPodAutoscalerV2SpecMetricPodsTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricPodsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsMetric]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsMetric], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricPodsTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricPodsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricPods]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricPods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricPods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33839806760da0c434fdfbda75de417111e1ab25d442157b2c3cd578711a486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2SpecMetricPodsTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5759a09e09f833813c47b2c3b7847da84f9a800971859298a975c7177c8a973)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricPodsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricPodsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricPodsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad656eceb52bdf973a76e0fc7a743f98bb4ea0f49f15ec5b7c6378e4cdd9eff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af1f519c2e2bfc325a2e19211928b031d4ada5c67707b9cf651314545a8c7beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfb2ddadcd99e052df9d595c7fcfd8d8a87c598dad207ddc78e879b582273d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca549397a0d357a1ac043fd6da3216add3143b229fd2c9f23b380b8ecbd2fee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ffa4c216622a9ddeb7962095f4609689f650585ac9f58ad67d4e2ed3b3a277e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caccc53dd01ef679a3ef0f854bc72343e13f206816867e28d575c58f1546ccc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricResource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "target": "target"},
)
class HorizontalPodAutoscalerV2SpecMetricResource:
    def __init__(
        self,
        *,
        name: builtins.str,
        target: typing.Optional[typing.Union["HorizontalPodAutoscalerV2SpecMetricResourceTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: name is the name of the resource in question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        if isinstance(target, dict):
            target = HorizontalPodAutoscalerV2SpecMetricResourceTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f869b32940afbd5d23107e46e2ef45ca4beaebdf2da7849a699dcd9e06cd861)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricResourceTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#target HorizontalPodAutoscalerV2#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricResourceTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57837a6e6b44849218f65996caef1b124cf923fd781e7d116694e0c66fe803eb)
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
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        value_ = HorizontalPodAutoscalerV2SpecMetricResourceTarget(
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
    ) -> "HorizontalPodAutoscalerV2SpecMetricResourceTargetOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecMetricResourceTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecMetricResourceTarget"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecMetricResourceTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ad8a750fe64bf6225fdd167704e62d3916ce6868082214217dbb2386140577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricResource]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe09b6eb38848c4bc2a4173408a6d7b1586ea01b7c99438f53d70b6d507446d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricResourceTarget",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "average_utilization": "averageUtilization",
        "average_value": "averageValue",
        "value": "value",
    },
)
class HorizontalPodAutoscalerV2SpecMetricResourceTarget:
    def __init__(
        self,
        *,
        type: builtins.str,
        average_utilization: typing.Optional[jsii.Number] = None,
        average_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: type represents whether the metric type is Utilization, Value, or AverageValue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        :param average_utilization: averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        :param average_value: averageValue is the target value of the average of the metric across all relevant pods (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        :param value: value is the target value of the metric (as a quantity). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacb1b8e1ecf6325ef8b15910e6b848a5549de6c40df14c2981d3684c521ebde)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#type HorizontalPodAutoscalerV2#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def average_utilization(self) -> typing.Optional[jsii.Number]:
        '''averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

        Currently only valid for Resource metric source type

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_utilization HorizontalPodAutoscalerV2#average_utilization}
        '''
        result = self._values.get("average_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_value(self) -> typing.Optional[builtins.str]:
        '''averageValue is the target value of the average of the metric across all relevant pods (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#average_value HorizontalPodAutoscalerV2#average_value}
        '''
        result = self._values.get("average_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''value is the target value of the metric (as a quantity).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#value HorizontalPodAutoscalerV2#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecMetricResourceTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecMetricResourceTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecMetricResourceTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1fbe0c79a8e28aeb224051a53e81940ac1d3bdcf57572c25cce8cfd95f49e11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a6aeb4530da4da1e6451c22682b9076064c82dbe01791a247d0ab8ff75ca3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageValue")
    def average_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "averageValue"))

    @average_value.setter
    def average_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e179cff031e52958b103393f9a3803a31b97a7a074773b741b851d05b788315a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9f69fe411b75668fbcd34f4e7c862208c23ac50296ed58f94bd17a59ac5491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e45055ea2f85feecac1a9ca176d7dfc240fe3ce52fe48e88da13cf5d2ab269b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecMetricResourceTarget]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecMetricResourceTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricResourceTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f356d26db081fdacedb05a9fc4cfcaf27320118f37e5d5963706e4cd5ac57f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HorizontalPodAutoscalerV2SpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddcfc466e071db831caf6561aa0d1e7d43ce952fcc7afb46ba8f1cba8d37fd72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBehavior")
    def put_behavior(
        self,
        *,
        scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]]] = None,
        scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param scale_down: scale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_down HorizontalPodAutoscalerV2#scale_down}
        :param scale_up: scale_up block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#scale_up HorizontalPodAutoscalerV2#scale_up}
        '''
        value = HorizontalPodAutoscalerV2SpecBehavior(
            scale_down=scale_down, scale_up=scale_up
        )

        return typing.cast(None, jsii.invoke(self, "putBehavior", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac754726661e25693806e88a7d4af4ecf65a9cedfb6d708e9058d1aaf150ab9)
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
        :param kind: Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#kind HorizontalPodAutoscalerV2#kind}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#api_version HorizontalPodAutoscalerV2#api_version}
        '''
        value = HorizontalPodAutoscalerV2SpecScaleTargetRef(
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
    def behavior(self) -> HorizontalPodAutoscalerV2SpecBehaviorOutputReference:
        return typing.cast(HorizontalPodAutoscalerV2SpecBehaviorOutputReference, jsii.get(self, "behavior"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> HorizontalPodAutoscalerV2SpecMetricList:
        return typing.cast(HorizontalPodAutoscalerV2SpecMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleTargetRef")
    def scale_target_ref(
        self,
    ) -> "HorizontalPodAutoscalerV2SpecScaleTargetRefOutputReference":
        return typing.cast("HorizontalPodAutoscalerV2SpecScaleTargetRefOutputReference", jsii.get(self, "scaleTargetRef"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[HorizontalPodAutoscalerV2SpecBehavior]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecBehavior], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetric]]], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleTargetRefInput")
    def scale_target_ref_input(
        self,
    ) -> typing.Optional["HorizontalPodAutoscalerV2SpecScaleTargetRef"]:
        return typing.cast(typing.Optional["HorizontalPodAutoscalerV2SpecScaleTargetRef"], jsii.get(self, "scaleTargetRefInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d54e103281501771eb6e9e23bd6633475e67dd469b5072122698414facfc67ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd31f298b3f1f462e081a466c8ef50b6921356a19caf74ddfc49182f7a1d6a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCpuUtilizationPercentage")
    def target_cpu_utilization_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetCpuUtilizationPercentage"))

    @target_cpu_utilization_percentage.setter
    def target_cpu_utilization_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7480eebda6283f0dc15e44cce245ecdd0b1a56f7405eeb673fa9494ff3014dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCpuUtilizationPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HorizontalPodAutoscalerV2Spec]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2Spec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2Spec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22bf2c307cd0cf387cda838e364b2d0b4ef3a8536ad62fda1e2c65eca9c03ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecScaleTargetRef",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind", "name": "name", "api_version": "apiVersion"},
)
class HorizontalPodAutoscalerV2SpecScaleTargetRef:
    def __init__(
        self,
        *,
        kind: builtins.str,
        name: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: Kind of the referent. e.g. ``ReplicationController``. More info: http://releases.k8s.io/HEAD/docs/devel/api-conventions.md#types-kinds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#kind HorizontalPodAutoscalerV2#kind}
        :param name: Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        :param api_version: API version of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#api_version HorizontalPodAutoscalerV2#api_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd52e6ec8b2cc5f85d4b30e6c45eedee4c5f0730518965c93968b6fd13fce3eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#kind HorizontalPodAutoscalerV2#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#name HorizontalPodAutoscalerV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''API version of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs/resources/horizontal_pod_autoscaler_v2#api_version HorizontalPodAutoscalerV2#api_version}
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalPodAutoscalerV2SpecScaleTargetRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HorizontalPodAutoscalerV2SpecScaleTargetRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-kubernetes.horizontalPodAutoscalerV2.HorizontalPodAutoscalerV2SpecScaleTargetRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a596d87e44dcba473d2d5a3cf56a14ddad6951e0534cc91e7cc0490d567c9831)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e84ba27d64521364b7c63a1b93635bd85c6b7998c523e6337af9828044d2f09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed29e7336d039565be751d986d24e177d7583c832c9d50abed48363f820e12a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e153d50b46462df37958cec1642cb9bceccdfb28575245f9f10ec9660235536d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HorizontalPodAutoscalerV2SpecScaleTargetRef]:
        return typing.cast(typing.Optional[HorizontalPodAutoscalerV2SpecScaleTargetRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HorizontalPodAutoscalerV2SpecScaleTargetRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060784fbfe58b31611b30c4c1fa9d720bd0648c79e553639624ad021dbe8bf8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HorizontalPodAutoscalerV2",
    "HorizontalPodAutoscalerV2Config",
    "HorizontalPodAutoscalerV2Metadata",
    "HorizontalPodAutoscalerV2MetadataOutputReference",
    "HorizontalPodAutoscalerV2Spec",
    "HorizontalPodAutoscalerV2SpecBehavior",
    "HorizontalPodAutoscalerV2SpecBehaviorOutputReference",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleDown",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleDownList",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleDownOutputReference",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyList",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicyOutputReference",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleUp",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleUpList",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleUpOutputReference",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyList",
    "HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicyOutputReference",
    "HorizontalPodAutoscalerV2SpecMetric",
    "HorizontalPodAutoscalerV2SpecMetricContainerResource",
    "HorizontalPodAutoscalerV2SpecMetricContainerResourceOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget",
    "HorizontalPodAutoscalerV2SpecMetricContainerResourceTargetOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricExternal",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetric",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorList",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricExternalOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricExternalTarget",
    "HorizontalPodAutoscalerV2SpecMetricExternalTargetOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricList",
    "HorizontalPodAutoscalerV2SpecMetricObject",
    "HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject",
    "HorizontalPodAutoscalerV2SpecMetricObjectDescribedObjectOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetric",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorList",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricObjectOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricObjectTarget",
    "HorizontalPodAutoscalerV2SpecMetricObjectTargetOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricPods",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetric",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorList",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsList",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressionsOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricPodsOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricPodsTarget",
    "HorizontalPodAutoscalerV2SpecMetricPodsTargetOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricResource",
    "HorizontalPodAutoscalerV2SpecMetricResourceOutputReference",
    "HorizontalPodAutoscalerV2SpecMetricResourceTarget",
    "HorizontalPodAutoscalerV2SpecMetricResourceTargetOutputReference",
    "HorizontalPodAutoscalerV2SpecOutputReference",
    "HorizontalPodAutoscalerV2SpecScaleTargetRef",
    "HorizontalPodAutoscalerV2SpecScaleTargetRefOutputReference",
]

publication.publish()

def _typecheckingstub__ca48c85652b0edbd246a5dba3f8e43c5eb451c350c25afac190238bf0b33dec7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[HorizontalPodAutoscalerV2Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[HorizontalPodAutoscalerV2Spec, typing.Dict[builtins.str, typing.Any]],
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

def _typecheckingstub__6d42e70f1923c0a62f6650747298cfba09b949bacd462c06aa6127a66f48245c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370ca6cfba557891cc14f42e9a1d47864dfde1bfaf3aedfedc7e59a878fdcc10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0699a9669997722cf7347a1a85f3ccc6aa66e164b641808330c3a10ffcffff49(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[HorizontalPodAutoscalerV2Metadata, typing.Dict[builtins.str, typing.Any]],
    spec: typing.Union[HorizontalPodAutoscalerV2Spec, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e804b38c9b8d5046b9617012f73c7e2ff9d9e63136c95590ba87de6ecc9e3a9d(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    generate_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d4737b0229a6a7c43f84fc0e37a0eeb30df7bc22cfebc11a8a845c5d32ab3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5190936fb844d9dd1c240c34eb8344f437a43e458319a679381ba0998c6397a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12b9de274310b51a3ccf7bcd29964a3fddb7197e3bf88eea8f91fed69ed1b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666f9c4741dd18f718022e7ff0fe781e93888eeb9d0585a239896eeddc78cd57(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded1c66e28404a0689d6a71c561d181d59b52b706b3ef48ac3ef320f09a9814b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279122ed751921a193acfc81faefe2b11e19726c7409d063cc8bce5c3b51cf18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ffe169f416797db34aa63f592f994e40820fbfe48885eef8c141dba72387ac(
    value: typing.Optional[HorizontalPodAutoscalerV2Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53448432822054c7d1a8ac05527a3ac3536549a7cbd5422c21d08e220d2a4de9(
    *,
    max_replicas: jsii.Number,
    scale_target_ref: typing.Union[HorizontalPodAutoscalerV2SpecScaleTargetRef, typing.Dict[builtins.str, typing.Any]],
    behavior: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecBehavior, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    min_replicas: typing.Optional[jsii.Number] = None,
    target_cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9de99c691e74bb45630f65ea493f60a753936456e78484b7631adcb1e4cdaa7(
    *,
    scale_down: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scale_up: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8357c370f0fb7c5b0c500f4c11ebdaabf907c1cda640bacbd79a73769f8b7408(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d87466512b0e7bb5766492c7e4cb4cbc27ac123a8195e2f98b64ec004894354(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleDown, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417ea81779205076b930d85e05187b0c1e1503bd254f18cb3ca8a9d3c31a7e2a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleUp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363a714a9691c47bb7fb7e2fc7582d74f24a013c65ec911cf42a12d24af2ef1a(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecBehavior],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560a39252b6878a4cbc18ed8b688cba3a6d1a662456b92abd93e72f9d596940b(
    *,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy, typing.Dict[builtins.str, typing.Any]]]],
    select_policy: typing.Optional[builtins.str] = None,
    stabilization_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177708a2f7e2aa29fd69bac9cad8126ad01d7bafb19706a567167397011ff57d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c354cf2f418b3c9812d7924f652ee62e12d4965025410db6d20463f1c474b84a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17e4ca652926bc81d92ce615c015e10cbb5aec4ffac559e0da1b3d55ad2acf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fb23cdeff98b32e7027f5f3a82e10e5593d464bd5649c57475f6c0880d609a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933e66480256a4cbaf4c384865bcad389adf1356eed6c45e1899f83b19ab5a29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7be231b96136f1aaf8026c2871dcacb107db7cdc45ebcea4c00672f9e31adf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDown]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb496cdfe59598da2ac946519c26ee8a3ab319a794018239268df24f132e9d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5f2fc376c3f30e2f22a42709de0b273425143caa84be46aa8422ba717b87ad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95be4c2a8d542b6e5a70e70699f223303c4cd7a420fdcb78145ed040c5a82f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d8512d1cb186853bccf9b6b785f9a7a8432e2650c808146b438f4bdf38544d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b47dee7c7459dc421d58496b2c24a04a8cf659ba95eecc9c03fd565d0d8df7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDown]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac8f6c4a066d54a7ebb2022e182b1b8ffa2936b9278bd838dfb2fc8d8387a60(
    *,
    period_seconds: jsii.Number,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d1d31357f5251e5002410f8c0d0cfcd34671b76a4ac7c87d17455451f469d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd62f564657e908b1b8758cf698917d7dd52d3af426b72c790074880c5a2deb3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5097127f3a98415ef40313d08d7b8c4e865ecd02bed9dca4b6a73e327bc71c19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8cd9bf61f3e7c7a4cbb3b736f66ae81cf69e0cce9f8bf136065bbca2ac1998(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55f618b67befffac4fe200fbca6649028ec3b6346055f524c25870b21ffede1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57daa751d801d5a5943d243b7cfd0452a636268250abc29f4fe1191851a5a1f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8299a81dc0e6425f27dfe699a81006dbf14a156ca6c43d295160d73e66285e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafea09da2367d8efa8f9d9c79e43778ab976c899a118d007aff59bd8dd5210c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defba12509aeabb4b1b66b1d09f10eaf9c98fb4e79c92036199c6d29ac0cb34a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5ad568b70de9007c9afb89187261ba7d22f8382ac3566086ef4052fca76cbb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d801d648a698f5de70e125a892f4cd73f242a9744254c87c946a284a47e4b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleDownPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867ad4b041cb0f817c0292be78d980c433905abf5bb61ee31a9e335028685aee(
    *,
    policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy, typing.Dict[builtins.str, typing.Any]]]],
    select_policy: typing.Optional[builtins.str] = None,
    stabilization_window_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55be2cf60442696143a428b244217392a9ed31444cba1f778458495b7d6a49c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be52f0c7cfdf85de8a47fced85c60fa611e81e900b7e10663f1519dea2e99c9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d358afac2dc436c47a32df71b44192f004b6f8133b2b72df34416b777b5c8c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26a3f9e1802c31032204f338f6a6511a56855687f303a83bb995179198eaf5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f500d7c980b2b9eb5d0e8ce99b9b068a78c3798bf39183edf8c34ebe9788212b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e1b529052b712af8307938d398454a8e967e95344fc9367bbd0d87911d0261(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2418aee35471981e81288bebf85352b690f619615620b1f4f3b9e271f94b3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e805da76c4c54fc509e8ff4b6e26d0b835abfb6d3c0f07d15f373a6683622411(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53418a1d7a5d4f719d1f92571526000192d65929bb7d6455b723f036971e140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475c281696c121bdf4aac83e34f42e6ef427215d6bb14f0b43015319c2dd6583(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3182150bce6a8948a5012ed8ef3551a45904c60e82a5bdf0ef0567cdab417056(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2544109ff0b0e2bfce45b551a610391be43003a80d1cbb022a150b7f5b0200f(
    *,
    period_seconds: jsii.Number,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82018e7296d3587a8818e1ece0f54e370e269c17932e767dc9a4dcf842e10559(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a704fa8df2a43690b87d48fb77058ab3c9e8b6686b300e9c43372e3c346b53f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de57ab37d13b26157dbe037fb7f6575a5cd609560cc04ea81c9522e89ccab318(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d0ff0b9b6d522b732bab2713722b2b669b2b19804c85554b26bd4557dd975a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253598d85380e1f9319e8c444cd4008bc9c16eddf14fa87c9e3b0176b2aced7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1973ab8671f997efefc8976ffac8c765b3bf6897e3d721389db34aad85d3771(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40d489f6ac79e48a43004ee26184c6205f179e3c73d1c2823aceb254ed6c599(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52cbff36c304064a3d16577342f7c93b501f802fa4f083d7120b4469d9ef6b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5567fa75cb139d23215aa216d54665dd5f7d9cdfa8287a2a0a4df2b553ed6dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07750549581aed268c6c1c06152c47eaf90e319c6c36b170d2eacbf2c5690f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240b26db47c2dfe6b87fa4a44647a0b9fa4f10916e39d30767da79d22105c844(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecBehaviorScaleUpPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11541fce4ca0f4007735c91afa5ab6fdd143414298835dad8b1d971e2ac5c017(
    *,
    type: builtins.str,
    container_resource: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricContainerResource, typing.Dict[builtins.str, typing.Any]]] = None,
    external: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternal, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricObject, typing.Dict[builtins.str, typing.Any]]] = None,
    pods: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricPods, typing.Dict[builtins.str, typing.Any]]] = None,
    resource: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricResource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b279c073ebcf864b35712bccbebbddbc891fc7fa70029a92076061235c9f548(
    *,
    container: builtins.str,
    name: builtins.str,
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8d52b40b81983655dbec0c192dfde75e1b9ed655328eec723e725940c57900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28a8951456de4aa232c8b92513e49edf5bc43e182cf5d3bbb6131c9e68f9ff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cae113e83c08ad55cab33bda053328ce341dae5d631e6ab0b544e00178ffa26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b100fa8df1c88c81001fbcf7dfd5036bb141ab759487f223f1f1a8b727282fe0(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31403485a571ee5683e345ccdc6d657547f560e002841830664dd2ea13552a1b(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbddf33aa389cd132fc2556c9fd522f788e4d9fe3098f98df416d4d5669a4cd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904a46895dc76997d8c73754ef6f3ae01c321711b8bb7083f4e88c63bf1c45b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be80620ea575ada9d09ea4e8f91579fc00546b3ff07a8b2fecd1a373ecd2b890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c7254fe14ca5f02afab5590cb89cc2e12014a6d720ce9b2ff0ee36530399e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6b0d3148e82c211ac193f39c5f7d2d628585eaa6ec9a4e0a7b968ef20e1777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fd3f826d3d103db2dc1912f209e478e81ef7506ad0e8a6fb069ebd1076d2b1(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricContainerResourceTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5430af7d5441640dd380c519ad9d877c3ce078b66ccc6fd39e342fb233edacc(
    *,
    metric: typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1915398b2ab5666cff3906b612c36a063dd73b0b062b7cfcac48cd91a138bf8(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d0b4750d6b92b331e1d4747c6d3567ec670bb367a2e5f774eced8744f9ead4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3c88d8e1803fad7df82bd93987de449a8628d6854fd54f630b736e9aa741b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb13abb2bbf91de9cbed618d978e2a3f81c0677d890f174e5cd4c89343dc9689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52776e601a141365d799a41fb69ea51f88ef1e60a0a2347e700632d85c2a6164(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49bcb887ca2b04255627b4cc0e549db96e876a32d5f14d60e411cd9abf615ae(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b63af2401ebcf114fee5d708d752c3d2c8054cc24ddcf7537d2f0e9d4fc4c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693da123493c04a50d17e9a9dfec7b30269a9a67d715b6f818e479d5fa69456c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3355a951e6f1c31621f51b05ece8fcb49c7bd1632e37a8b3f69a6c28cacb23d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21d82729db1bf6c74d72bf2f51333b7fe6ce12c3545c6acb0be3ee0a3dfd1c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f116bffa91ac53771d91e93b47cf54c1d762001942e8139061f6ca8528a671(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03c235fe91bd3d93e4f4dd7e11491f51baa9a8d9dce003ad66bb2eb926ec3a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3528e48b34844426a1b0c5e14501d8d412dce7f5c9b485b88142f010894f841(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0628a841d061c76f904fa0ef2280a47ad35ca5e29da8a1334f0b505ab1e422bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8863dcd0b075468bdd25f92f0f6ca942345b3846d2410c62c70448356ebbec3a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28cd6891ef346a6bd4c6fab24a1fd7bb2af5c97c5d4a6daf55f53e5ec99f55a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e418b3d6ff390c1289754784ec3b5966f6057eae81d6d690461643f2609bd90a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0469e96602ed4cca00d45df973c1c1849ce4a818612fd4eb684c7d97b6578fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1781435e300367891f85c9554f5041c06c723f9d108e7a56896163e2c4568bbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daaab170fccfec7ca35dd82a938f9a8146667adb9d6410ba8b923c27b6bca192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7920be8300e592a212183abcbb95abbe21bcdd702f4e618eeeddda23a9e7dda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7552966729cb4cacd102cb6f3342d6f5deb88405f038deca6951e25652c1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd5ecf0b1b7d1f94d3e815accf3ab858510223bfacc4bb090771b939398adee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac10bf19521b1f079786c130bcb3eb533420bc879ae3eabb3a515ac80c3651bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3972cce5a700682b51571dd1c246bf23b653a9e82e2f176daf85040839c8f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba60dd43a993cba35a60c60babb7d396a6b057c5808d01a8ee1001a2508574f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricExternalMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f032b37be2b656f01b9afbc3d7c575785ed7c6a47cc570479c898d5dd701372(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cef5f02cb50a175fdac01b2c2a8d9e6c75029f4bd9086897c04bc2a7c2c484d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricExternalMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0020ce3391cb04479e85ae62d566df29aee6cec867ad14ab2ed70b7b59e7fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e04620fd1bf17606c4db9164708bc0189081d39a9ace4498ab9bbde976a099e(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e486c6375dc8bb0e0c62c6c262c183500460d7564787b69ec899ebe3f58d2c14(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9718a0fbfc5230d94ce0ee19a16319dddb79d31e9de8640d6c9325bef156e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04e44ed8145763759bb09f623223f509435ff7997f840ffd75d935a1c2bafed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7f214d4f57fc6356d4a7fa49ab6ece2afa8aab3a1af03abb1a00eda9b0f30e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261489838fda38cfb6e7adc59e00b27a64301217609c45bc83f263a3b75ac765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7234af5d47e50c3db26626e1a687aee41665f32e50b2e3d917275f055d1f2790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed39a06952ea06a6e2e40de229b11995939c48033123ac3ad0da5308cc818038(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricExternalTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4df5d518532ba6b1119c492637ec10933e0bb5b16ab4b681bc04130589b654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d466cead42da16aa52e8a9efff979513124b6518e2aecdfa808b780d812cb039(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcc66f78d05bc872700f881387e95c02856592bed2c1d27fd4684ab7cd8b4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5416bdef88eb8597407a5e9245aadf343618abe733aaa12bb9b3c07379b242(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154bf85a64dede4c4ff8c2161df7f94e0a00ec8866ec94d26928e3f8340824fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c742b49224da0c4fb4ae7ea517d8b9733ac9f9e630949ec25b6d2b80ebdaaa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290602cfc1c8fa2608f0896e0e86b75e64fc5d1c8739ffcc43db6d6f1ad7fdb3(
    *,
    described_object: typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject, typing.Dict[builtins.str, typing.Any]],
    metric: typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d073760a6c110cdc3ce23276e9c247aba0e4b0b3feb03b81cacd912c064c5330(
    *,
    api_version: builtins.str,
    kind: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb3645f22f4631ce4453f020fdfce12b82ca9b96493e59b25c4fb7fbf749799(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8aea386114b6a30f63fe282f476e942641dffad29a55feaf7ea987e17ce587a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3308b24f356ebab31720ccc41e327534078eece2c3f81d92e432917e5c3529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853954ee31186f8b7dcb27241f032e97c93ac1d2b1b0244da74e200cfab234f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6cbf56e1a09b95e7ad7728201b8e7ebd22c18fb37cf7fc0249861057a576be(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectDescribedObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2833d58cc9b3c4262918aabb5328e52b6b7274513ba343c59d35ec1f0d2cd2fd(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0df442ba7f03cceee2cebb9961ba376edca2b4d698d8f4f99245ab2c082032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c028a135f32015ca9877da19623808843a2e170dd3c46e4caee9169a7013871(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254bd69627c93856231a92077d908d29474a133fe3a757414cee6557337b8b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba0a57c96301fd3cf82096deeed97fb23a4e20386adb9848225f279b9d6f1b1(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5edf623c1493e8b444bd08998b67ac921bba9d524d7ac65b88e484cd4bc9753(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a8d5362f3fe282d877f381eeb640d303cfc6b78b0ea3de25bd09d447e965e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c091b41305ebedd385749e44435bb6b94bdbd5d400153a865498f2149b3858(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a8740988ed342f275c74f2da4cd988df50b6320b4c7d4e67c5dbd8834694d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa51888b5b718655b62c238398dee941286883fda3853adf657a715e16625fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e1d354db4e93586bcf8cf9b366368964c98f6b10a60e3a9b90ab9946ef64c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb26a9ef58a5b9b782c08265a121ad098b9c26fba792437dd50e1a8e4757d0e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f453a07f169600cac1d2d9344525bdb7dd97417ba21993f542f0cc17b46742e(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fb9c8adce2b7d16c6ddb9ff16eb76bb821316e6e9cee8a7b4a453f7ca5fb0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5c26d3ad591ab335886ebcfd26fbc9e5d1404ed336ff554bc277cf3f78137c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fd439dcca09b6caa7555d6917cda2b4112c5373e6634f2f8942bb43e94cb6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348bb77c3201b899dae8dc3d99b45fb0fe40e6965cdadd1a1c9cf345de63b035(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b555daa3651ed61deaa366e5ff962a98f2d207ef3fd4e01c98af3aae9539184c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7ec4377b97e40cdc5b9c382ca652d6822b0063e023eaa3806c4e179099322b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482eb0aa9444c5b33676fe2b3fc136769f2bcd9970c867192aa50892c8e733a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee8fbba70aceef41e5c8f915b272986a9a03cfdc35b8f184278713717429597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b549b5900ba49818fdb43c57b8e15834b3ad25f7abbc33c355d91efc37b0b16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ecdb2e87d2aa89a6e8c569fc0eb176e5afb0885660da33fca95d6632a0d63a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dd2fcd9108ff23983d94d0d56c5d8c88a9a078874b9a2c0a378b8648aa936e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f28a8887c65b7ecd6bdbf43a3725620113a7fbc8c0c448965c8006a2f1db2a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c755ad7e3bd875c786ae69b1ee34066a56671c02cf4a6060536d8e3573a589(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricObjectMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aedebdce3ea67e33a34b91de61ccedd79f999a16f9e23df7ab082ad6bfdccd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdb67bd1d2a4cc0c473523e1b2e30927505b7b2dfc3e1ac1cdc7d079f233adc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricObjectMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39979d4c356c05d7898eb862c71fc2deccf10cfd344cb27609a02d37b0dcf402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5702369113a0607f26deab3aa5a15efa9113c70bc8192e099effe06cace34f2(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03a07fcef95f1169945c0045b41357f6da342ef3e046bf14aa278c928b6059b(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fca8fbee23a21aa6b474783b3eb873078d48e7f43023bbf554677fdcad0e33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b738c390cf6411a8ebd54956a2b41131d7f39171eb082da1bcacf8d430a2d099(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78bac05dd829a3e2fb9ae4a788a93304885e2f99f6f8b9ed00b847fa8e3ed06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a584be3227f5fd3d7283788e9b9955441e3844564f364a6ccfe4aeefde9a3c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f031620c25fcfb11254d27320d66a66134ad4cf225948a2c8445ef0961efc34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2d4785f8a4cbbbb338bea8f47bff88dac5f6d2ce9d03e581c0aaca49fd5f6c(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricObjectTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8f5fbbc318c5a7167620a5882575e253a7e72afe63c8c4e58bb1a01489affa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fed5eb4aeb9e12962041cae4733ff5e7471a45408258768d600a5608abd528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0d6de17e7c9be922301f6f9da5effab1e08a1666d18f77d83f04881bd918d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6097c199f8e113950dd31f2d5a4b081b002ac6c088370f72cd5f12113d5edacf(
    *,
    metric: typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetric, typing.Dict[builtins.str, typing.Any]],
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8aa03199a788dd1a60a4d9fbf07cefaee5d9b8ee8b6ced9136d5d61bbfeef51(
    *,
    name: builtins.str,
    selector: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433d9c11afa1d5a3b82735f1011df973da2f478a36358d726a7903fab2ed6ef0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00260b3fdd619c64317cf2bab304b42231c1cb95485cda6e40ab0d76d8c4e54b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914bc1a0bf657d255999a4ca25b88e2f245d401325130f9e51acd8f66fcdb4b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe136cc9e2d76f5ae5d8a1c8dd8b97c5a3125b2e8c27e41a67c7bdb5376cb301(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1202b3b64152bec4e73a0676cc851a851017bff442c109a4b0158da8a7380c(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dd7eed894c2d6ea630fb37cda8bff5253283541562c83199d6261e0a8c7ba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef731f95d4432b293ca45ceaac5e0aa34ea560b00433f8f2f8a2a41f281aeae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0db14e8206a8865592592fda53a4348b18d223d5585fffc13b0876590c6e83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f190d80376bf0fc87e67f9057abd837f8b9b0d82bb3ebf8a557c3da32111e935(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a529ad9fc676815cf71a124257909d19903539565f368325e77ee85d148f7592(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e5622d0be7db52ab8b1cb969df82f3e768702e01e10e36235096b9033eda6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a428edf8eeb7ea6e1b08b05140a9b37e1557d0faf6de6809c4b644b854e935d2(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17d5a90fcadbb2490358ad4736864b5f442214f2dd62f5640603955f9b9f277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c78d23e3750990162bc9330f6e4169bb2815291c742d0223312650431852f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb46d8f637420a76f780f9026525b38cf22bb71bd9906b634dbe185bc0bea1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f00506c3aa534c3e59993ebd538b44aace1ba672d64e5a02eeb7032e98f0d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f91460707fd1247f954d885734346dfb11e6bf87e60871f03aa3d8215fee269(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e584958a71d1318771940f04a175db493614d972089684902cca1e400e2521d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e7c5a41cb7cf7246fbe3563fdf23d6cbbd632c960b598f3730f1635ed65f76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d50990d892a89c171a0ca359448eea2a2953efe3521d0c65ff00823fab69ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c863e7e956b9c00128f56c123c519a33f1b491621502458f718c2be96cb52e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d813708279bfb1477f08d24e63063dcf0fabd2f63e00f3b7c144c50f71349a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518c8835b76a76fa61728c059b8e056120543649e6fd7ecd1e1fbf8eef66d5e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1e66d8d828575d1b91ae23630e08afcd4d04d3841f15154adaebba48d086d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae5af4c782d4f86d192c0b9e5f0814c3c09998990e495e20055370631a2e716(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetricPodsMetricSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccaf594abca20680d7afc2fa2d5262eeff424ba80d491264dcde89a220167465(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25765abf477c499449665d4820f56ab61af61897fae3b2c09a29157c93297c99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HorizontalPodAutoscalerV2SpecMetricPodsMetricSelector]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d624ee41da699f952686220e2640a074d18c97713fbbd54d8af96c3705a129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33839806760da0c434fdfbda75de417111e1ab25d442157b2c3cd578711a486(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricPods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5759a09e09f833813c47b2c3b7847da84f9a800971859298a975c7177c8a973(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad656eceb52bdf973a76e0fc7a743f98bb4ea0f49f15ec5b7c6378e4cdd9eff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1f519c2e2bfc325a2e19211928b031d4ada5c67707b9cf651314545a8c7beb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfb2ddadcd99e052df9d595c7fcfd8d8a87c598dad207ddc78e879b582273d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca549397a0d357a1ac043fd6da3216add3143b229fd2c9f23b380b8ecbd2fee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffa4c216622a9ddeb7962095f4609689f650585ac9f58ad67d4e2ed3b3a277e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caccc53dd01ef679a3ef0f854bc72343e13f206816867e28d575c58f1546ccc0(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricPodsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f869b32940afbd5d23107e46e2ef45ca4beaebdf2da7849a699dcd9e06cd861(
    *,
    name: builtins.str,
    target: typing.Optional[typing.Union[HorizontalPodAutoscalerV2SpecMetricResourceTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57837a6e6b44849218f65996caef1b124cf923fd781e7d116694e0c66fe803eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ad8a750fe64bf6225fdd167704e62d3916ce6868082214217dbb2386140577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe09b6eb38848c4bc2a4173408a6d7b1586ea01b7c99438f53d70b6d507446d(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacb1b8e1ecf6325ef8b15910e6b848a5549de6c40df14c2981d3684c521ebde(
    *,
    type: builtins.str,
    average_utilization: typing.Optional[jsii.Number] = None,
    average_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fbe0c79a8e28aeb224051a53e81940ac1d3bdcf57572c25cce8cfd95f49e11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a6aeb4530da4da1e6451c22682b9076064c82dbe01791a247d0ab8ff75ca3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e179cff031e52958b103393f9a3803a31b97a7a074773b741b851d05b788315a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9f69fe411b75668fbcd34f4e7c862208c23ac50296ed58f94bd17a59ac5491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e45055ea2f85feecac1a9ca176d7dfc240fe3ce52fe48e88da13cf5d2ab269b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f356d26db081fdacedb05a9fc4cfcaf27320118f37e5d5963706e4cd5ac57f3(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecMetricResourceTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcfc466e071db831caf6561aa0d1e7d43ce952fcc7afb46ba8f1cba8d37fd72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac754726661e25693806e88a7d4af4ecf65a9cedfb6d708e9058d1aaf150ab9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HorizontalPodAutoscalerV2SpecMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54e103281501771eb6e9e23bd6633475e67dd469b5072122698414facfc67ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd31f298b3f1f462e081a466c8ef50b6921356a19caf74ddfc49182f7a1d6a10(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7480eebda6283f0dc15e44cce245ecdd0b1a56f7405eeb673fa9494ff3014dca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bf2c307cd0cf387cda838e364b2d0b4ef3a8536ad62fda1e2c65eca9c03ac9(
    value: typing.Optional[HorizontalPodAutoscalerV2Spec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd52e6ec8b2cc5f85d4b30e6c45eedee4c5f0730518965c93968b6fd13fce3eb(
    *,
    kind: builtins.str,
    name: builtins.str,
    api_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a596d87e44dcba473d2d5a3cf56a14ddad6951e0534cc91e7cc0490d567c9831(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84ba27d64521364b7c63a1b93635bd85c6b7998c523e6337af9828044d2f09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed29e7336d039565be751d986d24e177d7583c832c9d50abed48363f820e12a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e153d50b46462df37958cec1642cb9bceccdfb28575245f9f10ec9660235536d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060784fbfe58b31611b30c4c1fa9d720bd0648c79e553639624ad021dbe8bf8c(
    value: typing.Optional[HorizontalPodAutoscalerV2SpecScaleTargetRef],
) -> None:
    """Type checking stubs"""
    pass
