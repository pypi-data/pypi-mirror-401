r'''
# `aws_lambda_event_source_mapping`

Refer to the Terraform Registry for docs: [`aws_lambda_event_source_mapping`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping).
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


class LambdaEventSourceMapping(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMapping",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping aws_lambda_event_source_mapping}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_name: builtins.str,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        document_db_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingDocumentDbEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union["LambdaEventSourceMappingFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        metrics_config: typing.Optional[typing.Union["LambdaEventSourceMappingMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        provisioned_poller_config: typing.Optional[typing.Union["LambdaEventSourceMappingProvisionedPollerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["LambdaEventSourceMappingScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_event_source: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping aws_lambda_event_source_mapping} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.
        :param amazon_managed_kafka_event_source_config: amazon_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.
        :param bisect_batch_on_function_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        :param document_db_event_source_config: document_db_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#document_db_event_source_config LambdaEventSourceMapping#document_db_event_source_config}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.
        :param event_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        :param function_response_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#id LambdaEventSourceMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#kms_key_arn LambdaEventSourceMapping#kms_key_arn}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#metrics_config LambdaEventSourceMapping#metrics_config}
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.
        :param provisioned_poller_config: provisioned_poller_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#provisioned_poller_config LambdaEventSourceMapping#provisioned_poller_config}
        :param queues: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#region LambdaEventSourceMapping#region}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#scaling_config LambdaEventSourceMapping#scaling_config}
        :param self_managed_event_source: self_managed_event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        :param self_managed_kafka_event_source_config: self_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        :param source_access_configuration: source_access_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tags LambdaEventSourceMapping#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tags_all LambdaEventSourceMapping#tags_all}.
        :param topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.
        :param tumbling_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb6ce533c6e65a9eb56e7ea548824ddb6aff1511a296fbd99148b15ab735c2c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LambdaEventSourceMappingConfig(
            function_name=function_name,
            amazon_managed_kafka_event_source_config=amazon_managed_kafka_event_source_config,
            batch_size=batch_size,
            bisect_batch_on_function_error=bisect_batch_on_function_error,
            destination_config=destination_config,
            document_db_event_source_config=document_db_event_source_config,
            enabled=enabled,
            event_source_arn=event_source_arn,
            filter_criteria=filter_criteria,
            function_response_types=function_response_types,
            id=id,
            kms_key_arn=kms_key_arn,
            maximum_batching_window_in_seconds=maximum_batching_window_in_seconds,
            maximum_record_age_in_seconds=maximum_record_age_in_seconds,
            maximum_retry_attempts=maximum_retry_attempts,
            metrics_config=metrics_config,
            parallelization_factor=parallelization_factor,
            provisioned_poller_config=provisioned_poller_config,
            queues=queues,
            region=region,
            scaling_config=scaling_config,
            self_managed_event_source=self_managed_event_source,
            self_managed_kafka_event_source_config=self_managed_kafka_event_source_config,
            source_access_configuration=source_access_configuration,
            starting_position=starting_position,
            starting_position_timestamp=starting_position_timestamp,
            tags=tags,
            tags_all=tags_all,
            topics=topics,
            tumbling_window_in_seconds=tumbling_window_in_seconds,
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
        '''Generates CDKTF code for importing a LambdaEventSourceMapping resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LambdaEventSourceMapping to import.
        :param import_from_id: The id of the existing LambdaEventSourceMapping that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LambdaEventSourceMapping to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273380baf80e663f9d240f7d4645a1aa5d21c92dffb6bbfe2d80dfb83dddb7ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAmazonManagedKafkaEventSourceConfig")
    def put_amazon_managed_kafka_event_source_config(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        value = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(
            consumer_group_id=consumer_group_id,
            schema_registry_config=schema_registry_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonManagedKafkaEventSourceConfig", [value]))

    @jsii.member(jsii_name="putDestinationConfig")
    def put_destination_config(
        self,
        *,
        on_failure: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfigOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        value = LambdaEventSourceMappingDestinationConfig(on_failure=on_failure)

        return typing.cast(None, jsii.invoke(self, "putDestinationConfig", [value]))

    @jsii.member(jsii_name="putDocumentDbEventSourceConfig")
    def put_document_db_event_source_config(
        self,
        *,
        database_name: builtins.str,
        collection_name: typing.Optional[builtins.str] = None,
        full_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#database_name LambdaEventSourceMapping#database_name}.
        :param collection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#collection_name LambdaEventSourceMapping#collection_name}.
        :param full_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#full_document LambdaEventSourceMapping#full_document}.
        '''
        value = LambdaEventSourceMappingDocumentDbEventSourceConfig(
            database_name=database_name,
            collection_name=collection_name,
            full_document=full_document,
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentDbEventSourceConfig", [value]))

    @jsii.member(jsii_name="putFilterCriteria")
    def put_filter_criteria(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        value = LambdaEventSourceMappingFilterCriteria(filter=filter)

        return typing.cast(None, jsii.invoke(self, "putFilterCriteria", [value]))

    @jsii.member(jsii_name="putMetricsConfig")
    def put_metrics_config(self, *, metrics: typing.Sequence[builtins.str]) -> None:
        '''
        :param metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#metrics LambdaEventSourceMapping#metrics}.
        '''
        value = LambdaEventSourceMappingMetricsConfig(metrics=metrics)

        return typing.cast(None, jsii.invoke(self, "putMetricsConfig", [value]))

    @jsii.member(jsii_name="putProvisionedPollerConfig")
    def put_provisioned_poller_config(
        self,
        *,
        maximum_pollers: typing.Optional[jsii.Number] = None,
        minimum_pollers: typing.Optional[jsii.Number] = None,
        poller_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_pollers LambdaEventSourceMapping#maximum_pollers}.
        :param minimum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#minimum_pollers LambdaEventSourceMapping#minimum_pollers}.
        :param poller_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#poller_group_name LambdaEventSourceMapping#poller_group_name}.
        '''
        value = LambdaEventSourceMappingProvisionedPollerConfig(
            maximum_pollers=maximum_pollers,
            minimum_pollers=minimum_pollers,
            poller_group_name=poller_group_name,
        )

        return typing.cast(None, jsii.invoke(self, "putProvisionedPollerConfig", [value]))

    @jsii.member(jsii_name="putScalingConfig")
    def put_scaling_config(
        self,
        *,
        maximum_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_concurrency LambdaEventSourceMapping#maximum_concurrency}.
        '''
        value = LambdaEventSourceMappingScalingConfig(
            maximum_concurrency=maximum_concurrency
        )

        return typing.cast(None, jsii.invoke(self, "putScalingConfig", [value]))

    @jsii.member(jsii_name="putSelfManagedEventSource")
    def put_self_managed_event_source(
        self,
        *,
        endpoints: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.
        '''
        value = LambdaEventSourceMappingSelfManagedEventSource(endpoints=endpoints)

        return typing.cast(None, jsii.invoke(self, "putSelfManagedEventSource", [value]))

    @jsii.member(jsii_name="putSelfManagedKafkaEventSourceConfig")
    def put_self_managed_kafka_event_source_config(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        value = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(
            consumer_group_id=consumer_group_id,
            schema_registry_config=schema_registry_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManagedKafkaEventSourceConfig", [value]))

    @jsii.member(jsii_name="putSourceAccessConfiguration")
    def put_source_access_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ae94aa09c4b72eaadcb1c6349daa4979c24854571a11f8d4cb7c93e96e6cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceAccessConfiguration", [value]))

    @jsii.member(jsii_name="resetAmazonManagedKafkaEventSourceConfig")
    def reset_amazon_managed_kafka_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonManagedKafkaEventSourceConfig", []))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetBisectBatchOnFunctionError")
    def reset_bisect_batch_on_function_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBisectBatchOnFunctionError", []))

    @jsii.member(jsii_name="resetDestinationConfig")
    def reset_destination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationConfig", []))

    @jsii.member(jsii_name="resetDocumentDbEventSourceConfig")
    def reset_document_db_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentDbEventSourceConfig", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventSourceArn")
    def reset_event_source_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventSourceArn", []))

    @jsii.member(jsii_name="resetFilterCriteria")
    def reset_filter_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCriteria", []))

    @jsii.member(jsii_name="resetFunctionResponseTypes")
    def reset_function_response_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionResponseTypes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetMaximumBatchingWindowInSeconds")
    def reset_maximum_batching_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBatchingWindowInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRecordAgeInSeconds")
    def reset_maximum_record_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRecordAgeInSeconds", []))

    @jsii.member(jsii_name="resetMaximumRetryAttempts")
    def reset_maximum_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryAttempts", []))

    @jsii.member(jsii_name="resetMetricsConfig")
    def reset_metrics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsConfig", []))

    @jsii.member(jsii_name="resetParallelizationFactor")
    def reset_parallelization_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelizationFactor", []))

    @jsii.member(jsii_name="resetProvisionedPollerConfig")
    def reset_provisioned_poller_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedPollerConfig", []))

    @jsii.member(jsii_name="resetQueues")
    def reset_queues(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueues", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScalingConfig")
    def reset_scaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfig", []))

    @jsii.member(jsii_name="resetSelfManagedEventSource")
    def reset_self_managed_event_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedEventSource", []))

    @jsii.member(jsii_name="resetSelfManagedKafkaEventSourceConfig")
    def reset_self_managed_kafka_event_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagedKafkaEventSourceConfig", []))

    @jsii.member(jsii_name="resetSourceAccessConfiguration")
    def reset_source_access_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceAccessConfiguration", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetStartingPositionTimestamp")
    def reset_starting_position_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionTimestamp", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetTumblingWindowInSeconds")
    def reset_tumbling_window_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTumblingWindowInSeconds", []))

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
    @jsii.member(jsii_name="amazonManagedKafkaEventSourceConfig")
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference", jsii.get(self, "amazonManagedKafkaEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(
        self,
    ) -> "LambdaEventSourceMappingDestinationConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingDestinationConfigOutputReference", jsii.get(self, "destinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="documentDbEventSourceConfig")
    def document_db_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference", jsii.get(self, "documentDbEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteria")
    def filter_criteria(
        self,
    ) -> "LambdaEventSourceMappingFilterCriteriaOutputReference":
        return typing.cast("LambdaEventSourceMappingFilterCriteriaOutputReference", jsii.get(self, "filterCriteria"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="lastModified")
    def last_modified(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModified"))

    @builtins.property
    @jsii.member(jsii_name="lastProcessingResult")
    def last_processing_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastProcessingResult"))

    @builtins.property
    @jsii.member(jsii_name="metricsConfig")
    def metrics_config(self) -> "LambdaEventSourceMappingMetricsConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingMetricsConfigOutputReference", jsii.get(self, "metricsConfig"))

    @builtins.property
    @jsii.member(jsii_name="provisionedPollerConfig")
    def provisioned_poller_config(
        self,
    ) -> "LambdaEventSourceMappingProvisionedPollerConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingProvisionedPollerConfigOutputReference", jsii.get(self, "provisionedPollerConfig"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(self) -> "LambdaEventSourceMappingScalingConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingScalingConfigOutputReference", jsii.get(self, "scalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedEventSource")
    def self_managed_event_source(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedEventSourceOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedEventSourceOutputReference", jsii.get(self, "selfManagedEventSource"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaEventSourceConfig")
    def self_managed_kafka_event_source_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference", jsii.get(self, "selfManagedKafkaEventSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccessConfiguration")
    def source_access_configuration(
        self,
    ) -> "LambdaEventSourceMappingSourceAccessConfigurationList":
        return typing.cast("LambdaEventSourceMappingSourceAccessConfigurationList", jsii.get(self, "sourceAccessConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateTransitionReason")
    def state_transition_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateTransitionReason"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="amazonManagedKafkaEventSourceConfigInput")
    def amazon_managed_kafka_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig"], jsii.get(self, "amazonManagedKafkaEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionErrorInput")
    def bisect_batch_on_function_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bisectBatchOnFunctionErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfigInput")
    def destination_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfig"], jsii.get(self, "destinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="documentDbEventSourceConfigInput")
    def document_db_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"], jsii.get(self, "documentDbEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceArnInput")
    def event_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCriteriaInput")
    def filter_criteria_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingFilterCriteria"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingFilterCriteria"], jsii.get(self, "filterCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="functionResponseTypesInput")
    def function_response_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "functionResponseTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

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
    @jsii.member(jsii_name="metricsConfigInput")
    def metrics_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingMetricsConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingMetricsConfig"], jsii.get(self, "metricsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactorInput")
    def parallelization_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelizationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedPollerConfigInput")
    def provisioned_poller_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"], jsii.get(self, "provisionedPollerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="queuesInput")
    def queues_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queuesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigInput")
    def scaling_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingScalingConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingScalingConfig"], jsii.get(self, "scalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedEventSourceInput")
    def self_managed_event_source_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"], jsii.get(self, "selfManagedEventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagedKafkaEventSourceConfigInput")
    def self_managed_kafka_event_source_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"], jsii.get(self, "selfManagedKafkaEventSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAccessConfigurationInput")
    def source_access_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]], jsii.get(self, "sourceAccessConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestampInput")
    def starting_position_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionTimestampInput"))

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
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="tumblingWindowInSecondsInput")
    def tumbling_window_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tumblingWindowInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec953d7f7e9362fc36d0c7f04b35797659bb2fdab959e52bcd556273c8947c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionError")
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bisectBatchOnFunctionError"))

    @bisect_batch_on_function_error.setter
    def bisect_batch_on_function_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18c36c12c4b00cc3845460481b9870f5e4ee1767358163f5ed8c345986ae69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bisectBatchOnFunctionError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd82623952d72eba23116dcfd6b06b4a38e2bd0404cb8f9e3e4784f5ad386b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventSourceArn")
    def event_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSourceArn"))

    @event_source_arn.setter
    def event_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176b20eee35e9e2ba68c2fa2be59145dcbb8d94ea646398e37bf0ec0d078b180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1c0f85e3038f9fa349a9a6af803c18b97324e0be12ddc03501f0b818ae4b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionResponseTypes")
    def function_response_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "functionResponseTypes"))

    @function_response_types.setter
    def function_response_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93810df7fa745971eac1f425bc1ab87b9e4078252ee525643063b761ec4eb5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionResponseTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31ccea0308a0b13a268fa9b17926a5f2cb135ba99906d47275d7fe90429aa5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2062126ce46c77d5b4990525b61e6e1a3de6a9bebb5ecac84fcc4803a9114a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBatchingWindowInSeconds"))

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96ac0ca74998f24fcd7230d19a3c48eca2b1d28285ea98ba16e3ea8b9e960be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBatchingWindowInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRecordAgeInSeconds"))

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434fdc4f5aa9af36f58b892b01eb12f5d4c4b26d0e2bf42315b6938326035c82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRecordAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryAttempts"))

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bde15cbb63d14aef01063de9cc47dd14f53321b10ca71f0410d827d7bb8eeb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelizationFactor"))

    @parallelization_factor.setter
    def parallelization_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddb5ba4f1bc732faa0759478d7b1a122649b6b7f89a36e3388486d1994e8b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelizationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queues")
    def queues(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queues"))

    @queues.setter
    def queues(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752c58e45cf783de49edc16ae4b29a1d5e69f230695a17092b896ee6bc7f6334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceceacebc1f07de2a5ea778f5fc1c0f9cabe1b61870bb8267ee14683facd4fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cad8d58c86b44dcdff9688d1a26bf09dfecddab6fb0600d880c88ecd9de540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingPositionTimestamp")
    def starting_position_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPositionTimestamp"))

    @starting_position_timestamp.setter
    def starting_position_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbb05d78af2407e8a2d162f87794f46be804925ce893effa015481115d9692c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPositionTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b04ee4d8b5ba3f98a768b1705471353527502156baca4244b799cfce22b3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe542f7a42dadb91b9de527a2d2d4ecf0acec87458e370741754bd6322927b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7419fb9dcae8c9c5d65a18840a7f81f5437ca2e01426c27685835aef27da2e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tumblingWindowInSeconds")
    def tumbling_window_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tumblingWindowInSeconds"))

    @tumbling_window_in_seconds.setter
    def tumbling_window_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d5f2dff8e03a3e1114b97ce3b03179134469da4d8f19f0dfc40d976a0bc67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tumblingWindowInSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_group_id": "consumerGroupId",
        "schema_registry_config": "schemaRegistryConfig",
    },
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig:
    def __init__(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        if isinstance(schema_registry_config, dict):
            schema_registry_config = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig(**schema_registry_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cfad2d903a33e792f280a50ccddb827105d6c62b6a26cff4b2b5a4f9fbc6336)
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument schema_registry_config", value=schema_registry_config, expected_type=type_hints["schema_registry_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if schema_registry_config is not None:
            self._values["schema_registry_config"] = schema_registry_config

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        '''schema_registry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        result = self._values.get("schema_registry_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43835249eefdbdabe02486bbd9d0b4f6484e95708f89f4896d06ffe90ff78cb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaRegistryConfig")
    def put_schema_registry_config(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        value = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig(
            access_config=access_config,
            event_record_format=event_record_format,
            schema_registry_uri=schema_registry_uri,
            schema_validation_config=schema_validation_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaRegistryConfig", [value]))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetSchemaRegistryConfig")
    def reset_schema_registry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryConfig", []))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfig")
    def schema_registry_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference", jsii.get(self, "schemaRegistryConfig"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfigInput")
    def schema_registry_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig"], jsii.get(self, "schemaRegistryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d2d130b4a7381b524234880d9e24d75e53c2776fe3a51f0338239fbb7e6fb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d45e9b56a32ce3c8d063cb6caec75b1174491be2f030ac05589446a74a8f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "event_record_format": "eventRecordFormat",
        "schema_registry_uri": "schemaRegistryUri",
        "schema_validation_config": "schemaValidationConfig",
    },
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50a0f247dd107d16bc8afca508397e783e5343a05ba80e600469e26df66a285)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument event_record_format", value=event_record_format, expected_type=type_hints["event_record_format"])
            check_type(argname="argument schema_registry_uri", value=schema_registry_uri, expected_type=type_hints["schema_registry_uri"])
            check_type(argname="argument schema_validation_config", value=schema_validation_config, expected_type=type_hints["schema_validation_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_config is not None:
            self._values["access_config"] = access_config
        if event_record_format is not None:
            self._values["event_record_format"] = event_record_format
        if schema_registry_uri is not None:
            self._values["schema_registry_uri"] = schema_registry_uri
        if schema_validation_config is not None:
            self._values["schema_validation_config"] = schema_validation_config

    @builtins.property
    def access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]], result)

    @builtins.property
    def event_record_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.'''
        result = self._values.get("event_record_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.'''
        result = self._values.get("schema_registry_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_validation_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        '''schema_validation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        result = self._values.get("schema_validation_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4753c99082471d4580ba1a7ffd29e962b76522f3a3eeddb559160e03a3b0a6cb)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__360750aa27956070f01c93146485ad42b517eeb040d701edb7d46214ba284188)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60451109141c59dbbd44221fa2f2920c8126b7bb4397474a6c7b8513dbaa6989)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c111bcc39c77be040c849d176b23040dddbfc08f82cbdcdecdb993fe79591c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e6f75cfa1969704a7e47d46540764abdafaad798e7d2142345c183b3b5c369f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37750f881c58e34d5680ced2b17f5d61239d623d46568e41d570521a7b6713d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baaf6bd8c31e92a7cbd4da795d49d376aedbce332d6daa818910e4431ab28fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__398cee90aa3a63768524a35db5a2dfc19ed310009c27e64b67c8915a302e8ace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927025ac75608d88da9b68db1cd59749c204d2e62d69fccf62546f73f8e483ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34914c52d047216978858472ad91831c25134f6bc26b487b4f6a1d9ff762312b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a3fc4d3f23eb0b8409f76646e79bf868b2e50a087e9a0e9c05fa40dd17a3af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a4450b06a350545e5c2e1e8995e93ee6e5c23193bf735b0b6cfcfaa3a43f283)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2368570bcfb34ad03b81d0e4917862f08b0c72fb2f490b9da2b72b6a45d06f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putSchemaValidationConfig")
    def put_schema_validation_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47dc24040ba37c0d46a5eb672b1e39043ce04ab26212dfe2391cb9118aacf406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaValidationConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetEventRecordFormat")
    def reset_event_record_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventRecordFormat", []))

    @jsii.member(jsii_name="resetSchemaRegistryUri")
    def reset_schema_registry_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryUri", []))

    @jsii.member(jsii_name="resetSchemaValidationConfig")
    def reset_schema_validation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaValidationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList:
        return typing.cast(LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfig")
    def schema_validation_config(
        self,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList":
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList", jsii.get(self, "schemaValidationConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormatInput")
    def event_record_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventRecordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUriInput")
    def schema_registry_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaRegistryUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfigInput")
    def schema_validation_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], jsii.get(self, "schemaValidationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormat")
    def event_record_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventRecordFormat"))

    @event_record_format.setter
    def event_record_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637df446f2054bd0cdacded2df3558e8610a46209ed93cf01f9c16f52c7eeb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventRecordFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUri")
    def schema_registry_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaRegistryUri"))

    @schema_registry_uri.setter
    def schema_registry_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04cb34ad0535f23465df705c239eff9b34e74a3e2cb6f4e639626e0dbd205169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaRegistryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1638534d36b009e2b4d52c9710a61ad41b919f8384b800dea3b4bfadc9b6c842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute"},
)
class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig:
    def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
        '''
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b40dc37628cbfe9191a5300b25b8c99410fcb3de162f91608f73d6499dae8a)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute is not None:
            self._values["attribute"] = attribute

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4e40be519b4e215217222001a3cd9afd73b1487cc3645623df46483896dee0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e7aa21b36c86f575f98ab15ed31ea383a7884406a6af88f3a9c729b3c5dad8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dcb38f35a4d71ddb7d282ef263bc9b8b8a7d7b22086d0eb3b9980e86480d4a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0761871fee1f574dd303b47aa28905445d480522575de2a6aab7a07ddcd3b80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a03c32a585223654eb6db64307f6952f6da9e8c8a5491b73f98fc389c1c21b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e374ba5d5061e821d7364dc6f9d49c3a06004b66a07b01a24eac174c06bf2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__115ae7ebf2961b88636110d16b49dd6a4ea785b684cfd8552c8ac018ba16eda1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6c58891a3f2039c02df8220d8fe7ea7c0942a9229a701b424803dbb2635da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2f54aa3f01286a4f0916babb25cd093f090e5f1d6bb360d10488a0dd0b2862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_name": "functionName",
        "amazon_managed_kafka_event_source_config": "amazonManagedKafkaEventSourceConfig",
        "batch_size": "batchSize",
        "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
        "destination_config": "destinationConfig",
        "document_db_event_source_config": "documentDbEventSourceConfig",
        "enabled": "enabled",
        "event_source_arn": "eventSourceArn",
        "filter_criteria": "filterCriteria",
        "function_response_types": "functionResponseTypes",
        "id": "id",
        "kms_key_arn": "kmsKeyArn",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "metrics_config": "metricsConfig",
        "parallelization_factor": "parallelizationFactor",
        "provisioned_poller_config": "provisionedPollerConfig",
        "queues": "queues",
        "region": "region",
        "scaling_config": "scalingConfig",
        "self_managed_event_source": "selfManagedEventSource",
        "self_managed_kafka_event_source_config": "selfManagedKafkaEventSourceConfig",
        "source_access_configuration": "sourceAccessConfiguration",
        "starting_position": "startingPosition",
        "starting_position_timestamp": "startingPositionTimestamp",
        "tags": "tags",
        "tags_all": "tagsAll",
        "topics": "topics",
        "tumbling_window_in_seconds": "tumblingWindowInSeconds",
    },
)
class LambdaEventSourceMappingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        function_name: builtins.str,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        document_db_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingDocumentDbEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union["LambdaEventSourceMappingFilterCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        metrics_config: typing.Optional[typing.Union["LambdaEventSourceMappingMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        provisioned_poller_config: typing.Optional[typing.Union["LambdaEventSourceMappingProvisionedPollerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["LambdaEventSourceMappingScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_event_source: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSourceAccessConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.
        :param amazon_managed_kafka_event_source_config: amazon_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.
        :param bisect_batch_on_function_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        :param document_db_event_source_config: document_db_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#document_db_event_source_config LambdaEventSourceMapping#document_db_event_source_config}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.
        :param event_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.
        :param filter_criteria: filter_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        :param function_response_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#id LambdaEventSourceMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#kms_key_arn LambdaEventSourceMapping#kms_key_arn}.
        :param maximum_batching_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.
        :param maximum_record_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.
        :param maximum_retry_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#metrics_config LambdaEventSourceMapping#metrics_config}
        :param parallelization_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.
        :param provisioned_poller_config: provisioned_poller_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#provisioned_poller_config LambdaEventSourceMapping#provisioned_poller_config}
        :param queues: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#region LambdaEventSourceMapping#region}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#scaling_config LambdaEventSourceMapping#scaling_config}
        :param self_managed_event_source: self_managed_event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        :param self_managed_kafka_event_source_config: self_managed_kafka_event_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        :param source_access_configuration: source_access_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.
        :param starting_position_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tags LambdaEventSourceMapping#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tags_all LambdaEventSourceMapping#tags_all}.
        :param topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.
        :param tumbling_window_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(amazon_managed_kafka_event_source_config, dict):
            amazon_managed_kafka_event_source_config = LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig(**amazon_managed_kafka_event_source_config)
        if isinstance(destination_config, dict):
            destination_config = LambdaEventSourceMappingDestinationConfig(**destination_config)
        if isinstance(document_db_event_source_config, dict):
            document_db_event_source_config = LambdaEventSourceMappingDocumentDbEventSourceConfig(**document_db_event_source_config)
        if isinstance(filter_criteria, dict):
            filter_criteria = LambdaEventSourceMappingFilterCriteria(**filter_criteria)
        if isinstance(metrics_config, dict):
            metrics_config = LambdaEventSourceMappingMetricsConfig(**metrics_config)
        if isinstance(provisioned_poller_config, dict):
            provisioned_poller_config = LambdaEventSourceMappingProvisionedPollerConfig(**provisioned_poller_config)
        if isinstance(scaling_config, dict):
            scaling_config = LambdaEventSourceMappingScalingConfig(**scaling_config)
        if isinstance(self_managed_event_source, dict):
            self_managed_event_source = LambdaEventSourceMappingSelfManagedEventSource(**self_managed_event_source)
        if isinstance(self_managed_kafka_event_source_config, dict):
            self_managed_kafka_event_source_config = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(**self_managed_kafka_event_source_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbbc460681fc2ad4150fe1062902897043c3521193786662018992d3176dad4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument amazon_managed_kafka_event_source_config", value=amazon_managed_kafka_event_source_config, expected_type=type_hints["amazon_managed_kafka_event_source_config"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument document_db_event_source_config", value=document_db_event_source_config, expected_type=type_hints["document_db_event_source_config"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_source_arn", value=event_source_arn, expected_type=type_hints["event_source_arn"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument function_response_types", value=function_response_types, expected_type=type_hints["function_response_types"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument provisioned_poller_config", value=provisioned_poller_config, expected_type=type_hints["provisioned_poller_config"])
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scaling_config", value=scaling_config, expected_type=type_hints["scaling_config"])
            check_type(argname="argument self_managed_event_source", value=self_managed_event_source, expected_type=type_hints["self_managed_event_source"])
            check_type(argname="argument self_managed_kafka_event_source_config", value=self_managed_kafka_event_source_config, expected_type=type_hints["self_managed_kafka_event_source_config"])
            check_type(argname="argument source_access_configuration", value=source_access_configuration, expected_type=type_hints["source_access_configuration"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument tumbling_window_in_seconds", value=tumbling_window_in_seconds, expected_type=type_hints["tumbling_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
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
        if amazon_managed_kafka_event_source_config is not None:
            self._values["amazon_managed_kafka_event_source_config"] = amazon_managed_kafka_event_source_config
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_function_error is not None:
            self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
        if destination_config is not None:
            self._values["destination_config"] = destination_config
        if document_db_event_source_config is not None:
            self._values["document_db_event_source_config"] = document_db_event_source_config
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_source_arn is not None:
            self._values["event_source_arn"] = event_source_arn
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if function_response_types is not None:
            self._values["function_response_types"] = function_response_types
        if id is not None:
            self._values["id"] = id
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if provisioned_poller_config is not None:
            self._values["provisioned_poller_config"] = provisioned_poller_config
        if queues is not None:
            self._values["queues"] = queues
        if region is not None:
            self._values["region"] = region
        if scaling_config is not None:
            self._values["scaling_config"] = scaling_config
        if self_managed_event_source is not None:
            self._values["self_managed_event_source"] = self_managed_event_source
        if self_managed_kafka_event_source_config is not None:
            self._values["self_managed_kafka_event_source_config"] = self_managed_kafka_event_source_config
        if source_access_configuration is not None:
            self._values["source_access_configuration"] = source_access_configuration
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if topics is not None:
            self._values["topics"] = topics
        if tumbling_window_in_seconds is not None:
            self._values["tumbling_window_in_seconds"] = tumbling_window_in_seconds

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
    def function_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#function_name LambdaEventSourceMapping#function_name}.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig]:
        '''amazon_managed_kafka_event_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#amazon_managed_kafka_event_source_config LambdaEventSourceMapping#amazon_managed_kafka_event_source_config}
        '''
        result = self._values.get("amazon_managed_kafka_event_source_config")
        return typing.cast(typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig], result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#batch_size LambdaEventSourceMapping#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#bisect_batch_on_function_error LambdaEventSourceMapping#bisect_batch_on_function_error}.'''
        result = self._values.get("bisect_batch_on_function_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfig"]:
        '''destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#destination_config LambdaEventSourceMapping#destination_config}
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfig"], result)

    @builtins.property
    def document_db_event_source_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"]:
        '''document_db_event_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#document_db_event_source_config LambdaEventSourceMapping#document_db_event_source_config}
        '''
        result = self._values.get("document_db_event_source_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDocumentDbEventSourceConfig"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#enabled LambdaEventSourceMapping#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_source_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_source_arn LambdaEventSourceMapping#event_source_arn}.'''
        result = self._values.get("event_source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingFilterCriteria"]:
        '''filter_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#filter_criteria LambdaEventSourceMapping#filter_criteria}
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional["LambdaEventSourceMappingFilterCriteria"], result)

    @builtins.property
    def function_response_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#function_response_types LambdaEventSourceMapping#function_response_types}.'''
        result = self._values.get("function_response_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#id LambdaEventSourceMapping#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#kms_key_arn LambdaEventSourceMapping#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_batching_window_in_seconds LambdaEventSourceMapping#maximum_batching_window_in_seconds}.'''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_record_age_in_seconds LambdaEventSourceMapping#maximum_record_age_in_seconds}.'''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_retry_attempts LambdaEventSourceMapping#maximum_retry_attempts}.'''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingMetricsConfig"]:
        '''metrics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#metrics_config LambdaEventSourceMapping#metrics_config}
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingMetricsConfig"], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#parallelization_factor LambdaEventSourceMapping#parallelization_factor}.'''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_poller_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"]:
        '''provisioned_poller_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#provisioned_poller_config LambdaEventSourceMapping#provisioned_poller_config}
        '''
        result = self._values.get("provisioned_poller_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingProvisionedPollerConfig"], result)

    @builtins.property
    def queues(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#queues LambdaEventSourceMapping#queues}.'''
        result = self._values.get("queues")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#region LambdaEventSourceMapping#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingScalingConfig"]:
        '''scaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#scaling_config LambdaEventSourceMapping#scaling_config}
        '''
        result = self._values.get("scaling_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingScalingConfig"], result)

    @builtins.property
    def self_managed_event_source(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"]:
        '''self_managed_event_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#self_managed_event_source LambdaEventSourceMapping#self_managed_event_source}
        '''
        result = self._values.get("self_managed_event_source")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedEventSource"], result)

    @builtins.property
    def self_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"]:
        '''self_managed_kafka_event_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#self_managed_kafka_event_source_config LambdaEventSourceMapping#self_managed_kafka_event_source_config}
        '''
        result = self._values.get("self_managed_kafka_event_source_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig"], result)

    @builtins.property
    def source_access_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]]:
        '''source_access_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#source_access_configuration LambdaEventSourceMapping#source_access_configuration}
        '''
        result = self._values.get("source_access_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSourceAccessConfiguration"]]], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#starting_position LambdaEventSourceMapping#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#starting_position_timestamp LambdaEventSourceMapping#starting_position_timestamp}.'''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tags LambdaEventSourceMapping#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tags_all LambdaEventSourceMapping#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#topics LambdaEventSourceMapping#topics}.'''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tumbling_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#tumbling_window_in_seconds LambdaEventSourceMapping#tumbling_window_in_seconds}.'''
        result = self._values.get("tumbling_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"on_failure": "onFailure"},
)
class LambdaEventSourceMappingDestinationConfig:
    def __init__(
        self,
        *,
        on_failure: typing.Optional[typing.Union["LambdaEventSourceMappingDestinationConfigOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: on_failure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        if isinstance(on_failure, dict):
            on_failure = LambdaEventSourceMappingDestinationConfigOnFailure(**on_failure)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028a90c33bb0c45db5f28ea8edcf86f291ffabf179170f25cbdb5dcd4fb1fb44)
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_failure is not None:
            self._values["on_failure"] = on_failure

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingDestinationConfigOnFailure"]:
        '''on_failure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#on_failure LambdaEventSourceMapping#on_failure}
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["LambdaEventSourceMappingDestinationConfigOnFailure"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOnFailure",
    jsii_struct_bases=[],
    name_mapping={"destination_arn": "destinationArn"},
)
class LambdaEventSourceMappingDestinationConfigOnFailure:
    def __init__(self, *, destination_arn: builtins.str) -> None:
        '''
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8314496e4eb0aa4d89864dfcbc3d7046bc9d4faaafb8fe3a8002d858f4817377)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
        }

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDestinationConfigOnFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingDestinationConfigOnFailureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOnFailureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cda9e23ed43ded982d0d842c4928bf5070cd21007adcd6f52c910304a341de2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d1ce955038c2e1a764ba36ba0e34b01addf4cf2804fd695e66d1994f957cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e3b743ea68d2a4a70849d57efaef67e2bf6f4566a2ece1ec20c26c9000ffda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4939f4e61cf10530de54603848d00dab8e112ff5c2e1bdde93c3a04edaa0627b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOnFailure")
    def put_on_failure(self, *, destination_arn: builtins.str) -> None:
        '''
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#destination_arn LambdaEventSourceMapping#destination_arn}.
        '''
        value = LambdaEventSourceMappingDestinationConfigOnFailure(
            destination_arn=destination_arn
        )

        return typing.cast(None, jsii.invoke(self, "putOnFailure", [value]))

    @jsii.member(jsii_name="resetOnFailure")
    def reset_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnFailure", []))

    @builtins.property
    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
    ) -> LambdaEventSourceMappingDestinationConfigOnFailureOutputReference:
        return typing.cast(LambdaEventSourceMappingDestinationConfigOnFailureOutputReference, jsii.get(self, "onFailure"))

    @builtins.property
    @jsii.member(jsii_name="onFailureInput")
    def on_failure_input(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure], jsii.get(self, "onFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDestinationConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd3a35cf87b5e6fb8e5fe706dae1f6a0d38f958ad1ac3815399abd360e9f728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDocumentDbEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "collection_name": "collectionName",
        "full_document": "fullDocument",
    },
)
class LambdaEventSourceMappingDocumentDbEventSourceConfig:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        collection_name: typing.Optional[builtins.str] = None,
        full_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#database_name LambdaEventSourceMapping#database_name}.
        :param collection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#collection_name LambdaEventSourceMapping#collection_name}.
        :param full_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#full_document LambdaEventSourceMapping#full_document}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba374d3afd5910dfe4e5ccdfcea94ce57e4738c544ac2d885dc3a58657ea1632)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
            check_type(argname="argument full_document", value=full_document, expected_type=type_hints["full_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
        }
        if collection_name is not None:
            self._values["collection_name"] = collection_name
        if full_document is not None:
            self._values["full_document"] = full_document

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#database_name LambdaEventSourceMapping#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#collection_name LambdaEventSourceMapping#collection_name}.'''
        result = self._values.get("collection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def full_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#full_document LambdaEventSourceMapping#full_document}.'''
        result = self._values.get("full_document")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingDocumentDbEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55534adbe3eaf1caaec14b372bae89af66afc5f1a530634e64538b9c75d366da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCollectionName")
    def reset_collection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionName", []))

    @jsii.member(jsii_name="resetFullDocument")
    def reset_full_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullDocument", []))

    @builtins.property
    @jsii.member(jsii_name="collectionNameInput")
    def collection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fullDocumentInput")
    def full_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionName")
    def collection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionName"))

    @collection_name.setter
    def collection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06a3c63200d1f14bc330a1c31970052c9da4da6abcb1497425d344913c654f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d477f1d41b62b5a0253dac7d268c59349d60e87ce4c4b258191e9e5480ba4fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullDocument")
    def full_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullDocument"))

    @full_document.setter
    def full_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97740642bd95c63c78f313dedc12a606374b263c095ce46b7664a59eaef34fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d63f26cc8a9f37ea46e13116ad8289cb959b6b450e6cd15e80aac66223c4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteria",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class LambdaEventSourceMappingFilterCriteria:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingFilterCriteriaFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3940c994dd7112704c875917bf796efa24d0fa30169aad09a714041c0d230ddf)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingFilterCriteriaFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#filter LambdaEventSourceMapping#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingFilterCriteriaFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingFilterCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilter",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class LambdaEventSourceMappingFilterCriteriaFilter:
    def __init__(self, *, pattern: typing.Optional[builtins.str] = None) -> None:
        '''
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#pattern LambdaEventSourceMapping#pattern}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443eecbbf79c0e4d45522fa23d20b39de954d3413005398876010b981dfccbe7)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pattern is not None:
            self._values["pattern"] = pattern

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#pattern LambdaEventSourceMapping#pattern}.'''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingFilterCriteriaFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingFilterCriteriaFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ebd6317127329a831a9279d9a2855fb113d54d32f91cae9d63615d768305fb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingFilterCriteriaFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600ff0e48cd3ee095053f29d65b99856d5a90a2e5e7c5ea2b28666ca66991b98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingFilterCriteriaFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7f3400ba01e196a9f48591ad17ac1fc2d43301572501dde4e658f3e104c03a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fca5c654b346c58b7589f9c6a065d8b9d36c37f354af6321ee298a8273b36980)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7fc46a265e4468c1a87d6d0dd09f1359063cf7a41e49dcfb7815a3cccb514a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ca5276ed784bc631ee025fc1cc2d799b1f4ae56279306a27448e2c9eb587bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingFilterCriteriaFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__093afaef6a831f420abefc9fc905a9e7b00e120cc114d84c00359cd9c6857354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1085abf87c7b461a8c7b4e62e5423cd9f2e831bf4c2122f7ff3b56a0ed0b8925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b32f849878158d0007dbf1046800f0daef2b26c8b2425449329819fa07edfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingFilterCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingFilterCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df129506a83ada76f0e182526a560c18be580c09bbe630dfe1d081d701ed857c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b22e1a650687225f2c1e1acf20810b1bfe9a2271f649f05bf4f442b0863a10b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> LambdaEventSourceMappingFilterCriteriaFilterList:
        return typing.cast(LambdaEventSourceMappingFilterCriteriaFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingFilterCriteria]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingFilterCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingFilterCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45214e67ed278410d0e8b4eb11f8b0aa57f4969c0cf6053acd24ac12f1aeb1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingMetricsConfig",
    jsii_struct_bases=[],
    name_mapping={"metrics": "metrics"},
)
class LambdaEventSourceMappingMetricsConfig:
    def __init__(self, *, metrics: typing.Sequence[builtins.str]) -> None:
        '''
        :param metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#metrics LambdaEventSourceMapping#metrics}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cb4769f3dfc23745c487e7d98833c3dbfae44625b9f272d6209249462f1da8)
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metrics": metrics,
        }

    @builtins.property
    def metrics(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#metrics LambdaEventSourceMapping#metrics}.'''
        result = self._values.get("metrics")
        assert result is not None, "Required property 'metrics' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingMetricsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingMetricsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingMetricsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d33ee652c759fc7f6bb033c4a578ee48df52e23ad027ce1533cf01fc60ca2c7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="metricsInput")
    def metrics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metricsInput"))

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metrics"))

    @metrics.setter
    def metrics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5d7e71d5d54d6358d2f4a0068c7f66f9a8779e8f30a4114962c1b0731c26e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metrics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingMetricsConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingMetricsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingMetricsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be99336559e3eb3c7499e3711922a3074cd4d70f7cf4248276232d83b6ad378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingProvisionedPollerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_pollers": "maximumPollers",
        "minimum_pollers": "minimumPollers",
        "poller_group_name": "pollerGroupName",
    },
)
class LambdaEventSourceMappingProvisionedPollerConfig:
    def __init__(
        self,
        *,
        maximum_pollers: typing.Optional[jsii.Number] = None,
        minimum_pollers: typing.Optional[jsii.Number] = None,
        poller_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_pollers LambdaEventSourceMapping#maximum_pollers}.
        :param minimum_pollers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#minimum_pollers LambdaEventSourceMapping#minimum_pollers}.
        :param poller_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#poller_group_name LambdaEventSourceMapping#poller_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3245bbe0713114d2abe0831b29d2acfeec5c2757da4ec8bfa4a2423203a9f6)
            check_type(argname="argument maximum_pollers", value=maximum_pollers, expected_type=type_hints["maximum_pollers"])
            check_type(argname="argument minimum_pollers", value=minimum_pollers, expected_type=type_hints["minimum_pollers"])
            check_type(argname="argument poller_group_name", value=poller_group_name, expected_type=type_hints["poller_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_pollers is not None:
            self._values["maximum_pollers"] = maximum_pollers
        if minimum_pollers is not None:
            self._values["minimum_pollers"] = minimum_pollers
        if poller_group_name is not None:
            self._values["poller_group_name"] = poller_group_name

    @builtins.property
    def maximum_pollers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_pollers LambdaEventSourceMapping#maximum_pollers}.'''
        result = self._values.get("maximum_pollers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_pollers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#minimum_pollers LambdaEventSourceMapping#minimum_pollers}.'''
        result = self._values.get("minimum_pollers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def poller_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#poller_group_name LambdaEventSourceMapping#poller_group_name}.'''
        result = self._values.get("poller_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingProvisionedPollerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingProvisionedPollerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingProvisionedPollerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__918744ae0ffa0cde71e001aea1fded591292f2f345ccc4a64c09072b935194db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximumPollers")
    def reset_maximum_pollers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumPollers", []))

    @jsii.member(jsii_name="resetMinimumPollers")
    def reset_minimum_pollers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumPollers", []))

    @jsii.member(jsii_name="resetPollerGroupName")
    def reset_poller_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPollerGroupName", []))

    @builtins.property
    @jsii.member(jsii_name="maximumPollersInput")
    def maximum_pollers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumPollersInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumPollersInput")
    def minimum_pollers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumPollersInput"))

    @builtins.property
    @jsii.member(jsii_name="pollerGroupNameInput")
    def poller_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pollerGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumPollers")
    def maximum_pollers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumPollers"))

    @maximum_pollers.setter
    def maximum_pollers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11e6fd6c28d0de63e024b685b745007253b5819e3c8cba688fa8c435be1bacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumPollers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumPollers")
    def minimum_pollers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumPollers"))

    @minimum_pollers.setter
    def minimum_pollers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0cbc4eed4808b5b6c075d549b64fb1fc1035b8ccbdda88a0da01c72f2bdb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumPollers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pollerGroupName")
    def poller_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pollerGroupName"))

    @poller_group_name.setter
    def poller_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12b79c1c9b70672111e9a4b80a4b3c469a4532910e0675b6674cb50a605f25b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pollerGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe149d5b03f6236650ba51c4652ce07376a41cba2caf7069ecfbb1c0af23ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingScalingConfig",
    jsii_struct_bases=[],
    name_mapping={"maximum_concurrency": "maximumConcurrency"},
)
class LambdaEventSourceMappingScalingConfig:
    def __init__(
        self,
        *,
        maximum_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_concurrency LambdaEventSourceMapping#maximum_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d0c735f1f7de981baa2961e38be83fb1bd3149fadf94fc8eeff706b9bcefef)
            check_type(argname="argument maximum_concurrency", value=maximum_concurrency, expected_type=type_hints["maximum_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_concurrency is not None:
            self._values["maximum_concurrency"] = maximum_concurrency

    @builtins.property
    def maximum_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#maximum_concurrency LambdaEventSourceMapping#maximum_concurrency}.'''
        result = self._values.get("maximum_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingScalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingScalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingScalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b99bc1d243e123e4522d2558c03c29e180ae8936e4b69671365fd3f66ed5eae4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximumConcurrency")
    def reset_maximum_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="maximumConcurrencyInput")
    def maximum_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumConcurrency")
    def maximum_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumConcurrency"))

    @maximum_concurrency.setter
    def maximum_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a9988bf7a2b163833f4398f16d2a978b1a179197c6c31d235700850921af26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LambdaEventSourceMappingScalingConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingScalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingScalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c46d5d2cc611a63fd9196c40ab39d80e0cf7111f924d90c4cb4427d84b6e0cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedEventSource",
    jsii_struct_bases=[],
    name_mapping={"endpoints": "endpoints"},
)
class LambdaEventSourceMappingSelfManagedEventSource:
    def __init__(
        self,
        *,
        endpoints: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115d5f9219177d46395e59fd314e311ce074ff570d1fd2eb722a542a2fdeb92e)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints": endpoints,
        }

    @builtins.property
    def endpoints(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#endpoints LambdaEventSourceMapping#endpoints}.'''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedEventSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedEventSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedEventSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c057784b30b58adb3cfa0937252747d0d0620877c62d4588f921e04b8a83dcaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b24c12c3ee41860ad4399dca8064e0edd863a51f40316a885ebd4a372b69113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedEventSource]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedEventSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedEventSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844a1e4e6b8a6381015bbe44eca4b4f9210408149c1ab092d68010582e393856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_group_id": "consumerGroupId",
        "schema_registry_config": "schemaRegistryConfig",
    },
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig:
    def __init__(
        self,
        *,
        consumer_group_id: typing.Optional[builtins.str] = None,
        schema_registry_config: typing.Optional[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param consumer_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.
        :param schema_registry_config: schema_registry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        if isinstance(schema_registry_config, dict):
            schema_registry_config = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig(**schema_registry_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354656de54122e5130a67f3e5a18ba33a4ffac9193a47bdfeb0f75b7917e0c25)
            check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
            check_type(argname="argument schema_registry_config", value=schema_registry_config, expected_type=type_hints["schema_registry_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_group_id is not None:
            self._values["consumer_group_id"] = consumer_group_id
        if schema_registry_config is not None:
            self._values["schema_registry_config"] = schema_registry_config

    @builtins.property
    def consumer_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#consumer_group_id LambdaEventSourceMapping#consumer_group_id}.'''
        result = self._values.get("consumer_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_config(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        '''schema_registry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_config LambdaEventSourceMapping#schema_registry_config}
        '''
        result = self._values.get("schema_registry_config")
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__133121669affb2177227430d7587890d3bf15fdd74f9e2208abfa3a602a382b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaRegistryConfig")
    def put_schema_registry_config(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        value = LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig(
            access_config=access_config,
            event_record_format=event_record_format,
            schema_registry_uri=schema_registry_uri,
            schema_validation_config=schema_validation_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaRegistryConfig", [value]))

    @jsii.member(jsii_name="resetConsumerGroupId")
    def reset_consumer_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupId", []))

    @jsii.member(jsii_name="resetSchemaRegistryConfig")
    def reset_schema_registry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryConfig", []))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfig")
    def schema_registry_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference", jsii.get(self, "schemaRegistryConfig"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupIdInput")
    def consumer_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryConfigInput")
    def schema_registry_config_input(
        self,
    ) -> typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"]:
        return typing.cast(typing.Optional["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig"], jsii.get(self, "schemaRegistryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupId")
    def consumer_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupId"))

    @consumer_group_id.setter
    def consumer_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efff89c72c62d7e3e060565d5aae79ee4cac8c6f79900965239abc5b9d32320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f294a68e13ae18b0552e19c16c6e558f83e6e8c4919a02377da48cf56d2cd4c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "event_record_format": "eventRecordFormat",
        "schema_registry_uri": "schemaRegistryUri",
        "schema_validation_config": "schemaValidationConfig",
    },
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_record_format: typing.Optional[builtins.str] = None,
        schema_registry_uri: typing.Optional[builtins.str] = None,
        schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        :param event_record_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.
        :param schema_registry_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.
        :param schema_validation_config: schema_validation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ad875f10054d66b09061165ae971330fcd147eb252588ec168dd4979b5c33d)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument event_record_format", value=event_record_format, expected_type=type_hints["event_record_format"])
            check_type(argname="argument schema_registry_uri", value=schema_registry_uri, expected_type=type_hints["schema_registry_uri"])
            check_type(argname="argument schema_validation_config", value=schema_validation_config, expected_type=type_hints["schema_validation_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_config is not None:
            self._values["access_config"] = access_config
        if event_record_format is not None:
            self._values["event_record_format"] = event_record_format
        if schema_registry_uri is not None:
            self._values["schema_registry_uri"] = schema_registry_uri
        if schema_validation_config is not None:
            self._values["schema_validation_config"] = schema_validation_config

    @builtins.property
    def access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#access_config LambdaEventSourceMapping#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig"]]], result)

    @builtins.property
    def event_record_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#event_record_format LambdaEventSourceMapping#event_record_format}.'''
        result = self._values.get("event_record_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_registry_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_registry_uri LambdaEventSourceMapping#schema_registry_uri}.'''
        result = self._values.get("schema_registry_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_validation_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        '''schema_validation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#schema_validation_config LambdaEventSourceMapping#schema_validation_config}
        '''
        result = self._values.get("schema_validation_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc01c8a30315ec4009f8f15d5bd5b03741f4a2f93c7572b665460b4091677eb)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd1a0e4ee22e84e9ad8cc6a60bb0624f3ad2fb958e070a358a26e50c82349bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331cd2594fc9b6264370906a31e40e5113f8f30691709d42b64338e1fa141025)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4d170702fe86f6f8a2cf9817836abfccda6ec070aaf675636310fe96a9f088)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a716e5f863f7d86ba1804755948fe3a182a0c54bb84f18aba63c9bc7dbb1e4d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc12adcaa169c1729650a85226a1fb55ef0f05e15ca426532ff75f035a340bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5365157bfe7d85e196743262873616a7547238023d06c558ddcd0c5b7d27558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e8cdccc2d7574beaf3d5f1f388643e2527f7eba06d9217dfa7c14219966d991)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61549e94c286f55a78b1a6984c52f553aa28b373b7006de2357a4a303385fe1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6682a0786cfe0922180888b19dfe5f34af9a709df52ac5cef8b77acb0a8ef0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf619b7d30d946ef2fafb72cc39ef5bb906b6aae11e4fd4212be171b4371105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff712135f9cb640c44f9dbfe30471cb2d48bf4e5ae250356dfd8080704e219e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902d130efd24c47b320b355119c2caaa66aa4f17034e63627192a08d1f833b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putSchemaValidationConfig")
    def put_schema_validation_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237a49a219411a26fb15cc614c7b860920b25f91241754048e835fd8db6b51d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaValidationConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetEventRecordFormat")
    def reset_event_record_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventRecordFormat", []))

    @jsii.member(jsii_name="resetSchemaRegistryUri")
    def reset_schema_registry_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaRegistryUri", []))

    @jsii.member(jsii_name="resetSchemaValidationConfig")
    def reset_schema_validation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaValidationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList:
        return typing.cast(LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfig")
    def schema_validation_config(
        self,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList":
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList", jsii.get(self, "schemaValidationConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormatInput")
    def event_record_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventRecordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUriInput")
    def schema_registry_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaRegistryUriInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaValidationConfigInput")
    def schema_validation_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig"]]], jsii.get(self, "schemaValidationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventRecordFormat")
    def event_record_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventRecordFormat"))

    @event_record_format.setter
    def event_record_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3892a3e125df320043a765651b2c0a16aa3efee04d4e1ff948c2a373ad9890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventRecordFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaRegistryUri")
    def schema_registry_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaRegistryUri"))

    @schema_registry_uri.setter
    def schema_registry_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5794c789f06d1890c39e6a592b040a7674f134030c7b6447ede54d2d51f88619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaRegistryUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig]:
        return typing.cast(typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57d6c76eac2a79dc8c15ee51521ec338fe086783a699581d84ffa5b599c3216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    jsii_struct_bases=[],
    name_mapping={"attribute": "attribute"},
)
class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig:
    def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
        '''
        :param attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5526f99aa164d7aeb9f486f635238e574607507891c2a1c970ca1918e6e09a12)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute is not None:
            self._values["attribute"] = attribute

    @builtins.property
    def attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#attribute LambdaEventSourceMapping#attribute}.'''
        result = self._values.get("attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c71d51b12e37eb8c0c1aded9302a8139fafe2a7652ff56e490304ba8723193)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2668af891c8a205207d7622c7c51ff56097bbbfdb4baf5fee27835d5122867c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4de5600eabb07149bb5bdf771db99ecdaf8568522f4fceb7adb4ac345587444)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a4246555ced3d1051927e6da16e5d71d0eae065236b530a32b446dccbcb108)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f7e46172d1f3e8f54cac39e3e079fe47746e9cde5cc2f17bde3476367ea4279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5a6906e618ecfe93881c5d92342b67a4eb99feb36da26f72ec334f32da7a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14359e3e3ecb79f296e472f3865e7feb70ef25de9ccbbf0f8d8c8c0f6f14c4e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttribute")
    def reset_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttribute", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbdacd3cc16daec919e5e973fa533f8e836f66b488b14b71f91b8891c4a897e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a183eaf5b1ed544e84f1d31cb8aa167ef8bf9ca324b900713a43ba67b78091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "uri": "uri"},
)
class LambdaEventSourceMappingSourceAccessConfiguration:
    def __init__(self, *, type: builtins.str, uri: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692fe6b5a0772a18039296bca5c5aefdd93a8ede0e0673278320a39043661ffb)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "uri": uri,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#type LambdaEventSourceMapping#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lambda_event_source_mapping#uri LambdaEventSourceMapping#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaEventSourceMappingSourceAccessConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaEventSourceMappingSourceAccessConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1a4974fbaeb2376edfb79465454f892610fbd3eb5378753d0b0bc20df176f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LambdaEventSourceMappingSourceAccessConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8602953ed2e8ee9add8263d91ebaecbd6b223eae47257034b108f789eae0900)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LambdaEventSourceMappingSourceAccessConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e14ae2cd637db402a9bba6dfda094122e25bc6b8baf087f21588ea5e692b805)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ac78ec485f68048deb02c7dfba04caae1f664d1363eb6727fe2c09e22844ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8af425498206707b40e2e5cfec85c90314aa5113ed0789bb8f78b6b9da904c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6cfe340651e936f4f606c4e7c1ca06fbf78244d4c108761a4a9cb3ff510036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LambdaEventSourceMappingSourceAccessConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lambdaEventSourceMapping.LambdaEventSourceMappingSourceAccessConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9af6958c1d50e789b22c006627653a5846874b53203203043bd08cad33d55256)
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
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b1b2eef46cba6539106742caeecd47d2fbecbbf3ee5d97e2daaa46932c662d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca914e27e3fb4a05e201739a8449c679e0da41e32bac601ff3949a4956d47797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd51a18ab8242c873325aa62c7785a33c8152a118fb781648a6bceb8534d259b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LambdaEventSourceMapping",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigOutputReference",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
    "LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
    "LambdaEventSourceMappingConfig",
    "LambdaEventSourceMappingDestinationConfig",
    "LambdaEventSourceMappingDestinationConfigOnFailure",
    "LambdaEventSourceMappingDestinationConfigOnFailureOutputReference",
    "LambdaEventSourceMappingDestinationConfigOutputReference",
    "LambdaEventSourceMappingDocumentDbEventSourceConfig",
    "LambdaEventSourceMappingDocumentDbEventSourceConfigOutputReference",
    "LambdaEventSourceMappingFilterCriteria",
    "LambdaEventSourceMappingFilterCriteriaFilter",
    "LambdaEventSourceMappingFilterCriteriaFilterList",
    "LambdaEventSourceMappingFilterCriteriaFilterOutputReference",
    "LambdaEventSourceMappingFilterCriteriaOutputReference",
    "LambdaEventSourceMappingMetricsConfig",
    "LambdaEventSourceMappingMetricsConfigOutputReference",
    "LambdaEventSourceMappingProvisionedPollerConfig",
    "LambdaEventSourceMappingProvisionedPollerConfigOutputReference",
    "LambdaEventSourceMappingScalingConfig",
    "LambdaEventSourceMappingScalingConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedEventSource",
    "LambdaEventSourceMappingSelfManagedEventSourceOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigList",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigOutputReference",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigList",
    "LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfigOutputReference",
    "LambdaEventSourceMappingSourceAccessConfiguration",
    "LambdaEventSourceMappingSourceAccessConfigurationList",
    "LambdaEventSourceMappingSourceAccessConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__6cb6ce533c6e65a9eb56e7ea548824ddb6aff1511a296fbd99148b15ab735c2c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_name: builtins.str,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    document_db_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingDocumentDbEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    metrics_config: typing.Optional[typing.Union[LambdaEventSourceMappingMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    provisioned_poller_config: typing.Optional[typing.Union[LambdaEventSourceMappingProvisionedPollerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[LambdaEventSourceMappingScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_event_source: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__273380baf80e663f9d240f7d4645a1aa5d21c92dffb6bbfe2d80dfb83dddb7ba(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ae94aa09c4b72eaadcb1c6349daa4979c24854571a11f8d4cb7c93e96e6cdb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec953d7f7e9362fc36d0c7f04b35797659bb2fdab959e52bcd556273c8947c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18c36c12c4b00cc3845460481b9870f5e4ee1767358163f5ed8c345986ae69b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd82623952d72eba23116dcfd6b06b4a38e2bd0404cb8f9e3e4784f5ad386b06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176b20eee35e9e2ba68c2fa2be59145dcbb8d94ea646398e37bf0ec0d078b180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1c0f85e3038f9fa349a9a6af803c18b97324e0be12ddc03501f0b818ae4b20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93810df7fa745971eac1f425bc1ab87b9e4078252ee525643063b761ec4eb5a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31ccea0308a0b13a268fa9b17926a5f2cb135ba99906d47275d7fe90429aa5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2062126ce46c77d5b4990525b61e6e1a3de6a9bebb5ecac84fcc4803a9114a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96ac0ca74998f24fcd7230d19a3c48eca2b1d28285ea98ba16e3ea8b9e960be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434fdc4f5aa9af36f58b892b01eb12f5d4c4b26d0e2bf42315b6938326035c82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bde15cbb63d14aef01063de9cc47dd14f53321b10ca71f0410d827d7bb8eeb4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddb5ba4f1bc732faa0759478d7b1a122649b6b7f89a36e3388486d1994e8b63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752c58e45cf783de49edc16ae4b29a1d5e69f230695a17092b896ee6bc7f6334(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceceacebc1f07de2a5ea778f5fc1c0f9cabe1b61870bb8267ee14683facd4fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cad8d58c86b44dcdff9688d1a26bf09dfecddab6fb0600d880c88ecd9de540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbb05d78af2407e8a2d162f87794f46be804925ce893effa015481115d9692c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b04ee4d8b5ba3f98a768b1705471353527502156baca4244b799cfce22b3ec(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe542f7a42dadb91b9de527a2d2d4ecf0acec87458e370741754bd6322927b26(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7419fb9dcae8c9c5d65a18840a7f81f5437ca2e01426c27685835aef27da2e32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d5f2dff8e03a3e1114b97ce3b03179134469da4d8f19f0dfc40d976a0bc67e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfad2d903a33e792f280a50ccddb827105d6c62b6a26cff4b2b5a4f9fbc6336(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
    schema_registry_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43835249eefdbdabe02486bbd9d0b4f6484e95708f89f4896d06ffe90ff78cb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d2d130b4a7381b524234880d9e24d75e53c2776fe3a51f0338239fbb7e6fb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d45e9b56a32ce3c8d063cb6caec75b1174491be2f030ac05589446a74a8f6d(
    value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50a0f247dd107d16bc8afca508397e783e5343a05ba80e600469e26df66a285(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_record_format: typing.Optional[builtins.str] = None,
    schema_registry_uri: typing.Optional[builtins.str] = None,
    schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4753c99082471d4580ba1a7ffd29e962b76522f3a3eeddb559160e03a3b0a6cb(
    *,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360750aa27956070f01c93146485ad42b517eeb040d701edb7d46214ba284188(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60451109141c59dbbd44221fa2f2920c8126b7bb4397474a6c7b8513dbaa6989(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c111bcc39c77be040c849d176b23040dddbfc08f82cbdcdecdb993fe79591c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6f75cfa1969704a7e47d46540764abdafaad798e7d2142345c183b3b5c369f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37750f881c58e34d5680ced2b17f5d61239d623d46568e41d570521a7b6713d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baaf6bd8c31e92a7cbd4da795d49d376aedbce332d6daa818910e4431ab28fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398cee90aa3a63768524a35db5a2dfc19ed310009c27e64b67c8915a302e8ace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927025ac75608d88da9b68db1cd59749c204d2e62d69fccf62546f73f8e483ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34914c52d047216978858472ad91831c25134f6bc26b487b4f6a1d9ff762312b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a3fc4d3f23eb0b8409f76646e79bf868b2e50a087e9a0e9c05fa40dd17a3af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4450b06a350545e5c2e1e8995e93ee6e5c23193bf735b0b6cfcfaa3a43f283(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2368570bcfb34ad03b81d0e4917862f08b0c72fb2f490b9da2b72b6a45d06f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47dc24040ba37c0d46a5eb672b1e39043ce04ab26212dfe2391cb9118aacf406(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637df446f2054bd0cdacded2df3558e8610a46209ed93cf01f9c16f52c7eeb2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04cb34ad0535f23465df705c239eff9b34e74a3e2cb6f4e639626e0dbd205169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1638534d36b009e2b4d52c9710a61ad41b919f8384b800dea3b4bfadc9b6c842(
    value: typing.Optional[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b40dc37628cbfe9191a5300b25b8c99410fcb3de162f91608f73d6499dae8a(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4e40be519b4e215217222001a3cd9afd73b1487cc3645623df46483896dee0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e7aa21b36c86f575f98ab15ed31ea383a7884406a6af88f3a9c729b3c5dad8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dcb38f35a4d71ddb7d282ef263bc9b8b8a7d7b22086d0eb3b9980e86480d4a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0761871fee1f574dd303b47aa28905445d480522575de2a6aab7a07ddcd3b80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a03c32a585223654eb6db64307f6952f6da9e8c8a5491b73f98fc389c1c21b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e374ba5d5061e821d7364dc6f9d49c3a06004b66a07b01a24eac174c06bf2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115ae7ebf2961b88636110d16b49dd6a4ea785b684cfd8552c8ac018ba16eda1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6c58891a3f2039c02df8220d8fe7ea7c0942a9229a701b424803dbb2635da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2f54aa3f01286a4f0916babb25cd093f090e5f1d6bb360d10488a0dd0b2862(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbbc460681fc2ad4150fe1062902897043c3521193786662018992d3176dad4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_name: builtins.str,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingAmazonManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    document_db_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingDocumentDbEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[LambdaEventSourceMappingFilterCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    metrics_config: typing.Optional[typing.Union[LambdaEventSourceMappingMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    provisioned_poller_config: typing.Optional[typing.Union[LambdaEventSourceMappingProvisionedPollerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[LambdaEventSourceMappingScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_event_source: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_access_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSourceAccessConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028a90c33bb0c45db5f28ea8edcf86f291ffabf179170f25cbdb5dcd4fb1fb44(
    *,
    on_failure: typing.Optional[typing.Union[LambdaEventSourceMappingDestinationConfigOnFailure, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8314496e4eb0aa4d89864dfcbc3d7046bc9d4faaafb8fe3a8002d858f4817377(
    *,
    destination_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cda9e23ed43ded982d0d842c4928bf5070cd21007adcd6f52c910304a341de2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d1ce955038c2e1a764ba36ba0e34b01addf4cf2804fd695e66d1994f957cb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e3b743ea68d2a4a70849d57efaef67e2bf6f4566a2ece1ec20c26c9000ffda(
    value: typing.Optional[LambdaEventSourceMappingDestinationConfigOnFailure],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4939f4e61cf10530de54603848d00dab8e112ff5c2e1bdde93c3a04edaa0627b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd3a35cf87b5e6fb8e5fe706dae1f6a0d38f958ad1ac3815399abd360e9f728(
    value: typing.Optional[LambdaEventSourceMappingDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba374d3afd5910dfe4e5ccdfcea94ce57e4738c544ac2d885dc3a58657ea1632(
    *,
    database_name: builtins.str,
    collection_name: typing.Optional[builtins.str] = None,
    full_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55534adbe3eaf1caaec14b372bae89af66afc5f1a530634e64538b9c75d366da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06a3c63200d1f14bc330a1c31970052c9da4da6abcb1497425d344913c654f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d477f1d41b62b5a0253dac7d268c59349d60e87ce4c4b258191e9e5480ba4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97740642bd95c63c78f313dedc12a606374b263c095ce46b7664a59eaef34fc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d63f26cc8a9f37ea46e13116ad8289cb959b6b450e6cd15e80aac66223c4e9(
    value: typing.Optional[LambdaEventSourceMappingDocumentDbEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3940c994dd7112704c875917bf796efa24d0fa30169aad09a714041c0d230ddf(
    *,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443eecbbf79c0e4d45522fa23d20b39de954d3413005398876010b981dfccbe7(
    *,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebd6317127329a831a9279d9a2855fb113d54d32f91cae9d63615d768305fb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600ff0e48cd3ee095053f29d65b99856d5a90a2e5e7c5ea2b28666ca66991b98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7f3400ba01e196a9f48591ad17ac1fc2d43301572501dde4e658f3e104c03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca5c654b346c58b7589f9c6a065d8b9d36c37f354af6321ee298a8273b36980(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fc46a265e4468c1a87d6d0dd09f1359063cf7a41e49dcfb7815a3cccb514a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ca5276ed784bc631ee025fc1cc2d799b1f4ae56279306a27448e2c9eb587bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingFilterCriteriaFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093afaef6a831f420abefc9fc905a9e7b00e120cc114d84c00359cd9c6857354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1085abf87c7b461a8c7b4e62e5423cd9f2e831bf4c2122f7ff3b56a0ed0b8925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b32f849878158d0007dbf1046800f0daef2b26c8b2425449329819fa07edfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingFilterCriteriaFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df129506a83ada76f0e182526a560c18be580c09bbe630dfe1d081d701ed857c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b22e1a650687225f2c1e1acf20810b1bfe9a2271f649f05bf4f442b0863a10b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingFilterCriteriaFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45214e67ed278410d0e8b4eb11f8b0aa57f4969c0cf6053acd24ac12f1aeb1e1(
    value: typing.Optional[LambdaEventSourceMappingFilterCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cb4769f3dfc23745c487e7d98833c3dbfae44625b9f272d6209249462f1da8(
    *,
    metrics: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33ee652c759fc7f6bb033c4a578ee48df52e23ad027ce1533cf01fc60ca2c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5d7e71d5d54d6358d2f4a0068c7f66f9a8779e8f30a4114962c1b0731c26e7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be99336559e3eb3c7499e3711922a3074cd4d70f7cf4248276232d83b6ad378(
    value: typing.Optional[LambdaEventSourceMappingMetricsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3245bbe0713114d2abe0831b29d2acfeec5c2757da4ec8bfa4a2423203a9f6(
    *,
    maximum_pollers: typing.Optional[jsii.Number] = None,
    minimum_pollers: typing.Optional[jsii.Number] = None,
    poller_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918744ae0ffa0cde71e001aea1fded591292f2f345ccc4a64c09072b935194db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11e6fd6c28d0de63e024b685b745007253b5819e3c8cba688fa8c435be1bacb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0cbc4eed4808b5b6c075d549b64fb1fc1035b8ccbdda88a0da01c72f2bdb1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12b79c1c9b70672111e9a4b80a4b3c469a4532910e0675b6674cb50a605f25b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe149d5b03f6236650ba51c4652ce07376a41cba2caf7069ecfbb1c0af23ae7(
    value: typing.Optional[LambdaEventSourceMappingProvisionedPollerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d0c735f1f7de981baa2961e38be83fb1bd3149fadf94fc8eeff706b9bcefef(
    *,
    maximum_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99bc1d243e123e4522d2558c03c29e180ae8936e4b69671365fd3f66ed5eae4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a9988bf7a2b163833f4398f16d2a978b1a179197c6c31d235700850921af26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c46d5d2cc611a63fd9196c40ab39d80e0cf7111f924d90c4cb4427d84b6e0cd(
    value: typing.Optional[LambdaEventSourceMappingScalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115d5f9219177d46395e59fd314e311ce074ff570d1fd2eb722a542a2fdeb92e(
    *,
    endpoints: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c057784b30b58adb3cfa0937252747d0d0620877c62d4588f921e04b8a83dcaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b24c12c3ee41860ad4399dca8064e0edd863a51f40316a885ebd4a372b69113(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844a1e4e6b8a6381015bbe44eca4b4f9210408149c1ab092d68010582e393856(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedEventSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354656de54122e5130a67f3e5a18ba33a4ffac9193a47bdfeb0f75b7917e0c25(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
    schema_registry_config: typing.Optional[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133121669affb2177227430d7587890d3bf15fdd74f9e2208abfa3a602a382b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efff89c72c62d7e3e060565d5aae79ee4cac8c6f79900965239abc5b9d32320(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f294a68e13ae18b0552e19c16c6e558f83e6e8c4919a02377da48cf56d2cd4c0(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ad875f10054d66b09061165ae971330fcd147eb252588ec168dd4979b5c33d(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_record_format: typing.Optional[builtins.str] = None,
    schema_registry_uri: typing.Optional[builtins.str] = None,
    schema_validation_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc01c8a30315ec4009f8f15d5bd5b03741f4a2f93c7572b665460b4091677eb(
    *,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd1a0e4ee22e84e9ad8cc6a60bb0624f3ad2fb958e070a358a26e50c82349bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331cd2594fc9b6264370906a31e40e5113f8f30691709d42b64338e1fa141025(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4d170702fe86f6f8a2cf9817836abfccda6ec070aaf675636310fe96a9f088(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a716e5f863f7d86ba1804755948fe3a182a0c54bb84f18aba63c9bc7dbb1e4d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc12adcaa169c1729650a85226a1fb55ef0f05e15ca426532ff75f035a340bb9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5365157bfe7d85e196743262873616a7547238023d06c558ddcd0c5b7d27558(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8cdccc2d7574beaf3d5f1f388643e2527f7eba06d9217dfa7c14219966d991(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61549e94c286f55a78b1a6984c52f553aa28b373b7006de2357a4a303385fe1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6682a0786cfe0922180888b19dfe5f34af9a709df52ac5cef8b77acb0a8ef0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf619b7d30d946ef2fafb72cc39ef5bb906b6aae11e4fd4212be171b4371105(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff712135f9cb640c44f9dbfe30471cb2d48bf4e5ae250356dfd8080704e219e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902d130efd24c47b320b355119c2caaa66aa4f17034e63627192a08d1f833b34(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237a49a219411a26fb15cc614c7b860920b25f91241754048e835fd8db6b51d1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3892a3e125df320043a765651b2c0a16aa3efee04d4e1ff948c2a373ad9890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5794c789f06d1890c39e6a592b040a7674f134030c7b6447ede54d2d51f88619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57d6c76eac2a79dc8c15ee51521ec338fe086783a699581d84ffa5b599c3216(
    value: typing.Optional[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5526f99aa164d7aeb9f486f635238e574607507891c2a1c970ca1918e6e09a12(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c71d51b12e37eb8c0c1aded9302a8139fafe2a7652ff56e490304ba8723193(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2668af891c8a205207d7622c7c51ff56097bbbfdb4baf5fee27835d5122867c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4de5600eabb07149bb5bdf771db99ecdaf8568522f4fceb7adb4ac345587444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a4246555ced3d1051927e6da16e5d71d0eae065236b530a32b446dccbcb108(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7e46172d1f3e8f54cac39e3e079fe47746e9cde5cc2f17bde3476367ea4279(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5a6906e618ecfe93881c5d92342b67a4eb99feb36da26f72ec334f32da7a56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14359e3e3ecb79f296e472f3865e7feb70ef25de9ccbbf0f8d8c8c0f6f14c4e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbdacd3cc16daec919e5e973fa533f8e836f66b488b14b71f91b8891c4a897e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a183eaf5b1ed544e84f1d31cb8aa167ef8bf9ca324b900713a43ba67b78091(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSelfManagedKafkaEventSourceConfigSchemaRegistryConfigSchemaValidationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692fe6b5a0772a18039296bca5c5aefdd93a8ede0e0673278320a39043661ffb(
    *,
    type: builtins.str,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1a4974fbaeb2376edfb79465454f892610fbd3eb5378753d0b0bc20df176f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8602953ed2e8ee9add8263d91ebaecbd6b223eae47257034b108f789eae0900(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e14ae2cd637db402a9bba6dfda094122e25bc6b8baf087f21588ea5e692b805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ac78ec485f68048deb02c7dfba04caae1f664d1363eb6727fe2c09e22844ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8af425498206707b40e2e5cfec85c90314aa5113ed0789bb8f78b6b9da904c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6cfe340651e936f4f606c4e7c1ca06fbf78244d4c108761a4a9cb3ff510036(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LambdaEventSourceMappingSourceAccessConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af6958c1d50e789b22c006627653a5846874b53203203043bd08cad33d55256(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b1b2eef46cba6539106742caeecd47d2fbecbbf3ee5d97e2daaa46932c662d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca914e27e3fb4a05e201739a8449c679e0da41e32bac601ff3949a4956d47797(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd51a18ab8242c873325aa62c7785a33c8152a118fb781648a6bceb8534d259b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LambdaEventSourceMappingSourceAccessConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
