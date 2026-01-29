r'''
# `aws_pipes_pipe`

Refer to the Terraform Registry for docs: [`aws_pipes_pipe`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe).
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


class PipesPipe(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipe",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe aws_pipes_pipe}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        role_arn: builtins.str,
        source: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        enrichment: typing.Optional[builtins.str] = None,
        enrichment_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["PipesPipeLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        source_parameters: typing.Optional[typing.Union["PipesPipeSourceParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_parameters: typing.Optional[typing.Union["PipesPipeTargetParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PipesPipeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe aws_pipes_pipe} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#role_arn PipesPipe#role_arn}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#target PipesPipe#target}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#description PipesPipe#description}.
        :param desired_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#desired_state PipesPipe#desired_state}.
        :param enrichment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enrichment PipesPipe#enrichment}.
        :param enrichment_parameters: enrichment_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enrichment_parameters PipesPipe#enrichment_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#id PipesPipe#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kms_key_identifier PipesPipe#kms_key_identifier}.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_configuration PipesPipe#log_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name_prefix PipesPipe#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#region PipesPipe#region}
        :param source_parameters: source_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source_parameters PipesPipe#source_parameters}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags_all PipesPipe#tags_all}.
        :param target_parameters: target_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#target_parameters PipesPipe#target_parameters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#timeouts PipesPipe#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6355d49fe49afd5d2d9c79c978d6ef634e4f2baf18d67546ab6fc28ac6d8a275)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PipesPipeConfig(
            role_arn=role_arn,
            source=source,
            target=target,
            description=description,
            desired_state=desired_state,
            enrichment=enrichment,
            enrichment_parameters=enrichment_parameters,
            id=id,
            kms_key_identifier=kms_key_identifier,
            log_configuration=log_configuration,
            name=name,
            name_prefix=name_prefix,
            region=region,
            source_parameters=source_parameters,
            tags=tags,
            tags_all=tags_all,
            target_parameters=target_parameters,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a PipesPipe resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PipesPipe to import.
        :param import_from_id: The id of the existing PipesPipe that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PipesPipe to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfe5164c3245f70d9e7bff1fb839094d2729ca7f4b1835f81b44bf7c01f2c47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnrichmentParameters")
    def put_enrichment_parameters(
        self,
        *,
        http_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        '''
        value = PipesPipeEnrichmentParameters(
            http_parameters=http_parameters, input_template=input_template
        )

        return typing.cast(None, jsii.invoke(self, "putEnrichmentParameters", [value]))

    @jsii.member(jsii_name="putLogConfiguration")
    def put_log_configuration(
        self,
        *,
        level: builtins.str,
        cloudwatch_logs_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationCloudwatchLogsLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationFirehoseLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationS3LogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#level PipesPipe#level}.
        :param cloudwatch_logs_log_destination: cloudwatch_logs_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cloudwatch_logs_log_destination PipesPipe#cloudwatch_logs_log_destination}
        :param firehose_log_destination: firehose_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#firehose_log_destination PipesPipe#firehose_log_destination}
        :param include_execution_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#include_execution_data PipesPipe#include_execution_data}.
        :param s3_log_destination: s3_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#s3_log_destination PipesPipe#s3_log_destination}
        '''
        value = PipesPipeLogConfiguration(
            level=level,
            cloudwatch_logs_log_destination=cloudwatch_logs_log_destination,
            firehose_log_destination=firehose_log_destination,
            include_execution_data=include_execution_data,
            s3_log_destination=s3_log_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfiguration", [value]))

    @jsii.member(jsii_name="putSourceParameters")
    def put_source_parameters(
        self,
        *,
        activemq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersActivemqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersDynamodbStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        filter_criteria: typing.Optional[typing.Union["PipesPipeSourceParametersFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_streaming_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersManagedStreamingKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        rabbitmq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersRabbitmqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param activemq_broker_parameters: activemq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#activemq_broker_parameters PipesPipe#activemq_broker_parameters}
        :param dynamodb_stream_parameters: dynamodb_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dynamodb_stream_parameters PipesPipe#dynamodb_stream_parameters}
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#filter_criteria PipesPipe#filter_criteria}
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param managed_streaming_kafka_parameters: managed_streaming_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#managed_streaming_kafka_parameters PipesPipe#managed_streaming_kafka_parameters}
        :param rabbitmq_broker_parameters: rabbitmq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#rabbitmq_broker_parameters PipesPipe#rabbitmq_broker_parameters}
        :param self_managed_kafka_parameters: self_managed_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#self_managed_kafka_parameters PipesPipe#self_managed_kafka_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        value = PipesPipeSourceParameters(
            activemq_broker_parameters=activemq_broker_parameters,
            dynamodb_stream_parameters=dynamodb_stream_parameters,
            filter_criteria=filter_criteria,
            kinesis_stream_parameters=kinesis_stream_parameters,
            managed_streaming_kafka_parameters=managed_streaming_kafka_parameters,
            rabbitmq_broker_parameters=rabbitmq_broker_parameters,
            self_managed_kafka_parameters=self_managed_kafka_parameters,
            sqs_queue_parameters=sqs_queue_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceParameters", [value]))

    @jsii.member(jsii_name="putTargetParameters")
    def put_target_parameters(
        self,
        *,
        batch_job_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersCloudwatchLogsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_task_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        eventbridge_event_bus_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEventbridgeEventBusParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        http_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersLambdaFunctionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_data_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersRedshiftDataParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sagemaker_pipeline_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSagemakerPipelineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        step_function_state_machine_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersStepFunctionStateMachineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_job_parameters: batch_job_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_job_parameters PipesPipe#batch_job_parameters}
        :param cloudwatch_logs_parameters: cloudwatch_logs_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cloudwatch_logs_parameters PipesPipe#cloudwatch_logs_parameters}
        :param ecs_task_parameters: ecs_task_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#ecs_task_parameters PipesPipe#ecs_task_parameters}
        :param eventbridge_event_bus_parameters: eventbridge_event_bus_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#eventbridge_event_bus_parameters PipesPipe#eventbridge_event_bus_parameters}
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param lambda_function_parameters: lambda_function_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#lambda_function_parameters PipesPipe#lambda_function_parameters}
        :param redshift_data_parameters: redshift_data_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#redshift_data_parameters PipesPipe#redshift_data_parameters}
        :param sagemaker_pipeline_parameters: sagemaker_pipeline_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sagemaker_pipeline_parameters PipesPipe#sagemaker_pipeline_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        :param step_function_state_machine_parameters: step_function_state_machine_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#step_function_state_machine_parameters PipesPipe#step_function_state_machine_parameters}
        '''
        value = PipesPipeTargetParameters(
            batch_job_parameters=batch_job_parameters,
            cloudwatch_logs_parameters=cloudwatch_logs_parameters,
            ecs_task_parameters=ecs_task_parameters,
            eventbridge_event_bus_parameters=eventbridge_event_bus_parameters,
            http_parameters=http_parameters,
            input_template=input_template,
            kinesis_stream_parameters=kinesis_stream_parameters,
            lambda_function_parameters=lambda_function_parameters,
            redshift_data_parameters=redshift_data_parameters,
            sagemaker_pipeline_parameters=sagemaker_pipeline_parameters,
            sqs_queue_parameters=sqs_queue_parameters,
            step_function_state_machine_parameters=step_function_state_machine_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putTargetParameters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#create PipesPipe#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#delete PipesPipe#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#update PipesPipe#update}.
        '''
        value = PipesPipeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetEnrichment")
    def reset_enrichment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnrichment", []))

    @jsii.member(jsii_name="resetEnrichmentParameters")
    def reset_enrichment_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnrichmentParameters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyIdentifier")
    def reset_kms_key_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyIdentifier", []))

    @jsii.member(jsii_name="resetLogConfiguration")
    def reset_log_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfiguration", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSourceParameters")
    def reset_source_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceParameters", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTargetParameters")
    def reset_target_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetParameters", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="enrichmentParameters")
    def enrichment_parameters(self) -> "PipesPipeEnrichmentParametersOutputReference":
        return typing.cast("PipesPipeEnrichmentParametersOutputReference", jsii.get(self, "enrichmentParameters"))

    @builtins.property
    @jsii.member(jsii_name="logConfiguration")
    def log_configuration(self) -> "PipesPipeLogConfigurationOutputReference":
        return typing.cast("PipesPipeLogConfigurationOutputReference", jsii.get(self, "logConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sourceParameters")
    def source_parameters(self) -> "PipesPipeSourceParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersOutputReference", jsii.get(self, "sourceParameters"))

    @builtins.property
    @jsii.member(jsii_name="targetParameters")
    def target_parameters(self) -> "PipesPipeTargetParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersOutputReference", jsii.get(self, "targetParameters"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PipesPipeTimeoutsOutputReference":
        return typing.cast("PipesPipeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="enrichmentInput")
    def enrichment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enrichmentInput"))

    @builtins.property
    @jsii.member(jsii_name="enrichmentParametersInput")
    def enrichment_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeEnrichmentParameters"]:
        return typing.cast(typing.Optional["PipesPipeEnrichmentParameters"], jsii.get(self, "enrichmentParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifierInput")
    def kms_key_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigurationInput")
    def log_configuration_input(self) -> typing.Optional["PipesPipeLogConfiguration"]:
        return typing.cast(typing.Optional["PipesPipeLogConfiguration"], jsii.get(self, "logConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceParametersInput")
    def source_parameters_input(self) -> typing.Optional["PipesPipeSourceParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParameters"], jsii.get(self, "sourceParametersInput"))

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
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetParametersInput")
    def target_parameters_input(self) -> typing.Optional["PipesPipeTargetParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParameters"], jsii.get(self, "targetParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PipesPipeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PipesPipeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5abc17f0c947c0c1dd31c40efae801ed267ed65ef8d7de8df39d27f1556d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89f3983147aeb9afc37bb27dddd1a83381a0b06fa046e83fec9cf04a13d13d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enrichment")
    def enrichment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enrichment"))

    @enrichment.setter
    def enrichment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e235f9f15928d63b63dad908d7bffc73f4575298fece6e667bea86e807b56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrichment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d272eec7606e8bc2dd541d131ba3f3359b6abb17d1d3c424d19e6c09711395d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyIdentifier"))

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f67565b4a2ad5b9bfaa5910aacb1099bdb8d109aca715e5df3909bf32b8d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f0adf10e7c550983ff4e6cf10fe7755151e871e9f0222726e8bb2222925df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ba4b3e2b3165ff82b888d3ac8c943ace08e686c207201ae2167d005f995e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d9193ec9c7ba5d86d7facd7078a14c02de1d3e2a0c52f9e375fe05e8b4735f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a2a635ee549e1d096a44f295648dd4782a35795c216f732e1a8759becdb6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cb2323059ca30cfccdb4b45a6f3e06601a25e168a590b2189681f9db5d27c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d124e6e9221f87f97cf9e5d12ba36dbed4dd59f6af9fcd8957a7a904f0bd643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8e3c1a542360cace6bbad49f57282a94a74dba081938b86efbfc7d41a43cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3158fac93bd17a371468521d95aecc4631f0f16f1492a9d70e5536a43cdd37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "role_arn": "roleArn",
        "source": "source",
        "target": "target",
        "description": "description",
        "desired_state": "desiredState",
        "enrichment": "enrichment",
        "enrichment_parameters": "enrichmentParameters",
        "id": "id",
        "kms_key_identifier": "kmsKeyIdentifier",
        "log_configuration": "logConfiguration",
        "name": "name",
        "name_prefix": "namePrefix",
        "region": "region",
        "source_parameters": "sourceParameters",
        "tags": "tags",
        "tags_all": "tagsAll",
        "target_parameters": "targetParameters",
        "timeouts": "timeouts",
    },
)
class PipesPipeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_arn: builtins.str,
        source: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        enrichment: typing.Optional[builtins.str] = None,
        enrichment_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["PipesPipeLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        source_parameters: typing.Optional[typing.Union["PipesPipeSourceParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_parameters: typing.Optional[typing.Union["PipesPipeTargetParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PipesPipeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#role_arn PipesPipe#role_arn}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#target PipesPipe#target}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#description PipesPipe#description}.
        :param desired_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#desired_state PipesPipe#desired_state}.
        :param enrichment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enrichment PipesPipe#enrichment}.
        :param enrichment_parameters: enrichment_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enrichment_parameters PipesPipe#enrichment_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#id PipesPipe#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kms_key_identifier PipesPipe#kms_key_identifier}.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_configuration PipesPipe#log_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name_prefix PipesPipe#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#region PipesPipe#region}
        :param source_parameters: source_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source_parameters PipesPipe#source_parameters}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags_all PipesPipe#tags_all}.
        :param target_parameters: target_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#target_parameters PipesPipe#target_parameters}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#timeouts PipesPipe#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(enrichment_parameters, dict):
            enrichment_parameters = PipesPipeEnrichmentParameters(**enrichment_parameters)
        if isinstance(log_configuration, dict):
            log_configuration = PipesPipeLogConfiguration(**log_configuration)
        if isinstance(source_parameters, dict):
            source_parameters = PipesPipeSourceParameters(**source_parameters)
        if isinstance(target_parameters, dict):
            target_parameters = PipesPipeTargetParameters(**target_parameters)
        if isinstance(timeouts, dict):
            timeouts = PipesPipeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0a9d27d6e68bb60d7a5bd9b6db74d6ef2d2e232d50d6581e224f795649d430)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument enrichment", value=enrichment, expected_type=type_hints["enrichment"])
            check_type(argname="argument enrichment_parameters", value=enrichment_parameters, expected_type=type_hints["enrichment_parameters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument source_parameters", value=source_parameters, expected_type=type_hints["source_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument target_parameters", value=target_parameters, expected_type=type_hints["target_parameters"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "source": source,
            "target": target,
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
        if description is not None:
            self._values["description"] = description
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if enrichment is not None:
            self._values["enrichment"] = enrichment
        if enrichment_parameters is not None:
            self._values["enrichment_parameters"] = enrichment_parameters
        if id is not None:
            self._values["id"] = id
        if kms_key_identifier is not None:
            self._values["kms_key_identifier"] = kms_key_identifier
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if region is not None:
            self._values["region"] = region
        if source_parameters is not None:
            self._values["source_parameters"] = source_parameters
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if target_parameters is not None:
            self._values["target_parameters"] = target_parameters
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#role_arn PipesPipe#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source PipesPipe#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#target PipesPipe#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#description PipesPipe#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#desired_state PipesPipe#desired_state}.'''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enrichment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enrichment PipesPipe#enrichment}.'''
        result = self._values.get("enrichment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enrichment_parameters(self) -> typing.Optional["PipesPipeEnrichmentParameters"]:
        '''enrichment_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enrichment_parameters PipesPipe#enrichment_parameters}
        '''
        result = self._values.get("enrichment_parameters")
        return typing.cast(typing.Optional["PipesPipeEnrichmentParameters"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#id PipesPipe#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kms_key_identifier PipesPipe#kms_key_identifier}.'''
        result = self._values.get("kms_key_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_configuration(self) -> typing.Optional["PipesPipeLogConfiguration"]:
        '''log_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_configuration PipesPipe#log_configuration}
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional["PipesPipeLogConfiguration"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name_prefix PipesPipe#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#region PipesPipe#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_parameters(self) -> typing.Optional["PipesPipeSourceParameters"]:
        '''source_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source_parameters PipesPipe#source_parameters}
        '''
        result = self._values.get("source_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParameters"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags_all PipesPipe#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_parameters(self) -> typing.Optional["PipesPipeTargetParameters"]:
        '''target_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#target_parameters PipesPipe#target_parameters}
        '''
        result = self._values.get("target_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParameters"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PipesPipeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#timeouts PipesPipe#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PipesPipeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeEnrichmentParameters",
    jsii_struct_bases=[],
    name_mapping={
        "http_parameters": "httpParameters",
        "input_template": "inputTemplate",
    },
)
class PipesPipeEnrichmentParameters:
    def __init__(
        self,
        *,
        http_parameters: typing.Optional[typing.Union["PipesPipeEnrichmentParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        '''
        if isinstance(http_parameters, dict):
            http_parameters = PipesPipeEnrichmentParametersHttpParameters(**http_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdb1da17624426207720f6ea7c1cf16f8dc11b8f3972e66368034d4282d2925)
            check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_parameters is not None:
            self._values["http_parameters"] = http_parameters
        if input_template is not None:
            self._values["input_template"] = input_template

    @builtins.property
    def http_parameters(
        self,
    ) -> typing.Optional["PipesPipeEnrichmentParametersHttpParameters"]:
        '''http_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        '''
        result = self._values.get("http_parameters")
        return typing.cast(typing.Optional["PipesPipeEnrichmentParametersHttpParameters"], result)

    @builtins.property
    def input_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.'''
        result = self._values.get("input_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeEnrichmentParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeEnrichmentParametersHttpParameters",
    jsii_struct_bases=[],
    name_mapping={
        "header_parameters": "headerParameters",
        "path_parameter_values": "pathParameterValues",
        "query_string_parameters": "queryStringParameters",
    },
)
class PipesPipeEnrichmentParametersHttpParameters:
    def __init__(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59c695454453403dbf9a6b9ba0fdeeb3e6137f908a0828a45dcf52f8520741e)
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.'''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.'''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.'''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeEnrichmentParametersHttpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeEnrichmentParametersHttpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeEnrichmentParametersHttpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa16b8520b91887e5e82043d548d6832b811041db5dbafaf79b5f6181665666e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeaderParameters")
    def reset_header_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderParameters", []))

    @jsii.member(jsii_name="resetPathParameterValues")
    def reset_path_parameter_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathParameterValues", []))

    @jsii.member(jsii_name="resetQueryStringParameters")
    def reset_query_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="headerParametersInput")
    def header_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathParameterValuesInput")
    def path_parameter_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathParameterValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringParametersInput")
    def query_string_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryStringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="headerParameters")
    def header_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headerParameters"))

    @header_parameters.setter
    def header_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0130b4752d7c91788b7b037fad366ecb4074901ac97e01199153e3c105770e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathParameterValues")
    def path_parameter_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pathParameterValues"))

    @path_parameter_values.setter
    def path_parameter_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79fe5ef30a398b19cfe3c7ac1802df61499ca4c5304abeb7ac5f69c5ef4dd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathParameterValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringParameters")
    def query_string_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "queryStringParameters"))

    @query_string_parameters.setter
    def query_string_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40fbf2a6d76819068260e0f18aa660390113cac053de63b3e6b8daf4e4c81f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeEnrichmentParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeEnrichmentParametersHttpParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeEnrichmentParametersHttpParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2326e3b0e8bfa412dd931a4f1232776c3f37b41d0304dc3ebdd6eb992228993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeEnrichmentParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeEnrichmentParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43bbeb4209bc64f4a43288ffa392f489df259e5e407b256a21383d98da4b5abd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpParameters")
    def put_http_parameters(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        value = PipesPipeEnrichmentParametersHttpParameters(
            header_parameters=header_parameters,
            path_parameter_values=path_parameter_values,
            query_string_parameters=query_string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpParameters", [value]))

    @jsii.member(jsii_name="resetHttpParameters")
    def reset_http_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpParameters", []))

    @jsii.member(jsii_name="resetInputTemplate")
    def reset_input_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="httpParameters")
    def http_parameters(
        self,
    ) -> PipesPipeEnrichmentParametersHttpParametersOutputReference:
        return typing.cast(PipesPipeEnrichmentParametersHttpParametersOutputReference, jsii.get(self, "httpParameters"))

    @builtins.property
    @jsii.member(jsii_name="httpParametersInput")
    def http_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeEnrichmentParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeEnrichmentParametersHttpParameters], jsii.get(self, "httpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplateInput")
    def input_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplate")
    def input_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputTemplate"))

    @input_template.setter
    def input_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645fb00c1502565c6f5aa36d293190ee4a263a564dbca40ea49277b50ffceea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeEnrichmentParameters]:
        return typing.cast(typing.Optional[PipesPipeEnrichmentParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeEnrichmentParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68be0482b8db6e1abcc660f862ad236e3e1d42915c950689355a4948514e0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "level": "level",
        "cloudwatch_logs_log_destination": "cloudwatchLogsLogDestination",
        "firehose_log_destination": "firehoseLogDestination",
        "include_execution_data": "includeExecutionData",
        "s3_log_destination": "s3LogDestination",
    },
)
class PipesPipeLogConfiguration:
    def __init__(
        self,
        *,
        level: builtins.str,
        cloudwatch_logs_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationCloudwatchLogsLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationFirehoseLogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_log_destination: typing.Optional[typing.Union["PipesPipeLogConfigurationS3LogDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#level PipesPipe#level}.
        :param cloudwatch_logs_log_destination: cloudwatch_logs_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cloudwatch_logs_log_destination PipesPipe#cloudwatch_logs_log_destination}
        :param firehose_log_destination: firehose_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#firehose_log_destination PipesPipe#firehose_log_destination}
        :param include_execution_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#include_execution_data PipesPipe#include_execution_data}.
        :param s3_log_destination: s3_log_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#s3_log_destination PipesPipe#s3_log_destination}
        '''
        if isinstance(cloudwatch_logs_log_destination, dict):
            cloudwatch_logs_log_destination = PipesPipeLogConfigurationCloudwatchLogsLogDestination(**cloudwatch_logs_log_destination)
        if isinstance(firehose_log_destination, dict):
            firehose_log_destination = PipesPipeLogConfigurationFirehoseLogDestination(**firehose_log_destination)
        if isinstance(s3_log_destination, dict):
            s3_log_destination = PipesPipeLogConfigurationS3LogDestination(**s3_log_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34db1f49e7e9f208f45272f441c0fabce7321bd8b08d5547992584ad591d19ec)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument cloudwatch_logs_log_destination", value=cloudwatch_logs_log_destination, expected_type=type_hints["cloudwatch_logs_log_destination"])
            check_type(argname="argument firehose_log_destination", value=firehose_log_destination, expected_type=type_hints["firehose_log_destination"])
            check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
            check_type(argname="argument s3_log_destination", value=s3_log_destination, expected_type=type_hints["s3_log_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "level": level,
        }
        if cloudwatch_logs_log_destination is not None:
            self._values["cloudwatch_logs_log_destination"] = cloudwatch_logs_log_destination
        if firehose_log_destination is not None:
            self._values["firehose_log_destination"] = firehose_log_destination
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if s3_log_destination is not None:
            self._values["s3_log_destination"] = s3_log_destination

    @builtins.property
    def level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#level PipesPipe#level}.'''
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_logs_log_destination(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationCloudwatchLogsLogDestination"]:
        '''cloudwatch_logs_log_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cloudwatch_logs_log_destination PipesPipe#cloudwatch_logs_log_destination}
        '''
        result = self._values.get("cloudwatch_logs_log_destination")
        return typing.cast(typing.Optional["PipesPipeLogConfigurationCloudwatchLogsLogDestination"], result)

    @builtins.property
    def firehose_log_destination(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationFirehoseLogDestination"]:
        '''firehose_log_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#firehose_log_destination PipesPipe#firehose_log_destination}
        '''
        result = self._values.get("firehose_log_destination")
        return typing.cast(typing.Optional["PipesPipeLogConfigurationFirehoseLogDestination"], result)

    @builtins.property
    def include_execution_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#include_execution_data PipesPipe#include_execution_data}.'''
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_log_destination(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationS3LogDestination"]:
        '''s3_log_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#s3_log_destination PipesPipe#s3_log_destination}
        '''
        result = self._values.get("s3_log_destination")
        return typing.cast(typing.Optional["PipesPipeLogConfigurationS3LogDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationCloudwatchLogsLogDestination",
    jsii_struct_bases=[],
    name_mapping={"log_group_arn": "logGroupArn"},
)
class PipesPipeLogConfigurationCloudwatchLogsLogDestination:
    def __init__(self, *, log_group_arn: builtins.str) -> None:
        '''
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_group_arn PipesPipe#log_group_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c624263540a00b7adfc955292a20ec5b0319a4e19f84ac9c1e709cafc66c71af)
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_arn": log_group_arn,
        }

    @builtins.property
    def log_group_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_group_arn PipesPipe#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        assert result is not None, "Required property 'log_group_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfigurationCloudwatchLogsLogDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9a8ef3a3e15c05b1b081f3b125fe8aeded30c4aa47d8949ba24fda4ec25701f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42014cbdaeb5e7085b7435639ca708baebc436cb935f3ea59111baf3224e36e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd86f514c28abec7bdbc81f4cb79ef4b1be438745ab0fab1ba4da108024aa6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationFirehoseLogDestination",
    jsii_struct_bases=[],
    name_mapping={"delivery_stream_arn": "deliveryStreamArn"},
)
class PipesPipeLogConfigurationFirehoseLogDestination:
    def __init__(self, *, delivery_stream_arn: builtins.str) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#delivery_stream_arn PipesPipe#delivery_stream_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4825c8b456c2a85d6a4808b0618b3219781384617bed09c0b8608459fc3ac19b)
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_arn": delivery_stream_arn,
        }

    @builtins.property
    def delivery_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#delivery_stream_arn PipesPipe#delivery_stream_arn}.'''
        result = self._values.get("delivery_stream_arn")
        assert result is not None, "Required property 'delivery_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfigurationFirehoseLogDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeLogConfigurationFirehoseLogDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationFirehoseLogDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf2c77ec83c44402bcbeb3a98efb8615396a02e60bcc7bc4e5dbfcf984e5440)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArnInput")
    def delivery_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @delivery_stream_arn.setter
    def delivery_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6baf7792bd2eb2d5f5882a04a4b82103ce5dc95b355bab90e3ca2138faffe9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9abb3b13299886c65a169beb19ddf9ae8a3390c9fdafdb8545f5dd8a3c4766e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeLogConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c43bcc1d2a73cc0b47525ef616516e4cdb4a168ba03e18de084db26b58930c92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogsLogDestination")
    def put_cloudwatch_logs_log_destination(
        self,
        *,
        log_group_arn: builtins.str,
    ) -> None:
        '''
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_group_arn PipesPipe#log_group_arn}.
        '''
        value = PipesPipeLogConfigurationCloudwatchLogsLogDestination(
            log_group_arn=log_group_arn
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogsLogDestination", [value]))

    @jsii.member(jsii_name="putFirehoseLogDestination")
    def put_firehose_log_destination(
        self,
        *,
        delivery_stream_arn: builtins.str,
    ) -> None:
        '''
        :param delivery_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#delivery_stream_arn PipesPipe#delivery_stream_arn}.
        '''
        value = PipesPipeLogConfigurationFirehoseLogDestination(
            delivery_stream_arn=delivery_stream_arn
        )

        return typing.cast(None, jsii.invoke(self, "putFirehoseLogDestination", [value]))

    @jsii.member(jsii_name="putS3LogDestination")
    def put_s3_log_destination(
        self,
        *,
        bucket_name: builtins.str,
        bucket_owner: builtins.str,
        output_format: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#bucket_name PipesPipe#bucket_name}.
        :param bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#bucket_owner PipesPipe#bucket_owner}.
        :param output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#output_format PipesPipe#output_format}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#prefix PipesPipe#prefix}.
        '''
        value = PipesPipeLogConfigurationS3LogDestination(
            bucket_name=bucket_name,
            bucket_owner=bucket_owner,
            output_format=output_format,
            prefix=prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3LogDestination", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogsLogDestination")
    def reset_cloudwatch_logs_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogsLogDestination", []))

    @jsii.member(jsii_name="resetFirehoseLogDestination")
    def reset_firehose_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehoseLogDestination", []))

    @jsii.member(jsii_name="resetIncludeExecutionData")
    def reset_include_execution_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeExecutionData", []))

    @jsii.member(jsii_name="resetS3LogDestination")
    def reset_s3_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3LogDestination", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsLogDestination")
    def cloudwatch_logs_log_destination(
        self,
    ) -> PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference:
        return typing.cast(PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference, jsii.get(self, "cloudwatchLogsLogDestination"))

    @builtins.property
    @jsii.member(jsii_name="firehoseLogDestination")
    def firehose_log_destination(
        self,
    ) -> PipesPipeLogConfigurationFirehoseLogDestinationOutputReference:
        return typing.cast(PipesPipeLogConfigurationFirehoseLogDestinationOutputReference, jsii.get(self, "firehoseLogDestination"))

    @builtins.property
    @jsii.member(jsii_name="s3LogDestination")
    def s3_log_destination(
        self,
    ) -> "PipesPipeLogConfigurationS3LogDestinationOutputReference":
        return typing.cast("PipesPipeLogConfigurationS3LogDestinationOutputReference", jsii.get(self, "s3LogDestination"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsLogDestinationInput")
    def cloudwatch_logs_log_destination_input(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination], jsii.get(self, "cloudwatchLogsLogDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseLogDestinationInput")
    def firehose_log_destination_input(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination], jsii.get(self, "firehoseLogDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExecutionDataInput")
    def include_execution_data_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeExecutionDataInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="s3LogDestinationInput")
    def s3_log_destination_input(
        self,
    ) -> typing.Optional["PipesPipeLogConfigurationS3LogDestination"]:
        return typing.cast(typing.Optional["PipesPipeLogConfigurationS3LogDestination"], jsii.get(self, "s3LogDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExecutionData")
    def include_execution_data(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeExecutionData"))

    @include_execution_data.setter
    def include_execution_data(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa2f4898ecfc4c7cb1a3f2a62a8f87cbe6ffbe9586ea6eacd7541ef04831f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeExecutionData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a93f573c36dd24fdc509f6e65509ae22e35b256f54cc82e3c2b23ce9456f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeLogConfiguration]:
        return typing.cast(typing.Optional[PipesPipeLogConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipesPipeLogConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62f6110cec504c8d9280e9facb982b20460662fd8ba73869a0b6e5538d9e87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationS3LogDestination",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_owner": "bucketOwner",
        "output_format": "outputFormat",
        "prefix": "prefix",
    },
)
class PipesPipeLogConfigurationS3LogDestination:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        bucket_owner: builtins.str,
        output_format: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#bucket_name PipesPipe#bucket_name}.
        :param bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#bucket_owner PipesPipe#bucket_owner}.
        :param output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#output_format PipesPipe#output_format}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#prefix PipesPipe#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76f24d1916295ca17f332f6c00fda815a1a5da58c05ff9808cc084eefe4b848)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "bucket_owner": bucket_owner,
        }
        if output_format is not None:
            self._values["output_format"] = output_format
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#bucket_name PipesPipe#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_owner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#bucket_owner PipesPipe#bucket_owner}.'''
        result = self._values.get("bucket_owner")
        assert result is not None, "Required property 'bucket_owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#output_format PipesPipe#output_format}.'''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#prefix PipesPipe#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeLogConfigurationS3LogDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeLogConfigurationS3LogDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeLogConfigurationS3LogDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d9ae59442c2a2dcf92ce53125b08cf11532095405a90b40254c21a57abd99a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOutputFormat")
    def reset_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFormat", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerInput")
    def bucket_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatInput")
    def output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f3a340078fc644e97bec4b62e5f7b7a16fcffecf79687f4fa36baf73fe0a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketOwner")
    def bucket_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketOwner"))

    @bucket_owner.setter
    def bucket_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690305a4cac686cc14cc2d639195062c38ec6c7a6b4fc2df63ed2e02e6a57d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2d4e4d671c6e28552f25d13bd8a6ca2ee4b0c0f94d86d9b4e35be8a0fa1843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431f764e59368ef7a3c12326842dedb31b29416217dfdead9880dd88c99e48a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeLogConfigurationS3LogDestination]:
        return typing.cast(typing.Optional[PipesPipeLogConfigurationS3LogDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeLogConfigurationS3LogDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6223d0204b3529f79c9826c708fa8e0dc695b2ae90dcb50c91bc6fc92b39eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "activemq_broker_parameters": "activemqBrokerParameters",
        "dynamodb_stream_parameters": "dynamodbStreamParameters",
        "filter_criteria": "filterCriteria",
        "kinesis_stream_parameters": "kinesisStreamParameters",
        "managed_streaming_kafka_parameters": "managedStreamingKafkaParameters",
        "rabbitmq_broker_parameters": "rabbitmqBrokerParameters",
        "self_managed_kafka_parameters": "selfManagedKafkaParameters",
        "sqs_queue_parameters": "sqsQueueParameters",
    },
)
class PipesPipeSourceParameters:
    def __init__(
        self,
        *,
        activemq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersActivemqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersDynamodbStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        filter_criteria: typing.Optional[typing.Union["PipesPipeSourceParametersFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_streaming_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersManagedStreamingKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        rabbitmq_broker_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersRabbitmqBrokerParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeSourceParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param activemq_broker_parameters: activemq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#activemq_broker_parameters PipesPipe#activemq_broker_parameters}
        :param dynamodb_stream_parameters: dynamodb_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dynamodb_stream_parameters PipesPipe#dynamodb_stream_parameters}
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#filter_criteria PipesPipe#filter_criteria}
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param managed_streaming_kafka_parameters: managed_streaming_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#managed_streaming_kafka_parameters PipesPipe#managed_streaming_kafka_parameters}
        :param rabbitmq_broker_parameters: rabbitmq_broker_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#rabbitmq_broker_parameters PipesPipe#rabbitmq_broker_parameters}
        :param self_managed_kafka_parameters: self_managed_kafka_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#self_managed_kafka_parameters PipesPipe#self_managed_kafka_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        if isinstance(activemq_broker_parameters, dict):
            activemq_broker_parameters = PipesPipeSourceParametersActivemqBrokerParameters(**activemq_broker_parameters)
        if isinstance(dynamodb_stream_parameters, dict):
            dynamodb_stream_parameters = PipesPipeSourceParametersDynamodbStreamParameters(**dynamodb_stream_parameters)
        if isinstance(filter_criteria, dict):
            filter_criteria = PipesPipeSourceParametersFilterCriteria(**filter_criteria)
        if isinstance(kinesis_stream_parameters, dict):
            kinesis_stream_parameters = PipesPipeSourceParametersKinesisStreamParameters(**kinesis_stream_parameters)
        if isinstance(managed_streaming_kafka_parameters, dict):
            managed_streaming_kafka_parameters = PipesPipeSourceParametersManagedStreamingKafkaParameters(**managed_streaming_kafka_parameters)
        if isinstance(rabbitmq_broker_parameters, dict):
            rabbitmq_broker_parameters = PipesPipeSourceParametersRabbitmqBrokerParameters(**rabbitmq_broker_parameters)
        if isinstance(self_managed_kafka_parameters, dict):
            self_managed_kafka_parameters = PipesPipeSourceParametersSelfManagedKafkaParameters(**self_managed_kafka_parameters)
        if isinstance(sqs_queue_parameters, dict):
            sqs_queue_parameters = PipesPipeSourceParametersSqsQueueParameters(**sqs_queue_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eabf03144eea28307ea992d6bb011346c21a9d0ed7a54ad642fd2838156a878a)
            check_type(argname="argument activemq_broker_parameters", value=activemq_broker_parameters, expected_type=type_hints["activemq_broker_parameters"])
            check_type(argname="argument dynamodb_stream_parameters", value=dynamodb_stream_parameters, expected_type=type_hints["dynamodb_stream_parameters"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
            check_type(argname="argument managed_streaming_kafka_parameters", value=managed_streaming_kafka_parameters, expected_type=type_hints["managed_streaming_kafka_parameters"])
            check_type(argname="argument rabbitmq_broker_parameters", value=rabbitmq_broker_parameters, expected_type=type_hints["rabbitmq_broker_parameters"])
            check_type(argname="argument self_managed_kafka_parameters", value=self_managed_kafka_parameters, expected_type=type_hints["self_managed_kafka_parameters"])
            check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activemq_broker_parameters is not None:
            self._values["activemq_broker_parameters"] = activemq_broker_parameters
        if dynamodb_stream_parameters is not None:
            self._values["dynamodb_stream_parameters"] = dynamodb_stream_parameters
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if kinesis_stream_parameters is not None:
            self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
        if managed_streaming_kafka_parameters is not None:
            self._values["managed_streaming_kafka_parameters"] = managed_streaming_kafka_parameters
        if rabbitmq_broker_parameters is not None:
            self._values["rabbitmq_broker_parameters"] = rabbitmq_broker_parameters
        if self_managed_kafka_parameters is not None:
            self._values["self_managed_kafka_parameters"] = self_managed_kafka_parameters
        if sqs_queue_parameters is not None:
            self._values["sqs_queue_parameters"] = sqs_queue_parameters

    @builtins.property
    def activemq_broker_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersActivemqBrokerParameters"]:
        '''activemq_broker_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#activemq_broker_parameters PipesPipe#activemq_broker_parameters}
        '''
        result = self._values.get("activemq_broker_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersActivemqBrokerParameters"], result)

    @builtins.property
    def dynamodb_stream_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersDynamodbStreamParameters"]:
        '''dynamodb_stream_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dynamodb_stream_parameters PipesPipe#dynamodb_stream_parameters}
        '''
        result = self._values.get("dynamodb_stream_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersDynamodbStreamParameters"], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersFilterCriteria"]:
        '''filter_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#filter_criteria PipesPipe#filter_criteria}
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional["PipesPipeSourceParametersFilterCriteria"], result)

    @builtins.property
    def kinesis_stream_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersKinesisStreamParameters"]:
        '''kinesis_stream_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        '''
        result = self._values.get("kinesis_stream_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersKinesisStreamParameters"], result)

    @builtins.property
    def managed_streaming_kafka_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParameters"]:
        '''managed_streaming_kafka_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#managed_streaming_kafka_parameters PipesPipe#managed_streaming_kafka_parameters}
        '''
        result = self._values.get("managed_streaming_kafka_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParameters"], result)

    @builtins.property
    def rabbitmq_broker_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"]:
        '''rabbitmq_broker_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#rabbitmq_broker_parameters PipesPipe#rabbitmq_broker_parameters}
        '''
        result = self._values.get("rabbitmq_broker_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"], result)

    @builtins.property
    def self_managed_kafka_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"]:
        '''self_managed_kafka_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#self_managed_kafka_parameters PipesPipe#self_managed_kafka_parameters}
        '''
        result = self._values.get("self_managed_kafka_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"], result)

    @builtins.property
    def sqs_queue_parameters(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSqsQueueParameters"]:
        '''sqs_queue_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        result = self._values.get("sqs_queue_parameters")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSqsQueueParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParameters",
    jsii_struct_bases=[],
    name_mapping={
        "credentials": "credentials",
        "queue_name": "queueName",
        "batch_size": "batchSize",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
    },
)
class PipesPipeSourceParametersActivemqBrokerParameters:
    def __init__(
        self,
        *,
        credentials: typing.Union["PipesPipeSourceParametersActivemqBrokerParametersCredentials", typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersActivemqBrokerParametersCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63838d22786a4e0ba2958744baa626247cd62f53e18890f240ec27a8071f7dd)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "queue_name": queue_name,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds

    @builtins.property
    def credentials(
        self,
    ) -> "PipesPipeSourceParametersActivemqBrokerParametersCredentials":
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast("PipesPipeSourceParametersActivemqBrokerParametersCredentials", result)

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersActivemqBrokerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={"basic_auth": "basicAuth"},
)
class PipesPipeSourceParametersActivemqBrokerParametersCredentials:
    def __init__(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cf9e26688431b73604c1574ff1d08243105c4478b08500a827b966a9f877d9)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "basic_auth": basic_auth,
        }

    @builtins.property
    def basic_auth(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.'''
        result = self._values.get("basic_auth")
        assert result is not None, "Required property 'basic_auth' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersActivemqBrokerParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0bd8bbcfa4f92a6c0385326e5432f0dcfa9ef29bcc49aea28a70f22d3de3c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicAuth"))

    @basic_auth.setter
    def basic_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacba6a06fcd2e87ce661ff4f6560749e2deffb392c1751ae083d078d3681e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eec62922003cea75b5c814a59f1a55ac74fbbaf8cba34d13c58a7946c4fd47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersActivemqBrokerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersActivemqBrokerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24109b15cb28552d5884ac40a09046be46f3e0ea53c85498fa44eccb94485b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        value = PipesPipeSourceParametersActivemqBrokerParametersCredentials(
            basic_auth=basic_auth
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueNameInput")
    def queue_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6f3fa2022e82661a505a90c0c6456de2d7c1f3b7c1c8a3b6fb21a6a33ec2fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f1a6be62d5a0598bb13c8ba88b3ac5471e89ef46046724d9c5a05adc1ca41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07ec5ac56240edc21b7c84b950600b78b07caec303abd88afed81e00bc96624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b9e1994d55f9da155b1b61080d5332c2d112d584bdb4176d3c79958a523960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParameters",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "dead_letter_config": "deadLetterConfig",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
    },
)
class PipesPipeSourceParametersDynamodbStreamParameters:
    def __init__(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union["PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        '''
        if isinstance(dead_letter_config, dict):
            dead_letter_config = PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig(**dead_letter_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a830723cd60156ea10f8b3693f336e2a5553ffd779125a0a959dbfbf1a583071)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor

    @builtins.property
    def starting_position(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig"]:
        '''dead_letter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional["PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.'''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersDynamodbStreamParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig:
    def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12635a1d29760e16b54df06e0ce68d2fc84ab167c7172a8c2581e6f2fbca2a92)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c6bacd3f83d9c68cfbab22289c36a9113678888af7fbdb235b39aa1d357a705)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3044a03db42452eec73028f964ff2e02cceb06b921e7ae2707d25a1838d655c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9559ab12257bc586890f8533f03707c39d645445f8633ac617189c091c34d813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersDynamodbStreamParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersDynamodbStreamParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b04c181fcfa64571e66dd4b15a25ba256f6eb771eb01fa3bca03cbb60180970f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeadLetterConfig")
    def put_dead_letter_config(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        value = PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig(
            arn=arn
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterConfig", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetDeadLetterConfig")
    def reset_dead_letter_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterConfig", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetOnPartialBatchItemFailure")
    def reset_on_partial_batch_item_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPartialBatchItemFailure", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfig")
    def dead_letter_config(
        self,
    ) -> PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference:
        return typing.cast(PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference, jsii.get(self, "deadLetterConfig"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfigInput")
    def dead_letter_config_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig], jsii.get(self, "deadLetterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSecondsInput")
    def maximum_record_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRecordAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttemptsInput")
    def maximum_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailureInput")
    def on_partial_batch_item_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPartialBatchItemFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7dfb92422dad773ceb170699edf7d69c486d609f24e39d669bfad68b30482e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d8aa14fb2c0b52565096ddabfd5c8c45193eb5a9219cad074a47fa760c9ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d389c8f08ebbaeb941cf3b553cf012f30ca133fc763b611bc89c2e179d44cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325e64222daf37c11b45ca148b5fe9b0c77fce60240a1ab0a5f0d72e94e2f877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailure")
    def on_partial_batch_item_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPartialBatchItemFailure"))

    @on_partial_batch_item_failure.setter
    def on_partial_batch_item_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d436db93482fc054f61b602bf5e1fc8b301271b1ec21a830a2af10e8ab41a18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPartialBatchItemFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ec83e3d256706235daa4af980f74c6fecb70bc787b3e0884e0e85028cd5f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3923263d97489f409e63238820a293ed04450d8457fb06c715e3bd09ded8029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e01ec621504f9e52dc9103966cd2aa5a76dc183eaf1802942d81834586cb0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteria",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class PipesPipeSourceParametersFilterCriteria:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeSourceParametersFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#filter PipesPipe#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bd39f08c855ea221c9387cc3c8c55aff3a1a5f38b92ad3da6cb7b464a734e4)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeSourceParametersFilterCriteriaFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#filter PipesPipe#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeSourceParametersFilterCriteriaFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersFilterCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaFilter",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class PipesPipeSourceParametersFilterCriteriaFilter:
    def __init__(self, *, pattern: builtins.str) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#pattern PipesPipe#pattern}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efd2946dc73b50b497ba4cf8a0f8282b35b7977d395b7e0236beece56357330)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#pattern PipesPipe#pattern}.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersFilterCriteriaFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersFilterCriteriaFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8b76aacc739815f3a94923c91a81602db5a8763df1744ddc089b2da9f319ff6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeSourceParametersFilterCriteriaFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2beb4acabd541d86e0af62bb7a5683cce9d73bdb53b96e0386658903cd5807bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeSourceParametersFilterCriteriaFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6c16e36cdd7bd0cd3ffd16113be5f12876fd2257de6171bf39df53868596c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__240e913cc4abaec5ed91ae1b36e6fe1151ba8c90f97ece1d13c6b2208a1aaf06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bda8284ae53806b769060681c4d12dc6e519f79af3718aeed0f312969a5c732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831d591061200245c83d84221d0329974f875f30455db114f8c4a01c574b4717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersFilterCriteriaFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5fd73c2ffda8986c09e34d5d105816d5a19313922b1eaddc8f46721bb317e31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff67c6b0c59159d3d1d6ea632d59e38e87efdee34aabe14fc63d643f97d6d18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278b5a1aa7c1228e698bd25129031474417ec72c59e625d446820a20786070cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersFilterCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersFilterCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c724bf464b127394bce53f5c647f18a60976e717245d79fef5187c254dd3b378)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70f2e042d29def4f53fdea45dfecdf9a69caed510887f45b1fbf3335cbf6015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> PipesPipeSourceParametersFilterCriteriaFilterList:
        return typing.cast(PipesPipeSourceParametersFilterCriteriaFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersFilterCriteria]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersFilterCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersFilterCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a17d8f5b2f38baa32095fcec8868333a971559d0e80726d075f182cdc3cb72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParameters",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "dead_letter_config": "deadLetterConfig",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "on_partial_batch_item_failure": "onPartialBatchItemFailure",
        "parallelization_factor": "parallelizationFactor",
        "starting_position_timestamp": "startingPositionTimestamp",
    },
)
class PipesPipeSourceParametersKinesisStreamParameters:
    def __init__(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union["PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position_timestamp PipesPipe#starting_position_timestamp}.
        '''
        if isinstance(dead_letter_config, dict):
            dead_letter_config = PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig(**dead_letter_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c46e6643fed5d98bd95309942af4c9361bc99dd098755306ae9a8fcc5b83e7)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if on_partial_batch_item_failure is not None:
            self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp

    @builtins.property
    def starting_position(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig"]:
        '''dead_letter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional["PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on_partial_batch_item_failure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.'''
        result = self._values.get("on_partial_batch_item_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position_timestamp PipesPipe#starting_position_timestamp}.'''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersKinesisStreamParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn"},
)
class PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig:
    def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be08880fc07d8489bd132590aee43b230db979407a35b098d439755a74ea3fb7)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8bc98902f8d0f709b69992993f46d7a4baebe4c7391e9cd1e4652753dee4a11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5051d12e0312b0a33716167b42be9302e4a81702ae5c60284a0e17e6f65e430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d004476a168997c1f2eae8cd0e32524bf1fc0b1553674919eca028b45f92ca5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersKinesisStreamParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersKinesisStreamParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e97dd812ecfa47994665e85ea63c2948c655599483606368a6d804014101227b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeadLetterConfig")
    def put_dead_letter_config(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#arn PipesPipe#arn}.
        '''
        value = PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig(
            arn=arn
        )

        return typing.cast(None, jsii.invoke(self, "putDeadLetterConfig", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetDeadLetterConfig")
    def reset_dead_letter_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterConfig", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetOnPartialBatchItemFailure")
    def reset_on_partial_batch_item_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPartialBatchItemFailure", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @jsii.member(jsii_name="resetStartingPositionTimestamp")
    def reset_starting_position_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfig")
    def dead_letter_config(
        self,
    ) -> PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference:
        return typing.cast(PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference, jsii.get(self, "deadLetterConfig"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfigInput")
    def dead_letter_config_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig], jsii.get(self, "deadLetterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSecondsInput")
    def maximum_record_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRecordAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttemptsInput")
    def maximum_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailureInput")
    def on_partial_batch_item_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onPartialBatchItemFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestampInput")
    def starting_position_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e6b87c1ea6b81639d0fc1c7bb04e552e5eda9cb85f0ef8de025d14f224d419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b46f43ba61457963dcfbb8686ca4e66ef3b77c8329da6abda69ea04e78e1dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc32931d31ccb1665480292563de9a792203f77d1925d6d2dfa615526efa63a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc85eb3d19fcfd5358321590947bc340c68880502007c2ec761773a9960e695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPartialBatchItemFailure")
    def on_partial_batch_item_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPartialBatchItemFailure"))

    @on_partial_batch_item_failure.setter
    def on_partial_batch_item_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62bc3ac5c1a3ef1f604b3bfea40c20840b9c902fc0e2ff98fbea6afcc15b8b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPartialBatchItemFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed349d0bceab0d6dea1704502d00d82609653e1a54e974d071e0d484a8560261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115d3989d565ddc9b3be1e5651856d09e3f6433c422b8eeba7d80e80daf3ffeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestamp")
    def starting_position_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPositionTimestamp"))

    @starting_position_timestamp.setter
    def starting_position_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71aaebdd91afa661784d94175eaa1f6778f7cb981a30a5d72962d4ae54e562e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPositionTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersKinesisStreamParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30499f0ae8ec3b60df9dffc9c4064f6d846deef62aa026f818145e9a00b2dd49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParameters",
    jsii_struct_bases=[],
    name_mapping={
        "topic_name": "topicName",
        "batch_size": "batchSize",
        "consumer_group_id": "consumerGroupId",
        "credentials": "credentials",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "starting_position": "startingPosition",
    },
)
class PipesPipeSourceParametersManagedStreamingKafkaParameters:
    def __init__(
        self,
        *,
        topic_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        starting_position: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02567329b8762fa7030179d3a8b800a42fc55ed140cbb18fa614fbd933c2441e)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if starting_position is not None:
            self._values["starting_position"] = starting_position

    @builtins.property
    def topic_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.'''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersManagedStreamingKafkaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "client_certificate_tls_auth": "clientCertificateTlsAuth",
        "sasl_scram512_auth": "saslScram512Auth",
    },
)
class PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials:
    def __init__(
        self,
        *,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784e5a845a7f1d2068125abed71414589eccfa2dd7eac676657c3c96be8dc0c3)
            check_type(argname="argument client_certificate_tls_auth", value=client_certificate_tls_auth, expected_type=type_hints["client_certificate_tls_auth"])
            check_type(argname="argument sasl_scram512_auth", value=sasl_scram512_auth, expected_type=type_hints["sasl_scram512_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_certificate_tls_auth is not None:
            self._values["client_certificate_tls_auth"] = client_certificate_tls_auth
        if sasl_scram512_auth is not None:
            self._values["sasl_scram512_auth"] = sasl_scram512_auth

    @builtins.property
    def client_certificate_tls_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.'''
        result = self._values.get("client_certificate_tls_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_scram512_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.'''
        result = self._values.get("sasl_scram512_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__887bed53c62519afd72790415c9ff817a2923e3e5d4d6941b89865f1e61ce79e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientCertificateTlsAuth")
    def reset_client_certificate_tls_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateTlsAuth", []))

    @jsii.member(jsii_name="resetSaslScram512Auth")
    def reset_sasl_scram512_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslScram512Auth", []))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuthInput")
    def client_certificate_tls_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateTlsAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="saslScram512AuthInput")
    def sasl_scram512_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslScram512AuthInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuth")
    def client_certificate_tls_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateTlsAuth"))

    @client_certificate_tls_auth.setter
    def client_certificate_tls_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6142c7067dabf66dc7a5851bc4e1b11f812784e326c4a3b6bf0d2e771221d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateTlsAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslScram512Auth")
    def sasl_scram512_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslScram512Auth"))

    @sasl_scram512_auth.setter
    def sasl_scram512_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf46e6a539014dde51b63af9074583349f9b3930f232d2074ebc82a9c6c2e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslScram512Auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9cfeb155386356d2409d8efa819afac6c1fd4d1b9bc72597b37170141db369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__511914c14fe07edd917cdcfcd530bcce60a296e9a27f8009cda725c276747bec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        value = PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials(
            client_certificate_tls_auth=client_certificate_tls_auth,
            sasl_scram512_auth=sasl_scram512_auth,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameInput")
    def topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fab8f4a8dfcfaccb081fcd91b7756711a7166c3518d9a52d0090d9ddec3815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ec6cc8431bd7ad1cf7f4b4f3eeb7717f7a844cf4c52d9b5081ff8b9731d8a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fce152ede5f25470ffb8a4287a7eef2549db29ae78469675306d75701e1f3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e02986d240024cf78c5b2149d58356ce2018067d69bc8c9bc5fff0240ec2933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba0553c7c843eea70a94e712867377e4e5ed7a10bc7b3669d52e6b3173910f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051f09df7d6325ce331a195692a581e7d13e1d10d1fa85ae2efee875db0cc138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b478f1596d0c56013104df1a14d53ae498d625599c11287d9165e69993e9ef5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActivemqBrokerParameters")
    def put_activemq_broker_parameters(
        self,
        *,
        credentials: typing.Union[PipesPipeSourceParametersActivemqBrokerParametersCredentials, typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        value = PipesPipeSourceParametersActivemqBrokerParameters(
            credentials=credentials,
            queue_name=queue_name,
            batch_size=batch_size,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putActivemqBrokerParameters", [value]))

    @jsii.member(jsii_name="putDynamodbStreamParameters")
    def put_dynamodb_stream_parameters(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        '''
        value = PipesPipeSourceParametersDynamodbStreamParameters(
            starting_position=starting_position,
            batch_size=batch_size,
            dead_letter_config=dead_letter_config,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamodbStreamParameters", [value]))

    @jsii.member(jsii_name="putFilterCriteria")
    def put_filter_criteria(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#filter PipesPipe#filter}
        '''
        value = PipesPipeSourceParametersFilterCriteria(filter=filter)

        return typing.cast(None, jsii.invoke(self, "putFilterCriteria", [value]))

    @jsii.member(jsii_name="putKinesisStreamParameters")
    def put_kinesis_stream_parameters(
        self,
        *,
        starting_position: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param dead_letter_config: dead_letter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#dead_letter_config PipesPipe#dead_letter_config}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_record_age_in_seconds PipesPipe#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_retry_attempts PipesPipe#maximum_retry_attempts}.
        :param on_partial_batch_item_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#on_partial_batch_item_failure PipesPipe#on_partial_batch_item_failure}.
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parallelization_factor PipesPipe#parallelization_factor}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position_timestamp PipesPipe#starting_position_timestamp}.
        '''
        value = PipesPipeSourceParametersKinesisStreamParameters(
            starting_position=starting_position,
            batch_size=batch_size,
            dead_letter_config=dead_letter_config,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            on_partial_batch_item_failure=on_partial_batch_item_failure,
            parallelization_factor=parallelization_factor,
            starting_position_timestamp=starting_position_timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStreamParameters", [value]))

    @jsii.member(jsii_name="putManagedStreamingKafkaParameters")
    def put_managed_streaming_kafka_parameters(
        self,
        *,
        topic_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        starting_position: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        '''
        value = PipesPipeSourceParametersManagedStreamingKafkaParameters(
            topic_name=topic_name,
            batch_size=batch_size,
            consumer_group_id=consumer_group_id,
            credentials=credentials,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            starting_position=starting_position,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedStreamingKafkaParameters", [value]))

    @jsii.member(jsii_name="putRabbitmqBrokerParameters")
    def put_rabbitmq_broker_parameters(
        self,
        *,
        credentials: typing.Union["PipesPipeSourceParametersRabbitmqBrokerParametersCredentials", typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        virtual_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param virtual_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#virtual_host PipesPipe#virtual_host}.
        '''
        value = PipesPipeSourceParametersRabbitmqBrokerParameters(
            credentials=credentials,
            queue_name=queue_name,
            batch_size=batch_size,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            virtual_host=virtual_host,
        )

        return typing.cast(None, jsii.invoke(self, "putRabbitmqBrokerParameters", [value]))

    @jsii.member(jsii_name="putSelfManagedKafkaParameters")
    def put_self_managed_kafka_parameters(
        self,
        *,
        topic_name: builtins.str,
        additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        server_root_ca_certificate: typing.Optional[builtins.str] = None,
        starting_position: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersVpc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param additional_bootstrap_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#additional_bootstrap_servers PipesPipe#additional_bootstrap_servers}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param server_root_ca_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#server_root_ca_certificate PipesPipe#server_root_ca_certificate}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#vpc PipesPipe#vpc}
        '''
        value = PipesPipeSourceParametersSelfManagedKafkaParameters(
            topic_name=topic_name,
            additional_bootstrap_servers=additional_bootstrap_servers,
            batch_size=batch_size,
            consumer_group_id=consumer_group_id,
            credentials=credentials,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            server_root_ca_certificate=server_root_ca_certificate,
            starting_position=starting_position,
            vpc=vpc,
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManagedKafkaParameters", [value]))

    @jsii.member(jsii_name="putSqsQueueParameters")
    def put_sqs_queue_parameters(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        value = PipesPipeSourceParametersSqsQueueParameters(
            batch_size=batch_size,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putSqsQueueParameters", [value]))

    @jsii.member(jsii_name="resetActivemqBrokerParameters")
    def reset_activemq_broker_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivemqBrokerParameters", []))

    @jsii.member(jsii_name="resetDynamodbStreamParameters")
    def reset_dynamodb_stream_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbStreamParameters", []))

    @jsii.member(jsii_name="resetFilterCriteria")
    def reset_filter_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCriteria", []))

    @jsii.member(jsii_name="resetKinesisStreamParameters")
    def reset_kinesis_stream_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStreamParameters", []))

    @jsii.member(jsii_name="resetManagedStreamingKafkaParameters")
    def reset_managed_streaming_kafka_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedStreamingKafkaParameters", []))

    @jsii.member(jsii_name="resetRabbitmqBrokerParameters")
    def reset_rabbitmq_broker_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRabbitmqBrokerParameters", []))

    @jsii.member(jsii_name="resetSelfManagedKafkaParameters")
    def reset_self_managed_kafka_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedKafkaParameters", []))

    @jsii.member(jsii_name="resetSqsQueueParameters")
    def reset_sqs_queue_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsQueueParameters", []))

    @builtins.property
    @jsii.member(jsii_name="activemqBrokerParameters")
    def activemq_broker_parameters(
        self,
    ) -> PipesPipeSourceParametersActivemqBrokerParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersActivemqBrokerParametersOutputReference, jsii.get(self, "activemqBrokerParameters"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbStreamParameters")
    def dynamodb_stream_parameters(
        self,
    ) -> PipesPipeSourceParametersDynamodbStreamParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersDynamodbStreamParametersOutputReference, jsii.get(self, "dynamodbStreamParameters"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteria")
    def filter_criteria(self) -> PipesPipeSourceParametersFilterCriteriaOutputReference:
        return typing.cast(PipesPipeSourceParametersFilterCriteriaOutputReference, jsii.get(self, "filterCriteria"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParameters")
    def kinesis_stream_parameters(
        self,
    ) -> PipesPipeSourceParametersKinesisStreamParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersKinesisStreamParametersOutputReference, jsii.get(self, "kinesisStreamParameters"))

    @builtins.property
    @jsii.member(jsii_name="managedStreamingKafkaParameters")
    def managed_streaming_kafka_parameters(
        self,
    ) -> PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference:
        return typing.cast(PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference, jsii.get(self, "managedStreamingKafkaParameters"))

    @builtins.property
    @jsii.member(jsii_name="rabbitmqBrokerParameters")
    def rabbitmq_broker_parameters(
        self,
    ) -> "PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference", jsii.get(self, "rabbitmqBrokerParameters"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaParameters")
    def self_managed_kafka_parameters(
        self,
    ) -> "PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference", jsii.get(self, "selfManagedKafkaParameters"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParameters")
    def sqs_queue_parameters(
        self,
    ) -> "PipesPipeSourceParametersSqsQueueParametersOutputReference":
        return typing.cast("PipesPipeSourceParametersSqsQueueParametersOutputReference", jsii.get(self, "sqsQueueParameters"))

    @builtins.property
    @jsii.member(jsii_name="activemqBrokerParametersInput")
    def activemq_broker_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters], jsii.get(self, "activemqBrokerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbStreamParametersInput")
    def dynamodb_stream_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters], jsii.get(self, "dynamodbStreamParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteriaInput")
    def filter_criteria_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersFilterCriteria]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersFilterCriteria], jsii.get(self, "filterCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParametersInput")
    def kinesis_stream_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersKinesisStreamParameters], jsii.get(self, "kinesisStreamParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="managedStreamingKafkaParametersInput")
    def managed_streaming_kafka_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters], jsii.get(self, "managedStreamingKafkaParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="rabbitmqBrokerParametersInput")
    def rabbitmq_broker_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersRabbitmqBrokerParameters"], jsii.get(self, "rabbitmqBrokerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaParametersInput")
    def self_managed_kafka_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParameters"], jsii.get(self, "selfManagedKafkaParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParametersInput")
    def sqs_queue_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSqsQueueParameters"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersSqsQueueParameters"], jsii.get(self, "sqsQueueParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeSourceParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipesPipeSourceParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36ea00912e235eb3c7a91fecf72d13b24ed5d1a8575eb8069cbd9d20dba35e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParameters",
    jsii_struct_bases=[],
    name_mapping={
        "credentials": "credentials",
        "queue_name": "queueName",
        "batch_size": "batchSize",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "virtual_host": "virtualHost",
    },
)
class PipesPipeSourceParametersRabbitmqBrokerParameters:
    def __init__(
        self,
        *,
        credentials: typing.Union["PipesPipeSourceParametersRabbitmqBrokerParametersCredentials", typing.Dict[builtins.str, typing.Any]],
        queue_name: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        virtual_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param virtual_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#virtual_host PipesPipe#virtual_host}.
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersRabbitmqBrokerParametersCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ecdc12ac359746a53a9fcc188b8648a30a8d4eaaff9f8428c72805aa3ac13f)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument virtual_host", value=virtual_host, expected_type=type_hints["virtual_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "queue_name": queue_name,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if virtual_host is not None:
            self._values["virtual_host"] = virtual_host

    @builtins.property
    def credentials(
        self,
    ) -> "PipesPipeSourceParametersRabbitmqBrokerParametersCredentials":
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast("PipesPipeSourceParametersRabbitmqBrokerParametersCredentials", result)

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#queue_name PipesPipe#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def virtual_host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#virtual_host PipesPipe#virtual_host}.'''
        result = self._values.get("virtual_host")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersRabbitmqBrokerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={"basic_auth": "basicAuth"},
)
class PipesPipeSourceParametersRabbitmqBrokerParametersCredentials:
    def __init__(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4c4927769f363590cffd925caf487a1c93fd8fdfd4a71d551d9e3d000fe912)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "basic_auth": basic_auth,
        }

    @builtins.property
    def basic_auth(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.'''
        result = self._values.get("basic_auth")
        assert result is not None, "Required property 'basic_auth' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersRabbitmqBrokerParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9639d63ccddc3c6ae8e5635dd17c89697dcf489f9e0de36458f18e2f62740827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicAuth"))

    @basic_auth.setter
    def basic_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9fef0236563707125ad30376024eeab2089373fe0632a67d069e131cdff271f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee2b690637c1d088460a45187ed41bec75b257de0eb72272d9094b1421b6467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0635ba53e3fee7fa8d9520cc199e4a01229472b12a632fb9b33cb108c2b3f2c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(self, *, basic_auth: builtins.str) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        '''
        value = PipesPipeSourceParametersRabbitmqBrokerParametersCredentials(
            basic_auth=basic_auth
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetVirtualHost")
    def reset_virtual_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualHost", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueNameInput")
    def queue_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualHostInput")
    def virtual_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualHostInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d0c7299e887db46207cd6495677b3fff512bbff23e4c63983c512ce6f131b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a128b6ac832829441de1be627a3992cd6298df80413e63faf8a57ccefc9d747c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2558d8eea58772003082930db4e03fe5b2533978984f898f04976fb803ffb376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualHost")
    def virtual_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualHost"))

    @virtual_host.setter
    def virtual_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868db3c567d8bcb48783fa5dd10afee1747aff4932109ab15973f6feab4aa3ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4239e080c04efe41457859a78a354f53d1a9d0e39db26e5cec73a8bc7d76aabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParameters",
    jsii_struct_bases=[],
    name_mapping={
        "topic_name": "topicName",
        "additional_bootstrap_servers": "additionalBootstrapServers",
        "batch_size": "batchSize",
        "consumer_group_id": "consumerGroupId",
        "credentials": "credentials",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "server_root_ca_certificate": "serverRootCaCertificate",
        "starting_position": "startingPosition",
        "vpc": "vpc",
    },
)
class PipesPipeSourceParametersSelfManagedKafkaParameters:
    def __init__(
        self,
        *,
        topic_name: builtins.str,
        additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        consumer_group_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        server_root_ca_certificate: typing.Optional[builtins.str] = None,
        starting_position: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[typing.Union["PipesPipeSourceParametersSelfManagedKafkaParametersVpc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.
        :param additional_bootstrap_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#additional_bootstrap_servers PipesPipe#additional_bootstrap_servers}.
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        :param server_root_ca_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#server_root_ca_certificate PipesPipe#server_root_ca_certificate}.
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#vpc PipesPipe#vpc}
        '''
        if isinstance(credentials, dict):
            credentials = PipesPipeSourceParametersSelfManagedKafkaParametersCredentials(**credentials)
        if isinstance(vpc, dict):
            vpc = PipesPipeSourceParametersSelfManagedKafkaParametersVpc(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff23c6584a00363773050f916a12785d211c71ca9dfbd11d11750c013f8d54d)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument additional_bootstrap_servers", value=additional_bootstrap_servers, expected_type=type_hints["additional_bootstrap_servers"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument server_root_ca_certificate", value=server_root_ca_certificate, expected_type=type_hints["server_root_ca_certificate"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if additional_bootstrap_servers is not None:
            self._values["additional_bootstrap_servers"] = additional_bootstrap_servers
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if server_root_ca_certificate is not None:
            self._values["server_root_ca_certificate"] = server_root_ca_certificate
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def topic_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#topic_name PipesPipe#topic_name}.'''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_bootstrap_servers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#additional_bootstrap_servers PipesPipe#additional_bootstrap_servers}.'''
        result = self._values.get("additional_bootstrap_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#consumer_group_id PipesPipe#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#credentials PipesPipe#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersCredentials"], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_root_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#server_root_ca_certificate PipesPipe#server_root_ca_certificate}.'''
        result = self._values.get("server_root_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#starting_position PipesPipe#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"]:
        '''vpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#vpc PipesPipe#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSelfManagedKafkaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "basic_auth": "basicAuth",
        "client_certificate_tls_auth": "clientCertificateTlsAuth",
        "sasl_scram256_auth": "saslScram256Auth",
        "sasl_scram512_auth": "saslScram512Auth",
    },
)
class PipesPipeSourceParametersSelfManagedKafkaParametersCredentials:
    def __init__(
        self,
        *,
        basic_auth: typing.Optional[builtins.str] = None,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram256_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram256_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_256_auth PipesPipe#sasl_scram_256_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11893978bfe6c1f8cbeb683d8db5b1e631e8692ae5f005e7e0b33c6b63030a6d)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument client_certificate_tls_auth", value=client_certificate_tls_auth, expected_type=type_hints["client_certificate_tls_auth"])
            check_type(argname="argument sasl_scram256_auth", value=sasl_scram256_auth, expected_type=type_hints["sasl_scram256_auth"])
            check_type(argname="argument sasl_scram512_auth", value=sasl_scram512_auth, expected_type=type_hints["sasl_scram512_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if client_certificate_tls_auth is not None:
            self._values["client_certificate_tls_auth"] = client_certificate_tls_auth
        if sasl_scram256_auth is not None:
            self._values["sasl_scram256_auth"] = sasl_scram256_auth
        if sasl_scram512_auth is not None:
            self._values["sasl_scram512_auth"] = sasl_scram512_auth

    @builtins.property
    def basic_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.'''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_tls_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.'''
        result = self._values.get("client_certificate_tls_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_scram256_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_256_auth PipesPipe#sasl_scram_256_auth}.'''
        result = self._values.get("sasl_scram256_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_scram512_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.'''
        result = self._values.get("sasl_scram512_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSelfManagedKafkaParametersCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d618efb25e50d23e405474607bb7d43a6249ba5c99be9fb289d7a12f271470)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetClientCertificateTlsAuth")
    def reset_client_certificate_tls_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateTlsAuth", []))

    @jsii.member(jsii_name="resetSaslScram256Auth")
    def reset_sasl_scram256_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslScram256Auth", []))

    @jsii.member(jsii_name="resetSaslScram512Auth")
    def reset_sasl_scram512_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslScram512Auth", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuthInput")
    def client_certificate_tls_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateTlsAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="saslScram256AuthInput")
    def sasl_scram256_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslScram256AuthInput"))

    @builtins.property
    @jsii.member(jsii_name="saslScram512AuthInput")
    def sasl_scram512_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslScram512AuthInput"))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicAuth"))

    @basic_auth.setter
    def basic_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e541cc812180ec9d70baf22ec74cff511d66490856cb60db182ab72ac666375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateTlsAuth")
    def client_certificate_tls_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateTlsAuth"))

    @client_certificate_tls_auth.setter
    def client_certificate_tls_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec231ca1fbb5fef5121e7219b3d8f53864c91b9776f886e05f8073776c03c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateTlsAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslScram256Auth")
    def sasl_scram256_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslScram256Auth"))

    @sasl_scram256_auth.setter
    def sasl_scram256_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674122d4fc49dd3a27b39b174b127f9635fc7c319b29f8f40ea6f2d1b6ff8189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslScram256Auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslScram512Auth")
    def sasl_scram512_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslScram512Auth"))

    @sasl_scram512_auth.setter
    def sasl_scram512_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4badca414f17a8f1dfae79abb17d631b5ab168fa15447e6581ff7b1772cca4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslScram512Auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2b683e9e0e9a4018dcd8365e149713472dc200b18d506b00c789885263e88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ce120c141a88d06cd805248f1c196b7fbb544b60d009527e4ab84dacced97b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        basic_auth: typing.Optional[builtins.str] = None,
        client_certificate_tls_auth: typing.Optional[builtins.str] = None,
        sasl_scram256_auth: typing.Optional[builtins.str] = None,
        sasl_scram512_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#basic_auth PipesPipe#basic_auth}.
        :param client_certificate_tls_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#client_certificate_tls_auth PipesPipe#client_certificate_tls_auth}.
        :param sasl_scram256_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_256_auth PipesPipe#sasl_scram_256_auth}.
        :param sasl_scram512_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sasl_scram_512_auth PipesPipe#sasl_scram_512_auth}.
        '''
        value = PipesPipeSourceParametersSelfManagedKafkaParametersCredentials(
            basic_auth=basic_auth,
            client_certificate_tls_auth=client_certificate_tls_auth,
            sasl_scram256_auth=sasl_scram256_auth,
            sasl_scram512_auth=sasl_scram512_auth,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="putVpc")
    def put_vpc(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        value = PipesPipeSourceParametersSelfManagedKafkaParametersVpc(
            security_groups=security_groups, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpc", [value]))

    @jsii.member(jsii_name="resetAdditionalBootstrapServers")
    def reset_additional_bootstrap_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalBootstrapServers", []))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetServerRootCaCertificate")
    def reset_server_root_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerRootCaCertificate", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference:
        return typing.cast(PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(
        self,
    ) -> "PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference":
        return typing.cast("PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference", jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="additionalBootstrapServersInput")
    def additional_bootstrap_servers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalBootstrapServersInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverRootCaCertificateInput")
    def server_root_ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverRootCaCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameInput")
    def topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(
        self,
    ) -> typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"]:
        return typing.cast(typing.Optional["PipesPipeSourceParametersSelfManagedKafkaParametersVpc"], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalBootstrapServers")
    def additional_bootstrap_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalBootstrapServers"))

    @additional_bootstrap_servers.setter
    def additional_bootstrap_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5410d7f5133c36d9cedb144efd89891efb07143819627de6152f602aa4d49ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalBootstrapServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092a682bb3e29118bd6f5840965fa6440aa60a1f06ce660c98ef36c5ec617cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159e8478b7c70f84c85bac4e57c1d3df7f40229db061fb743b59202e226022ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2407af6ffa2a2ff9d08af0241303d129187f20ed975b20b7f896bf24f7989b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverRootCaCertificate")
    def server_root_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverRootCaCertificate"))

    @server_root_ca_certificate.setter
    def server_root_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c070d6bd1df50e87ebc6659f035e7438ef39c8bce21832db2daaf17ee086659a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverRootCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91f4058094925c85489cafc913d21a344b911e8c9865ca836aa21d5375517e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e4d51004ddf826d5c3646ee0314d339f8dfac31b69aca55b39902788074098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c6eff7400a43ff2548172099f61c7d5e6719dc9014279d48241c0a3f7f60b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersVpc",
    jsii_struct_bases=[],
    name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
)
class PipesPipeSourceParametersSelfManagedKafkaParametersVpc:
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d582535e185553e2fd9134c887faa1372838aecf67d05e5d066ed77a02485e)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.'''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSelfManagedKafkaParametersVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5978d89445306248f3559e74b186926e4d6ed930047076ecc28c7b1edfe5f30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSubnets")
    def reset_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnets", []))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e36408451997903984d4e4c238c01e54b7f8eb025c499bef7060cdb9db290ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baca39933f7cfaba9906369bde2d087696707222ed84a0c0214c334a120a6efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75356f0fcab0f63d45a6bb9b81ff165f18487cf8c913e96ac4e90bf109d6f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSqsQueueParameters",
    jsii_struct_bases=[],
    name_mapping={
        "batch_size": "batchSize",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
    },
)
class PipesPipeSourceParametersSqsQueueParameters:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c562074a6bec572bc8010a9eb86cb9ee8883fd4836be2a3f13513f3dbcace0a9)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_size PipesPipe#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#maximum_batching_window_in_seconds PipesPipe#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeSourceParametersSqsQueueParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeSourceParametersSqsQueueParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeSourceParametersSqsQueueParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b6b8442cdc59b96a249246776419aaf78c31b5add950b89c9df3ae8746a60d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSecondsInput")
    def maximum_batching_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBatchingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46c341f29621d8bb0bd1365efd8d4b47585ecd47cd8464e42b8226f3fbbf877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e255847aaec34b61c2f256ef9645c1d134264246f2cb0f67ad2041bd39edd8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeSourceParametersSqsQueueParameters]:
        return typing.cast(typing.Optional[PipesPipeSourceParametersSqsQueueParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeSourceParametersSqsQueueParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4183d600871595d8bef51338f0c75f7700338c975536b5fb087d12edfa4237a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "batch_job_parameters": "batchJobParameters",
        "cloudwatch_logs_parameters": "cloudwatchLogsParameters",
        "ecs_task_parameters": "ecsTaskParameters",
        "eventbridge_event_bus_parameters": "eventbridgeEventBusParameters",
        "http_parameters": "httpParameters",
        "input_template": "inputTemplate",
        "kinesis_stream_parameters": "kinesisStreamParameters",
        "lambda_function_parameters": "lambdaFunctionParameters",
        "redshift_data_parameters": "redshiftDataParameters",
        "sagemaker_pipeline_parameters": "sagemakerPipelineParameters",
        "sqs_queue_parameters": "sqsQueueParameters",
        "step_function_state_machine_parameters": "stepFunctionStateMachineParameters",
    },
)
class PipesPipeTargetParameters:
    def __init__(
        self,
        *,
        batch_job_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersCloudwatchLogsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_task_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        eventbridge_event_bus_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersEventbridgeEventBusParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        http_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        input_template: typing.Optional[builtins.str] = None,
        kinesis_stream_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersKinesisStreamParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersLambdaFunctionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_data_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersRedshiftDataParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sagemaker_pipeline_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSagemakerPipelineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersSqsQueueParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        step_function_state_machine_parameters: typing.Optional[typing.Union["PipesPipeTargetParametersStepFunctionStateMachineParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_job_parameters: batch_job_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_job_parameters PipesPipe#batch_job_parameters}
        :param cloudwatch_logs_parameters: cloudwatch_logs_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cloudwatch_logs_parameters PipesPipe#cloudwatch_logs_parameters}
        :param ecs_task_parameters: ecs_task_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#ecs_task_parameters PipesPipe#ecs_task_parameters}
        :param eventbridge_event_bus_parameters: eventbridge_event_bus_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#eventbridge_event_bus_parameters PipesPipe#eventbridge_event_bus_parameters}
        :param http_parameters: http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        :param input_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.
        :param kinesis_stream_parameters: kinesis_stream_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        :param lambda_function_parameters: lambda_function_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#lambda_function_parameters PipesPipe#lambda_function_parameters}
        :param redshift_data_parameters: redshift_data_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#redshift_data_parameters PipesPipe#redshift_data_parameters}
        :param sagemaker_pipeline_parameters: sagemaker_pipeline_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sagemaker_pipeline_parameters PipesPipe#sagemaker_pipeline_parameters}
        :param sqs_queue_parameters: sqs_queue_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        :param step_function_state_machine_parameters: step_function_state_machine_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#step_function_state_machine_parameters PipesPipe#step_function_state_machine_parameters}
        '''
        if isinstance(batch_job_parameters, dict):
            batch_job_parameters = PipesPipeTargetParametersBatchJobParameters(**batch_job_parameters)
        if isinstance(cloudwatch_logs_parameters, dict):
            cloudwatch_logs_parameters = PipesPipeTargetParametersCloudwatchLogsParameters(**cloudwatch_logs_parameters)
        if isinstance(ecs_task_parameters, dict):
            ecs_task_parameters = PipesPipeTargetParametersEcsTaskParameters(**ecs_task_parameters)
        if isinstance(eventbridge_event_bus_parameters, dict):
            eventbridge_event_bus_parameters = PipesPipeTargetParametersEventbridgeEventBusParameters(**eventbridge_event_bus_parameters)
        if isinstance(http_parameters, dict):
            http_parameters = PipesPipeTargetParametersHttpParameters(**http_parameters)
        if isinstance(kinesis_stream_parameters, dict):
            kinesis_stream_parameters = PipesPipeTargetParametersKinesisStreamParameters(**kinesis_stream_parameters)
        if isinstance(lambda_function_parameters, dict):
            lambda_function_parameters = PipesPipeTargetParametersLambdaFunctionParameters(**lambda_function_parameters)
        if isinstance(redshift_data_parameters, dict):
            redshift_data_parameters = PipesPipeTargetParametersRedshiftDataParameters(**redshift_data_parameters)
        if isinstance(sagemaker_pipeline_parameters, dict):
            sagemaker_pipeline_parameters = PipesPipeTargetParametersSagemakerPipelineParameters(**sagemaker_pipeline_parameters)
        if isinstance(sqs_queue_parameters, dict):
            sqs_queue_parameters = PipesPipeTargetParametersSqsQueueParameters(**sqs_queue_parameters)
        if isinstance(step_function_state_machine_parameters, dict):
            step_function_state_machine_parameters = PipesPipeTargetParametersStepFunctionStateMachineParameters(**step_function_state_machine_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517264ccc4ab8f4865339a0ab5ecd726595b2ec241e126f0f71e7479bb9c1455)
            check_type(argname="argument batch_job_parameters", value=batch_job_parameters, expected_type=type_hints["batch_job_parameters"])
            check_type(argname="argument cloudwatch_logs_parameters", value=cloudwatch_logs_parameters, expected_type=type_hints["cloudwatch_logs_parameters"])
            check_type(argname="argument ecs_task_parameters", value=ecs_task_parameters, expected_type=type_hints["ecs_task_parameters"])
            check_type(argname="argument eventbridge_event_bus_parameters", value=eventbridge_event_bus_parameters, expected_type=type_hints["eventbridge_event_bus_parameters"])
            check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
            check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
            check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
            check_type(argname="argument lambda_function_parameters", value=lambda_function_parameters, expected_type=type_hints["lambda_function_parameters"])
            check_type(argname="argument redshift_data_parameters", value=redshift_data_parameters, expected_type=type_hints["redshift_data_parameters"])
            check_type(argname="argument sagemaker_pipeline_parameters", value=sagemaker_pipeline_parameters, expected_type=type_hints["sagemaker_pipeline_parameters"])
            check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
            check_type(argname="argument step_function_state_machine_parameters", value=step_function_state_machine_parameters, expected_type=type_hints["step_function_state_machine_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_job_parameters is not None:
            self._values["batch_job_parameters"] = batch_job_parameters
        if cloudwatch_logs_parameters is not None:
            self._values["cloudwatch_logs_parameters"] = cloudwatch_logs_parameters
        if ecs_task_parameters is not None:
            self._values["ecs_task_parameters"] = ecs_task_parameters
        if eventbridge_event_bus_parameters is not None:
            self._values["eventbridge_event_bus_parameters"] = eventbridge_event_bus_parameters
        if http_parameters is not None:
            self._values["http_parameters"] = http_parameters
        if input_template is not None:
            self._values["input_template"] = input_template
        if kinesis_stream_parameters is not None:
            self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
        if lambda_function_parameters is not None:
            self._values["lambda_function_parameters"] = lambda_function_parameters
        if redshift_data_parameters is not None:
            self._values["redshift_data_parameters"] = redshift_data_parameters
        if sagemaker_pipeline_parameters is not None:
            self._values["sagemaker_pipeline_parameters"] = sagemaker_pipeline_parameters
        if sqs_queue_parameters is not None:
            self._values["sqs_queue_parameters"] = sqs_queue_parameters
        if step_function_state_machine_parameters is not None:
            self._values["step_function_state_machine_parameters"] = step_function_state_machine_parameters

    @builtins.property
    def batch_job_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParameters"]:
        '''batch_job_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#batch_job_parameters PipesPipe#batch_job_parameters}
        '''
        result = self._values.get("batch_job_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParameters"], result)

    @builtins.property
    def cloudwatch_logs_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersCloudwatchLogsParameters"]:
        '''cloudwatch_logs_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cloudwatch_logs_parameters PipesPipe#cloudwatch_logs_parameters}
        '''
        result = self._values.get("cloudwatch_logs_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersCloudwatchLogsParameters"], result)

    @builtins.property
    def ecs_task_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParameters"]:
        '''ecs_task_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#ecs_task_parameters PipesPipe#ecs_task_parameters}
        '''
        result = self._values.get("ecs_task_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParameters"], result)

    @builtins.property
    def eventbridge_event_bus_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEventbridgeEventBusParameters"]:
        '''eventbridge_event_bus_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#eventbridge_event_bus_parameters PipesPipe#eventbridge_event_bus_parameters}
        '''
        result = self._values.get("eventbridge_event_bus_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEventbridgeEventBusParameters"], result)

    @builtins.property
    def http_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersHttpParameters"]:
        '''http_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#http_parameters PipesPipe#http_parameters}
        '''
        result = self._values.get("http_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersHttpParameters"], result)

    @builtins.property
    def input_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#input_template PipesPipe#input_template}.'''
        result = self._values.get("input_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis_stream_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersKinesisStreamParameters"]:
        '''kinesis_stream_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#kinesis_stream_parameters PipesPipe#kinesis_stream_parameters}
        '''
        result = self._values.get("kinesis_stream_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersKinesisStreamParameters"], result)

    @builtins.property
    def lambda_function_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersLambdaFunctionParameters"]:
        '''lambda_function_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#lambda_function_parameters PipesPipe#lambda_function_parameters}
        '''
        result = self._values.get("lambda_function_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersLambdaFunctionParameters"], result)

    @builtins.property
    def redshift_data_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"]:
        '''redshift_data_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#redshift_data_parameters PipesPipe#redshift_data_parameters}
        '''
        result = self._values.get("redshift_data_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"], result)

    @builtins.property
    def sagemaker_pipeline_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"]:
        '''sagemaker_pipeline_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sagemaker_pipeline_parameters PipesPipe#sagemaker_pipeline_parameters}
        '''
        result = self._values.get("sagemaker_pipeline_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"], result)

    @builtins.property
    def sqs_queue_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSqsQueueParameters"]:
        '''sqs_queue_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqs_queue_parameters PipesPipe#sqs_queue_parameters}
        '''
        result = self._values.get("sqs_queue_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersSqsQueueParameters"], result)

    @builtins.property
    def step_function_state_machine_parameters(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"]:
        '''step_function_state_machine_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#step_function_state_machine_parameters PipesPipe#step_function_state_machine_parameters}
        '''
        result = self._values.get("step_function_state_machine_parameters")
        return typing.cast(typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParameters",
    jsii_struct_bases=[],
    name_mapping={
        "job_definition": "jobDefinition",
        "job_name": "jobName",
        "array_properties": "arrayProperties",
        "container_overrides": "containerOverrides",
        "depends_on": "dependsOn",
        "parameters": "parameters",
        "retry_strategy": "retryStrategy",
    },
)
class PipesPipeTargetParametersBatchJobParameters:
    def __init__(
        self,
        *,
        job_definition: builtins.str,
        job_name: builtins.str,
        array_properties: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParametersArrayProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        container_overrides: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        depends_on: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersDependsOn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry_strategy: typing.Optional[typing.Union["PipesPipeTargetParametersBatchJobParametersRetryStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_definition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_definition PipesPipe#job_definition}.
        :param job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_name PipesPipe#job_name}.
        :param array_properties: array_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#array_properties PipesPipe#array_properties}
        :param container_overrides: container_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#container_overrides PipesPipe#container_overrides}
        :param depends_on: depends_on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#depends_on PipesPipe#depends_on}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parameters PipesPipe#parameters}.
        :param retry_strategy: retry_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#retry_strategy PipesPipe#retry_strategy}
        '''
        if isinstance(array_properties, dict):
            array_properties = PipesPipeTargetParametersBatchJobParametersArrayProperties(**array_properties)
        if isinstance(container_overrides, dict):
            container_overrides = PipesPipeTargetParametersBatchJobParametersContainerOverrides(**container_overrides)
        if isinstance(retry_strategy, dict):
            retry_strategy = PipesPipeTargetParametersBatchJobParametersRetryStrategy(**retry_strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d507ab3e09c043407350c30d370115ca64b7f563e39325ad9b008412952649f0)
            check_type(argname="argument job_definition", value=job_definition, expected_type=type_hints["job_definition"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument array_properties", value=array_properties, expected_type=type_hints["array_properties"])
            check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_definition": job_definition,
            "job_name": job_name,
        }
        if array_properties is not None:
            self._values["array_properties"] = array_properties
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy

    @builtins.property
    def job_definition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_definition PipesPipe#job_definition}.'''
        result = self._values.get("job_definition")
        assert result is not None, "Required property 'job_definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_name PipesPipe#job_name}.'''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def array_properties(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersArrayProperties"]:
        '''array_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#array_properties PipesPipe#array_properties}
        '''
        result = self._values.get("array_properties")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersArrayProperties"], result)

    @builtins.property
    def container_overrides(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersContainerOverrides"]:
        '''container_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#container_overrides PipesPipe#container_overrides}
        '''
        result = self._values.get("container_overrides")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersContainerOverrides"], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersDependsOn"]]]:
        '''depends_on block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#depends_on PipesPipe#depends_on}
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersDependsOn"]]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parameters PipesPipe#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def retry_strategy(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"]:
        '''retry_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#retry_strategy PipesPipe#retry_strategy}
        '''
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersArrayProperties",
    jsii_struct_bases=[],
    name_mapping={"size": "size"},
)
class PipesPipeTargetParametersBatchJobParametersArrayProperties:
    def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#size PipesPipe#size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab124f5d102ad05e9ce981b3fd55ad3c2669bb71004c033311ae184d54d1218c)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#size PipesPipe#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersArrayProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eddc03d34b3d1621e2053d3a01b8afe4d57d02a294817ea6f67555b7aa385e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad9bda15236fc12e0fd91a019bdc322f627eed36f3d2f8c27627f7c5d139d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72063a9a4d118a97c2073e50ee661c6d434b3c4913eb53bd1d83c697988b8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "environment": "environment",
        "instance_type": "instanceType",
        "resource_requirement": "resourceRequirement",
    },
)
class PipesPipeTargetParametersBatchJobParametersContainerOverrides:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#command PipesPipe#command}.
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#instance_type PipesPipe#instance_type}.
        :param resource_requirement: resource_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d124d87cc47d182f3e94b6650ad7d47475e5c0ef62d215f5067a72446e9f046d)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument resource_requirement", value=resource_requirement, expected_type=type_hints["resource_requirement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if resource_requirement is not None:
            self._values["resource_requirement"] = resource_requirement

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#command PipesPipe#command}.'''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment"]]]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment"]]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#instance_type PipesPipe#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_requirement(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]]:
        '''resource_requirement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        result = self._values.get("resource_requirement")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersContainerOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10167ad770981379de62d6c2b29c1ab3e8a6ba8fb186075f977cc7e23daca749)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__611439f1aab7609392489478f7ffbfe35569cc6dc94a741bef77e43127e6ec8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e99ea5e18fab78099549244b4d7698b7c4ff3ad264be409947858423d9bf229)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beab07798bc7b95fd9d6b49c29387ad51d24b9b034cc3b4f3218f2208fe8deae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ed8e8d839824a98c315cb4b5836f94a1258db5879e4103b29a1141437fc927a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e959caadd6d03e9aa576ee646abb8dd233e2ecfb87b8aed29dd53878d74bfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3bd6193d7dc5779c221089a7674951eada601e9a2a94f099944a51664248ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9f668b9abf0d4450083cd01fe5492ea9121092d5ee23be1d08fe12ccb616ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3e84314f9eda9356706949b4890c424904fe38e52acefba7bace849fe52e5dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbf3563a9189eca9f9cad68f3224ee03d039663161bb8a45277d04a4172b149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd47584158b589386a951522f9e45fd60ccbce0ccb0b041815ac5f9a0a618e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa72e3d7d1b7ccd28ada300ff7c09eb02d0d3da3c353430e076714ce31a956d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25fd2621d59a2d71cf6637a5c16fab8e379d37861773297867432b832f13633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putResourceRequirement")
    def put_resource_requirement(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3affc2cf9068a62197fa822f084d0cf46ae6979d2d3d2f59d9fd9b3a8c1469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceRequirement", [value]))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetResourceRequirement")
    def reset_resource_requirement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceRequirement", []))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirement")
    def resource_requirement(
        self,
    ) -> "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList":
        return typing.cast("PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList", jsii.get(self, "resourceRequirement"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirementInput")
    def resource_requirement_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement"]]], jsii.get(self, "resourceRequirementInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a663b3be7cfb9dae96ad2b8c7f1b433d9a16f7d146cd213fb51db3abdfe7ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1994b747aa42807ca3da38d3de8665829c640567b9c6972513721fb3e979c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098df9d4e26cf84a8a7acb552361b688c93f8a82b2cf346d7415ab5442e30665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b247381962513f50e69b1c3d8e437826ced6420aff91fe39f816bde8df03024)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a1a70f9238f4694d021d9ef362ed7e04891730a6b5c09f60bad8c9dca291668)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cfc952741464f858abcb5a614da66bd48ebdb3b8a37f4e8b3aec7937ae5cef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319905867a59a794c5330d9f51ce02ac92de277a7f96d0f66ca916cf3d6c370b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__560d8d2b2eb7d688ee184eeb9bb82e138cce7bc19387c1b9f8dc611dbfb5fd7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfb61deeb17c5e2ff4bd1349f7aa259d4539a1c6cc2f3d98d759969a337596f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53deb18ca68b556f5e92444fb7815e7c917486d3d94b9b7c189029858d92905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45186ffa937c8d0bb29071b26f2273c815bd3238ed09eff8d889801d12cf0495)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ab39fbb724346682a53cf62327aabe7c0590baf0dd799a51824c7932852a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec2e1453102c0a460d1781418ecbfb0489dd5ed25ca179405fe5bd9150ac43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91235bdd666c571f30d65288bfad4125fc97622a02b0e05a7eeb5701b0bedfc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersDependsOn",
    jsii_struct_bases=[],
    name_mapping={"job_id": "jobId", "type": "type"},
)
class PipesPipeTargetParametersBatchJobParametersDependsOn:
    def __init__(
        self,
        *,
        job_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_id PipesPipe#job_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b24bee1c386c3466f9bb2072be07c0f1c0cc76ae59fc6b357d3b38091c8633)
            check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_id is not None:
            self._values["job_id"] = job_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_id PipesPipe#job_id}.'''
        result = self._values.get("job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersDependsOn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersDependsOnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersDependsOnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13f86fe68d93c3c02d302b25fd7d8c80fa238b4c930635123da339848d68ecc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a8f3e4763a5ff9871012d8f44aa76f012200197a807f0701c32e0ca49641bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc284ca9ddf885440b55c1a0b401f5b09450b11cfa255d56b204106dea89befe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f10e8caf6935dcb4347b04b2ae69a5d478cdac7556cbe7fadfb428ee83e2c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__646285afee39c3fe255e6c4775d0e49c0c29a7711f0c70a7b074f0e70fe15517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347afbb6f02578fd6f0fa7cd4b6f0f6a8397c274be38129324c14557f8ec8ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c86d6753b5c5c7ac20a094a1f7d874df060f3e729d4fc3a6fb9883daa879cb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetJobId")
    def reset_job_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="jobIdInput")
    def job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce04ecdbdc34adf6299633ed716900449168e378e9b68fa0eefe46bf7e761206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca0335cedecc72a890f5ab35adc1453aac356c971566488564b909a755c938e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e474b86804e11b62fb7f413ef1ab666d4087f41db2fafcba8487ececa82854e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersBatchJobParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84e3d7dc770572b4ebfc8352cda7c9288fafbc2ab29e9dccdad7780acb5bb752)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArrayProperties")
    def put_array_properties(
        self,
        *,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#size PipesPipe#size}.
        '''
        value = PipesPipeTargetParametersBatchJobParametersArrayProperties(size=size)

        return typing.cast(None, jsii.invoke(self, "putArrayProperties", [value]))

    @jsii.member(jsii_name="putContainerOverrides")
    def put_container_overrides(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#command PipesPipe#command}.
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#instance_type PipesPipe#instance_type}.
        :param resource_requirement: resource_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        value = PipesPipeTargetParametersBatchJobParametersContainerOverrides(
            command=command,
            environment=environment,
            instance_type=instance_type,
            resource_requirement=resource_requirement,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerOverrides", [value]))

    @jsii.member(jsii_name="putDependsOn")
    def put_depends_on(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694b1fae9c222bd4ba6607a4b11eaf898d86cfb0aaa9cf90860171c0832a2258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDependsOn", [value]))

    @jsii.member(jsii_name="putRetryStrategy")
    def put_retry_strategy(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#attempts PipesPipe#attempts}.
        '''
        value = PipesPipeTargetParametersBatchJobParametersRetryStrategy(
            attempts=attempts
        )

        return typing.cast(None, jsii.invoke(self, "putRetryStrategy", [value]))

    @jsii.member(jsii_name="resetArrayProperties")
    def reset_array_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayProperties", []))

    @jsii.member(jsii_name="resetContainerOverrides")
    def reset_container_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerOverrides", []))

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetRetryStrategy")
    def reset_retry_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="arrayProperties")
    def array_properties(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference, jsii.get(self, "arrayProperties"))

    @builtins.property
    @jsii.member(jsii_name="containerOverrides")
    def container_overrides(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference, jsii.get(self, "containerOverrides"))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> PipesPipeTargetParametersBatchJobParametersDependsOnList:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersDependsOnList, jsii.get(self, "dependsOn"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategy")
    def retry_strategy(
        self,
    ) -> "PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference":
        return typing.cast("PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference", jsii.get(self, "retryStrategy"))

    @builtins.property
    @jsii.member(jsii_name="arrayPropertiesInput")
    def array_properties_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties], jsii.get(self, "arrayPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerOverridesInput")
    def container_overrides_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides], jsii.get(self, "containerOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="dependsOnInput")
    def depends_on_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]], jsii.get(self, "dependsOnInput"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionInput")
    def job_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNameInput")
    def job_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategyInput")
    def retry_strategy_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersBatchJobParametersRetryStrategy"], jsii.get(self, "retryStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinition")
    def job_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobDefinition"))

    @job_definition.setter
    def job_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c0fb74e0b269f73b733b021373b6e0b036abb4ad901c1ee511791b8bb90520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e6d9842f8d328565bb8068bc35aa43c9c95041e7a4c3f7094f30f598d7e9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c3334236401edea72e51ccaea760c3bd5f327687e47f190a6be7c3f8aa0df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25297960bbc40132218b23e481713f4cc9ec865b3c2e71c49222779684fa902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersRetryStrategy",
    jsii_struct_bases=[],
    name_mapping={"attempts": "attempts"},
)
class PipesPipeTargetParametersBatchJobParametersRetryStrategy:
    def __init__(self, *, attempts: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#attempts PipesPipe#attempts}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6378cbb14a0a38a00b8bd631e770025765b609d064a2ed7b8cff0405383957)
            check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#attempts PipesPipe#attempts}.'''
        result = self._values.get("attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersBatchJobParametersRetryStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b3028597cf87105263db0a47468cf3664958702b5ceeef16c371b49a54558b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttempts")
    def reset_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttempts", []))

    @builtins.property
    @jsii.member(jsii_name="attemptsInput")
    def attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "attemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="attempts")
    def attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "attempts"))

    @attempts.setter
    def attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0469de7aea9d0df25936fc1afe9578459a7343327e41e20137258b8ff53e13c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630e9dee51b08585bc5b91df62c1e1894238753d409d1774d34bd8844e877bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersCloudwatchLogsParameters",
    jsii_struct_bases=[],
    name_mapping={"log_stream_name": "logStreamName", "timestamp": "timestamp"},
)
class PipesPipeTargetParametersCloudwatchLogsParameters:
    def __init__(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_stream_name PipesPipe#log_stream_name}.
        :param timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#timestamp PipesPipe#timestamp}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d33089d04cb02df362af27cbbe24a9418e21b9379930590ed0c5621e2885fcc)
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_stream_name PipesPipe#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#timestamp PipesPipe#timestamp}.'''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersCloudwatchLogsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersCloudwatchLogsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersCloudwatchLogsParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6589b9c514d88033a49b6377468e067a72b7622abcbfc6e24f8da4c752d636a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a39289fed8ad65770be5e92b245ab9189a08a7ae7e653822facc3dce6af9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceedecdcb238e4762c9a8550cee02cea282fd372afe18923dd04dc041d3aeb46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190143b9999f7af0e599feae8b53ab32663ad8e4ed91f29dbe2a21edbe89d170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParameters",
    jsii_struct_bases=[],
    name_mapping={
        "task_definition_arn": "taskDefinitionArn",
        "capacity_provider_strategy": "capacityProviderStrategy",
        "enable_ecs_managed_tags": "enableEcsManagedTags",
        "enable_execute_command": "enableExecuteCommand",
        "group": "group",
        "launch_type": "launchType",
        "network_configuration": "networkConfiguration",
        "overrides": "overrides",
        "placement_constraint": "placementConstraint",
        "placement_strategy": "placementStrategy",
        "platform_version": "platformVersion",
        "propagate_tags": "propagateTags",
        "reference_id": "referenceId",
        "tags": "tags",
        "task_count": "taskCount",
    },
)
class PipesPipeTargetParametersEcsTaskParameters:
    def __init__(
        self,
        *,
        task_definition_arn: builtins.str,
        capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_execute_command: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group: typing.Optional[builtins.str] = None,
        launch_type: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        placement_constraint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        platform_version: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.str] = None,
        reference_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param task_definition_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_definition_arn PipesPipe#task_definition_arn}.
        :param capacity_provider_strategy: capacity_provider_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#capacity_provider_strategy PipesPipe#capacity_provider_strategy}
        :param enable_ecs_managed_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enable_ecs_managed_tags PipesPipe#enable_ecs_managed_tags}.
        :param enable_execute_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enable_execute_command PipesPipe#enable_execute_command}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#group PipesPipe#group}.
        :param launch_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#launch_type PipesPipe#launch_type}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#network_configuration PipesPipe#network_configuration}
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#overrides PipesPipe#overrides}
        :param placement_constraint: placement_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#placement_constraint PipesPipe#placement_constraint}
        :param placement_strategy: placement_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#placement_strategy PipesPipe#placement_strategy}
        :param platform_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#platform_version PipesPipe#platform_version}.
        :param propagate_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#propagate_tags PipesPipe#propagate_tags}.
        :param reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#reference_id PipesPipe#reference_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param task_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_count PipesPipe#task_count}.
        '''
        if isinstance(network_configuration, dict):
            network_configuration = PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration(**network_configuration)
        if isinstance(overrides, dict):
            overrides = PipesPipeTargetParametersEcsTaskParametersOverrides(**overrides)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1a05199a24e51ae60e3cadb3fe5891a2ef0036620c211715de72268356f38f)
            check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
            check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument placement_constraint", value=placement_constraint, expected_type=type_hints["placement_constraint"])
            check_type(argname="argument placement_strategy", value=placement_strategy, expected_type=type_hints["placement_strategy"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition_arn": task_definition_arn,
        }
        if capacity_provider_strategy is not None:
            self._values["capacity_provider_strategy"] = capacity_provider_strategy
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_execute_command is not None:
            self._values["enable_execute_command"] = enable_execute_command
        if group is not None:
            self._values["group"] = group
        if launch_type is not None:
            self._values["launch_type"] = launch_type
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if overrides is not None:
            self._values["overrides"] = overrides
        if placement_constraint is not None:
            self._values["placement_constraint"] = placement_constraint
        if placement_strategy is not None:
            self._values["placement_strategy"] = placement_strategy
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if reference_id is not None:
            self._values["reference_id"] = reference_id
        if tags is not None:
            self._values["tags"] = tags
        if task_count is not None:
            self._values["task_count"] = task_count

    @builtins.property
    def task_definition_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_definition_arn PipesPipe#task_definition_arn}.'''
        result = self._values.get("task_definition_arn")
        assert result is not None, "Required property 'task_definition_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy"]]]:
        '''capacity_provider_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#capacity_provider_strategy PipesPipe#capacity_provider_strategy}
        '''
        result = self._values.get("capacity_provider_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy"]]], result)

    @builtins.property
    def enable_ecs_managed_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enable_ecs_managed_tags PipesPipe#enable_ecs_managed_tags}.'''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_execute_command(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enable_execute_command PipesPipe#enable_execute_command}.'''
        result = self._values.get("enable_execute_command")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#group PipesPipe#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#launch_type PipesPipe#launch_type}.'''
        result = self._values.get("launch_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration"]:
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#network_configuration PipesPipe#network_configuration}
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration"], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"]:
        '''overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#overrides PipesPipe#overrides}
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"], result)

    @builtins.property
    def placement_constraint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]]:
        '''placement_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#placement_constraint PipesPipe#placement_constraint}
        '''
        result = self._values.get("placement_constraint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]], result)

    @builtins.property
    def placement_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]]:
        '''placement_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#placement_strategy PipesPipe#placement_strategy}
        '''
        result = self._values.get("placement_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]], result)

    @builtins.property
    def platform_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#platform_version PipesPipe#platform_version}.'''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#propagate_tags PipesPipe#propagate_tags}.'''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#reference_id PipesPipe#reference_id}.'''
        result = self._values.get("reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_count PipesPipe#task_count}.'''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_provider": "capacityProvider",
        "base": "base",
        "weight": "weight",
    },
)
class PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy:
    def __init__(
        self,
        *,
        capacity_provider: builtins.str,
        base: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param capacity_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#capacity_provider PipesPipe#capacity_provider}.
        :param base: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#base PipesPipe#base}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#weight PipesPipe#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661756089b5d97eab601c57bb1bc934e252e220a16e289398975e36f2e708065)
            check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_provider": capacity_provider,
        }
        if base is not None:
            self._values["base"] = base
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def capacity_provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#capacity_provider PipesPipe#capacity_provider}.'''
        result = self._values.get("capacity_provider")
        assert result is not None, "Required property 'capacity_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#base PipesPipe#base}.'''
        result = self._values.get("base")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#weight PipesPipe#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__080a2b80105173f00ad5d29b7ec9d2926d0418052bf4cffb1a1cefac02b63b0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b2d8787e9c08714022ad22e7e004d36fdab737cfafaa83e82e8d5f8b3938077)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edb4cd4f4c95695aa8f81528c61714cc8a8ab96d5036a61a2458ae2d7ae9df5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f0c173a638f2595045c45ed659a07e512e76b0229089dd5e6bf56c766407ea9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad0980c3a57ce4a0b5ab2e55933c104156d79e6b6f9dcc8aa4331c43b029dabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253b7e1d3eb8167d15bfd7ba65b8708fea832945a281c448b63dc2d3c0f52602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1ecca2a88f7899ae35d7136fa6587cd18fc2baa35f3a4d991cf76f11c1b0a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBase")
    def reset_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="baseInput")
    def base_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "baseInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderInput")
    def capacity_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="base")
    def base(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "base"))

    @base.setter
    def base(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069e2b04f89d5390e9eb6ee37719782480a72ea67e02e60092011f34e041a338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "base", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityProvider")
    def capacity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityProvider"))

    @capacity_provider.setter
    def capacity_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c9df6a6cc26c6946468bbfb79e070dc463dd4fd6434faf4dd7527379ddc0b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789b18fc675b4f5955e0b4a30e6b308410ecef4b7c752d284997a498bf29afef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824fc3c4ec6caf4fed16b7aadce67168e524f44b56efc650dce52c77b3680be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"aws_vpc_configuration": "awsVpcConfiguration"},
)
class PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration:
    def __init__(
        self,
        *,
        aws_vpc_configuration: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_vpc_configuration: aws_vpc_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#aws_vpc_configuration PipesPipe#aws_vpc_configuration}
        '''
        if isinstance(aws_vpc_configuration, dict):
            aws_vpc_configuration = PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration(**aws_vpc_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ed8b695734cbba1ab90ce7a0d375e9b2195560badf47344c0ad379fa2475e0)
            check_type(argname="argument aws_vpc_configuration", value=aws_vpc_configuration, expected_type=type_hints["aws_vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_vpc_configuration is not None:
            self._values["aws_vpc_configuration"] = aws_vpc_configuration

    @builtins.property
    def aws_vpc_configuration(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration"]:
        '''aws_vpc_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#aws_vpc_configuration PipesPipe#aws_vpc_configuration}
        '''
        result = self._values.get("aws_vpc_configuration")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assign_public_ip": "assignPublicIp",
        "security_groups": "securityGroups",
        "subnets": "subnets",
    },
)
class PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration:
    def __init__(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assign_public_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#assign_public_ip PipesPipe#assign_public_ip}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4e9b3763362c4d316fcfc948c5b35e3a7a0ec27df3e68093e33b75e688a5c9)
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#assign_public_ip PipesPipe#assign_public_ip}.'''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.'''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a165ae2c2467dc103d344ee49390a8e70d30f3cfce6d98331575b98dae571cb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAssignPublicIp")
    def reset_assign_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignPublicIp", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSubnets")
    def reset_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnets", []))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIpInput")
    def assign_public_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assignPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assignPublicIp"))

    @assign_public_ip.setter
    def assign_public_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc696a46c0eff0a25e0d08e891ceaec15fee4d8455090ec2d9c1f333fe992f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignPublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c315ac80e8dce8fe20513e23ac2528f23b46f84f0a666ced3259c19be470a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2be006ca9d70b9d8effea956991ec54d7ff1da09fdf555af56f4b5171472ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8d6d239a4092d84c8861e2854bb2d4cba53d152be14602284c79f107e533bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2130de0f148d13c3d5581b2138bf523275f56d563e13da825109e27623ac57ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsVpcConfiguration")
    def put_aws_vpc_configuration(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assign_public_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#assign_public_ip PipesPipe#assign_public_ip}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#security_groups PipesPipe#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#subnets PipesPipe#subnets}.
        '''
        value = PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration(
            assign_public_ip=assign_public_ip,
            security_groups=security_groups,
            subnets=subnets,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsVpcConfiguration", [value]))

    @jsii.member(jsii_name="resetAwsVpcConfiguration")
    def reset_aws_vpc_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsVpcConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="awsVpcConfiguration")
    def aws_vpc_configuration(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference, jsii.get(self, "awsVpcConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="awsVpcConfigurationInput")
    def aws_vpc_configuration_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration], jsii.get(self, "awsVpcConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dec30e6b074eb33a15c0d180ddfa55bfb09d98d2f91737590140133c85255d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac33f2bfbee99836198d6540000bc1ac3b0ccc5f2764984d9af9e89d792169a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCapacityProviderStrategy")
    def put_capacity_provider_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58623cbefb906f45dca683c4e7714ea073da6f3e1619de44604b27890814260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCapacityProviderStrategy", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        aws_vpc_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_vpc_configuration: aws_vpc_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#aws_vpc_configuration PipesPipe#aws_vpc_configuration}
        '''
        value = PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration(
            aws_vpc_configuration=aws_vpc_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putOverrides")
    def put_overrides(
        self,
        *,
        container_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        inference_accelerator_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[builtins.str] = None,
        task_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_override: container_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#container_override PipesPipe#container_override}
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.
        :param ephemeral_storage: ephemeral_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#ephemeral_storage PipesPipe#ephemeral_storage}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#execution_role_arn PipesPipe#execution_role_arn}.
        :param inference_accelerator_override: inference_accelerator_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#inference_accelerator_override PipesPipe#inference_accelerator_override}
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.
        :param task_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_role_arn PipesPipe#task_role_arn}.
        '''
        value = PipesPipeTargetParametersEcsTaskParametersOverrides(
            container_override=container_override,
            cpu=cpu,
            ephemeral_storage=ephemeral_storage,
            execution_role_arn=execution_role_arn,
            inference_accelerator_override=inference_accelerator_override,
            memory=memory,
            task_role_arn=task_role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putOverrides", [value]))

    @jsii.member(jsii_name="putPlacementConstraint")
    def put_placement_constraint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7083dcdc4a3e04ed11266f984e9a789e613a2caaefb88b499f8edf6d5bccabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlacementConstraint", [value]))

    @jsii.member(jsii_name="putPlacementStrategy")
    def put_placement_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae6bdd8125edcdc5f68424458f10d166484d2dd847cd4a6819bea299965d02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlacementStrategy", [value]))

    @jsii.member(jsii_name="resetCapacityProviderStrategy")
    def reset_capacity_provider_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityProviderStrategy", []))

    @jsii.member(jsii_name="resetEnableEcsManagedTags")
    def reset_enable_ecs_managed_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEcsManagedTags", []))

    @jsii.member(jsii_name="resetEnableExecuteCommand")
    def reset_enable_execute_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableExecuteCommand", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetLaunchType")
    def reset_launch_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchType", []))

    @jsii.member(jsii_name="resetNetworkConfiguration")
    def reset_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfiguration", []))

    @jsii.member(jsii_name="resetOverrides")
    def reset_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrides", []))

    @jsii.member(jsii_name="resetPlacementConstraint")
    def reset_placement_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementConstraint", []))

    @jsii.member(jsii_name="resetPlacementStrategy")
    def reset_placement_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementStrategy", []))

    @jsii.member(jsii_name="resetPlatformVersion")
    def reset_platform_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformVersion", []))

    @jsii.member(jsii_name="resetPropagateTags")
    def reset_propagate_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagateTags", []))

    @jsii.member(jsii_name="resetReferenceId")
    def reset_reference_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaskCount")
    def reset_task_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskCount", []))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderStrategy")
    def capacity_provider_strategy(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList, jsii.get(self, "capacityProviderStrategy"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference, jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference", jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="placementConstraint")
    def placement_constraint(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList", jsii.get(self, "placementConstraint"))

    @builtins.property
    @jsii.member(jsii_name="placementStrategy")
    def placement_strategy(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList", jsii.get(self, "placementStrategy"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderStrategyInput")
    def capacity_provider_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]], jsii.get(self, "capacityProviderStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEcsManagedTagsInput")
    def enable_ecs_managed_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEcsManagedTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableExecuteCommandInput")
    def enable_execute_command_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableExecuteCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="launchTypeInput")
    def launch_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="overridesInput")
    def overrides_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverrides"], jsii.get(self, "overridesInput"))

    @builtins.property
    @jsii.member(jsii_name="placementConstraintInput")
    def placement_constraint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementConstraint"]]], jsii.get(self, "placementConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="placementStrategyInput")
    def placement_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersPlacementStrategy"]]], jsii.get(self, "placementStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="platformVersionInput")
    def platform_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="propagateTagsInput")
    def propagate_tags_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propagateTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceIdInput")
    def reference_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referenceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskCountInput")
    def task_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskCountInput"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArnInput")
    def task_definition_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskDefinitionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEcsManagedTags")
    def enable_ecs_managed_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEcsManagedTags"))

    @enable_ecs_managed_tags.setter
    def enable_ecs_managed_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0285de38b2541026a75549cda6ca1b35b0bce0b0eeb3e62ed1b852b5c71c7bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEcsManagedTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableExecuteCommand")
    def enable_execute_command(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableExecuteCommand"))

    @enable_execute_command.setter
    def enable_execute_command(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d827ea2c75497374b4d6247a295c5d03c8fefa773317d9795fb7e7e55b2a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableExecuteCommand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b332eb362eb5c4c5424df659e4c8efeaeab55edb19954a9cb3df059a36822d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchType")
    def launch_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchType"))

    @launch_type.setter
    def launch_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c165dad139e6b96af351ea8c6a12d6980efbee5c7b52d0a309bc299e711639ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformVersion"))

    @platform_version.setter
    def platform_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980a496cd7703797ef5493d7d3ec4c4494efdec7089389707eb9f56af5a448c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "propagateTags"))

    @propagate_tags.setter
    def propagate_tags(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162ef8b588dc9a211fa066fa6d983b860a53a3d4b2c7802aadc0fc88cdad11cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referenceId")
    def reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceId"))

    @reference_id.setter
    def reference_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6f5608488ff4fce7569c755c84d3a9b2d153223019b4ac30c0fe139154854e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59b2380cc83296667d679e843368b15344a78aaf2207012c0ee5b3e779763ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskCount")
    def task_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskCount"))

    @task_count.setter
    def task_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac76d62b9c33a45aa793ba633e49b0ac976ec8e5d3f83ac398e9a19cb72b09fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskDefinitionArn"))

    @task_definition_arn.setter
    def task_definition_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae5e2e5f720e72815b8dbd8c04a19db8448e6151a323e8f821132c3a3da3de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskDefinitionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c69e5ca053a1ade0e5722e987b46a872756e5a10207fca627664046222e3db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "container_override": "containerOverride",
        "cpu": "cpu",
        "ephemeral_storage": "ephemeralStorage",
        "execution_role_arn": "executionRoleArn",
        "inference_accelerator_override": "inferenceAcceleratorOverride",
        "memory": "memory",
        "task_role_arn": "taskRoleArn",
    },
)
class PipesPipeTargetParametersEcsTaskParametersOverrides:
    def __init__(
        self,
        *,
        container_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        inference_accelerator_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[builtins.str] = None,
        task_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_override: container_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#container_override PipesPipe#container_override}
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.
        :param ephemeral_storage: ephemeral_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#ephemeral_storage PipesPipe#ephemeral_storage}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#execution_role_arn PipesPipe#execution_role_arn}.
        :param inference_accelerator_override: inference_accelerator_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#inference_accelerator_override PipesPipe#inference_accelerator_override}
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.
        :param task_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_role_arn PipesPipe#task_role_arn}.
        '''
        if isinstance(ephemeral_storage, dict):
            ephemeral_storage = PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage(**ephemeral_storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc0f097ace15c0b3afec310fbdfb66e32f0b8229f8fe3017d3c2c11210962ff)
            check_type(argname="argument container_override", value=container_override, expected_type=type_hints["container_override"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument inference_accelerator_override", value=inference_accelerator_override, expected_type=type_hints["inference_accelerator_override"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument task_role_arn", value=task_role_arn, expected_type=type_hints["task_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_override is not None:
            self._values["container_override"] = container_override
        if cpu is not None:
            self._values["cpu"] = cpu
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if inference_accelerator_override is not None:
            self._values["inference_accelerator_override"] = inference_accelerator_override
        if memory is not None:
            self._values["memory"] = memory
        if task_role_arn is not None:
            self._values["task_role_arn"] = task_role_arn

    @builtins.property
    def container_override(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride"]]]:
        '''container_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#container_override PipesPipe#container_override}
        '''
        result = self._values.get("container_override")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride"]]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral_storage(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage"]:
        '''ephemeral_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#ephemeral_storage PipesPipe#ephemeral_storage}
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional["PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage"], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#execution_role_arn PipesPipe#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_accelerator_override(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride"]]]:
        '''inference_accelerator_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#inference_accelerator_override PipesPipe#inference_accelerator_override}
        '''
        result = self._values.get("inference_accelerator_override")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride"]]], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_role_arn PipesPipe#task_role_arn}.'''
        result = self._values.get("task_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "cpu": "cpu",
        "environment": "environment",
        "environment_file": "environmentFile",
        "memory": "memory",
        "memory_reservation": "memoryReservation",
        "name": "name",
        "resource_requirement": "resourceRequirement",
    },
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#command PipesPipe#command}.
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        :param environment_file: environment_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment_file PipesPipe#environment_file}
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.
        :param memory_reservation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory_reservation PipesPipe#memory_reservation}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param resource_requirement: resource_requirement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad2028fe7aeb2abe4fb4c7e769e582180f6032e74ee05c4d78b76a33805ce30)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_file", value=environment_file, expected_type=type_hints["environment_file"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_requirement", value=resource_requirement, expected_type=type_hints["resource_requirement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if environment is not None:
            self._values["environment"] = environment
        if environment_file is not None:
            self._values["environment_file"] = environment_file
        if memory is not None:
            self._values["memory"] = memory
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation
        if name is not None:
            self._values["name"] = name
        if resource_requirement is not None:
            self._values["resource_requirement"] = resource_requirement

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#command PipesPipe#command}.'''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#cpu PipesPipe#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment"]]]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment PipesPipe#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment"]]], result)

    @builtins.property
    def environment_file(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile"]]]:
        '''environment_file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#environment_file PipesPipe#environment_file}
        '''
        result = self._values.get("environment_file")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile"]]], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory PipesPipe#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#memory_reservation PipesPipe#memory_reservation}.'''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_requirement(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]]:
        '''resource_requirement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resource_requirement PipesPipe#resource_requirement}
        '''
        result = self._values.get("resource_requirement")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e11339c9ebb9d9d701f298a78df71f002a77760383c979bae4d84f2d5324421)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed979cf96c3bfcd95c753355d18482d36d25a467dc9a8cb9bc692994e4726290)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__316290cd049434e322c6bcff5cd017d9c8ba122a72295a8b34f95df8b9ba8850)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092e30cc25adc326d2342a9fe6c6dac1b574b4b4c81a31dcf2609596de85d492)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e5f75110cda085aec0aa203995a3beb989fc96318dd81b73e76591a0a590dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51cb6ae8e6e38a7ac674eae4131eaba1de1cc0018ca545b44c348c132e3c90d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21b4815e674078e612970a8ae015b2dded9ad6ab1d2da9b35c4bdab6793e293d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe4cefee693036e6191bccbacf666ebe2e0c8b37a2b06eafa23ba0dc65cf031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff1fd60dc084d38a6de334b66f1e04ab25daabf978c1b5036bac33f765a98972)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bbdef1bb0ec5e676367fd908b7ce64bec8c8a2b7402c6b7af48290a7b2bb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f74c89fd2a446a2fb183156807bca337972163ef2eb753378fb81deb11c014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e93de00cb3691eade49bcc8180303d7c40a26ad24564337872ffce513952de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efa5f28cac097e47c529fb1caca63fc2380f072b5461c3e647c020de2438b397)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bb88bc1d09c7ca891905e516a6fadfbab20a1dd9e68dcf43313a0d0b18061a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d529ffbee974b56a4d7653f1065ee9bba376380863eaeb403e48af43d7c97296)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bedfcdbf51c1318b6050bb72791d3c10779716f7a9a8c55fec7ff2a6d53106a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__989b52e1b8282632dc3672d635ecdbd43e0538961cfedd52fd7490159a2aac24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641e85206b66ac878b8599bb39df80fa8dd47a283c7da31ea7539a02d464ec88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e4cef462bccbbc5438f19726735478fbba63a41ba4214eb873d9d51c5f78369)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ae0e727343cf92d0742c7b4d7c33ecdc76894693e94f924237667b10fafa9d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710e19bef2182fde54b49ec59994cefce0c1cf8f5c0e5fba0a94bf6b53f8d735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7501c8ef77976c08088df6640814d3f007864019ef0c046646be4212e8039faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__924bffa29d6c1733e18cabc1dd27fa8698586624488fe1493df887cd575921d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48730c31ef479295f61b36a22d1f5ab054cecb769c014796965cd3a745c6abb0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63457818fd425f60feb417e05e86860399093409b32c9a60ff0110ea8c622775)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d03aa6c8a47cf48c5f235ebf76e260077753917282a008de04d43c4a4b428fd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ac3d103e55ef194caf866e90326c73389049c7e32770e0a1a2efea4d7847108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4474e6580859da7ec499735671c64b7bddf9d000addc5b3bd6305614f89c250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94ebd5b9a6f92f64ad22b1331ecfbdf09be2b6cd10fe9c355fb5123177a0d214)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd9571ec234036e2c66bd99eaed10ad92400bfe4d0feaa2bcfb78b387859fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putEnvironmentFile")
    def put_environment_file(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2bad4338d2421e5f40b11b3268ea99f830ee98a93fb3870f4f7fed982d42f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironmentFile", [value]))

    @jsii.member(jsii_name="putResourceRequirement")
    def put_resource_requirement(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b520275110dd7d6d20006a3328689cc8da69ee8093098698dc266e1f365beac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceRequirement", [value]))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetEnvironmentFile")
    def reset_environment_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentFile", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemoryReservation")
    def reset_memory_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryReservation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetResourceRequirement")
    def reset_resource_requirement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceRequirement", []))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="environmentFile")
    def environment_file(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList, jsii.get(self, "environmentFile"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirement")
    def resource_requirement(
        self,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList":
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList", jsii.get(self, "resourceRequirement"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentFileInput")
    def environment_file_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]], jsii.get(self, "environmentFileInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryReservationInput")
    def memory_reservation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceRequirementInput")
    def resource_requirement_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement"]]], jsii.get(self, "resourceRequirementInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3318cec9fcf42220c30089b0bf2a2b80c056278a7a05ca6dea09380394f5cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ae0fa51648d8ad5fa4e9a7ef92f660c1376b850464db80e2ce1a60f8da69be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcdd44e84dcc5514405fc3793738937c8f7b6512ea73f15d548892e7d5672951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryReservation"))

    @memory_reservation.setter
    def memory_reservation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7bd407eef0bca3d1e5d057625760f9e2b3311a830f297de84f0a01836414e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryReservation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5201d46a04217f5ee7d1671d0526c1f015a565068b2adfe3077808411084c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63fee808bad3474a6f11848dc7e39aa6555342419573bc7a25264051d47ab2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52020c4ca61fd22e13be4b190ed1ab86027e57694ebf4f17fbcc044ca730d091)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad1b6d2dd6cd5151492bf6c15eedea7a4bd61783c2750f930a3d218082566796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff95afecf0d83ffb93880a280f4bc5170a3f42400b448a8ccd93e301d179493)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4a1de7d660e39ae08a14e0d35a062e0f9d894bb3d41e21334e38c6319323e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52089b9274a24e4ac85dc7281a3d6a76dd21a811daff6b55da6f5cac83e72586)
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
            type_hints = typing.get_type_hints(_typecheckingstub__488d793456d88d815f9cabad67d8538462661a18b58955d9ce7fc450908ff469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__464d1f5ba0697a32012f4efe3c452bb2cec70e065b82bdf604c7938d37635648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7935fe61822f652a191002cfac04a9f363adbe858cf6780e69cfbbf581e91f4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50e2f4d290b0b2708056afeed1eef5a04674bebc7262fe577229d66845be809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64029b7d3375b08d47809603e15d9002551764ce95fbe169c4a69ee87589cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed92d5ffeff16d3fd25d01b7048b0c53d4a0e83ff6648bc3675c9503f8c9da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage",
    jsii_struct_bases=[],
    name_mapping={"size_in_gib": "sizeInGib"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage:
    def __init__(self, *, size_in_gib: jsii.Number) -> None:
        '''
        :param size_in_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#size_in_gib PipesPipe#size_in_gib}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1451a0a3e348bfbc8455837077216987590f7c894c00b24c9981a9314db8f7a7)
            check_type(argname="argument size_in_gib", value=size_in_gib, expected_type=type_hints["size_in_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size_in_gib": size_in_gib,
        }

    @builtins.property
    def size_in_gib(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#size_in_gib PipesPipe#size_in_gib}.'''
        result = self._values.get("size_in_gib")
        assert result is not None, "Required property 'size_in_gib' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__210b6f679972ca5639b96c058cb5264e797a8f6e0941f8f02c6a671f5ad803d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sizeInGibInput")
    def size_in_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInGibInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInGib")
    def size_in_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInGib"))

    @size_in_gib.setter
    def size_in_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1cf44b680fe2b40dea76441acd672c06368fddcb7153304edec25eba482255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3e260e53ef2524d2700af3c0221e7709039f111b977c59675f35478cdfd2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride",
    jsii_struct_bases=[],
    name_mapping={"device_name": "deviceName", "device_type": "deviceType"},
)
class PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride:
    def __init__(
        self,
        *,
        device_name: typing.Optional[builtins.str] = None,
        device_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#device_name PipesPipe#device_name}.
        :param device_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#device_type PipesPipe#device_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1b951f7cfe94bdd2c12c74e8c1a2443d943a0efa8961590f5f73d4d8526617)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_name is not None:
            self._values["device_name"] = device_name
        if device_type is not None:
            self._values["device_type"] = device_type

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#device_name PipesPipe#device_name}.'''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#device_type PipesPipe#device_type}.'''
        result = self._values.get("device_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca538002bd97059b0551ac9da1ba8f05971a2e80084c22bae2572f15e73c1076)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596482a493e53fde35a567d4193d499ef9680bd8fff9bd2d585796a1a1f5d0b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edfd6efc3e7772b0a9a45b7930dc909be4e9e8874cbb39917c410dc65e3103d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eaf67d69685a60f0d4923dc7234b489c2de7aed12d7f972c9d7349db5aa1b5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f86647879d8a0aee7e4fa83ddac96965cd50a4731f4d55e5360ad88b2f4b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af92027b38d82329f0b6dbf64aa17bc99b654b35476956d0fb4f0551f601d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__459db39d683185533033f0f7a4328f523f0b3342b312b02cfa82b2f61ba751bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetDeviceType")
    def reset_device_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceType", []))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeInput")
    def device_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fce9386d499310a04b8a28cb5501963783ca52b31bde2e3de24f28575e54be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceType")
    def device_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceType"))

    @device_type.setter
    def device_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6317a8864ed9cb40077ee9650bd1df3eac58260cb810f87f3207a3f7df37e9c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341fe47839b0b0a8e3ad7e01bea0c428c0c8659a99ae693a1dbb8884ec189098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38dba157fbe772c51664da115b10866e31e7d0d7fbc1644815ff5424468af2fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerOverride")
    def put_container_override(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5cbd1705cba4bf9d4622168394d2a6b89c0efa2becad616c238bca3b47b9e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainerOverride", [value]))

    @jsii.member(jsii_name="putEphemeralStorage")
    def put_ephemeral_storage(self, *, size_in_gib: jsii.Number) -> None:
        '''
        :param size_in_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#size_in_gib PipesPipe#size_in_gib}.
        '''
        value = PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage(
            size_in_gib=size_in_gib
        )

        return typing.cast(None, jsii.invoke(self, "putEphemeralStorage", [value]))

    @jsii.member(jsii_name="putInferenceAcceleratorOverride")
    def put_inference_accelerator_override(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f8f44a14897afc495e5dd6fbfea3ef301f16295993026b6feb08d07e23d215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInferenceAcceleratorOverride", [value]))

    @jsii.member(jsii_name="resetContainerOverride")
    def reset_container_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerOverride", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEphemeralStorage")
    def reset_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorage", []))

    @jsii.member(jsii_name="resetExecutionRoleArn")
    def reset_execution_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRoleArn", []))

    @jsii.member(jsii_name="resetInferenceAcceleratorOverride")
    def reset_inference_accelerator_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceAcceleratorOverride", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetTaskRoleArn")
    def reset_task_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="containerOverride")
    def container_override(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList, jsii.get(self, "containerOverride"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAcceleratorOverride")
    def inference_accelerator_override(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList, jsii.get(self, "inferenceAcceleratorOverride"))

    @builtins.property
    @jsii.member(jsii_name="containerOverrideInput")
    def container_override_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]], jsii.get(self, "containerOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageInput")
    def ephemeral_storage_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage], jsii.get(self, "ephemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAcceleratorOverrideInput")
    def inference_accelerator_override_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]], jsii.get(self, "inferenceAcceleratorOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="taskRoleArnInput")
    def task_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19856fdd98e4e9c92936ba83b8570cdc8b545d0eed9bf1e177e10558e8e4d148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4f295f2a6e8a411a291072ae1e577fea6fc6102304fb4927bd889b0e9054e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618d4bcec4542a876a20fa3d481682e8c055809764c4353c7b3abd57bd5279c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskRoleArn")
    def task_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskRoleArn"))

    @task_role_arn.setter
    def task_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9187d9cfb3bd0d39728f914cf419246f5da1394acf2b260a48afb54a6e0741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1a8e9e37f78629e6a1a1ce61a4ff6f082bc7cea4aec9e65e2f98f8555d426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementConstraint",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression", "type": "type"},
)
class PipesPipeTargetParametersEcsTaskParametersPlacementConstraint:
    def __init__(
        self,
        *,
        expression: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#expression PipesPipe#expression}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf32cdc55de9568f6b9330dd43091547f544c53e0f8e23e0c313398ba6bda66d)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expression is not None:
            self._values["expression"] = expression
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#expression PipesPipe#expression}.'''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersPlacementConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f45c8f3611d8975d2e60ff0cfd607f3b90233978b8b611b03113cbd6480299)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acb7a0a8cd439d4f77871de4cdeb44cb73ea4dd0ad71ace0737e6b4ea189acc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c9b9607f3011e21bc1a28ea969ba883d86bb3330a8a3383b283de726bb4418)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2de164b3cbe276117fdf1ccb9856c38c1698e4fa2f06537e07a1220dcc01e2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2106f95d8fa0510e3ab2dac336c18cdd217e9597b9a63fd5a601e5da8590164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c1e63b947595c0494ea8e53bdcf3170965f49b1672d37f5f3f935fcedf7369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8146c4bbe5e153ac43de733c9a4a24a39f111e0f9265f0d1ec4affe2afc4c690)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d5c85a8daf8e0bb97f98d05f254a9f1e55fbd67c3b88a52085f2b327df761e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776354ef60c1d9e08640786a983995d40e2394d933c48e457d681c76299a32d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9d41d72f861a2a1c710590523beefd354d7faf1713325d0684abb43ad00be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementStrategy",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "type": "type"},
)
class PipesPipeTargetParametersEcsTaskParametersPlacementStrategy:
    def __init__(
        self,
        *,
        field: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#field PipesPipe#field}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0601883476a6e0cca204abc0b3f7649e81fdf663fe68db9c4aaa5b3c15fcbb)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field is not None:
            self._values["field"] = field
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#field PipesPipe#field}.'''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#type PipesPipe#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEcsTaskParametersPlacementStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8dd2e0cd0dcf6760ff016bf89e621081d216f1e211507a0f15dc4f5fc0ad8f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdb65b854804c944901b7ead61f20e911bd7f43ef80a64a307030018579b222)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ef62ede77f328a2ed0fc82a5518f2a4863e8baea3141d68d5e23169a529627)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa5a02e1f0fac0b6b1d2fd216d4e98ed7f3104c4ca32957236557d7866502d89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef9cfafa9821ab846681c079ff86416d68bf72b0e55ec71d34ecacfa884b2eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a931502582a6e2bd16fc509c0a9a3dd250c2f5512ef97255f6642126087c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__367c6c75d2ccd0d5ed3ce97a667c893d45a8a378f2d602cf2a2d622423d84d38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ec23b3634a50f5b94c2df0262d3cdb0356f2ab5841d0dbc2e2732f67d78e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2356d5a9ffadf0d23004bbe84cca72f8a27695385f3f247cc8baf0c3872375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115ee7b18966cee00ac8971c63b667186d435dbe18c3295d136dbcff00a9bbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEventbridgeEventBusParameters",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "endpoint_id": "endpointId",
        "resources": "resources",
        "source": "source",
        "time": "time",
    },
)
class PipesPipeTargetParametersEventbridgeEventBusParameters:
    def __init__(
        self,
        *,
        detail_type: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#detail_type PipesPipe#detail_type}.
        :param endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#endpoint_id PipesPipe#endpoint_id}.
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resources PipesPipe#resources}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#time PipesPipe#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19ee0f621de4b5274ed809d22f8717d76980aac7a588ece138055ee41598bbf)
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if endpoint_id is not None:
            self._values["endpoint_id"] = endpoint_id
        if resources is not None:
            self._values["resources"] = resources
        if source is not None:
            self._values["source"] = source
        if time is not None:
            self._values["time"] = time

    @builtins.property
    def detail_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#detail_type PipesPipe#detail_type}.'''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#endpoint_id PipesPipe#endpoint_id}.'''
        result = self._values.get("endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resources PipesPipe#resources}.'''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source PipesPipe#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#time PipesPipe#time}.'''
        result = self._values.get("time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersEventbridgeEventBusParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5332d32c88b5b7b6f596b4c2135cefa9086b9f1fb0e09fb7a7ebf11b2cac1ebb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDetailType")
    def reset_detail_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetailType", []))

    @jsii.member(jsii_name="resetEndpointId")
    def reset_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointId", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetTime")
    def reset_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTime", []))

    @builtins.property
    @jsii.member(jsii_name="detailTypeInput")
    def detail_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detailTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointIdInput")
    def endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="detailType")
    def detail_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detailType"))

    @detail_type.setter
    def detail_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38cc172bb65b07ccabcf6d333aa21cc884f3c5812a95ae5bfb02a7c6b44fe61c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detailType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointId")
    def endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointId"))

    @endpoint_id.setter
    def endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209ca7dc391123a1f965075be6d5a22f8dfbe51e6975dec5733873f3f4a229ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10d2b0e7b0213c2148df8be016b0dffb7e78b1a400eb13754e1531ee686e7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c739edc82cbcc5aeebb50a4203427bacbb0304b847ef9edcd6f59b2846ec8a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1577c8468b726399cc45c5446897ca9797573ece821eac8d3c01f418bc0987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fce27582cddc5cde444b227c61511301561361fb2281d861479254271555e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersHttpParameters",
    jsii_struct_bases=[],
    name_mapping={
        "header_parameters": "headerParameters",
        "path_parameter_values": "pathParameterValues",
        "query_string_parameters": "queryStringParameters",
    },
)
class PipesPipeTargetParametersHttpParameters:
    def __init__(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f9878fe9ee0d9c1d5a39108407db0e877d3b6014a04f708b86b5e360f478f5)
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.'''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.'''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.'''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersHttpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersHttpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersHttpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f84f1fd449a15bc7a14708fd9f8d169a785841b21cec8e1303d739077d13a57e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeaderParameters")
    def reset_header_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderParameters", []))

    @jsii.member(jsii_name="resetPathParameterValues")
    def reset_path_parameter_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathParameterValues", []))

    @jsii.member(jsii_name="resetQueryStringParameters")
    def reset_query_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="headerParametersInput")
    def header_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathParameterValuesInput")
    def path_parameter_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathParameterValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringParametersInput")
    def query_string_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryStringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="headerParameters")
    def header_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headerParameters"))

    @header_parameters.setter
    def header_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10abf67d8d240ea003b5756370919a0debd00e1e546aee6f475f397ad9145b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathParameterValues")
    def path_parameter_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pathParameterValues"))

    @path_parameter_values.setter
    def path_parameter_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c7ab4992b77ed02519ce6e1126478ee8551c1228d11745b78c13c630a5bbc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathParameterValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringParameters")
    def query_string_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "queryStringParameters"))

    @query_string_parameters.setter
    def query_string_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a86949a523748d52538f454c1b24ec9bff587018cf458e40d28a3c43b10af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersHttpParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersHttpParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fce1a56d42aa730a9b5ca31b6335d9bbf898c86aa5f8166e186557c8fe5dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersKinesisStreamParameters",
    jsii_struct_bases=[],
    name_mapping={"partition_key": "partitionKey"},
)
class PipesPipeTargetParametersKinesisStreamParameters:
    def __init__(self, *, partition_key: builtins.str) -> None:
        '''
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#partition_key PipesPipe#partition_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581965ae4e458c91acd2cce33d22228fda2dad758ce3a1f1d742ed8aa30c02d1)
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#partition_key PipesPipe#partition_key}.'''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersKinesisStreamParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersKinesisStreamParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersKinesisStreamParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__524c61c935dfb74f707aa9873021d53610024c332b1856c45e978b4212aecba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKey"))

    @partition_key.setter
    def partition_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9407b18c00d3f6d232fc45a37ade63859df5aaa37852ccdadbc2a61ac20532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersKinesisStreamParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersKinesisStreamParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c3df58d13896c5fb2fab34a332ebdea50ee4cae9bf88645a44ec8f9b8b26d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersLambdaFunctionParameters",
    jsii_struct_bases=[],
    name_mapping={"invocation_type": "invocationType"},
)
class PipesPipeTargetParametersLambdaFunctionParameters:
    def __init__(self, *, invocation_type: builtins.str) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e58163a3f1168cf4d81ebafd1e025a1247b1938d2b6de1f074c18ad7f1860c6)
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "invocation_type": invocation_type,
        }

    @builtins.property
    def invocation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.'''
        result = self._values.get("invocation_type")
        assert result is not None, "Required property 'invocation_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersLambdaFunctionParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersLambdaFunctionParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersLambdaFunctionParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__150fb01c8703b3ecdbafb6653678e986a6dccaaddd4054971682dd9de1783bcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="invocationTypeInput")
    def invocation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationType")
    def invocation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationType"))

    @invocation_type.setter
    def invocation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156b01c53f2c741dca797b10307b1f8868408d92f21d2f6bff40c00ede9daeed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257e65100f69a98ac6d0ba6f874b98ae994bf26b61ff770d58fdc9cd88bae0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc0fdb117ace85b72d4d89a5502553223ae391a4d6335b421266000ba20e17e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBatchJobParameters")
    def put_batch_job_parameters(
        self,
        *,
        job_definition: builtins.str,
        job_name: builtins.str,
        array_properties: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersArrayProperties, typing.Dict[builtins.str, typing.Any]]] = None,
        container_overrides: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
        depends_on: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry_strategy: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersRetryStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_definition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_definition PipesPipe#job_definition}.
        :param job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#job_name PipesPipe#job_name}.
        :param array_properties: array_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#array_properties PipesPipe#array_properties}
        :param container_overrides: container_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#container_overrides PipesPipe#container_overrides}
        :param depends_on: depends_on block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#depends_on PipesPipe#depends_on}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#parameters PipesPipe#parameters}.
        :param retry_strategy: retry_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#retry_strategy PipesPipe#retry_strategy}
        '''
        value = PipesPipeTargetParametersBatchJobParameters(
            job_definition=job_definition,
            job_name=job_name,
            array_properties=array_properties,
            container_overrides=container_overrides,
            depends_on=depends_on,
            parameters=parameters,
            retry_strategy=retry_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putBatchJobParameters", [value]))

    @jsii.member(jsii_name="putCloudwatchLogsParameters")
    def put_cloudwatch_logs_parameters(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#log_stream_name PipesPipe#log_stream_name}.
        :param timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#timestamp PipesPipe#timestamp}.
        '''
        value = PipesPipeTargetParametersCloudwatchLogsParameters(
            log_stream_name=log_stream_name, timestamp=timestamp
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogsParameters", [value]))

    @jsii.member(jsii_name="putEcsTaskParameters")
    def put_ecs_task_parameters(
        self,
        *,
        task_definition_arn: builtins.str,
        capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_execute_command: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group: typing.Optional[builtins.str] = None,
        launch_type: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
        placement_constraint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint, typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
        platform_version: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.str] = None,
        reference_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param task_definition_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_definition_arn PipesPipe#task_definition_arn}.
        :param capacity_provider_strategy: capacity_provider_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#capacity_provider_strategy PipesPipe#capacity_provider_strategy}
        :param enable_ecs_managed_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enable_ecs_managed_tags PipesPipe#enable_ecs_managed_tags}.
        :param enable_execute_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#enable_execute_command PipesPipe#enable_execute_command}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#group PipesPipe#group}.
        :param launch_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#launch_type PipesPipe#launch_type}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#network_configuration PipesPipe#network_configuration}
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#overrides PipesPipe#overrides}
        :param placement_constraint: placement_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#placement_constraint PipesPipe#placement_constraint}
        :param placement_strategy: placement_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#placement_strategy PipesPipe#placement_strategy}
        :param platform_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#platform_version PipesPipe#platform_version}.
        :param propagate_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#propagate_tags PipesPipe#propagate_tags}.
        :param reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#reference_id PipesPipe#reference_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#tags PipesPipe#tags}.
        :param task_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#task_count PipesPipe#task_count}.
        '''
        value = PipesPipeTargetParametersEcsTaskParameters(
            task_definition_arn=task_definition_arn,
            capacity_provider_strategy=capacity_provider_strategy,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_execute_command=enable_execute_command,
            group=group,
            launch_type=launch_type,
            network_configuration=network_configuration,
            overrides=overrides,
            placement_constraint=placement_constraint,
            placement_strategy=placement_strategy,
            platform_version=platform_version,
            propagate_tags=propagate_tags,
            reference_id=reference_id,
            tags=tags,
            task_count=task_count,
        )

        return typing.cast(None, jsii.invoke(self, "putEcsTaskParameters", [value]))

    @jsii.member(jsii_name="putEventbridgeEventBusParameters")
    def put_eventbridge_event_bus_parameters(
        self,
        *,
        detail_type: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#detail_type PipesPipe#detail_type}.
        :param endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#endpoint_id PipesPipe#endpoint_id}.
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#resources PipesPipe#resources}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#source PipesPipe#source}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#time PipesPipe#time}.
        '''
        value = PipesPipeTargetParametersEventbridgeEventBusParameters(
            detail_type=detail_type,
            endpoint_id=endpoint_id,
            resources=resources,
            source=source,
            time=time,
        )

        return typing.cast(None, jsii.invoke(self, "putEventbridgeEventBusParameters", [value]))

    @jsii.member(jsii_name="putHttpParameters")
    def put_http_parameters(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param header_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#header_parameters PipesPipe#header_parameters}.
        :param path_parameter_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#path_parameter_values PipesPipe#path_parameter_values}.
        :param query_string_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#query_string_parameters PipesPipe#query_string_parameters}.
        '''
        value = PipesPipeTargetParametersHttpParameters(
            header_parameters=header_parameters,
            path_parameter_values=path_parameter_values,
            query_string_parameters=query_string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpParameters", [value]))

    @jsii.member(jsii_name="putKinesisStreamParameters")
    def put_kinesis_stream_parameters(self, *, partition_key: builtins.str) -> None:
        '''
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#partition_key PipesPipe#partition_key}.
        '''
        value = PipesPipeTargetParametersKinesisStreamParameters(
            partition_key=partition_key
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStreamParameters", [value]))

    @jsii.member(jsii_name="putLambdaFunctionParameters")
    def put_lambda_function_parameters(self, *, invocation_type: builtins.str) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        value = PipesPipeTargetParametersLambdaFunctionParameters(
            invocation_type=invocation_type
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionParameters", [value]))

    @jsii.member(jsii_name="putRedshiftDataParameters")
    def put_redshift_data_parameters(
        self,
        *,
        database: builtins.str,
        sqls: typing.Sequence[builtins.str],
        db_user: typing.Optional[builtins.str] = None,
        secret_manager_arn: typing.Optional[builtins.str] = None,
        statement_name: typing.Optional[builtins.str] = None,
        with_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#database PipesPipe#database}.
        :param sqls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqls PipesPipe#sqls}.
        :param db_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#db_user PipesPipe#db_user}.
        :param secret_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#secret_manager_arn PipesPipe#secret_manager_arn}.
        :param statement_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#statement_name PipesPipe#statement_name}.
        :param with_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#with_event PipesPipe#with_event}.
        '''
        value = PipesPipeTargetParametersRedshiftDataParameters(
            database=database,
            sqls=sqls,
            db_user=db_user,
            secret_manager_arn=secret_manager_arn,
            statement_name=statement_name,
            with_event=with_event,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshiftDataParameters", [value]))

    @jsii.member(jsii_name="putSagemakerPipelineParameters")
    def put_sagemaker_pipeline_parameters(
        self,
        *,
        pipeline_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param pipeline_parameter: pipeline_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#pipeline_parameter PipesPipe#pipeline_parameter}
        '''
        value = PipesPipeTargetParametersSagemakerPipelineParameters(
            pipeline_parameter=pipeline_parameter
        )

        return typing.cast(None, jsii.invoke(self, "putSagemakerPipelineParameters", [value]))

    @jsii.member(jsii_name="putSqsQueueParameters")
    def put_sqs_queue_parameters(
        self,
        *,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_deduplication_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#message_deduplication_id PipesPipe#message_deduplication_id}.
        :param message_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#message_group_id PipesPipe#message_group_id}.
        '''
        value = PipesPipeTargetParametersSqsQueueParameters(
            message_deduplication_id=message_deduplication_id,
            message_group_id=message_group_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSqsQueueParameters", [value]))

    @jsii.member(jsii_name="putStepFunctionStateMachineParameters")
    def put_step_function_state_machine_parameters(
        self,
        *,
        invocation_type: builtins.str,
    ) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        value = PipesPipeTargetParametersStepFunctionStateMachineParameters(
            invocation_type=invocation_type
        )

        return typing.cast(None, jsii.invoke(self, "putStepFunctionStateMachineParameters", [value]))

    @jsii.member(jsii_name="resetBatchJobParameters")
    def reset_batch_job_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchJobParameters", []))

    @jsii.member(jsii_name="resetCloudwatchLogsParameters")
    def reset_cloudwatch_logs_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogsParameters", []))

    @jsii.member(jsii_name="resetEcsTaskParameters")
    def reset_ecs_task_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsTaskParameters", []))

    @jsii.member(jsii_name="resetEventbridgeEventBusParameters")
    def reset_eventbridge_event_bus_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventbridgeEventBusParameters", []))

    @jsii.member(jsii_name="resetHttpParameters")
    def reset_http_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpParameters", []))

    @jsii.member(jsii_name="resetInputTemplate")
    def reset_input_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputTemplate", []))

    @jsii.member(jsii_name="resetKinesisStreamParameters")
    def reset_kinesis_stream_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStreamParameters", []))

    @jsii.member(jsii_name="resetLambdaFunctionParameters")
    def reset_lambda_function_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionParameters", []))

    @jsii.member(jsii_name="resetRedshiftDataParameters")
    def reset_redshift_data_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshiftDataParameters", []))

    @jsii.member(jsii_name="resetSagemakerPipelineParameters")
    def reset_sagemaker_pipeline_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerPipelineParameters", []))

    @jsii.member(jsii_name="resetSqsQueueParameters")
    def reset_sqs_queue_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsQueueParameters", []))

    @jsii.member(jsii_name="resetStepFunctionStateMachineParameters")
    def reset_step_function_state_machine_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctionStateMachineParameters", []))

    @builtins.property
    @jsii.member(jsii_name="batchJobParameters")
    def batch_job_parameters(
        self,
    ) -> PipesPipeTargetParametersBatchJobParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersBatchJobParametersOutputReference, jsii.get(self, "batchJobParameters"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsParameters")
    def cloudwatch_logs_parameters(
        self,
    ) -> PipesPipeTargetParametersCloudwatchLogsParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersCloudwatchLogsParametersOutputReference, jsii.get(self, "cloudwatchLogsParameters"))

    @builtins.property
    @jsii.member(jsii_name="ecsTaskParameters")
    def ecs_task_parameters(
        self,
    ) -> PipesPipeTargetParametersEcsTaskParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersEcsTaskParametersOutputReference, jsii.get(self, "ecsTaskParameters"))

    @builtins.property
    @jsii.member(jsii_name="eventbridgeEventBusParameters")
    def eventbridge_event_bus_parameters(
        self,
    ) -> PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference, jsii.get(self, "eventbridgeEventBusParameters"))

    @builtins.property
    @jsii.member(jsii_name="httpParameters")
    def http_parameters(self) -> PipesPipeTargetParametersHttpParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersHttpParametersOutputReference, jsii.get(self, "httpParameters"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParameters")
    def kinesis_stream_parameters(
        self,
    ) -> PipesPipeTargetParametersKinesisStreamParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersKinesisStreamParametersOutputReference, jsii.get(self, "kinesisStreamParameters"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionParameters")
    def lambda_function_parameters(
        self,
    ) -> PipesPipeTargetParametersLambdaFunctionParametersOutputReference:
        return typing.cast(PipesPipeTargetParametersLambdaFunctionParametersOutputReference, jsii.get(self, "lambdaFunctionParameters"))

    @builtins.property
    @jsii.member(jsii_name="redshiftDataParameters")
    def redshift_data_parameters(
        self,
    ) -> "PipesPipeTargetParametersRedshiftDataParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersRedshiftDataParametersOutputReference", jsii.get(self, "redshiftDataParameters"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerPipelineParameters")
    def sagemaker_pipeline_parameters(
        self,
    ) -> "PipesPipeTargetParametersSagemakerPipelineParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersSagemakerPipelineParametersOutputReference", jsii.get(self, "sagemakerPipelineParameters"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParameters")
    def sqs_queue_parameters(
        self,
    ) -> "PipesPipeTargetParametersSqsQueueParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersSqsQueueParametersOutputReference", jsii.get(self, "sqsQueueParameters"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionStateMachineParameters")
    def step_function_state_machine_parameters(
        self,
    ) -> "PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference":
        return typing.cast("PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference", jsii.get(self, "stepFunctionStateMachineParameters"))

    @builtins.property
    @jsii.member(jsii_name="batchJobParametersInput")
    def batch_job_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersBatchJobParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersBatchJobParameters], jsii.get(self, "batchJobParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsParametersInput")
    def cloudwatch_logs_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters], jsii.get(self, "cloudwatchLogsParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsTaskParametersInput")
    def ecs_task_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEcsTaskParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEcsTaskParameters], jsii.get(self, "ecsTaskParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="eventbridgeEventBusParametersInput")
    def eventbridge_event_bus_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters], jsii.get(self, "eventbridgeEventBusParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpParametersInput")
    def http_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersHttpParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersHttpParameters], jsii.get(self, "httpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplateInput")
    def input_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamParametersInput")
    def kinesis_stream_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersKinesisStreamParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersKinesisStreamParameters], jsii.get(self, "kinesisStreamParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionParametersInput")
    def lambda_function_parameters_input(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters], jsii.get(self, "lambdaFunctionParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftDataParametersInput")
    def redshift_data_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersRedshiftDataParameters"], jsii.get(self, "redshiftDataParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerPipelineParametersInput")
    def sagemaker_pipeline_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersSagemakerPipelineParameters"], jsii.get(self, "sagemakerPipelineParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueParametersInput")
    def sqs_queue_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersSqsQueueParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersSqsQueueParameters"], jsii.get(self, "sqsQueueParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionStateMachineParametersInput")
    def step_function_state_machine_parameters_input(
        self,
    ) -> typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"]:
        return typing.cast(typing.Optional["PipesPipeTargetParametersStepFunctionStateMachineParameters"], jsii.get(self, "stepFunctionStateMachineParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="inputTemplate")
    def input_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputTemplate"))

    @input_template.setter
    def input_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1203e54f309e6121db523ed6e5ab029cfc6c0dd82080ed46a83bb123627f0e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipesPipeTargetParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipesPipeTargetParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8afdd6f4d46d0a354a392b920e80aa5a2d596f31bbed3bf4c747fda0370013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersRedshiftDataParameters",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "sqls": "sqls",
        "db_user": "dbUser",
        "secret_manager_arn": "secretManagerArn",
        "statement_name": "statementName",
        "with_event": "withEvent",
    },
)
class PipesPipeTargetParametersRedshiftDataParameters:
    def __init__(
        self,
        *,
        database: builtins.str,
        sqls: typing.Sequence[builtins.str],
        db_user: typing.Optional[builtins.str] = None,
        secret_manager_arn: typing.Optional[builtins.str] = None,
        statement_name: typing.Optional[builtins.str] = None,
        with_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#database PipesPipe#database}.
        :param sqls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqls PipesPipe#sqls}.
        :param db_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#db_user PipesPipe#db_user}.
        :param secret_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#secret_manager_arn PipesPipe#secret_manager_arn}.
        :param statement_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#statement_name PipesPipe#statement_name}.
        :param with_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#with_event PipesPipe#with_event}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d80323ed7f563790e811a29145124d8c9abbf2158bac63aefa25a4678e0c58)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument sqls", value=sqls, expected_type=type_hints["sqls"])
            check_type(argname="argument db_user", value=db_user, expected_type=type_hints["db_user"])
            check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
            check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
            check_type(argname="argument with_event", value=with_event, expected_type=type_hints["with_event"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "sqls": sqls,
        }
        if db_user is not None:
            self._values["db_user"] = db_user
        if secret_manager_arn is not None:
            self._values["secret_manager_arn"] = secret_manager_arn
        if statement_name is not None:
            self._values["statement_name"] = statement_name
        if with_event is not None:
            self._values["with_event"] = with_event

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#database PipesPipe#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sqls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#sqls PipesPipe#sqls}.'''
        result = self._values.get("sqls")
        assert result is not None, "Required property 'sqls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#db_user PipesPipe#db_user}.'''
        result = self._values.get("db_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_manager_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#secret_manager_arn PipesPipe#secret_manager_arn}.'''
        result = self._values.get("secret_manager_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#statement_name PipesPipe#statement_name}.'''
        result = self._values.get("statement_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_event(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#with_event PipesPipe#with_event}.'''
        result = self._values.get("with_event")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersRedshiftDataParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersRedshiftDataParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersRedshiftDataParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__014ba15f1bc4b7a041a96da6d781dca341c495daed608b16ecf380aaa3d874d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDbUser")
    def reset_db_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbUser", []))

    @jsii.member(jsii_name="resetSecretManagerArn")
    def reset_secret_manager_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerArn", []))

    @jsii.member(jsii_name="resetStatementName")
    def reset_statement_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementName", []))

    @jsii.member(jsii_name="resetWithEvent")
    def reset_with_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithEvent", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="dbUserInput")
    def db_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbUserInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerArnInput")
    def secret_manager_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretManagerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlsInput")
    def sqls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sqlsInput"))

    @builtins.property
    @jsii.member(jsii_name="statementNameInput")
    def statement_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementNameInput"))

    @builtins.property
    @jsii.member(jsii_name="withEventInput")
    def with_event_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withEventInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a442621d69a6b44b61ad9fda165b1e11144d017e575301dd5ae8b62c1f30a573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbUser")
    def db_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbUser"))

    @db_user.setter
    def db_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e940192c68bc7713d1491bf3d48e89df4c8c0037c7d4ce3b2f735a22e0bd07d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretManagerArn")
    def secret_manager_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretManagerArn"))

    @secret_manager_arn.setter
    def secret_manager_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a6cb1165ed73b399d7483186ac75307df0bb1ca8abdd07041c76b1f70ae057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretManagerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqls")
    def sqls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sqls"))

    @sqls.setter
    def sqls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326e46496522cf3a50c67857583d97264568701c1ed73fdc9eb0cefa03d3ef0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementName")
    def statement_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statementName"))

    @statement_name.setter
    def statement_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacd29afb98c4f86275cba7d801597918cb028f81b13f21250cf8fba574ce301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withEvent")
    def with_event(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withEvent"))

    @with_event.setter
    def with_event(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfd1fd07ef6083fa1366ac1be10e9a9202b8198e24c487e98a4594699c91621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withEvent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersRedshiftDataParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersRedshiftDataParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersRedshiftDataParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac02df3156db76f1922f3328dac77785b0cfb27879ebf606f824e1879b11ebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParameters",
    jsii_struct_bases=[],
    name_mapping={"pipeline_parameter": "pipelineParameter"},
)
class PipesPipeTargetParametersSagemakerPipelineParameters:
    def __init__(
        self,
        *,
        pipeline_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param pipeline_parameter: pipeline_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#pipeline_parameter PipesPipe#pipeline_parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f6502eec0df20235ee40b2ecb726566ee7e974ee56dd542f2a53070968e2c4)
            check_type(argname="argument pipeline_parameter", value=pipeline_parameter, expected_type=type_hints["pipeline_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pipeline_parameter is not None:
            self._values["pipeline_parameter"] = pipeline_parameter

    @builtins.property
    def pipeline_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]]:
        '''pipeline_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#pipeline_parameter PipesPipe#pipeline_parameter}
        '''
        result = self._values.get("pipeline_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersSagemakerPipelineParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersSagemakerPipelineParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c7ab10ee3347003d95f5167ab84eb1b7a9807841ac924f2652774a6f18818d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPipelineParameter")
    def put_pipeline_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f9d6d47014fea5b8db7712ba3014928012c231114442ebdc438515bc87eae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPipelineParameter", [value]))

    @jsii.member(jsii_name="resetPipelineParameter")
    def reset_pipeline_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineParameter", []))

    @builtins.property
    @jsii.member(jsii_name="pipelineParameter")
    def pipeline_parameter(
        self,
    ) -> "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList":
        return typing.cast("PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList", jsii.get(self, "pipelineParameter"))

    @builtins.property
    @jsii.member(jsii_name="pipelineParameterInput")
    def pipeline_parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter"]]], jsii.get(self, "pipelineParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c70812f0ee26da962d5caf5a3c33f1bc5cf19c0da8d526609fd79d871e7e1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75feb0c748cf597b2fdf85d9157c7361a1bb685209d68a6df386b25e9c8915bb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#name PipesPipe#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#value PipesPipe#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090f7b561b8747f46d322e8616423e6a39564cb8e8ca046c9861326cd8402dcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec78f858dea484c62da11cd01a0a3067e8a1b651f7c372f47807d188720698c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e67dde4fab21f3603c33ba212028dac34eb585b856431d5abce2387aedb903)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc89aa7650ff59b42fc07b8e61095061f6cf21aa0a60ab1217934a9149010bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac9b8a5122cd4541e16a4b83ec997aa8aa31a867dede71d8066ace7272d756d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5b62dd26bcf48c1fb0f0dae2dafbd95e6036635fb1ee9aeff15f54eabce578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a73d590291fd8af6ac99fac3424c7b7cbe6ced87e92ff211fadc28f5331f444)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3f783e108d09212aa851bb537c9b10a2e29994e03fe6826aa6a424c95a1a00f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7e7bada7b3c954dfbcd88d7ef2f7f03e690cc4fd4590aa039bbf22d6462162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3c01f9a1c1d24ff58a3df58e6e17fa30ca933c778a8e53ce518be2e37e0723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSqsQueueParameters",
    jsii_struct_bases=[],
    name_mapping={
        "message_deduplication_id": "messageDeduplicationId",
        "message_group_id": "messageGroupId",
    },
)
class PipesPipeTargetParametersSqsQueueParameters:
    def __init__(
        self,
        *,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message_deduplication_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#message_deduplication_id PipesPipe#message_deduplication_id}.
        :param message_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#message_group_id PipesPipe#message_group_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba0676b888273124f513b071b348120152f6c9401ed618b7fcfeb158426e11f)
            check_type(argname="argument message_deduplication_id", value=message_deduplication_id, expected_type=type_hints["message_deduplication_id"])
            check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_deduplication_id is not None:
            self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#message_deduplication_id PipesPipe#message_deduplication_id}.'''
        result = self._values.get("message_deduplication_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#message_group_id PipesPipe#message_group_id}.'''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersSqsQueueParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersSqsQueueParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersSqsQueueParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__342c0b768ceb70b342701252f7f88e71fec277704c18d6f1ce6aa8abf95cc1fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageDeduplicationId")
    def reset_message_deduplication_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageDeduplicationId", []))

    @jsii.member(jsii_name="resetMessageGroupId")
    def reset_message_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="messageDeduplicationIdInput")
    def message_deduplication_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageDeduplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="messageGroupIdInput")
    def message_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="messageDeduplicationId")
    def message_deduplication_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageDeduplicationId"))

    @message_deduplication_id.setter
    def message_deduplication_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8a11d251672aecc6fed208cd5abde327fe29c21bc38ee0af8a79f98d118aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageDeduplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageGroupId")
    def message_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageGroupId"))

    @message_group_id.setter
    def message_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279a1b919b0717dd6058082b06ff1585c39657b6b07c78a5e8e02c19b4c3ebcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersSqsQueueParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersSqsQueueParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersSqsQueueParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96140183c3ef9ac4c55044029101756cbd1dfe6c0035754216c7f65ebbffc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersStepFunctionStateMachineParameters",
    jsii_struct_bases=[],
    name_mapping={"invocation_type": "invocationType"},
)
class PipesPipeTargetParametersStepFunctionStateMachineParameters:
    def __init__(self, *, invocation_type: builtins.str) -> None:
        '''
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b75f3a843bbcc2c553941495b4b1ae639417a8b46ced4f6fa7e1bfee5f4f88)
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "invocation_type": invocation_type,
        }

    @builtins.property
    def invocation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#invocation_type PipesPipe#invocation_type}.'''
        result = self._values.get("invocation_type")
        assert result is not None, "Required property 'invocation_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTargetParametersStepFunctionStateMachineParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79a817ee3e7a129c32ccc87dc80ef1f7d2734a741a4f901425fea6f5c024638e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="invocationTypeInput")
    def invocation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationType")
    def invocation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationType"))

    @invocation_type.setter
    def invocation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80545ffb2d8f694623d79d093f85c599eb674f1f8239d5cadd02c2c6687b3596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters]:
        return typing.cast(typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c566f404ce6e2e6ba65c3b8ca18162377a77907aec9be4feeaff96e6cf94c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PipesPipeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#create PipesPipe#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#delete PipesPipe#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#update PipesPipe#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b44988988af52f926f544fc50bbaf6394e5a935b60c1f7084b281351552867)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#create PipesPipe#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#delete PipesPipe#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/pipes_pipe#update PipesPipe#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipesPipeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipesPipeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.pipesPipe.PipesPipeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28eb8dcad5cd1826d98830e5e248115b80b299d7e5400e7601502ead7f05c7a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7c57f002969ff0cbaeec168425fb5066661ab4b6599ccfd950cfae2e54ee25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8182b65a929d3acbebf7b7ce7024843904591b653769f02ae1df7295f3b76a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed18888729f2685d425182925d2cde8a265a5130908c006a72f47516ab54ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d9ed8af9adfb8348cc79347245303cbc168b33a9d524b7b72b2ce99aab8e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PipesPipe",
    "PipesPipeConfig",
    "PipesPipeEnrichmentParameters",
    "PipesPipeEnrichmentParametersHttpParameters",
    "PipesPipeEnrichmentParametersHttpParametersOutputReference",
    "PipesPipeEnrichmentParametersOutputReference",
    "PipesPipeLogConfiguration",
    "PipesPipeLogConfigurationCloudwatchLogsLogDestination",
    "PipesPipeLogConfigurationCloudwatchLogsLogDestinationOutputReference",
    "PipesPipeLogConfigurationFirehoseLogDestination",
    "PipesPipeLogConfigurationFirehoseLogDestinationOutputReference",
    "PipesPipeLogConfigurationOutputReference",
    "PipesPipeLogConfigurationS3LogDestination",
    "PipesPipeLogConfigurationS3LogDestinationOutputReference",
    "PipesPipeSourceParameters",
    "PipesPipeSourceParametersActivemqBrokerParameters",
    "PipesPipeSourceParametersActivemqBrokerParametersCredentials",
    "PipesPipeSourceParametersActivemqBrokerParametersCredentialsOutputReference",
    "PipesPipeSourceParametersActivemqBrokerParametersOutputReference",
    "PipesPipeSourceParametersDynamodbStreamParameters",
    "PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig",
    "PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfigOutputReference",
    "PipesPipeSourceParametersDynamodbStreamParametersOutputReference",
    "PipesPipeSourceParametersFilterCriteria",
    "PipesPipeSourceParametersFilterCriteriaFilter",
    "PipesPipeSourceParametersFilterCriteriaFilterList",
    "PipesPipeSourceParametersFilterCriteriaFilterOutputReference",
    "PipesPipeSourceParametersFilterCriteriaOutputReference",
    "PipesPipeSourceParametersKinesisStreamParameters",
    "PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig",
    "PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfigOutputReference",
    "PipesPipeSourceParametersKinesisStreamParametersOutputReference",
    "PipesPipeSourceParametersManagedStreamingKafkaParameters",
    "PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials",
    "PipesPipeSourceParametersManagedStreamingKafkaParametersCredentialsOutputReference",
    "PipesPipeSourceParametersManagedStreamingKafkaParametersOutputReference",
    "PipesPipeSourceParametersOutputReference",
    "PipesPipeSourceParametersRabbitmqBrokerParameters",
    "PipesPipeSourceParametersRabbitmqBrokerParametersCredentials",
    "PipesPipeSourceParametersRabbitmqBrokerParametersCredentialsOutputReference",
    "PipesPipeSourceParametersRabbitmqBrokerParametersOutputReference",
    "PipesPipeSourceParametersSelfManagedKafkaParameters",
    "PipesPipeSourceParametersSelfManagedKafkaParametersCredentials",
    "PipesPipeSourceParametersSelfManagedKafkaParametersCredentialsOutputReference",
    "PipesPipeSourceParametersSelfManagedKafkaParametersOutputReference",
    "PipesPipeSourceParametersSelfManagedKafkaParametersVpc",
    "PipesPipeSourceParametersSelfManagedKafkaParametersVpcOutputReference",
    "PipesPipeSourceParametersSqsQueueParameters",
    "PipesPipeSourceParametersSqsQueueParametersOutputReference",
    "PipesPipeTargetParameters",
    "PipesPipeTargetParametersBatchJobParameters",
    "PipesPipeTargetParametersBatchJobParametersArrayProperties",
    "PipesPipeTargetParametersBatchJobParametersArrayPropertiesOutputReference",
    "PipesPipeTargetParametersBatchJobParametersContainerOverrides",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentList",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironmentOutputReference",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesOutputReference",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementList",
    "PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirementOutputReference",
    "PipesPipeTargetParametersBatchJobParametersDependsOn",
    "PipesPipeTargetParametersBatchJobParametersDependsOnList",
    "PipesPipeTargetParametersBatchJobParametersDependsOnOutputReference",
    "PipesPipeTargetParametersBatchJobParametersOutputReference",
    "PipesPipeTargetParametersBatchJobParametersRetryStrategy",
    "PipesPipeTargetParametersBatchJobParametersRetryStrategyOutputReference",
    "PipesPipeTargetParametersCloudwatchLogsParameters",
    "PipesPipeTargetParametersCloudwatchLogsParametersOutputReference",
    "PipesPipeTargetParametersEcsTaskParameters",
    "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy",
    "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyList",
    "PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategyOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfigurationOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverrides",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFileOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirementOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage",
    "PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorageOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride",
    "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideList",
    "PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverrideOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersOverridesOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersPlacementConstraint",
    "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintList",
    "PipesPipeTargetParametersEcsTaskParametersPlacementConstraintOutputReference",
    "PipesPipeTargetParametersEcsTaskParametersPlacementStrategy",
    "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyList",
    "PipesPipeTargetParametersEcsTaskParametersPlacementStrategyOutputReference",
    "PipesPipeTargetParametersEventbridgeEventBusParameters",
    "PipesPipeTargetParametersEventbridgeEventBusParametersOutputReference",
    "PipesPipeTargetParametersHttpParameters",
    "PipesPipeTargetParametersHttpParametersOutputReference",
    "PipesPipeTargetParametersKinesisStreamParameters",
    "PipesPipeTargetParametersKinesisStreamParametersOutputReference",
    "PipesPipeTargetParametersLambdaFunctionParameters",
    "PipesPipeTargetParametersLambdaFunctionParametersOutputReference",
    "PipesPipeTargetParametersOutputReference",
    "PipesPipeTargetParametersRedshiftDataParameters",
    "PipesPipeTargetParametersRedshiftDataParametersOutputReference",
    "PipesPipeTargetParametersSagemakerPipelineParameters",
    "PipesPipeTargetParametersSagemakerPipelineParametersOutputReference",
    "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter",
    "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterList",
    "PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameterOutputReference",
    "PipesPipeTargetParametersSqsQueueParameters",
    "PipesPipeTargetParametersSqsQueueParametersOutputReference",
    "PipesPipeTargetParametersStepFunctionStateMachineParameters",
    "PipesPipeTargetParametersStepFunctionStateMachineParametersOutputReference",
    "PipesPipeTimeouts",
    "PipesPipeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6355d49fe49afd5d2d9c79c978d6ef634e4f2baf18d67546ab6fc28ac6d8a275(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    role_arn: builtins.str,
    source: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    enrichment: typing.Optional[builtins.str] = None,
    enrichment_parameters: typing.Optional[typing.Union[PipesPipeEnrichmentParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[PipesPipeLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    source_parameters: typing.Optional[typing.Union[PipesPipeSourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_parameters: typing.Optional[typing.Union[PipesPipeTargetParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PipesPipeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dbfe5164c3245f70d9e7bff1fb839094d2729ca7f4b1835f81b44bf7c01f2c47(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5abc17f0c947c0c1dd31c40efae801ed267ed65ef8d7de8df39d27f1556d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89f3983147aeb9afc37bb27dddd1a83381a0b06fa046e83fec9cf04a13d13d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e235f9f15928d63b63dad908d7bffc73f4575298fece6e667bea86e807b56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d272eec7606e8bc2dd541d131ba3f3359b6abb17d1d3c424d19e6c09711395d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f67565b4a2ad5b9bfaa5910aacb1099bdb8d109aca715e5df3909bf32b8d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f0adf10e7c550983ff4e6cf10fe7755151e871e9f0222726e8bb2222925df8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ba4b3e2b3165ff82b888d3ac8c943ace08e686c207201ae2167d005f995e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d9193ec9c7ba5d86d7facd7078a14c02de1d3e2a0c52f9e375fe05e8b4735f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a2a635ee549e1d096a44f295648dd4782a35795c216f732e1a8759becdb6d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cb2323059ca30cfccdb4b45a6f3e06601a25e168a590b2189681f9db5d27c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d124e6e9221f87f97cf9e5d12ba36dbed4dd59f6af9fcd8957a7a904f0bd643(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8e3c1a542360cace6bbad49f57282a94a74dba081938b86efbfc7d41a43cd0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3158fac93bd17a371468521d95aecc4631f0f16f1492a9d70e5536a43cdd37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0a9d27d6e68bb60d7a5bd9b6db74d6ef2d2e232d50d6581e224f795649d430(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role_arn: builtins.str,
    source: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    enrichment: typing.Optional[builtins.str] = None,
    enrichment_parameters: typing.Optional[typing.Union[PipesPipeEnrichmentParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[PipesPipeLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    source_parameters: typing.Optional[typing.Union[PipesPipeSourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_parameters: typing.Optional[typing.Union[PipesPipeTargetParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PipesPipeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdb1da17624426207720f6ea7c1cf16f8dc11b8f3972e66368034d4282d2925(
    *,
    http_parameters: typing.Optional[typing.Union[PipesPipeEnrichmentParametersHttpParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    input_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59c695454453403dbf9a6b9ba0fdeeb3e6137f908a0828a45dcf52f8520741e(
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa16b8520b91887e5e82043d548d6832b811041db5dbafaf79b5f6181665666e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0130b4752d7c91788b7b037fad366ecb4074901ac97e01199153e3c105770e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79fe5ef30a398b19cfe3c7ac1802df61499ca4c5304abeb7ac5f69c5ef4dd7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40fbf2a6d76819068260e0f18aa660390113cac053de63b3e6b8daf4e4c81f9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2326e3b0e8bfa412dd931a4f1232776c3f37b41d0304dc3ebdd6eb992228993(
    value: typing.Optional[PipesPipeEnrichmentParametersHttpParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bbeb4209bc64f4a43288ffa392f489df259e5e407b256a21383d98da4b5abd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645fb00c1502565c6f5aa36d293190ee4a263a564dbca40ea49277b50ffceea1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68be0482b8db6e1abcc660f862ad236e3e1d42915c950689355a4948514e0f0(
    value: typing.Optional[PipesPipeEnrichmentParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34db1f49e7e9f208f45272f441c0fabce7321bd8b08d5547992584ad591d19ec(
    *,
    level: builtins.str,
    cloudwatch_logs_log_destination: typing.Optional[typing.Union[PipesPipeLogConfigurationCloudwatchLogsLogDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose_log_destination: typing.Optional[typing.Union[PipesPipeLogConfigurationFirehoseLogDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_log_destination: typing.Optional[typing.Union[PipesPipeLogConfigurationS3LogDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c624263540a00b7adfc955292a20ec5b0319a4e19f84ac9c1e709cafc66c71af(
    *,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a8ef3a3e15c05b1b081f3b125fe8aeded30c4aa47d8949ba24fda4ec25701f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42014cbdaeb5e7085b7435639ca708baebc436cb935f3ea59111baf3224e36e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd86f514c28abec7bdbc81f4cb79ef4b1be438745ab0fab1ba4da108024aa6e(
    value: typing.Optional[PipesPipeLogConfigurationCloudwatchLogsLogDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4825c8b456c2a85d6a4808b0618b3219781384617bed09c0b8608459fc3ac19b(
    *,
    delivery_stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf2c77ec83c44402bcbeb3a98efb8615396a02e60bcc7bc4e5dbfcf984e5440(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6baf7792bd2eb2d5f5882a04a4b82103ce5dc95b355bab90e3ca2138faffe9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9abb3b13299886c65a169beb19ddf9ae8a3390c9fdafdb8545f5dd8a3c4766e(
    value: typing.Optional[PipesPipeLogConfigurationFirehoseLogDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43bcc1d2a73cc0b47525ef616516e4cdb4a168ba03e18de084db26b58930c92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa2f4898ecfc4c7cb1a3f2a62a8f87cbe6ffbe9586ea6eacd7541ef04831f81(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a93f573c36dd24fdc509f6e65509ae22e35b256f54cc82e3c2b23ce9456f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62f6110cec504c8d9280e9facb982b20460662fd8ba73869a0b6e5538d9e87c(
    value: typing.Optional[PipesPipeLogConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76f24d1916295ca17f332f6c00fda815a1a5da58c05ff9808cc084eefe4b848(
    *,
    bucket_name: builtins.str,
    bucket_owner: builtins.str,
    output_format: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9ae59442c2a2dcf92ce53125b08cf11532095405a90b40254c21a57abd99a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f3a340078fc644e97bec4b62e5f7b7a16fcffecf79687f4fa36baf73fe0a51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690305a4cac686cc14cc2d639195062c38ec6c7a6b4fc2df63ed2e02e6a57d52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2d4e4d671c6e28552f25d13bd8a6ca2ee4b0c0f94d86d9b4e35be8a0fa1843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431f764e59368ef7a3c12326842dedb31b29416217dfdead9880dd88c99e48a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6223d0204b3529f79c9826c708fa8e0dc695b2ae90dcb50c91bc6fc92b39eae(
    value: typing.Optional[PipesPipeLogConfigurationS3LogDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabf03144eea28307ea992d6bb011346c21a9d0ed7a54ad642fd2838156a878a(
    *,
    activemq_broker_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersActivemqBrokerParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodb_stream_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersDynamodbStreamParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    filter_criteria: typing.Optional[typing.Union[PipesPipeSourceParametersFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersKinesisStreamParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_streaming_kafka_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersManagedStreamingKafkaParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    rabbitmq_broker_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersRabbitmqBrokerParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersSelfManagedKafkaParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[PipesPipeSourceParametersSqsQueueParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63838d22786a4e0ba2958744baa626247cd62f53e18890f240ec27a8071f7dd(
    *,
    credentials: typing.Union[PipesPipeSourceParametersActivemqBrokerParametersCredentials, typing.Dict[builtins.str, typing.Any]],
    queue_name: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cf9e26688431b73604c1574ff1d08243105c4478b08500a827b966a9f877d9(
    *,
    basic_auth: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0bd8bbcfa4f92a6c0385326e5432f0dcfa9ef29bcc49aea28a70f22d3de3c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacba6a06fcd2e87ce661ff4f6560749e2deffb392c1751ae083d078d3681e03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eec62922003cea75b5c814a59f1a55ac74fbbaf8cba34d13c58a7946c4fd47c(
    value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24109b15cb28552d5884ac40a09046be46f3e0ea53c85498fa44eccb94485b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6f3fa2022e82661a505a90c0c6456de2d7c1f3b7c1c8a3b6fb21a6a33ec2fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f1a6be62d5a0598bb13c8ba88b3ac5471e89ef46046724d9c5a05adc1ca41d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07ec5ac56240edc21b7c84b950600b78b07caec303abd88afed81e00bc96624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b9e1994d55f9da155b1b61080d5332c2d112d584bdb4176d3c79958a523960(
    value: typing.Optional[PipesPipeSourceParametersActivemqBrokerParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a830723cd60156ea10f8b3693f336e2a5553ffd779125a0a959dbfbf1a583071(
    *,
    starting_position: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12635a1d29760e16b54df06e0ce68d2fc84ab167c7172a8c2581e6f2fbca2a92(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6bacd3f83d9c68cfbab22289c36a9113678888af7fbdb235b39aa1d357a705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3044a03db42452eec73028f964ff2e02cceb06b921e7ae2707d25a1838d655c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9559ab12257bc586890f8533f03707c39d645445f8633ac617189c091c34d813(
    value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParametersDeadLetterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04c181fcfa64571e66dd4b15a25ba256f6eb771eb01fa3bca03cbb60180970f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7dfb92422dad773ceb170699edf7d69c486d609f24e39d669bfad68b30482e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d8aa14fb2c0b52565096ddabfd5c8c45193eb5a9219cad074a47fa760c9ba2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d389c8f08ebbaeb941cf3b553cf012f30ca133fc763b611bc89c2e179d44cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325e64222daf37c11b45ca148b5fe9b0c77fce60240a1ab0a5f0d72e94e2f877(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d436db93482fc054f61b602bf5e1fc8b301271b1ec21a830a2af10e8ab41a18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ec83e3d256706235daa4af980f74c6fecb70bc787b3e0884e0e85028cd5f30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3923263d97489f409e63238820a293ed04450d8457fb06c715e3bd09ded8029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e01ec621504f9e52dc9103966cd2aa5a76dc183eaf1802942d81834586cb0da(
    value: typing.Optional[PipesPipeSourceParametersDynamodbStreamParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bd39f08c855ea221c9387cc3c8c55aff3a1a5f38b92ad3da6cb7b464a734e4(
    *,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efd2946dc73b50b497ba4cf8a0f8282b35b7977d395b7e0236beece56357330(
    *,
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b76aacc739815f3a94923c91a81602db5a8763df1744ddc089b2da9f319ff6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2beb4acabd541d86e0af62bb7a5683cce9d73bdb53b96e0386658903cd5807bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6c16e36cdd7bd0cd3ffd16113be5f12876fd2257de6171bf39df53868596c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240e913cc4abaec5ed91ae1b36e6fe1151ba8c90f97ece1d13c6b2208a1aaf06(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bda8284ae53806b769060681c4d12dc6e519f79af3718aeed0f312969a5c732(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831d591061200245c83d84221d0329974f875f30455db114f8c4a01c574b4717(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeSourceParametersFilterCriteriaFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fd73c2ffda8986c09e34d5d105816d5a19313922b1eaddc8f46721bb317e31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff67c6b0c59159d3d1d6ea632d59e38e87efdee34aabe14fc63d643f97d6d18f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278b5a1aa7c1228e698bd25129031474417ec72c59e625d446820a20786070cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeSourceParametersFilterCriteriaFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c724bf464b127394bce53f5c647f18a60976e717245d79fef5187c254dd3b378(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70f2e042d29def4f53fdea45dfecdf9a69caed510887f45b1fbf3335cbf6015(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeSourceParametersFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a17d8f5b2f38baa32095fcec8868333a971559d0e80726d075f182cdc3cb72d(
    value: typing.Optional[PipesPipeSourceParametersFilterCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c46e6643fed5d98bd95309942af4c9361bc99dd098755306ae9a8fcc5b83e7(
    *,
    starting_position: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_config: typing.Optional[typing.Union[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be08880fc07d8489bd132590aee43b230db979407a35b098d439755a74ea3fb7(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bc98902f8d0f709b69992993f46d7a4baebe4c7391e9cd1e4652753dee4a11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5051d12e0312b0a33716167b42be9302e4a81702ae5c60284a0e17e6f65e430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d004476a168997c1f2eae8cd0e32524bf1fc0b1553674919eca028b45f92ca5d(
    value: typing.Optional[PipesPipeSourceParametersKinesisStreamParametersDeadLetterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97dd812ecfa47994665e85ea63c2948c655599483606368a6d804014101227b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e6b87c1ea6b81639d0fc1c7bb04e552e5eda9cb85f0ef8de025d14f224d419(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b46f43ba61457963dcfbb8686ca4e66ef3b77c8329da6abda69ea04e78e1dbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc32931d31ccb1665480292563de9a792203f77d1925d6d2dfa615526efa63a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc85eb3d19fcfd5358321590947bc340c68880502007c2ec761773a9960e695(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bc3ac5c1a3ef1f604b3bfea40c20840b9c902fc0e2ff98fbea6afcc15b8b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed349d0bceab0d6dea1704502d00d82609653e1a54e974d071e0d484a8560261(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115d3989d565ddc9b3be1e5651856d09e3f6433c422b8eeba7d80e80daf3ffeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71aaebdd91afa661784d94175eaa1f6778f7cb981a30a5d72962d4ae54e562e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30499f0ae8ec3b60df9dffc9c4064f6d846deef62aa026f818145e9a00b2dd49(
    value: typing.Optional[PipesPipeSourceParametersKinesisStreamParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02567329b8762fa7030179d3a8b800a42fc55ed140cbb18fa614fbd933c2441e(
    *,
    topic_name: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    consumer_group_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    starting_position: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784e5a845a7f1d2068125abed71414589eccfa2dd7eac676657c3c96be8dc0c3(
    *,
    client_certificate_tls_auth: typing.Optional[builtins.str] = None,
    sasl_scram512_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887bed53c62519afd72790415c9ff817a2923e3e5d4d6941b89865f1e61ce79e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6142c7067dabf66dc7a5851bc4e1b11f812784e326c4a3b6bf0d2e771221d39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf46e6a539014dde51b63af9074583349f9b3930f232d2074ebc82a9c6c2e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9cfeb155386356d2409d8efa819afac6c1fd4d1b9bc72597b37170141db369(
    value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511914c14fe07edd917cdcfcd530bcce60a296e9a27f8009cda725c276747bec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fab8f4a8dfcfaccb081fcd91b7756711a7166c3518d9a52d0090d9ddec3815(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ec6cc8431bd7ad1cf7f4b4f3eeb7717f7a844cf4c52d9b5081ff8b9731d8a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fce152ede5f25470ffb8a4287a7eef2549db29ae78469675306d75701e1f3a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e02986d240024cf78c5b2149d58356ce2018067d69bc8c9bc5fff0240ec2933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba0553c7c843eea70a94e712867377e4e5ed7a10bc7b3669d52e6b3173910f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051f09df7d6325ce331a195692a581e7d13e1d10d1fa85ae2efee875db0cc138(
    value: typing.Optional[PipesPipeSourceParametersManagedStreamingKafkaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b478f1596d0c56013104df1a14d53ae498d625599c11287d9165e69993e9ef5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36ea00912e235eb3c7a91fecf72d13b24ed5d1a8575eb8069cbd9d20dba35e1(
    value: typing.Optional[PipesPipeSourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ecdc12ac359746a53a9fcc188b8648a30a8d4eaaff9f8428c72805aa3ac13f(
    *,
    credentials: typing.Union[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials, typing.Dict[builtins.str, typing.Any]],
    queue_name: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    virtual_host: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4c4927769f363590cffd925caf487a1c93fd8fdfd4a71d551d9e3d000fe912(
    *,
    basic_auth: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9639d63ccddc3c6ae8e5635dd17c89697dcf489f9e0de36458f18e2f62740827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fef0236563707125ad30376024eeab2089373fe0632a67d069e131cdff271f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee2b690637c1d088460a45187ed41bec75b257de0eb72272d9094b1421b6467(
    value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0635ba53e3fee7fa8d9520cc199e4a01229472b12a632fb9b33cb108c2b3f2c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d0c7299e887db46207cd6495677b3fff512bbff23e4c63983c512ce6f131b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a128b6ac832829441de1be627a3992cd6298df80413e63faf8a57ccefc9d747c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2558d8eea58772003082930db4e03fe5b2533978984f898f04976fb803ffb376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868db3c567d8bcb48783fa5dd10afee1747aff4932109ab15973f6feab4aa3ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4239e080c04efe41457859a78a354f53d1a9d0e39db26e5cec73a8bc7d76aabb(
    value: typing.Optional[PipesPipeSourceParametersRabbitmqBrokerParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff23c6584a00363773050f916a12785d211c71ca9dfbd11d11750c013f8d54d(
    *,
    topic_name: builtins.str,
    additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    consumer_group_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    server_root_ca_certificate: typing.Optional[builtins.str] = None,
    starting_position: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[typing.Union[PipesPipeSourceParametersSelfManagedKafkaParametersVpc, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11893978bfe6c1f8cbeb683d8db5b1e631e8692ae5f005e7e0b33c6b63030a6d(
    *,
    basic_auth: typing.Optional[builtins.str] = None,
    client_certificate_tls_auth: typing.Optional[builtins.str] = None,
    sasl_scram256_auth: typing.Optional[builtins.str] = None,
    sasl_scram512_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d618efb25e50d23e405474607bb7d43a6249ba5c99be9fb289d7a12f271470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e541cc812180ec9d70baf22ec74cff511d66490856cb60db182ab72ac666375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec231ca1fbb5fef5121e7219b3d8f53864c91b9776f886e05f8073776c03c2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674122d4fc49dd3a27b39b174b127f9635fc7c319b29f8f40ea6f2d1b6ff8189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4badca414f17a8f1dfae79abb17d631b5ab168fa15447e6581ff7b1772cca4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2b683e9e0e9a4018dcd8365e149713472dc200b18d506b00c789885263e88c(
    value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce120c141a88d06cd805248f1c196b7fbb544b60d009527e4ab84dacced97b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5410d7f5133c36d9cedb144efd89891efb07143819627de6152f602aa4d49ceb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092a682bb3e29118bd6f5840965fa6440aa60a1f06ce660c98ef36c5ec617cd9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159e8478b7c70f84c85bac4e57c1d3df7f40229db061fb743b59202e226022ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2407af6ffa2a2ff9d08af0241303d129187f20ed975b20b7f896bf24f7989b0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c070d6bd1df50e87ebc6659f035e7438ef39c8bce21832db2daaf17ee086659a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91f4058094925c85489cafc913d21a344b911e8c9865ca836aa21d5375517e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e4d51004ddf826d5c3646ee0314d339f8dfac31b69aca55b39902788074098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c6eff7400a43ff2548172099f61c7d5e6719dc9014279d48241c0a3f7f60b0(
    value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d582535e185553e2fd9134c887faa1372838aecf67d05e5d066ed77a02485e(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5978d89445306248f3559e74b186926e4d6ed930047076ecc28c7b1edfe5f30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e36408451997903984d4e4c238c01e54b7f8eb025c499bef7060cdb9db290ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baca39933f7cfaba9906369bde2d087696707222ed84a0c0214c334a120a6efb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75356f0fcab0f63d45a6bb9b81ff165f18487cf8c913e96ac4e90bf109d6f36(
    value: typing.Optional[PipesPipeSourceParametersSelfManagedKafkaParametersVpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c562074a6bec572bc8010a9eb86cb9ee8883fd4836be2a3f13513f3dbcace0a9(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b6b8442cdc59b96a249246776419aaf78c31b5add950b89c9df3ae8746a60d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46c341f29621d8bb0bd1365efd8d4b47585ecd47cd8464e42b8226f3fbbf877(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e255847aaec34b61c2f256ef9645c1d134264246f2cb0f67ad2041bd39edd8a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4183d600871595d8bef51338f0c75f7700338c975536b5fb087d12edfa4237a(
    value: typing.Optional[PipesPipeSourceParametersSqsQueueParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517264ccc4ab8f4865339a0ab5ecd726595b2ec241e126f0f71e7479bb9c1455(
    *,
    batch_job_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_logs_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersCloudwatchLogsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs_task_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    eventbridge_event_bus_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersEventbridgeEventBusParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    http_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersHttpParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    input_template: typing.Optional[builtins.str] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersKinesisStreamParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersLambdaFunctionParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift_data_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersRedshiftDataParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    sagemaker_pipeline_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersSagemakerPipelineParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersSqsQueueParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    step_function_state_machine_parameters: typing.Optional[typing.Union[PipesPipeTargetParametersStepFunctionStateMachineParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d507ab3e09c043407350c30d370115ca64b7f563e39325ad9b008412952649f0(
    *,
    job_definition: builtins.str,
    job_name: builtins.str,
    array_properties: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersArrayProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    container_overrides: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
    depends_on: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    retry_strategy: typing.Optional[typing.Union[PipesPipeTargetParametersBatchJobParametersRetryStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab124f5d102ad05e9ce981b3fd55ad3c2669bb71004c033311ae184d54d1218c(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddc03d34b3d1621e2053d3a01b8afe4d57d02a294817ea6f67555b7aa385e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad9bda15236fc12e0fd91a019bdc322f627eed36f3d2f8c27627f7c5d139d50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72063a9a4d118a97c2073e50ee661c6d434b3c4913eb53bd1d83c697988b8e8(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParametersArrayProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d124d87cc47d182f3e94b6650ad7d47475e5c0ef62d215f5067a72446e9f046d(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10167ad770981379de62d6c2b29c1ab3e8a6ba8fb186075f977cc7e23daca749(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611439f1aab7609392489478f7ffbfe35569cc6dc94a741bef77e43127e6ec8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e99ea5e18fab78099549244b4d7698b7c4ff3ad264be409947858423d9bf229(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beab07798bc7b95fd9d6b49c29387ad51d24b9b034cc3b4f3218f2208fe8deae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed8e8d839824a98c315cb4b5836f94a1258db5879e4103b29a1141437fc927a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e959caadd6d03e9aa576ee646abb8dd233e2ecfb87b8aed29dd53878d74bfa2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3bd6193d7dc5779c221089a7674951eada601e9a2a94f099944a51664248ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9f668b9abf0d4450083cd01fe5492ea9121092d5ee23be1d08fe12ccb616ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e84314f9eda9356706949b4890c424904fe38e52acefba7bace849fe52e5dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbf3563a9189eca9f9cad68f3224ee03d039663161bb8a45277d04a4172b149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd47584158b589386a951522f9e45fd60ccbce0ccb0b041815ac5f9a0a618e6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa72e3d7d1b7ccd28ada300ff7c09eb02d0d3da3c353430e076714ce31a956d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25fd2621d59a2d71cf6637a5c16fab8e379d37861773297867432b832f13633(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesEnvironment, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3affc2cf9068a62197fa822f084d0cf46ae6979d2d3d2f59d9fd9b3a8c1469(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a663b3be7cfb9dae96ad2b8c7f1b433d9a16f7d146cd213fb51db3abdfe7ef4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1994b747aa42807ca3da38d3de8665829c640567b9c6972513721fb3e979c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098df9d4e26cf84a8a7acb552361b688c93f8a82b2cf346d7415ab5442e30665(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParametersContainerOverrides],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b247381962513f50e69b1c3d8e437826ced6420aff91fe39f816bde8df03024(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1a70f9238f4694d021d9ef362ed7e04891730a6b5c09f60bad8c9dca291668(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cfc952741464f858abcb5a614da66bd48ebdb3b8a37f4e8b3aec7937ae5cef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319905867a59a794c5330d9f51ce02ac92de277a7f96d0f66ca916cf3d6c370b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560d8d2b2eb7d688ee184eeb9bb82e138cce7bc19387c1b9f8dc611dbfb5fd7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb61deeb17c5e2ff4bd1349f7aa259d4539a1c6cc2f3d98d759969a337596f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53deb18ca68b556f5e92444fb7815e7c917486d3d94b9b7c189029858d92905(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45186ffa937c8d0bb29071b26f2273c815bd3238ed09eff8d889801d12cf0495(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ab39fbb724346682a53cf62327aabe7c0590baf0dd799a51824c7932852a95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec2e1453102c0a460d1781418ecbfb0489dd5ed25ca179405fe5bd9150ac43f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91235bdd666c571f30d65288bfad4125fc97622a02b0e05a7eeb5701b0bedfc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersContainerOverridesResourceRequirement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b24bee1c386c3466f9bb2072be07c0f1c0cc76ae59fc6b357d3b38091c8633(
    *,
    job_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f86fe68d93c3c02d302b25fd7d8c80fa238b4c930635123da339848d68ecc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a8f3e4763a5ff9871012d8f44aa76f012200197a807f0701c32e0ca49641bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc284ca9ddf885440b55c1a0b401f5b09450b11cfa255d56b204106dea89befe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f10e8caf6935dcb4347b04b2ae69a5d478cdac7556cbe7fadfb428ee83e2c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646285afee39c3fe255e6c4775d0e49c0c29a7711f0c70a7b074f0e70fe15517(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347afbb6f02578fd6f0fa7cd4b6f0f6a8397c274be38129324c14557f8ec8ddd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersBatchJobParametersDependsOn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c86d6753b5c5c7ac20a094a1f7d874df060f3e729d4fc3a6fb9883daa879cb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce04ecdbdc34adf6299633ed716900449168e378e9b68fa0eefe46bf7e761206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca0335cedecc72a890f5ab35adc1453aac356c971566488564b909a755c938e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e474b86804e11b62fb7f413ef1ab666d4087f41db2fafcba8487ececa82854e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersBatchJobParametersDependsOn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e3d7dc770572b4ebfc8352cda7c9288fafbc2ab29e9dccdad7780acb5bb752(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694b1fae9c222bd4ba6607a4b11eaf898d86cfb0aaa9cf90860171c0832a2258(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersBatchJobParametersDependsOn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c0fb74e0b269f73b733b021373b6e0b036abb4ad901c1ee511791b8bb90520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e6d9842f8d328565bb8068bc35aa43c9c95041e7a4c3f7094f30f598d7e9f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c3334236401edea72e51ccaea760c3bd5f327687e47f190a6be7c3f8aa0df9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25297960bbc40132218b23e481713f4cc9ec865b3c2e71c49222779684fa902(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6378cbb14a0a38a00b8bd631e770025765b609d064a2ed7b8cff0405383957(
    *,
    attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3028597cf87105263db0a47468cf3664958702b5ceeef16c371b49a54558b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0469de7aea9d0df25936fc1afe9578459a7343327e41e20137258b8ff53e13c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630e9dee51b08585bc5b91df62c1e1894238753d409d1774d34bd8844e877bc9(
    value: typing.Optional[PipesPipeTargetParametersBatchJobParametersRetryStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d33089d04cb02df362af27cbbe24a9418e21b9379930590ed0c5621e2885fcc(
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6589b9c514d88033a49b6377468e067a72b7622abcbfc6e24f8da4c752d636a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a39289fed8ad65770be5e92b245ab9189a08a7ae7e653822facc3dce6af9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceedecdcb238e4762c9a8550cee02cea282fd372afe18923dd04dc041d3aeb46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190143b9999f7af0e599feae8b53ab32663ad8e4ed91f29dbe2a21edbe89d170(
    value: typing.Optional[PipesPipeTargetParametersCloudwatchLogsParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1a05199a24e51ae60e3cadb3fe5891a2ef0036620c211715de72268356f38f(
    *,
    task_definition_arn: builtins.str,
    capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group: typing.Optional[builtins.str] = None,
    launch_type: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
    placement_constraint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    platform_version: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
    reference_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    task_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661756089b5d97eab601c57bb1bc934e252e220a16e289398975e36f2e708065(
    *,
    capacity_provider: builtins.str,
    base: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080a2b80105173f00ad5d29b7ec9d2926d0418052bf4cffb1a1cefac02b63b0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2d8787e9c08714022ad22e7e004d36fdab737cfafaa83e82e8d5f8b3938077(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edb4cd4f4c95695aa8f81528c61714cc8a8ab96d5036a61a2458ae2d7ae9df5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0c173a638f2595045c45ed659a07e512e76b0229089dd5e6bf56c766407ea9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0980c3a57ce4a0b5ab2e55933c104156d79e6b6f9dcc8aa4331c43b029dabf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253b7e1d3eb8167d15bfd7ba65b8708fea832945a281c448b63dc2d3c0f52602(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1ecca2a88f7899ae35d7136fa6587cd18fc2baa35f3a4d991cf76f11c1b0a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069e2b04f89d5390e9eb6ee37719782480a72ea67e02e60092011f34e041a338(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c9df6a6cc26c6946468bbfb79e070dc463dd4fd6434faf4dd7527379ddc0b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789b18fc675b4f5955e0b4a30e6b308410ecef4b7c752d284997a498bf29afef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824fc3c4ec6caf4fed16b7aadce67168e524f44b56efc650dce52c77b3680be3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ed8b695734cbba1ab90ce7a0d375e9b2195560badf47344c0ad379fa2475e0(
    *,
    aws_vpc_configuration: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4e9b3763362c4d316fcfc948c5b35e3a7a0ec27df3e68093e33b75e688a5c9(
    *,
    assign_public_ip: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a165ae2c2467dc103d344ee49390a8e70d30f3cfce6d98331575b98dae571cb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc696a46c0eff0a25e0d08e891ceaec15fee4d8455090ec2d9c1f333fe992f4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c315ac80e8dce8fe20513e23ac2528f23b46f84f0a666ced3259c19be470a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2be006ca9d70b9d8effea956991ec54d7ff1da09fdf555af56f4b5171472ef5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8d6d239a4092d84c8861e2854bb2d4cba53d152be14602284c79f107e533bc(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfigurationAwsVpcConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2130de0f148d13c3d5581b2138bf523275f56d563e13da825109e27623ac57ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dec30e6b074eb33a15c0d180ddfa55bfb09d98d2f91737590140133c85255d(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac33f2bfbee99836198d6540000bc1ac3b0ccc5f2764984d9af9e89d792169a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58623cbefb906f45dca683c4e7714ea073da6f3e1619de44604b27890814260(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7083dcdc4a3e04ed11266f984e9a789e613a2caaefb88b499f8edf6d5bccabe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae6bdd8125edcdc5f68424458f10d166484d2dd847cd4a6819bea299965d02c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0285de38b2541026a75549cda6ca1b35b0bce0b0eeb3e62ed1b852b5c71c7bc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d827ea2c75497374b4d6247a295c5d03c8fefa773317d9795fb7e7e55b2a47(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b332eb362eb5c4c5424df659e4c8efeaeab55edb19954a9cb3df059a36822d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c165dad139e6b96af351ea8c6a12d6980efbee5c7b52d0a309bc299e711639ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980a496cd7703797ef5493d7d3ec4c4494efdec7089389707eb9f56af5a448c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162ef8b588dc9a211fa066fa6d983b860a53a3d4b2c7802aadc0fc88cdad11cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6f5608488ff4fce7569c755c84d3a9b2d153223019b4ac30c0fe139154854e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59b2380cc83296667d679e843368b15344a78aaf2207012c0ee5b3e779763ef(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac76d62b9c33a45aa793ba633e49b0ac976ec8e5d3f83ac398e9a19cb72b09fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae5e2e5f720e72815b8dbd8c04a19db8448e6151a323e8f821132c3a3da3de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c69e5ca053a1ade0e5722e987b46a872756e5a10207fca627664046222e3db(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc0f097ace15c0b3afec310fbdfb66e32f0b8229f8fe3017d3c2c11210962ff(
    *,
    container_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cpu: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    inference_accelerator_override: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory: typing.Optional[builtins.str] = None,
    task_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad2028fe7aeb2abe4fb4c7e769e582180f6032e74ee05c4d78b76a33805ce30(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environment_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_reservation: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    resource_requirement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e11339c9ebb9d9d701f298a78df71f002a77760383c979bae4d84f2d5324421(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed979cf96c3bfcd95c753355d18482d36d25a467dc9a8cb9bc692994e4726290(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316290cd049434e322c6bcff5cd017d9c8ba122a72295a8b34f95df8b9ba8850(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092e30cc25adc326d2342a9fe6c6dac1b574b4b4c81a31dcf2609596de85d492(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e5f75110cda085aec0aa203995a3beb989fc96318dd81b73e76591a0a590dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cb6ae8e6e38a7ac674eae4131eaba1de1cc0018ca545b44c348c132e3c90d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b4815e674078e612970a8ae015b2dded9ad6ab1d2da9b35c4bdab6793e293d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe4cefee693036e6191bccbacf666ebe2e0c8b37a2b06eafa23ba0dc65cf031(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1fd60dc084d38a6de334b66f1e04ab25daabf978c1b5036bac33f765a98972(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bbdef1bb0ec5e676367fd908b7ce64bec8c8a2b7402c6b7af48290a7b2bb45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f74c89fd2a446a2fb183156807bca337972163ef2eb753378fb81deb11c014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e93de00cb3691eade49bcc8180303d7c40a26ad24564337872ffce513952de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa5f28cac097e47c529fb1caca63fc2380f072b5461c3e647c020de2438b397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bb88bc1d09c7ca891905e516a6fadfbab20a1dd9e68dcf43313a0d0b18061a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d529ffbee974b56a4d7653f1065ee9bba376380863eaeb403e48af43d7c97296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bedfcdbf51c1318b6050bb72791d3c10779716f7a9a8c55fec7ff2a6d53106a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989b52e1b8282632dc3672d635ecdbd43e0538961cfedd52fd7490159a2aac24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641e85206b66ac878b8599bb39df80fa8dd47a283c7da31ea7539a02d464ec88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4cef462bccbbc5438f19726735478fbba63a41ba4214eb873d9d51c5f78369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0e727343cf92d0742c7b4d7c33ecdc76894693e94f924237667b10fafa9d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710e19bef2182fde54b49ec59994cefce0c1cf8f5c0e5fba0a94bf6b53f8d735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7501c8ef77976c08088df6640814d3f007864019ef0c046646be4212e8039faf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924bffa29d6c1733e18cabc1dd27fa8698586624488fe1493df887cd575921d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48730c31ef479295f61b36a22d1f5ab054cecb769c014796965cd3a745c6abb0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63457818fd425f60feb417e05e86860399093409b32c9a60ff0110ea8c622775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03aa6c8a47cf48c5f235ebf76e260077753917282a008de04d43c4a4b428fd1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac3d103e55ef194caf866e90326c73389049c7e32770e0a1a2efea4d7847108(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4474e6580859da7ec499735671c64b7bddf9d000addc5b3bd6305614f89c250(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ebd5b9a6f92f64ad22b1331ecfbdf09be2b6cd10fe9c355fb5123177a0d214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd9571ec234036e2c66bd99eaed10ad92400bfe4d0feaa2bcfb78b387859fda(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironment, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2bad4338d2421e5f40b11b3268ea99f830ee98a93fb3870f4f7fed982d42f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideEnvironmentFile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b520275110dd7d6d20006a3328689cc8da69ee8093098698dc266e1f365beac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3318cec9fcf42220c30089b0bf2a2b80c056278a7a05ca6dea09380394f5cd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ae0fa51648d8ad5fa4e9a7ef92f660c1376b850464db80e2ce1a60f8da69be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdd44e84dcc5514405fc3793738937c8f7b6512ea73f15d548892e7d5672951(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7bd407eef0bca3d1e5d057625760f9e2b3311a830f297de84f0a01836414e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5201d46a04217f5ee7d1671d0526c1f015a565068b2adfe3077808411084c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63fee808bad3474a6f11848dc7e39aa6555342419573bc7a25264051d47ab2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52020c4ca61fd22e13be4b190ed1ab86027e57694ebf4f17fbcc044ca730d091(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1b6d2dd6cd5151492bf6c15eedea7a4bd61783c2750f930a3d218082566796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff95afecf0d83ffb93880a280f4bc5170a3f42400b448a8ccd93e301d179493(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4a1de7d660e39ae08a14e0d35a062e0f9d894bb3d41e21334e38c6319323e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52089b9274a24e4ac85dc7281a3d6a76dd21a811daff6b55da6f5cac83e72586(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488d793456d88d815f9cabad67d8538462661a18b58955d9ce7fc450908ff469(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464d1f5ba0697a32012f4efe3c452bb2cec70e065b82bdf604c7938d37635648(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7935fe61822f652a191002cfac04a9f363adbe858cf6780e69cfbbf581e91f4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50e2f4d290b0b2708056afeed1eef5a04674bebc7262fe577229d66845be809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64029b7d3375b08d47809603e15d9002551764ce95fbe169c4a69ee87589cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed92d5ffeff16d3fd25d01b7048b0c53d4a0e83ff6648bc3675c9503f8c9da6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverrideResourceRequirement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1451a0a3e348bfbc8455837077216987590f7c894c00b24c9981a9314db8f7a7(
    *,
    size_in_gib: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210b6f679972ca5639b96c058cb5264e797a8f6e0941f8f02c6a671f5ad803d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1cf44b680fe2b40dea76441acd672c06368fddcb7153304edec25eba482255(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3e260e53ef2524d2700af3c0221e7709039f111b977c59675f35478cdfd2be(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverridesEphemeralStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1b951f7cfe94bdd2c12c74e8c1a2443d943a0efa8961590f5f73d4d8526617(
    *,
    device_name: typing.Optional[builtins.str] = None,
    device_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca538002bd97059b0551ac9da1ba8f05971a2e80084c22bae2572f15e73c1076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596482a493e53fde35a567d4193d499ef9680bd8fff9bd2d585796a1a1f5d0b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edfd6efc3e7772b0a9a45b7930dc909be4e9e8874cbb39917c410dc65e3103d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaf67d69685a60f0d4923dc7234b489c2de7aed12d7f972c9d7349db5aa1b5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f86647879d8a0aee7e4fa83ddac96965cd50a4731f4d55e5360ad88b2f4b11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af92027b38d82329f0b6dbf64aa17bc99b654b35476956d0fb4f0551f601d17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459db39d683185533033f0f7a4328f523f0b3342b312b02cfa82b2f61ba751bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fce9386d499310a04b8a28cb5501963783ca52b31bde2e3de24f28575e54be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6317a8864ed9cb40077ee9650bd1df3eac58260cb810f87f3207a3f7df37e9c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341fe47839b0b0a8e3ad7e01bea0c428c0c8659a99ae693a1dbb8884ec189098(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dba157fbe772c51664da115b10866e31e7d0d7fbc1644815ff5424468af2fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5cbd1705cba4bf9d4622168394d2a6b89c0efa2becad616c238bca3b47b9e51(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesContainerOverride, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f8f44a14897afc495e5dd6fbfea3ef301f16295993026b6feb08d07e23d215(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersEcsTaskParametersOverridesInferenceAcceleratorOverride, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19856fdd98e4e9c92936ba83b8570cdc8b545d0eed9bf1e177e10558e8e4d148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4f295f2a6e8a411a291072ae1e577fea6fc6102304fb4927bd889b0e9054e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618d4bcec4542a876a20fa3d481682e8c055809764c4353c7b3abd57bd5279c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9187d9cfb3bd0d39728f914cf419246f5da1394acf2b260a48afb54a6e0741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb1a8e9e37f78629e6a1a1ce61a4ff6f082bc7cea4aec9e65e2f98f8555d426(
    value: typing.Optional[PipesPipeTargetParametersEcsTaskParametersOverrides],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf32cdc55de9568f6b9330dd43091547f544c53e0f8e23e0c313398ba6bda66d(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f45c8f3611d8975d2e60ff0cfd607f3b90233978b8b611b03113cbd6480299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acb7a0a8cd439d4f77871de4cdeb44cb73ea4dd0ad71ace0737e6b4ea189acc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c9b9607f3011e21bc1a28ea969ba883d86bb3330a8a3383b283de726bb4418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2de164b3cbe276117fdf1ccb9856c38c1698e4fa2f06537e07a1220dcc01e2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2106f95d8fa0510e3ab2dac336c18cdd217e9597b9a63fd5a601e5da8590164(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c1e63b947595c0494ea8e53bdcf3170965f49b1672d37f5f3f935fcedf7369(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8146c4bbe5e153ac43de733c9a4a24a39f111e0f9265f0d1ec4affe2afc4c690(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d5c85a8daf8e0bb97f98d05f254a9f1e55fbd67c3b88a52085f2b327df761e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776354ef60c1d9e08640786a983995d40e2394d933c48e457d681c76299a32d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9d41d72f861a2a1c710590523beefd354d7faf1713325d0684abb43ad00be7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementConstraint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0601883476a6e0cca204abc0b3f7649e81fdf663fe68db9c4aaa5b3c15fcbb(
    *,
    field: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8dd2e0cd0dcf6760ff016bf89e621081d216f1e211507a0f15dc4f5fc0ad8f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdb65b854804c944901b7ead61f20e911bd7f43ef80a64a307030018579b222(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ef62ede77f328a2ed0fc82a5518f2a4863e8baea3141d68d5e23169a529627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5a02e1f0fac0b6b1d2fd216d4e98ed7f3104c4ca32957236557d7866502d89(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9cfafa9821ab846681c079ff86416d68bf72b0e55ec71d34ecacfa884b2eda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a931502582a6e2bd16fc509c0a9a3dd250c2f5512ef97255f6642126087c6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367c6c75d2ccd0d5ed3ce97a667c893d45a8a378f2d602cf2a2d622423d84d38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ec23b3634a50f5b94c2df0262d3cdb0356f2ab5841d0dbc2e2732f67d78e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2356d5a9ffadf0d23004bbe84cca72f8a27695385f3f247cc8baf0c3872375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115ee7b18966cee00ac8971c63b667186d435dbe18c3295d136dbcff00a9bbe0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersEcsTaskParametersPlacementStrategy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19ee0f621de4b5274ed809d22f8717d76980aac7a588ece138055ee41598bbf(
    *,
    detail_type: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5332d32c88b5b7b6f596b4c2135cefa9086b9f1fb0e09fb7a7ebf11b2cac1ebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38cc172bb65b07ccabcf6d333aa21cc884f3c5812a95ae5bfb02a7c6b44fe61c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209ca7dc391123a1f965075be6d5a22f8dfbe51e6975dec5733873f3f4a229ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10d2b0e7b0213c2148df8be016b0dffb7e78b1a400eb13754e1531ee686e7a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c739edc82cbcc5aeebb50a4203427bacbb0304b847ef9edcd6f59b2846ec8a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1577c8468b726399cc45c5446897ca9797573ece821eac8d3c01f418bc0987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fce27582cddc5cde444b227c61511301561361fb2281d861479254271555e6(
    value: typing.Optional[PipesPipeTargetParametersEventbridgeEventBusParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f9878fe9ee0d9c1d5a39108407db0e877d3b6014a04f708b86b5e360f478f5(
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84f1fd449a15bc7a14708fd9f8d169a785841b21cec8e1303d739077d13a57e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10abf67d8d240ea003b5756370919a0debd00e1e546aee6f475f397ad9145b7f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c7ab4992b77ed02519ce6e1126478ee8551c1228d11745b78c13c630a5bbc8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a86949a523748d52538f454c1b24ec9bff587018cf458e40d28a3c43b10af8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fce1a56d42aa730a9b5ca31b6335d9bbf898c86aa5f8166e186557c8fe5dac(
    value: typing.Optional[PipesPipeTargetParametersHttpParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581965ae4e458c91acd2cce33d22228fda2dad758ce3a1f1d742ed8aa30c02d1(
    *,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524c61c935dfb74f707aa9873021d53610024c332b1856c45e978b4212aecba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9407b18c00d3f6d232fc45a37ade63859df5aaa37852ccdadbc2a61ac20532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c3df58d13896c5fb2fab34a332ebdea50ee4cae9bf88645a44ec8f9b8b26d1(
    value: typing.Optional[PipesPipeTargetParametersKinesisStreamParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e58163a3f1168cf4d81ebafd1e025a1247b1938d2b6de1f074c18ad7f1860c6(
    *,
    invocation_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150fb01c8703b3ecdbafb6653678e986a6dccaaddd4054971682dd9de1783bcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156b01c53f2c741dca797b10307b1f8868408d92f21d2f6bff40c00ede9daeed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257e65100f69a98ac6d0ba6f874b98ae994bf26b61ff770d58fdc9cd88bae0c5(
    value: typing.Optional[PipesPipeTargetParametersLambdaFunctionParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0fdb117ace85b72d4d89a5502553223ae391a4d6335b421266000ba20e17e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1203e54f309e6121db523ed6e5ab029cfc6c0dd82080ed46a83bb123627f0e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8afdd6f4d46d0a354a392b920e80aa5a2d596f31bbed3bf4c747fda0370013(
    value: typing.Optional[PipesPipeTargetParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d80323ed7f563790e811a29145124d8c9abbf2158bac63aefa25a4678e0c58(
    *,
    database: builtins.str,
    sqls: typing.Sequence[builtins.str],
    db_user: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    statement_name: typing.Optional[builtins.str] = None,
    with_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014ba15f1bc4b7a041a96da6d781dca341c495daed608b16ecf380aaa3d874d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a442621d69a6b44b61ad9fda165b1e11144d017e575301dd5ae8b62c1f30a573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e940192c68bc7713d1491bf3d48e89df4c8c0037c7d4ce3b2f735a22e0bd07d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a6cb1165ed73b399d7483186ac75307df0bb1ca8abdd07041c76b1f70ae057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326e46496522cf3a50c67857583d97264568701c1ed73fdc9eb0cefa03d3ef0c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacd29afb98c4f86275cba7d801597918cb028f81b13f21250cf8fba574ce301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfd1fd07ef6083fa1366ac1be10e9a9202b8198e24c487e98a4594699c91621(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac02df3156db76f1922f3328dac77785b0cfb27879ebf606f824e1879b11ebc1(
    value: typing.Optional[PipesPipeTargetParametersRedshiftDataParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f6502eec0df20235ee40b2ecb726566ee7e974ee56dd542f2a53070968e2c4(
    *,
    pipeline_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7ab10ee3347003d95f5167ab84eb1b7a9807841ac924f2652774a6f18818d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f9d6d47014fea5b8db7712ba3014928012c231114442ebdc438515bc87eae7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c70812f0ee26da962d5caf5a3c33f1bc5cf19c0da8d526609fd79d871e7e1c6(
    value: typing.Optional[PipesPipeTargetParametersSagemakerPipelineParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75feb0c748cf597b2fdf85d9157c7361a1bb685209d68a6df386b25e9c8915bb(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090f7b561b8747f46d322e8616423e6a39564cb8e8ca046c9861326cd8402dcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec78f858dea484c62da11cd01a0a3067e8a1b651f7c372f47807d188720698c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e67dde4fab21f3603c33ba212028dac34eb585b856431d5abce2387aedb903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc89aa7650ff59b42fc07b8e61095061f6cf21aa0a60ab1217934a9149010bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9b8a5122cd4541e16a4b83ec997aa8aa31a867dede71d8066ace7272d756d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5b62dd26bcf48c1fb0f0dae2dafbd95e6036635fb1ee9aeff15f54eabce578(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a73d590291fd8af6ac99fac3424c7b7cbe6ced87e92ff211fadc28f5331f444(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f783e108d09212aa851bb537c9b10a2e29994e03fe6826aa6a424c95a1a00f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7e7bada7b3c954dfbcd88d7ef2f7f03e690cc4fd4590aa039bbf22d6462162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3c01f9a1c1d24ff58a3df58e6e17fa30ca933c778a8e53ce518be2e37e0723(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTargetParametersSagemakerPipelineParametersPipelineParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba0676b888273124f513b071b348120152f6c9401ed618b7fcfeb158426e11f(
    *,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342c0b768ceb70b342701252f7f88e71fec277704c18d6f1ce6aa8abf95cc1fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8a11d251672aecc6fed208cd5abde327fe29c21bc38ee0af8a79f98d118aa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279a1b919b0717dd6058082b06ff1585c39657b6b07c78a5e8e02c19b4c3ebcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96140183c3ef9ac4c55044029101756cbd1dfe6c0035754216c7f65ebbffc71(
    value: typing.Optional[PipesPipeTargetParametersSqsQueueParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b75f3a843bbcc2c553941495b4b1ae639417a8b46ced4f6fa7e1bfee5f4f88(
    *,
    invocation_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a817ee3e7a129c32ccc87dc80ef1f7d2734a741a4f901425fea6f5c024638e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80545ffb2d8f694623d79d093f85c599eb674f1f8239d5cadd02c2c6687b3596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c566f404ce6e2e6ba65c3b8ca18162377a77907aec9be4feeaff96e6cf94c1(
    value: typing.Optional[PipesPipeTargetParametersStepFunctionStateMachineParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b44988988af52f926f544fc50bbaf6394e5a935b60c1f7084b281351552867(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28eb8dcad5cd1826d98830e5e248115b80b299d7e5400e7601502ead7f05c7a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7c57f002969ff0cbaeec168425fb5066661ab4b6599ccfd950cfae2e54ee25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8182b65a929d3acbebf7b7ce7024843904591b653769f02ae1df7295f3b76a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed18888729f2685d425182925d2cde8a265a5130908c006a72f47516ab54ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d9ed8af9adfb8348cc79347245303cbc168b33a9d524b7b72b2ce99aab8e93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PipesPipeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
