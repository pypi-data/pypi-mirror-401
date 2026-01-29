r'''
# `aws_sagemaker_endpoint_configuration`

Refer to the Terraform Registry for docs: [`aws_sagemaker_endpoint_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration).
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


class SagemakerEndpointConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration aws_sagemaker_endpoint_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
        async_inference_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_capture_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariants", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration aws_sagemaker_endpoint_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param production_variants: production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#production_variants SagemakerEndpointConfiguration#production_variants}
        :param async_inference_config: async_inference_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#async_inference_config SagemakerEndpointConfiguration#async_inference_config}
        :param data_capture_config: data_capture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#data_capture_config SagemakerEndpointConfiguration#data_capture_config}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#execution_role_arn SagemakerEndpointConfiguration#execution_role_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#id SagemakerEndpointConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_arn SagemakerEndpointConfiguration#kms_key_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#name SagemakerEndpointConfiguration#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#name_prefix SagemakerEndpointConfiguration#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#region SagemakerEndpointConfiguration#region}
        :param shadow_production_variants: shadow_production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#shadow_production_variants SagemakerEndpointConfiguration#shadow_production_variants}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#tags SagemakerEndpointConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#tags_all SagemakerEndpointConfiguration#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e5f1a18bd7c0c29ecf34d89cccde8ab7a57b94165c3bf94a6cf4cda774a441)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerEndpointConfigurationConfig(
            production_variants=production_variants,
            async_inference_config=async_inference_config,
            data_capture_config=data_capture_config,
            execution_role_arn=execution_role_arn,
            id=id,
            kms_key_arn=kms_key_arn,
            name=name,
            name_prefix=name_prefix,
            region=region,
            shadow_production_variants=shadow_production_variants,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a SagemakerEndpointConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerEndpointConfiguration to import.
        :param import_from_id: The id of the existing SagemakerEndpointConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerEndpointConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__464701cdc7a286ecbd687d268469461c422e08bdfb5816a498e6de7f4160b6eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAsyncInferenceConfig")
    def put_async_inference_config(
        self,
        *,
        output_config: typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig", typing.Dict[builtins.str, typing.Any]],
        client_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#output_config SagemakerEndpointConfiguration#output_config}
        :param client_config: client_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#client_config SagemakerEndpointConfiguration#client_config}
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfig(
            output_config=output_config, client_config=client_config
        )

        return typing.cast(None, jsii.invoke(self, "putAsyncInferenceConfig", [value]))

    @jsii.member(jsii_name="putDataCaptureConfig")
    def put_data_capture_config(
        self,
        *,
        capture_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions", typing.Dict[builtins.str, typing.Any]]]],
        destination_s3_uri: builtins.str,
        initial_sampling_percentage: jsii.Number,
        capture_content_type_header: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_capture: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capture_options: capture_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_options SagemakerEndpointConfiguration#capture_options}
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param initial_sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_sampling_percentage SagemakerEndpointConfiguration#initial_sampling_percentage}.
        :param capture_content_type_header: capture_content_type_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_content_type_header SagemakerEndpointConfiguration#capture_content_type_header}
        :param enable_capture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_capture SagemakerEndpointConfiguration#enable_capture}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        value = SagemakerEndpointConfigurationDataCaptureConfig(
            capture_options=capture_options,
            destination_s3_uri=destination_s3_uri,
            initial_sampling_percentage=initial_sampling_percentage,
            capture_content_type_header=capture_content_type_header,
            enable_capture=enable_capture,
            kms_key_id=kms_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDataCaptureConfig", [value]))

    @jsii.member(jsii_name="putProductionVariants")
    def put_production_variants(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d409101870b9d31406ede9dc0d6d59f9fa4fa12e707d09c13ef211f945024fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProductionVariants", [value]))

    @jsii.member(jsii_name="putShadowProductionVariants")
    def put_shadow_production_variants(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ad8c41d683eac2118b6f93e1146c75ed82a1ac769d7fc2f1b18c7a05262a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putShadowProductionVariants", [value]))

    @jsii.member(jsii_name="resetAsyncInferenceConfig")
    def reset_async_inference_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsyncInferenceConfig", []))

    @jsii.member(jsii_name="resetDataCaptureConfig")
    def reset_data_capture_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCaptureConfig", []))

    @jsii.member(jsii_name="resetExecutionRoleArn")
    def reset_execution_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRoleArn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetShadowProductionVariants")
    def reset_shadow_production_variants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShadowProductionVariants", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="asyncInferenceConfig")
    def async_inference_config(
        self,
    ) -> "SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference", jsii.get(self, "asyncInferenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCaptureConfig")
    def data_capture_config(
        self,
    ) -> "SagemakerEndpointConfigurationDataCaptureConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationDataCaptureConfigOutputReference", jsii.get(self, "dataCaptureConfig"))

    @builtins.property
    @jsii.member(jsii_name="productionVariants")
    def production_variants(
        self,
    ) -> "SagemakerEndpointConfigurationProductionVariantsList":
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsList", jsii.get(self, "productionVariants"))

    @builtins.property
    @jsii.member(jsii_name="shadowProductionVariants")
    def shadow_production_variants(
        self,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsList":
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsList", jsii.get(self, "shadowProductionVariants"))

    @builtins.property
    @jsii.member(jsii_name="asyncInferenceConfigInput")
    def async_inference_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfig"], jsii.get(self, "asyncInferenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCaptureConfigInput")
    def data_capture_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"], jsii.get(self, "dataCaptureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="productionVariantsInput")
    def production_variants_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]]], jsii.get(self, "productionVariantsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="shadowProductionVariantsInput")
    def shadow_production_variants_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]], jsii.get(self, "shadowProductionVariantsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a66b750588497abf9d325572da1ecd53644fd0f545f0dc801e99939c71c33fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d120bee8f83b8fbca8ef51895358a729be21a4824ceb2d98a492a740cbc2b99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8aa6466bb10be647b2730e8fce3fa487fd02079e545f82232bb7d5d98d0d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7396942e891b2657f9a55f4c82f5ebff34fdd4909d71386aeb2688f9d6f2d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df4ef5bafbaa31230a376a4922797f2bd90e58fcd42864c5f7f1099c3707b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cddca4b19997db895dad581ef1c3e1c97c8582d4e39fc18329e8cb5cbf2c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315c3bc76a30e84e6e830a37bfdd35e70636dff5effc51146d85a89036653022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5f704b1492cb96913ec2ddcbb37b44a0c3f243fde4360e0c579774e034c8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfig",
    jsii_struct_bases=[],
    name_mapping={"output_config": "outputConfig", "client_config": "clientConfig"},
)
class SagemakerEndpointConfigurationAsyncInferenceConfig:
    def __init__(
        self,
        *,
        output_config: typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig", typing.Dict[builtins.str, typing.Any]],
        client_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#output_config SagemakerEndpointConfiguration#output_config}
        :param client_config: client_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#client_config SagemakerEndpointConfiguration#client_config}
        '''
        if isinstance(output_config, dict):
            output_config = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig(**output_config)
        if isinstance(client_config, dict):
            client_config = SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig(**client_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720cd2c81794152bb8ec89bec87838f4b3b4bb87c68f4005dd24bdd82b5a464d)
            check_type(argname="argument output_config", value=output_config, expected_type=type_hints["output_config"])
            check_type(argname="argument client_config", value=client_config, expected_type=type_hints["client_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_config": output_config,
        }
        if client_config is not None:
            self._values["client_config"] = client_config

    @builtins.property
    def output_config(
        self,
    ) -> "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig":
        '''output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#output_config SagemakerEndpointConfiguration#output_config}
        '''
        result = self._values.get("output_config")
        assert result is not None, "Required property 'output_config' is missing"
        return typing.cast("SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig", result)

    @builtins.property
    def client_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig"]:
        '''client_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#client_config SagemakerEndpointConfiguration#client_config}
        '''
        result = self._values.get("client_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_invocations_per_instance": "maxConcurrentInvocationsPerInstance",
    },
)
class SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig:
    def __init__(
        self,
        *,
        max_concurrent_invocations_per_instance: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_invocations_per_instance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrent_invocations_per_instance SagemakerEndpointConfiguration#max_concurrent_invocations_per_instance}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055b16bb51bf6667751ec62b721c53bcf5fd2d31e6da447bb8e41fd830d9b30f)
            check_type(argname="argument max_concurrent_invocations_per_instance", value=max_concurrent_invocations_per_instance, expected_type=type_hints["max_concurrent_invocations_per_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_invocations_per_instance is not None:
            self._values["max_concurrent_invocations_per_instance"] = max_concurrent_invocations_per_instance

    @builtins.property
    def max_concurrent_invocations_per_instance(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrent_invocations_per_instance SagemakerEndpointConfiguration#max_concurrent_invocations_per_instance}.'''
        result = self._values.get("max_concurrent_invocations_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe9b6d7c0ba0789bd3e1235a72d7861725a41a5fdf6cbc763b2698a74614e969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentInvocationsPerInstance")
    def reset_max_concurrent_invocations_per_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentInvocationsPerInstance", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentInvocationsPerInstanceInput")
    def max_concurrent_invocations_per_instance_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentInvocationsPerInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentInvocationsPerInstance")
    def max_concurrent_invocations_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentInvocationsPerInstance"))

    @max_concurrent_invocations_per_instance.setter
    def max_concurrent_invocations_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a85d532369b24385a89be01b58e16eac098904757eee0f2b11a208949dda21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentInvocationsPerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bceb2e9365e0056ece57fb99c86ac88f2c3e3e0159831d44c8616938c747bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_output_path": "s3OutputPath",
        "kms_key_id": "kmsKeyId",
        "notification_config": "notificationConfig",
        "s3_failure_path": "s3FailurePath",
    },
)
class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig:
    def __init__(
        self,
        *,
        s3_output_path: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_failure_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_output_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#s3_output_path SagemakerEndpointConfiguration#s3_output_path}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#notification_config SagemakerEndpointConfiguration#notification_config}
        :param s3_failure_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#s3_failure_path SagemakerEndpointConfiguration#s3_failure_path}.
        '''
        if isinstance(notification_config, dict):
            notification_config = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig(**notification_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c69351dec282aa75236cf3aa7f5760cedf6b8aa5d3816d07ae7654aac1d9c0)
            check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument s3_failure_path", value=s3_failure_path, expected_type=type_hints["s3_failure_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_output_path": s3_output_path,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if s3_failure_path is not None:
            self._values["s3_failure_path"] = s3_failure_path

    @builtins.property
    def s3_output_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#s3_output_path SagemakerEndpointConfiguration#s3_output_path}.'''
        result = self._values.get("s3_output_path")
        assert result is not None, "Required property 's3_output_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#notification_config SagemakerEndpointConfiguration#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig"], result)

    @builtins.property
    def s3_failure_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#s3_failure_path SagemakerEndpointConfiguration#s3_failure_path}.'''
        result = self._values.get("s3_failure_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "error_topic": "errorTopic",
        "include_inference_response_in": "includeInferenceResponseIn",
        "success_topic": "successTopic",
    },
)
class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig:
    def __init__(
        self,
        *,
        error_topic: typing.Optional[builtins.str] = None,
        include_inference_response_in: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#error_topic SagemakerEndpointConfiguration#error_topic}.
        :param include_inference_response_in: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#include_inference_response_in SagemakerEndpointConfiguration#include_inference_response_in}.
        :param success_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#success_topic SagemakerEndpointConfiguration#success_topic}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144fdc270689803e343b736cb73c47135067bea2447ba4e7671b89607f38d772)
            check_type(argname="argument error_topic", value=error_topic, expected_type=type_hints["error_topic"])
            check_type(argname="argument include_inference_response_in", value=include_inference_response_in, expected_type=type_hints["include_inference_response_in"])
            check_type(argname="argument success_topic", value=success_topic, expected_type=type_hints["success_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if error_topic is not None:
            self._values["error_topic"] = error_topic
        if include_inference_response_in is not None:
            self._values["include_inference_response_in"] = include_inference_response_in
        if success_topic is not None:
            self._values["success_topic"] = success_topic

    @builtins.property
    def error_topic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#error_topic SagemakerEndpointConfiguration#error_topic}.'''
        result = self._values.get("error_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_inference_response_in(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#include_inference_response_in SagemakerEndpointConfiguration#include_inference_response_in}.'''
        result = self._values.get("include_inference_response_in")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def success_topic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#success_topic SagemakerEndpointConfiguration#success_topic}.'''
        result = self._values.get("success_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7528e08be06e87ede2a94024937c09c2a35e45fe2a3dfdbc089a90845e3d8d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetErrorTopic")
    def reset_error_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorTopic", []))

    @jsii.member(jsii_name="resetIncludeInferenceResponseIn")
    def reset_include_inference_response_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeInferenceResponseIn", []))

    @jsii.member(jsii_name="resetSuccessTopic")
    def reset_success_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessTopic", []))

    @builtins.property
    @jsii.member(jsii_name="errorTopicInput")
    def error_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInferenceResponseInInput")
    def include_inference_response_in_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeInferenceResponseInInput"))

    @builtins.property
    @jsii.member(jsii_name="successTopicInput")
    def success_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="errorTopic")
    def error_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorTopic"))

    @error_topic.setter
    def error_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3d6b8761b5d38119643ccd51fe79ba0ca5d66e4597d38c0789c60ebd3acd6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeInferenceResponseIn")
    def include_inference_response_in(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeInferenceResponseIn"))

    @include_inference_response_in.setter
    def include_inference_response_in(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaf5763df01aa0a63ed823287064afbbad5e5f82e2c24b7e091ef75c764031e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeInferenceResponseIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successTopic")
    def success_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successTopic"))

    @success_topic.setter
    def success_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56db7a84bc599e9d5e81a6a4bdf2217fcf8a904951ba648275bff40fabaea38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e56a8753bb99ae372727dcce9be66cf8a0c71eb2b78f9b32909fa9ca468dd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fc671aef5f1cbccea7e14939d2590fa3bca1694c999b3aa2ea23f81a3e72a99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        error_topic: typing.Optional[builtins.str] = None,
        include_inference_response_in: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#error_topic SagemakerEndpointConfiguration#error_topic}.
        :param include_inference_response_in: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#include_inference_response_in SagemakerEndpointConfiguration#include_inference_response_in}.
        :param success_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#success_topic SagemakerEndpointConfiguration#success_topic}.
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig(
            error_topic=error_topic,
            include_inference_response_in=include_inference_response_in,
            success_topic=success_topic,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetS3FailurePath")
    def reset_s3_failure_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3FailurePath", []))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference, jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="s3FailurePathInput")
    def s3_failure_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3FailurePathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputPathInput")
    def s3_output_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3OutputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5155a7dd407017dce0997f5bebf842cb84df61f427d6003c7baa96c7c2eb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3FailurePath")
    def s3_failure_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3FailurePath"))

    @s3_failure_path.setter
    def s3_failure_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544081bc84ad7c62ccebc8ebf08214c1d0f23067f67f23ac9521184d493b5b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3FailurePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3OutputPath")
    def s3_output_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3OutputPath"))

    @s3_output_path.setter
    def s3_output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158d22d7e336846e647abbe681bce05b7ccc54e9b9555d53681e7755029c2063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3OutputPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225486491489eb57d34f2c544b77a3e53b54bfa1da8799277ba17c5ec5e0a5d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d890f6422fadd98d3a4fb42bc7b877488039fa0bc2ed7ae1d2956fea1feeac4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientConfig")
    def put_client_config(
        self,
        *,
        max_concurrent_invocations_per_instance: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_invocations_per_instance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrent_invocations_per_instance SagemakerEndpointConfiguration#max_concurrent_invocations_per_instance}.
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig(
            max_concurrent_invocations_per_instance=max_concurrent_invocations_per_instance,
        )

        return typing.cast(None, jsii.invoke(self, "putClientConfig", [value]))

    @jsii.member(jsii_name="putOutputConfig")
    def put_output_config(
        self,
        *,
        s3_output_path: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_failure_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_output_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#s3_output_path SagemakerEndpointConfiguration#s3_output_path}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#notification_config SagemakerEndpointConfiguration#notification_config}
        :param s3_failure_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#s3_failure_path SagemakerEndpointConfiguration#s3_failure_path}.
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig(
            s3_output_path=s3_output_path,
            kms_key_id=kms_key_id,
            notification_config=notification_config,
            s3_failure_path=s3_failure_path,
        )

        return typing.cast(None, jsii.invoke(self, "putOutputConfig", [value]))

    @jsii.member(jsii_name="resetClientConfig")
    def reset_client_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientConfig", []))

    @builtins.property
    @jsii.member(jsii_name="clientConfig")
    def client_config(
        self,
    ) -> SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference, jsii.get(self, "clientConfig"))

    @builtins.property
    @jsii.member(jsii_name="outputConfig")
    def output_config(
        self,
    ) -> SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference, jsii.get(self, "outputConfig"))

    @builtins.property
    @jsii.member(jsii_name="clientConfigInput")
    def client_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig], jsii.get(self, "clientConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputConfigInput")
    def output_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig], jsii.get(self, "outputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85ed5e6e0c9023a06f97b89275db10aff99491405163da655c832dd51d80588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "production_variants": "productionVariants",
        "async_inference_config": "asyncInferenceConfig",
        "data_capture_config": "dataCaptureConfig",
        "execution_role_arn": "executionRoleArn",
        "id": "id",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "name_prefix": "namePrefix",
        "region": "region",
        "shadow_production_variants": "shadowProductionVariants",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerEndpointConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
        async_inference_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        data_capture_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariants", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param production_variants: production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#production_variants SagemakerEndpointConfiguration#production_variants}
        :param async_inference_config: async_inference_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#async_inference_config SagemakerEndpointConfiguration#async_inference_config}
        :param data_capture_config: data_capture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#data_capture_config SagemakerEndpointConfiguration#data_capture_config}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#execution_role_arn SagemakerEndpointConfiguration#execution_role_arn}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#id SagemakerEndpointConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_arn SagemakerEndpointConfiguration#kms_key_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#name SagemakerEndpointConfiguration#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#name_prefix SagemakerEndpointConfiguration#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#region SagemakerEndpointConfiguration#region}
        :param shadow_production_variants: shadow_production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#shadow_production_variants SagemakerEndpointConfiguration#shadow_production_variants}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#tags SagemakerEndpointConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#tags_all SagemakerEndpointConfiguration#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(async_inference_config, dict):
            async_inference_config = SagemakerEndpointConfigurationAsyncInferenceConfig(**async_inference_config)
        if isinstance(data_capture_config, dict):
            data_capture_config = SagemakerEndpointConfigurationDataCaptureConfig(**data_capture_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f2d056d9d0139a7b51838573de4ca5eda8eba8f0d8b0e9df915e0996d47bda)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument production_variants", value=production_variants, expected_type=type_hints["production_variants"])
            check_type(argname="argument async_inference_config", value=async_inference_config, expected_type=type_hints["async_inference_config"])
            check_type(argname="argument data_capture_config", value=data_capture_config, expected_type=type_hints["data_capture_config"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument shadow_production_variants", value=shadow_production_variants, expected_type=type_hints["shadow_production_variants"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "production_variants": production_variants,
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
        if async_inference_config is not None:
            self._values["async_inference_config"] = async_inference_config
        if data_capture_config is not None:
            self._values["data_capture_config"] = data_capture_config
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if id is not None:
            self._values["id"] = id
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if region is not None:
            self._values["region"] = region
        if shadow_production_variants is not None:
            self._values["shadow_production_variants"] = shadow_production_variants
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def production_variants(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]]:
        '''production_variants block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#production_variants SagemakerEndpointConfiguration#production_variants}
        '''
        result = self._values.get("production_variants")
        assert result is not None, "Required property 'production_variants' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]], result)

    @builtins.property
    def async_inference_config(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig]:
        '''async_inference_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#async_inference_config SagemakerEndpointConfiguration#async_inference_config}
        '''
        result = self._values.get("async_inference_config")
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig], result)

    @builtins.property
    def data_capture_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"]:
        '''data_capture_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#data_capture_config SagemakerEndpointConfiguration#data_capture_config}
        '''
        result = self._values.get("data_capture_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#execution_role_arn SagemakerEndpointConfiguration#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#id SagemakerEndpointConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_arn SagemakerEndpointConfiguration#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#name SagemakerEndpointConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#name_prefix SagemakerEndpointConfiguration#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#region SagemakerEndpointConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shadow_production_variants(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]]:
        '''shadow_production_variants block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#shadow_production_variants SagemakerEndpointConfiguration#shadow_production_variants}
        '''
        result = self._values.get("shadow_production_variants")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#tags SagemakerEndpointConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#tags_all SagemakerEndpointConfiguration#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfig",
    jsii_struct_bases=[],
    name_mapping={
        "capture_options": "captureOptions",
        "destination_s3_uri": "destinationS3Uri",
        "initial_sampling_percentage": "initialSamplingPercentage",
        "capture_content_type_header": "captureContentTypeHeader",
        "enable_capture": "enableCapture",
        "kms_key_id": "kmsKeyId",
    },
)
class SagemakerEndpointConfigurationDataCaptureConfig:
    def __init__(
        self,
        *,
        capture_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions", typing.Dict[builtins.str, typing.Any]]]],
        destination_s3_uri: builtins.str,
        initial_sampling_percentage: jsii.Number,
        capture_content_type_header: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_capture: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capture_options: capture_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_options SagemakerEndpointConfiguration#capture_options}
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param initial_sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_sampling_percentage SagemakerEndpointConfiguration#initial_sampling_percentage}.
        :param capture_content_type_header: capture_content_type_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_content_type_header SagemakerEndpointConfiguration#capture_content_type_header}
        :param enable_capture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_capture SagemakerEndpointConfiguration#enable_capture}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        if isinstance(capture_content_type_header, dict):
            capture_content_type_header = SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader(**capture_content_type_header)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92dedb9aa102563a1b1cd2472fd6b7ea28f687e80241ef95ada5d8b0531c09b3)
            check_type(argname="argument capture_options", value=capture_options, expected_type=type_hints["capture_options"])
            check_type(argname="argument destination_s3_uri", value=destination_s3_uri, expected_type=type_hints["destination_s3_uri"])
            check_type(argname="argument initial_sampling_percentage", value=initial_sampling_percentage, expected_type=type_hints["initial_sampling_percentage"])
            check_type(argname="argument capture_content_type_header", value=capture_content_type_header, expected_type=type_hints["capture_content_type_header"])
            check_type(argname="argument enable_capture", value=enable_capture, expected_type=type_hints["enable_capture"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capture_options": capture_options,
            "destination_s3_uri": destination_s3_uri,
            "initial_sampling_percentage": initial_sampling_percentage,
        }
        if capture_content_type_header is not None:
            self._values["capture_content_type_header"] = capture_content_type_header
        if enable_capture is not None:
            self._values["enable_capture"] = enable_capture
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def capture_options(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions"]]:
        '''capture_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_options SagemakerEndpointConfiguration#capture_options}
        '''
        result = self._values.get("capture_options")
        assert result is not None, "Required property 'capture_options' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions"]], result)

    @builtins.property
    def destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.'''
        result = self._values.get("destination_s3_uri")
        assert result is not None, "Required property 'destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_sampling_percentage(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_sampling_percentage SagemakerEndpointConfiguration#initial_sampling_percentage}.'''
        result = self._values.get("initial_sampling_percentage")
        assert result is not None, "Required property 'initial_sampling_percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def capture_content_type_header(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader"]:
        '''capture_content_type_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_content_type_header SagemakerEndpointConfiguration#capture_content_type_header}
        '''
        result = self._values.get("capture_content_type_header")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader"], result)

    @builtins.property
    def enable_capture(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_capture SagemakerEndpointConfiguration#enable_capture}.'''
        result = self._values.get("enable_capture")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationDataCaptureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader",
    jsii_struct_bases=[],
    name_mapping={
        "csv_content_types": "csvContentTypes",
        "json_content_types": "jsonContentTypes",
    },
)
class SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader:
    def __init__(
        self,
        *,
        csv_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param csv_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#csv_content_types SagemakerEndpointConfiguration#csv_content_types}.
        :param json_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#json_content_types SagemakerEndpointConfiguration#json_content_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7b9888f82e885d87c9d95c1a0ad87b06826f2f5720a37f1c18fec5299f1350)
            check_type(argname="argument csv_content_types", value=csv_content_types, expected_type=type_hints["csv_content_types"])
            check_type(argname="argument json_content_types", value=json_content_types, expected_type=type_hints["json_content_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv_content_types is not None:
            self._values["csv_content_types"] = csv_content_types
        if json_content_types is not None:
            self._values["json_content_types"] = json_content_types

    @builtins.property
    def csv_content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#csv_content_types SagemakerEndpointConfiguration#csv_content_types}.'''
        result = self._values.get("csv_content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def json_content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#json_content_types SagemakerEndpointConfiguration#json_content_types}.'''
        result = self._values.get("json_content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cb40dbda232a5aac10457d89f42240c3021e97ae09b43abf57fac0b920035cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCsvContentTypes")
    def reset_csv_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvContentTypes", []))

    @jsii.member(jsii_name="resetJsonContentTypes")
    def reset_json_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonContentTypes", []))

    @builtins.property
    @jsii.member(jsii_name="csvContentTypesInput")
    def csv_content_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "csvContentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonContentTypesInput")
    def json_content_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jsonContentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="csvContentTypes")
    def csv_content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "csvContentTypes"))

    @csv_content_types.setter
    def csv_content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de38aaa9cf4aee4a71a8bc057986cbd6c8d1447bcae117e56f6612a24aa3b2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "csvContentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonContentTypes")
    def json_content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jsonContentTypes"))

    @json_content_types.setter
    def json_content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61df39393bccc725b4b252c64648c227281f5ff38a310c175c43f70bf449106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonContentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8fea878c05fc385ef96a168fdecb3755a2bd929898ec598f19a57cbb561160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions",
    jsii_struct_bases=[],
    name_mapping={"capture_mode": "captureMode"},
)
class SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions:
    def __init__(self, *, capture_mode: builtins.str) -> None:
        '''
        :param capture_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_mode SagemakerEndpointConfiguration#capture_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd935e1696a348d246d3f68a2010d9fc7db95ea0cfc4758d1ffd54b1d7a57d52)
            check_type(argname="argument capture_mode", value=capture_mode, expected_type=type_hints["capture_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capture_mode": capture_mode,
        }

    @builtins.property
    def capture_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#capture_mode SagemakerEndpointConfiguration#capture_mode}.'''
        result = self._values.get("capture_mode")
        assert result is not None, "Required property 'capture_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d427a4936465b576c53b573771a6be0eab2ae99f19366c802f78d643864befe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43616ba8639d2e277bc414f4420b5e36da0c2c4404febf41abe8a1cb1caba0df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b268bff5feb666ca64d1a9809fe42086e568772b4f142b08b7cb0ac51d7d54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5abe7d1c5a8c9a7c2d4b36cfe081d0beb5b8a19bcf8697c9723a3a2f09c6507f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3138dd45cbbf80b3a538b155666380a93a8a267b3ecf3b535134245554b60c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797d19f9846327bb146acaa9750814308e8462659b086c181fb4c712f86e9688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83f9b01c6e73d5bc7051d974d3fd20af5107007c09487a969d434f95b7ac536)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="captureModeInput")
    def capture_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "captureModeInput"))

    @builtins.property
    @jsii.member(jsii_name="captureMode")
    def capture_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "captureMode"))

    @capture_mode.setter
    def capture_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56cd89ccc460e6ea64650db27fea73235b3bd6d1db2886f209cce7e3cdb2c376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "captureMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3c2e6b2f5a37730df9cf84565f0c31e941591562a1de14cfb7ec5bc68562ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationDataCaptureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a71db61eed693a5c06de18efd0d793bdaac8d03953b17b968d225b222caaf80c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCaptureContentTypeHeader")
    def put_capture_content_type_header(
        self,
        *,
        csv_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param csv_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#csv_content_types SagemakerEndpointConfiguration#csv_content_types}.
        :param json_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#json_content_types SagemakerEndpointConfiguration#json_content_types}.
        '''
        value = SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader(
            csv_content_types=csv_content_types, json_content_types=json_content_types
        )

        return typing.cast(None, jsii.invoke(self, "putCaptureContentTypeHeader", [value]))

    @jsii.member(jsii_name="putCaptureOptions")
    def put_capture_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9b99a597bee466024cc3c03245d11d321534a4b4b9ac30407d6c10db7cd93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCaptureOptions", [value]))

    @jsii.member(jsii_name="resetCaptureContentTypeHeader")
    def reset_capture_content_type_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptureContentTypeHeader", []))

    @jsii.member(jsii_name="resetEnableCapture")
    def reset_enable_capture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableCapture", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="captureContentTypeHeader")
    def capture_content_type_header(
        self,
    ) -> SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference:
        return typing.cast(SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference, jsii.get(self, "captureContentTypeHeader"))

    @builtins.property
    @jsii.member(jsii_name="captureOptions")
    def capture_options(
        self,
    ) -> SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList:
        return typing.cast(SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList, jsii.get(self, "captureOptions"))

    @builtins.property
    @jsii.member(jsii_name="captureContentTypeHeaderInput")
    def capture_content_type_header_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader], jsii.get(self, "captureContentTypeHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="captureOptionsInput")
    def capture_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]], jsii.get(self, "captureOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3UriInput")
    def destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="enableCaptureInput")
    def enable_capture_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableCaptureInput"))

    @builtins.property
    @jsii.member(jsii_name="initialSamplingPercentageInput")
    def initial_sampling_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialSamplingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3Uri")
    def destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationS3Uri"))

    @destination_s3_uri.setter
    def destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b9f885e465f86f8a97ca89327f09920cffa905dab5fa47e11f5dc531f23935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableCapture")
    def enable_capture(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableCapture"))

    @enable_capture.setter
    def enable_capture(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc6e75af04525e092baff877d5d113d86f1970b2db00e053fb7960629c4e434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCapture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialSamplingPercentage")
    def initial_sampling_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialSamplingPercentage"))

    @initial_sampling_percentage.setter
    def initial_sampling_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1251aed1ad75b5edf037624b81088690666f5d9800b68eb7054d0c6606b149b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialSamplingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e179ce9e622535edfaff43bfee9186323e470bd7a814dcbfeba60ae2833e28ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe3ffeeb5c63d9b6649f1a7d5098735e4ca3482998b8e475b3f7ff8031a49dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariants",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_type": "acceleratorType",
        "container_startup_health_check_timeout_in_seconds": "containerStartupHealthCheckTimeoutInSeconds",
        "core_dump_config": "coreDumpConfig",
        "enable_ssm_access": "enableSsmAccess",
        "inference_ami_version": "inferenceAmiVersion",
        "initial_instance_count": "initialInstanceCount",
        "initial_variant_weight": "initialVariantWeight",
        "instance_type": "instanceType",
        "managed_instance_scaling": "managedInstanceScaling",
        "model_data_download_timeout_in_seconds": "modelDataDownloadTimeoutInSeconds",
        "model_name": "modelName",
        "routing_config": "routingConfig",
        "serverless_config": "serverlessConfig",
        "variant_name": "variantName",
        "volume_size_in_gb": "volumeSizeInGb",
    },
)
class SagemakerEndpointConfigurationProductionVariants:
    def __init__(
        self,
        *,
        accelerator_type: typing.Optional[builtins.str] = None,
        container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        core_dump_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inference_ami_version: typing.Optional[builtins.str] = None,
        initial_instance_count: typing.Optional[jsii.Number] = None,
        initial_variant_weight: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[builtins.str] = None,
        managed_instance_scaling: typing.Optional[typing.Union["SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        model_name: typing.Optional[builtins.str] = None,
        routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serverless_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationProductionVariantsServerlessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        variant_name: typing.Optional[builtins.str] = None,
        volume_size_in_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerator_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.
        :param container_startup_health_check_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.
        :param core_dump_config: core_dump_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        :param enable_ssm_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.
        :param inference_ami_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.
        :param initial_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.
        :param initial_variant_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.
        :param managed_instance_scaling: managed_instance_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        :param model_data_download_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.
        :param model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.
        :param routing_config: routing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        :param serverless_config: serverless_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        :param variant_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.
        '''
        if isinstance(core_dump_config, dict):
            core_dump_config = SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig(**core_dump_config)
        if isinstance(managed_instance_scaling, dict):
            managed_instance_scaling = SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling(**managed_instance_scaling)
        if isinstance(serverless_config, dict):
            serverless_config = SagemakerEndpointConfigurationProductionVariantsServerlessConfig(**serverless_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5219294cbac728ee0df2941f486085e0ca0d53a1481778c0ad8e69ae379863)
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument container_startup_health_check_timeout_in_seconds", value=container_startup_health_check_timeout_in_seconds, expected_type=type_hints["container_startup_health_check_timeout_in_seconds"])
            check_type(argname="argument core_dump_config", value=core_dump_config, expected_type=type_hints["core_dump_config"])
            check_type(argname="argument enable_ssm_access", value=enable_ssm_access, expected_type=type_hints["enable_ssm_access"])
            check_type(argname="argument inference_ami_version", value=inference_ami_version, expected_type=type_hints["inference_ami_version"])
            check_type(argname="argument initial_instance_count", value=initial_instance_count, expected_type=type_hints["initial_instance_count"])
            check_type(argname="argument initial_variant_weight", value=initial_variant_weight, expected_type=type_hints["initial_variant_weight"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument managed_instance_scaling", value=managed_instance_scaling, expected_type=type_hints["managed_instance_scaling"])
            check_type(argname="argument model_data_download_timeout_in_seconds", value=model_data_download_timeout_in_seconds, expected_type=type_hints["model_data_download_timeout_in_seconds"])
            check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
            check_type(argname="argument routing_config", value=routing_config, expected_type=type_hints["routing_config"])
            check_type(argname="argument serverless_config", value=serverless_config, expected_type=type_hints["serverless_config"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if container_startup_health_check_timeout_in_seconds is not None:
            self._values["container_startup_health_check_timeout_in_seconds"] = container_startup_health_check_timeout_in_seconds
        if core_dump_config is not None:
            self._values["core_dump_config"] = core_dump_config
        if enable_ssm_access is not None:
            self._values["enable_ssm_access"] = enable_ssm_access
        if inference_ami_version is not None:
            self._values["inference_ami_version"] = inference_ami_version
        if initial_instance_count is not None:
            self._values["initial_instance_count"] = initial_instance_count
        if initial_variant_weight is not None:
            self._values["initial_variant_weight"] = initial_variant_weight
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if managed_instance_scaling is not None:
            self._values["managed_instance_scaling"] = managed_instance_scaling
        if model_data_download_timeout_in_seconds is not None:
            self._values["model_data_download_timeout_in_seconds"] = model_data_download_timeout_in_seconds
        if model_name is not None:
            self._values["model_name"] = model_name
        if routing_config is not None:
            self._values["routing_config"] = routing_config
        if serverless_config is not None:
            self._values["serverless_config"] = serverless_config
        if variant_name is not None:
            self._values["variant_name"] = variant_name
        if volume_size_in_gb is not None:
            self._values["volume_size_in_gb"] = volume_size_in_gb

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.'''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_startup_health_check_timeout_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.'''
        result = self._values.get("container_startup_health_check_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_dump_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig"]:
        '''core_dump_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        '''
        result = self._values.get("core_dump_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig"], result)

    @builtins.property
    def enable_ssm_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.'''
        result = self._values.get("enable_ssm_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inference_ami_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.'''
        result = self._values.get("inference_ami_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.'''
        result = self._values.get("initial_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def initial_variant_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.'''
        result = self._values.get("initial_variant_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_instance_scaling(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling"]:
        '''managed_instance_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        '''
        result = self._values.get("managed_instance_scaling")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling"], result)

    @builtins.property
    def model_data_download_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.'''
        result = self._values.get("model_data_download_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def model_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.'''
        result = self._values.get("model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]]:
        '''routing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        '''
        result = self._values.get("routing_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]], result)

    @builtins.property
    def serverless_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"]:
        '''serverless_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        '''
        result = self._values.get("serverless_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"], result)

    @builtins.property
    def variant_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.'''
        result = self._values.get("variant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.'''
        result = self._values.get("volume_size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariants(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig",
    jsii_struct_bases=[],
    name_mapping={"destination_s3_uri": "destinationS3Uri", "kms_key_id": "kmsKeyId"},
)
class SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig:
    def __init__(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3af8f00ebf7650a141a5c5f6e775a267fdc5fbbeb73cc7cfbd5c772d0b93d7)
            check_type(argname="argument destination_s3_uri", value=destination_s3_uri, expected_type=type_hints["destination_s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_s3_uri": destination_s3_uri,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.'''
        result = self._values.get("destination_s3_uri")
        assert result is not None, "Required property 'destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5176586e5bbe669173f51e928e8d1961b38ccbeb2c2687794ff6a6f88af6dbc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="destinationS3UriInput")
    def destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3Uri")
    def destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationS3Uri"))

    @destination_s3_uri.setter
    def destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efb0a372e88fe9f15f43ae20869c95c668acafaabbc2fb13447c94f9a3f88fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1c4841448068b9e3f29bafd666174924561deb73a834b739038901bdc10999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925fe9d6f804fbb0abf10c039f746e71828026cad7f115bd1693a4439b22b816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationProductionVariantsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d3f55fb142593bd9f424e086857a03c07e70113c329d256629e7a9b60925c90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationProductionVariantsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fc1e4083f1c72d57ba574427170c451d7390634fc516a027e3c05ee2edf3f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c890c66453f63d69f1d4f2e9e63eea03becaaa4536576d7611802a72b398c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__742613823b57f36657ad9af2278ee7e747c047c20b4965ef4903cc436eb355c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22c733cc37c684ea0eefb8217bbdcad4a579909e552486200ad58fcd91bfffcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb9c9ad766b09d1e4669da07de79d7482d17378b2cf4dfdfb5d717dfb4cabcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
        "status": "status",
    },
)
class SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa619c69771e25d9133c2ccdbc4f0c8dea3fa5d688b2546a90986bd53402185b)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.'''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__146fe1cf8472622af11907aa9e66d585db59913cc694f8a87aac48353946f2ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0ab93b728a361ac5541554fac1ccf406677c230f211d3e50e91e650dae29b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fed8852467fe5e0004fb63938d09d447baf51a09045b7ef7a5bac170699a3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf3f1aaf7fec3bd9d61188aaacbc2f121c0b57316dc1276f9946d03928d6085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c3730a9905fe40905b98f2cf08087e3e0a5e7700928cde23db9993c0538ca13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationProductionVariantsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d2bd3ef99aee6bb5795ad5b534aa5a72c1151844d48a7d974a80b93e0e0abb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCoreDumpConfig")
    def put_core_dump_config(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        value = SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig(
            destination_s3_uri=destination_s3_uri, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putCoreDumpConfig", [value]))

    @jsii.member(jsii_name="putManagedInstanceScaling")
    def put_managed_instance_scaling(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        value = SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedInstanceScaling", [value]))

    @jsii.member(jsii_name="putRoutingConfig")
    def put_routing_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a307d23b6f87453bee4f4fcb88076ad183c569184a88c589c8648bcc730bbcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoutingConfig", [value]))

    @jsii.member(jsii_name="putServerlessConfig")
    def put_serverless_config(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        value = SagemakerEndpointConfigurationProductionVariantsServerlessConfig(
            max_concurrency=max_concurrency,
            memory_size_in_mb=memory_size_in_mb,
            provisioned_concurrency=provisioned_concurrency,
        )

        return typing.cast(None, jsii.invoke(self, "putServerlessConfig", [value]))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetContainerStartupHealthCheckTimeoutInSeconds")
    def reset_container_startup_health_check_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerStartupHealthCheckTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetCoreDumpConfig")
    def reset_core_dump_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDumpConfig", []))

    @jsii.member(jsii_name="resetEnableSsmAccess")
    def reset_enable_ssm_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSsmAccess", []))

    @jsii.member(jsii_name="resetInferenceAmiVersion")
    def reset_inference_ami_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceAmiVersion", []))

    @jsii.member(jsii_name="resetInitialInstanceCount")
    def reset_initial_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialInstanceCount", []))

    @jsii.member(jsii_name="resetInitialVariantWeight")
    def reset_initial_variant_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialVariantWeight", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetManagedInstanceScaling")
    def reset_managed_instance_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedInstanceScaling", []))

    @jsii.member(jsii_name="resetModelDataDownloadTimeoutInSeconds")
    def reset_model_data_download_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataDownloadTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetModelName")
    def reset_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelName", []))

    @jsii.member(jsii_name="resetRoutingConfig")
    def reset_routing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingConfig", []))

    @jsii.member(jsii_name="resetServerlessConfig")
    def reset_serverless_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessConfig", []))

    @jsii.member(jsii_name="resetVariantName")
    def reset_variant_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariantName", []))

    @jsii.member(jsii_name="resetVolumeSizeInGb")
    def reset_volume_size_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSizeInGb", []))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfig")
    def core_dump_config(
        self,
    ) -> SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference, jsii.get(self, "coreDumpConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScaling")
    def managed_instance_scaling(
        self,
    ) -> SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference:
        return typing.cast(SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference, jsii.get(self, "managedInstanceScaling"))

    @builtins.property
    @jsii.member(jsii_name="routingConfig")
    def routing_config(
        self,
    ) -> "SagemakerEndpointConfigurationProductionVariantsRoutingConfigList":
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsRoutingConfigList", jsii.get(self, "routingConfig"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfig")
    def serverless_config(
        self,
    ) -> "SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference", jsii.get(self, "serverlessConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSecondsInput")
    def container_startup_health_check_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerStartupHealthCheckTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfigInput")
    def core_dump_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig], jsii.get(self, "coreDumpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccessInput")
    def enable_ssm_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSsmAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersionInput")
    def inference_ami_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceAmiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCountInput")
    def initial_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeightInput")
    def initial_variant_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialVariantWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScalingInput")
    def managed_instance_scaling_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling], jsii.get(self, "managedInstanceScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSecondsInput")
    def model_data_download_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modelDataDownloadTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelNameInput")
    def model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingConfigInput")
    def routing_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]], jsii.get(self, "routingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfigInput")
    def serverless_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"], jsii.get(self, "serverlessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="variantNameInput")
    def variant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGbInput")
    def volume_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede185b947edc44ed61d061d99615bf5d4f7f6225c235372642b540f50743f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSeconds")
    def container_startup_health_check_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerStartupHealthCheckTimeoutInSeconds"))

    @container_startup_health_check_timeout_in_seconds.setter
    def container_startup_health_check_timeout_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0e16e5b6d8ae87b04ba1e5ad19e620c064b5d5b156096377443391b9415a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerStartupHealthCheckTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccess")
    def enable_ssm_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSsmAccess"))

    @enable_ssm_access.setter
    def enable_ssm_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c94454bba63f172d83ad36dbfd4c612ff58e654997f9853fc56b81e79a27d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSsmAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersion")
    def inference_ami_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inferenceAmiVersion"))

    @inference_ami_version.setter
    def inference_ami_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77233882865dcbf69592a26216384ebf09492b981e9b3af5604138bf7891192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceAmiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCount")
    def initial_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialInstanceCount"))

    @initial_instance_count.setter
    def initial_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4273209ea2c73d035988e894ecab380eec98919dbd5a2ecd9cd0a0bb34613c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeight")
    def initial_variant_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialVariantWeight"))

    @initial_variant_weight.setter
    def initial_variant_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d215cd825fd07194098750d375b84198b2a9c9c76c988d36a3055f532ba641d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVariantWeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcb34cc6d85fc3590aacfd4c991286c5d4414be8e653bd686801870f26e5447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSeconds")
    def model_data_download_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "modelDataDownloadTimeoutInSeconds"))

    @model_data_download_timeout_in_seconds.setter
    def model_data_download_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aced7a0ceab479a20de7c4cc46fa8304aadc384368d53a5efa9d741db9b598d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataDownloadTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelName"))

    @model_name.setter
    def model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d101a3ccafc702a9450f5c0e611fe575cae9500a8df1958d0acd90a91d481b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variantName")
    def variant_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variantName"))

    @variant_name.setter
    def variant_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249830508b0f16d71002195fc88cf66a917794a8744606db7078276ba111c886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variantName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInGb"))

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b65c41537e88bd6ceafb6df8b58e1dad612553462b9d739649c1c75bf96844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d29f1c08ce0bebe2fac1ec0f422df14ebbf860ad4fdbb817d55b3b1968b178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsRoutingConfig",
    jsii_struct_bases=[],
    name_mapping={"routing_strategy": "routingStrategy"},
)
class SagemakerEndpointConfigurationProductionVariantsRoutingConfig:
    def __init__(self, *, routing_strategy: builtins.str) -> None:
        '''
        :param routing_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e547c4010bcfc18721d69a903e770a0f7a68eabaccf481fa079eefa662dbdf25)
            check_type(argname="argument routing_strategy", value=routing_strategy, expected_type=type_hints["routing_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "routing_strategy": routing_strategy,
        }

    @builtins.property
    def routing_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.'''
        result = self._values.get("routing_strategy")
        assert result is not None, "Required property 'routing_strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsRoutingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsRoutingConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsRoutingConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b11f1eea3940e8ca2236fa7e7c27ddf7ceedcdb1043ff8238b69ddfcb245da21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7ea500d7022e4a90f0b43aea89ad80e49ad9a2de38c4a73187054f24de3fb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11ee1d4d82de73f47130614c45ab1f9869a60b4e6e61f6d4e2373967aaa7b86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a30e27a1f7f5df3004059913fd43a68a33ab1750ee03ab8f898498de084101e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef02cc78097b7d2b9c163dbbc57ef656c552d97f0afb1f349f0538b09222ee28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49df7a30d947d4a226e511ba88a3ce7626f34df944363a0eff476e33a2a9ef9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8871809d7ca6d8c8d2d0b5d6eb9cf6a6c8aaf4800ba26d2d31a57ba31a431a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="routingStrategyInput")
    def routing_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="routingStrategy")
    def routing_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingStrategy"))

    @routing_strategy.setter
    def routing_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12352f2c9a9d59708b90f680702c42a1bbc13b53be8de5675a9b49fbd142af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4665da96a21a824b271b75d3bf29328a8b0e54c24c2eed6be55f004b434afe1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsServerlessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrency": "maxConcurrency",
        "memory_size_in_mb": "memorySizeInMb",
        "provisioned_concurrency": "provisionedConcurrency",
    },
)
class SagemakerEndpointConfigurationProductionVariantsServerlessConfig:
    def __init__(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd84e4d34c20369186c7c6e196580617f7682c9e946c9ce5dc06d6f222979c45)
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument memory_size_in_mb", value=memory_size_in_mb, expected_type=type_hints["memory_size_in_mb"])
            check_type(argname="argument provisioned_concurrency", value=provisioned_concurrency, expected_type=type_hints["provisioned_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_concurrency": max_concurrency,
            "memory_size_in_mb": memory_size_in_mb,
        }
        if provisioned_concurrency is not None:
            self._values["provisioned_concurrency"] = provisioned_concurrency

    @builtins.property
    def max_concurrency(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.'''
        result = self._values.get("max_concurrency")
        assert result is not None, "Required property 'max_concurrency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_size_in_mb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.'''
        result = self._values.get("memory_size_in_mb")
        assert result is not None, "Required property 'memory_size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def provisioned_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.'''
        result = self._values.get("provisioned_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsServerlessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78176fec3f09b7225db74a7f19b7a3a55e8cdd46f46629f18f84210f744b45b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProvisionedConcurrency")
    def reset_provisioned_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyInput")
    def max_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMbInput")
    def memory_size_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyInput")
    def provisioned_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrency"))

    @max_concurrency.setter
    def max_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad8d2f61db88e4b5360cec7e865dfa353dfcf07f288bc1e5f9bdb1c8cb28296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMb")
    def memory_size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInMb"))

    @memory_size_in_mb.setter
    def memory_size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b71711632e1eb55bfcbf0e12749941f10e51358feb81f2fd40d288f5093de42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrency")
    def provisioned_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedConcurrency"))

    @provisioned_concurrency.setter
    def provisioned_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7246b5d4e1a83ca0e03bd0e2c9db7878a3cb041fded3b28159d9e4c39719c708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a94e76de15561ab01bf3ea2b7f490446ad3a1cbbb3baf760d75a221db1e62e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariants",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_type": "acceleratorType",
        "container_startup_health_check_timeout_in_seconds": "containerStartupHealthCheckTimeoutInSeconds",
        "core_dump_config": "coreDumpConfig",
        "enable_ssm_access": "enableSsmAccess",
        "inference_ami_version": "inferenceAmiVersion",
        "initial_instance_count": "initialInstanceCount",
        "initial_variant_weight": "initialVariantWeight",
        "instance_type": "instanceType",
        "managed_instance_scaling": "managedInstanceScaling",
        "model_data_download_timeout_in_seconds": "modelDataDownloadTimeoutInSeconds",
        "model_name": "modelName",
        "routing_config": "routingConfig",
        "serverless_config": "serverlessConfig",
        "variant_name": "variantName",
        "volume_size_in_gb": "volumeSizeInGb",
    },
)
class SagemakerEndpointConfigurationShadowProductionVariants:
    def __init__(
        self,
        *,
        accelerator_type: typing.Optional[builtins.str] = None,
        container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        core_dump_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inference_ami_version: typing.Optional[builtins.str] = None,
        initial_instance_count: typing.Optional[jsii.Number] = None,
        initial_variant_weight: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[builtins.str] = None,
        managed_instance_scaling: typing.Optional[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        model_name: typing.Optional[builtins.str] = None,
        routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serverless_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        variant_name: typing.Optional[builtins.str] = None,
        volume_size_in_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerator_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.
        :param container_startup_health_check_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.
        :param core_dump_config: core_dump_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        :param enable_ssm_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.
        :param inference_ami_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.
        :param initial_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.
        :param initial_variant_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.
        :param managed_instance_scaling: managed_instance_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        :param model_data_download_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.
        :param model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.
        :param routing_config: routing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        :param serverless_config: serverless_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        :param variant_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.
        '''
        if isinstance(core_dump_config, dict):
            core_dump_config = SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig(**core_dump_config)
        if isinstance(managed_instance_scaling, dict):
            managed_instance_scaling = SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling(**managed_instance_scaling)
        if isinstance(serverless_config, dict):
            serverless_config = SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig(**serverless_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c15d132289af4ea68aaea36c60a11060fd984c9e307d02a68bddeb3308ab2f5)
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument container_startup_health_check_timeout_in_seconds", value=container_startup_health_check_timeout_in_seconds, expected_type=type_hints["container_startup_health_check_timeout_in_seconds"])
            check_type(argname="argument core_dump_config", value=core_dump_config, expected_type=type_hints["core_dump_config"])
            check_type(argname="argument enable_ssm_access", value=enable_ssm_access, expected_type=type_hints["enable_ssm_access"])
            check_type(argname="argument inference_ami_version", value=inference_ami_version, expected_type=type_hints["inference_ami_version"])
            check_type(argname="argument initial_instance_count", value=initial_instance_count, expected_type=type_hints["initial_instance_count"])
            check_type(argname="argument initial_variant_weight", value=initial_variant_weight, expected_type=type_hints["initial_variant_weight"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument managed_instance_scaling", value=managed_instance_scaling, expected_type=type_hints["managed_instance_scaling"])
            check_type(argname="argument model_data_download_timeout_in_seconds", value=model_data_download_timeout_in_seconds, expected_type=type_hints["model_data_download_timeout_in_seconds"])
            check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
            check_type(argname="argument routing_config", value=routing_config, expected_type=type_hints["routing_config"])
            check_type(argname="argument serverless_config", value=serverless_config, expected_type=type_hints["serverless_config"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if container_startup_health_check_timeout_in_seconds is not None:
            self._values["container_startup_health_check_timeout_in_seconds"] = container_startup_health_check_timeout_in_seconds
        if core_dump_config is not None:
            self._values["core_dump_config"] = core_dump_config
        if enable_ssm_access is not None:
            self._values["enable_ssm_access"] = enable_ssm_access
        if inference_ami_version is not None:
            self._values["inference_ami_version"] = inference_ami_version
        if initial_instance_count is not None:
            self._values["initial_instance_count"] = initial_instance_count
        if initial_variant_weight is not None:
            self._values["initial_variant_weight"] = initial_variant_weight
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if managed_instance_scaling is not None:
            self._values["managed_instance_scaling"] = managed_instance_scaling
        if model_data_download_timeout_in_seconds is not None:
            self._values["model_data_download_timeout_in_seconds"] = model_data_download_timeout_in_seconds
        if model_name is not None:
            self._values["model_name"] = model_name
        if routing_config is not None:
            self._values["routing_config"] = routing_config
        if serverless_config is not None:
            self._values["serverless_config"] = serverless_config
        if variant_name is not None:
            self._values["variant_name"] = variant_name
        if volume_size_in_gb is not None:
            self._values["volume_size_in_gb"] = volume_size_in_gb

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.'''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_startup_health_check_timeout_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.'''
        result = self._values.get("container_startup_health_check_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_dump_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig"]:
        '''core_dump_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        '''
        result = self._values.get("core_dump_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig"], result)

    @builtins.property
    def enable_ssm_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.'''
        result = self._values.get("enable_ssm_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inference_ami_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.'''
        result = self._values.get("inference_ami_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.'''
        result = self._values.get("initial_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def initial_variant_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.'''
        result = self._values.get("initial_variant_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_instance_scaling(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling"]:
        '''managed_instance_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        '''
        result = self._values.get("managed_instance_scaling")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling"], result)

    @builtins.property
    def model_data_download_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.'''
        result = self._values.get("model_data_download_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def model_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.'''
        result = self._values.get("model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]]:
        '''routing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        '''
        result = self._values.get("routing_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]], result)

    @builtins.property
    def serverless_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"]:
        '''serverless_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        '''
        result = self._values.get("serverless_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"], result)

    @builtins.property
    def variant_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.'''
        result = self._values.get("variant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.'''
        result = self._values.get("volume_size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariants(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig",
    jsii_struct_bases=[],
    name_mapping={"destination_s3_uri": "destinationS3Uri", "kms_key_id": "kmsKeyId"},
)
class SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig:
    def __init__(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: builtins.str,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53d41ede059aa360e4e6f28d84852e5ad4577a3fdc0b22ff50879e0684e7a4f)
            check_type(argname="argument destination_s3_uri", value=destination_s3_uri, expected_type=type_hints["destination_s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_s3_uri": destination_s3_uri,
            "kms_key_id": kms_key_id,
        }

    @builtins.property
    def destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.'''
        result = self._values.get("destination_s3_uri")
        assert result is not None, "Required property 'destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        assert result is not None, "Required property 'kms_key_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08afde8dd7f9ebc5e2cdc8598bff96d1c1c1b2721fdff232c804aeef91fe69b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationS3UriInput")
    def destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3Uri")
    def destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationS3Uri"))

    @destination_s3_uri.setter
    def destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1965a0c1e5e19b39bc2c601c7903ae23bf618fb5fb3a07e3fea3d837d5c1a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e9b04712a2ae08458cca99ac91564769a1fb50e6ee6de0d442b65b8d818332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2a8ecb8caa0b97ce43233e0d3dd63f62d620d0015dd2f12b340a415a9d5f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationShadowProductionVariantsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31966fd03d176908d45d936ee615d66e2dfdefca02d3db094d7e2f4b7eedb313)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42d5175355121d0d42dac52dc3f0bf85fc0c987f061066241645e5d942f0e30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8dfa8246489798697392a8b83928404f8bfba3337f014e97d1e038fb7c5131)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f27c92cc84af1a8aaf4b09a39b21a06284f2b6a0c2c35bcdaf114783fc7f63e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0233e6227a511e9400ab4a71ef4f80a8885c530767541f65c9f27b72525d7750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1199b2ec0b60ef503bb5669b23505f3ba5a64262620051b2c202be6499cbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
        "status": "status",
    },
)
class SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972492ae36355e57ecb65a0ceea0956c54f66908fec46a6627bc442e8ffc7614)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.'''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a34b5d7c5e5c4e1981bc939c9b2a7ad8553fe837e92a64699886758d862866)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933236c62b618d063397c0ce9943366102b04438281ad27f53c82a0082ac2cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238b8033feb075e82fa45f42467243055a8806f1e4fca93370c71cdf3ffbddf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a97401e98793e3aa450d94f07db1186fd9847fbe037d13fd49c7124162da5d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342595795b0014728a083033f980e3400434c4751e3069beea1836d2bc8fe672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationShadowProductionVariantsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4254e82bebd69997165c686bbf9ef5af49a7a5f796456526122d535fe1c58ac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCoreDumpConfig")
    def put_core_dump_config(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: builtins.str,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        value = SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig(
            destination_s3_uri=destination_s3_uri, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putCoreDumpConfig", [value]))

    @jsii.member(jsii_name="putManagedInstanceScaling")
    def put_managed_instance_scaling(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        value = SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedInstanceScaling", [value]))

    @jsii.member(jsii_name="putRoutingConfig")
    def put_routing_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a523a03e27c8aa2dc9b650f7dc45a4d253add3bcf2ee617bac4921b63a60584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoutingConfig", [value]))

    @jsii.member(jsii_name="putServerlessConfig")
    def put_serverless_config(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        value = SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig(
            max_concurrency=max_concurrency,
            memory_size_in_mb=memory_size_in_mb,
            provisioned_concurrency=provisioned_concurrency,
        )

        return typing.cast(None, jsii.invoke(self, "putServerlessConfig", [value]))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetContainerStartupHealthCheckTimeoutInSeconds")
    def reset_container_startup_health_check_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerStartupHealthCheckTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetCoreDumpConfig")
    def reset_core_dump_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDumpConfig", []))

    @jsii.member(jsii_name="resetEnableSsmAccess")
    def reset_enable_ssm_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSsmAccess", []))

    @jsii.member(jsii_name="resetInferenceAmiVersion")
    def reset_inference_ami_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceAmiVersion", []))

    @jsii.member(jsii_name="resetInitialInstanceCount")
    def reset_initial_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialInstanceCount", []))

    @jsii.member(jsii_name="resetInitialVariantWeight")
    def reset_initial_variant_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialVariantWeight", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetManagedInstanceScaling")
    def reset_managed_instance_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedInstanceScaling", []))

    @jsii.member(jsii_name="resetModelDataDownloadTimeoutInSeconds")
    def reset_model_data_download_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataDownloadTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetModelName")
    def reset_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelName", []))

    @jsii.member(jsii_name="resetRoutingConfig")
    def reset_routing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingConfig", []))

    @jsii.member(jsii_name="resetServerlessConfig")
    def reset_serverless_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessConfig", []))

    @jsii.member(jsii_name="resetVariantName")
    def reset_variant_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariantName", []))

    @jsii.member(jsii_name="resetVolumeSizeInGb")
    def reset_volume_size_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSizeInGb", []))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfig")
    def core_dump_config(
        self,
    ) -> SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference, jsii.get(self, "coreDumpConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScaling")
    def managed_instance_scaling(
        self,
    ) -> SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference:
        return typing.cast(SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference, jsii.get(self, "managedInstanceScaling"))

    @builtins.property
    @jsii.member(jsii_name="routingConfig")
    def routing_config(
        self,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList":
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList", jsii.get(self, "routingConfig"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfig")
    def serverless_config(
        self,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference", jsii.get(self, "serverlessConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSecondsInput")
    def container_startup_health_check_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerStartupHealthCheckTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfigInput")
    def core_dump_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig], jsii.get(self, "coreDumpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccessInput")
    def enable_ssm_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSsmAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersionInput")
    def inference_ami_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceAmiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCountInput")
    def initial_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeightInput")
    def initial_variant_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialVariantWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScalingInput")
    def managed_instance_scaling_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling], jsii.get(self, "managedInstanceScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSecondsInput")
    def model_data_download_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modelDataDownloadTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelNameInput")
    def model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingConfigInput")
    def routing_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]], jsii.get(self, "routingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfigInput")
    def serverless_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"], jsii.get(self, "serverlessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="variantNameInput")
    def variant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGbInput")
    def volume_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14862d265497ae4580233d574d2ab28692f0c279b767754747efc396efa49ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSeconds")
    def container_startup_health_check_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerStartupHealthCheckTimeoutInSeconds"))

    @container_startup_health_check_timeout_in_seconds.setter
    def container_startup_health_check_timeout_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cb4a50f3ce32001f9f5dc74288cd8f4bb352577635ece5ff4030e118843e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerStartupHealthCheckTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccess")
    def enable_ssm_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSsmAccess"))

    @enable_ssm_access.setter
    def enable_ssm_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e84db4f17ba1daa9c550473467f922979f7a5fbaf65d1a040421dbaf79c742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSsmAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersion")
    def inference_ami_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inferenceAmiVersion"))

    @inference_ami_version.setter
    def inference_ami_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bf0de055333aaddfa7a1b13fc038f61bbf120eada08f572ea22faad5695127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceAmiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCount")
    def initial_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialInstanceCount"))

    @initial_instance_count.setter
    def initial_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0a0e5a96c526f843e29e78cc4fe4b5a8867f670cea3f99e2d890a5fc8f0c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeight")
    def initial_variant_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialVariantWeight"))

    @initial_variant_weight.setter
    def initial_variant_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917acb98f4d36b4a852392d95142df7332c70a7c953129d6e3dfc6102b3547fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVariantWeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8f2e8230771c87a181a1ff8a4459176211067c5d2b36c4f52247a18f514951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSeconds")
    def model_data_download_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "modelDataDownloadTimeoutInSeconds"))

    @model_data_download_timeout_in_seconds.setter
    def model_data_download_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce5edcc9b172e30dc60556f0175bc40e27985c8ff0fa1536d1aa7fb19586e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataDownloadTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelName"))

    @model_name.setter
    def model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b84a69b8e9ecde485b1222c67649b3f0bc2d5ea456bbdd6ba3f5d2958352e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variantName")
    def variant_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variantName"))

    @variant_name.setter
    def variant_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b3a43efb39912cbdc64a23a26edee2f5e3b9b515943fa43beaecad489e285b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variantName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInGb"))

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801731bac92cd749f63c8d022bfbcb899197502882bf0ef003fcad215d45093a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd43ecd9b260d8b883981fea665b8ad1bcb0d73bf4a17a48e96646e7021a97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig",
    jsii_struct_bases=[],
    name_mapping={"routing_strategy": "routingStrategy"},
)
class SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig:
    def __init__(self, *, routing_strategy: builtins.str) -> None:
        '''
        :param routing_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc11afea9b7836649f3669c2ffbf5637d669ddeabd44308b9fe70fcec8d1db1)
            check_type(argname="argument routing_strategy", value=routing_strategy, expected_type=type_hints["routing_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "routing_strategy": routing_strategy,
        }

    @builtins.property
    def routing_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.'''
        result = self._values.get("routing_strategy")
        assert result is not None, "Required property 'routing_strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfaae1b75c239de325e99e926d85729d10e5b8979e729200b39f83159c1a503a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50f103d8837d67857b0443bc3bc6b32158856982c097eceeb00abb833382dda)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6076382442905b44e4930e40a9ff24e2225b03db2bf2f15c5e256c35ccdd0ff1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc7fc7f64e19f79859b11baac98b07f14e70724404e4a5853ea5b7fea5940206)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d50f0c2a08844478a843217743fe3afa125a8612eb326a0342312fffaf616603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8c8e7e8d766dbf3bfe351417d2b18e205537dd39a96874888e49bc19a544b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d4cf774ab60cc939df274b607337d9145bb558e5a1491c5879e17b68535c971)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="routingStrategyInput")
    def routing_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="routingStrategy")
    def routing_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingStrategy"))

    @routing_strategy.setter
    def routing_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b46cf8a253e868f1e33d4a4556d3be559d31b0f7dd4a13812b396c2b62aabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8b0e7de1f7e12ccaa718076e069b9c11837b25d008b46a0614d6c6ffc3a306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrency": "maxConcurrency",
        "memory_size_in_mb": "memorySizeInMb",
        "provisioned_concurrency": "provisionedConcurrency",
    },
)
class SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig:
    def __init__(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb6808dadead365fedbebafc9ba7aed5790290ece17fa1a9c6b314d112933c7)
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument memory_size_in_mb", value=memory_size_in_mb, expected_type=type_hints["memory_size_in_mb"])
            check_type(argname="argument provisioned_concurrency", value=provisioned_concurrency, expected_type=type_hints["provisioned_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_concurrency": max_concurrency,
            "memory_size_in_mb": memory_size_in_mb,
        }
        if provisioned_concurrency is not None:
            self._values["provisioned_concurrency"] = provisioned_concurrency

    @builtins.property
    def max_concurrency(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.'''
        result = self._values.get("max_concurrency")
        assert result is not None, "Required property 'max_concurrency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_size_in_mb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.'''
        result = self._values.get("memory_size_in_mb")
        assert result is not None, "Required property 'memory_size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def provisioned_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.'''
        result = self._values.get("provisioned_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__020bb125518abb1c69a56c001c837335b5ee4303229724bc16285b8c4fb54530)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProvisionedConcurrency")
    def reset_provisioned_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyInput")
    def max_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMbInput")
    def memory_size_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyInput")
    def provisioned_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrency"))

    @max_concurrency.setter
    def max_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfd25d6c53e2c470b6cdb4b9e3e6de4e3dc24b1fa909630dd55a4ab9b54d1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMb")
    def memory_size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInMb"))

    @memory_size_in_mb.setter
    def memory_size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b184cc838a2a47b146a6cb2a72bffe8784d440999797785587383f5335d1a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrency")
    def provisioned_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedConcurrency"))

    @provisioned_concurrency.setter
    def provisioned_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809a3fcf5734df07ad9264b837638dc9fcae904c24c3e41557c5bc35b8dcb8dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827abb371822452b2559a6bf4d067d35448116a3cfc4610a82d76ccd98bd1e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerEndpointConfiguration",
    "SagemakerEndpointConfigurationAsyncInferenceConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference",
    "SagemakerEndpointConfigurationConfig",
    "SagemakerEndpointConfigurationDataCaptureConfig",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference",
    "SagemakerEndpointConfigurationDataCaptureConfigOutputReference",
    "SagemakerEndpointConfigurationProductionVariants",
    "SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig",
    "SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsList",
    "SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling",
    "SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsRoutingConfig",
    "SagemakerEndpointConfigurationProductionVariantsRoutingConfigList",
    "SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsServerlessConfig",
    "SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariants",
    "SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig",
    "SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsList",
    "SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling",
    "SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig",
    "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList",
    "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig",
    "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference",
]

publication.publish()

def _typecheckingstub__10e5f1a18bd7c0c29ecf34d89cccde8ab7a57b94165c3bf94a6cf4cda774a441(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
    async_inference_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_capture_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationDataCaptureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariants, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__464701cdc7a286ecbd687d268469461c422e08bdfb5816a498e6de7f4160b6eb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d409101870b9d31406ede9dc0d6d59f9fa4fa12e707d09c13ef211f945024fb0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ad8c41d683eac2118b6f93e1146c75ed82a1ac769d7fc2f1b18c7a05262a2a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a66b750588497abf9d325572da1ecd53644fd0f545f0dc801e99939c71c33fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d120bee8f83b8fbca8ef51895358a729be21a4824ceb2d98a492a740cbc2b99c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8aa6466bb10be647b2730e8fce3fa487fd02079e545f82232bb7d5d98d0d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7396942e891b2657f9a55f4c82f5ebff34fdd4909d71386aeb2688f9d6f2d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df4ef5bafbaa31230a376a4922797f2bd90e58fcd42864c5f7f1099c3707b91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cddca4b19997db895dad581ef1c3e1c97c8582d4e39fc18329e8cb5cbf2c3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315c3bc76a30e84e6e830a37bfdd35e70636dff5effc51146d85a89036653022(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5f704b1492cb96913ec2ddcbb37b44a0c3f243fde4360e0c579774e034c8e5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720cd2c81794152bb8ec89bec87838f4b3b4bb87c68f4005dd24bdd82b5a464d(
    *,
    output_config: typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig, typing.Dict[builtins.str, typing.Any]],
    client_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055b16bb51bf6667751ec62b721c53bcf5fd2d31e6da447bb8e41fd830d9b30f(
    *,
    max_concurrent_invocations_per_instance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9b6d7c0ba0789bd3e1235a72d7861725a41a5fdf6cbc763b2698a74614e969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a85d532369b24385a89be01b58e16eac098904757eee0f2b11a208949dda21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bceb2e9365e0056ece57fb99c86ac88f2c3e3e0159831d44c8616938c747bc(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c69351dec282aa75236cf3aa7f5760cedf6b8aa5d3816d07ae7654aac1d9c0(
    *,
    s3_output_path: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_failure_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144fdc270689803e343b736cb73c47135067bea2447ba4e7671b89607f38d772(
    *,
    error_topic: typing.Optional[builtins.str] = None,
    include_inference_response_in: typing.Optional[typing.Sequence[builtins.str]] = None,
    success_topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7528e08be06e87ede2a94024937c09c2a35e45fe2a3dfdbc089a90845e3d8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3d6b8761b5d38119643ccd51fe79ba0ca5d66e4597d38c0789c60ebd3acd6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaf5763df01aa0a63ed823287064afbbad5e5f82e2c24b7e091ef75c764031e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56db7a84bc599e9d5e81a6a4bdf2217fcf8a904951ba648275bff40fabaea38f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e56a8753bb99ae372727dcce9be66cf8a0c71eb2b78f9b32909fa9ca468dd1d(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc671aef5f1cbccea7e14939d2590fa3bca1694c999b3aa2ea23f81a3e72a99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5155a7dd407017dce0997f5bebf842cb84df61f427d6003c7baa96c7c2eb68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544081bc84ad7c62ccebc8ebf08214c1d0f23067f67f23ac9521184d493b5b36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158d22d7e336846e647abbe681bce05b7ccc54e9b9555d53681e7755029c2063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225486491489eb57d34f2c544b77a3e53b54bfa1da8799277ba17c5ec5e0a5d4(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d890f6422fadd98d3a4fb42bc7b877488039fa0bc2ed7ae1d2956fea1feeac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85ed5e6e0c9023a06f97b89275db10aff99491405163da655c832dd51d80588(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f2d056d9d0139a7b51838573de4ca5eda8eba8f0d8b0e9df915e0996d47bda(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
    async_inference_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_capture_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationDataCaptureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariants, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92dedb9aa102563a1b1cd2472fd6b7ea28f687e80241ef95ada5d8b0531c09b3(
    *,
    capture_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions, typing.Dict[builtins.str, typing.Any]]]],
    destination_s3_uri: builtins.str,
    initial_sampling_percentage: jsii.Number,
    capture_content_type_header: typing.Optional[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_capture: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7b9888f82e885d87c9d95c1a0ad87b06826f2f5720a37f1c18fec5299f1350(
    *,
    csv_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb40dbda232a5aac10457d89f42240c3021e97ae09b43abf57fac0b920035cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de38aaa9cf4aee4a71a8bc057986cbd6c8d1447bcae117e56f6612a24aa3b2a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61df39393bccc725b4b252c64648c227281f5ff38a310c175c43f70bf449106(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8fea878c05fc385ef96a168fdecb3755a2bd929898ec598f19a57cbb561160(
    value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd935e1696a348d246d3f68a2010d9fc7db95ea0cfc4758d1ffd54b1d7a57d52(
    *,
    capture_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d427a4936465b576c53b573771a6be0eab2ae99f19366c802f78d643864befe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43616ba8639d2e277bc414f4420b5e36da0c2c4404febf41abe8a1cb1caba0df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b268bff5feb666ca64d1a9809fe42086e568772b4f142b08b7cb0ac51d7d54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abe7d1c5a8c9a7c2d4b36cfe081d0beb5b8a19bcf8697c9723a3a2f09c6507f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3138dd45cbbf80b3a538b155666380a93a8a267b3ecf3b535134245554b60c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797d19f9846327bb146acaa9750814308e8462659b086c181fb4c712f86e9688(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83f9b01c6e73d5bc7051d974d3fd20af5107007c09487a969d434f95b7ac536(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56cd89ccc460e6ea64650db27fea73235b3bd6d1db2886f209cce7e3cdb2c376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3c2e6b2f5a37730df9cf84565f0c31e941591562a1de14cfb7ec5bc68562ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71db61eed693a5c06de18efd0d793bdaac8d03953b17b968d225b222caaf80c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9b99a597bee466024cc3c03245d11d321534a4b4b9ac30407d6c10db7cd93f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b9f885e465f86f8a97ca89327f09920cffa905dab5fa47e11f5dc531f23935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc6e75af04525e092baff877d5d113d86f1970b2db00e053fb7960629c4e434(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1251aed1ad75b5edf037624b81088690666f5d9800b68eb7054d0c6606b149b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e179ce9e622535edfaff43bfee9186323e470bd7a814dcbfeba60ae2833e28ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe3ffeeb5c63d9b6649f1a7d5098735e4ca3482998b8e475b3f7ff8031a49dd(
    value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5219294cbac728ee0df2941f486085e0ca0d53a1481778c0ad8e69ae379863(
    *,
    accelerator_type: typing.Optional[builtins.str] = None,
    container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    core_dump_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inference_ami_version: typing.Optional[builtins.str] = None,
    initial_instance_count: typing.Optional[jsii.Number] = None,
    initial_variant_weight: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    managed_instance_scaling: typing.Optional[typing.Union[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    model_name: typing.Optional[builtins.str] = None,
    routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    serverless_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationProductionVariantsServerlessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    variant_name: typing.Optional[builtins.str] = None,
    volume_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3af8f00ebf7650a141a5c5f6e775a267fdc5fbbeb73cc7cfbd5c772d0b93d7(
    *,
    destination_s3_uri: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5176586e5bbe669173f51e928e8d1961b38ccbeb2c2687794ff6a6f88af6dbc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efb0a372e88fe9f15f43ae20869c95c668acafaabbc2fb13447c94f9a3f88fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1c4841448068b9e3f29bafd666174924561deb73a834b739038901bdc10999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925fe9d6f804fbb0abf10c039f746e71828026cad7f115bd1693a4439b22b816(
    value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3f55fb142593bd9f424e086857a03c07e70113c329d256629e7a9b60925c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fc1e4083f1c72d57ba574427170c451d7390634fc516a027e3c05ee2edf3f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c890c66453f63d69f1d4f2e9e63eea03becaaa4536576d7611802a72b398c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742613823b57f36657ad9af2278ee7e747c047c20b4965ef4903cc436eb355c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c733cc37c684ea0eefb8217bbdcad4a579909e552486200ad58fcd91bfffcb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb9c9ad766b09d1e4669da07de79d7482d17378b2cf4dfdfb5d717dfb4cabcb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa619c69771e25d9133c2ccdbc4f0c8dea3fa5d688b2546a90986bd53402185b(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146fe1cf8472622af11907aa9e66d585db59913cc694f8a87aac48353946f2ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0ab93b728a361ac5541554fac1ccf406677c230f211d3e50e91e650dae29b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fed8852467fe5e0004fb63938d09d447baf51a09045b7ef7a5bac170699a3b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf3f1aaf7fec3bd9d61188aaacbc2f121c0b57316dc1276f9946d03928d6085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3730a9905fe40905b98f2cf08087e3e0a5e7700928cde23db9993c0538ca13(
    value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2bd3ef99aee6bb5795ad5b534aa5a72c1151844d48a7d974a80b93e0e0abb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a307d23b6f87453bee4f4fcb88076ad183c569184a88c589c8648bcc730bbcb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede185b947edc44ed61d061d99615bf5d4f7f6225c235372642b540f50743f2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0e16e5b6d8ae87b04ba1e5ad19e620c064b5d5b156096377443391b9415a03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c94454bba63f172d83ad36dbfd4c612ff58e654997f9853fc56b81e79a27d29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77233882865dcbf69592a26216384ebf09492b981e9b3af5604138bf7891192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4273209ea2c73d035988e894ecab380eec98919dbd5a2ecd9cd0a0bb34613c9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d215cd825fd07194098750d375b84198b2a9c9c76c988d36a3055f532ba641d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcb34cc6d85fc3590aacfd4c991286c5d4414be8e653bd686801870f26e5447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aced7a0ceab479a20de7c4cc46fa8304aadc384368d53a5efa9d741db9b598d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d101a3ccafc702a9450f5c0e611fe575cae9500a8df1958d0acd90a91d481b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249830508b0f16d71002195fc88cf66a917794a8744606db7078276ba111c886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b65c41537e88bd6ceafb6df8b58e1dad612553462b9d739649c1c75bf96844(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d29f1c08ce0bebe2fac1ec0f422df14ebbf860ad4fdbb817d55b3b1968b178(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e547c4010bcfc18721d69a903e770a0f7a68eabaccf481fa079eefa662dbdf25(
    *,
    routing_strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11f1eea3940e8ca2236fa7e7c27ddf7ceedcdb1043ff8238b69ddfcb245da21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7ea500d7022e4a90f0b43aea89ad80e49ad9a2de38c4a73187054f24de3fb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11ee1d4d82de73f47130614c45ab1f9869a60b4e6e61f6d4e2373967aaa7b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30e27a1f7f5df3004059913fd43a68a33ab1750ee03ab8f898498de084101e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef02cc78097b7d2b9c163dbbc57ef656c552d97f0afb1f349f0538b09222ee28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49df7a30d947d4a226e511ba88a3ce7626f34df944363a0eff476e33a2a9ef9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8871809d7ca6d8c8d2d0b5d6eb9cf6a6c8aaf4800ba26d2d31a57ba31a431a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12352f2c9a9d59708b90f680702c42a1bbc13b53be8de5675a9b49fbd142af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4665da96a21a824b271b75d3bf29328a8b0e54c24c2eed6be55f004b434afe1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd84e4d34c20369186c7c6e196580617f7682c9e946c9ce5dc06d6f222979c45(
    *,
    max_concurrency: jsii.Number,
    memory_size_in_mb: jsii.Number,
    provisioned_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78176fec3f09b7225db74a7f19b7a3a55e8cdd46f46629f18f84210f744b45b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad8d2f61db88e4b5360cec7e865dfa353dfcf07f288bc1e5f9bdb1c8cb28296(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b71711632e1eb55bfcbf0e12749941f10e51358feb81f2fd40d288f5093de42(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7246b5d4e1a83ca0e03bd0e2c9db7878a3cb041fded3b28159d9e4c39719c708(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a94e76de15561ab01bf3ea2b7f490446ad3a1cbbb3baf760d75a221db1e62e(
    value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c15d132289af4ea68aaea36c60a11060fd984c9e307d02a68bddeb3308ab2f5(
    *,
    accelerator_type: typing.Optional[builtins.str] = None,
    container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    core_dump_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inference_ami_version: typing.Optional[builtins.str] = None,
    initial_instance_count: typing.Optional[jsii.Number] = None,
    initial_variant_weight: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    managed_instance_scaling: typing.Optional[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    model_name: typing.Optional[builtins.str] = None,
    routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    serverless_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    variant_name: typing.Optional[builtins.str] = None,
    volume_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53d41ede059aa360e4e6f28d84852e5ad4577a3fdc0b22ff50879e0684e7a4f(
    *,
    destination_s3_uri: builtins.str,
    kms_key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08afde8dd7f9ebc5e2cdc8598bff96d1c1c1b2721fdff232c804aeef91fe69b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1965a0c1e5e19b39bc2c601c7903ae23bf618fb5fb3a07e3fea3d837d5c1a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e9b04712a2ae08458cca99ac91564769a1fb50e6ee6de0d442b65b8d818332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2a8ecb8caa0b97ce43233e0d3dd63f62d620d0015dd2f12b340a415a9d5f9f(
    value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31966fd03d176908d45d936ee615d66e2dfdefca02d3db094d7e2f4b7eedb313(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42d5175355121d0d42dac52dc3f0bf85fc0c987f061066241645e5d942f0e30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8dfa8246489798697392a8b83928404f8bfba3337f014e97d1e038fb7c5131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f27c92cc84af1a8aaf4b09a39b21a06284f2b6a0c2c35bcdaf114783fc7f63e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0233e6227a511e9400ab4a71ef4f80a8885c530767541f65c9f27b72525d7750(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1199b2ec0b60ef503bb5669b23505f3ba5a64262620051b2c202be6499cbac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972492ae36355e57ecb65a0ceea0956c54f66908fec46a6627bc442e8ffc7614(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a34b5d7c5e5c4e1981bc939c9b2a7ad8553fe837e92a64699886758d862866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933236c62b618d063397c0ce9943366102b04438281ad27f53c82a0082ac2cf0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238b8033feb075e82fa45f42467243055a8806f1e4fca93370c71cdf3ffbddf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a97401e98793e3aa450d94f07db1186fd9847fbe037d13fd49c7124162da5d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342595795b0014728a083033f980e3400434c4751e3069beea1836d2bc8fe672(
    value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4254e82bebd69997165c686bbf9ef5af49a7a5f796456526122d535fe1c58ac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a523a03e27c8aa2dc9b650f7dc45a4d253add3bcf2ee617bac4921b63a60584(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14862d265497ae4580233d574d2ab28692f0c279b767754747efc396efa49ed3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cb4a50f3ce32001f9f5dc74288cd8f4bb352577635ece5ff4030e118843e1f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e84db4f17ba1daa9c550473467f922979f7a5fbaf65d1a040421dbaf79c742(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bf0de055333aaddfa7a1b13fc038f61bbf120eada08f572ea22faad5695127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0a0e5a96c526f843e29e78cc4fe4b5a8867f670cea3f99e2d890a5fc8f0c8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917acb98f4d36b4a852392d95142df7332c70a7c953129d6e3dfc6102b3547fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8f2e8230771c87a181a1ff8a4459176211067c5d2b36c4f52247a18f514951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce5edcc9b172e30dc60556f0175bc40e27985c8ff0fa1536d1aa7fb19586e3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b84a69b8e9ecde485b1222c67649b3f0bc2d5ea456bbdd6ba3f5d2958352e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b3a43efb39912cbdc64a23a26edee2f5e3b9b515943fa43beaecad489e285b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801731bac92cd749f63c8d022bfbcb899197502882bf0ef003fcad215d45093a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd43ecd9b260d8b883981fea665b8ad1bcb0d73bf4a17a48e96646e7021a97b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc11afea9b7836649f3669c2ffbf5637d669ddeabd44308b9fe70fcec8d1db1(
    *,
    routing_strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfaae1b75c239de325e99e926d85729d10e5b8979e729200b39f83159c1a503a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50f103d8837d67857b0443bc3bc6b32158856982c097eceeb00abb833382dda(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6076382442905b44e4930e40a9ff24e2225b03db2bf2f15c5e256c35ccdd0ff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7fc7f64e19f79859b11baac98b07f14e70724404e4a5853ea5b7fea5940206(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50f0c2a08844478a843217743fe3afa125a8612eb326a0342312fffaf616603(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8c8e7e8d766dbf3bfe351417d2b18e205537dd39a96874888e49bc19a544b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4cf774ab60cc939df274b607337d9145bb558e5a1491c5879e17b68535c971(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b46cf8a253e868f1e33d4a4556d3be559d31b0f7dd4a13812b396c2b62aabf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8b0e7de1f7e12ccaa718076e069b9c11837b25d008b46a0614d6c6ffc3a306(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb6808dadead365fedbebafc9ba7aed5790290ece17fa1a9c6b314d112933c7(
    *,
    max_concurrency: jsii.Number,
    memory_size_in_mb: jsii.Number,
    provisioned_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020bb125518abb1c69a56c001c837335b5ee4303229724bc16285b8c4fb54530(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfd25d6c53e2c470b6cdb4b9e3e6de4e3dc24b1fa909630dd55a4ab9b54d1fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b184cc838a2a47b146a6cb2a72bffe8784d440999797785587383f5335d1a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809a3fcf5734df07ad9264b837638dc9fcae904c24c3e41557c5bc35b8dcb8dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827abb371822452b2559a6bf4d067d35448116a3cfc4610a82d76ccd98bd1e88(
    value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig],
) -> None:
    """Type checking stubs"""
    pass
