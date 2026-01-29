r'''
# `aws_dms_endpoint`

Refer to the Terraform Registry for docs: [`aws_dms_endpoint`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint).
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


class DmsEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpoint",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint aws_dms_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        endpoint_id: builtins.str,
        endpoint_type: builtins.str,
        engine_name: builtins.str,
        certificate_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        elasticsearch_settings: typing.Optional[typing.Union["DmsEndpointElasticsearchSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        extra_connection_attributes: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kafka_settings: typing.Optional[typing.Union["DmsEndpointKafkaSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_settings: typing.Optional[typing.Union["DmsEndpointKinesisSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        mongodb_settings: typing.Optional[typing.Union["DmsEndpointMongodbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql_settings: typing.Optional[typing.Union["DmsEndpointMysqlSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_settings: typing.Optional[typing.Union["DmsEndpointOracleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        pause_replication_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port: typing.Optional[jsii.Number] = None,
        postgres_settings: typing.Optional[typing.Union["DmsEndpointPostgresSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        redis_settings: typing.Optional[typing.Union["DmsEndpointRedisSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_settings: typing.Optional[typing.Union["DmsEndpointRedshiftSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
        server_name: typing.Optional[builtins.str] = None,
        service_access_role: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DmsEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint aws_dms_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_id DmsEndpoint#endpoint_id}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_type DmsEndpoint#endpoint_type}.
        :param engine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#engine_name DmsEndpoint#engine_name}.
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#certificate_arn DmsEndpoint#certificate_arn}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#database_name DmsEndpoint#database_name}.
        :param elasticsearch_settings: elasticsearch_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#elasticsearch_settings DmsEndpoint#elasticsearch_settings}
        :param extra_connection_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#extra_connection_attributes DmsEndpoint#extra_connection_attributes}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#id DmsEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kafka_settings: kafka_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kafka_settings DmsEndpoint#kafka_settings}
        :param kinesis_settings: kinesis_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kinesis_settings DmsEndpoint#kinesis_settings}
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kms_key_arn DmsEndpoint#kms_key_arn}.
        :param mongodb_settings: mongodb_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#mongodb_settings DmsEndpoint#mongodb_settings}
        :param mysql_settings: mysql_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#mysql_settings DmsEndpoint#mysql_settings}
        :param oracle_settings: oracle_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#oracle_settings DmsEndpoint#oracle_settings}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#password DmsEndpoint#password}.
        :param pause_replication_tasks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#pause_replication_tasks DmsEndpoint#pause_replication_tasks}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#port DmsEndpoint#port}.
        :param postgres_settings: postgres_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#postgres_settings DmsEndpoint#postgres_settings}
        :param redis_settings: redis_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#redis_settings DmsEndpoint#redis_settings}
        :param redshift_settings: redshift_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#redshift_settings DmsEndpoint#redshift_settings}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#region DmsEndpoint#region}
        :param secrets_manager_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#secrets_manager_access_role_arn DmsEndpoint#secrets_manager_access_role_arn}.
        :param secrets_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#secrets_manager_arn DmsEndpoint#secrets_manager_arn}.
        :param server_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_name DmsEndpoint#server_name}.
        :param service_access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role DmsEndpoint#service_access_role}.
        :param ssl_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_mode DmsEndpoint#ssl_mode}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#tags DmsEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#tags_all DmsEndpoint#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#timeouts DmsEndpoint#timeouts}
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#username DmsEndpoint#username}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82865518ff11ec0d7c79e82a70ac8a1694fac502beded9c6729248e96d91d964)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DmsEndpointConfig(
            endpoint_id=endpoint_id,
            endpoint_type=endpoint_type,
            engine_name=engine_name,
            certificate_arn=certificate_arn,
            database_name=database_name,
            elasticsearch_settings=elasticsearch_settings,
            extra_connection_attributes=extra_connection_attributes,
            id=id,
            kafka_settings=kafka_settings,
            kinesis_settings=kinesis_settings,
            kms_key_arn=kms_key_arn,
            mongodb_settings=mongodb_settings,
            mysql_settings=mysql_settings,
            oracle_settings=oracle_settings,
            password=password,
            pause_replication_tasks=pause_replication_tasks,
            port=port,
            postgres_settings=postgres_settings,
            redis_settings=redis_settings,
            redshift_settings=redshift_settings,
            region=region,
            secrets_manager_access_role_arn=secrets_manager_access_role_arn,
            secrets_manager_arn=secrets_manager_arn,
            server_name=server_name,
            service_access_role=service_access_role,
            ssl_mode=ssl_mode,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            username=username,
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
        '''Generates CDKTF code for importing a DmsEndpoint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DmsEndpoint to import.
        :param import_from_id: The id of the existing DmsEndpoint that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DmsEndpoint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72cd95dd55b0ef427210f6c30803eeed8a9e1bf7a62c73ebffa11a0aed8a62ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putElasticsearchSettings")
    def put_elasticsearch_settings(
        self,
        *,
        endpoint_uri: builtins.str,
        service_access_role_arn: builtins.str,
        error_retry_duration: typing.Optional[jsii.Number] = None,
        full_load_error_percentage: typing.Optional[jsii.Number] = None,
        use_new_mapping_type: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpoint_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_uri DmsEndpoint#endpoint_uri}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param error_retry_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#error_retry_duration DmsEndpoint#error_retry_duration}.
        :param full_load_error_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#full_load_error_percentage DmsEndpoint#full_load_error_percentage}.
        :param use_new_mapping_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#use_new_mapping_type DmsEndpoint#use_new_mapping_type}.
        '''
        value = DmsEndpointElasticsearchSettings(
            endpoint_uri=endpoint_uri,
            service_access_role_arn=service_access_role_arn,
            error_retry_duration=error_retry_duration,
            full_load_error_percentage=full_load_error_percentage,
            use_new_mapping_type=use_new_mapping_type,
        )

        return typing.cast(None, jsii.invoke(self, "putElasticsearchSettings", [value]))

    @jsii.member(jsii_name="putKafkaSettings")
    def put_kafka_settings(
        self,
        *,
        broker: builtins.str,
        include_control_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_partition_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_transaction_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_format: typing.Optional[builtins.str] = None,
        message_max_bytes: typing.Optional[jsii.Number] = None,
        no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sasl_mechanism: typing.Optional[builtins.str] = None,
        sasl_password: typing.Optional[builtins.str] = None,
        sasl_username: typing.Optional[builtins.str] = None,
        security_protocol: typing.Optional[builtins.str] = None,
        ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_client_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_client_key_arn: typing.Optional[builtins.str] = None,
        ssl_client_key_password: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param broker: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#broker DmsEndpoint#broker}.
        :param include_control_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_control_details DmsEndpoint#include_control_details}.
        :param include_null_and_empty: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_null_and_empty DmsEndpoint#include_null_and_empty}.
        :param include_partition_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_partition_value DmsEndpoint#include_partition_value}.
        :param include_table_alter_operations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_table_alter_operations DmsEndpoint#include_table_alter_operations}.
        :param include_transaction_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_transaction_details DmsEndpoint#include_transaction_details}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_format DmsEndpoint#message_format}.
        :param message_max_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_max_bytes DmsEndpoint#message_max_bytes}.
        :param no_hex_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#no_hex_prefix DmsEndpoint#no_hex_prefix}.
        :param partition_include_schema_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#partition_include_schema_table DmsEndpoint#partition_include_schema_table}.
        :param sasl_mechanism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_mechanism DmsEndpoint#sasl_mechanism}.
        :param sasl_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_password DmsEndpoint#sasl_password}.
        :param sasl_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_username DmsEndpoint#sasl_username}.
        :param security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#security_protocol DmsEndpoint#security_protocol}.
        :param ssl_ca_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_ca_certificate_arn DmsEndpoint#ssl_ca_certificate_arn}.
        :param ssl_client_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_certificate_arn DmsEndpoint#ssl_client_certificate_arn}.
        :param ssl_client_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_key_arn DmsEndpoint#ssl_client_key_arn}.
        :param ssl_client_key_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_key_password DmsEndpoint#ssl_client_key_password}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#topic DmsEndpoint#topic}.
        '''
        value = DmsEndpointKafkaSettings(
            broker=broker,
            include_control_details=include_control_details,
            include_null_and_empty=include_null_and_empty,
            include_partition_value=include_partition_value,
            include_table_alter_operations=include_table_alter_operations,
            include_transaction_details=include_transaction_details,
            message_format=message_format,
            message_max_bytes=message_max_bytes,
            no_hex_prefix=no_hex_prefix,
            partition_include_schema_table=partition_include_schema_table,
            sasl_mechanism=sasl_mechanism,
            sasl_password=sasl_password,
            sasl_username=sasl_username,
            security_protocol=security_protocol,
            ssl_ca_certificate_arn=ssl_ca_certificate_arn,
            ssl_client_certificate_arn=ssl_client_certificate_arn,
            ssl_client_key_arn=ssl_client_key_arn,
            ssl_client_key_password=ssl_client_key_password,
            topic=topic,
        )

        return typing.cast(None, jsii.invoke(self, "putKafkaSettings", [value]))

    @jsii.member(jsii_name="putKinesisSettings")
    def put_kinesis_settings(
        self,
        *,
        include_control_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_partition_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_transaction_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_format: typing.Optional[builtins.str] = None,
        partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        stream_arn: typing.Optional[builtins.str] = None,
        use_large_integer_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param include_control_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_control_details DmsEndpoint#include_control_details}.
        :param include_null_and_empty: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_null_and_empty DmsEndpoint#include_null_and_empty}.
        :param include_partition_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_partition_value DmsEndpoint#include_partition_value}.
        :param include_table_alter_operations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_table_alter_operations DmsEndpoint#include_table_alter_operations}.
        :param include_transaction_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_transaction_details DmsEndpoint#include_transaction_details}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_format DmsEndpoint#message_format}.
        :param partition_include_schema_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#partition_include_schema_table DmsEndpoint#partition_include_schema_table}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#stream_arn DmsEndpoint#stream_arn}.
        :param use_large_integer_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#use_large_integer_value DmsEndpoint#use_large_integer_value}.
        '''
        value = DmsEndpointKinesisSettings(
            include_control_details=include_control_details,
            include_null_and_empty=include_null_and_empty,
            include_partition_value=include_partition_value,
            include_table_alter_operations=include_table_alter_operations,
            include_transaction_details=include_transaction_details,
            message_format=message_format,
            partition_include_schema_table=partition_include_schema_table,
            service_access_role_arn=service_access_role_arn,
            stream_arn=stream_arn,
            use_large_integer_value=use_large_integer_value,
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisSettings", [value]))

    @jsii.member(jsii_name="putMongodbSettings")
    def put_mongodb_settings(
        self,
        *,
        auth_mechanism: typing.Optional[builtins.str] = None,
        auth_source: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        docs_to_investigate: typing.Optional[builtins.str] = None,
        extract_doc_id: typing.Optional[builtins.str] = None,
        nesting_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_mechanism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_mechanism DmsEndpoint#auth_mechanism}.
        :param auth_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_source DmsEndpoint#auth_source}.
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_type DmsEndpoint#auth_type}.
        :param docs_to_investigate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#docs_to_investigate DmsEndpoint#docs_to_investigate}.
        :param extract_doc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#extract_doc_id DmsEndpoint#extract_doc_id}.
        :param nesting_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#nesting_level DmsEndpoint#nesting_level}.
        '''
        value = DmsEndpointMongodbSettings(
            auth_mechanism=auth_mechanism,
            auth_source=auth_source,
            auth_type=auth_type,
            docs_to_investigate=docs_to_investigate,
            extract_doc_id=extract_doc_id,
            nesting_level=nesting_level,
        )

        return typing.cast(None, jsii.invoke(self, "putMongodbSettings", [value]))

    @jsii.member(jsii_name="putMysqlSettings")
    def put_mysql_settings(
        self,
        *,
        after_connect_script: typing.Optional[builtins.str] = None,
        authentication_method: typing.Optional[builtins.str] = None,
        clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events_poll_interval: typing.Optional[jsii.Number] = None,
        execute_timeout: typing.Optional[jsii.Number] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        parallel_load_threads: typing.Optional[jsii.Number] = None,
        server_timezone: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        target_db_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param after_connect_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#after_connect_script DmsEndpoint#after_connect_script}.
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.
        :param clean_source_metadata_on_mismatch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#clean_source_metadata_on_mismatch DmsEndpoint#clean_source_metadata_on_mismatch}.
        :param events_poll_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#events_poll_interval DmsEndpoint#events_poll_interval}.
        :param execute_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#execute_timeout DmsEndpoint#execute_timeout}.
        :param max_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#max_file_size DmsEndpoint#max_file_size}.
        :param parallel_load_threads: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#parallel_load_threads DmsEndpoint#parallel_load_threads}.
        :param server_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_timezone DmsEndpoint#server_timezone}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param target_db_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#target_db_type DmsEndpoint#target_db_type}.
        '''
        value = DmsEndpointMysqlSettings(
            after_connect_script=after_connect_script,
            authentication_method=authentication_method,
            clean_source_metadata_on_mismatch=clean_source_metadata_on_mismatch,
            events_poll_interval=events_poll_interval,
            execute_timeout=execute_timeout,
            max_file_size=max_file_size,
            parallel_load_threads=parallel_load_threads,
            server_timezone=server_timezone,
            service_access_role_arn=service_access_role_arn,
            target_db_type=target_db_type,
        )

        return typing.cast(None, jsii.invoke(self, "putMysqlSettings", [value]))

    @jsii.member(jsii_name="putOracleSettings")
    def put_oracle_settings(
        self,
        *,
        authentication_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.
        '''
        value = DmsEndpointOracleSettings(authentication_method=authentication_method)

        return typing.cast(None, jsii.invoke(self, "putOracleSettings", [value]))

    @jsii.member(jsii_name="putPostgresSettings")
    def put_postgres_settings(
        self,
        *,
        after_connect_script: typing.Optional[builtins.str] = None,
        authentication_method: typing.Optional[builtins.str] = None,
        babelfish_database_name: typing.Optional[builtins.str] = None,
        capture_ddls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        database_mode: typing.Optional[builtins.str] = None,
        ddl_artifacts_schema: typing.Optional[builtins.str] = None,
        execute_timeout: typing.Optional[jsii.Number] = None,
        fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        heartbeat_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        heartbeat_frequency: typing.Optional[jsii.Number] = None,
        heartbeat_schema: typing.Optional[builtins.str] = None,
        map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_jsonb_as_clob: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_long_varchar_as: typing.Optional[builtins.str] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        slot_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param after_connect_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#after_connect_script DmsEndpoint#after_connect_script}.
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.
        :param babelfish_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#babelfish_database_name DmsEndpoint#babelfish_database_name}.
        :param capture_ddls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#capture_ddls DmsEndpoint#capture_ddls}.
        :param database_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#database_mode DmsEndpoint#database_mode}.
        :param ddl_artifacts_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ddl_artifacts_schema DmsEndpoint#ddl_artifacts_schema}.
        :param execute_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#execute_timeout DmsEndpoint#execute_timeout}.
        :param fail_tasks_on_lob_truncation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#fail_tasks_on_lob_truncation DmsEndpoint#fail_tasks_on_lob_truncation}.
        :param heartbeat_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_enable DmsEndpoint#heartbeat_enable}.
        :param heartbeat_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_frequency DmsEndpoint#heartbeat_frequency}.
        :param heartbeat_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_schema DmsEndpoint#heartbeat_schema}.
        :param map_boolean_as_boolean: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_boolean_as_boolean DmsEndpoint#map_boolean_as_boolean}.
        :param map_jsonb_as_clob: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_jsonb_as_clob DmsEndpoint#map_jsonb_as_clob}.
        :param map_long_varchar_as: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_long_varchar_as DmsEndpoint#map_long_varchar_as}.
        :param max_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#max_file_size DmsEndpoint#max_file_size}.
        :param plugin_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#plugin_name DmsEndpoint#plugin_name}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param slot_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#slot_name DmsEndpoint#slot_name}.
        '''
        value = DmsEndpointPostgresSettings(
            after_connect_script=after_connect_script,
            authentication_method=authentication_method,
            babelfish_database_name=babelfish_database_name,
            capture_ddls=capture_ddls,
            database_mode=database_mode,
            ddl_artifacts_schema=ddl_artifacts_schema,
            execute_timeout=execute_timeout,
            fail_tasks_on_lob_truncation=fail_tasks_on_lob_truncation,
            heartbeat_enable=heartbeat_enable,
            heartbeat_frequency=heartbeat_frequency,
            heartbeat_schema=heartbeat_schema,
            map_boolean_as_boolean=map_boolean_as_boolean,
            map_jsonb_as_clob=map_jsonb_as_clob,
            map_long_varchar_as=map_long_varchar_as,
            max_file_size=max_file_size,
            plugin_name=plugin_name,
            service_access_role_arn=service_access_role_arn,
            slot_name=slot_name,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresSettings", [value]))

    @jsii.member(jsii_name="putRedisSettings")
    def put_redis_settings(
        self,
        *,
        auth_type: builtins.str,
        port: jsii.Number,
        server_name: builtins.str,
        auth_password: typing.Optional[builtins.str] = None,
        auth_user_name: typing.Optional[builtins.str] = None,
        ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_security_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_type DmsEndpoint#auth_type}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#port DmsEndpoint#port}.
        :param server_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_name DmsEndpoint#server_name}.
        :param auth_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_password DmsEndpoint#auth_password}.
        :param auth_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_user_name DmsEndpoint#auth_user_name}.
        :param ssl_ca_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_ca_certificate_arn DmsEndpoint#ssl_ca_certificate_arn}.
        :param ssl_security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_security_protocol DmsEndpoint#ssl_security_protocol}.
        '''
        value = DmsEndpointRedisSettings(
            auth_type=auth_type,
            port=port,
            server_name=server_name,
            auth_password=auth_password,
            auth_user_name=auth_user_name,
            ssl_ca_certificate_arn=ssl_ca_certificate_arn,
            ssl_security_protocol=ssl_security_protocol,
        )

        return typing.cast(None, jsii.invoke(self, "putRedisSettings", [value]))

    @jsii.member(jsii_name="putRedshiftSettings")
    def put_redshift_settings(
        self,
        *,
        bucket_folder: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        encryption_mode: typing.Optional[builtins.str] = None,
        server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#bucket_folder DmsEndpoint#bucket_folder}.
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#bucket_name DmsEndpoint#bucket_name}.
        :param encryption_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#encryption_mode DmsEndpoint#encryption_mode}.
        :param server_side_encryption_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_side_encryption_kms_key_id DmsEndpoint#server_side_encryption_kms_key_id}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        '''
        value = DmsEndpointRedshiftSettings(
            bucket_folder=bucket_folder,
            bucket_name=bucket_name,
            encryption_mode=encryption_mode,
            server_side_encryption_kms_key_id=server_side_encryption_kms_key_id,
            service_access_role_arn=service_access_role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshiftSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#create DmsEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#delete DmsEndpoint#delete}.
        '''
        value = DmsEndpointTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertificateArn")
    def reset_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateArn", []))

    @jsii.member(jsii_name="resetDatabaseName")
    def reset_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseName", []))

    @jsii.member(jsii_name="resetElasticsearchSettings")
    def reset_elasticsearch_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchSettings", []))

    @jsii.member(jsii_name="resetExtraConnectionAttributes")
    def reset_extra_connection_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraConnectionAttributes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKafkaSettings")
    def reset_kafka_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafkaSettings", []))

    @jsii.member(jsii_name="resetKinesisSettings")
    def reset_kinesis_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisSettings", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetMongodbSettings")
    def reset_mongodb_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodbSettings", []))

    @jsii.member(jsii_name="resetMysqlSettings")
    def reset_mysql_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlSettings", []))

    @jsii.member(jsii_name="resetOracleSettings")
    def reset_oracle_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleSettings", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPauseReplicationTasks")
    def reset_pause_replication_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPauseReplicationTasks", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPostgresSettings")
    def reset_postgres_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresSettings", []))

    @jsii.member(jsii_name="resetRedisSettings")
    def reset_redis_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisSettings", []))

    @jsii.member(jsii_name="resetRedshiftSettings")
    def reset_redshift_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshiftSettings", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecretsManagerAccessRoleArn")
    def reset_secrets_manager_access_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsManagerAccessRoleArn", []))

    @jsii.member(jsii_name="resetSecretsManagerArn")
    def reset_secrets_manager_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsManagerArn", []))

    @jsii.member(jsii_name="resetServerName")
    def reset_server_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerName", []))

    @jsii.member(jsii_name="resetServiceAccessRole")
    def reset_service_access_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccessRole", []))

    @jsii.member(jsii_name="resetSslMode")
    def reset_ssl_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslMode", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

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
    @jsii.member(jsii_name="elasticsearchSettings")
    def elasticsearch_settings(
        self,
    ) -> "DmsEndpointElasticsearchSettingsOutputReference":
        return typing.cast("DmsEndpointElasticsearchSettingsOutputReference", jsii.get(self, "elasticsearchSettings"))

    @builtins.property
    @jsii.member(jsii_name="endpointArn")
    def endpoint_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointArn"))

    @builtins.property
    @jsii.member(jsii_name="kafkaSettings")
    def kafka_settings(self) -> "DmsEndpointKafkaSettingsOutputReference":
        return typing.cast("DmsEndpointKafkaSettingsOutputReference", jsii.get(self, "kafkaSettings"))

    @builtins.property
    @jsii.member(jsii_name="kinesisSettings")
    def kinesis_settings(self) -> "DmsEndpointKinesisSettingsOutputReference":
        return typing.cast("DmsEndpointKinesisSettingsOutputReference", jsii.get(self, "kinesisSettings"))

    @builtins.property
    @jsii.member(jsii_name="mongodbSettings")
    def mongodb_settings(self) -> "DmsEndpointMongodbSettingsOutputReference":
        return typing.cast("DmsEndpointMongodbSettingsOutputReference", jsii.get(self, "mongodbSettings"))

    @builtins.property
    @jsii.member(jsii_name="mysqlSettings")
    def mysql_settings(self) -> "DmsEndpointMysqlSettingsOutputReference":
        return typing.cast("DmsEndpointMysqlSettingsOutputReference", jsii.get(self, "mysqlSettings"))

    @builtins.property
    @jsii.member(jsii_name="oracleSettings")
    def oracle_settings(self) -> "DmsEndpointOracleSettingsOutputReference":
        return typing.cast("DmsEndpointOracleSettingsOutputReference", jsii.get(self, "oracleSettings"))

    @builtins.property
    @jsii.member(jsii_name="postgresSettings")
    def postgres_settings(self) -> "DmsEndpointPostgresSettingsOutputReference":
        return typing.cast("DmsEndpointPostgresSettingsOutputReference", jsii.get(self, "postgresSettings"))

    @builtins.property
    @jsii.member(jsii_name="redisSettings")
    def redis_settings(self) -> "DmsEndpointRedisSettingsOutputReference":
        return typing.cast("DmsEndpointRedisSettingsOutputReference", jsii.get(self, "redisSettings"))

    @builtins.property
    @jsii.member(jsii_name="redshiftSettings")
    def redshift_settings(self) -> "DmsEndpointRedshiftSettingsOutputReference":
        return typing.cast("DmsEndpointRedshiftSettingsOutputReference", jsii.get(self, "redshiftSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DmsEndpointTimeoutsOutputReference":
        return typing.cast("DmsEndpointTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="certificateArnInput")
    def certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchSettingsInput")
    def elasticsearch_settings_input(
        self,
    ) -> typing.Optional["DmsEndpointElasticsearchSettings"]:
        return typing.cast(typing.Optional["DmsEndpointElasticsearchSettings"], jsii.get(self, "elasticsearchSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointIdInput")
    def endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="engineNameInput")
    def engine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="extraConnectionAttributesInput")
    def extra_connection_attributes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extraConnectionAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaSettingsInput")
    def kafka_settings_input(self) -> typing.Optional["DmsEndpointKafkaSettings"]:
        return typing.cast(typing.Optional["DmsEndpointKafkaSettings"], jsii.get(self, "kafkaSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisSettingsInput")
    def kinesis_settings_input(self) -> typing.Optional["DmsEndpointKinesisSettings"]:
        return typing.cast(typing.Optional["DmsEndpointKinesisSettings"], jsii.get(self, "kinesisSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbSettingsInput")
    def mongodb_settings_input(self) -> typing.Optional["DmsEndpointMongodbSettings"]:
        return typing.cast(typing.Optional["DmsEndpointMongodbSettings"], jsii.get(self, "mongodbSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlSettingsInput")
    def mysql_settings_input(self) -> typing.Optional["DmsEndpointMysqlSettings"]:
        return typing.cast(typing.Optional["DmsEndpointMysqlSettings"], jsii.get(self, "mysqlSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleSettingsInput")
    def oracle_settings_input(self) -> typing.Optional["DmsEndpointOracleSettings"]:
        return typing.cast(typing.Optional["DmsEndpointOracleSettings"], jsii.get(self, "oracleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pauseReplicationTasksInput")
    def pause_replication_tasks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pauseReplicationTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresSettingsInput")
    def postgres_settings_input(self) -> typing.Optional["DmsEndpointPostgresSettings"]:
        return typing.cast(typing.Optional["DmsEndpointPostgresSettings"], jsii.get(self, "postgresSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="redisSettingsInput")
    def redis_settings_input(self) -> typing.Optional["DmsEndpointRedisSettings"]:
        return typing.cast(typing.Optional["DmsEndpointRedisSettings"], jsii.get(self, "redisSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftSettingsInput")
    def redshift_settings_input(self) -> typing.Optional["DmsEndpointRedshiftSettings"]:
        return typing.cast(typing.Optional["DmsEndpointRedshiftSettings"], jsii.get(self, "redshiftSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsManagerAccessRoleArnInput")
    def secrets_manager_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsManagerAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsManagerArnInput")
    def secrets_manager_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsManagerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="serverNameInput")
    def server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleInput")
    def service_access_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccessRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="sslModeInput")
    def ssl_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslModeInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsEndpointTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsEndpointTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b377c78d11666a4f207dffc165c5558eef9c779d1db6a7896f678e9709e3c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf020450c8098d62d97e24aecad3923f321a7c03ff3fd02fcaa94939db2dd101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointId")
    def endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointId"))

    @endpoint_id.setter
    def endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cca73304c43ed9f0530576647f25dc884612544dff70ec0325b99eb0e8e643d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89d89edc28b3bf9863b8bc462975cb980c134b222b0c6310674c23b4ae02203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineName")
    def engine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineName"))

    @engine_name.setter
    def engine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c655bf7645f162d6c5781ab6e4a88ce69aee6527754ff3a5ef7e84eff7968f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraConnectionAttributes")
    def extra_connection_attributes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extraConnectionAttributes"))

    @extra_connection_attributes.setter
    def extra_connection_attributes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2332929ab9f9fee91673cfe39cd52e3cdb53759f5bf966cd87ec3f23ed8ff158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraConnectionAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c59d242326572531979145f8b580cabd42f524cee1826a9dea30006258a6938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436bbbd6fd671d72ae4819049cad8f7d4d45a23b846e250888b9c7e4c89ec068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d77f26e123922083eaa50b923a5ebd6e75bcd3be19c959381523d52a8d146d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pauseReplicationTasks")
    def pause_replication_tasks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pauseReplicationTasks"))

    @pause_replication_tasks.setter
    def pause_replication_tasks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8afc16112ae43fac9e726ade028a07f58f3d05a96bb0d1a838b8cc5051a6fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pauseReplicationTasks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1f6c73cdc81fba11037472e16d8b0ce4a571d63cfaa249d57d7f3b96d3ee05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0d57fafb8e1785051bf92f270123e72b687a19d45c6416ba717ee3ab733634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretsManagerAccessRoleArn")
    def secrets_manager_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsManagerAccessRoleArn"))

    @secrets_manager_access_role_arn.setter
    def secrets_manager_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734ab7903343a2e2a2ed5dd32e6fdeb5df419082390924bed55ed612abebf25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretsManagerAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretsManagerArn")
    def secrets_manager_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsManagerArn"))

    @secrets_manager_arn.setter
    def secrets_manager_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6470149a8cb8bd31f67828f162b58c847dc92d25189f872a0a509983bd50d035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretsManagerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverName")
    def server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverName"))

    @server_name.setter
    def server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecf8ab79355935e77ed1cafc5c0e2da698975f69839b9393d220d30ec175b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRole")
    def service_access_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccessRole"))

    @service_access_role.setter
    def service_access_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1b09e5c54b434947dd5229bcba6da0829fcbcac973cacfdce7f843a69a08e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslMode")
    def ssl_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslMode"))

    @ssl_mode.setter
    def ssl_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d468d57d9c44903719c9038d15109cab2d3c83632cf0a094225a91a545b22a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989a50b47f85c3f419df7951d743a20bb1f1c2274bab8e4d92ad3e22780ad4f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23aac4dcf0b5b7011dd47715c70fdf104cee01a945450d8b18020ac01c7dc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2611ba00b52953341c42861c26e00e60daa2d10a082183218d782470b6dd54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "endpoint_id": "endpointId",
        "endpoint_type": "endpointType",
        "engine_name": "engineName",
        "certificate_arn": "certificateArn",
        "database_name": "databaseName",
        "elasticsearch_settings": "elasticsearchSettings",
        "extra_connection_attributes": "extraConnectionAttributes",
        "id": "id",
        "kafka_settings": "kafkaSettings",
        "kinesis_settings": "kinesisSettings",
        "kms_key_arn": "kmsKeyArn",
        "mongodb_settings": "mongodbSettings",
        "mysql_settings": "mysqlSettings",
        "oracle_settings": "oracleSettings",
        "password": "password",
        "pause_replication_tasks": "pauseReplicationTasks",
        "port": "port",
        "postgres_settings": "postgresSettings",
        "redis_settings": "redisSettings",
        "redshift_settings": "redshiftSettings",
        "region": "region",
        "secrets_manager_access_role_arn": "secretsManagerAccessRoleArn",
        "secrets_manager_arn": "secretsManagerArn",
        "server_name": "serverName",
        "service_access_role": "serviceAccessRole",
        "ssl_mode": "sslMode",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "username": "username",
    },
)
class DmsEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        endpoint_id: builtins.str,
        endpoint_type: builtins.str,
        engine_name: builtins.str,
        certificate_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        elasticsearch_settings: typing.Optional[typing.Union["DmsEndpointElasticsearchSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        extra_connection_attributes: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kafka_settings: typing.Optional[typing.Union["DmsEndpointKafkaSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_settings: typing.Optional[typing.Union["DmsEndpointKinesisSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        mongodb_settings: typing.Optional[typing.Union["DmsEndpointMongodbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql_settings: typing.Optional[typing.Union["DmsEndpointMysqlSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_settings: typing.Optional[typing.Union["DmsEndpointOracleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        pause_replication_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        port: typing.Optional[jsii.Number] = None,
        postgres_settings: typing.Optional[typing.Union["DmsEndpointPostgresSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        redis_settings: typing.Optional[typing.Union["DmsEndpointRedisSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_settings: typing.Optional[typing.Union["DmsEndpointRedshiftSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
        server_name: typing.Optional[builtins.str] = None,
        service_access_role: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DmsEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_id DmsEndpoint#endpoint_id}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_type DmsEndpoint#endpoint_type}.
        :param engine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#engine_name DmsEndpoint#engine_name}.
        :param certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#certificate_arn DmsEndpoint#certificate_arn}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#database_name DmsEndpoint#database_name}.
        :param elasticsearch_settings: elasticsearch_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#elasticsearch_settings DmsEndpoint#elasticsearch_settings}
        :param extra_connection_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#extra_connection_attributes DmsEndpoint#extra_connection_attributes}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#id DmsEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kafka_settings: kafka_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kafka_settings DmsEndpoint#kafka_settings}
        :param kinesis_settings: kinesis_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kinesis_settings DmsEndpoint#kinesis_settings}
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kms_key_arn DmsEndpoint#kms_key_arn}.
        :param mongodb_settings: mongodb_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#mongodb_settings DmsEndpoint#mongodb_settings}
        :param mysql_settings: mysql_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#mysql_settings DmsEndpoint#mysql_settings}
        :param oracle_settings: oracle_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#oracle_settings DmsEndpoint#oracle_settings}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#password DmsEndpoint#password}.
        :param pause_replication_tasks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#pause_replication_tasks DmsEndpoint#pause_replication_tasks}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#port DmsEndpoint#port}.
        :param postgres_settings: postgres_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#postgres_settings DmsEndpoint#postgres_settings}
        :param redis_settings: redis_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#redis_settings DmsEndpoint#redis_settings}
        :param redshift_settings: redshift_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#redshift_settings DmsEndpoint#redshift_settings}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#region DmsEndpoint#region}
        :param secrets_manager_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#secrets_manager_access_role_arn DmsEndpoint#secrets_manager_access_role_arn}.
        :param secrets_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#secrets_manager_arn DmsEndpoint#secrets_manager_arn}.
        :param server_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_name DmsEndpoint#server_name}.
        :param service_access_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role DmsEndpoint#service_access_role}.
        :param ssl_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_mode DmsEndpoint#ssl_mode}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#tags DmsEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#tags_all DmsEndpoint#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#timeouts DmsEndpoint#timeouts}
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#username DmsEndpoint#username}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(elasticsearch_settings, dict):
            elasticsearch_settings = DmsEndpointElasticsearchSettings(**elasticsearch_settings)
        if isinstance(kafka_settings, dict):
            kafka_settings = DmsEndpointKafkaSettings(**kafka_settings)
        if isinstance(kinesis_settings, dict):
            kinesis_settings = DmsEndpointKinesisSettings(**kinesis_settings)
        if isinstance(mongodb_settings, dict):
            mongodb_settings = DmsEndpointMongodbSettings(**mongodb_settings)
        if isinstance(mysql_settings, dict):
            mysql_settings = DmsEndpointMysqlSettings(**mysql_settings)
        if isinstance(oracle_settings, dict):
            oracle_settings = DmsEndpointOracleSettings(**oracle_settings)
        if isinstance(postgres_settings, dict):
            postgres_settings = DmsEndpointPostgresSettings(**postgres_settings)
        if isinstance(redis_settings, dict):
            redis_settings = DmsEndpointRedisSettings(**redis_settings)
        if isinstance(redshift_settings, dict):
            redshift_settings = DmsEndpointRedshiftSettings(**redshift_settings)
        if isinstance(timeouts, dict):
            timeouts = DmsEndpointTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4271b8edf97e24550273f060cffa2fae9e24f0ef043f68fcbc1416eec910c536)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument engine_name", value=engine_name, expected_type=type_hints["engine_name"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument elasticsearch_settings", value=elasticsearch_settings, expected_type=type_hints["elasticsearch_settings"])
            check_type(argname="argument extra_connection_attributes", value=extra_connection_attributes, expected_type=type_hints["extra_connection_attributes"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kafka_settings", value=kafka_settings, expected_type=type_hints["kafka_settings"])
            check_type(argname="argument kinesis_settings", value=kinesis_settings, expected_type=type_hints["kinesis_settings"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument mongodb_settings", value=mongodb_settings, expected_type=type_hints["mongodb_settings"])
            check_type(argname="argument mysql_settings", value=mysql_settings, expected_type=type_hints["mysql_settings"])
            check_type(argname="argument oracle_settings", value=oracle_settings, expected_type=type_hints["oracle_settings"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument pause_replication_tasks", value=pause_replication_tasks, expected_type=type_hints["pause_replication_tasks"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument postgres_settings", value=postgres_settings, expected_type=type_hints["postgres_settings"])
            check_type(argname="argument redis_settings", value=redis_settings, expected_type=type_hints["redis_settings"])
            check_type(argname="argument redshift_settings", value=redshift_settings, expected_type=type_hints["redshift_settings"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secrets_manager_access_role_arn", value=secrets_manager_access_role_arn, expected_type=type_hints["secrets_manager_access_role_arn"])
            check_type(argname="argument secrets_manager_arn", value=secrets_manager_arn, expected_type=type_hints["secrets_manager_arn"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            check_type(argname="argument service_access_role", value=service_access_role, expected_type=type_hints["service_access_role"])
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_id": endpoint_id,
            "endpoint_type": endpoint_type,
            "engine_name": engine_name,
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
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if database_name is not None:
            self._values["database_name"] = database_name
        if elasticsearch_settings is not None:
            self._values["elasticsearch_settings"] = elasticsearch_settings
        if extra_connection_attributes is not None:
            self._values["extra_connection_attributes"] = extra_connection_attributes
        if id is not None:
            self._values["id"] = id
        if kafka_settings is not None:
            self._values["kafka_settings"] = kafka_settings
        if kinesis_settings is not None:
            self._values["kinesis_settings"] = kinesis_settings
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if mongodb_settings is not None:
            self._values["mongodb_settings"] = mongodb_settings
        if mysql_settings is not None:
            self._values["mysql_settings"] = mysql_settings
        if oracle_settings is not None:
            self._values["oracle_settings"] = oracle_settings
        if password is not None:
            self._values["password"] = password
        if pause_replication_tasks is not None:
            self._values["pause_replication_tasks"] = pause_replication_tasks
        if port is not None:
            self._values["port"] = port
        if postgres_settings is not None:
            self._values["postgres_settings"] = postgres_settings
        if redis_settings is not None:
            self._values["redis_settings"] = redis_settings
        if redshift_settings is not None:
            self._values["redshift_settings"] = redshift_settings
        if region is not None:
            self._values["region"] = region
        if secrets_manager_access_role_arn is not None:
            self._values["secrets_manager_access_role_arn"] = secrets_manager_access_role_arn
        if secrets_manager_arn is not None:
            self._values["secrets_manager_arn"] = secrets_manager_arn
        if server_name is not None:
            self._values["server_name"] = server_name
        if service_access_role is not None:
            self._values["service_access_role"] = service_access_role
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if username is not None:
            self._values["username"] = username

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
    def endpoint_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_id DmsEndpoint#endpoint_id}.'''
        result = self._values.get("endpoint_id")
        assert result is not None, "Required property 'endpoint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_type DmsEndpoint#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#engine_name DmsEndpoint#engine_name}.'''
        result = self._values.get("engine_name")
        assert result is not None, "Required property 'engine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#certificate_arn DmsEndpoint#certificate_arn}.'''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#database_name DmsEndpoint#database_name}.'''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_settings(
        self,
    ) -> typing.Optional["DmsEndpointElasticsearchSettings"]:
        '''elasticsearch_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#elasticsearch_settings DmsEndpoint#elasticsearch_settings}
        '''
        result = self._values.get("elasticsearch_settings")
        return typing.cast(typing.Optional["DmsEndpointElasticsearchSettings"], result)

    @builtins.property
    def extra_connection_attributes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#extra_connection_attributes DmsEndpoint#extra_connection_attributes}.'''
        result = self._values.get("extra_connection_attributes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#id DmsEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka_settings(self) -> typing.Optional["DmsEndpointKafkaSettings"]:
        '''kafka_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kafka_settings DmsEndpoint#kafka_settings}
        '''
        result = self._values.get("kafka_settings")
        return typing.cast(typing.Optional["DmsEndpointKafkaSettings"], result)

    @builtins.property
    def kinesis_settings(self) -> typing.Optional["DmsEndpointKinesisSettings"]:
        '''kinesis_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kinesis_settings DmsEndpoint#kinesis_settings}
        '''
        result = self._values.get("kinesis_settings")
        return typing.cast(typing.Optional["DmsEndpointKinesisSettings"], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#kms_key_arn DmsEndpoint#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mongodb_settings(self) -> typing.Optional["DmsEndpointMongodbSettings"]:
        '''mongodb_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#mongodb_settings DmsEndpoint#mongodb_settings}
        '''
        result = self._values.get("mongodb_settings")
        return typing.cast(typing.Optional["DmsEndpointMongodbSettings"], result)

    @builtins.property
    def mysql_settings(self) -> typing.Optional["DmsEndpointMysqlSettings"]:
        '''mysql_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#mysql_settings DmsEndpoint#mysql_settings}
        '''
        result = self._values.get("mysql_settings")
        return typing.cast(typing.Optional["DmsEndpointMysqlSettings"], result)

    @builtins.property
    def oracle_settings(self) -> typing.Optional["DmsEndpointOracleSettings"]:
        '''oracle_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#oracle_settings DmsEndpoint#oracle_settings}
        '''
        result = self._values.get("oracle_settings")
        return typing.cast(typing.Optional["DmsEndpointOracleSettings"], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#password DmsEndpoint#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pause_replication_tasks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#pause_replication_tasks DmsEndpoint#pause_replication_tasks}.'''
        result = self._values.get("pause_replication_tasks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#port DmsEndpoint#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def postgres_settings(self) -> typing.Optional["DmsEndpointPostgresSettings"]:
        '''postgres_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#postgres_settings DmsEndpoint#postgres_settings}
        '''
        result = self._values.get("postgres_settings")
        return typing.cast(typing.Optional["DmsEndpointPostgresSettings"], result)

    @builtins.property
    def redis_settings(self) -> typing.Optional["DmsEndpointRedisSettings"]:
        '''redis_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#redis_settings DmsEndpoint#redis_settings}
        '''
        result = self._values.get("redis_settings")
        return typing.cast(typing.Optional["DmsEndpointRedisSettings"], result)

    @builtins.property
    def redshift_settings(self) -> typing.Optional["DmsEndpointRedshiftSettings"]:
        '''redshift_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#redshift_settings DmsEndpoint#redshift_settings}
        '''
        result = self._values.get("redshift_settings")
        return typing.cast(typing.Optional["DmsEndpointRedshiftSettings"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#region DmsEndpoint#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_manager_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#secrets_manager_access_role_arn DmsEndpoint#secrets_manager_access_role_arn}.'''
        result = self._values.get("secrets_manager_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_manager_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#secrets_manager_arn DmsEndpoint#secrets_manager_arn}.'''
        result = self._values.get("secrets_manager_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_name DmsEndpoint#server_name}.'''
        result = self._values.get("server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_access_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role DmsEndpoint#service_access_role}.'''
        result = self._values.get("service_access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_mode DmsEndpoint#ssl_mode}.'''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#tags DmsEndpoint#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#tags_all DmsEndpoint#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DmsEndpointTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#timeouts DmsEndpoint#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DmsEndpointTimeouts"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#username DmsEndpoint#username}.'''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointElasticsearchSettings",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_uri": "endpointUri",
        "service_access_role_arn": "serviceAccessRoleArn",
        "error_retry_duration": "errorRetryDuration",
        "full_load_error_percentage": "fullLoadErrorPercentage",
        "use_new_mapping_type": "useNewMappingType",
    },
)
class DmsEndpointElasticsearchSettings:
    def __init__(
        self,
        *,
        endpoint_uri: builtins.str,
        service_access_role_arn: builtins.str,
        error_retry_duration: typing.Optional[jsii.Number] = None,
        full_load_error_percentage: typing.Optional[jsii.Number] = None,
        use_new_mapping_type: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpoint_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_uri DmsEndpoint#endpoint_uri}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param error_retry_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#error_retry_duration DmsEndpoint#error_retry_duration}.
        :param full_load_error_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#full_load_error_percentage DmsEndpoint#full_load_error_percentage}.
        :param use_new_mapping_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#use_new_mapping_type DmsEndpoint#use_new_mapping_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0935c528bd62469f23d809b6fa1d43cec2b42fea93e6a81bc5cdbb73e8e12008)
            check_type(argname="argument endpoint_uri", value=endpoint_uri, expected_type=type_hints["endpoint_uri"])
            check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            check_type(argname="argument error_retry_duration", value=error_retry_duration, expected_type=type_hints["error_retry_duration"])
            check_type(argname="argument full_load_error_percentage", value=full_load_error_percentage, expected_type=type_hints["full_load_error_percentage"])
            check_type(argname="argument use_new_mapping_type", value=use_new_mapping_type, expected_type=type_hints["use_new_mapping_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_uri": endpoint_uri,
            "service_access_role_arn": service_access_role_arn,
        }
        if error_retry_duration is not None:
            self._values["error_retry_duration"] = error_retry_duration
        if full_load_error_percentage is not None:
            self._values["full_load_error_percentage"] = full_load_error_percentage
        if use_new_mapping_type is not None:
            self._values["use_new_mapping_type"] = use_new_mapping_type

    @builtins.property
    def endpoint_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#endpoint_uri DmsEndpoint#endpoint_uri}.'''
        result = self._values.get("endpoint_uri")
        assert result is not None, "Required property 'endpoint_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_access_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.'''
        result = self._values.get("service_access_role_arn")
        assert result is not None, "Required property 'service_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_retry_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#error_retry_duration DmsEndpoint#error_retry_duration}.'''
        result = self._values.get("error_retry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def full_load_error_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#full_load_error_percentage DmsEndpoint#full_load_error_percentage}.'''
        result = self._values.get("full_load_error_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_new_mapping_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#use_new_mapping_type DmsEndpoint#use_new_mapping_type}.'''
        result = self._values.get("use_new_mapping_type")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointElasticsearchSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointElasticsearchSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointElasticsearchSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2426837a5a65a7bdcffce69fc9d4a13cbd0a1c70760d297c3d36bef6c85c96fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetErrorRetryDuration")
    def reset_error_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorRetryDuration", []))

    @jsii.member(jsii_name="resetFullLoadErrorPercentage")
    def reset_full_load_error_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullLoadErrorPercentage", []))

    @jsii.member(jsii_name="resetUseNewMappingType")
    def reset_use_new_mapping_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseNewMappingType", []))

    @builtins.property
    @jsii.member(jsii_name="endpointUriInput")
    def endpoint_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointUriInput"))

    @builtins.property
    @jsii.member(jsii_name="errorRetryDurationInput")
    def error_retry_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "errorRetryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="fullLoadErrorPercentageInput")
    def full_load_error_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fullLoadErrorPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArnInput")
    def service_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="useNewMappingTypeInput")
    def use_new_mapping_type_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useNewMappingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointUri")
    def endpoint_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointUri"))

    @endpoint_uri.setter
    def endpoint_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0485f47c371d32303d40fa06be133b48ccec2b373200319b6d3f14f9886ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorRetryDuration")
    def error_retry_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "errorRetryDuration"))

    @error_retry_duration.setter
    def error_retry_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4ed5995dc86a12a8960ecdf2d0b670267dc7ed051dad8286cff699863ca2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorRetryDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullLoadErrorPercentage")
    def full_load_error_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fullLoadErrorPercentage"))

    @full_load_error_percentage.setter
    def full_load_error_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1ea82d66826e4111b489c92a6fd612d8317180b19c471e9801505263540a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullLoadErrorPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccessRoleArn"))

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db7ae8011492e0b066a9e892aa6456cbe3a99702fb655ee08e1ba772dd7f636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNewMappingType")
    def use_new_mapping_type(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useNewMappingType"))

    @use_new_mapping_type.setter
    def use_new_mapping_type(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c080155112f741e50cc28c99d3d81f3386be7cdb3a6ecb80e403e360fce3954a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNewMappingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointElasticsearchSettings]:
        return typing.cast(typing.Optional[DmsEndpointElasticsearchSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsEndpointElasticsearchSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3493cc9a19b442f1acaaa73452a80d544a94fe2f7331ea478a5519e2ac84d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointKafkaSettings",
    jsii_struct_bases=[],
    name_mapping={
        "broker": "broker",
        "include_control_details": "includeControlDetails",
        "include_null_and_empty": "includeNullAndEmpty",
        "include_partition_value": "includePartitionValue",
        "include_table_alter_operations": "includeTableAlterOperations",
        "include_transaction_details": "includeTransactionDetails",
        "message_format": "messageFormat",
        "message_max_bytes": "messageMaxBytes",
        "no_hex_prefix": "noHexPrefix",
        "partition_include_schema_table": "partitionIncludeSchemaTable",
        "sasl_mechanism": "saslMechanism",
        "sasl_password": "saslPassword",
        "sasl_username": "saslUsername",
        "security_protocol": "securityProtocol",
        "ssl_ca_certificate_arn": "sslCaCertificateArn",
        "ssl_client_certificate_arn": "sslClientCertificateArn",
        "ssl_client_key_arn": "sslClientKeyArn",
        "ssl_client_key_password": "sslClientKeyPassword",
        "topic": "topic",
    },
)
class DmsEndpointKafkaSettings:
    def __init__(
        self,
        *,
        broker: builtins.str,
        include_control_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_partition_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_transaction_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_format: typing.Optional[builtins.str] = None,
        message_max_bytes: typing.Optional[jsii.Number] = None,
        no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sasl_mechanism: typing.Optional[builtins.str] = None,
        sasl_password: typing.Optional[builtins.str] = None,
        sasl_username: typing.Optional[builtins.str] = None,
        security_protocol: typing.Optional[builtins.str] = None,
        ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_client_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_client_key_arn: typing.Optional[builtins.str] = None,
        ssl_client_key_password: typing.Optional[builtins.str] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param broker: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#broker DmsEndpoint#broker}.
        :param include_control_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_control_details DmsEndpoint#include_control_details}.
        :param include_null_and_empty: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_null_and_empty DmsEndpoint#include_null_and_empty}.
        :param include_partition_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_partition_value DmsEndpoint#include_partition_value}.
        :param include_table_alter_operations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_table_alter_operations DmsEndpoint#include_table_alter_operations}.
        :param include_transaction_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_transaction_details DmsEndpoint#include_transaction_details}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_format DmsEndpoint#message_format}.
        :param message_max_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_max_bytes DmsEndpoint#message_max_bytes}.
        :param no_hex_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#no_hex_prefix DmsEndpoint#no_hex_prefix}.
        :param partition_include_schema_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#partition_include_schema_table DmsEndpoint#partition_include_schema_table}.
        :param sasl_mechanism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_mechanism DmsEndpoint#sasl_mechanism}.
        :param sasl_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_password DmsEndpoint#sasl_password}.
        :param sasl_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_username DmsEndpoint#sasl_username}.
        :param security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#security_protocol DmsEndpoint#security_protocol}.
        :param ssl_ca_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_ca_certificate_arn DmsEndpoint#ssl_ca_certificate_arn}.
        :param ssl_client_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_certificate_arn DmsEndpoint#ssl_client_certificate_arn}.
        :param ssl_client_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_key_arn DmsEndpoint#ssl_client_key_arn}.
        :param ssl_client_key_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_key_password DmsEndpoint#ssl_client_key_password}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#topic DmsEndpoint#topic}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492b0f45f640bbe5e03b9d2867e32dc7af8a38b827990014de779d4877f07dac)
            check_type(argname="argument broker", value=broker, expected_type=type_hints["broker"])
            check_type(argname="argument include_control_details", value=include_control_details, expected_type=type_hints["include_control_details"])
            check_type(argname="argument include_null_and_empty", value=include_null_and_empty, expected_type=type_hints["include_null_and_empty"])
            check_type(argname="argument include_partition_value", value=include_partition_value, expected_type=type_hints["include_partition_value"])
            check_type(argname="argument include_table_alter_operations", value=include_table_alter_operations, expected_type=type_hints["include_table_alter_operations"])
            check_type(argname="argument include_transaction_details", value=include_transaction_details, expected_type=type_hints["include_transaction_details"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
            check_type(argname="argument message_max_bytes", value=message_max_bytes, expected_type=type_hints["message_max_bytes"])
            check_type(argname="argument no_hex_prefix", value=no_hex_prefix, expected_type=type_hints["no_hex_prefix"])
            check_type(argname="argument partition_include_schema_table", value=partition_include_schema_table, expected_type=type_hints["partition_include_schema_table"])
            check_type(argname="argument sasl_mechanism", value=sasl_mechanism, expected_type=type_hints["sasl_mechanism"])
            check_type(argname="argument sasl_password", value=sasl_password, expected_type=type_hints["sasl_password"])
            check_type(argname="argument sasl_username", value=sasl_username, expected_type=type_hints["sasl_username"])
            check_type(argname="argument security_protocol", value=security_protocol, expected_type=type_hints["security_protocol"])
            check_type(argname="argument ssl_ca_certificate_arn", value=ssl_ca_certificate_arn, expected_type=type_hints["ssl_ca_certificate_arn"])
            check_type(argname="argument ssl_client_certificate_arn", value=ssl_client_certificate_arn, expected_type=type_hints["ssl_client_certificate_arn"])
            check_type(argname="argument ssl_client_key_arn", value=ssl_client_key_arn, expected_type=type_hints["ssl_client_key_arn"])
            check_type(argname="argument ssl_client_key_password", value=ssl_client_key_password, expected_type=type_hints["ssl_client_key_password"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "broker": broker,
        }
        if include_control_details is not None:
            self._values["include_control_details"] = include_control_details
        if include_null_and_empty is not None:
            self._values["include_null_and_empty"] = include_null_and_empty
        if include_partition_value is not None:
            self._values["include_partition_value"] = include_partition_value
        if include_table_alter_operations is not None:
            self._values["include_table_alter_operations"] = include_table_alter_operations
        if include_transaction_details is not None:
            self._values["include_transaction_details"] = include_transaction_details
        if message_format is not None:
            self._values["message_format"] = message_format
        if message_max_bytes is not None:
            self._values["message_max_bytes"] = message_max_bytes
        if no_hex_prefix is not None:
            self._values["no_hex_prefix"] = no_hex_prefix
        if partition_include_schema_table is not None:
            self._values["partition_include_schema_table"] = partition_include_schema_table
        if sasl_mechanism is not None:
            self._values["sasl_mechanism"] = sasl_mechanism
        if sasl_password is not None:
            self._values["sasl_password"] = sasl_password
        if sasl_username is not None:
            self._values["sasl_username"] = sasl_username
        if security_protocol is not None:
            self._values["security_protocol"] = security_protocol
        if ssl_ca_certificate_arn is not None:
            self._values["ssl_ca_certificate_arn"] = ssl_ca_certificate_arn
        if ssl_client_certificate_arn is not None:
            self._values["ssl_client_certificate_arn"] = ssl_client_certificate_arn
        if ssl_client_key_arn is not None:
            self._values["ssl_client_key_arn"] = ssl_client_key_arn
        if ssl_client_key_password is not None:
            self._values["ssl_client_key_password"] = ssl_client_key_password
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def broker(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#broker DmsEndpoint#broker}.'''
        result = self._values.get("broker")
        assert result is not None, "Required property 'broker' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_control_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_control_details DmsEndpoint#include_control_details}.'''
        result = self._values.get("include_control_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_null_and_empty(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_null_and_empty DmsEndpoint#include_null_and_empty}.'''
        result = self._values.get("include_null_and_empty")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_partition_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_partition_value DmsEndpoint#include_partition_value}.'''
        result = self._values.get("include_partition_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_table_alter_operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_table_alter_operations DmsEndpoint#include_table_alter_operations}.'''
        result = self._values.get("include_table_alter_operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_transaction_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_transaction_details DmsEndpoint#include_transaction_details}.'''
        result = self._values.get("include_transaction_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_format DmsEndpoint#message_format}.'''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_max_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_max_bytes DmsEndpoint#message_max_bytes}.'''
        result = self._values.get("message_max_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def no_hex_prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#no_hex_prefix DmsEndpoint#no_hex_prefix}.'''
        result = self._values.get("no_hex_prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def partition_include_schema_table(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#partition_include_schema_table DmsEndpoint#partition_include_schema_table}.'''
        result = self._values.get("partition_include_schema_table")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sasl_mechanism(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_mechanism DmsEndpoint#sasl_mechanism}.'''
        result = self._values.get("sasl_mechanism")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_password DmsEndpoint#sasl_password}.'''
        result = self._values.get("sasl_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sasl_username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#sasl_username DmsEndpoint#sasl_username}.'''
        result = self._values.get("sasl_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#security_protocol DmsEndpoint#security_protocol}.'''
        result = self._values.get("security_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_ca_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_ca_certificate_arn DmsEndpoint#ssl_ca_certificate_arn}.'''
        result = self._values.get("ssl_ca_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_client_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_certificate_arn DmsEndpoint#ssl_client_certificate_arn}.'''
        result = self._values.get("ssl_client_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_client_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_key_arn DmsEndpoint#ssl_client_key_arn}.'''
        result = self._values.get("ssl_client_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_client_key_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_client_key_password DmsEndpoint#ssl_client_key_password}.'''
        result = self._values.get("ssl_client_key_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#topic DmsEndpoint#topic}.'''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointKafkaSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointKafkaSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointKafkaSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f025d75cfb569d4b8998674a01d14fd5b0deb61a1eb1ddc6887de067d61a6726)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeControlDetails")
    def reset_include_control_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeControlDetails", []))

    @jsii.member(jsii_name="resetIncludeNullAndEmpty")
    def reset_include_null_and_empty(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeNullAndEmpty", []))

    @jsii.member(jsii_name="resetIncludePartitionValue")
    def reset_include_partition_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePartitionValue", []))

    @jsii.member(jsii_name="resetIncludeTableAlterOperations")
    def reset_include_table_alter_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTableAlterOperations", []))

    @jsii.member(jsii_name="resetIncludeTransactionDetails")
    def reset_include_transaction_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTransactionDetails", []))

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @jsii.member(jsii_name="resetMessageMaxBytes")
    def reset_message_max_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageMaxBytes", []))

    @jsii.member(jsii_name="resetNoHexPrefix")
    def reset_no_hex_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoHexPrefix", []))

    @jsii.member(jsii_name="resetPartitionIncludeSchemaTable")
    def reset_partition_include_schema_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionIncludeSchemaTable", []))

    @jsii.member(jsii_name="resetSaslMechanism")
    def reset_sasl_mechanism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslMechanism", []))

    @jsii.member(jsii_name="resetSaslPassword")
    def reset_sasl_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslPassword", []))

    @jsii.member(jsii_name="resetSaslUsername")
    def reset_sasl_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslUsername", []))

    @jsii.member(jsii_name="resetSecurityProtocol")
    def reset_security_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProtocol", []))

    @jsii.member(jsii_name="resetSslCaCertificateArn")
    def reset_ssl_ca_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCaCertificateArn", []))

    @jsii.member(jsii_name="resetSslClientCertificateArn")
    def reset_ssl_client_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslClientCertificateArn", []))

    @jsii.member(jsii_name="resetSslClientKeyArn")
    def reset_ssl_client_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslClientKeyArn", []))

    @jsii.member(jsii_name="resetSslClientKeyPassword")
    def reset_ssl_client_key_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslClientKeyPassword", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="brokerInput")
    def broker_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "brokerInput"))

    @builtins.property
    @jsii.member(jsii_name="includeControlDetailsInput")
    def include_control_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeControlDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeNullAndEmptyInput")
    def include_null_and_empty_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeNullAndEmptyInput"))

    @builtins.property
    @jsii.member(jsii_name="includePartitionValueInput")
    def include_partition_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includePartitionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTableAlterOperationsInput")
    def include_table_alter_operations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTableAlterOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTransactionDetailsInput")
    def include_transaction_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTransactionDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="messageMaxBytesInput")
    def message_max_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "messageMaxBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="noHexPrefixInput")
    def no_hex_prefix_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noHexPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionIncludeSchemaTableInput")
    def partition_include_schema_table_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "partitionIncludeSchemaTableInput"))

    @builtins.property
    @jsii.member(jsii_name="saslMechanismInput")
    def sasl_mechanism_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslMechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="saslPasswordInput")
    def sasl_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="saslUsernameInput")
    def sasl_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProtocolInput")
    def security_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateArnInput")
    def ssl_ca_certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaCertificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sslClientCertificateArnInput")
    def ssl_client_certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslClientCertificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sslClientKeyArnInput")
    def ssl_client_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslClientKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sslClientKeyPasswordInput")
    def ssl_client_key_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslClientKeyPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="broker")
    def broker(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "broker"))

    @broker.setter
    def broker(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983f5975bfa124c4e5014e1b9a7bd312bff3859b050bf5d595e2dc4aa92584c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "broker", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeControlDetails")
    def include_control_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeControlDetails"))

    @include_control_details.setter
    def include_control_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b554a07d86d35db83c71175f8cb44a4bcc33fc26ee0b7666072cb0714b038d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeControlDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNullAndEmpty")
    def include_null_and_empty(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeNullAndEmpty"))

    @include_null_and_empty.setter
    def include_null_and_empty(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1806090128f89cc12ff09dfe5c3a1208432d9c2f42ac81b3b3971ad394987b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeNullAndEmpty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePartitionValue")
    def include_partition_value(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includePartitionValue"))

    @include_partition_value.setter
    def include_partition_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75d66bba249a8a18ebc8758bd6570e6a66f8e9094200bff07d072c1d237247f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePartitionValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTableAlterOperations")
    def include_table_alter_operations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTableAlterOperations"))

    @include_table_alter_operations.setter
    def include_table_alter_operations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bd14900f33ec68f53748f88ce80e878e04ecfbe1e8dfad50f5ff4f8e95e544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTableAlterOperations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTransactionDetails")
    def include_transaction_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTransactionDetails"))

    @include_transaction_details.setter
    def include_transaction_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd3c730f6c8f8061e79b43ead35ff12cd9c5217a9e351751f78d769e3311bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTransactionDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904fafe50eca77090c2d171b86d032282eddcd0d0343bba89148e63a18b82221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageMaxBytes")
    def message_max_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "messageMaxBytes"))

    @message_max_bytes.setter
    def message_max_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa251cb4a0a272f6373097014268752913a292e49cbd8de49f33c6538344385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageMaxBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noHexPrefix")
    def no_hex_prefix(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noHexPrefix"))

    @no_hex_prefix.setter
    def no_hex_prefix(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90df562e067695228f6b66e9bda9309b8018a23d3c0e766310e6c2b4bd0cb8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHexPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionIncludeSchemaTable")
    def partition_include_schema_table(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "partitionIncludeSchemaTable"))

    @partition_include_schema_table.setter
    def partition_include_schema_table(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538b81ddac35c64061e6f7e163a3ae91fe98511d4a335a6fbb5362054c78061f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionIncludeSchemaTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslMechanism")
    def sasl_mechanism(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslMechanism"))

    @sasl_mechanism.setter
    def sasl_mechanism(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb6f67113292e1fb4f133fa44804de7d1a89f94536f6354a002ee31ce22938e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslMechanism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslPassword")
    def sasl_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslPassword"))

    @sasl_password.setter
    def sasl_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b092753bb755d5f16c4d2bdf425a935b2908c9c961f5c5b82bb60c00b578c972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslUsername")
    def sasl_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslUsername"))

    @sasl_username.setter
    def sasl_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae28a7328d50097d7212403cffa3e6681d92f617c2eae30195dc66c93ef4cb63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProtocol")
    def security_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProtocol"))

    @security_protocol.setter
    def security_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b70ddf8fb253e3753756042e5c03d952ebcd758d7ebdfca0e9535aefde74c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateArn")
    def ssl_ca_certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificateArn"))

    @ssl_ca_certificate_arn.setter
    def ssl_ca_certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ca6645c4c2d117c5a2ad5d891aade8ef14561f8bebc66766582675e043d1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslClientCertificateArn")
    def ssl_client_certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslClientCertificateArn"))

    @ssl_client_certificate_arn.setter
    def ssl_client_certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d9332142c6f728d0eddd39d1eea1321f9f4752c641ed5b8f411bdb8901bab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslClientCertificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslClientKeyArn")
    def ssl_client_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslClientKeyArn"))

    @ssl_client_key_arn.setter
    def ssl_client_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559a728992f63be2df5e88585272e03c1941f807cc990c50e6021dba000ef176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslClientKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslClientKeyPassword")
    def ssl_client_key_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslClientKeyPassword"))

    @ssl_client_key_password.setter
    def ssl_client_key_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8ccc44d56787d8402afc8e4823e7b74def31999af435aaddada416f82418d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslClientKeyPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac49684cf6fba772d54b390b5f3c9bebfaa40d1ddf863551e5c9164929bc34ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointKafkaSettings]:
        return typing.cast(typing.Optional[DmsEndpointKafkaSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DmsEndpointKafkaSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb9c5f6b7a1b8c0daf118224b0f0caf376d553bd91ec8e2cb73614d11cb1dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointKinesisSettings",
    jsii_struct_bases=[],
    name_mapping={
        "include_control_details": "includeControlDetails",
        "include_null_and_empty": "includeNullAndEmpty",
        "include_partition_value": "includePartitionValue",
        "include_table_alter_operations": "includeTableAlterOperations",
        "include_transaction_details": "includeTransactionDetails",
        "message_format": "messageFormat",
        "partition_include_schema_table": "partitionIncludeSchemaTable",
        "service_access_role_arn": "serviceAccessRoleArn",
        "stream_arn": "streamArn",
        "use_large_integer_value": "useLargeIntegerValue",
    },
)
class DmsEndpointKinesisSettings:
    def __init__(
        self,
        *,
        include_control_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_partition_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_transaction_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_format: typing.Optional[builtins.str] = None,
        partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        stream_arn: typing.Optional[builtins.str] = None,
        use_large_integer_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param include_control_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_control_details DmsEndpoint#include_control_details}.
        :param include_null_and_empty: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_null_and_empty DmsEndpoint#include_null_and_empty}.
        :param include_partition_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_partition_value DmsEndpoint#include_partition_value}.
        :param include_table_alter_operations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_table_alter_operations DmsEndpoint#include_table_alter_operations}.
        :param include_transaction_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_transaction_details DmsEndpoint#include_transaction_details}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_format DmsEndpoint#message_format}.
        :param partition_include_schema_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#partition_include_schema_table DmsEndpoint#partition_include_schema_table}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#stream_arn DmsEndpoint#stream_arn}.
        :param use_large_integer_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#use_large_integer_value DmsEndpoint#use_large_integer_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b1603904f76bde961fda96c7307bc5ba4881b8bfe458d4797edf06955ad312)
            check_type(argname="argument include_control_details", value=include_control_details, expected_type=type_hints["include_control_details"])
            check_type(argname="argument include_null_and_empty", value=include_null_and_empty, expected_type=type_hints["include_null_and_empty"])
            check_type(argname="argument include_partition_value", value=include_partition_value, expected_type=type_hints["include_partition_value"])
            check_type(argname="argument include_table_alter_operations", value=include_table_alter_operations, expected_type=type_hints["include_table_alter_operations"])
            check_type(argname="argument include_transaction_details", value=include_transaction_details, expected_type=type_hints["include_transaction_details"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
            check_type(argname="argument partition_include_schema_table", value=partition_include_schema_table, expected_type=type_hints["partition_include_schema_table"])
            check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            check_type(argname="argument use_large_integer_value", value=use_large_integer_value, expected_type=type_hints["use_large_integer_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_control_details is not None:
            self._values["include_control_details"] = include_control_details
        if include_null_and_empty is not None:
            self._values["include_null_and_empty"] = include_null_and_empty
        if include_partition_value is not None:
            self._values["include_partition_value"] = include_partition_value
        if include_table_alter_operations is not None:
            self._values["include_table_alter_operations"] = include_table_alter_operations
        if include_transaction_details is not None:
            self._values["include_transaction_details"] = include_transaction_details
        if message_format is not None:
            self._values["message_format"] = message_format
        if partition_include_schema_table is not None:
            self._values["partition_include_schema_table"] = partition_include_schema_table
        if service_access_role_arn is not None:
            self._values["service_access_role_arn"] = service_access_role_arn
        if stream_arn is not None:
            self._values["stream_arn"] = stream_arn
        if use_large_integer_value is not None:
            self._values["use_large_integer_value"] = use_large_integer_value

    @builtins.property
    def include_control_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_control_details DmsEndpoint#include_control_details}.'''
        result = self._values.get("include_control_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_null_and_empty(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_null_and_empty DmsEndpoint#include_null_and_empty}.'''
        result = self._values.get("include_null_and_empty")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_partition_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_partition_value DmsEndpoint#include_partition_value}.'''
        result = self._values.get("include_partition_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_table_alter_operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_table_alter_operations DmsEndpoint#include_table_alter_operations}.'''
        result = self._values.get("include_table_alter_operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_transaction_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#include_transaction_details DmsEndpoint#include_transaction_details}.'''
        result = self._values.get("include_transaction_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#message_format DmsEndpoint#message_format}.'''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_include_schema_table(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#partition_include_schema_table DmsEndpoint#partition_include_schema_table}.'''
        result = self._values.get("partition_include_schema_table")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.'''
        result = self._values.get("service_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#stream_arn DmsEndpoint#stream_arn}.'''
        result = self._values.get("stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_large_integer_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#use_large_integer_value DmsEndpoint#use_large_integer_value}.'''
        result = self._values.get("use_large_integer_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointKinesisSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointKinesisSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointKinesisSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__957ae377877e01f5ff11db44397f76c0b2c1d446f5f60ffc94432f4ca3319517)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeControlDetails")
    def reset_include_control_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeControlDetails", []))

    @jsii.member(jsii_name="resetIncludeNullAndEmpty")
    def reset_include_null_and_empty(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeNullAndEmpty", []))

    @jsii.member(jsii_name="resetIncludePartitionValue")
    def reset_include_partition_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludePartitionValue", []))

    @jsii.member(jsii_name="resetIncludeTableAlterOperations")
    def reset_include_table_alter_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTableAlterOperations", []))

    @jsii.member(jsii_name="resetIncludeTransactionDetails")
    def reset_include_transaction_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTransactionDetails", []))

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @jsii.member(jsii_name="resetPartitionIncludeSchemaTable")
    def reset_partition_include_schema_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionIncludeSchemaTable", []))

    @jsii.member(jsii_name="resetServiceAccessRoleArn")
    def reset_service_access_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccessRoleArn", []))

    @jsii.member(jsii_name="resetStreamArn")
    def reset_stream_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamArn", []))

    @jsii.member(jsii_name="resetUseLargeIntegerValue")
    def reset_use_large_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLargeIntegerValue", []))

    @builtins.property
    @jsii.member(jsii_name="includeControlDetailsInput")
    def include_control_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeControlDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeNullAndEmptyInput")
    def include_null_and_empty_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeNullAndEmptyInput"))

    @builtins.property
    @jsii.member(jsii_name="includePartitionValueInput")
    def include_partition_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includePartitionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTableAlterOperationsInput")
    def include_table_alter_operations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTableAlterOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTransactionDetailsInput")
    def include_transaction_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTransactionDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionIncludeSchemaTableInput")
    def partition_include_schema_table_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "partitionIncludeSchemaTableInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArnInput")
    def service_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamArnInput")
    def stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="useLargeIntegerValueInput")
    def use_large_integer_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLargeIntegerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="includeControlDetails")
    def include_control_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeControlDetails"))

    @include_control_details.setter
    def include_control_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ee432def92209ad48889acd665a506b0e0e91d2be2dcadd7182a2a159cabec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeControlDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNullAndEmpty")
    def include_null_and_empty(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeNullAndEmpty"))

    @include_null_and_empty.setter
    def include_null_and_empty(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc72ed37cb717dadc0943e30b110f711e73d4d120368f913b7821c384691a557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeNullAndEmpty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePartitionValue")
    def include_partition_value(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includePartitionValue"))

    @include_partition_value.setter
    def include_partition_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c7203cc0289fcdb69d73aa345f68b9c134452c60373596373c90352d2195ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePartitionValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTableAlterOperations")
    def include_table_alter_operations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTableAlterOperations"))

    @include_table_alter_operations.setter
    def include_table_alter_operations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b4a6c702864b88fa6e2bb52cb74d6ff278d8627c624eaca55fbb17678707c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTableAlterOperations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTransactionDetails")
    def include_transaction_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTransactionDetails"))

    @include_transaction_details.setter
    def include_transaction_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea183c3946437ac5082d702b06ad99936d90b5c815ad301b751d9d0232ff352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTransactionDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791d42ee49983b1ba1ed1e9ad54c11ba1d6fa2e14e391e0723c0fd2094cd59dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionIncludeSchemaTable")
    def partition_include_schema_table(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "partitionIncludeSchemaTable"))

    @partition_include_schema_table.setter
    def partition_include_schema_table(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5207b7c857c7a0b7ad3006fc0b18bac8796f71f01fa7a8ca50d92cbd8cd7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionIncludeSchemaTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccessRoleArn"))

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbc73b808a7c74b2723f0bf72790dca988954dee86cc76a65a39303498a1e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @stream_arn.setter
    def stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0011f0e935f495dffca145d2a3f8e10af6bbe353953d94ff82ad87ebceabe485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLargeIntegerValue")
    def use_large_integer_value(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useLargeIntegerValue"))

    @use_large_integer_value.setter
    def use_large_integer_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e71e25b19bd9e50e002dd6af70b7bed3e94179b82ec15eaf433e85025a42ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLargeIntegerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointKinesisSettings]:
        return typing.cast(typing.Optional[DmsEndpointKinesisSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsEndpointKinesisSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360bf155de9eae35975801f65b1917c05f8831cefff7c62bb47cf594a6e4f0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointMongodbSettings",
    jsii_struct_bases=[],
    name_mapping={
        "auth_mechanism": "authMechanism",
        "auth_source": "authSource",
        "auth_type": "authType",
        "docs_to_investigate": "docsToInvestigate",
        "extract_doc_id": "extractDocId",
        "nesting_level": "nestingLevel",
    },
)
class DmsEndpointMongodbSettings:
    def __init__(
        self,
        *,
        auth_mechanism: typing.Optional[builtins.str] = None,
        auth_source: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        docs_to_investigate: typing.Optional[builtins.str] = None,
        extract_doc_id: typing.Optional[builtins.str] = None,
        nesting_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_mechanism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_mechanism DmsEndpoint#auth_mechanism}.
        :param auth_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_source DmsEndpoint#auth_source}.
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_type DmsEndpoint#auth_type}.
        :param docs_to_investigate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#docs_to_investigate DmsEndpoint#docs_to_investigate}.
        :param extract_doc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#extract_doc_id DmsEndpoint#extract_doc_id}.
        :param nesting_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#nesting_level DmsEndpoint#nesting_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa47d92ed2a40aad2d1ab9655f01e12689c2bb7650142fe12e7e80c04eedc02f)
            check_type(argname="argument auth_mechanism", value=auth_mechanism, expected_type=type_hints["auth_mechanism"])
            check_type(argname="argument auth_source", value=auth_source, expected_type=type_hints["auth_source"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument docs_to_investigate", value=docs_to_investigate, expected_type=type_hints["docs_to_investigate"])
            check_type(argname="argument extract_doc_id", value=extract_doc_id, expected_type=type_hints["extract_doc_id"])
            check_type(argname="argument nesting_level", value=nesting_level, expected_type=type_hints["nesting_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_mechanism is not None:
            self._values["auth_mechanism"] = auth_mechanism
        if auth_source is not None:
            self._values["auth_source"] = auth_source
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if docs_to_investigate is not None:
            self._values["docs_to_investigate"] = docs_to_investigate
        if extract_doc_id is not None:
            self._values["extract_doc_id"] = extract_doc_id
        if nesting_level is not None:
            self._values["nesting_level"] = nesting_level

    @builtins.property
    def auth_mechanism(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_mechanism DmsEndpoint#auth_mechanism}.'''
        result = self._values.get("auth_mechanism")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_source DmsEndpoint#auth_source}.'''
        result = self._values.get("auth_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_type DmsEndpoint#auth_type}.'''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docs_to_investigate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#docs_to_investigate DmsEndpoint#docs_to_investigate}.'''
        result = self._values.get("docs_to_investigate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extract_doc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#extract_doc_id DmsEndpoint#extract_doc_id}.'''
        result = self._values.get("extract_doc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nesting_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#nesting_level DmsEndpoint#nesting_level}.'''
        result = self._values.get("nesting_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointMongodbSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointMongodbSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointMongodbSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bd8267ca2131f95b789c5601c74790cfc8670b8f9364447a73585bf68eb207c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthMechanism")
    def reset_auth_mechanism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMechanism", []))

    @jsii.member(jsii_name="resetAuthSource")
    def reset_auth_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthSource", []))

    @jsii.member(jsii_name="resetAuthType")
    def reset_auth_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthType", []))

    @jsii.member(jsii_name="resetDocsToInvestigate")
    def reset_docs_to_investigate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocsToInvestigate", []))

    @jsii.member(jsii_name="resetExtractDocId")
    def reset_extract_doc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtractDocId", []))

    @jsii.member(jsii_name="resetNestingLevel")
    def reset_nesting_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNestingLevel", []))

    @builtins.property
    @jsii.member(jsii_name="authMechanismInput")
    def auth_mechanism_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="authSourceInput")
    def auth_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="docsToInvestigateInput")
    def docs_to_investigate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "docsToInvestigateInput"))

    @builtins.property
    @jsii.member(jsii_name="extractDocIdInput")
    def extract_doc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extractDocIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nestingLevelInput")
    def nesting_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nestingLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="authMechanism")
    def auth_mechanism(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMechanism"))

    @auth_mechanism.setter
    def auth_mechanism(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ebd8e8bd1af4a55e7f289ac54d6e6b3904b8476f8375b3c393e3d51dd7cc99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMechanism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authSource")
    def auth_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authSource"))

    @auth_source.setter
    def auth_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f5fd3e6486bddd234e6108b13dafce16e4e05ef397cb70daf4ed2322c1c967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061cc32e180f7f08511bd25c415a70de0698f291e5d3253e6cba934849081e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="docsToInvestigate")
    def docs_to_investigate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "docsToInvestigate"))

    @docs_to_investigate.setter
    def docs_to_investigate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0058003c58d76aec9767ed880f78308fd54d24e0a6df840e0ab4cc571251f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "docsToInvestigate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extractDocId")
    def extract_doc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extractDocId"))

    @extract_doc_id.setter
    def extract_doc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f822cd6e466844f9c79f0ca2ff6434e659991b10e819fd3628c7d785544d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extractDocId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nestingLevel")
    def nesting_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nestingLevel"))

    @nesting_level.setter
    def nesting_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868afaba143788a4aaaa6bb2992d2cf1378c836bdd1d11793f613f0cc024123b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nestingLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointMongodbSettings]:
        return typing.cast(typing.Optional[DmsEndpointMongodbSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsEndpointMongodbSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1180f9cb7605a47356a201c17301e771ecfbf9782c0d2c958a270734bd9501d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointMysqlSettings",
    jsii_struct_bases=[],
    name_mapping={
        "after_connect_script": "afterConnectScript",
        "authentication_method": "authenticationMethod",
        "clean_source_metadata_on_mismatch": "cleanSourceMetadataOnMismatch",
        "events_poll_interval": "eventsPollInterval",
        "execute_timeout": "executeTimeout",
        "max_file_size": "maxFileSize",
        "parallel_load_threads": "parallelLoadThreads",
        "server_timezone": "serverTimezone",
        "service_access_role_arn": "serviceAccessRoleArn",
        "target_db_type": "targetDbType",
    },
)
class DmsEndpointMysqlSettings:
    def __init__(
        self,
        *,
        after_connect_script: typing.Optional[builtins.str] = None,
        authentication_method: typing.Optional[builtins.str] = None,
        clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events_poll_interval: typing.Optional[jsii.Number] = None,
        execute_timeout: typing.Optional[jsii.Number] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        parallel_load_threads: typing.Optional[jsii.Number] = None,
        server_timezone: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        target_db_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param after_connect_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#after_connect_script DmsEndpoint#after_connect_script}.
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.
        :param clean_source_metadata_on_mismatch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#clean_source_metadata_on_mismatch DmsEndpoint#clean_source_metadata_on_mismatch}.
        :param events_poll_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#events_poll_interval DmsEndpoint#events_poll_interval}.
        :param execute_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#execute_timeout DmsEndpoint#execute_timeout}.
        :param max_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#max_file_size DmsEndpoint#max_file_size}.
        :param parallel_load_threads: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#parallel_load_threads DmsEndpoint#parallel_load_threads}.
        :param server_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_timezone DmsEndpoint#server_timezone}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param target_db_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#target_db_type DmsEndpoint#target_db_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8a042e25c91268a6f7985e9b80798823264ef6fff72eaa010048b60ab9be39)
            check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
            check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
            check_type(argname="argument clean_source_metadata_on_mismatch", value=clean_source_metadata_on_mismatch, expected_type=type_hints["clean_source_metadata_on_mismatch"])
            check_type(argname="argument events_poll_interval", value=events_poll_interval, expected_type=type_hints["events_poll_interval"])
            check_type(argname="argument execute_timeout", value=execute_timeout, expected_type=type_hints["execute_timeout"])
            check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
            check_type(argname="argument parallel_load_threads", value=parallel_load_threads, expected_type=type_hints["parallel_load_threads"])
            check_type(argname="argument server_timezone", value=server_timezone, expected_type=type_hints["server_timezone"])
            check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            check_type(argname="argument target_db_type", value=target_db_type, expected_type=type_hints["target_db_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if after_connect_script is not None:
            self._values["after_connect_script"] = after_connect_script
        if authentication_method is not None:
            self._values["authentication_method"] = authentication_method
        if clean_source_metadata_on_mismatch is not None:
            self._values["clean_source_metadata_on_mismatch"] = clean_source_metadata_on_mismatch
        if events_poll_interval is not None:
            self._values["events_poll_interval"] = events_poll_interval
        if execute_timeout is not None:
            self._values["execute_timeout"] = execute_timeout
        if max_file_size is not None:
            self._values["max_file_size"] = max_file_size
        if parallel_load_threads is not None:
            self._values["parallel_load_threads"] = parallel_load_threads
        if server_timezone is not None:
            self._values["server_timezone"] = server_timezone
        if service_access_role_arn is not None:
            self._values["service_access_role_arn"] = service_access_role_arn
        if target_db_type is not None:
            self._values["target_db_type"] = target_db_type

    @builtins.property
    def after_connect_script(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#after_connect_script DmsEndpoint#after_connect_script}.'''
        result = self._values.get("after_connect_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.'''
        result = self._values.get("authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clean_source_metadata_on_mismatch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#clean_source_metadata_on_mismatch DmsEndpoint#clean_source_metadata_on_mismatch}.'''
        result = self._values.get("clean_source_metadata_on_mismatch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def events_poll_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#events_poll_interval DmsEndpoint#events_poll_interval}.'''
        result = self._values.get("events_poll_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def execute_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#execute_timeout DmsEndpoint#execute_timeout}.'''
        result = self._values.get("execute_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_file_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#max_file_size DmsEndpoint#max_file_size}.'''
        result = self._values.get("max_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parallel_load_threads(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#parallel_load_threads DmsEndpoint#parallel_load_threads}.'''
        result = self._values.get("parallel_load_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_timezone DmsEndpoint#server_timezone}.'''
        result = self._values.get("server_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.'''
        result = self._values.get("service_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_db_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#target_db_type DmsEndpoint#target_db_type}.'''
        result = self._values.get("target_db_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointMysqlSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointMysqlSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointMysqlSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__688658782d483136eb50e65cc9d8b32ec6491924379e879fafd1f456a61faa93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAfterConnectScript")
    def reset_after_connect_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAfterConnectScript", []))

    @jsii.member(jsii_name="resetAuthenticationMethod")
    def reset_authentication_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMethod", []))

    @jsii.member(jsii_name="resetCleanSourceMetadataOnMismatch")
    def reset_clean_source_metadata_on_mismatch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCleanSourceMetadataOnMismatch", []))

    @jsii.member(jsii_name="resetEventsPollInterval")
    def reset_events_poll_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventsPollInterval", []))

    @jsii.member(jsii_name="resetExecuteTimeout")
    def reset_execute_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteTimeout", []))

    @jsii.member(jsii_name="resetMaxFileSize")
    def reset_max_file_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFileSize", []))

    @jsii.member(jsii_name="resetParallelLoadThreads")
    def reset_parallel_load_threads(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelLoadThreads", []))

    @jsii.member(jsii_name="resetServerTimezone")
    def reset_server_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerTimezone", []))

    @jsii.member(jsii_name="resetServiceAccessRoleArn")
    def reset_service_access_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccessRoleArn", []))

    @jsii.member(jsii_name="resetTargetDbType")
    def reset_target_db_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDbType", []))

    @builtins.property
    @jsii.member(jsii_name="afterConnectScriptInput")
    def after_connect_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "afterConnectScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethodInput")
    def authentication_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="cleanSourceMetadataOnMismatchInput")
    def clean_source_metadata_on_mismatch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cleanSourceMetadataOnMismatchInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsPollIntervalInput")
    def events_poll_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "eventsPollIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="executeTimeoutInput")
    def execute_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executeTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFileSizeInput")
    def max_file_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFileSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelLoadThreadsInput")
    def parallel_load_threads_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelLoadThreadsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTimezoneInput")
    def server_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArnInput")
    def service_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDbTypeInput")
    def target_db_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDbTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="afterConnectScript")
    def after_connect_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "afterConnectScript"))

    @after_connect_script.setter
    def after_connect_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1c04b588f6d0668903452aa8c00c713648b8a5e1885238d975002808a9ced5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "afterConnectScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationMethod")
    def authentication_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMethod"))

    @authentication_method.setter
    def authentication_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06bda059913599dbeabba665495118c29e94e97b3968e5f9479f601a4e60e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cleanSourceMetadataOnMismatch")
    def clean_source_metadata_on_mismatch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cleanSourceMetadataOnMismatch"))

    @clean_source_metadata_on_mismatch.setter
    def clean_source_metadata_on_mismatch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fd7d750f08658ecb0b07ab031a54f0c5194b3b5ef72992b8d41cb7e056db55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cleanSourceMetadataOnMismatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventsPollInterval")
    def events_poll_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eventsPollInterval"))

    @events_poll_interval.setter
    def events_poll_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413f7e483a3d40c0ca047dfe83043769581f626c43cc34544ae9a395ca10e3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventsPollInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executeTimeout")
    def execute_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executeTimeout"))

    @execute_timeout.setter
    def execute_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597cb43837c55ade81abe1e1cda967ea41233500f538de6d2c382df66f03c215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFileSize")
    def max_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFileSize"))

    @max_file_size.setter
    def max_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341f827e552be0ccebc15b258cd174738d314c2803faeb6447ecb850199e2483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFileSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelLoadThreads")
    def parallel_load_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelLoadThreads"))

    @parallel_load_threads.setter
    def parallel_load_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59fb4489b6e9ce54e92bb9f4bf61e58ce92dc4cb02e6b31c7a970b4329b02b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelLoadThreads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverTimezone")
    def server_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverTimezone"))

    @server_timezone.setter
    def server_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc4f540b6f48e4525e5546e0df9c6bd6b4023c5fd7e2c0a632679addcf2f847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccessRoleArn"))

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b965b9e3bd2c9d9417b02f75f11238cd63970df8a6b596ab7afd83c9c405d49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDbType")
    def target_db_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDbType"))

    @target_db_type.setter
    def target_db_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb3fb9cab56e687a0678333fe756129936425bb0c37267fc4ce672273f8ab2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDbType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointMysqlSettings]:
        return typing.cast(typing.Optional[DmsEndpointMysqlSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DmsEndpointMysqlSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1bd31a99f986b75749bff2f4cbdc0c57ba61fdc5313c9f46328935d06b2957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointOracleSettings",
    jsii_struct_bases=[],
    name_mapping={"authentication_method": "authenticationMethod"},
)
class DmsEndpointOracleSettings:
    def __init__(
        self,
        *,
        authentication_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1885b6ca06a07065461896d8c4b48bb8e0377e761a57f0219c398065dd9a6f7)
            check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_method is not None:
            self._values["authentication_method"] = authentication_method

    @builtins.property
    def authentication_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.'''
        result = self._values.get("authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointOracleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointOracleSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointOracleSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af6a59b91a1dbc40e796c9e9fa70c55cb6a514cecb3e891f7a6e85ec962f8652)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationMethod")
    def reset_authentication_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMethod", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethodInput")
    def authentication_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethod")
    def authentication_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMethod"))

    @authentication_method.setter
    def authentication_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5a447ddc913283626168a2dda24331b96d27a19cd0e46747aaa5ec73ecbf52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointOracleSettings]:
        return typing.cast(typing.Optional[DmsEndpointOracleSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DmsEndpointOracleSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6287d565035d1d8b800b8656c290545d2a2fc186d1c26ff8697655ea91d290b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointPostgresSettings",
    jsii_struct_bases=[],
    name_mapping={
        "after_connect_script": "afterConnectScript",
        "authentication_method": "authenticationMethod",
        "babelfish_database_name": "babelfishDatabaseName",
        "capture_ddls": "captureDdls",
        "database_mode": "databaseMode",
        "ddl_artifacts_schema": "ddlArtifactsSchema",
        "execute_timeout": "executeTimeout",
        "fail_tasks_on_lob_truncation": "failTasksOnLobTruncation",
        "heartbeat_enable": "heartbeatEnable",
        "heartbeat_frequency": "heartbeatFrequency",
        "heartbeat_schema": "heartbeatSchema",
        "map_boolean_as_boolean": "mapBooleanAsBoolean",
        "map_jsonb_as_clob": "mapJsonbAsClob",
        "map_long_varchar_as": "mapLongVarcharAs",
        "max_file_size": "maxFileSize",
        "plugin_name": "pluginName",
        "service_access_role_arn": "serviceAccessRoleArn",
        "slot_name": "slotName",
    },
)
class DmsEndpointPostgresSettings:
    def __init__(
        self,
        *,
        after_connect_script: typing.Optional[builtins.str] = None,
        authentication_method: typing.Optional[builtins.str] = None,
        babelfish_database_name: typing.Optional[builtins.str] = None,
        capture_ddls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        database_mode: typing.Optional[builtins.str] = None,
        ddl_artifacts_schema: typing.Optional[builtins.str] = None,
        execute_timeout: typing.Optional[jsii.Number] = None,
        fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        heartbeat_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        heartbeat_frequency: typing.Optional[jsii.Number] = None,
        heartbeat_schema: typing.Optional[builtins.str] = None,
        map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_jsonb_as_clob: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_long_varchar_as: typing.Optional[builtins.str] = None,
        max_file_size: typing.Optional[jsii.Number] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
        slot_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param after_connect_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#after_connect_script DmsEndpoint#after_connect_script}.
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.
        :param babelfish_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#babelfish_database_name DmsEndpoint#babelfish_database_name}.
        :param capture_ddls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#capture_ddls DmsEndpoint#capture_ddls}.
        :param database_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#database_mode DmsEndpoint#database_mode}.
        :param ddl_artifacts_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ddl_artifacts_schema DmsEndpoint#ddl_artifacts_schema}.
        :param execute_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#execute_timeout DmsEndpoint#execute_timeout}.
        :param fail_tasks_on_lob_truncation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#fail_tasks_on_lob_truncation DmsEndpoint#fail_tasks_on_lob_truncation}.
        :param heartbeat_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_enable DmsEndpoint#heartbeat_enable}.
        :param heartbeat_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_frequency DmsEndpoint#heartbeat_frequency}.
        :param heartbeat_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_schema DmsEndpoint#heartbeat_schema}.
        :param map_boolean_as_boolean: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_boolean_as_boolean DmsEndpoint#map_boolean_as_boolean}.
        :param map_jsonb_as_clob: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_jsonb_as_clob DmsEndpoint#map_jsonb_as_clob}.
        :param map_long_varchar_as: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_long_varchar_as DmsEndpoint#map_long_varchar_as}.
        :param max_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#max_file_size DmsEndpoint#max_file_size}.
        :param plugin_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#plugin_name DmsEndpoint#plugin_name}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        :param slot_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#slot_name DmsEndpoint#slot_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e69b81228b21e6646e58c724e16464d9d76ff1c863612942c5fae83a7055bb6)
            check_type(argname="argument after_connect_script", value=after_connect_script, expected_type=type_hints["after_connect_script"])
            check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
            check_type(argname="argument babelfish_database_name", value=babelfish_database_name, expected_type=type_hints["babelfish_database_name"])
            check_type(argname="argument capture_ddls", value=capture_ddls, expected_type=type_hints["capture_ddls"])
            check_type(argname="argument database_mode", value=database_mode, expected_type=type_hints["database_mode"])
            check_type(argname="argument ddl_artifacts_schema", value=ddl_artifacts_schema, expected_type=type_hints["ddl_artifacts_schema"])
            check_type(argname="argument execute_timeout", value=execute_timeout, expected_type=type_hints["execute_timeout"])
            check_type(argname="argument fail_tasks_on_lob_truncation", value=fail_tasks_on_lob_truncation, expected_type=type_hints["fail_tasks_on_lob_truncation"])
            check_type(argname="argument heartbeat_enable", value=heartbeat_enable, expected_type=type_hints["heartbeat_enable"])
            check_type(argname="argument heartbeat_frequency", value=heartbeat_frequency, expected_type=type_hints["heartbeat_frequency"])
            check_type(argname="argument heartbeat_schema", value=heartbeat_schema, expected_type=type_hints["heartbeat_schema"])
            check_type(argname="argument map_boolean_as_boolean", value=map_boolean_as_boolean, expected_type=type_hints["map_boolean_as_boolean"])
            check_type(argname="argument map_jsonb_as_clob", value=map_jsonb_as_clob, expected_type=type_hints["map_jsonb_as_clob"])
            check_type(argname="argument map_long_varchar_as", value=map_long_varchar_as, expected_type=type_hints["map_long_varchar_as"])
            check_type(argname="argument max_file_size", value=max_file_size, expected_type=type_hints["max_file_size"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
            check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if after_connect_script is not None:
            self._values["after_connect_script"] = after_connect_script
        if authentication_method is not None:
            self._values["authentication_method"] = authentication_method
        if babelfish_database_name is not None:
            self._values["babelfish_database_name"] = babelfish_database_name
        if capture_ddls is not None:
            self._values["capture_ddls"] = capture_ddls
        if database_mode is not None:
            self._values["database_mode"] = database_mode
        if ddl_artifacts_schema is not None:
            self._values["ddl_artifacts_schema"] = ddl_artifacts_schema
        if execute_timeout is not None:
            self._values["execute_timeout"] = execute_timeout
        if fail_tasks_on_lob_truncation is not None:
            self._values["fail_tasks_on_lob_truncation"] = fail_tasks_on_lob_truncation
        if heartbeat_enable is not None:
            self._values["heartbeat_enable"] = heartbeat_enable
        if heartbeat_frequency is not None:
            self._values["heartbeat_frequency"] = heartbeat_frequency
        if heartbeat_schema is not None:
            self._values["heartbeat_schema"] = heartbeat_schema
        if map_boolean_as_boolean is not None:
            self._values["map_boolean_as_boolean"] = map_boolean_as_boolean
        if map_jsonb_as_clob is not None:
            self._values["map_jsonb_as_clob"] = map_jsonb_as_clob
        if map_long_varchar_as is not None:
            self._values["map_long_varchar_as"] = map_long_varchar_as
        if max_file_size is not None:
            self._values["max_file_size"] = max_file_size
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if service_access_role_arn is not None:
            self._values["service_access_role_arn"] = service_access_role_arn
        if slot_name is not None:
            self._values["slot_name"] = slot_name

    @builtins.property
    def after_connect_script(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#after_connect_script DmsEndpoint#after_connect_script}.'''
        result = self._values.get("after_connect_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#authentication_method DmsEndpoint#authentication_method}.'''
        result = self._values.get("authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def babelfish_database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#babelfish_database_name DmsEndpoint#babelfish_database_name}.'''
        result = self._values.get("babelfish_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capture_ddls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#capture_ddls DmsEndpoint#capture_ddls}.'''
        result = self._values.get("capture_ddls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def database_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#database_mode DmsEndpoint#database_mode}.'''
        result = self._values.get("database_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ddl_artifacts_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ddl_artifacts_schema DmsEndpoint#ddl_artifacts_schema}.'''
        result = self._values.get("ddl_artifacts_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#execute_timeout DmsEndpoint#execute_timeout}.'''
        result = self._values.get("execute_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fail_tasks_on_lob_truncation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#fail_tasks_on_lob_truncation DmsEndpoint#fail_tasks_on_lob_truncation}.'''
        result = self._values.get("fail_tasks_on_lob_truncation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def heartbeat_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_enable DmsEndpoint#heartbeat_enable}.'''
        result = self._values.get("heartbeat_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def heartbeat_frequency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_frequency DmsEndpoint#heartbeat_frequency}.'''
        result = self._values.get("heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def heartbeat_schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#heartbeat_schema DmsEndpoint#heartbeat_schema}.'''
        result = self._values.get("heartbeat_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def map_boolean_as_boolean(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_boolean_as_boolean DmsEndpoint#map_boolean_as_boolean}.'''
        result = self._values.get("map_boolean_as_boolean")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_jsonb_as_clob(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_jsonb_as_clob DmsEndpoint#map_jsonb_as_clob}.'''
        result = self._values.get("map_jsonb_as_clob")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_long_varchar_as(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#map_long_varchar_as DmsEndpoint#map_long_varchar_as}.'''
        result = self._values.get("map_long_varchar_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_file_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#max_file_size DmsEndpoint#max_file_size}.'''
        result = self._values.get("max_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#plugin_name DmsEndpoint#plugin_name}.'''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.'''
        result = self._values.get("service_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slot_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#slot_name DmsEndpoint#slot_name}.'''
        result = self._values.get("slot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointPostgresSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointPostgresSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointPostgresSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4240d56f2d196f9de89dff6a494381666cdc6a09778a24e3af595ec606ea6a2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAfterConnectScript")
    def reset_after_connect_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAfterConnectScript", []))

    @jsii.member(jsii_name="resetAuthenticationMethod")
    def reset_authentication_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMethod", []))

    @jsii.member(jsii_name="resetBabelfishDatabaseName")
    def reset_babelfish_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBabelfishDatabaseName", []))

    @jsii.member(jsii_name="resetCaptureDdls")
    def reset_capture_ddls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptureDdls", []))

    @jsii.member(jsii_name="resetDatabaseMode")
    def reset_database_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseMode", []))

    @jsii.member(jsii_name="resetDdlArtifactsSchema")
    def reset_ddl_artifacts_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDdlArtifactsSchema", []))

    @jsii.member(jsii_name="resetExecuteTimeout")
    def reset_execute_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteTimeout", []))

    @jsii.member(jsii_name="resetFailTasksOnLobTruncation")
    def reset_fail_tasks_on_lob_truncation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailTasksOnLobTruncation", []))

    @jsii.member(jsii_name="resetHeartbeatEnable")
    def reset_heartbeat_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeartbeatEnable", []))

    @jsii.member(jsii_name="resetHeartbeatFrequency")
    def reset_heartbeat_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeartbeatFrequency", []))

    @jsii.member(jsii_name="resetHeartbeatSchema")
    def reset_heartbeat_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeartbeatSchema", []))

    @jsii.member(jsii_name="resetMapBooleanAsBoolean")
    def reset_map_boolean_as_boolean(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapBooleanAsBoolean", []))

    @jsii.member(jsii_name="resetMapJsonbAsClob")
    def reset_map_jsonb_as_clob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapJsonbAsClob", []))

    @jsii.member(jsii_name="resetMapLongVarcharAs")
    def reset_map_long_varchar_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapLongVarcharAs", []))

    @jsii.member(jsii_name="resetMaxFileSize")
    def reset_max_file_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFileSize", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetServiceAccessRoleArn")
    def reset_service_access_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccessRoleArn", []))

    @jsii.member(jsii_name="resetSlotName")
    def reset_slot_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlotName", []))

    @builtins.property
    @jsii.member(jsii_name="afterConnectScriptInput")
    def after_connect_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "afterConnectScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethodInput")
    def authentication_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="babelfishDatabaseNameInput")
    def babelfish_database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "babelfishDatabaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="captureDdlsInput")
    def capture_ddls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "captureDdlsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseModeInput")
    def database_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseModeInput"))

    @builtins.property
    @jsii.member(jsii_name="ddlArtifactsSchemaInput")
    def ddl_artifacts_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ddlArtifactsSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="executeTimeoutInput")
    def execute_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executeTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="failTasksOnLobTruncationInput")
    def fail_tasks_on_lob_truncation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failTasksOnLobTruncationInput"))

    @builtins.property
    @jsii.member(jsii_name="heartbeatEnableInput")
    def heartbeat_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "heartbeatEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="heartbeatFrequencyInput")
    def heartbeat_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heartbeatFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="heartbeatSchemaInput")
    def heartbeat_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "heartbeatSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="mapBooleanAsBooleanInput")
    def map_boolean_as_boolean_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mapBooleanAsBooleanInput"))

    @builtins.property
    @jsii.member(jsii_name="mapJsonbAsClobInput")
    def map_jsonb_as_clob_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mapJsonbAsClobInput"))

    @builtins.property
    @jsii.member(jsii_name="mapLongVarcharAsInput")
    def map_long_varchar_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mapLongVarcharAsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFileSizeInput")
    def max_file_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFileSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArnInput")
    def service_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="slotNameInput")
    def slot_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slotNameInput"))

    @builtins.property
    @jsii.member(jsii_name="afterConnectScript")
    def after_connect_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "afterConnectScript"))

    @after_connect_script.setter
    def after_connect_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dec6e8ed671bc1cad9bd50ef2c46c3d94617812fb4e7e3e8e40a76a90388abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "afterConnectScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationMethod")
    def authentication_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMethod"))

    @authentication_method.setter
    def authentication_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5006a5c2a250734785afc40b3521d8eb7127dc26a0d3524196f86e890711dad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="babelfishDatabaseName")
    def babelfish_database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "babelfishDatabaseName"))

    @babelfish_database_name.setter
    def babelfish_database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8943bbbcf3a5e55fe104c3213ee97dc83a5a7750f64e699c73f2f81e7376c884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "babelfishDatabaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="captureDdls")
    def capture_ddls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "captureDdls"))

    @capture_ddls.setter
    def capture_ddls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e58907c06f90385d4ebb6ef19908f582fa7c197e78f3b8efebb5a24ab294ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "captureDdls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseMode")
    def database_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseMode"))

    @database_mode.setter
    def database_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1007b7cb08e4eebbcc09593fd44479a5ac58d9e01e6060f1cc9c50679b9c16c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ddlArtifactsSchema")
    def ddl_artifacts_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ddlArtifactsSchema"))

    @ddl_artifacts_schema.setter
    def ddl_artifacts_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c5651f79ed4794ad7cfd290349f53b826ffee5f77351a42465f4a3a2294458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ddlArtifactsSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executeTimeout")
    def execute_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executeTimeout"))

    @execute_timeout.setter
    def execute_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58caacc4d3b301b64c864b504e31ca4075ab40a2b1a96ab9f29f4567edf493d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failTasksOnLobTruncation")
    def fail_tasks_on_lob_truncation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failTasksOnLobTruncation"))

    @fail_tasks_on_lob_truncation.setter
    def fail_tasks_on_lob_truncation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e7e7d84dd7f1355d3b72d778d144a1e523885b0b9e6a683079692eab57c26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failTasksOnLobTruncation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heartbeatEnable")
    def heartbeat_enable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "heartbeatEnable"))

    @heartbeat_enable.setter
    def heartbeat_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891b8c6b79634ec349b52cff11f7ce2f48c31ce4ca4e0eefb8c2ca722bb84652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heartbeatEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heartbeatFrequency")
    def heartbeat_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "heartbeatFrequency"))

    @heartbeat_frequency.setter
    def heartbeat_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238b13dbe2a00b7169d0329a6f2aa19f1a21249a323b2d2a30e5fa1d77855d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heartbeatFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heartbeatSchema")
    def heartbeat_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "heartbeatSchema"))

    @heartbeat_schema.setter
    def heartbeat_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36c38cf91602d1372e3597a1fc162616818583ff94476618c5ceeb1c0d836dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heartbeatSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mapBooleanAsBoolean")
    def map_boolean_as_boolean(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mapBooleanAsBoolean"))

    @map_boolean_as_boolean.setter
    def map_boolean_as_boolean(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457f1eb88c9f903f326fc082d255f733aaae93baf9a778ffeaf6d43f66a15963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapBooleanAsBoolean", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mapJsonbAsClob")
    def map_jsonb_as_clob(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mapJsonbAsClob"))

    @map_jsonb_as_clob.setter
    def map_jsonb_as_clob(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c60d080f92844c7cc4f9206ec66da84345bda6ec2375aaea4c8c3e6ea17906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapJsonbAsClob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mapLongVarcharAs")
    def map_long_varchar_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mapLongVarcharAs"))

    @map_long_varchar_as.setter
    def map_long_varchar_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc0f3d77bd89b46eabbf81887cfbe364c5a1bcd5463e8ad579364fa5d9cfa53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapLongVarcharAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFileSize")
    def max_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFileSize"))

    @max_file_size.setter
    def max_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3b650bfe66605428828420da921fc0628c5cce998578743d62a5b7812d3e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFileSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db216ed2abad88c11a7c2baf029df6e1399f9780f6840b7be0209463dd4e03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccessRoleArn"))

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0fb9a81fc8d50d0ea2ac1415b42d971aa23a62d85e400269d277139cb75139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotName")
    def slot_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotName"))

    @slot_name.setter
    def slot_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ce815377265aece9cdd51ad7cfd3872074ab898f2843c3728ce0c39ec1a4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointPostgresSettings]:
        return typing.cast(typing.Optional[DmsEndpointPostgresSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsEndpointPostgresSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da490ac0be3594120725fc5ae5431aff5849cc4d509da1beb37a75ef72f7a139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointRedisSettings",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "port": "port",
        "server_name": "serverName",
        "auth_password": "authPassword",
        "auth_user_name": "authUserName",
        "ssl_ca_certificate_arn": "sslCaCertificateArn",
        "ssl_security_protocol": "sslSecurityProtocol",
    },
)
class DmsEndpointRedisSettings:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        port: jsii.Number,
        server_name: builtins.str,
        auth_password: typing.Optional[builtins.str] = None,
        auth_user_name: typing.Optional[builtins.str] = None,
        ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
        ssl_security_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_type DmsEndpoint#auth_type}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#port DmsEndpoint#port}.
        :param server_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_name DmsEndpoint#server_name}.
        :param auth_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_password DmsEndpoint#auth_password}.
        :param auth_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_user_name DmsEndpoint#auth_user_name}.
        :param ssl_ca_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_ca_certificate_arn DmsEndpoint#ssl_ca_certificate_arn}.
        :param ssl_security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_security_protocol DmsEndpoint#ssl_security_protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50edcbd2b69bd8ec6a62b43b65669c5e96c0cf5291c7c158ddb8dd4b0377c715)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            check_type(argname="argument auth_password", value=auth_password, expected_type=type_hints["auth_password"])
            check_type(argname="argument auth_user_name", value=auth_user_name, expected_type=type_hints["auth_user_name"])
            check_type(argname="argument ssl_ca_certificate_arn", value=ssl_ca_certificate_arn, expected_type=type_hints["ssl_ca_certificate_arn"])
            check_type(argname="argument ssl_security_protocol", value=ssl_security_protocol, expected_type=type_hints["ssl_security_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
            "port": port,
            "server_name": server_name,
        }
        if auth_password is not None:
            self._values["auth_password"] = auth_password
        if auth_user_name is not None:
            self._values["auth_user_name"] = auth_user_name
        if ssl_ca_certificate_arn is not None:
            self._values["ssl_ca_certificate_arn"] = ssl_ca_certificate_arn
        if ssl_security_protocol is not None:
            self._values["ssl_security_protocol"] = ssl_security_protocol

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_type DmsEndpoint#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#port DmsEndpoint#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def server_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_name DmsEndpoint#server_name}.'''
        result = self._values.get("server_name")
        assert result is not None, "Required property 'server_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_password DmsEndpoint#auth_password}.'''
        result = self._values.get("auth_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#auth_user_name DmsEndpoint#auth_user_name}.'''
        result = self._values.get("auth_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_ca_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_ca_certificate_arn DmsEndpoint#ssl_ca_certificate_arn}.'''
        result = self._values.get("ssl_ca_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_security_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#ssl_security_protocol DmsEndpoint#ssl_security_protocol}.'''
        result = self._values.get("ssl_security_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointRedisSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointRedisSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointRedisSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58563c2aae8526853c5aed3b2ae26c0cd38079a2fbcdc42d01e1dcec569fca4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthPassword")
    def reset_auth_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthPassword", []))

    @jsii.member(jsii_name="resetAuthUserName")
    def reset_auth_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUserName", []))

    @jsii.member(jsii_name="resetSslCaCertificateArn")
    def reset_ssl_ca_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCaCertificateArn", []))

    @jsii.member(jsii_name="resetSslSecurityProtocol")
    def reset_ssl_security_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslSecurityProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="authPasswordInput")
    def auth_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authUserNameInput")
    def auth_user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUserNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serverNameInput")
    def server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateArnInput")
    def ssl_ca_certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaCertificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sslSecurityProtocolInput")
    def ssl_security_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslSecurityProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="authPassword")
    def auth_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authPassword"))

    @auth_password.setter
    def auth_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603379634c6784f34bb136b2e319c9626ef14bf1a1a3693608ff6f7fa2c25d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c108f3ed12e5e3529e809d9a5db3de2023f07ecf186f35878c93adce62b362f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authUserName")
    def auth_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authUserName"))

    @auth_user_name.setter
    def auth_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a767d9d901491381e86afb5beb94cd36a093b1fd2d2708b743766adb84e4d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUserName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3458861f3fc55a97829631e77e5e5b6fe8b7de0cd931b17f907dd1eb7876e3c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverName")
    def server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverName"))

    @server_name.setter
    def server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa095ff8f1f875de5a7de0fa3e3ec0417ac79a1d944b1932f827a8dae7a14d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateArn")
    def ssl_ca_certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificateArn"))

    @ssl_ca_certificate_arn.setter
    def ssl_ca_certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0587255356059913cd483d66149b5161b70b6c9ca46669de7ff9f7efabd2d4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslSecurityProtocol")
    def ssl_security_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslSecurityProtocol"))

    @ssl_security_protocol.setter
    def ssl_security_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2d2974bd169b9f91edc5ae0f055d560cd5c8a4e90ba6ffaa5ce407ac582cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslSecurityProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointRedisSettings]:
        return typing.cast(typing.Optional[DmsEndpointRedisSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DmsEndpointRedisSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c432ff9c1e536045cfdd4d0df9d81e165b9a17d65fd8657392a9cbcc8a622740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointRedshiftSettings",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_folder": "bucketFolder",
        "bucket_name": "bucketName",
        "encryption_mode": "encryptionMode",
        "server_side_encryption_kms_key_id": "serverSideEncryptionKmsKeyId",
        "service_access_role_arn": "serviceAccessRoleArn",
    },
)
class DmsEndpointRedshiftSettings:
    def __init__(
        self,
        *,
        bucket_folder: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        encryption_mode: typing.Optional[builtins.str] = None,
        server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
        service_access_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#bucket_folder DmsEndpoint#bucket_folder}.
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#bucket_name DmsEndpoint#bucket_name}.
        :param encryption_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#encryption_mode DmsEndpoint#encryption_mode}.
        :param server_side_encryption_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_side_encryption_kms_key_id DmsEndpoint#server_side_encryption_kms_key_id}.
        :param service_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fdfffd9028818e5ac85e2f4f249a4133cbabb8d11fa6029d8a6f0ff7cbe851)
            check_type(argname="argument bucket_folder", value=bucket_folder, expected_type=type_hints["bucket_folder"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
            check_type(argname="argument server_side_encryption_kms_key_id", value=server_side_encryption_kms_key_id, expected_type=type_hints["server_side_encryption_kms_key_id"])
            check_type(argname="argument service_access_role_arn", value=service_access_role_arn, expected_type=type_hints["service_access_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_folder is not None:
            self._values["bucket_folder"] = bucket_folder
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if encryption_mode is not None:
            self._values["encryption_mode"] = encryption_mode
        if server_side_encryption_kms_key_id is not None:
            self._values["server_side_encryption_kms_key_id"] = server_side_encryption_kms_key_id
        if service_access_role_arn is not None:
            self._values["service_access_role_arn"] = service_access_role_arn

    @builtins.property
    def bucket_folder(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#bucket_folder DmsEndpoint#bucket_folder}.'''
        result = self._values.get("bucket_folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#bucket_name DmsEndpoint#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#encryption_mode DmsEndpoint#encryption_mode}.'''
        result = self._values.get("encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#server_side_encryption_kms_key_id DmsEndpoint#server_side_encryption_kms_key_id}.'''
        result = self._values.get("server_side_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#service_access_role_arn DmsEndpoint#service_access_role_arn}.'''
        result = self._values.get("service_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointRedshiftSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointRedshiftSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointRedshiftSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71268a87424b2943890e1e76cb2cd66c615c8355efafcb8c5e7c839944a415ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketFolder")
    def reset_bucket_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketFolder", []))

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetEncryptionMode")
    def reset_encryption_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionMode", []))

    @jsii.member(jsii_name="resetServerSideEncryptionKmsKeyId")
    def reset_server_side_encryption_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryptionKmsKeyId", []))

    @jsii.member(jsii_name="resetServiceAccessRoleArn")
    def reset_service_access_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccessRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="bucketFolderInput")
    def bucket_folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketFolderInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionModeInput")
    def encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionKmsKeyIdInput")
    def server_side_encryption_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverSideEncryptionKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArnInput")
    def service_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketFolder")
    def bucket_folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketFolder"))

    @bucket_folder.setter
    def bucket_folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0efeae98114677b9a72d8316c48e6108db43580a7444b5dcdb23c50c1f3652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc816642fa4338485044ca00b7bf3c6a17192160a6aa0b5485f5332f3d37e483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionMode")
    def encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionMode"))

    @encryption_mode.setter
    def encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c613a7d1a7b7f7260e442e53b75b6e77d3a3ace0d11f4c170c10ac1ffa415c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionKmsKeyId")
    def server_side_encryption_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverSideEncryptionKmsKeyId"))

    @server_side_encryption_kms_key_id.setter
    def server_side_encryption_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba4157bf19b0a1206e8a94b7787229361d63943d1e214fc035f720072bb6290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryptionKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccessRoleArn"))

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718decf5141e5f04a4604c24db10b50629498e9c6088c22eff41192bb37ebfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsEndpointRedshiftSettings]:
        return typing.cast(typing.Optional[DmsEndpointRedshiftSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsEndpointRedshiftSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0e497e9586776cab03bf07b2fadf182584011f5327140d5ac114b0e442c563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DmsEndpointTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#create DmsEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#delete DmsEndpoint#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551ae0fdfae5db31af2b32085d9804df69d407f96938f4a19226d9f519340cae)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#create DmsEndpoint#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/dms_endpoint#delete DmsEndpoint#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsEndpointTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsEndpointTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.dmsEndpoint.DmsEndpointTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc0fced37196d2c72f2ee547d56c6ce0c05c24cd1469d03c60016deb6bd05e47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3ec67b1b5c78aafc83eaa13f91418372151ce3c7d4b8f12cd56529403d4b1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330207c2083d0f5943a13890fc270d9ae6e544c0c73cfa1ff28b46222206e68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsEndpointTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsEndpointTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsEndpointTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b801c26b573ae087355fafc0501599286acc68601c78e21e631c7bfeb1cb5eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DmsEndpoint",
    "DmsEndpointConfig",
    "DmsEndpointElasticsearchSettings",
    "DmsEndpointElasticsearchSettingsOutputReference",
    "DmsEndpointKafkaSettings",
    "DmsEndpointKafkaSettingsOutputReference",
    "DmsEndpointKinesisSettings",
    "DmsEndpointKinesisSettingsOutputReference",
    "DmsEndpointMongodbSettings",
    "DmsEndpointMongodbSettingsOutputReference",
    "DmsEndpointMysqlSettings",
    "DmsEndpointMysqlSettingsOutputReference",
    "DmsEndpointOracleSettings",
    "DmsEndpointOracleSettingsOutputReference",
    "DmsEndpointPostgresSettings",
    "DmsEndpointPostgresSettingsOutputReference",
    "DmsEndpointRedisSettings",
    "DmsEndpointRedisSettingsOutputReference",
    "DmsEndpointRedshiftSettings",
    "DmsEndpointRedshiftSettingsOutputReference",
    "DmsEndpointTimeouts",
    "DmsEndpointTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__82865518ff11ec0d7c79e82a70ac8a1694fac502beded9c6729248e96d91d964(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    endpoint_id: builtins.str,
    endpoint_type: builtins.str,
    engine_name: builtins.str,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    elasticsearch_settings: typing.Optional[typing.Union[DmsEndpointElasticsearchSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    extra_connection_attributes: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kafka_settings: typing.Optional[typing.Union[DmsEndpointKafkaSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_settings: typing.Optional[typing.Union[DmsEndpointKinesisSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    mongodb_settings: typing.Optional[typing.Union[DmsEndpointMongodbSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql_settings: typing.Optional[typing.Union[DmsEndpointMysqlSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_settings: typing.Optional[typing.Union[DmsEndpointOracleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    password: typing.Optional[builtins.str] = None,
    pause_replication_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port: typing.Optional[jsii.Number] = None,
    postgres_settings: typing.Optional[typing.Union[DmsEndpointPostgresSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    redis_settings: typing.Optional[typing.Union[DmsEndpointRedisSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift_settings: typing.Optional[typing.Union[DmsEndpointRedshiftSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_arn: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    service_access_role: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DmsEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__72cd95dd55b0ef427210f6c30803eeed8a9e1bf7a62c73ebffa11a0aed8a62ce(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b377c78d11666a4f207dffc165c5558eef9c779d1db6a7896f678e9709e3c38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf020450c8098d62d97e24aecad3923f321a7c03ff3fd02fcaa94939db2dd101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cca73304c43ed9f0530576647f25dc884612544dff70ec0325b99eb0e8e643d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89d89edc28b3bf9863b8bc462975cb980c134b222b0c6310674c23b4ae02203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c655bf7645f162d6c5781ab6e4a88ce69aee6527754ff3a5ef7e84eff7968f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2332929ab9f9fee91673cfe39cd52e3cdb53759f5bf966cd87ec3f23ed8ff158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c59d242326572531979145f8b580cabd42f524cee1826a9dea30006258a6938(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436bbbd6fd671d72ae4819049cad8f7d4d45a23b846e250888b9c7e4c89ec068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d77f26e123922083eaa50b923a5ebd6e75bcd3be19c959381523d52a8d146d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8afc16112ae43fac9e726ade028a07f58f3d05a96bb0d1a838b8cc5051a6fb3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1f6c73cdc81fba11037472e16d8b0ce4a571d63cfaa249d57d7f3b96d3ee05(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0d57fafb8e1785051bf92f270123e72b687a19d45c6416ba717ee3ab733634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734ab7903343a2e2a2ed5dd32e6fdeb5df419082390924bed55ed612abebf25c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6470149a8cb8bd31f67828f162b58c847dc92d25189f872a0a509983bd50d035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecf8ab79355935e77ed1cafc5c0e2da698975f69839b9393d220d30ec175b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1b09e5c54b434947dd5229bcba6da0829fcbcac973cacfdce7f843a69a08e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d468d57d9c44903719c9038d15109cab2d3c83632cf0a094225a91a545b22a65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989a50b47f85c3f419df7951d743a20bb1f1c2274bab8e4d92ad3e22780ad4f7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23aac4dcf0b5b7011dd47715c70fdf104cee01a945450d8b18020ac01c7dc07(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2611ba00b52953341c42861c26e00e60daa2d10a082183218d782470b6dd54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4271b8edf97e24550273f060cffa2fae9e24f0ef043f68fcbc1416eec910c536(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    endpoint_id: builtins.str,
    endpoint_type: builtins.str,
    engine_name: builtins.str,
    certificate_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    elasticsearch_settings: typing.Optional[typing.Union[DmsEndpointElasticsearchSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    extra_connection_attributes: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kafka_settings: typing.Optional[typing.Union[DmsEndpointKafkaSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_settings: typing.Optional[typing.Union[DmsEndpointKinesisSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    mongodb_settings: typing.Optional[typing.Union[DmsEndpointMongodbSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql_settings: typing.Optional[typing.Union[DmsEndpointMysqlSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_settings: typing.Optional[typing.Union[DmsEndpointOracleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    password: typing.Optional[builtins.str] = None,
    pause_replication_tasks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    port: typing.Optional[jsii.Number] = None,
    postgres_settings: typing.Optional[typing.Union[DmsEndpointPostgresSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    redis_settings: typing.Optional[typing.Union[DmsEndpointRedisSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift_settings: typing.Optional[typing.Union[DmsEndpointRedshiftSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    secrets_manager_access_role_arn: typing.Optional[builtins.str] = None,
    secrets_manager_arn: typing.Optional[builtins.str] = None,
    server_name: typing.Optional[builtins.str] = None,
    service_access_role: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DmsEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0935c528bd62469f23d809b6fa1d43cec2b42fea93e6a81bc5cdbb73e8e12008(
    *,
    endpoint_uri: builtins.str,
    service_access_role_arn: builtins.str,
    error_retry_duration: typing.Optional[jsii.Number] = None,
    full_load_error_percentage: typing.Optional[jsii.Number] = None,
    use_new_mapping_type: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2426837a5a65a7bdcffce69fc9d4a13cbd0a1c70760d297c3d36bef6c85c96fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0485f47c371d32303d40fa06be133b48ccec2b373200319b6d3f14f9886ece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4ed5995dc86a12a8960ecdf2d0b670267dc7ed051dad8286cff699863ca2f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1ea82d66826e4111b489c92a6fd612d8317180b19c471e9801505263540a03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db7ae8011492e0b066a9e892aa6456cbe3a99702fb655ee08e1ba772dd7f636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c080155112f741e50cc28c99d3d81f3386be7cdb3a6ecb80e403e360fce3954a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3493cc9a19b442f1acaaa73452a80d544a94fe2f7331ea478a5519e2ac84d6(
    value: typing.Optional[DmsEndpointElasticsearchSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492b0f45f640bbe5e03b9d2867e32dc7af8a38b827990014de779d4877f07dac(
    *,
    broker: builtins.str,
    include_control_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_partition_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_transaction_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message_format: typing.Optional[builtins.str] = None,
    message_max_bytes: typing.Optional[jsii.Number] = None,
    no_hex_prefix: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sasl_mechanism: typing.Optional[builtins.str] = None,
    sasl_password: typing.Optional[builtins.str] = None,
    sasl_username: typing.Optional[builtins.str] = None,
    security_protocol: typing.Optional[builtins.str] = None,
    ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_client_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_client_key_arn: typing.Optional[builtins.str] = None,
    ssl_client_key_password: typing.Optional[builtins.str] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f025d75cfb569d4b8998674a01d14fd5b0deb61a1eb1ddc6887de067d61a6726(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983f5975bfa124c4e5014e1b9a7bd312bff3859b050bf5d595e2dc4aa92584c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b554a07d86d35db83c71175f8cb44a4bcc33fc26ee0b7666072cb0714b038d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1806090128f89cc12ff09dfe5c3a1208432d9c2f42ac81b3b3971ad394987b84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75d66bba249a8a18ebc8758bd6570e6a66f8e9094200bff07d072c1d237247f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bd14900f33ec68f53748f88ce80e878e04ecfbe1e8dfad50f5ff4f8e95e544(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd3c730f6c8f8061e79b43ead35ff12cd9c5217a9e351751f78d769e3311bfb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904fafe50eca77090c2d171b86d032282eddcd0d0343bba89148e63a18b82221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa251cb4a0a272f6373097014268752913a292e49cbd8de49f33c6538344385(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90df562e067695228f6b66e9bda9309b8018a23d3c0e766310e6c2b4bd0cb8e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538b81ddac35c64061e6f7e163a3ae91fe98511d4a335a6fbb5362054c78061f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb6f67113292e1fb4f133fa44804de7d1a89f94536f6354a002ee31ce22938e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b092753bb755d5f16c4d2bdf425a935b2908c9c961f5c5b82bb60c00b578c972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae28a7328d50097d7212403cffa3e6681d92f617c2eae30195dc66c93ef4cb63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b70ddf8fb253e3753756042e5c03d952ebcd758d7ebdfca0e9535aefde74c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ca6645c4c2d117c5a2ad5d891aade8ef14561f8bebc66766582675e043d1f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d9332142c6f728d0eddd39d1eea1321f9f4752c641ed5b8f411bdb8901bab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559a728992f63be2df5e88585272e03c1941f807cc990c50e6021dba000ef176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8ccc44d56787d8402afc8e4823e7b74def31999af435aaddada416f82418d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac49684cf6fba772d54b390b5f3c9bebfaa40d1ddf863551e5c9164929bc34ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb9c5f6b7a1b8c0daf118224b0f0caf376d553bd91ec8e2cb73614d11cb1dfa(
    value: typing.Optional[DmsEndpointKafkaSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b1603904f76bde961fda96c7307bc5ba4881b8bfe458d4797edf06955ad312(
    *,
    include_control_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_null_and_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_partition_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_table_alter_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_transaction_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message_format: typing.Optional[builtins.str] = None,
    partition_include_schema_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    stream_arn: typing.Optional[builtins.str] = None,
    use_large_integer_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957ae377877e01f5ff11db44397f76c0b2c1d446f5f60ffc94432f4ca3319517(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ee432def92209ad48889acd665a506b0e0e91d2be2dcadd7182a2a159cabec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc72ed37cb717dadc0943e30b110f711e73d4d120368f913b7821c384691a557(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c7203cc0289fcdb69d73aa345f68b9c134452c60373596373c90352d2195ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b4a6c702864b88fa6e2bb52cb74d6ff278d8627c624eaca55fbb17678707c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea183c3946437ac5082d702b06ad99936d90b5c815ad301b751d9d0232ff352(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791d42ee49983b1ba1ed1e9ad54c11ba1d6fa2e14e391e0723c0fd2094cd59dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5207b7c857c7a0b7ad3006fc0b18bac8796f71f01fa7a8ca50d92cbd8cd7cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbc73b808a7c74b2723f0bf72790dca988954dee86cc76a65a39303498a1e59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0011f0e935f495dffca145d2a3f8e10af6bbe353953d94ff82ad87ebceabe485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e71e25b19bd9e50e002dd6af70b7bed3e94179b82ec15eaf433e85025a42ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360bf155de9eae35975801f65b1917c05f8831cefff7c62bb47cf594a6e4f0cf(
    value: typing.Optional[DmsEndpointKinesisSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa47d92ed2a40aad2d1ab9655f01e12689c2bb7650142fe12e7e80c04eedc02f(
    *,
    auth_mechanism: typing.Optional[builtins.str] = None,
    auth_source: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    docs_to_investigate: typing.Optional[builtins.str] = None,
    extract_doc_id: typing.Optional[builtins.str] = None,
    nesting_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd8267ca2131f95b789c5601c74790cfc8670b8f9364447a73585bf68eb207c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ebd8e8bd1af4a55e7f289ac54d6e6b3904b8476f8375b3c393e3d51dd7cc99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f5fd3e6486bddd234e6108b13dafce16e4e05ef397cb70daf4ed2322c1c967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061cc32e180f7f08511bd25c415a70de0698f291e5d3253e6cba934849081e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0058003c58d76aec9767ed880f78308fd54d24e0a6df840e0ab4cc571251f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f822cd6e466844f9c79f0ca2ff6434e659991b10e819fd3628c7d785544d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868afaba143788a4aaaa6bb2992d2cf1378c836bdd1d11793f613f0cc024123b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1180f9cb7605a47356a201c17301e771ecfbf9782c0d2c958a270734bd9501d7(
    value: typing.Optional[DmsEndpointMongodbSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8a042e25c91268a6f7985e9b80798823264ef6fff72eaa010048b60ab9be39(
    *,
    after_connect_script: typing.Optional[builtins.str] = None,
    authentication_method: typing.Optional[builtins.str] = None,
    clean_source_metadata_on_mismatch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    events_poll_interval: typing.Optional[jsii.Number] = None,
    execute_timeout: typing.Optional[jsii.Number] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    parallel_load_threads: typing.Optional[jsii.Number] = None,
    server_timezone: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    target_db_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688658782d483136eb50e65cc9d8b32ec6491924379e879fafd1f456a61faa93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1c04b588f6d0668903452aa8c00c713648b8a5e1885238d975002808a9ced5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06bda059913599dbeabba665495118c29e94e97b3968e5f9479f601a4e60e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fd7d750f08658ecb0b07ab031a54f0c5194b3b5ef72992b8d41cb7e056db55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413f7e483a3d40c0ca047dfe83043769581f626c43cc34544ae9a395ca10e3ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597cb43837c55ade81abe1e1cda967ea41233500f538de6d2c382df66f03c215(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341f827e552be0ccebc15b258cd174738d314c2803faeb6447ecb850199e2483(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59fb4489b6e9ce54e92bb9f4bf61e58ce92dc4cb02e6b31c7a970b4329b02b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc4f540b6f48e4525e5546e0df9c6bd6b4023c5fd7e2c0a632679addcf2f847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b965b9e3bd2c9d9417b02f75f11238cd63970df8a6b596ab7afd83c9c405d49e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb3fb9cab56e687a0678333fe756129936425bb0c37267fc4ce672273f8ab2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1bd31a99f986b75749bff2f4cbdc0c57ba61fdc5313c9f46328935d06b2957(
    value: typing.Optional[DmsEndpointMysqlSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1885b6ca06a07065461896d8c4b48bb8e0377e761a57f0219c398065dd9a6f7(
    *,
    authentication_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6a59b91a1dbc40e796c9e9fa70c55cb6a514cecb3e891f7a6e85ec962f8652(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5a447ddc913283626168a2dda24331b96d27a19cd0e46747aaa5ec73ecbf52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6287d565035d1d8b800b8656c290545d2a2fc186d1c26ff8697655ea91d290b(
    value: typing.Optional[DmsEndpointOracleSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e69b81228b21e6646e58c724e16464d9d76ff1c863612942c5fae83a7055bb6(
    *,
    after_connect_script: typing.Optional[builtins.str] = None,
    authentication_method: typing.Optional[builtins.str] = None,
    babelfish_database_name: typing.Optional[builtins.str] = None,
    capture_ddls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    database_mode: typing.Optional[builtins.str] = None,
    ddl_artifacts_schema: typing.Optional[builtins.str] = None,
    execute_timeout: typing.Optional[jsii.Number] = None,
    fail_tasks_on_lob_truncation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    heartbeat_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    heartbeat_frequency: typing.Optional[jsii.Number] = None,
    heartbeat_schema: typing.Optional[builtins.str] = None,
    map_boolean_as_boolean: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_jsonb_as_clob: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_long_varchar_as: typing.Optional[builtins.str] = None,
    max_file_size: typing.Optional[jsii.Number] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
    slot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4240d56f2d196f9de89dff6a494381666cdc6a09778a24e3af595ec606ea6a2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dec6e8ed671bc1cad9bd50ef2c46c3d94617812fb4e7e3e8e40a76a90388abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5006a5c2a250734785afc40b3521d8eb7127dc26a0d3524196f86e890711dad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8943bbbcf3a5e55fe104c3213ee97dc83a5a7750f64e699c73f2f81e7376c884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e58907c06f90385d4ebb6ef19908f582fa7c197e78f3b8efebb5a24ab294ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1007b7cb08e4eebbcc09593fd44479a5ac58d9e01e6060f1cc9c50679b9c16c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c5651f79ed4794ad7cfd290349f53b826ffee5f77351a42465f4a3a2294458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58caacc4d3b301b64c864b504e31ca4075ab40a2b1a96ab9f29f4567edf493d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e7e7d84dd7f1355d3b72d778d144a1e523885b0b9e6a683079692eab57c26d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891b8c6b79634ec349b52cff11f7ce2f48c31ce4ca4e0eefb8c2ca722bb84652(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238b13dbe2a00b7169d0329a6f2aa19f1a21249a323b2d2a30e5fa1d77855d5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36c38cf91602d1372e3597a1fc162616818583ff94476618c5ceeb1c0d836dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457f1eb88c9f903f326fc082d255f733aaae93baf9a778ffeaf6d43f66a15963(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c60d080f92844c7cc4f9206ec66da84345bda6ec2375aaea4c8c3e6ea17906(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc0f3d77bd89b46eabbf81887cfbe364c5a1bcd5463e8ad579364fa5d9cfa53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3b650bfe66605428828420da921fc0628c5cce998578743d62a5b7812d3e6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db216ed2abad88c11a7c2baf029df6e1399f9780f6840b7be0209463dd4e03c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0fb9a81fc8d50d0ea2ac1415b42d971aa23a62d85e400269d277139cb75139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ce815377265aece9cdd51ad7cfd3872074ab898f2843c3728ce0c39ec1a4d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da490ac0be3594120725fc5ae5431aff5849cc4d509da1beb37a75ef72f7a139(
    value: typing.Optional[DmsEndpointPostgresSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50edcbd2b69bd8ec6a62b43b65669c5e96c0cf5291c7c158ddb8dd4b0377c715(
    *,
    auth_type: builtins.str,
    port: jsii.Number,
    server_name: builtins.str,
    auth_password: typing.Optional[builtins.str] = None,
    auth_user_name: typing.Optional[builtins.str] = None,
    ssl_ca_certificate_arn: typing.Optional[builtins.str] = None,
    ssl_security_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58563c2aae8526853c5aed3b2ae26c0cd38079a2fbcdc42d01e1dcec569fca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603379634c6784f34bb136b2e319c9626ef14bf1a1a3693608ff6f7fa2c25d15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c108f3ed12e5e3529e809d9a5db3de2023f07ecf186f35878c93adce62b362f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a767d9d901491381e86afb5beb94cd36a093b1fd2d2708b743766adb84e4d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3458861f3fc55a97829631e77e5e5b6fe8b7de0cd931b17f907dd1eb7876e3c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa095ff8f1f875de5a7de0fa3e3ec0417ac79a1d944b1932f827a8dae7a14d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0587255356059913cd483d66149b5161b70b6c9ca46669de7ff9f7efabd2d4c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2d2974bd169b9f91edc5ae0f055d560cd5c8a4e90ba6ffaa5ce407ac582cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c432ff9c1e536045cfdd4d0df9d81e165b9a17d65fd8657392a9cbcc8a622740(
    value: typing.Optional[DmsEndpointRedisSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fdfffd9028818e5ac85e2f4f249a4133cbabb8d11fa6029d8a6f0ff7cbe851(
    *,
    bucket_folder: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption_mode: typing.Optional[builtins.str] = None,
    server_side_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    service_access_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71268a87424b2943890e1e76cb2cd66c615c8355efafcb8c5e7c839944a415ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0efeae98114677b9a72d8316c48e6108db43580a7444b5dcdb23c50c1f3652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc816642fa4338485044ca00b7bf3c6a17192160a6aa0b5485f5332f3d37e483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c613a7d1a7b7f7260e442e53b75b6e77d3a3ace0d11f4c170c10ac1ffa415c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba4157bf19b0a1206e8a94b7787229361d63943d1e214fc035f720072bb6290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718decf5141e5f04a4604c24db10b50629498e9c6088c22eff41192bb37ebfa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0e497e9586776cab03bf07b2fadf182584011f5327140d5ac114b0e442c563(
    value: typing.Optional[DmsEndpointRedshiftSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551ae0fdfae5db31af2b32085d9804df69d407f96938f4a19226d9f519340cae(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0fced37196d2c72f2ee547d56c6ce0c05c24cd1469d03c60016deb6bd05e47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3ec67b1b5c78aafc83eaa13f91418372151ce3c7d4b8f12cd56529403d4b1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330207c2083d0f5943a13890fc270d9ae6e544c0c73cfa1ff28b46222206e68a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b801c26b573ae087355fafc0501599286acc68601c78e21e631c7bfeb1cb5eea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsEndpointTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
