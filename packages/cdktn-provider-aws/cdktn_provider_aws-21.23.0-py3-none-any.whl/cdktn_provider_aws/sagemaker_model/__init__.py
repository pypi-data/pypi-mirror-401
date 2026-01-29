r'''
# `aws_sagemaker_model`

Refer to the Terraform Registry for docs: [`aws_sagemaker_model`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model).
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


class SagemakerModel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModel",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model aws_sagemaker_model}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        execution_role_arn: builtins.str,
        container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inference_execution_config: typing.Optional[typing.Union["SagemakerModelInferenceExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        primary_container: typing.Optional[typing.Union["SagemakerModelPrimaryContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerModelVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model aws_sagemaker_model} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#execution_role_arn SagemakerModel#execution_role_arn}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container SagemakerModel#container}
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#enable_network_isolation SagemakerModel#enable_network_isolation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#id SagemakerModel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inference_execution_config: inference_execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_execution_config SagemakerModel#inference_execution_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#name SagemakerModel#name}.
        :param primary_container: primary_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#primary_container SagemakerModel#primary_container}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#region SagemakerModel#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#tags SagemakerModel#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#tags_all SagemakerModel#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#vpc_config SagemakerModel#vpc_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc992f0e8277e59cc21fe09f24993030ab291c74c4cbeb6771a34ad34202211f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerModelConfig(
            execution_role_arn=execution_role_arn,
            container=container,
            enable_network_isolation=enable_network_isolation,
            id=id,
            inference_execution_config=inference_execution_config,
            name=name,
            primary_container=primary_container,
            region=region,
            tags=tags,
            tags_all=tags_all,
            vpc_config=vpc_config,
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
        '''Generates CDKTF code for importing a SagemakerModel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerModel to import.
        :param import_from_id: The id of the existing SagemakerModel that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerModel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545e2a3b0e25cf4905a61259ba51df2a4edd9a1c4e9c0eb6a88dc01d650e8f02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c0d41d1c1fa9712698bbb9f68a6b782bc57a9090fea3ca014996cb25c48aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putInferenceExecutionConfig")
    def put_inference_execution_config(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.
        '''
        value = SagemakerModelInferenceExecutionConfig(mode=mode)

        return typing.cast(None, jsii.invoke(self, "putInferenceExecutionConfig", [value]))

    @jsii.member(jsii_name="putPrimaryContainer")
    def put_primary_container(
        self,
        *,
        additional_model_data_source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelPrimaryContainerAdditionalModelDataSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        container_hostname: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inference_specification_name: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        model_data_source: typing.Optional[typing.Union["SagemakerModelPrimaryContainerModelDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_url: typing.Optional[builtins.str] = None,
        model_package_name: typing.Optional[builtins.str] = None,
        multi_model_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerMultiModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_model_data_source: additional_model_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#additional_model_data_source SagemakerModel#additional_model_data_source}
        :param container_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container_hostname SagemakerModel#container_hostname}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#environment SagemakerModel#environment}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image SagemakerModel#image}.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image_config SagemakerModel#image_config}
        :param inference_specification_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_specification_name SagemakerModel#inference_specification_name}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.
        :param model_data_source: model_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_source SagemakerModel#model_data_source}
        :param model_data_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_url SagemakerModel#model_data_url}.
        :param model_package_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_package_name SagemakerModel#model_package_name}.
        :param multi_model_config: multi_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#multi_model_config SagemakerModel#multi_model_config}
        '''
        value = SagemakerModelPrimaryContainer(
            additional_model_data_source=additional_model_data_source,
            container_hostname=container_hostname,
            environment=environment,
            image=image,
            image_config=image_config,
            inference_specification_name=inference_specification_name,
            mode=mode,
            model_data_source=model_data_source,
            model_data_url=model_data_url,
            model_package_name=model_package_name,
            multi_model_config=multi_model_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryContainer", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#security_group_ids SagemakerModel#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#subnets SagemakerModel#subnets}.
        '''
        value = SagemakerModelVpcConfig(
            security_group_ids=security_group_ids, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetEnableNetworkIsolation")
    def reset_enable_network_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNetworkIsolation", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInferenceExecutionConfig")
    def reset_inference_execution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceExecutionConfig", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPrimaryContainer")
    def reset_primary_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContainer", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

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
    @jsii.member(jsii_name="container")
    def container(self) -> "SagemakerModelContainerList":
        return typing.cast("SagemakerModelContainerList", jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="inferenceExecutionConfig")
    def inference_execution_config(
        self,
    ) -> "SagemakerModelInferenceExecutionConfigOutputReference":
        return typing.cast("SagemakerModelInferenceExecutionConfigOutputReference", jsii.get(self, "inferenceExecutionConfig"))

    @builtins.property
    @jsii.member(jsii_name="primaryContainer")
    def primary_container(self) -> "SagemakerModelPrimaryContainerOutputReference":
        return typing.cast("SagemakerModelPrimaryContainerOutputReference", jsii.get(self, "primaryContainer"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "SagemakerModelVpcConfigOutputReference":
        return typing.cast("SagemakerModelVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolationInput")
    def enable_network_isolation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNetworkIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceExecutionConfigInput")
    def inference_execution_config_input(
        self,
    ) -> typing.Optional["SagemakerModelInferenceExecutionConfig"]:
        return typing.cast(typing.Optional["SagemakerModelInferenceExecutionConfig"], jsii.get(self, "inferenceExecutionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContainerInput")
    def primary_container_input(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainer"]:
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainer"], jsii.get(self, "primaryContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

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
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["SagemakerModelVpcConfig"]:
        return typing.cast(typing.Optional["SagemakerModelVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolation")
    def enable_network_isolation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNetworkIsolation"))

    @enable_network_isolation.setter
    def enable_network_isolation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8d68503b43076392be58d3fdc26f3fee2ff94f9346df76cfbbb5e6936952bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNetworkIsolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ecf523ba1b3fb06054b71d7435f79cb9760d2d8a3d9a80697e603ce87d388e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b02152f71f13a7f7d3cbcf37087146c08bd4288889830a95389f0af0e43370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f7fc929a5c1efc92cb217b0816c110f660b2f529de901b3b2cd65e2d4ea11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ddb6b82e55639260630dab7e22a1945f6fb1cefa3e0ea619fcb8c8d82612f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4103bd20fbbd75687be453db8e83eafef84d5485d0c67baf5db66632d8a6b458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ce273f514dec9d8f7e8b1ca34d921c72033b4aa00c561f6662913f6e50fcfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "execution_role_arn": "executionRoleArn",
        "container": "container",
        "enable_network_isolation": "enableNetworkIsolation",
        "id": "id",
        "inference_execution_config": "inferenceExecutionConfig",
        "name": "name",
        "primary_container": "primaryContainer",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_config": "vpcConfig",
    },
)
class SagemakerModelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        execution_role_arn: builtins.str,
        container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inference_execution_config: typing.Optional[typing.Union["SagemakerModelInferenceExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        primary_container: typing.Optional[typing.Union["SagemakerModelPrimaryContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerModelVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#execution_role_arn SagemakerModel#execution_role_arn}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container SagemakerModel#container}
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#enable_network_isolation SagemakerModel#enable_network_isolation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#id SagemakerModel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inference_execution_config: inference_execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_execution_config SagemakerModel#inference_execution_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#name SagemakerModel#name}.
        :param primary_container: primary_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#primary_container SagemakerModel#primary_container}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#region SagemakerModel#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#tags SagemakerModel#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#tags_all SagemakerModel#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#vpc_config SagemakerModel#vpc_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inference_execution_config, dict):
            inference_execution_config = SagemakerModelInferenceExecutionConfig(**inference_execution_config)
        if isinstance(primary_container, dict):
            primary_container = SagemakerModelPrimaryContainer(**primary_container)
        if isinstance(vpc_config, dict):
            vpc_config = SagemakerModelVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8783df7ef7c4a0999f4e94071bf08fe6eeaa7070e4f39d226c81c727fd864cca)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument enable_network_isolation", value=enable_network_isolation, expected_type=type_hints["enable_network_isolation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inference_execution_config", value=inference_execution_config, expected_type=type_hints["inference_execution_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_container", value=primary_container, expected_type=type_hints["primary_container"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
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
        if enable_network_isolation is not None:
            self._values["enable_network_isolation"] = enable_network_isolation
        if id is not None:
            self._values["id"] = id
        if inference_execution_config is not None:
            self._values["inference_execution_config"] = inference_execution_config
        if name is not None:
            self._values["name"] = name
        if primary_container is not None:
            self._values["primary_container"] = primary_container
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

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
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#execution_role_arn SagemakerModel#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container SagemakerModel#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]], result)

    @builtins.property
    def enable_network_isolation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#enable_network_isolation SagemakerModel#enable_network_isolation}.'''
        result = self._values.get("enable_network_isolation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#id SagemakerModel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_execution_config(
        self,
    ) -> typing.Optional["SagemakerModelInferenceExecutionConfig"]:
        '''inference_execution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_execution_config SagemakerModel#inference_execution_config}
        '''
        result = self._values.get("inference_execution_config")
        return typing.cast(typing.Optional["SagemakerModelInferenceExecutionConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#name SagemakerModel#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_container(self) -> typing.Optional["SagemakerModelPrimaryContainer"]:
        '''primary_container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#primary_container SagemakerModel#primary_container}
        '''
        result = self._values.get("primary_container")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainer"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#region SagemakerModel#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#tags SagemakerModel#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#tags_all SagemakerModel#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_config(self) -> typing.Optional["SagemakerModelVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#vpc_config SagemakerModel#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["SagemakerModelVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainer",
    jsii_struct_bases=[],
    name_mapping={
        "additional_model_data_source": "additionalModelDataSource",
        "container_hostname": "containerHostname",
        "environment": "environment",
        "image": "image",
        "image_config": "imageConfig",
        "inference_specification_name": "inferenceSpecificationName",
        "mode": "mode",
        "model_data_source": "modelDataSource",
        "model_data_url": "modelDataUrl",
        "model_package_name": "modelPackageName",
        "multi_model_config": "multiModelConfig",
    },
)
class SagemakerModelContainer:
    def __init__(
        self,
        *,
        additional_model_data_source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainerAdditionalModelDataSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        container_hostname: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union["SagemakerModelContainerImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inference_specification_name: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        model_data_source: typing.Optional[typing.Union["SagemakerModelContainerModelDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_url: typing.Optional[builtins.str] = None,
        model_package_name: typing.Optional[builtins.str] = None,
        multi_model_config: typing.Optional[typing.Union["SagemakerModelContainerMultiModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_model_data_source: additional_model_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#additional_model_data_source SagemakerModel#additional_model_data_source}
        :param container_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container_hostname SagemakerModel#container_hostname}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#environment SagemakerModel#environment}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image SagemakerModel#image}.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image_config SagemakerModel#image_config}
        :param inference_specification_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_specification_name SagemakerModel#inference_specification_name}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.
        :param model_data_source: model_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_source SagemakerModel#model_data_source}
        :param model_data_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_url SagemakerModel#model_data_url}.
        :param model_package_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_package_name SagemakerModel#model_package_name}.
        :param multi_model_config: multi_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#multi_model_config SagemakerModel#multi_model_config}
        '''
        if isinstance(image_config, dict):
            image_config = SagemakerModelContainerImageConfig(**image_config)
        if isinstance(model_data_source, dict):
            model_data_source = SagemakerModelContainerModelDataSource(**model_data_source)
        if isinstance(multi_model_config, dict):
            multi_model_config = SagemakerModelContainerMultiModelConfig(**multi_model_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6d44aaff424faedd9b53588d6bcf4422f3d354020f603b42a4d06a0fe1f4f8)
            check_type(argname="argument additional_model_data_source", value=additional_model_data_source, expected_type=type_hints["additional_model_data_source"])
            check_type(argname="argument container_hostname", value=container_hostname, expected_type=type_hints["container_hostname"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument inference_specification_name", value=inference_specification_name, expected_type=type_hints["inference_specification_name"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument model_data_source", value=model_data_source, expected_type=type_hints["model_data_source"])
            check_type(argname="argument model_data_url", value=model_data_url, expected_type=type_hints["model_data_url"])
            check_type(argname="argument model_package_name", value=model_package_name, expected_type=type_hints["model_package_name"])
            check_type(argname="argument multi_model_config", value=multi_model_config, expected_type=type_hints["multi_model_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_model_data_source is not None:
            self._values["additional_model_data_source"] = additional_model_data_source
        if container_hostname is not None:
            self._values["container_hostname"] = container_hostname
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if image_config is not None:
            self._values["image_config"] = image_config
        if inference_specification_name is not None:
            self._values["inference_specification_name"] = inference_specification_name
        if mode is not None:
            self._values["mode"] = mode
        if model_data_source is not None:
            self._values["model_data_source"] = model_data_source
        if model_data_url is not None:
            self._values["model_data_url"] = model_data_url
        if model_package_name is not None:
            self._values["model_package_name"] = model_package_name
        if multi_model_config is not None:
            self._values["multi_model_config"] = multi_model_config

    @builtins.property
    def additional_model_data_source(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerAdditionalModelDataSource"]]]:
        '''additional_model_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#additional_model_data_source SagemakerModel#additional_model_data_source}
        '''
        result = self._values.get("additional_model_data_source")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerAdditionalModelDataSource"]]], result)

    @builtins.property
    def container_hostname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container_hostname SagemakerModel#container_hostname}.'''
        result = self._values.get("container_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#environment SagemakerModel#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image SagemakerModel#image}.'''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(self) -> typing.Optional["SagemakerModelContainerImageConfig"]:
        '''image_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image_config SagemakerModel#image_config}
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional["SagemakerModelContainerImageConfig"], result)

    @builtins.property
    def inference_specification_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_specification_name SagemakerModel#inference_specification_name}.'''
        result = self._values.get("inference_specification_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_data_source(
        self,
    ) -> typing.Optional["SagemakerModelContainerModelDataSource"]:
        '''model_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_source SagemakerModel#model_data_source}
        '''
        result = self._values.get("model_data_source")
        return typing.cast(typing.Optional["SagemakerModelContainerModelDataSource"], result)

    @builtins.property
    def model_data_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_url SagemakerModel#model_data_url}.'''
        result = self._values.get("model_data_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_package_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_package_name SagemakerModel#model_package_name}.'''
        result = self._values.get("model_package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_model_config(
        self,
    ) -> typing.Optional["SagemakerModelContainerMultiModelConfig"]:
        '''multi_model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#multi_model_config SagemakerModel#multi_model_config}
        '''
        result = self._values.get("multi_model_config")
        return typing.cast(typing.Optional["SagemakerModelContainerMultiModelConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSource",
    jsii_struct_bases=[],
    name_mapping={"channel_name": "channelName", "s3_data_source": "s3DataSource"},
)
class SagemakerModelContainerAdditionalModelDataSource:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainerAdditionalModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#channel_name SagemakerModel#channel_name}.
        :param s3_data_source: s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36232968630ac85fb8076b0a1a66c057974ee6988ffc53f4af1323cee7a4ae58)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_name": channel_name,
            "s3_data_source": s3_data_source,
        }

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#channel_name SagemakerModel#channel_name}.'''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_data_source(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerAdditionalModelDataSourceS3DataSource"]]:
        '''s3_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        result = self._values.get("s3_data_source")
        assert result is not None, "Required property 's3_data_source' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerAdditionalModelDataSourceS3DataSource"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerAdditionalModelDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerAdditionalModelDataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb3f918717b1846395a0fae86146b31172298fb434b83c03404f004a2980282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerModelContainerAdditionalModelDataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd940abf481f6ecf0a92010f7f02d8065eaafdc48b9c5e8935b79e93b03cad64)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelContainerAdditionalModelDataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a601bb08d2f21716cca976317f39495ac86ecbd1d9a5f23dc20bee1eb94b2d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7614e95d1089e45fefdec7fb31a28c4f4835b8e1a466a7460af5ba14b0793489)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfd6d1501756299d9a337f853aee7ff6466ef88b54b1996c643e002f775f99bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9974d10aee7b7a0861d9951df24d4878500cb8785427963f1f04c87e44b15fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelContainerAdditionalModelDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6187f3a42e1455f71e60ba4ae9a9a0086115ecd985358c6b60c771cdfd019e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putS3DataSource")
    def put_s3_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainerAdditionalModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9d5dae47011c221ca6e763e013a6e5def707519eb0a55f7300f668e68e3985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3DataSource", [value]))

    @builtins.property
    @jsii.member(jsii_name="s3DataSource")
    def s3_data_source(
        self,
    ) -> "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceList":
        return typing.cast("SagemakerModelContainerAdditionalModelDataSourceS3DataSourceList", jsii.get(self, "s3DataSource"))

    @builtins.property
    @jsii.member(jsii_name="channelNameInput")
    def channel_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataSourceInput")
    def s3_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerAdditionalModelDataSourceS3DataSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerAdditionalModelDataSourceS3DataSource"]]], jsii.get(self, "s3DataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73cfab283a6323d7667c7ed05a813ebf48d4f292cf74eba7b659b3eacb5a94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ebffee651505f6da68488abea44378dadf0a9e0802c560e5274d8849ed7005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceS3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "compression_type": "compressionType",
        "s3_data_type": "s3DataType",
        "s3_uri": "s3Uri",
        "model_access_config": "modelAccessConfig",
    },
)
class SagemakerModelContainerAdditionalModelDataSourceS3DataSource:
    def __init__(
        self,
        *,
        compression_type: builtins.str,
        s3_data_type: builtins.str,
        s3_uri: builtins.str,
        model_access_config: typing.Optional[typing.Union["SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.
        :param s3_data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.
        :param model_access_config: model_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        if isinstance(model_access_config, dict):
            model_access_config = SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig(**model_access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75915e58f59d07124d49746f946f0ecc902e7985e3ef732e257a2090c4024246)
            check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
            check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument model_access_config", value=model_access_config, expected_type=type_hints["model_access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression_type": compression_type,
            "s3_data_type": s3_data_type,
            "s3_uri": s3_uri,
        }
        if model_access_config is not None:
            self._values["model_access_config"] = model_access_config

    @builtins.property
    def compression_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.'''
        result = self._values.get("compression_type")
        assert result is not None, "Required property 'compression_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_data_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.'''
        result = self._values.get("s3_data_type")
        assert result is not None, "Required property 's3_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_access_config(
        self,
    ) -> typing.Optional["SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig"]:
        '''model_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        result = self._values.get("model_access_config")
        return typing.cast(typing.Optional["SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerAdditionalModelDataSourceS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerAdditionalModelDataSourceS3DataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceS3DataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f4ca8b7f13fd43dfefd57d0bb0b248fe3d2d7b4c9d1ced59e894bcf71bffa0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33412c2afa8256613465b69652e58dffe8eb337bc2eb05d38ddb50a139f561cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelContainerAdditionalModelDataSourceS3DataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c64af59f58f0be83d75c3ab09b35535d343d3061d4498ff68ea40f3d6eafce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fad5c64ab1c26ff1e9d68afb144e56dfed7dd9376c4a9f3c520b524c0db3612b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e62baf1fff924931a486a5f14fd2ac47bb7dd13802ddeb7fbeeebb01bcfa8cb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSourceS3DataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSourceS3DataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSourceS3DataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b63e0392b563612b4ac9ff9e814737c06eefbf7aedffdae33e4ecdc58f6315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"accept_eula": "acceptEula"},
)
class SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig:
    def __init__(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac35ad7a151c870e46b632a8de2632b8004f53ba8569b2eba49b77390cccf3b9)
            check_type(argname="argument accept_eula", value=accept_eula, expected_type=type_hints["accept_eula"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accept_eula": accept_eula,
        }

    @builtins.property
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.'''
        result = self._values.get("accept_eula")
        assert result is not None, "Required property 'accept_eula' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a25d74f00397ced13150e46cf1ab5327e30163ad0ce4246d24dcef81c0ee901)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="acceptEulaInput")
    def accept_eula_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptEulaInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptEula")
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptEula"))

    @accept_eula.setter
    def accept_eula(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc08e3df3484b11e53534a8a4df7f511f9d65188ab14f314118d3e3a294df1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptEula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35236ff5db627b0bc168f30e7b9773722c83cb1eca2aeb5607de249a8f7af798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelContainerAdditionalModelDataSourceS3DataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerAdditionalModelDataSourceS3DataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9d64184d739d99d5f7848189081fc501ce69962cb63a4ae2ccb979408eca56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putModelAccessConfig")
    def put_model_access_config(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        value = SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig(
            accept_eula=accept_eula
        )

        return typing.cast(None, jsii.invoke(self, "putModelAccessConfig", [value]))

    @jsii.member(jsii_name="resetModelAccessConfig")
    def reset_model_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelAccessConfig", []))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfig")
    def model_access_config(
        self,
    ) -> SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference:
        return typing.cast(SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference, jsii.get(self, "modelAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="compressionTypeInput")
    def compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfigInput")
    def model_access_config_input(
        self,
    ) -> typing.Optional[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "modelAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataTypeInput")
    def s3_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionType")
    def compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionType"))

    @compression_type.setter
    def compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4899c4e6139dcb94cb7881ddbdace41e8ea9d53120ac485090d4d8814f578e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataType")
    def s3_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataType"))

    @s3_data_type.setter
    def s3_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f22d18b1a2a8ce4240a27b0c50ff35db4a8b1fd680fee00f9c53447b447452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3378fea05dfa872d26bc185fb120f3487759d638c78543fd1b9a493ce9d59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSourceS3DataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSourceS3DataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSourceS3DataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96e6c349a26a48a899f12e8b5163339955b5d26fff29fda8db35cb2c8f4428c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerImageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_access_mode": "repositoryAccessMode",
        "repository_auth_config": "repositoryAuthConfig",
    },
)
class SagemakerModelContainerImageConfig:
    def __init__(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union["SagemakerModelContainerImageConfigRepositoryAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        if isinstance(repository_auth_config, dict):
            repository_auth_config = SagemakerModelContainerImageConfigRepositoryAuthConfig(**repository_auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a47c28b8f4753c4fcc68ca840f83e90b8600c667774c1e8de89bbe9fc7a98bf)
            check_type(argname="argument repository_access_mode", value=repository_access_mode, expected_type=type_hints["repository_access_mode"])
            check_type(argname="argument repository_auth_config", value=repository_auth_config, expected_type=type_hints["repository_auth_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_access_mode": repository_access_mode,
        }
        if repository_auth_config is not None:
            self._values["repository_auth_config"] = repository_auth_config

    @builtins.property
    def repository_access_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.'''
        result = self._values.get("repository_access_mode")
        assert result is not None, "Required property 'repository_access_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_auth_config(
        self,
    ) -> typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"]:
        '''repository_auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        result = self._values.get("repository_auth_config")
        return typing.cast(typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerImageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerImageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6374e1067c22177648c957b66c2b17328beab73ea3d2ea721b8d28c035c8768)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepositoryAuthConfig")
    def put_repository_auth_config(
        self,
        *,
        repository_credentials_provider_arn: builtins.str,
    ) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        value = SagemakerModelContainerImageConfigRepositoryAuthConfig(
            repository_credentials_provider_arn=repository_credentials_provider_arn
        )

        return typing.cast(None, jsii.invoke(self, "putRepositoryAuthConfig", [value]))

    @jsii.member(jsii_name="resetRepositoryAuthConfig")
    def reset_repository_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryAuthConfig", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfig")
    def repository_auth_config(
        self,
    ) -> "SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference":
        return typing.cast("SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference", jsii.get(self, "repositoryAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessModeInput")
    def repository_access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryAccessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfigInput")
    def repository_auth_config_input(
        self,
    ) -> typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"]:
        return typing.cast(typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"], jsii.get(self, "repositoryAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessMode")
    def repository_access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryAccessMode"))

    @repository_access_mode.setter
    def repository_access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c19932a6833906ed68e6b7e227d93cd5151a631f33d5f279bd506b058869bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryAccessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerImageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerImageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16746e0a97613ea91d43a507c0d7cad0dc6f1d17375e78db578cd9451533e07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerImageConfigRepositoryAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_credentials_provider_arn": "repositoryCredentialsProviderArn",
    },
)
class SagemakerModelContainerImageConfigRepositoryAuthConfig:
    def __init__(self, *, repository_credentials_provider_arn: builtins.str) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c7c4ccfbe3284ec37540bffa54e6cacc719b82b02d199d75a5e824f9d5e34a)
            check_type(argname="argument repository_credentials_provider_arn", value=repository_credentials_provider_arn, expected_type=type_hints["repository_credentials_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_credentials_provider_arn": repository_credentials_provider_arn,
        }

    @builtins.property
    def repository_credentials_provider_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.'''
        result = self._values.get("repository_credentials_provider_arn")
        assert result is not None, "Required property 'repository_credentials_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerImageConfigRepositoryAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c220fafaf621742ade0dc652f43880ba2e41f07c2bd09c34eece7e4adcc7007d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArnInput")
    def repository_credentials_provider_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCredentialsProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArn")
    def repository_credentials_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCredentialsProviderArn"))

    @repository_credentials_provider_arn.setter
    def repository_credentials_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a56d2f7eecfe330d0dc333a947d0dd1d30f74484375426e1bdd234e89638a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCredentialsProviderArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f11b6cb9d58bda004fa591a78569d32f6ce1aea5c9b1099f09697640cf7723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f083a5cb39f7a64c2f17aeca4e61317d2122b8c458362f20ce3cbb856b93a8be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SagemakerModelContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef372e2d68a1ed8fe302e8887734b54a2d2e3c96492fecafa45b440212160933)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0729913b118bfe4cafb0de5d32de907092dac76a5bb2905b84f07f312b930f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__962ab446c73cc5616f792bbea028d463bf07c8a631ffa62686d387b8a9c53900)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63db4acbac599a0abf0f741608b9bd2fc41f73f00461c166c209c92eadcca9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2b3bc1e068fec0171294572c9afe08c2bd2d43df153e5a11f43c1d9184e36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSource",
    jsii_struct_bases=[],
    name_mapping={"s3_data_source": "s3DataSource"},
)
class SagemakerModelContainerModelDataSource:
    def __init__(
        self,
        *,
        s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainerModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param s3_data_source: s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624c0fc420a6b78c0fc21d27c226fb683c3d781e15f54397b7865ad5f63ef8f0)
            check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_data_source": s3_data_source,
        }

    @builtins.property
    def s3_data_source(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerModelDataSourceS3DataSource"]]:
        '''s3_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        result = self._values.get("s3_data_source")
        assert result is not None, "Required property 's3_data_source' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerModelDataSourceS3DataSource"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerModelDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerModelDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba113b66b9f05cab2f4d622379df9d92ac59a4787ac669f0bc7a2ed0ad79c185)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3DataSource")
    def put_s3_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainerModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f2ce9a8e9d97b18fc3720a9bf5afab663371b096b8254c04091a4d13a4ca17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3DataSource", [value]))

    @builtins.property
    @jsii.member(jsii_name="s3DataSource")
    def s3_data_source(
        self,
    ) -> "SagemakerModelContainerModelDataSourceS3DataSourceList":
        return typing.cast("SagemakerModelContainerModelDataSourceS3DataSourceList", jsii.get(self, "s3DataSource"))

    @builtins.property
    @jsii.member(jsii_name="s3DataSourceInput")
    def s3_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerModelDataSourceS3DataSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainerModelDataSourceS3DataSource"]]], jsii.get(self, "s3DataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelContainerModelDataSource]:
        return typing.cast(typing.Optional[SagemakerModelContainerModelDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerModelDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288ea51e5d2db803a8f0e10fe9b657ae76e00432b121f383bcc7a828a168ab00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSourceS3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "compression_type": "compressionType",
        "s3_data_type": "s3DataType",
        "s3_uri": "s3Uri",
        "model_access_config": "modelAccessConfig",
    },
)
class SagemakerModelContainerModelDataSourceS3DataSource:
    def __init__(
        self,
        *,
        compression_type: builtins.str,
        s3_data_type: builtins.str,
        s3_uri: builtins.str,
        model_access_config: typing.Optional[typing.Union["SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.
        :param s3_data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.
        :param model_access_config: model_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        if isinstance(model_access_config, dict):
            model_access_config = SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig(**model_access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a75fc14d17be2c2692d7fadb286697b09473d7568d3dd6e4f86f6c4142f653)
            check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
            check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument model_access_config", value=model_access_config, expected_type=type_hints["model_access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression_type": compression_type,
            "s3_data_type": s3_data_type,
            "s3_uri": s3_uri,
        }
        if model_access_config is not None:
            self._values["model_access_config"] = model_access_config

    @builtins.property
    def compression_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.'''
        result = self._values.get("compression_type")
        assert result is not None, "Required property 'compression_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_data_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.'''
        result = self._values.get("s3_data_type")
        assert result is not None, "Required property 's3_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_access_config(
        self,
    ) -> typing.Optional["SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig"]:
        '''model_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        result = self._values.get("model_access_config")
        return typing.cast(typing.Optional["SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerModelDataSourceS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerModelDataSourceS3DataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSourceS3DataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af036fe0c8720fea0825370ac2107e7319dd7b4d8140a2d0846ba44e829d3398)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerModelContainerModelDataSourceS3DataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0075c2471ccab9403595507740b5b1b8c610085a4577353a14824e2606500245)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelContainerModelDataSourceS3DataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f23af1734c4a9bebc6097e1568c8d17ce5617b8495025630e97835b6a34db5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0797d7081abd1499ca4f437bf144eed0b21b7915efd4c309c6d1ef904e2eda12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70142a9eaad93df55304f042b6f1775f8e9140c601edcbf6af23bb977e7589c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerModelDataSourceS3DataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerModelDataSourceS3DataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerModelDataSourceS3DataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52908c434422470876c4d6a42b3076a1d2ad6a46bef7d6de685a209d67de18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"accept_eula": "acceptEula"},
)
class SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig:
    def __init__(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842f0ff5b11209edd2b179b3c84d6252886bcf5a7cd8a0bf492c6b7cd0a764f2)
            check_type(argname="argument accept_eula", value=accept_eula, expected_type=type_hints["accept_eula"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accept_eula": accept_eula,
        }

    @builtins.property
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.'''
        result = self._values.get("accept_eula")
        assert result is not None, "Required property 'accept_eula' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__635fa9fbe8c95c61b6255c81922158b5bf868e1670ba76c756ee57b46bbe538b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="acceptEulaInput")
    def accept_eula_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptEulaInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptEula")
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptEula"))

    @accept_eula.setter
    def accept_eula(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561ed446019cfa933fed1f7895f6132e056fe133837abf4f93e1772e7a86f3a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptEula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c30f4c00f33674288f13c06c90e1d341848f945c46d4b66523bf568d5f90ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelContainerModelDataSourceS3DataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerModelDataSourceS3DataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec5aee46ee45614f81ebeb15aa5fa5620e062e265b1f20b6b6d1fc9312a2dc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putModelAccessConfig")
    def put_model_access_config(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        value = SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig(
            accept_eula=accept_eula
        )

        return typing.cast(None, jsii.invoke(self, "putModelAccessConfig", [value]))

    @jsii.member(jsii_name="resetModelAccessConfig")
    def reset_model_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelAccessConfig", []))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfig")
    def model_access_config(
        self,
    ) -> SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference:
        return typing.cast(SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference, jsii.get(self, "modelAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="compressionTypeInput")
    def compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfigInput")
    def model_access_config_input(
        self,
    ) -> typing.Optional[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "modelAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataTypeInput")
    def s3_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionType")
    def compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionType"))

    @compression_type.setter
    def compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70881edcc2043bda42e90dea9dea3b34af54c2e7ba63a5efe00fa5c818ddb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataType")
    def s3_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataType"))

    @s3_data_type.setter
    def s3_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808b8a38a446ec10252595f732e22cc8bbce9f9675c3d5f4177a87a1e0de8386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302a507e324d825e3364fc08d447ca1c428abcb569ee8f9bd2b672331dc4186f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerModelDataSourceS3DataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerModelDataSourceS3DataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerModelDataSourceS3DataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca4933c1ffa2b078a616888d44d4173b164f47f64abc1981f6fccc57b72a220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerMultiModelConfig",
    jsii_struct_bases=[],
    name_mapping={"model_cache_setting": "modelCacheSetting"},
)
class SagemakerModelContainerMultiModelConfig:
    def __init__(
        self,
        *,
        model_cache_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model_cache_setting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_cache_setting SagemakerModel#model_cache_setting}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91020eb18bd7446d96ad621c73a425fa7c00e6f49df266e4ea9d4f5b9223930)
            check_type(argname="argument model_cache_setting", value=model_cache_setting, expected_type=type_hints["model_cache_setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if model_cache_setting is not None:
            self._values["model_cache_setting"] = model_cache_setting

    @builtins.property
    def model_cache_setting(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_cache_setting SagemakerModel#model_cache_setting}.'''
        result = self._values.get("model_cache_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerMultiModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerMultiModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerMultiModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__753543badcf1826f9f2ce9d90016f6abddaf0e69743e679537e343b60ef55858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModelCacheSetting")
    def reset_model_cache_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelCacheSetting", []))

    @builtins.property
    @jsii.member(jsii_name="modelCacheSettingInput")
    def model_cache_setting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelCacheSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="modelCacheSetting")
    def model_cache_setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelCacheSetting"))

    @model_cache_setting.setter
    def model_cache_setting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496e104901cb587a9b4bca1e3a2eed6725bdd5dd08412e1eda2c3df7c59cbdfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelCacheSetting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelContainerMultiModelConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerMultiModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerMultiModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb64361c1c1ee2cb4fa6524abe08c0c1c248cad3a4a7b20fecaec3012bf02a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43c9f960780075444cff802b5d51efa7cf0d5c7033e0c39c6a3295ee7bdb7485)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdditionalModelDataSource")
    def put_additional_model_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerAdditionalModelDataSource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d96ffab10bd5c243eb8c87c48f5095b27c434083cc44cf07d97d35a827af30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalModelDataSource", [value]))

    @jsii.member(jsii_name="putImageConfig")
    def put_image_config(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union[SagemakerModelContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        value = SagemakerModelContainerImageConfig(
            repository_access_mode=repository_access_mode,
            repository_auth_config=repository_auth_config,
        )

        return typing.cast(None, jsii.invoke(self, "putImageConfig", [value]))

    @jsii.member(jsii_name="putModelDataSource")
    def put_model_data_source(
        self,
        *,
        s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param s3_data_source: s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        value = SagemakerModelContainerModelDataSource(s3_data_source=s3_data_source)

        return typing.cast(None, jsii.invoke(self, "putModelDataSource", [value]))

    @jsii.member(jsii_name="putMultiModelConfig")
    def put_multi_model_config(
        self,
        *,
        model_cache_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model_cache_setting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_cache_setting SagemakerModel#model_cache_setting}.
        '''
        value = SagemakerModelContainerMultiModelConfig(
            model_cache_setting=model_cache_setting
        )

        return typing.cast(None, jsii.invoke(self, "putMultiModelConfig", [value]))

    @jsii.member(jsii_name="resetAdditionalModelDataSource")
    def reset_additional_model_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalModelDataSource", []))

    @jsii.member(jsii_name="resetContainerHostname")
    def reset_container_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerHostname", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetImageConfig")
    def reset_image_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfig", []))

    @jsii.member(jsii_name="resetInferenceSpecificationName")
    def reset_inference_specification_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceSpecificationName", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetModelDataSource")
    def reset_model_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataSource", []))

    @jsii.member(jsii_name="resetModelDataUrl")
    def reset_model_data_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataUrl", []))

    @jsii.member(jsii_name="resetModelPackageName")
    def reset_model_package_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelPackageName", []))

    @jsii.member(jsii_name="resetMultiModelConfig")
    def reset_multi_model_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiModelConfig", []))

    @builtins.property
    @jsii.member(jsii_name="additionalModelDataSource")
    def additional_model_data_source(
        self,
    ) -> SagemakerModelContainerAdditionalModelDataSourceList:
        return typing.cast(SagemakerModelContainerAdditionalModelDataSourceList, jsii.get(self, "additionalModelDataSource"))

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(self) -> SagemakerModelContainerImageConfigOutputReference:
        return typing.cast(SagemakerModelContainerImageConfigOutputReference, jsii.get(self, "imageConfig"))

    @builtins.property
    @jsii.member(jsii_name="modelDataSource")
    def model_data_source(
        self,
    ) -> SagemakerModelContainerModelDataSourceOutputReference:
        return typing.cast(SagemakerModelContainerModelDataSourceOutputReference, jsii.get(self, "modelDataSource"))

    @builtins.property
    @jsii.member(jsii_name="multiModelConfig")
    def multi_model_config(
        self,
    ) -> SagemakerModelContainerMultiModelConfigOutputReference:
        return typing.cast(SagemakerModelContainerMultiModelConfigOutputReference, jsii.get(self, "multiModelConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalModelDataSourceInput")
    def additional_model_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSource]]], jsii.get(self, "additionalModelDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="containerHostnameInput")
    def container_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigInput")
    def image_config_input(self) -> typing.Optional[SagemakerModelContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerImageConfig], jsii.get(self, "imageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceSpecificationNameInput")
    def inference_specification_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceSpecificationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataSourceInput")
    def model_data_source_input(
        self,
    ) -> typing.Optional[SagemakerModelContainerModelDataSource]:
        return typing.cast(typing.Optional[SagemakerModelContainerModelDataSource], jsii.get(self, "modelDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataUrlInput")
    def model_data_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelDataUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="modelPackageNameInput")
    def model_package_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelPackageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="multiModelConfigInput")
    def multi_model_config_input(
        self,
    ) -> typing.Optional[SagemakerModelContainerMultiModelConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerMultiModelConfig], jsii.get(self, "multiModelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="containerHostname")
    def container_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerHostname"))

    @container_hostname.setter
    def container_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab39ffcf98f43a73706797d66962726c247fc8c4aeced2a9760a4ff37e533252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerHostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c7ea3f4f6ac05473dfd819a247cde2428a978f3c7cad4a1a29cac4cd430850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd8bf66c91b5bc51b359ab15e2535a6b51cc1b8d138a376ef3977e134b20d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceSpecificationName")
    def inference_specification_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inferenceSpecificationName"))

    @inference_specification_name.setter
    def inference_specification_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9155fc4cbc87efc78aacb75eedb14e59aee1695c49a225c4dd4edc0763718704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceSpecificationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff29ad288011e63c6c3d65dc99bb072c7abe05145685f96d99c1be376f0cd21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDataUrl")
    def model_data_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDataUrl"))

    @model_data_url.setter
    def model_data_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2445a188233d48ffe0fe39d01b419745c678bfb5fc09e7304a94eb7695f5eb69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelPackageName")
    def model_package_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelPackageName"))

    @model_package_name.setter
    def model_package_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df7d64529b4ef5093356c0f66d884976784aa603b6f9381538ef7c359c6b056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelPackageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d12b183d2bb55eba64dd37dd5e8ca4aba8d91d487842e64c6cf80ea202dd716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelInferenceExecutionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class SagemakerModelInferenceExecutionConfig:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a0764f69de895b19d113bc4402e50ad7aae2b46dc1d5cbfbf02e46d152b65e)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelInferenceExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelInferenceExecutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelInferenceExecutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dbc0daa23a907248d97f0df705588c9abf9e7898a3ec119784110d8f256ee6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41fbea755d30cc9bbe174271d126b6dc5c41b6d7c56bdda70e6637eef5b7cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelInferenceExecutionConfig]:
        return typing.cast(typing.Optional[SagemakerModelInferenceExecutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelInferenceExecutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df681990093f93fc138efe7050bef8e156c432073edca6e7a7122058ab496b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainer",
    jsii_struct_bases=[],
    name_mapping={
        "additional_model_data_source": "additionalModelDataSource",
        "container_hostname": "containerHostname",
        "environment": "environment",
        "image": "image",
        "image_config": "imageConfig",
        "inference_specification_name": "inferenceSpecificationName",
        "mode": "mode",
        "model_data_source": "modelDataSource",
        "model_data_url": "modelDataUrl",
        "model_package_name": "modelPackageName",
        "multi_model_config": "multiModelConfig",
    },
)
class SagemakerModelPrimaryContainer:
    def __init__(
        self,
        *,
        additional_model_data_source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelPrimaryContainerAdditionalModelDataSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        container_hostname: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inference_specification_name: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        model_data_source: typing.Optional[typing.Union["SagemakerModelPrimaryContainerModelDataSource", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_url: typing.Optional[builtins.str] = None,
        model_package_name: typing.Optional[builtins.str] = None,
        multi_model_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerMultiModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_model_data_source: additional_model_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#additional_model_data_source SagemakerModel#additional_model_data_source}
        :param container_hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container_hostname SagemakerModel#container_hostname}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#environment SagemakerModel#environment}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image SagemakerModel#image}.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image_config SagemakerModel#image_config}
        :param inference_specification_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_specification_name SagemakerModel#inference_specification_name}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.
        :param model_data_source: model_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_source SagemakerModel#model_data_source}
        :param model_data_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_url SagemakerModel#model_data_url}.
        :param model_package_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_package_name SagemakerModel#model_package_name}.
        :param multi_model_config: multi_model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#multi_model_config SagemakerModel#multi_model_config}
        '''
        if isinstance(image_config, dict):
            image_config = SagemakerModelPrimaryContainerImageConfig(**image_config)
        if isinstance(model_data_source, dict):
            model_data_source = SagemakerModelPrimaryContainerModelDataSource(**model_data_source)
        if isinstance(multi_model_config, dict):
            multi_model_config = SagemakerModelPrimaryContainerMultiModelConfig(**multi_model_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65caec35c880e7284ac695ae649d754801a853d240863f27fab55a5f29d0394)
            check_type(argname="argument additional_model_data_source", value=additional_model_data_source, expected_type=type_hints["additional_model_data_source"])
            check_type(argname="argument container_hostname", value=container_hostname, expected_type=type_hints["container_hostname"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument inference_specification_name", value=inference_specification_name, expected_type=type_hints["inference_specification_name"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument model_data_source", value=model_data_source, expected_type=type_hints["model_data_source"])
            check_type(argname="argument model_data_url", value=model_data_url, expected_type=type_hints["model_data_url"])
            check_type(argname="argument model_package_name", value=model_package_name, expected_type=type_hints["model_package_name"])
            check_type(argname="argument multi_model_config", value=multi_model_config, expected_type=type_hints["multi_model_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_model_data_source is not None:
            self._values["additional_model_data_source"] = additional_model_data_source
        if container_hostname is not None:
            self._values["container_hostname"] = container_hostname
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if image_config is not None:
            self._values["image_config"] = image_config
        if inference_specification_name is not None:
            self._values["inference_specification_name"] = inference_specification_name
        if mode is not None:
            self._values["mode"] = mode
        if model_data_source is not None:
            self._values["model_data_source"] = model_data_source
        if model_data_url is not None:
            self._values["model_data_url"] = model_data_url
        if model_package_name is not None:
            self._values["model_package_name"] = model_package_name
        if multi_model_config is not None:
            self._values["multi_model_config"] = multi_model_config

    @builtins.property
    def additional_model_data_source(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerAdditionalModelDataSource"]]]:
        '''additional_model_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#additional_model_data_source SagemakerModel#additional_model_data_source}
        '''
        result = self._values.get("additional_model_data_source")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerAdditionalModelDataSource"]]], result)

    @builtins.property
    def container_hostname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#container_hostname SagemakerModel#container_hostname}.'''
        result = self._values.get("container_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#environment SagemakerModel#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image SagemakerModel#image}.'''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerImageConfig"]:
        '''image_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#image_config SagemakerModel#image_config}
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerImageConfig"], result)

    @builtins.property
    def inference_specification_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#inference_specification_name SagemakerModel#inference_specification_name}.'''
        result = self._values.get("inference_specification_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#mode SagemakerModel#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_data_source(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerModelDataSource"]:
        '''model_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_source SagemakerModel#model_data_source}
        '''
        result = self._values.get("model_data_source")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerModelDataSource"], result)

    @builtins.property
    def model_data_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_data_url SagemakerModel#model_data_url}.'''
        result = self._values.get("model_data_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_package_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_package_name SagemakerModel#model_package_name}.'''
        result = self._values.get("model_package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_model_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerMultiModelConfig"]:
        '''multi_model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#multi_model_config SagemakerModel#multi_model_config}
        '''
        result = self._values.get("multi_model_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerMultiModelConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSource",
    jsii_struct_bases=[],
    name_mapping={"channel_name": "channelName", "s3_data_source": "s3DataSource"},
)
class SagemakerModelPrimaryContainerAdditionalModelDataSource:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#channel_name SagemakerModel#channel_name}.
        :param s3_data_source: s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb410a41441c77b78c65802c6687e11f036464f6295e3572eaf754b2e109022)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_name": channel_name,
            "s3_data_source": s3_data_source,
        }

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#channel_name SagemakerModel#channel_name}.'''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_data_source(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource"]]:
        '''s3_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        result = self._values.get("s3_data_source")
        assert result is not None, "Required property 's3_data_source' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerAdditionalModelDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerAdditionalModelDataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea487d46d462d08781f68052109c6a79d3a3dd70283270e5eae5fef7f13801f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerModelPrimaryContainerAdditionalModelDataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518e19d83dd265b13cca2e52291f7ff5e959533f66c70b717628b084a04e78c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelPrimaryContainerAdditionalModelDataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a761e1ddbc008ce098aad34d8fb2756900dde405c9ff5d52fc3c687917a60cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f228529ba1f68a0e42a5f9f4ba5c01096439689dc9e47733446984457159f3c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3fc82f3f261cf15ca152c1914410485dee9ae9ba397b353ed8d88d3d5992bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fed100656403c6ee0ce9e89a1046dd509aff799be7a09331ebd8cd453d74137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelPrimaryContainerAdditionalModelDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3955dd871526637ea9bb2d9d62f102eacbf4f1bbb774a7302fe97ebb361e820)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putS3DataSource")
    def put_s3_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e03533c212748a827241c002b954d3b8d897fd981e6f2aa3089f2caaca0608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3DataSource", [value]))

    @builtins.property
    @jsii.member(jsii_name="s3DataSource")
    def s3_data_source(
        self,
    ) -> "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceList":
        return typing.cast("SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceList", jsii.get(self, "s3DataSource"))

    @builtins.property
    @jsii.member(jsii_name="channelNameInput")
    def channel_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataSourceInput")
    def s3_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource"]]], jsii.get(self, "s3DataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13b55f8e9d269e7d6f68364b7fb0f774febd60bdf9deb3c40151c79561e3575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa6bff2d4dc564ab3a3b343e1ea0bfc5bf2d1dbbbf326f8d3afedc263bb0252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "compression_type": "compressionType",
        "s3_data_type": "s3DataType",
        "s3_uri": "s3Uri",
        "model_access_config": "modelAccessConfig",
    },
)
class SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource:
    def __init__(
        self,
        *,
        compression_type: builtins.str,
        s3_data_type: builtins.str,
        s3_uri: builtins.str,
        model_access_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.
        :param s3_data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.
        :param model_access_config: model_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        if isinstance(model_access_config, dict):
            model_access_config = SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig(**model_access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5be10226f3991290bcb5b8985125a6bc3e4f7732e81612542dfd77acc6386e)
            check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
            check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument model_access_config", value=model_access_config, expected_type=type_hints["model_access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression_type": compression_type,
            "s3_data_type": s3_data_type,
            "s3_uri": s3_uri,
        }
        if model_access_config is not None:
            self._values["model_access_config"] = model_access_config

    @builtins.property
    def compression_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.'''
        result = self._values.get("compression_type")
        assert result is not None, "Required property 'compression_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_data_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.'''
        result = self._values.get("s3_data_type")
        assert result is not None, "Required property 's3_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_access_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig"]:
        '''model_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        result = self._values.get("model_access_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24aa49018fb9a9fb24218d3072930a52452d19e91c396a744d6207481401aa3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53b87aee564e3dbae118ea73103e3db01b6fc51a39a2b6e83f0e14296df5893)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47222c20620443098db6babb90e42aab167b34c29d09f0aabdfaac3c3326ded3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6c667a03d2050ddd571e4fe2f18f0eaaee083c6daeb5493e766ee2462e2205)
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
            type_hints = typing.get_type_hints(_typecheckingstub__464392d42aac691c7c0b2fad98c1218832b1166e5e89e5eda3845fb4194eae18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb11e4ea424666c4c1af6e900c1f60f687347690866c17d3e5498216c49bc66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"accept_eula": "acceptEula"},
)
class SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig:
    def __init__(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814ea1a9b82955c5958a7ca62a6d485d7fac316c05f5f472471212e2f0c6c100)
            check_type(argname="argument accept_eula", value=accept_eula, expected_type=type_hints["accept_eula"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accept_eula": accept_eula,
        }

    @builtins.property
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.'''
        result = self._values.get("accept_eula")
        assert result is not None, "Required property 'accept_eula' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a8f64b2b47106dc023ba08803f93726458f17113d402d2a626790c1900a867c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="acceptEulaInput")
    def accept_eula_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptEulaInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptEula")
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptEula"))

    @accept_eula.setter
    def accept_eula(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e93f2507117d73f97f4c7a9d944431f9c78f1fb94dee84d5e8e8f954881703c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptEula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10501486bcbdc71f834f46c8590ed09183ec6036a5f569199d7ba790918c25ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98587e743a0a049eab81321849657ef9a3e041f6f3b6a72836ec26faf71baa77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putModelAccessConfig")
    def put_model_access_config(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        value = SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig(
            accept_eula=accept_eula
        )

        return typing.cast(None, jsii.invoke(self, "putModelAccessConfig", [value]))

    @jsii.member(jsii_name="resetModelAccessConfig")
    def reset_model_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelAccessConfig", []))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfig")
    def model_access_config(
        self,
    ) -> SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference:
        return typing.cast(SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference, jsii.get(self, "modelAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="compressionTypeInput")
    def compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfigInput")
    def model_access_config_input(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "modelAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataTypeInput")
    def s3_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionType")
    def compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionType"))

    @compression_type.setter
    def compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c33ed4bcd67940dbb57b2364b7d3cfe3a76cb8bd5175c656c3b6bd2799982b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataType")
    def s3_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataType"))

    @s3_data_type.setter
    def s3_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0689bb08d790d5ade280dca8b47eec8f29713da08db074fabd271b890400ece7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef6f94d260407f0ae864a8dcf597b3a26cd17eff3c5d65be12ef3bfc0c0f2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278c851cf8a02a416b930c366f5d751c263efe912e045d2786ab97ef9f63953d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_access_mode": "repositoryAccessMode",
        "repository_auth_config": "repositoryAuthConfig",
    },
)
class SagemakerModelPrimaryContainerImageConfig:
    def __init__(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        if isinstance(repository_auth_config, dict):
            repository_auth_config = SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig(**repository_auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba222d19db627ec3464af31af37e699f7c72e08a583e5a2e14387038d46e1b7)
            check_type(argname="argument repository_access_mode", value=repository_access_mode, expected_type=type_hints["repository_access_mode"])
            check_type(argname="argument repository_auth_config", value=repository_auth_config, expected_type=type_hints["repository_auth_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_access_mode": repository_access_mode,
        }
        if repository_auth_config is not None:
            self._values["repository_auth_config"] = repository_auth_config

    @builtins.property
    def repository_access_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.'''
        result = self._values.get("repository_access_mode")
        assert result is not None, "Required property 'repository_access_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_auth_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"]:
        '''repository_auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        result = self._values.get("repository_auth_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerImageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__904047d5b6c14390e8c9ed92def129aa739563659cbd61f1d8f62732d59ff106)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepositoryAuthConfig")
    def put_repository_auth_config(
        self,
        *,
        repository_credentials_provider_arn: builtins.str,
    ) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        value = SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig(
            repository_credentials_provider_arn=repository_credentials_provider_arn
        )

        return typing.cast(None, jsii.invoke(self, "putRepositoryAuthConfig", [value]))

    @jsii.member(jsii_name="resetRepositoryAuthConfig")
    def reset_repository_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryAuthConfig", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfig")
    def repository_auth_config(
        self,
    ) -> "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference":
        return typing.cast("SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference", jsii.get(self, "repositoryAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessModeInput")
    def repository_access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryAccessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfigInput")
    def repository_auth_config_input(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"]:
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"], jsii.get(self, "repositoryAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessMode")
    def repository_access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryAccessMode"))

    @repository_access_mode.setter
    def repository_access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737403acd806690a1c3b6bf4c8e631d6c601bceb288beb7450ad02d618c7149a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryAccessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerImageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerImageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9babdafc0450afd11ef1f7d492ad2edb91741ccb07622e7ef9660f9d8642c037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_credentials_provider_arn": "repositoryCredentialsProviderArn",
    },
)
class SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig:
    def __init__(self, *, repository_credentials_provider_arn: builtins.str) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e50067a06ed2e699693f1f2d7ea5b9045acfb6b94772aed1d866b007b33ed0)
            check_type(argname="argument repository_credentials_provider_arn", value=repository_credentials_provider_arn, expected_type=type_hints["repository_credentials_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_credentials_provider_arn": repository_credentials_provider_arn,
        }

    @builtins.property
    def repository_credentials_provider_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.'''
        result = self._values.get("repository_credentials_provider_arn")
        assert result is not None, "Required property 'repository_credentials_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c42f4882902f2e2164b4d3ea4f56bd9b350f3a9e1ed7eecd36db27c1cee7b9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArnInput")
    def repository_credentials_provider_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCredentialsProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArn")
    def repository_credentials_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCredentialsProviderArn"))

    @repository_credentials_provider_arn.setter
    def repository_credentials_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05de01a823c52bb5173c5dbe1769d166cf6e3dac40d18d87efa52c428c58ee10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCredentialsProviderArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1bd16be552c684ccb47a34e268a8448d36d2abb48ad7095ee17092b3d890569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSource",
    jsii_struct_bases=[],
    name_mapping={"s3_data_source": "s3DataSource"},
)
class SagemakerModelPrimaryContainerModelDataSource:
    def __init__(
        self,
        *,
        s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelPrimaryContainerModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param s3_data_source: s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79210c72c78860aeef24db1c1388f72897b0540536d65aaf943acc6c61957ec5)
            check_type(argname="argument s3_data_source", value=s3_data_source, expected_type=type_hints["s3_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_data_source": s3_data_source,
        }

    @builtins.property
    def s3_data_source(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerModelDataSourceS3DataSource"]]:
        '''s3_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        result = self._values.get("s3_data_source")
        assert result is not None, "Required property 's3_data_source' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerModelDataSourceS3DataSource"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerModelDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerModelDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3198c35a5f807fa603300a38a1d768bb2f0ee79a84d59f0cfbb5d1179af961f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3DataSource")
    def put_s3_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelPrimaryContainerModelDataSourceS3DataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87881c1e31b0c13631b1e726b7dba07650d20dd13ff2b86f0cea8791721334cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3DataSource", [value]))

    @builtins.property
    @jsii.member(jsii_name="s3DataSource")
    def s3_data_source(
        self,
    ) -> "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceList":
        return typing.cast("SagemakerModelPrimaryContainerModelDataSourceS3DataSourceList", jsii.get(self, "s3DataSource"))

    @builtins.property
    @jsii.member(jsii_name="s3DataSourceInput")
    def s3_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerModelDataSourceS3DataSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelPrimaryContainerModelDataSourceS3DataSource"]]], jsii.get(self, "s3DataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerModelDataSource]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerModelDataSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerModelDataSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2f3b3bd2f7db2a9c4aab33fc11f18e469179b93a7c67a0521f75858037f8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSourceS3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "compression_type": "compressionType",
        "s3_data_type": "s3DataType",
        "s3_uri": "s3Uri",
        "model_access_config": "modelAccessConfig",
    },
)
class SagemakerModelPrimaryContainerModelDataSourceS3DataSource:
    def __init__(
        self,
        *,
        compression_type: builtins.str,
        s3_data_type: builtins.str,
        s3_uri: builtins.str,
        model_access_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.
        :param s3_data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.
        :param model_access_config: model_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        if isinstance(model_access_config, dict):
            model_access_config = SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig(**model_access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb286b44ffb323c68560c2dba9cefd9882e3ace5bcda6a327dd907db878f4953)
            check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
            check_type(argname="argument s3_data_type", value=s3_data_type, expected_type=type_hints["s3_data_type"])
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument model_access_config", value=model_access_config, expected_type=type_hints["model_access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compression_type": compression_type,
            "s3_data_type": s3_data_type,
            "s3_uri": s3_uri,
        }
        if model_access_config is not None:
            self._values["model_access_config"] = model_access_config

    @builtins.property
    def compression_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#compression_type SagemakerModel#compression_type}.'''
        result = self._values.get("compression_type")
        assert result is not None, "Required property 'compression_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_data_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_type SagemakerModel#s3_data_type}.'''
        result = self._values.get("s3_data_type")
        assert result is not None, "Required property 's3_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_uri SagemakerModel#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_access_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig"]:
        '''model_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_access_config SagemakerModel#model_access_config}
        '''
        result = self._values.get("model_access_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerModelDataSourceS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerModelDataSourceS3DataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSourceS3DataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b83103b0609736a36f84cb94c36a0839e268f3f7c752a7a3644cb5ea49819e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6006474eed0ed54764e34baaf17a0a5296683803710fdfc236054a7fdd7aab8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelPrimaryContainerModelDataSourceS3DataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7cc1e673ccb37dc5ddcc22ab946b2849ec83c1045fe7d3c652e8c5829fe2cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__215a8f0d558291755b1238ea5dc7d0dc3b7c9f82639990d8293b5fcbe25eaaa6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b0ddc0902a3546b753b9cf388b4dcfe0ca97f2751efc0f041dc781de8666be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerModelDataSourceS3DataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerModelDataSourceS3DataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerModelDataSourceS3DataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04025f41e365d92b6ff519b804a1a5b06b6a92a6f06d546ee9b1d40f3aa01b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"accept_eula": "acceptEula"},
)
class SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig:
    def __init__(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85bd64afbfaf9ff63ac2838fa9fade9eb0934cd48d98c4c2000c7a5a437b17c)
            check_type(argname="argument accept_eula", value=accept_eula, expected_type=type_hints["accept_eula"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accept_eula": accept_eula,
        }

    @builtins.property
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.'''
        result = self._values.get("accept_eula")
        assert result is not None, "Required property 'accept_eula' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__166d6fd827e9105d21c39fbf80804d931134f38b4979650dae4c029135c93e21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="acceptEulaInput")
    def accept_eula_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptEulaInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptEula")
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptEula"))

    @accept_eula.setter
    def accept_eula(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b709ff23f385de0e2751a7ebb08b3dd0c010e5dfee6accd59e085cb6d87f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptEula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937a4a606cf7ca108b64730f445d5815312eae786df0107a45873dc447fd3e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelPrimaryContainerModelDataSourceS3DataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerModelDataSourceS3DataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c10f6919f7c208987dbfdd085f77811dc7e98ac767c05564d0b2fda44c7fb138)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putModelAccessConfig")
    def put_model_access_config(
        self,
        *,
        accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param accept_eula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#accept_eula SagemakerModel#accept_eula}.
        '''
        value = SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig(
            accept_eula=accept_eula
        )

        return typing.cast(None, jsii.invoke(self, "putModelAccessConfig", [value]))

    @jsii.member(jsii_name="resetModelAccessConfig")
    def reset_model_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelAccessConfig", []))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfig")
    def model_access_config(
        self,
    ) -> SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference:
        return typing.cast(SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference, jsii.get(self, "modelAccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="compressionTypeInput")
    def compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelAccessConfigInput")
    def model_access_config_input(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig], jsii.get(self, "modelAccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataTypeInput")
    def s3_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionType")
    def compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionType"))

    @compression_type.setter
    def compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3dd1ab7c27d3a5479afc6537137bdaf1118d3225c0870017d5369ed96c87b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataType")
    def s3_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataType"))

    @s3_data_type.setter
    def s3_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344066830af4cf4612788be72f746ea663a6b857d444a2dfd5a1138e15cbaac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b49e4045fe317384810917b10f265cd4b7a3d26ad79a7ffd987e0c32bf588dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerModelDataSourceS3DataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerModelDataSourceS3DataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerModelDataSourceS3DataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b30cceebcbcdcc82b5920b2bc83103943f285de88f44596e118cbce1c4ca51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerMultiModelConfig",
    jsii_struct_bases=[],
    name_mapping={"model_cache_setting": "modelCacheSetting"},
)
class SagemakerModelPrimaryContainerMultiModelConfig:
    def __init__(
        self,
        *,
        model_cache_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model_cache_setting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_cache_setting SagemakerModel#model_cache_setting}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a9718b1e7daf3475b408cab07d2ee89f349bb0b8d7974991b1b3f379711253)
            check_type(argname="argument model_cache_setting", value=model_cache_setting, expected_type=type_hints["model_cache_setting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if model_cache_setting is not None:
            self._values["model_cache_setting"] = model_cache_setting

    @builtins.property
    def model_cache_setting(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_cache_setting SagemakerModel#model_cache_setting}.'''
        result = self._values.get("model_cache_setting")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerMultiModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerMultiModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerMultiModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e15be38a3888392f59c7d020002e164890539f7a445f0f8df2c68587765d319)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModelCacheSetting")
    def reset_model_cache_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelCacheSetting", []))

    @builtins.property
    @jsii.member(jsii_name="modelCacheSettingInput")
    def model_cache_setting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelCacheSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="modelCacheSetting")
    def model_cache_setting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelCacheSetting"))

    @model_cache_setting.setter
    def model_cache_setting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b903dc9671a9f7bca95440254b12bbd67ea0622f89f6f5d46bc3289284ec4601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelCacheSetting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerMultiModelConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerMultiModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerMultiModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c96377db38cfbaa125ba310d666bda7b7176d7ad10343294bbfce2e6b3d1106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerModelPrimaryContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67bb061bf42d20f2d39bb0b536417a39ffda4fe44b653515a27d1c184de99e5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalModelDataSource")
    def put_additional_model_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerAdditionalModelDataSource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6106c7f2e48618c3c5809ec4828e0b7f7c095ab06f83a4439df65880ed6a99fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalModelDataSource", [value]))

    @jsii.member(jsii_name="putImageConfig")
    def put_image_config(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        value = SagemakerModelPrimaryContainerImageConfig(
            repository_access_mode=repository_access_mode,
            repository_auth_config=repository_auth_config,
        )

        return typing.cast(None, jsii.invoke(self, "putImageConfig", [value]))

    @jsii.member(jsii_name="putModelDataSource")
    def put_model_data_source(
        self,
        *,
        s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param s3_data_source: s3_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#s3_data_source SagemakerModel#s3_data_source}
        '''
        value = SagemakerModelPrimaryContainerModelDataSource(
            s3_data_source=s3_data_source
        )

        return typing.cast(None, jsii.invoke(self, "putModelDataSource", [value]))

    @jsii.member(jsii_name="putMultiModelConfig")
    def put_multi_model_config(
        self,
        *,
        model_cache_setting: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model_cache_setting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#model_cache_setting SagemakerModel#model_cache_setting}.
        '''
        value = SagemakerModelPrimaryContainerMultiModelConfig(
            model_cache_setting=model_cache_setting
        )

        return typing.cast(None, jsii.invoke(self, "putMultiModelConfig", [value]))

    @jsii.member(jsii_name="resetAdditionalModelDataSource")
    def reset_additional_model_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalModelDataSource", []))

    @jsii.member(jsii_name="resetContainerHostname")
    def reset_container_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerHostname", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetImageConfig")
    def reset_image_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfig", []))

    @jsii.member(jsii_name="resetInferenceSpecificationName")
    def reset_inference_specification_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceSpecificationName", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetModelDataSource")
    def reset_model_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataSource", []))

    @jsii.member(jsii_name="resetModelDataUrl")
    def reset_model_data_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataUrl", []))

    @jsii.member(jsii_name="resetModelPackageName")
    def reset_model_package_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelPackageName", []))

    @jsii.member(jsii_name="resetMultiModelConfig")
    def reset_multi_model_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiModelConfig", []))

    @builtins.property
    @jsii.member(jsii_name="additionalModelDataSource")
    def additional_model_data_source(
        self,
    ) -> SagemakerModelPrimaryContainerAdditionalModelDataSourceList:
        return typing.cast(SagemakerModelPrimaryContainerAdditionalModelDataSourceList, jsii.get(self, "additionalModelDataSource"))

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(self) -> SagemakerModelPrimaryContainerImageConfigOutputReference:
        return typing.cast(SagemakerModelPrimaryContainerImageConfigOutputReference, jsii.get(self, "imageConfig"))

    @builtins.property
    @jsii.member(jsii_name="modelDataSource")
    def model_data_source(
        self,
    ) -> SagemakerModelPrimaryContainerModelDataSourceOutputReference:
        return typing.cast(SagemakerModelPrimaryContainerModelDataSourceOutputReference, jsii.get(self, "modelDataSource"))

    @builtins.property
    @jsii.member(jsii_name="multiModelConfig")
    def multi_model_config(
        self,
    ) -> SagemakerModelPrimaryContainerMultiModelConfigOutputReference:
        return typing.cast(SagemakerModelPrimaryContainerMultiModelConfigOutputReference, jsii.get(self, "multiModelConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalModelDataSourceInput")
    def additional_model_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSource]]], jsii.get(self, "additionalModelDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="containerHostnameInput")
    def container_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigInput")
    def image_config_input(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerImageConfig], jsii.get(self, "imageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceSpecificationNameInput")
    def inference_specification_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceSpecificationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataSourceInput")
    def model_data_source_input(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerModelDataSource]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerModelDataSource], jsii.get(self, "modelDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataUrlInput")
    def model_data_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelDataUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="modelPackageNameInput")
    def model_package_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelPackageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="multiModelConfigInput")
    def multi_model_config_input(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerMultiModelConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerMultiModelConfig], jsii.get(self, "multiModelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="containerHostname")
    def container_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerHostname"))

    @container_hostname.setter
    def container_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4ed248e0049b33361b8b0c118d512f800bf33d7d18cbc5496e48b4fb138e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerHostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4bd5b5a3f34a7319cc953d38c62461ba7a76eb79c03b1b972ab0d312433724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b584e24c93f24031b8c0ffaebb17a247a0aa3bed855275f8a3945338ccda782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceSpecificationName")
    def inference_specification_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inferenceSpecificationName"))

    @inference_specification_name.setter
    def inference_specification_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a790166b4dde7c94184b1b5c7b42061f9c42f941ab47d5083f157d165c1ff9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceSpecificationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efccc8887c248f43adec61b5e0d780703e65d82fed51e55328719ba7faf42144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDataUrl")
    def model_data_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDataUrl"))

    @model_data_url.setter
    def model_data_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096b6109bd84be97324ec6bde583e616513129bc1ae11c296aa3d8c2247e908b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelPackageName")
    def model_package_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelPackageName"))

    @model_package_name.setter
    def model_package_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71770e4d080fba21093dfe5ebaf443e2a280894cf7a61cf26d528643e7f39594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelPackageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelPrimaryContainer]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd96ca158cd315bb78b01bfa3abb5e35c481fe827c88686ddf6fd118c3f2509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelVpcConfig",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnets": "subnets"},
)
class SagemakerModelVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#security_group_ids SagemakerModel#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#subnets SagemakerModel#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a3789ac6a79020c4dd5d6a4003e32be455c3c421364e8c7f8dc986cd114b72)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnets": subnets,
        }

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#security_group_ids SagemakerModel#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_model#subnets SagemakerModel#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerModel.SagemakerModelVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1d63c9f27142f055e8da41332488b96dd8f9895f9df3f9452d54bed26075e96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee92d712d1d9a11ec0696a6454e25d4e11a212ca56fab3f237fc4eda526e797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa5469638f562680aae5c3a9857aeecda6232bab2914bac383d8a95022f8b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelVpcConfig]:
        return typing.cast(typing.Optional[SagemakerModelVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SagemakerModelVpcConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c192fbab2ecc0deb5f4b13bc4873492948b8d664317f2492fe56c8a30a6ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerModel",
    "SagemakerModelConfig",
    "SagemakerModelContainer",
    "SagemakerModelContainerAdditionalModelDataSource",
    "SagemakerModelContainerAdditionalModelDataSourceList",
    "SagemakerModelContainerAdditionalModelDataSourceOutputReference",
    "SagemakerModelContainerAdditionalModelDataSourceS3DataSource",
    "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceList",
    "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig",
    "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference",
    "SagemakerModelContainerAdditionalModelDataSourceS3DataSourceOutputReference",
    "SagemakerModelContainerImageConfig",
    "SagemakerModelContainerImageConfigOutputReference",
    "SagemakerModelContainerImageConfigRepositoryAuthConfig",
    "SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference",
    "SagemakerModelContainerList",
    "SagemakerModelContainerModelDataSource",
    "SagemakerModelContainerModelDataSourceOutputReference",
    "SagemakerModelContainerModelDataSourceS3DataSource",
    "SagemakerModelContainerModelDataSourceS3DataSourceList",
    "SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig",
    "SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference",
    "SagemakerModelContainerModelDataSourceS3DataSourceOutputReference",
    "SagemakerModelContainerMultiModelConfig",
    "SagemakerModelContainerMultiModelConfigOutputReference",
    "SagemakerModelContainerOutputReference",
    "SagemakerModelInferenceExecutionConfig",
    "SagemakerModelInferenceExecutionConfigOutputReference",
    "SagemakerModelPrimaryContainer",
    "SagemakerModelPrimaryContainerAdditionalModelDataSource",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceList",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceOutputReference",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceList",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfigOutputReference",
    "SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceOutputReference",
    "SagemakerModelPrimaryContainerImageConfig",
    "SagemakerModelPrimaryContainerImageConfigOutputReference",
    "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig",
    "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference",
    "SagemakerModelPrimaryContainerModelDataSource",
    "SagemakerModelPrimaryContainerModelDataSourceOutputReference",
    "SagemakerModelPrimaryContainerModelDataSourceS3DataSource",
    "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceList",
    "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig",
    "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfigOutputReference",
    "SagemakerModelPrimaryContainerModelDataSourceS3DataSourceOutputReference",
    "SagemakerModelPrimaryContainerMultiModelConfig",
    "SagemakerModelPrimaryContainerMultiModelConfigOutputReference",
    "SagemakerModelPrimaryContainerOutputReference",
    "SagemakerModelVpcConfig",
    "SagemakerModelVpcConfigOutputReference",
]

publication.publish()

def _typecheckingstub__fc992f0e8277e59cc21fe09f24993030ab291c74c4cbeb6771a34ad34202211f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    execution_role_arn: builtins.str,
    container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    inference_execution_config: typing.Optional[typing.Union[SagemakerModelInferenceExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    primary_container: typing.Optional[typing.Union[SagemakerModelPrimaryContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[SagemakerModelVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__545e2a3b0e25cf4905a61259ba51df2a4edd9a1c4e9c0eb6a88dc01d650e8f02(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c0d41d1c1fa9712698bbb9f68a6b782bc57a9090fea3ca014996cb25c48aad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8d68503b43076392be58d3fdc26f3fee2ff94f9346df76cfbbb5e6936952bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ecf523ba1b3fb06054b71d7435f79cb9760d2d8a3d9a80697e603ce87d388e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b02152f71f13a7f7d3cbcf37087146c08bd4288889830a95389f0af0e43370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f7fc929a5c1efc92cb217b0816c110f660b2f529de901b3b2cd65e2d4ea11b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ddb6b82e55639260630dab7e22a1945f6fb1cefa3e0ea619fcb8c8d82612f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4103bd20fbbd75687be453db8e83eafef84d5485d0c67baf5db66632d8a6b458(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ce273f514dec9d8f7e8b1ca34d921c72033b4aa00c561f6662913f6e50fcfa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8783df7ef7c4a0999f4e94071bf08fe6eeaa7070e4f39d226c81c727fd864cca(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    execution_role_arn: builtins.str,
    container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    inference_execution_config: typing.Optional[typing.Union[SagemakerModelInferenceExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    primary_container: typing.Optional[typing.Union[SagemakerModelPrimaryContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[SagemakerModelVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6d44aaff424faedd9b53588d6bcf4422f3d354020f603b42a4d06a0fe1f4f8(
    *,
    additional_model_data_source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerAdditionalModelDataSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_hostname: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[SagemakerModelContainerImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inference_specification_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    model_data_source: typing.Optional[typing.Union[SagemakerModelContainerModelDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    model_data_url: typing.Optional[builtins.str] = None,
    model_package_name: typing.Optional[builtins.str] = None,
    multi_model_config: typing.Optional[typing.Union[SagemakerModelContainerMultiModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36232968630ac85fb8076b0a1a66c057974ee6988ffc53f4af1323cee7a4ae58(
    *,
    channel_name: builtins.str,
    s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerAdditionalModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb3f918717b1846395a0fae86146b31172298fb434b83c03404f004a2980282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd940abf481f6ecf0a92010f7f02d8065eaafdc48b9c5e8935b79e93b03cad64(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a601bb08d2f21716cca976317f39495ac86ecbd1d9a5f23dc20bee1eb94b2d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7614e95d1089e45fefdec7fb31a28c4f4835b8e1a466a7460af5ba14b0793489(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd6d1501756299d9a337f853aee7ff6466ef88b54b1996c643e002f775f99bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9974d10aee7b7a0861d9951df24d4878500cb8785427963f1f04c87e44b15fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6187f3a42e1455f71e60ba4ae9a9a0086115ecd985358c6b60c771cdfd019e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9d5dae47011c221ca6e763e013a6e5def707519eb0a55f7300f668e68e3985(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerAdditionalModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73cfab283a6323d7667c7ed05a813ebf48d4f292cf74eba7b659b3eacb5a94d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ebffee651505f6da68488abea44378dadf0a9e0802c560e5274d8849ed7005(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75915e58f59d07124d49746f946f0ecc902e7985e3ef732e257a2090c4024246(
    *,
    compression_type: builtins.str,
    s3_data_type: builtins.str,
    s3_uri: builtins.str,
    model_access_config: typing.Optional[typing.Union[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f4ca8b7f13fd43dfefd57d0bb0b248fe3d2d7b4c9d1ced59e894bcf71bffa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33412c2afa8256613465b69652e58dffe8eb337bc2eb05d38ddb50a139f561cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c64af59f58f0be83d75c3ab09b35535d343d3061d4498ff68ea40f3d6eafce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad5c64ab1c26ff1e9d68afb144e56dfed7dd9376c4a9f3c520b524c0db3612b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62baf1fff924931a486a5f14fd2ac47bb7dd13802ddeb7fbeeebb01bcfa8cb0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b63e0392b563612b4ac9ff9e814737c06eefbf7aedffdae33e4ecdc58f6315(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerAdditionalModelDataSourceS3DataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac35ad7a151c870e46b632a8de2632b8004f53ba8569b2eba49b77390cccf3b9(
    *,
    accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a25d74f00397ced13150e46cf1ab5327e30163ad0ce4246d24dcef81c0ee901(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc08e3df3484b11e53534a8a4df7f511f9d65188ab14f314118d3e3a294df1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35236ff5db627b0bc168f30e7b9773722c83cb1eca2aeb5607de249a8f7af798(
    value: typing.Optional[SagemakerModelContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9d64184d739d99d5f7848189081fc501ce69962cb63a4ae2ccb979408eca56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4899c4e6139dcb94cb7881ddbdace41e8ea9d53120ac485090d4d8814f578e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f22d18b1a2a8ce4240a27b0c50ff35db4a8b1fd680fee00f9c53447b447452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3378fea05dfa872d26bc185fb120f3487759d638c78543fd1b9a493ce9d59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96e6c349a26a48a899f12e8b5163339955b5d26fff29fda8db35cb2c8f4428c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerAdditionalModelDataSourceS3DataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a47c28b8f4753c4fcc68ca840f83e90b8600c667774c1e8de89bbe9fc7a98bf(
    *,
    repository_access_mode: builtins.str,
    repository_auth_config: typing.Optional[typing.Union[SagemakerModelContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6374e1067c22177648c957b66c2b17328beab73ea3d2ea721b8d28c035c8768(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c19932a6833906ed68e6b7e227d93cd5151a631f33d5f279bd506b058869bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16746e0a97613ea91d43a507c0d7cad0dc6f1d17375e78db578cd9451533e07b(
    value: typing.Optional[SagemakerModelContainerImageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c7c4ccfbe3284ec37540bffa54e6cacc719b82b02d199d75a5e824f9d5e34a(
    *,
    repository_credentials_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c220fafaf621742ade0dc652f43880ba2e41f07c2bd09c34eece7e4adcc7007d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a56d2f7eecfe330d0dc333a947d0dd1d30f74484375426e1bdd234e89638a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f11b6cb9d58bda004fa591a78569d32f6ce1aea5c9b1099f09697640cf7723(
    value: typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f083a5cb39f7a64c2f17aeca4e61317d2122b8c458362f20ce3cbb856b93a8be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef372e2d68a1ed8fe302e8887734b54a2d2e3c96492fecafa45b440212160933(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0729913b118bfe4cafb0de5d32de907092dac76a5bb2905b84f07f312b930f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962ab446c73cc5616f792bbea028d463bf07c8a631ffa62686d387b8a9c53900(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63db4acbac599a0abf0f741608b9bd2fc41f73f00461c166c209c92eadcca9c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2b3bc1e068fec0171294572c9afe08c2bd2d43df153e5a11f43c1d9184e36c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624c0fc420a6b78c0fc21d27c226fb683c3d781e15f54397b7865ad5f63ef8f0(
    *,
    s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba113b66b9f05cab2f4d622379df9d92ac59a4787ac669f0bc7a2ed0ad79c185(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f2ce9a8e9d97b18fc3720a9bf5afab663371b096b8254c04091a4d13a4ca17(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288ea51e5d2db803a8f0e10fe9b657ae76e00432b121f383bcc7a828a168ab00(
    value: typing.Optional[SagemakerModelContainerModelDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a75fc14d17be2c2692d7fadb286697b09473d7568d3dd6e4f86f6c4142f653(
    *,
    compression_type: builtins.str,
    s3_data_type: builtins.str,
    s3_uri: builtins.str,
    model_access_config: typing.Optional[typing.Union[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af036fe0c8720fea0825370ac2107e7319dd7b4d8140a2d0846ba44e829d3398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0075c2471ccab9403595507740b5b1b8c610085a4577353a14824e2606500245(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f23af1734c4a9bebc6097e1568c8d17ce5617b8495025630e97835b6a34db5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0797d7081abd1499ca4f437bf144eed0b21b7915efd4c309c6d1ef904e2eda12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70142a9eaad93df55304f042b6f1775f8e9140c601edcbf6af23bb977e7589c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52908c434422470876c4d6a42b3076a1d2ad6a46bef7d6de685a209d67de18a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainerModelDataSourceS3DataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842f0ff5b11209edd2b179b3c84d6252886bcf5a7cd8a0bf492c6b7cd0a764f2(
    *,
    accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635fa9fbe8c95c61b6255c81922158b5bf868e1670ba76c756ee57b46bbe538b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561ed446019cfa933fed1f7895f6132e056fe133837abf4f93e1772e7a86f3a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c30f4c00f33674288f13c06c90e1d341848f945c46d4b66523bf568d5f90ca(
    value: typing.Optional[SagemakerModelContainerModelDataSourceS3DataSourceModelAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec5aee46ee45614f81ebeb15aa5fa5620e062e265b1f20b6b6d1fc9312a2dc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70881edcc2043bda42e90dea9dea3b34af54c2e7ba63a5efe00fa5c818ddb90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808b8a38a446ec10252595f732e22cc8bbce9f9675c3d5f4177a87a1e0de8386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302a507e324d825e3364fc08d447ca1c428abcb569ee8f9bd2b672331dc4186f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca4933c1ffa2b078a616888d44d4173b164f47f64abc1981f6fccc57b72a220(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainerModelDataSourceS3DataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91020eb18bd7446d96ad621c73a425fa7c00e6f49df266e4ea9d4f5b9223930(
    *,
    model_cache_setting: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753543badcf1826f9f2ce9d90016f6abddaf0e69743e679537e343b60ef55858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496e104901cb587a9b4bca1e3a2eed6725bdd5dd08412e1eda2c3df7c59cbdfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb64361c1c1ee2cb4fa6524abe08c0c1c248cad3a4a7b20fecaec3012bf02a5(
    value: typing.Optional[SagemakerModelContainerMultiModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c9f960780075444cff802b5d51efa7cf0d5c7033e0c39c6a3295ee7bdb7485(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d96ffab10bd5c243eb8c87c48f5095b27c434083cc44cf07d97d35a827af30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainerAdditionalModelDataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab39ffcf98f43a73706797d66962726c247fc8c4aeced2a9760a4ff37e533252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c7ea3f4f6ac05473dfd819a247cde2428a978f3c7cad4a1a29cac4cd430850(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd8bf66c91b5bc51b359ab15e2535a6b51cc1b8d138a376ef3977e134b20d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9155fc4cbc87efc78aacb75eedb14e59aee1695c49a225c4dd4edc0763718704(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff29ad288011e63c6c3d65dc99bb072c7abe05145685f96d99c1be376f0cd21a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2445a188233d48ffe0fe39d01b419745c678bfb5fc09e7304a94eb7695f5eb69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df7d64529b4ef5093356c0f66d884976784aa603b6f9381538ef7c359c6b056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d12b183d2bb55eba64dd37dd5e8ca4aba8d91d487842e64c6cf80ea202dd716(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelContainer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a0764f69de895b19d113bc4402e50ad7aae2b46dc1d5cbfbf02e46d152b65e(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbc0daa23a907248d97f0df705588c9abf9e7898a3ec119784110d8f256ee6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41fbea755d30cc9bbe174271d126b6dc5c41b6d7c56bdda70e6637eef5b7cac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df681990093f93fc138efe7050bef8e156c432073edca6e7a7122058ab496b61(
    value: typing.Optional[SagemakerModelInferenceExecutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65caec35c880e7284ac695ae649d754801a853d240863f27fab55a5f29d0394(
    *,
    additional_model_data_source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerAdditionalModelDataSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_hostname: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inference_specification_name: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    model_data_source: typing.Optional[typing.Union[SagemakerModelPrimaryContainerModelDataSource, typing.Dict[builtins.str, typing.Any]]] = None,
    model_data_url: typing.Optional[builtins.str] = None,
    model_package_name: typing.Optional[builtins.str] = None,
    multi_model_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerMultiModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb410a41441c77b78c65802c6687e11f036464f6295e3572eaf754b2e109022(
    *,
    channel_name: builtins.str,
    s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea487d46d462d08781f68052109c6a79d3a3dd70283270e5eae5fef7f13801f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518e19d83dd265b13cca2e52291f7ff5e959533f66c70b717628b084a04e78c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a761e1ddbc008ce098aad34d8fb2756900dde405c9ff5d52fc3c687917a60cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f228529ba1f68a0e42a5f9f4ba5c01096439689dc9e47733446984457159f3c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fc82f3f261cf15ca152c1914410485dee9ae9ba397b353ed8d88d3d5992bc7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fed100656403c6ee0ce9e89a1046dd509aff799be7a09331ebd8cd453d74137(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3955dd871526637ea9bb2d9d62f102eacbf4f1bbb774a7302fe97ebb361e820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e03533c212748a827241c002b954d3b8d897fd981e6f2aa3089f2caaca0608(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13b55f8e9d269e7d6f68364b7fb0f774febd60bdf9deb3c40151c79561e3575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa6bff2d4dc564ab3a3b343e1ea0bfc5bf2d1dbbbf326f8d3afedc263bb0252(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5be10226f3991290bcb5b8985125a6bc3e4f7732e81612542dfd77acc6386e(
    *,
    compression_type: builtins.str,
    s3_data_type: builtins.str,
    s3_uri: builtins.str,
    model_access_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24aa49018fb9a9fb24218d3072930a52452d19e91c396a744d6207481401aa3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53b87aee564e3dbae118ea73103e3db01b6fc51a39a2b6e83f0e14296df5893(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47222c20620443098db6babb90e42aab167b34c29d09f0aabdfaac3c3326ded3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6c667a03d2050ddd571e4fe2f18f0eaaee083c6daeb5493e766ee2462e2205(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464392d42aac691c7c0b2fad98c1218832b1166e5e89e5eda3845fb4194eae18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb11e4ea424666c4c1af6e900c1f60f687347690866c17d3e5498216c49bc66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814ea1a9b82955c5958a7ca62a6d485d7fac316c05f5f472471212e2f0c6c100(
    *,
    accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8f64b2b47106dc023ba08803f93726458f17113d402d2a626790c1900a867c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e93f2507117d73f97f4c7a9d944431f9c78f1fb94dee84d5e8e8f954881703c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10501486bcbdc71f834f46c8590ed09183ec6036a5f569199d7ba790918c25ec(
    value: typing.Optional[SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSourceModelAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98587e743a0a049eab81321849657ef9a3e041f6f3b6a72836ec26faf71baa77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c33ed4bcd67940dbb57b2364b7d3cfe3a76cb8bd5175c656c3b6bd2799982b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0689bb08d790d5ade280dca8b47eec8f29713da08db074fabd271b890400ece7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef6f94d260407f0ae864a8dcf597b3a26cd17eff3c5d65be12ef3bfc0c0f2ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278c851cf8a02a416b930c366f5d751c263efe912e045d2786ab97ef9f63953d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerAdditionalModelDataSourceS3DataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba222d19db627ec3464af31af37e699f7c72e08a583e5a2e14387038d46e1b7(
    *,
    repository_access_mode: builtins.str,
    repository_auth_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904047d5b6c14390e8c9ed92def129aa739563659cbd61f1d8f62732d59ff106(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737403acd806690a1c3b6bf4c8e631d6c601bceb288beb7450ad02d618c7149a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9babdafc0450afd11ef1f7d492ad2edb91741ccb07622e7ef9660f9d8642c037(
    value: typing.Optional[SagemakerModelPrimaryContainerImageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e50067a06ed2e699693f1f2d7ea5b9045acfb6b94772aed1d866b007b33ed0(
    *,
    repository_credentials_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c42f4882902f2e2164b4d3ea4f56bd9b350f3a9e1ed7eecd36db27c1cee7b9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05de01a823c52bb5173c5dbe1769d166cf6e3dac40d18d87efa52c428c58ee10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bd16be552c684ccb47a34e268a8448d36d2abb48ad7095ee17092b3d890569(
    value: typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79210c72c78860aeef24db1c1388f72897b0540536d65aaf943acc6c61957ec5(
    *,
    s3_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3198c35a5f807fa603300a38a1d768bb2f0ee79a84d59f0cfbb5d1179af961f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87881c1e31b0c13631b1e726b7dba07650d20dd13ff2b86f0cea8791721334cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerModelDataSourceS3DataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2f3b3bd2f7db2a9c4aab33fc11f18e469179b93a7c67a0521f75858037f8e2(
    value: typing.Optional[SagemakerModelPrimaryContainerModelDataSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb286b44ffb323c68560c2dba9cefd9882e3ace5bcda6a327dd907db878f4953(
    *,
    compression_type: builtins.str,
    s3_data_type: builtins.str,
    s3_uri: builtins.str,
    model_access_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b83103b0609736a36f84cb94c36a0839e268f3f7c752a7a3644cb5ea49819e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6006474eed0ed54764e34baaf17a0a5296683803710fdfc236054a7fdd7aab8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7cc1e673ccb37dc5ddcc22ab946b2849ec83c1045fe7d3c652e8c5829fe2cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215a8f0d558291755b1238ea5dc7d0dc3b7c9f82639990d8293b5fcbe25eaaa6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0ddc0902a3546b753b9cf388b4dcfe0ca97f2751efc0f041dc781de8666be1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04025f41e365d92b6ff519b804a1a5b06b6a92a6f06d546ee9b1d40f3aa01b24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelPrimaryContainerModelDataSourceS3DataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85bd64afbfaf9ff63ac2838fa9fade9eb0934cd48d98c4c2000c7a5a437b17c(
    *,
    accept_eula: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166d6fd827e9105d21c39fbf80804d931134f38b4979650dae4c029135c93e21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b709ff23f385de0e2751a7ebb08b3dd0c010e5dfee6accd59e085cb6d87f4c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937a4a606cf7ca108b64730f445d5815312eae786df0107a45873dc447fd3e56(
    value: typing.Optional[SagemakerModelPrimaryContainerModelDataSourceS3DataSourceModelAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10f6919f7c208987dbfdd085f77811dc7e98ac767c05564d0b2fda44c7fb138(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3dd1ab7c27d3a5479afc6537137bdaf1118d3225c0870017d5369ed96c87b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344066830af4cf4612788be72f746ea663a6b857d444a2dfd5a1138e15cbaac5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b49e4045fe317384810917b10f265cd4b7a3d26ad79a7ffd987e0c32bf588dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b30cceebcbcdcc82b5920b2bc83103943f285de88f44596e118cbce1c4ca51(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerModelPrimaryContainerModelDataSourceS3DataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a9718b1e7daf3475b408cab07d2ee89f349bb0b8d7974991b1b3f379711253(
    *,
    model_cache_setting: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e15be38a3888392f59c7d020002e164890539f7a445f0f8df2c68587765d319(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b903dc9671a9f7bca95440254b12bbd67ea0622f89f6f5d46bc3289284ec4601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c96377db38cfbaa125ba310d666bda7b7176d7ad10343294bbfce2e6b3d1106(
    value: typing.Optional[SagemakerModelPrimaryContainerMultiModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bb061bf42d20f2d39bb0b536417a39ffda4fe44b653515a27d1c184de99e5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6106c7f2e48618c3c5809ec4828e0b7f7c095ab06f83a4439df65880ed6a99fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelPrimaryContainerAdditionalModelDataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4ed248e0049b33361b8b0c118d512f800bf33d7d18cbc5496e48b4fb138e8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4bd5b5a3f34a7319cc953d38c62461ba7a76eb79c03b1b972ab0d312433724(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b584e24c93f24031b8c0ffaebb17a247a0aa3bed855275f8a3945338ccda782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a790166b4dde7c94184b1b5c7b42061f9c42f941ab47d5083f157d165c1ff9b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efccc8887c248f43adec61b5e0d780703e65d82fed51e55328719ba7faf42144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096b6109bd84be97324ec6bde583e616513129bc1ae11c296aa3d8c2247e908b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71770e4d080fba21093dfe5ebaf443e2a280894cf7a61cf26d528643e7f39594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd96ca158cd315bb78b01bfa3abb5e35c481fe827c88686ddf6fd118c3f2509(
    value: typing.Optional[SagemakerModelPrimaryContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a3789ac6a79020c4dd5d6a4003e32be455c3c421364e8c7f8dc986cd114b72(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d63c9f27142f055e8da41332488b96dd8f9895f9df3f9452d54bed26075e96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee92d712d1d9a11ec0696a6454e25d4e11a212ca56fab3f237fc4eda526e797(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa5469638f562680aae5c3a9857aeecda6232bab2914bac383d8a95022f8b01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c192fbab2ecc0deb5f4b13bc4873492948b8d664317f2492fe56c8a30a6ed2(
    value: typing.Optional[SagemakerModelVpcConfig],
) -> None:
    """Type checking stubs"""
    pass
