r'''
# `aws_sagemaker_data_quality_job_definition`

Refer to the Terraform Registry for docs: [`aws_sagemaker_data_quality_job_definition`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition).
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


class SagemakerDataQualityJobDefinition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinition",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition aws_sagemaker_data_quality_job_definition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_quality_app_specification: typing.Union["SagemakerDataQualityJobDefinitionDataQualityAppSpecification", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_input: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInput", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_output_config: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig", typing.Dict[builtins.str, typing.Any]],
        job_resources: typing.Union["SagemakerDataQualityJobDefinitionJobResources", typing.Dict[builtins.str, typing.Any]],
        role_arn: builtins.str,
        data_quality_baseline_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        stopping_condition: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionStoppingCondition", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition aws_sagemaker_data_quality_job_definition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_quality_app_specification: data_quality_app_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_app_specification SagemakerDataQualityJobDefinition#data_quality_app_specification}
        :param data_quality_job_input: data_quality_job_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_input SagemakerDataQualityJobDefinition#data_quality_job_input}
        :param data_quality_job_output_config: data_quality_job_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_output_config SagemakerDataQualityJobDefinition#data_quality_job_output_config}
        :param job_resources: job_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#job_resources SagemakerDataQualityJobDefinition#job_resources}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#role_arn SagemakerDataQualityJobDefinition#role_arn}.
        :param data_quality_baseline_config: data_quality_baseline_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_baseline_config SagemakerDataQualityJobDefinition#data_quality_baseline_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#id SagemakerDataQualityJobDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#name SagemakerDataQualityJobDefinition#name}.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#network_config SagemakerDataQualityJobDefinition#network_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#region SagemakerDataQualityJobDefinition#region}
        :param stopping_condition: stopping_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#stopping_condition SagemakerDataQualityJobDefinition#stopping_condition}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#tags SagemakerDataQualityJobDefinition#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#tags_all SagemakerDataQualityJobDefinition#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa0cd1c3e8e97cc839c775a744dbb3b443516b515fa266b3513268452656f88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerDataQualityJobDefinitionConfig(
            data_quality_app_specification=data_quality_app_specification,
            data_quality_job_input=data_quality_job_input,
            data_quality_job_output_config=data_quality_job_output_config,
            job_resources=job_resources,
            role_arn=role_arn,
            data_quality_baseline_config=data_quality_baseline_config,
            id=id,
            name=name,
            network_config=network_config,
            region=region,
            stopping_condition=stopping_condition,
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
        '''Generates CDKTF code for importing a SagemakerDataQualityJobDefinition resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerDataQualityJobDefinition to import.
        :param import_from_id: The id of the existing SagemakerDataQualityJobDefinition that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerDataQualityJobDefinition to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b740ca9e42311cf9c986ed996898a1580b74da21467012733ceae31a87e870c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataQualityAppSpecification")
    def put_data_quality_app_specification(
        self,
        *,
        image_uri: builtins.str,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        post_analytics_processor_source_uri: typing.Optional[builtins.str] = None,
        record_preprocessor_source_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#image_uri SagemakerDataQualityJobDefinition#image_uri}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#environment SagemakerDataQualityJobDefinition#environment}.
        :param post_analytics_processor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#post_analytics_processor_source_uri SagemakerDataQualityJobDefinition#post_analytics_processor_source_uri}.
        :param record_preprocessor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#record_preprocessor_source_uri SagemakerDataQualityJobDefinition#record_preprocessor_source_uri}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityAppSpecification(
            image_uri=image_uri,
            environment=environment,
            post_analytics_processor_source_uri=post_analytics_processor_source_uri,
            record_preprocessor_source_uri=record_preprocessor_source_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityAppSpecification", [value]))

    @jsii.member(jsii_name="putDataQualityBaselineConfig")
    def put_data_quality_baseline_config(
        self,
        *,
        constraints_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource", typing.Dict[builtins.str, typing.Any]]] = None,
        statistics_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param constraints_resource: constraints_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#constraints_resource SagemakerDataQualityJobDefinition#constraints_resource}
        :param statistics_resource: statistics_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#statistics_resource SagemakerDataQualityJobDefinition#statistics_resource}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityBaselineConfig(
            constraints_resource=constraints_resource,
            statistics_resource=statistics_resource,
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityBaselineConfig", [value]))

    @jsii.member(jsii_name="putDataQualityJobInput")
    def put_data_quality_job_input(
        self,
        *,
        batch_transform_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_transform_input: batch_transform_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#batch_transform_input SagemakerDataQualityJobDefinition#batch_transform_input}
        :param endpoint_input: endpoint_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_input SagemakerDataQualityJobDefinition#endpoint_input}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInput(
            batch_transform_input=batch_transform_input, endpoint_input=endpoint_input
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityJobInput", [value]))

    @jsii.member(jsii_name="putDataQualityJobOutputConfig")
    def put_data_quality_job_output_config(
        self,
        *,
        monitoring_outputs: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs", typing.Dict[builtins.str, typing.Any]],
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param monitoring_outputs: monitoring_outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#monitoring_outputs SagemakerDataQualityJobDefinition#monitoring_outputs}
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#kms_key_id SagemakerDataQualityJobDefinition#kms_key_id}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig(
            monitoring_outputs=monitoring_outputs, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataQualityJobOutputConfig", [value]))

    @jsii.member(jsii_name="putJobResources")
    def put_job_resources(
        self,
        *,
        cluster_config: typing.Union["SagemakerDataQualityJobDefinitionJobResourcesClusterConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#cluster_config SagemakerDataQualityJobDefinition#cluster_config}
        '''
        value = SagemakerDataQualityJobDefinitionJobResources(
            cluster_config=cluster_config
        )

        return typing.cast(None, jsii.invoke(self, "putJobResources", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        enable_inter_container_traffic_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_inter_container_traffic_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#enable_inter_container_traffic_encryption SagemakerDataQualityJobDefinition#enable_inter_container_traffic_encryption}.
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#enable_network_isolation SagemakerDataQualityJobDefinition#enable_network_isolation}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#vpc_config SagemakerDataQualityJobDefinition#vpc_config}
        '''
        value = SagemakerDataQualityJobDefinitionNetworkConfig(
            enable_inter_container_traffic_encryption=enable_inter_container_traffic_encryption,
            enable_network_isolation=enable_network_isolation,
            vpc_config=vpc_config,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putStoppingCondition")
    def put_stopping_condition(
        self,
        *,
        max_runtime_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_runtime_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#max_runtime_in_seconds SagemakerDataQualityJobDefinition#max_runtime_in_seconds}.
        '''
        value = SagemakerDataQualityJobDefinitionStoppingCondition(
            max_runtime_in_seconds=max_runtime_in_seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStoppingCondition", [value]))

    @jsii.member(jsii_name="resetDataQualityBaselineConfig")
    def reset_data_quality_baseline_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataQualityBaselineConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStoppingCondition")
    def reset_stopping_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoppingCondition", []))

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
    @jsii.member(jsii_name="dataQualityAppSpecification")
    def data_quality_app_specification(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference", jsii.get(self, "dataQualityAppSpecification"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityBaselineConfig")
    def data_quality_baseline_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference", jsii.get(self, "dataQualityBaselineConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobInput")
    def data_quality_job_input(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference", jsii.get(self, "dataQualityJobInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobOutputConfig")
    def data_quality_job_output_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference", jsii.get(self, "dataQualityJobOutputConfig"))

    @builtins.property
    @jsii.member(jsii_name="jobResources")
    def job_resources(
        self,
    ) -> "SagemakerDataQualityJobDefinitionJobResourcesOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionJobResourcesOutputReference", jsii.get(self, "jobResources"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionNetworkConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="stoppingCondition")
    def stopping_condition(
        self,
    ) -> "SagemakerDataQualityJobDefinitionStoppingConditionOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionStoppingConditionOutputReference", jsii.get(self, "stoppingCondition"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityAppSpecificationInput")
    def data_quality_app_specification_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityAppSpecification"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityAppSpecification"], jsii.get(self, "dataQualityAppSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityBaselineConfigInput")
    def data_quality_baseline_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"], jsii.get(self, "dataQualityBaselineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobInputInput")
    def data_quality_job_input_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInput"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInput"], jsii.get(self, "dataQualityJobInputInput"))

    @builtins.property
    @jsii.member(jsii_name="dataQualityJobOutputConfigInput")
    def data_quality_job_output_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig"], jsii.get(self, "dataQualityJobOutputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobResourcesInput")
    def job_resources_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionJobResources"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionJobResources"], jsii.get(self, "jobResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stoppingConditionInput")
    def stopping_condition_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"], jsii.get(self, "stoppingConditionInput"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d70728ad8068f61303cbe759c25252720599b8de45f1193607fb7bb44a18b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603177c4886de16c45bf9bb6ac8891c635e91d613146e250cf0c1872725ad9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89be73f1f5918ac624c1cba201a014bcb87ff9cbe60d3414d5bc7659faefd942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc26e57bcd33734c49b5a75a79d7dfa2f3b9da6287f4cccf50846942c963c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a252c0208496b82154a246870311f6d28ab9d1127cdca2a5e6eed867047b11bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4666e269c131e7ab9802689f252d349ce4b97a9e08699fed6664c80514038dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_quality_app_specification": "dataQualityAppSpecification",
        "data_quality_job_input": "dataQualityJobInput",
        "data_quality_job_output_config": "dataQualityJobOutputConfig",
        "job_resources": "jobResources",
        "role_arn": "roleArn",
        "data_quality_baseline_config": "dataQualityBaselineConfig",
        "id": "id",
        "name": "name",
        "network_config": "networkConfig",
        "region": "region",
        "stopping_condition": "stoppingCondition",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerDataQualityJobDefinitionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_quality_app_specification: typing.Union["SagemakerDataQualityJobDefinitionDataQualityAppSpecification", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_input: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInput", typing.Dict[builtins.str, typing.Any]],
        data_quality_job_output_config: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig", typing.Dict[builtins.str, typing.Any]],
        job_resources: typing.Union["SagemakerDataQualityJobDefinitionJobResources", typing.Dict[builtins.str, typing.Any]],
        role_arn: builtins.str,
        data_quality_baseline_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        stopping_condition: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionStoppingCondition", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param data_quality_app_specification: data_quality_app_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_app_specification SagemakerDataQualityJobDefinition#data_quality_app_specification}
        :param data_quality_job_input: data_quality_job_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_input SagemakerDataQualityJobDefinition#data_quality_job_input}
        :param data_quality_job_output_config: data_quality_job_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_output_config SagemakerDataQualityJobDefinition#data_quality_job_output_config}
        :param job_resources: job_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#job_resources SagemakerDataQualityJobDefinition#job_resources}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#role_arn SagemakerDataQualityJobDefinition#role_arn}.
        :param data_quality_baseline_config: data_quality_baseline_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_baseline_config SagemakerDataQualityJobDefinition#data_quality_baseline_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#id SagemakerDataQualityJobDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#name SagemakerDataQualityJobDefinition#name}.
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#network_config SagemakerDataQualityJobDefinition#network_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#region SagemakerDataQualityJobDefinition#region}
        :param stopping_condition: stopping_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#stopping_condition SagemakerDataQualityJobDefinition#stopping_condition}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#tags SagemakerDataQualityJobDefinition#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#tags_all SagemakerDataQualityJobDefinition#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_quality_app_specification, dict):
            data_quality_app_specification = SagemakerDataQualityJobDefinitionDataQualityAppSpecification(**data_quality_app_specification)
        if isinstance(data_quality_job_input, dict):
            data_quality_job_input = SagemakerDataQualityJobDefinitionDataQualityJobInput(**data_quality_job_input)
        if isinstance(data_quality_job_output_config, dict):
            data_quality_job_output_config = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig(**data_quality_job_output_config)
        if isinstance(job_resources, dict):
            job_resources = SagemakerDataQualityJobDefinitionJobResources(**job_resources)
        if isinstance(data_quality_baseline_config, dict):
            data_quality_baseline_config = SagemakerDataQualityJobDefinitionDataQualityBaselineConfig(**data_quality_baseline_config)
        if isinstance(network_config, dict):
            network_config = SagemakerDataQualityJobDefinitionNetworkConfig(**network_config)
        if isinstance(stopping_condition, dict):
            stopping_condition = SagemakerDataQualityJobDefinitionStoppingCondition(**stopping_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab75ab0d9cbece5339476ee8404fcbcf4648f0ae46eaaa27d72e3a84e2a679aa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_quality_app_specification", value=data_quality_app_specification, expected_type=type_hints["data_quality_app_specification"])
            check_type(argname="argument data_quality_job_input", value=data_quality_job_input, expected_type=type_hints["data_quality_job_input"])
            check_type(argname="argument data_quality_job_output_config", value=data_quality_job_output_config, expected_type=type_hints["data_quality_job_output_config"])
            check_type(argname="argument job_resources", value=job_resources, expected_type=type_hints["job_resources"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument data_quality_baseline_config", value=data_quality_baseline_config, expected_type=type_hints["data_quality_baseline_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument stopping_condition", value=stopping_condition, expected_type=type_hints["stopping_condition"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_quality_app_specification": data_quality_app_specification,
            "data_quality_job_input": data_quality_job_input,
            "data_quality_job_output_config": data_quality_job_output_config,
            "job_resources": job_resources,
            "role_arn": role_arn,
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
        if data_quality_baseline_config is not None:
            self._values["data_quality_baseline_config"] = data_quality_baseline_config
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if network_config is not None:
            self._values["network_config"] = network_config
        if region is not None:
            self._values["region"] = region
        if stopping_condition is not None:
            self._values["stopping_condition"] = stopping_condition
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
    def data_quality_app_specification(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityAppSpecification":
        '''data_quality_app_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_app_specification SagemakerDataQualityJobDefinition#data_quality_app_specification}
        '''
        result = self._values.get("data_quality_app_specification")
        assert result is not None, "Required property 'data_quality_app_specification' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityAppSpecification", result)

    @builtins.property
    def data_quality_job_input(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobInput":
        '''data_quality_job_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_input SagemakerDataQualityJobDefinition#data_quality_job_input}
        '''
        result = self._values.get("data_quality_job_input")
        assert result is not None, "Required property 'data_quality_job_input' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobInput", result)

    @builtins.property
    def data_quality_job_output_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig":
        '''data_quality_job_output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_job_output_config SagemakerDataQualityJobDefinition#data_quality_job_output_config}
        '''
        result = self._values.get("data_quality_job_output_config")
        assert result is not None, "Required property 'data_quality_job_output_config' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig", result)

    @builtins.property
    def job_resources(self) -> "SagemakerDataQualityJobDefinitionJobResources":
        '''job_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#job_resources SagemakerDataQualityJobDefinition#job_resources}
        '''
        result = self._values.get("job_resources")
        assert result is not None, "Required property 'job_resources' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionJobResources", result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#role_arn SagemakerDataQualityJobDefinition#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_quality_baseline_config(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"]:
        '''data_quality_baseline_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_quality_baseline_config SagemakerDataQualityJobDefinition#data_quality_baseline_config}
        '''
        result = self._values.get("data_quality_baseline_config")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#id SagemakerDataQualityJobDefinition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#name SagemakerDataQualityJobDefinition#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#network_config SagemakerDataQualityJobDefinition#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfig"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#region SagemakerDataQualityJobDefinition#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stopping_condition(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"]:
        '''stopping_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#stopping_condition SagemakerDataQualityJobDefinition#stopping_condition}
        '''
        result = self._values.get("stopping_condition")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionStoppingCondition"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#tags SagemakerDataQualityJobDefinition#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#tags_all SagemakerDataQualityJobDefinition#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityAppSpecification",
    jsii_struct_bases=[],
    name_mapping={
        "image_uri": "imageUri",
        "environment": "environment",
        "post_analytics_processor_source_uri": "postAnalyticsProcessorSourceUri",
        "record_preprocessor_source_uri": "recordPreprocessorSourceUri",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityAppSpecification:
    def __init__(
        self,
        *,
        image_uri: builtins.str,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        post_analytics_processor_source_uri: typing.Optional[builtins.str] = None,
        record_preprocessor_source_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#image_uri SagemakerDataQualityJobDefinition#image_uri}.
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#environment SagemakerDataQualityJobDefinition#environment}.
        :param post_analytics_processor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#post_analytics_processor_source_uri SagemakerDataQualityJobDefinition#post_analytics_processor_source_uri}.
        :param record_preprocessor_source_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#record_preprocessor_source_uri SagemakerDataQualityJobDefinition#record_preprocessor_source_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78ef6677159b89e489f6701d6f2ed98caaa9b9d7a36bec6d32bb007a415e6ad)
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument post_analytics_processor_source_uri", value=post_analytics_processor_source_uri, expected_type=type_hints["post_analytics_processor_source_uri"])
            check_type(argname="argument record_preprocessor_source_uri", value=record_preprocessor_source_uri, expected_type=type_hints["record_preprocessor_source_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_uri": image_uri,
        }
        if environment is not None:
            self._values["environment"] = environment
        if post_analytics_processor_source_uri is not None:
            self._values["post_analytics_processor_source_uri"] = post_analytics_processor_source_uri
        if record_preprocessor_source_uri is not None:
            self._values["record_preprocessor_source_uri"] = record_preprocessor_source_uri

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#image_uri SagemakerDataQualityJobDefinition#image_uri}.'''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#environment SagemakerDataQualityJobDefinition#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def post_analytics_processor_source_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#post_analytics_processor_source_uri SagemakerDataQualityJobDefinition#post_analytics_processor_source_uri}.'''
        result = self._values.get("post_analytics_processor_source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_preprocessor_source_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#record_preprocessor_source_uri SagemakerDataQualityJobDefinition#record_preprocessor_source_uri}.'''
        result = self._values.get("record_preprocessor_source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityAppSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87cec6d61111cc342cca7a63c1243e042e1192371e31ecc8fee3624b0969eb33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetPostAnalyticsProcessorSourceUri")
    def reset_post_analytics_processor_source_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAnalyticsProcessorSourceUri", []))

    @jsii.member(jsii_name="resetRecordPreprocessorSourceUri")
    def reset_record_preprocessor_source_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordPreprocessorSourceUri", []))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="postAnalyticsProcessorSourceUriInput")
    def post_analytics_processor_source_uri_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postAnalyticsProcessorSourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="recordPreprocessorSourceUriInput")
    def record_preprocessor_source_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordPreprocessorSourceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2be6bd075928e372986ec5a06ac06c2e78c17c43f3c610312a9b811322c224f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f451515c068241c32429d853d8ef37b2565e793f1442d3f7394a53b9a529a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postAnalyticsProcessorSourceUri")
    def post_analytics_processor_source_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postAnalyticsProcessorSourceUri"))

    @post_analytics_processor_source_uri.setter
    def post_analytics_processor_source_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee7c3187cb76267d61f53d7e16a9209083a014985f16482f673f97ac01dd316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postAnalyticsProcessorSourceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordPreprocessorSourceUri")
    def record_preprocessor_source_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordPreprocessorSourceUri"))

    @record_preprocessor_source_uri.setter
    def record_preprocessor_source_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894114fb0ebca40642540a4144059e2e7b6445c47b11c77f9010913aa17f4575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordPreprocessorSourceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac28aa17a6fd09698b6e91eabbe5843d22bd34e12e2a9bb4d2d66c9657366cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "constraints_resource": "constraintsResource",
        "statistics_resource": "statisticsResource",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityBaselineConfig:
    def __init__(
        self,
        *,
        constraints_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource", typing.Dict[builtins.str, typing.Any]]] = None,
        statistics_resource: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param constraints_resource: constraints_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#constraints_resource SagemakerDataQualityJobDefinition#constraints_resource}
        :param statistics_resource: statistics_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#statistics_resource SagemakerDataQualityJobDefinition#statistics_resource}
        '''
        if isinstance(constraints_resource, dict):
            constraints_resource = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource(**constraints_resource)
        if isinstance(statistics_resource, dict):
            statistics_resource = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource(**statistics_resource)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7bce33f58bb9224db19dd0372df4efdf0c1e8032d68ba10a207f862853be38)
            check_type(argname="argument constraints_resource", value=constraints_resource, expected_type=type_hints["constraints_resource"])
            check_type(argname="argument statistics_resource", value=statistics_resource, expected_type=type_hints["statistics_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if constraints_resource is not None:
            self._values["constraints_resource"] = constraints_resource
        if statistics_resource is not None:
            self._values["statistics_resource"] = statistics_resource

    @builtins.property
    def constraints_resource(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource"]:
        '''constraints_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#constraints_resource SagemakerDataQualityJobDefinition#constraints_resource}
        '''
        result = self._values.get("constraints_resource")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource"], result)

    @builtins.property
    def statistics_resource(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"]:
        '''statistics_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#statistics_resource SagemakerDataQualityJobDefinition#statistics_resource}
        '''
        result = self._values.get("statistics_resource")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityBaselineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource",
    jsii_struct_bases=[],
    name_mapping={"s3_uri": "s3Uri"},
)
class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource:
    def __init__(self, *, s3_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609a875d20660907467edfbcfa0f7c2052245d0b0b05ecd144468e827528dcc8)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_uri is not None:
            self._values["s3_uri"] = s3_uri

    @builtins.property
    def s3_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.'''
        result = self._values.get("s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a99cdf925fa0f867dd477919dc0686dfe055ab430d1d47f333347168fa9bc9ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Uri")
    def reset_s3_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Uri", []))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97de9018cf185dcadc80258f64cb51dc02c41c6a96fa7f340e3932885db0e03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9623fa0f52bc0c0bb10853ae1003e1fcb8e0af3dd1b45a4fbc210531c3b5b0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__838975ac3ee9d233b131ea3efd2972701516a5e857f4b6579f3a0468ca945e37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConstraintsResource")
    def put_constraints_resource(
        self,
        *,
        s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource(
            s3_uri=s3_uri
        )

        return typing.cast(None, jsii.invoke(self, "putConstraintsResource", [value]))

    @jsii.member(jsii_name="putStatisticsResource")
    def put_statistics_resource(
        self,
        *,
        s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource(
            s3_uri=s3_uri
        )

        return typing.cast(None, jsii.invoke(self, "putStatisticsResource", [value]))

    @jsii.member(jsii_name="resetConstraintsResource")
    def reset_constraints_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraintsResource", []))

    @jsii.member(jsii_name="resetStatisticsResource")
    def reset_statistics_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatisticsResource", []))

    @builtins.property
    @jsii.member(jsii_name="constraintsResource")
    def constraints_resource(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference, jsii.get(self, "constraintsResource"))

    @builtins.property
    @jsii.member(jsii_name="statisticsResource")
    def statistics_resource(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference", jsii.get(self, "statisticsResource"))

    @builtins.property
    @jsii.member(jsii_name="constraintsResourceInput")
    def constraints_resource_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource], jsii.get(self, "constraintsResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="statisticsResourceInput")
    def statistics_resource_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource"], jsii.get(self, "statisticsResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d66610f3c56952dbf25d2e3ac6b71b785bfe24ec41e6fd885c9241175f1ec72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource",
    jsii_struct_bases=[],
    name_mapping={"s3_uri": "s3Uri"},
)
class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource:
    def __init__(self, *, s3_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bd3878b01ec90de1ada8e2d012efb7d99296524922d6793042bba0d43dc1cd)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_uri is not None:
            self._values["s3_uri"] = s3_uri

    @builtins.property
    def s3_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.'''
        result = self._values.get("s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07135e394d2b93e76a82a9419033c21edba47bb0902665582f1228bbf2404e15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Uri")
    def reset_s3_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Uri", []))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25ad05e1a02da9fa89bf39f48c3ffd271ce0c9fa7faeb89f4dfb0e653c68b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f94c04c4eb95eb2f0ca9d0b589acd9eb60ccdce8165e6ed09c5e10b0d3d15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInput",
    jsii_struct_bases=[],
    name_mapping={
        "batch_transform_input": "batchTransformInput",
        "endpoint_input": "endpointInput",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobInput:
    def __init__(
        self,
        *,
        batch_transform_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_input: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_transform_input: batch_transform_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#batch_transform_input SagemakerDataQualityJobDefinition#batch_transform_input}
        :param endpoint_input: endpoint_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_input SagemakerDataQualityJobDefinition#endpoint_input}
        '''
        if isinstance(batch_transform_input, dict):
            batch_transform_input = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput(**batch_transform_input)
        if isinstance(endpoint_input, dict):
            endpoint_input = SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput(**endpoint_input)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6301e2a74acc1d2682980f852b089ed43dcc3133848822ba445b4b14227f364a)
            check_type(argname="argument batch_transform_input", value=batch_transform_input, expected_type=type_hints["batch_transform_input"])
            check_type(argname="argument endpoint_input", value=endpoint_input, expected_type=type_hints["endpoint_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_transform_input is not None:
            self._values["batch_transform_input"] = batch_transform_input
        if endpoint_input is not None:
            self._values["endpoint_input"] = endpoint_input

    @builtins.property
    def batch_transform_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput"]:
        '''batch_transform_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#batch_transform_input SagemakerDataQualityJobDefinition#batch_transform_input}
        '''
        result = self._values.get("batch_transform_input")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput"], result)

    @builtins.property
    def endpoint_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput"]:
        '''endpoint_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_input SagemakerDataQualityJobDefinition#endpoint_input}
        '''
        result = self._values.get("endpoint_input")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput",
    jsii_struct_bases=[],
    name_mapping={
        "data_captured_destination_s3_uri": "dataCapturedDestinationS3Uri",
        "dataset_format": "datasetFormat",
        "local_path": "localPath",
        "s3_data_distribution_type": "s3DataDistributionType",
        "s3_input_mode": "s3InputMode",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput:
    def __init__(
        self,
        *,
        data_captured_destination_s3_uri: builtins.str,
        dataset_format: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat", typing.Dict[builtins.str, typing.Any]],
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_captured_destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_captured_destination_s3_uri SagemakerDataQualityJobDefinition#data_captured_destination_s3_uri}.
        :param dataset_format: dataset_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#dataset_format SagemakerDataQualityJobDefinition#dataset_format}
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        if isinstance(dataset_format, dict):
            dataset_format = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat(**dataset_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81a12b0a4937077be4b583b0413844b6f6d37f375429b1deb0c2c42dcff3914)
            check_type(argname="argument data_captured_destination_s3_uri", value=data_captured_destination_s3_uri, expected_type=type_hints["data_captured_destination_s3_uri"])
            check_type(argname="argument dataset_format", value=dataset_format, expected_type=type_hints["dataset_format"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_data_distribution_type", value=s3_data_distribution_type, expected_type=type_hints["s3_data_distribution_type"])
            check_type(argname="argument s3_input_mode", value=s3_input_mode, expected_type=type_hints["s3_input_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_captured_destination_s3_uri": data_captured_destination_s3_uri,
            "dataset_format": dataset_format,
        }
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_data_distribution_type is not None:
            self._values["s3_data_distribution_type"] = s3_data_distribution_type
        if s3_input_mode is not None:
            self._values["s3_input_mode"] = s3_input_mode

    @builtins.property
    def data_captured_destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_captured_destination_s3_uri SagemakerDataQualityJobDefinition#data_captured_destination_s3_uri}.'''
        result = self._values.get("data_captured_destination_s3_uri")
        assert result is not None, "Required property 'data_captured_destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_format(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat":
        '''dataset_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#dataset_format SagemakerDataQualityJobDefinition#dataset_format}
        '''
        result = self._values.get("dataset_format")
        assert result is not None, "Required property 'dataset_format' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat", result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_data_distribution_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.'''
        result = self._values.get("s3_data_distribution_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_input_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.'''
        result = self._values.get("s3_input_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat",
    jsii_struct_bases=[],
    name_mapping={"csv": "csv", "json": "json"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat:
    def __init__(
        self,
        *,
        csv: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#csv SagemakerDataQualityJobDefinition#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#json SagemakerDataQualityJobDefinition#json}
        '''
        if isinstance(csv, dict):
            csv = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv(**csv)
        if isinstance(json, dict):
            json = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson(**json)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc0a2a45f86eee12d7aac736ae23d7bc0ed0595bb0d04a5021af3b70f937d4d)
            check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv is not None:
            self._values["csv"] = csv
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def csv(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv"]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#csv SagemakerDataQualityJobDefinition#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#json SagemakerDataQualityJobDefinition#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv",
    jsii_struct_bases=[],
    name_mapping={"header": "header"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv:
    def __init__(
        self,
        *,
        header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#header SagemakerDataQualityJobDefinition#header}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888b3e82d8cf06d5968f16e89005a207ce4e46e80add188ceacb85795e50ae32)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header is not None:
            self._values["header"] = header

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#header SagemakerDataQualityJobDefinition#header}.'''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__181764e4dd76d3b886817d872e930622f51ffd8a308da5c3c5272a419806f4fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "header"))

    @header.setter
    def header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0b89bb2448fbc0d76c6617856fd362941e658f4376aea4b14e88b694b450ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36eeef3357f391385b09192c7451135c9a37aa0c3d53b71317b0194fa4978eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson",
    jsii_struct_bases=[],
    name_mapping={"line": "line"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson:
    def __init__(
        self,
        *,
        line: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#line SagemakerDataQualityJobDefinition#line}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbc27ec3763e4ad56b1c277a37e62143085ee283271cf501f919605c7a5c9ea)
            check_type(argname="argument line", value=line, expected_type=type_hints["line"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if line is not None:
            self._values["line"] = line

    @builtins.property
    def line(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#line SagemakerDataQualityJobDefinition#line}.'''
        result = self._values.get("line")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__265eb40225e34368438ba3527a2b57aad9ca90caa0416aa6fe9d4d0d97074814)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLine")
    def reset_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLine", []))

    @builtins.property
    @jsii.member(jsii_name="lineInput")
    def line_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lineInput"))

    @builtins.property
    @jsii.member(jsii_name="line")
    def line(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "line"))

    @line.setter
    def line(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab87521e46cf1b9b101261d74fc150b301c838d5ca4c4904c0b34906d85bd238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "line", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e737defe4b942713fc198f6acf9a7b2aae099ab985e08d0400c8423ae2e4b174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a15495e6bf696bc31709e2ed9afe9a5eb558b0f4b2415326b1f681612c7bc171)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        *,
        header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#header SagemakerDataQualityJobDefinition#header}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv(
            header=header
        )

        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(
        self,
        *,
        line: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#line SagemakerDataQualityJobDefinition#line}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson(
            line=line
        )

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="resetCsv")
    def reset_csv(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsv", []))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @builtins.property
    @jsii.member(jsii_name="csv")
    def csv(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffbdff641bedbd8b2b77499f9141bc22cb4a8339587908101aeb8d77785c588f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c47241769803098164c48063358ecdcce35fd10051d03630aa7125c7c640ff50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatasetFormat")
    def put_dataset_format(
        self,
        *,
        csv: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#csv SagemakerDataQualityJobDefinition#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#json SagemakerDataQualityJobDefinition#json}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat(
            csv=csv, json=json
        )

        return typing.cast(None, jsii.invoke(self, "putDatasetFormat", [value]))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetS3DataDistributionType")
    def reset_s3_data_distribution_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3DataDistributionType", []))

    @jsii.member(jsii_name="resetS3InputMode")
    def reset_s3_input_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputMode", []))

    @builtins.property
    @jsii.member(jsii_name="datasetFormat")
    def dataset_format(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference, jsii.get(self, "datasetFormat"))

    @builtins.property
    @jsii.member(jsii_name="dataCapturedDestinationS3UriInput")
    def data_captured_destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataCapturedDestinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetFormatInput")
    def dataset_format_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat], jsii.get(self, "datasetFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionTypeInput")
    def s3_data_distribution_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataDistributionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputModeInput")
    def s3_input_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3InputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCapturedDestinationS3Uri")
    def data_captured_destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataCapturedDestinationS3Uri"))

    @data_captured_destination_s3_uri.setter
    def data_captured_destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c15a79479af3bdf329356167daaea3c73993e9a96a1bf7571a2a752f3b72f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCapturedDestinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9def02c78f618a237bf8348b2b0a9b6254a82ba6377782fcb01ca46352d8bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionType")
    def s3_data_distribution_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataDistributionType"))

    @s3_data_distribution_type.setter
    def s3_data_distribution_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e26800ec9a91066c3a935fb7f58b3b2cb896c8d43c458fc9c6d8f7e749a30ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataDistributionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3InputMode")
    def s3_input_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3InputMode"))

    @s3_input_mode.setter
    def s3_input_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680b5fbeadcf16c6e3038d3c58ac1721457fb076e17740aaa3e5f66be539aedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3InputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39585ce29502af95ede75bd16fd7a3e0063121ce5f620ae3990674c6739c7f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_name": "endpointName",
        "local_path": "localPath",
        "s3_data_distribution_type": "s3DataDistributionType",
        "s3_input_mode": "s3InputMode",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput:
    def __init__(
        self,
        *,
        endpoint_name: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_name SagemakerDataQualityJobDefinition#endpoint_name}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7951a0dee4e7b5a625a83c743506345cbc06caf4a1aec010276cc6781ab9d426)
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_data_distribution_type", value=s3_data_distribution_type, expected_type=type_hints["s3_data_distribution_type"])
            check_type(argname="argument s3_input_mode", value=s3_input_mode, expected_type=type_hints["s3_input_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_name": endpoint_name,
        }
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_data_distribution_type is not None:
            self._values["s3_data_distribution_type"] = s3_data_distribution_type
        if s3_input_mode is not None:
            self._values["s3_input_mode"] = s3_input_mode

    @builtins.property
    def endpoint_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_name SagemakerDataQualityJobDefinition#endpoint_name}.'''
        result = self._values.get("endpoint_name")
        assert result is not None, "Required property 'endpoint_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_data_distribution_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.'''
        result = self._values.get("s3_data_distribution_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_input_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.'''
        result = self._values.get("s3_input_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccc9cb7e199abcb297abf1d8456642447a47998a27ebb645223c7f0d84e75552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetS3DataDistributionType")
    def reset_s3_data_distribution_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3DataDistributionType", []))

    @jsii.member(jsii_name="resetS3InputMode")
    def reset_s3_input_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputMode", []))

    @builtins.property
    @jsii.member(jsii_name="endpointNameInput")
    def endpoint_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointNameInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionTypeInput")
    def s3_data_distribution_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3DataDistributionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputModeInput")
    def s3_input_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3InputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointName"))

    @endpoint_name.setter
    def endpoint_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0711cc1397cbedc448a45ecfdb52d9fad67b5d7a07aefddcd1c2cd4692f8e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd3ffa4a7561bd198614157ca1ab152a4fe56d34d449d60a3e9db529de23f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3DataDistributionType")
    def s3_data_distribution_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3DataDistributionType"))

    @s3_data_distribution_type.setter
    def s3_data_distribution_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594faa584b810056bf71f14154c64bde277eab22aaefd8b38387a638dc2bfd0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3DataDistributionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3InputMode")
    def s3_input_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3InputMode"))

    @s3_input_mode.setter
    def s3_input_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4c4e3cce3cdd34281d1146eebdfdc13c0a8b5ee2e4348908115603528fe0b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3InputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed6fc454176c1af914305534d29a552ed19e5b95f1d1e2935c1bfbcd4787b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72236da76f9ba8c91fde7585959868fbba47537d481e5340c3287f0ba2ccd3b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBatchTransformInput")
    def put_batch_transform_input(
        self,
        *,
        data_captured_destination_s3_uri: builtins.str,
        dataset_format: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat, typing.Dict[builtins.str, typing.Any]],
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_captured_destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#data_captured_destination_s3_uri SagemakerDataQualityJobDefinition#data_captured_destination_s3_uri}.
        :param dataset_format: dataset_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#dataset_format SagemakerDataQualityJobDefinition#dataset_format}
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput(
            data_captured_destination_s3_uri=data_captured_destination_s3_uri,
            dataset_format=dataset_format,
            local_path=local_path,
            s3_data_distribution_type=s3_data_distribution_type,
            s3_input_mode=s3_input_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putBatchTransformInput", [value]))

    @jsii.member(jsii_name="putEndpointInput")
    def put_endpoint_input(
        self,
        *,
        endpoint_name: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_data_distribution_type: typing.Optional[builtins.str] = None,
        s3_input_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#endpoint_name SagemakerDataQualityJobDefinition#endpoint_name}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_data_distribution_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_data_distribution_type SagemakerDataQualityJobDefinition#s3_data_distribution_type}.
        :param s3_input_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_input_mode SagemakerDataQualityJobDefinition#s3_input_mode}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput(
            endpoint_name=endpoint_name,
            local_path=local_path,
            s3_data_distribution_type=s3_data_distribution_type,
            s3_input_mode=s3_input_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointInput", [value]))

    @jsii.member(jsii_name="resetBatchTransformInput")
    def reset_batch_transform_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchTransformInput", []))

    @jsii.member(jsii_name="resetEndpointInput")
    def reset_endpoint_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointInput", []))

    @builtins.property
    @jsii.member(jsii_name="batchTransformInput")
    def batch_transform_input(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference, jsii.get(self, "batchTransformInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference, jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="batchTransformInputInput")
    def batch_transform_input_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput], jsii.get(self, "batchTransformInputInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInputInput")
    def endpoint_input_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput], jsii.get(self, "endpointInputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa74ac3f04b9152159843f3b27f7f73f0d262d8edf987efd0bc81fb843f4c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"monitoring_outputs": "monitoringOutputs", "kms_key_id": "kmsKeyId"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig:
    def __init__(
        self,
        *,
        monitoring_outputs: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs", typing.Dict[builtins.str, typing.Any]],
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param monitoring_outputs: monitoring_outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#monitoring_outputs SagemakerDataQualityJobDefinition#monitoring_outputs}
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#kms_key_id SagemakerDataQualityJobDefinition#kms_key_id}.
        '''
        if isinstance(monitoring_outputs, dict):
            monitoring_outputs = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs(**monitoring_outputs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ef1bb754ec1d186b92c0a38e9c3e220c37c4c328db9281cddd23b831df7738)
            check_type(argname="argument monitoring_outputs", value=monitoring_outputs, expected_type=type_hints["monitoring_outputs"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitoring_outputs": monitoring_outputs,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def monitoring_outputs(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs":
        '''monitoring_outputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#monitoring_outputs SagemakerDataQualityJobDefinition#monitoring_outputs}
        '''
        result = self._values.get("monitoring_outputs")
        assert result is not None, "Required property 'monitoring_outputs' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs", result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#kms_key_id SagemakerDataQualityJobDefinition#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs",
    jsii_struct_bases=[],
    name_mapping={"s3_output": "s3Output"},
)
class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs:
    def __init__(
        self,
        *,
        s3_output: typing.Union["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param s3_output: s3_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_output SagemakerDataQualityJobDefinition#s3_output}
        '''
        if isinstance(s3_output, dict):
            s3_output = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output(**s3_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c4d2470f147992791262288505cc6fa024ae2f5cfb249bbbf855384b06c15a)
            check_type(argname="argument s3_output", value=s3_output, expected_type=type_hints["s3_output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_output": s3_output,
        }

    @builtins.property
    def s3_output(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output":
        '''s3_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_output SagemakerDataQualityJobDefinition#s3_output}
        '''
        result = self._values.get("s3_output")
        assert result is not None, "Required property 's3_output' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c82d27eeadc3f21fa3cea645838cf17ca58450c4c76994c4b865c98d52095707)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Output")
    def put_s3_output(
        self,
        *,
        s3_uri: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_upload_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_upload_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_upload_mode SagemakerDataQualityJobDefinition#s3_upload_mode}.
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output(
            s3_uri=s3_uri, local_path=local_path, s3_upload_mode=s3_upload_mode
        )

        return typing.cast(None, jsii.invoke(self, "putS3Output", [value]))

    @builtins.property
    @jsii.member(jsii_name="s3Output")
    def s3_output(
        self,
    ) -> "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference", jsii.get(self, "s3Output"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputInput")
    def s3_output_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output"], jsii.get(self, "s3OutputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f102589b6d75f38ad77495bf9cd62f578fcf1c01e331de9233658343cc05bc64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output",
    jsii_struct_bases=[],
    name_mapping={
        "s3_uri": "s3Uri",
        "local_path": "localPath",
        "s3_upload_mode": "s3UploadMode",
    },
)
class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output:
    def __init__(
        self,
        *,
        s3_uri: builtins.str,
        local_path: typing.Optional[builtins.str] = None,
        s3_upload_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.
        :param local_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.
        :param s3_upload_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_upload_mode SagemakerDataQualityJobDefinition#s3_upload_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082ff55d0cc18240746d3494d60dd6c3024e981cce9b2aff4e0c17fda85675b9)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_upload_mode", value=s3_upload_mode, expected_type=type_hints["s3_upload_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_uri": s3_uri,
        }
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_upload_mode is not None:
            self._values["s3_upload_mode"] = s3_upload_mode

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_uri SagemakerDataQualityJobDefinition#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#local_path SagemakerDataQualityJobDefinition#local_path}.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_upload_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_upload_mode SagemakerDataQualityJobDefinition#s3_upload_mode}.'''
        result = self._values.get("s3_upload_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c4fd270e91065fe2e8271dc2f34f91fb8df6520c5d7a9e69e900572e009c979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetS3UploadMode")
    def reset_s3_upload_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3UploadMode", []))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UploadModeInput")
    def s3_upload_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UploadModeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458e9a0b793cfe25370d9f631c5206614ccf0d5b313e96066a93213bba0ff174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3UploadMode")
    def s3_upload_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3UploadMode"))

    @s3_upload_mode.setter
    def s3_upload_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38440327aaf086e54d3e7db5febfa69bf25875d7d69fa4d468acdeaaeac9395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3UploadMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acaf1120f41ab5d544f8fb2da7fbfd07761cd70d652aa7464bb4e54c5f0885b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adad28cd888b6736db1b1c2926487f921bbdfa463a546a434d63666e92cd82db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f651fde5f7d84800bec32104b7a68d6c61750244e221fe6e03cf76fe8e9263b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonitoringOutputs")
    def put_monitoring_outputs(
        self,
        *,
        s3_output: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param s3_output: s3_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#s3_output SagemakerDataQualityJobDefinition#s3_output}
        '''
        value = SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs(
            s3_output=s3_output
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringOutputs", [value]))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="monitoringOutputs")
    def monitoring_outputs(
        self,
    ) -> SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference, jsii.get(self, "monitoringOutputs"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringOutputsInput")
    def monitoring_outputs_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs], jsii.get(self, "monitoringOutputsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32281eb982afadf3bfddcd02210ca750a7dd452a1c705212487f56e0ae71ce5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a644fc42b91a3bb37495bf3a99986c1829006e21b2049d6c26ae885bf9900ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResources",
    jsii_struct_bases=[],
    name_mapping={"cluster_config": "clusterConfig"},
)
class SagemakerDataQualityJobDefinitionJobResources:
    def __init__(
        self,
        *,
        cluster_config: typing.Union["SagemakerDataQualityJobDefinitionJobResourcesClusterConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#cluster_config SagemakerDataQualityJobDefinition#cluster_config}
        '''
        if isinstance(cluster_config, dict):
            cluster_config = SagemakerDataQualityJobDefinitionJobResourcesClusterConfig(**cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7b6a871785a356a22baa048905db571421359c81cebcf945974229d477afd5)
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_config": cluster_config,
        }

    @builtins.property
    def cluster_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionJobResourcesClusterConfig":
        '''cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#cluster_config SagemakerDataQualityJobDefinition#cluster_config}
        '''
        result = self._values.get("cluster_config")
        assert result is not None, "Required property 'cluster_config' is missing"
        return typing.cast("SagemakerDataQualityJobDefinitionJobResourcesClusterConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionJobResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResourcesClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "instance_type": "instanceType",
        "volume_size_in_gb": "volumeSizeInGb",
        "volume_kms_key_id": "volumeKmsKeyId",
    },
)
class SagemakerDataQualityJobDefinitionJobResourcesClusterConfig:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        instance_type: builtins.str,
        volume_size_in_gb: jsii.Number,
        volume_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#instance_count SagemakerDataQualityJobDefinition#instance_count}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#instance_type SagemakerDataQualityJobDefinition#instance_type}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#volume_size_in_gb SagemakerDataQualityJobDefinition#volume_size_in_gb}.
        :param volume_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#volume_kms_key_id SagemakerDataQualityJobDefinition#volume_kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec598ed4c4e6b4feb4379d57e57db5f43277b071abf6d9289c23e0e35b648ea)
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
            check_type(argname="argument volume_kms_key_id", value=volume_kms_key_id, expected_type=type_hints["volume_kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_count": instance_count,
            "instance_type": instance_type,
            "volume_size_in_gb": volume_size_in_gb,
        }
        if volume_kms_key_id is not None:
            self._values["volume_kms_key_id"] = volume_kms_key_id

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#instance_count SagemakerDataQualityJobDefinition#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#instance_type SagemakerDataQualityJobDefinition#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_size_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#volume_size_in_gb SagemakerDataQualityJobDefinition#volume_size_in_gb}.'''
        result = self._values.get("volume_size_in_gb")
        assert result is not None, "Required property 'volume_size_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#volume_kms_key_id SagemakerDataQualityJobDefinition#volume_kms_key_id}.'''
        result = self._values.get("volume_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionJobResourcesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a0a4bc61d74e2fccb551e76edb8af5ea26a5e98a25fdc39f43b29276feff77a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVolumeKmsKeyId")
    def reset_volume_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeKmsKeyIdInput")
    def volume_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGbInput")
    def volume_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bb6943a805e6bbb0e7bd9d32a204d4dc52f3d8c47be5d673cf490a9ff4fdc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf338e4cd3e6e457147815e69b8012e1cd13665057f3d10cea5d427a9dd72a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeKmsKeyId")
    def volume_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeKmsKeyId"))

    @volume_kms_key_id.setter
    def volume_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb9660841ffe08dcb779a66325dd6c426e385aa0768676a65c3be44c675f2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInGb"))

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602282d2e7b08beb9897449cf6fbecdc033248ac784172e9747daef49f8f0af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe4c1a929e16d4717a00df3d8e52b9c590d8c05e314aa68d30e2a3c78317730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerDataQualityJobDefinitionJobResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionJobResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f588c282c822d7a9e35f0b432240695e0a7d9a6eb2d06ca53a7069aa37dddbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterConfig")
    def put_cluster_config(
        self,
        *,
        instance_count: jsii.Number,
        instance_type: builtins.str,
        volume_size_in_gb: jsii.Number,
        volume_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#instance_count SagemakerDataQualityJobDefinition#instance_count}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#instance_type SagemakerDataQualityJobDefinition#instance_type}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#volume_size_in_gb SagemakerDataQualityJobDefinition#volume_size_in_gb}.
        :param volume_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#volume_kms_key_id SagemakerDataQualityJobDefinition#volume_kms_key_id}.
        '''
        value = SagemakerDataQualityJobDefinitionJobResourcesClusterConfig(
            instance_count=instance_count,
            instance_type=instance_type,
            volume_size_in_gb=volume_size_in_gb,
            volume_kms_key_id=volume_kms_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(
        self,
    ) -> SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference:
        return typing.cast(SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference, jsii.get(self, "clusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfigInput")
    def cluster_config_input(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig], jsii.get(self, "clusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionJobResources]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionJobResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionJobResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14ecbb69c9e990c8b68bfee68c34dc3ea2b612c6b649a07cf34c52d52bccca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_inter_container_traffic_encryption": "enableInterContainerTrafficEncryption",
        "enable_network_isolation": "enableNetworkIsolation",
        "vpc_config": "vpcConfig",
    },
)
class SagemakerDataQualityJobDefinitionNetworkConfig:
    def __init__(
        self,
        *,
        enable_inter_container_traffic_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_inter_container_traffic_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#enable_inter_container_traffic_encryption SagemakerDataQualityJobDefinition#enable_inter_container_traffic_encryption}.
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#enable_network_isolation SagemakerDataQualityJobDefinition#enable_network_isolation}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#vpc_config SagemakerDataQualityJobDefinition#vpc_config}
        '''
        if isinstance(vpc_config, dict):
            vpc_config = SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9920e3b5f6f0cf9c2850f712be627b4d27b2b0535c09c27c51e587ffa12bd0c)
            check_type(argname="argument enable_inter_container_traffic_encryption", value=enable_inter_container_traffic_encryption, expected_type=type_hints["enable_inter_container_traffic_encryption"])
            check_type(argname="argument enable_network_isolation", value=enable_network_isolation, expected_type=type_hints["enable_network_isolation"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_inter_container_traffic_encryption is not None:
            self._values["enable_inter_container_traffic_encryption"] = enable_inter_container_traffic_encryption
        if enable_network_isolation is not None:
            self._values["enable_network_isolation"] = enable_network_isolation
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def enable_inter_container_traffic_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#enable_inter_container_traffic_encryption SagemakerDataQualityJobDefinition#enable_inter_container_traffic_encryption}.'''
        result = self._values.get("enable_inter_container_traffic_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_network_isolation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#enable_network_isolation SagemakerDataQualityJobDefinition#enable_network_isolation}.'''
        result = self._values.get("enable_network_isolation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#vpc_config SagemakerDataQualityJobDefinition#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0de9df7ee3dcb7cebcb90bba12e0daed2a19fa75e1aef09265f995916c3ff46b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#security_group_ids SagemakerDataQualityJobDefinition#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#subnets SagemakerDataQualityJobDefinition#subnets}.
        '''
        value = SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig(
            security_group_ids=security_group_ids, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetEnableInterContainerTrafficEncryption")
    def reset_enable_inter_container_traffic_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInterContainerTrafficEncryption", []))

    @jsii.member(jsii_name="resetEnableNetworkIsolation")
    def reset_enable_network_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNetworkIsolation", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference":
        return typing.cast("SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="enableInterContainerTrafficEncryptionInput")
    def enable_inter_container_traffic_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInterContainerTrafficEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolationInput")
    def enable_network_isolation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNetworkIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(
        self,
    ) -> typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"]:
        return typing.cast(typing.Optional["SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInterContainerTrafficEncryption")
    def enable_inter_container_traffic_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInterContainerTrafficEncryption"))

    @enable_inter_container_traffic_encryption.setter
    def enable_inter_container_traffic_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59817abd44dd4544a32e4bbc3e7446060998f276a01b64606e2f9ebc5d319554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInterContainerTrafficEncryption", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__776d5ec7b363823bd3c85df77bc73197a559de758a04fbf8c340b863c06e0c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNetworkIsolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a6a8656f157c8dcea94e1521812d8333e976f95a69e4d4bebb357b3f2b7047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnets": "subnets"},
)
class SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#security_group_ids SagemakerDataQualityJobDefinition#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#subnets SagemakerDataQualityJobDefinition#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c321d7125a082fc41ec90c8092632eb87e6b2413987806c2ef7467ab168e570c)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnets": subnets,
        }

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#security_group_ids SagemakerDataQualityJobDefinition#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#subnets SagemakerDataQualityJobDefinition#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b44139776bfe3bf3ac479e82cb300f598f31e8e3eb2d0133bdfa2a12fff1331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6729e0e49160215c46f774e80041842f40729b5c5d8cf79c222e169c953feed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34171b146f4d9b405588fabc1ef75abdb888a9733e9368c01c36e7acdaaf9a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71874344e0ba6f7e69e91e46128c86016783ea86dc26fa81df5d312b4b0bd1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionStoppingCondition",
    jsii_struct_bases=[],
    name_mapping={"max_runtime_in_seconds": "maxRuntimeInSeconds"},
)
class SagemakerDataQualityJobDefinitionStoppingCondition:
    def __init__(
        self,
        *,
        max_runtime_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_runtime_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#max_runtime_in_seconds SagemakerDataQualityJobDefinition#max_runtime_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb386310bc3bfaf36c4a60515bda1e72fd0722c16cc73cceac2fa7d117b9dd7f)
            check_type(argname="argument max_runtime_in_seconds", value=max_runtime_in_seconds, expected_type=type_hints["max_runtime_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_runtime_in_seconds is not None:
            self._values["max_runtime_in_seconds"] = max_runtime_in_seconds

    @builtins.property
    def max_runtime_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/sagemaker_data_quality_job_definition#max_runtime_in_seconds SagemakerDataQualityJobDefinition#max_runtime_in_seconds}.'''
        result = self._values.get("max_runtime_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDataQualityJobDefinitionStoppingCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDataQualityJobDefinitionStoppingConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.sagemakerDataQualityJobDefinition.SagemakerDataQualityJobDefinitionStoppingConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d8128838512c44114baa6c0a23fa11bc1ebacb7feff52e9ad38531b1e9704c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxRuntimeInSeconds")
    def reset_max_runtime_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRuntimeInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="maxRuntimeInSecondsInput")
    def max_runtime_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRuntimeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRuntimeInSeconds")
    def max_runtime_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRuntimeInSeconds"))

    @max_runtime_in_seconds.setter
    def max_runtime_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7554684d76a76622ae08aa732fe52758837c3e94de5f998f0355502fc2b0d715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRuntimeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition]:
        return typing.cast(typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879a26cccf2e039e04d2a1e28d6324f751cbbb017b846fd8c879404bc263948f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerDataQualityJobDefinition",
    "SagemakerDataQualityJobDefinitionConfig",
    "SagemakerDataQualityJobDefinitionDataQualityAppSpecification",
    "SagemakerDataQualityJobDefinitionDataQualityAppSpecificationOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfig",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResourceOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource",
    "SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResourceOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInput",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsvOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJsonOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobInputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3OutputOutputReference",
    "SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigOutputReference",
    "SagemakerDataQualityJobDefinitionJobResources",
    "SagemakerDataQualityJobDefinitionJobResourcesClusterConfig",
    "SagemakerDataQualityJobDefinitionJobResourcesClusterConfigOutputReference",
    "SagemakerDataQualityJobDefinitionJobResourcesOutputReference",
    "SagemakerDataQualityJobDefinitionNetworkConfig",
    "SagemakerDataQualityJobDefinitionNetworkConfigOutputReference",
    "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig",
    "SagemakerDataQualityJobDefinitionNetworkConfigVpcConfigOutputReference",
    "SagemakerDataQualityJobDefinitionStoppingCondition",
    "SagemakerDataQualityJobDefinitionStoppingConditionOutputReference",
]

publication.publish()

def _typecheckingstub__eaa0cd1c3e8e97cc839c775a744dbb3b443516b515fa266b3513268452656f88(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_quality_app_specification: typing.Union[SagemakerDataQualityJobDefinitionDataQualityAppSpecification, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_input: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInput, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_output_config: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig, typing.Dict[builtins.str, typing.Any]],
    job_resources: typing.Union[SagemakerDataQualityJobDefinitionJobResources, typing.Dict[builtins.str, typing.Any]],
    role_arn: builtins.str,
    data_quality_baseline_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    stopping_condition: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionStoppingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b740ca9e42311cf9c986ed996898a1580b74da21467012733ceae31a87e870c2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d70728ad8068f61303cbe759c25252720599b8de45f1193607fb7bb44a18b30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603177c4886de16c45bf9bb6ac8891c635e91d613146e250cf0c1872725ad9ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89be73f1f5918ac624c1cba201a014bcb87ff9cbe60d3414d5bc7659faefd942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc26e57bcd33734c49b5a75a79d7dfa2f3b9da6287f4cccf50846942c963c52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a252c0208496b82154a246870311f6d28ab9d1127cdca2a5e6eed867047b11bf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4666e269c131e7ab9802689f252d349ce4b97a9e08699fed6664c80514038dd3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab75ab0d9cbece5339476ee8404fcbcf4648f0ae46eaaa27d72e3a84e2a679aa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_quality_app_specification: typing.Union[SagemakerDataQualityJobDefinitionDataQualityAppSpecification, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_input: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInput, typing.Dict[builtins.str, typing.Any]],
    data_quality_job_output_config: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig, typing.Dict[builtins.str, typing.Any]],
    job_resources: typing.Union[SagemakerDataQualityJobDefinitionJobResources, typing.Dict[builtins.str, typing.Any]],
    role_arn: builtins.str,
    data_quality_baseline_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    stopping_condition: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionStoppingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78ef6677159b89e489f6701d6f2ed98caaa9b9d7a36bec6d32bb007a415e6ad(
    *,
    image_uri: builtins.str,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    post_analytics_processor_source_uri: typing.Optional[builtins.str] = None,
    record_preprocessor_source_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cec6d61111cc342cca7a63c1243e042e1192371e31ecc8fee3624b0969eb33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2be6bd075928e372986ec5a06ac06c2e78c17c43f3c610312a9b811322c224f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f451515c068241c32429d853d8ef37b2565e793f1442d3f7394a53b9a529a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee7c3187cb76267d61f53d7e16a9209083a014985f16482f673f97ac01dd316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894114fb0ebca40642540a4144059e2e7b6445c47b11c77f9010913aa17f4575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac28aa17a6fd09698b6e91eabbe5843d22bd34e12e2a9bb4d2d66c9657366cc(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityAppSpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7bce33f58bb9224db19dd0372df4efdf0c1e8032d68ba10a207f862853be38(
    *,
    constraints_resource: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource, typing.Dict[builtins.str, typing.Any]]] = None,
    statistics_resource: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609a875d20660907467edfbcfa0f7c2052245d0b0b05ecd144468e827528dcc8(
    *,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99cdf925fa0f867dd477919dc0686dfe055ab430d1d47f333347168fa9bc9ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97de9018cf185dcadc80258f64cb51dc02c41c6a96fa7f340e3932885db0e03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9623fa0f52bc0c0bb10853ae1003e1fcb8e0af3dd1b45a4fbc210531c3b5b0bc(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigConstraintsResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838975ac3ee9d233b131ea3efd2972701516a5e857f4b6579f3a0468ca945e37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d66610f3c56952dbf25d2e3ac6b71b785bfe24ec41e6fd885c9241175f1ec72(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bd3878b01ec90de1ada8e2d012efb7d99296524922d6793042bba0d43dc1cd(
    *,
    s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07135e394d2b93e76a82a9419033c21edba47bb0902665582f1228bbf2404e15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25ad05e1a02da9fa89bf39f48c3ffd271ce0c9fa7faeb89f4dfb0e653c68b79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f94c04c4eb95eb2f0ca9d0b589acd9eb60ccdce8165e6ed09c5e10b0d3d15b(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityBaselineConfigStatisticsResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6301e2a74acc1d2682980f852b089ed43dcc3133848822ba445b4b14227f364a(
    *,
    batch_transform_input: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_input: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81a12b0a4937077be4b583b0413844b6f6d37f375429b1deb0c2c42dcff3914(
    *,
    data_captured_destination_s3_uri: builtins.str,
    dataset_format: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat, typing.Dict[builtins.str, typing.Any]],
    local_path: typing.Optional[builtins.str] = None,
    s3_data_distribution_type: typing.Optional[builtins.str] = None,
    s3_input_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc0a2a45f86eee12d7aac736ae23d7bc0ed0595bb0d04a5021af3b70f937d4d(
    *,
    csv: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888b3e82d8cf06d5968f16e89005a207ce4e46e80add188ceacb85795e50ae32(
    *,
    header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181764e4dd76d3b886817d872e930622f51ffd8a308da5c3c5272a419806f4fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0b89bb2448fbc0d76c6617856fd362941e658f4376aea4b14e88b694b450ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36eeef3357f391385b09192c7451135c9a37aa0c3d53b71317b0194fa4978eed(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatCsv],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbc27ec3763e4ad56b1c277a37e62143085ee283271cf501f919605c7a5c9ea(
    *,
    line: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265eb40225e34368438ba3527a2b57aad9ca90caa0416aa6fe9d4d0d97074814(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab87521e46cf1b9b101261d74fc150b301c838d5ca4c4904c0b34906d85bd238(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e737defe4b942713fc198f6acf9a7b2aae099ab985e08d0400c8423ae2e4b174(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormatJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15495e6bf696bc31709e2ed9afe9a5eb558b0f4b2415326b1f681612c7bc171(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbdff641bedbd8b2b77499f9141bc22cb4a8339587908101aeb8d77785c588f(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInputDatasetFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47241769803098164c48063358ecdcce35fd10051d03630aa7125c7c640ff50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c15a79479af3bdf329356167daaea3c73993e9a96a1bf7571a2a752f3b72f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9def02c78f618a237bf8348b2b0a9b6254a82ba6377782fcb01ca46352d8bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e26800ec9a91066c3a935fb7f58b3b2cb896c8d43c458fc9c6d8f7e749a30ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680b5fbeadcf16c6e3038d3c58ac1721457fb076e17740aaa3e5f66be539aedf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39585ce29502af95ede75bd16fd7a3e0063121ce5f620ae3990674c6739c7f77(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputBatchTransformInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7951a0dee4e7b5a625a83c743506345cbc06caf4a1aec010276cc6781ab9d426(
    *,
    endpoint_name: builtins.str,
    local_path: typing.Optional[builtins.str] = None,
    s3_data_distribution_type: typing.Optional[builtins.str] = None,
    s3_input_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc9cb7e199abcb297abf1d8456642447a47998a27ebb645223c7f0d84e75552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0711cc1397cbedc448a45ecfdb52d9fad67b5d7a07aefddcd1c2cd4692f8e11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd3ffa4a7561bd198614157ca1ab152a4fe56d34d449d60a3e9db529de23f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594faa584b810056bf71f14154c64bde277eab22aaefd8b38387a638dc2bfd0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4c4e3cce3cdd34281d1146eebdfdc13c0a8b5ee2e4348908115603528fe0b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed6fc454176c1af914305534d29a552ed19e5b95f1d1e2935c1bfbcd4787b4c(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInputEndpointInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72236da76f9ba8c91fde7585959868fbba47537d481e5340c3287f0ba2ccd3b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa74ac3f04b9152159843f3b27f7f73f0d262d8edf987efd0bc81fb843f4c42(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ef1bb754ec1d186b92c0a38e9c3e220c37c4c328db9281cddd23b831df7738(
    *,
    monitoring_outputs: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs, typing.Dict[builtins.str, typing.Any]],
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c4d2470f147992791262288505cc6fa024ae2f5cfb249bbbf855384b06c15a(
    *,
    s3_output: typing.Union[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82d27eeadc3f21fa3cea645838cf17ca58450c4c76994c4b865c98d52095707(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f102589b6d75f38ad77495bf9cd62f578fcf1c01e331de9233658343cc05bc64(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082ff55d0cc18240746d3494d60dd6c3024e981cce9b2aff4e0c17fda85675b9(
    *,
    s3_uri: builtins.str,
    local_path: typing.Optional[builtins.str] = None,
    s3_upload_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4fd270e91065fe2e8271dc2f34f91fb8df6520c5d7a9e69e900572e009c979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458e9a0b793cfe25370d9f631c5206614ccf0d5b313e96066a93213bba0ff174(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38440327aaf086e54d3e7db5febfa69bf25875d7d69fa4d468acdeaaeac9395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acaf1120f41ab5d544f8fb2da7fbfd07761cd70d652aa7464bb4e54c5f0885b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adad28cd888b6736db1b1c2926487f921bbdfa463a546a434d63666e92cd82db(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfigMonitoringOutputsS3Output],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f651fde5f7d84800bec32104b7a68d6c61750244e221fe6e03cf76fe8e9263b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32281eb982afadf3bfddcd02210ca750a7dd452a1c705212487f56e0ae71ce5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a644fc42b91a3bb37495bf3a99986c1829006e21b2049d6c26ae885bf9900ad(
    value: typing.Optional[SagemakerDataQualityJobDefinitionDataQualityJobOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7b6a871785a356a22baa048905db571421359c81cebcf945974229d477afd5(
    *,
    cluster_config: typing.Union[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec598ed4c4e6b4feb4379d57e57db5f43277b071abf6d9289c23e0e35b648ea(
    *,
    instance_count: jsii.Number,
    instance_type: builtins.str,
    volume_size_in_gb: jsii.Number,
    volume_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0a4bc61d74e2fccb551e76edb8af5ea26a5e98a25fdc39f43b29276feff77a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bb6943a805e6bbb0e7bd9d32a204d4dc52f3d8c47be5d673cf490a9ff4fdc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf338e4cd3e6e457147815e69b8012e1cd13665057f3d10cea5d427a9dd72a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb9660841ffe08dcb779a66325dd6c426e385aa0768676a65c3be44c675f2d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602282d2e7b08beb9897449cf6fbecdc033248ac784172e9747daef49f8f0af9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe4c1a929e16d4717a00df3d8e52b9c590d8c05e314aa68d30e2a3c78317730(
    value: typing.Optional[SagemakerDataQualityJobDefinitionJobResourcesClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f588c282c822d7a9e35f0b432240695e0a7d9a6eb2d06ca53a7069aa37dddbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14ecbb69c9e990c8b68bfee68c34dc3ea2b612c6b649a07cf34c52d52bccca1(
    value: typing.Optional[SagemakerDataQualityJobDefinitionJobResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9920e3b5f6f0cf9c2850f712be627b4d27b2b0535c09c27c51e587ffa12bd0c(
    *,
    enable_inter_container_traffic_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc_config: typing.Optional[typing.Union[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de9df7ee3dcb7cebcb90bba12e0daed2a19fa75e1aef09265f995916c3ff46b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59817abd44dd4544a32e4bbc3e7446060998f276a01b64606e2f9ebc5d319554(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776d5ec7b363823bd3c85df77bc73197a559de758a04fbf8c340b863c06e0c08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a6a8656f157c8dcea94e1521812d8333e976f95a69e4d4bebb357b3f2b7047(
    value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c321d7125a082fc41ec90c8092632eb87e6b2413987806c2ef7467ab168e570c(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b44139776bfe3bf3ac479e82cb300f598f31e8e3eb2d0133bdfa2a12fff1331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6729e0e49160215c46f774e80041842f40729b5c5d8cf79c222e169c953feed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34171b146f4d9b405588fabc1ef75abdb888a9733e9368c01c36e7acdaaf9a0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71874344e0ba6f7e69e91e46128c86016783ea86dc26fa81df5d312b4b0bd1fa(
    value: typing.Optional[SagemakerDataQualityJobDefinitionNetworkConfigVpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb386310bc3bfaf36c4a60515bda1e72fd0722c16cc73cceac2fa7d117b9dd7f(
    *,
    max_runtime_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d8128838512c44114baa6c0a23fa11bc1ebacb7feff52e9ad38531b1e9704c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7554684d76a76622ae08aa732fe52758837c3e94de5f998f0355502fc2b0d715(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879a26cccf2e039e04d2a1e28d6324f751cbbb017b846fd8c879404bc263948f(
    value: typing.Optional[SagemakerDataQualityJobDefinitionStoppingCondition],
) -> None:
    """Type checking stubs"""
    pass
