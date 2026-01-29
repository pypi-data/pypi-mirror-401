r'''
# `aws_mskconnect_connector`

Refer to the Terraform Registry for docs: [`aws_mskconnect_connector`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector).
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


class MskconnectConnector(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnector",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector aws_mskconnect_connector}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity: typing.Union["MskconnectConnectorCapacity", typing.Dict[builtins.str, typing.Any]],
        connector_configuration: typing.Mapping[builtins.str, builtins.str],
        kafka_cluster: typing.Union["MskconnectConnectorKafkaCluster", typing.Dict[builtins.str, typing.Any]],
        kafka_cluster_client_authentication: typing.Union["MskconnectConnectorKafkaClusterClientAuthentication", typing.Dict[builtins.str, typing.Any]],
        kafka_cluster_encryption_in_transit: typing.Union["MskconnectConnectorKafkaClusterEncryptionInTransit", typing.Dict[builtins.str, typing.Any]],
        kafkaconnect_version: builtins.str,
        name: builtins.str,
        plugin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskconnectConnectorPlugin", typing.Dict[builtins.str, typing.Any]]]],
        service_execution_role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union["MskconnectConnectorLogDelivery", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MskconnectConnectorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_configuration: typing.Optional[typing.Union["MskconnectConnectorWorkerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector aws_mskconnect_connector} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#capacity MskconnectConnector#capacity}
        :param connector_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#connector_configuration MskconnectConnector#connector_configuration}.
        :param kafka_cluster: kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster MskconnectConnector#kafka_cluster}
        :param kafka_cluster_client_authentication: kafka_cluster_client_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster_client_authentication MskconnectConnector#kafka_cluster_client_authentication}
        :param kafka_cluster_encryption_in_transit: kafka_cluster_encryption_in_transit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster_encryption_in_transit MskconnectConnector#kafka_cluster_encryption_in_transit}
        :param kafkaconnect_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafkaconnect_version MskconnectConnector#kafkaconnect_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#name MskconnectConnector#name}.
        :param plugin: plugin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#plugin MskconnectConnector#plugin}
        :param service_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#service_execution_role_arn MskconnectConnector#service_execution_role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#description MskconnectConnector#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#id MskconnectConnector#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_delivery: log_delivery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#log_delivery MskconnectConnector#log_delivery}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#region MskconnectConnector#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#tags MskconnectConnector#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#tags_all MskconnectConnector#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#timeouts MskconnectConnector#timeouts}
        :param worker_configuration: worker_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_configuration MskconnectConnector#worker_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfddbe8a630b39d02b4e8dbbbf4fa6dc50a726b9ff8501991623ff341a085303)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MskconnectConnectorConfig(
            capacity=capacity,
            connector_configuration=connector_configuration,
            kafka_cluster=kafka_cluster,
            kafka_cluster_client_authentication=kafka_cluster_client_authentication,
            kafka_cluster_encryption_in_transit=kafka_cluster_encryption_in_transit,
            kafkaconnect_version=kafkaconnect_version,
            name=name,
            plugin=plugin,
            service_execution_role_arn=service_execution_role_arn,
            description=description,
            id=id,
            log_delivery=log_delivery,
            region=region,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            worker_configuration=worker_configuration,
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
        '''Generates CDKTF code for importing a MskconnectConnector resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MskconnectConnector to import.
        :param import_from_id: The id of the existing MskconnectConnector that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MskconnectConnector to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8247dca66cfc7da7fc26d3c7ca5da63ecf5d4b5b1e01faeae3f045b3c4cbc336)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapacity")
    def put_capacity(
        self,
        *,
        autoscaling: typing.Optional[typing.Union["MskconnectConnectorCapacityAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        provisioned_capacity: typing.Optional[typing.Union["MskconnectConnectorCapacityProvisionedCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#autoscaling MskconnectConnector#autoscaling}
        :param provisioned_capacity: provisioned_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#provisioned_capacity MskconnectConnector#provisioned_capacity}
        '''
        value = MskconnectConnectorCapacity(
            autoscaling=autoscaling, provisioned_capacity=provisioned_capacity
        )

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="putKafkaCluster")
    def put_kafka_cluster(
        self,
        *,
        apache_kafka_cluster: typing.Union["MskconnectConnectorKafkaClusterApacheKafkaCluster", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param apache_kafka_cluster: apache_kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#apache_kafka_cluster MskconnectConnector#apache_kafka_cluster}
        '''
        value = MskconnectConnectorKafkaCluster(
            apache_kafka_cluster=apache_kafka_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putKafkaCluster", [value]))

    @jsii.member(jsii_name="putKafkaClusterClientAuthentication")
    def put_kafka_cluster_client_authentication(
        self,
        *,
        authentication_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#authentication_type MskconnectConnector#authentication_type}.
        '''
        value = MskconnectConnectorKafkaClusterClientAuthentication(
            authentication_type=authentication_type
        )

        return typing.cast(None, jsii.invoke(self, "putKafkaClusterClientAuthentication", [value]))

    @jsii.member(jsii_name="putKafkaClusterEncryptionInTransit")
    def put_kafka_cluster_encryption_in_transit(
        self,
        *,
        encryption_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#encryption_type MskconnectConnector#encryption_type}.
        '''
        value = MskconnectConnectorKafkaClusterEncryptionInTransit(
            encryption_type=encryption_type
        )

        return typing.cast(None, jsii.invoke(self, "putKafkaClusterEncryptionInTransit", [value]))

    @jsii.member(jsii_name="putLogDelivery")
    def put_log_delivery(
        self,
        *,
        worker_log_delivery: typing.Union["MskconnectConnectorLogDeliveryWorkerLogDelivery", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param worker_log_delivery: worker_log_delivery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_log_delivery MskconnectConnector#worker_log_delivery}
        '''
        value = MskconnectConnectorLogDelivery(worker_log_delivery=worker_log_delivery)

        return typing.cast(None, jsii.invoke(self, "putLogDelivery", [value]))

    @jsii.member(jsii_name="putPlugin")
    def put_plugin(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskconnectConnectorPlugin", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f393437701b55aabb5bf2de9b1662717a99d50f930690d69e0dd4f364a6073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlugin", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#create MskconnectConnector#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#delete MskconnectConnector#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#update MskconnectConnector#update}.
        '''
        value = MskconnectConnectorTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkerConfiguration")
    def put_worker_configuration(
        self,
        *,
        arn: builtins.str,
        revision: jsii.Number,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#arn MskconnectConnector#arn}.
        :param revision: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#revision MskconnectConnector#revision}.
        '''
        value = MskconnectConnectorWorkerConfiguration(arn=arn, revision=revision)

        return typing.cast(None, jsii.invoke(self, "putWorkerConfiguration", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogDelivery")
    def reset_log_delivery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDelivery", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkerConfiguration")
    def reset_worker_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfiguration", []))

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
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> "MskconnectConnectorCapacityOutputReference":
        return typing.cast("MskconnectConnectorCapacityOutputReference", jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="kafkaCluster")
    def kafka_cluster(self) -> "MskconnectConnectorKafkaClusterOutputReference":
        return typing.cast("MskconnectConnectorKafkaClusterOutputReference", jsii.get(self, "kafkaCluster"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterClientAuthentication")
    def kafka_cluster_client_authentication(
        self,
    ) -> "MskconnectConnectorKafkaClusterClientAuthenticationOutputReference":
        return typing.cast("MskconnectConnectorKafkaClusterClientAuthenticationOutputReference", jsii.get(self, "kafkaClusterClientAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterEncryptionInTransit")
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> "MskconnectConnectorKafkaClusterEncryptionInTransitOutputReference":
        return typing.cast("MskconnectConnectorKafkaClusterEncryptionInTransitOutputReference", jsii.get(self, "kafkaClusterEncryptionInTransit"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def log_delivery(self) -> "MskconnectConnectorLogDeliveryOutputReference":
        return typing.cast("MskconnectConnectorLogDeliveryOutputReference", jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="plugin")
    def plugin(self) -> "MskconnectConnectorPluginList":
        return typing.cast("MskconnectConnectorPluginList", jsii.get(self, "plugin"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MskconnectConnectorTimeoutsOutputReference":
        return typing.cast("MskconnectConnectorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="workerConfiguration")
    def worker_configuration(
        self,
    ) -> "MskconnectConnectorWorkerConfigurationOutputReference":
        return typing.cast("MskconnectConnectorWorkerConfigurationOutputReference", jsii.get(self, "workerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional["MskconnectConnectorCapacity"]:
        return typing.cast(typing.Optional["MskconnectConnectorCapacity"], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorConfigurationInput")
    def connector_configuration_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "connectorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterClientAuthenticationInput")
    def kafka_cluster_client_authentication_input(
        self,
    ) -> typing.Optional["MskconnectConnectorKafkaClusterClientAuthentication"]:
        return typing.cast(typing.Optional["MskconnectConnectorKafkaClusterClientAuthentication"], jsii.get(self, "kafkaClusterClientAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterEncryptionInTransitInput")
    def kafka_cluster_encryption_in_transit_input(
        self,
    ) -> typing.Optional["MskconnectConnectorKafkaClusterEncryptionInTransit"]:
        return typing.cast(typing.Optional["MskconnectConnectorKafkaClusterEncryptionInTransit"], jsii.get(self, "kafkaClusterEncryptionInTransitInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterInput")
    def kafka_cluster_input(self) -> typing.Optional["MskconnectConnectorKafkaCluster"]:
        return typing.cast(typing.Optional["MskconnectConnectorKafkaCluster"], jsii.get(self, "kafkaClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaconnectVersionInput")
    def kafkaconnect_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kafkaconnectVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="logDeliveryInput")
    def log_delivery_input(self) -> typing.Optional["MskconnectConnectorLogDelivery"]:
        return typing.cast(typing.Optional["MskconnectConnectorLogDelivery"], jsii.get(self, "logDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginInput")
    def plugin_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskconnectConnectorPlugin"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskconnectConnectorPlugin"]]], jsii.get(self, "pluginInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceExecutionRoleArnInput")
    def service_execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceExecutionRoleArnInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MskconnectConnectorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MskconnectConnectorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigurationInput")
    def worker_configuration_input(
        self,
    ) -> typing.Optional["MskconnectConnectorWorkerConfiguration"]:
        return typing.cast(typing.Optional["MskconnectConnectorWorkerConfiguration"], jsii.get(self, "workerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorConfiguration")
    def connector_configuration(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "connectorConfiguration"))

    @connector_configuration.setter
    def connector_configuration(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b157d18d405af6c880bd1e49ea699e29fa0cb5a0ffb370e3ec33ed74937af7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e696f87cbc7123848803299dddc7d6a64e723ffb14db32465416b3a4de0709d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cf8f6077e9f54421b520fa5677e4dca4a403627ec5f425511e69f070644e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kafkaconnectVersion")
    def kafkaconnect_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kafkaconnectVersion"))

    @kafkaconnect_version.setter
    def kafkaconnect_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c63104c00c81f65bb397f9bf725e276a3c44608816653773512d3ee7f0079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafkaconnectVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a72b738286eba97dfd5c0a9fbff68d6b1579b84349e7ba103cc6a35f3631ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5c5852c1b6eadd963f71d6a821e5ef789f1ad5a416b1889abae6cea8993c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceExecutionRoleArn"))

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfbd9d823e0ac46eea686e888da6f3ab566a531784d072cfbfb77488819a9c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceExecutionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d2373ca16cea4a25cb902c6e32400af8fbd13594729bd58d0ef4e4f07acfc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a1dab380886114d16510e6efddf731cb59720a1b414b404f273c7d55c7e82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling": "autoscaling",
        "provisioned_capacity": "provisionedCapacity",
    },
)
class MskconnectConnectorCapacity:
    def __init__(
        self,
        *,
        autoscaling: typing.Optional[typing.Union["MskconnectConnectorCapacityAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        provisioned_capacity: typing.Optional[typing.Union["MskconnectConnectorCapacityProvisionedCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#autoscaling MskconnectConnector#autoscaling}
        :param provisioned_capacity: provisioned_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#provisioned_capacity MskconnectConnector#provisioned_capacity}
        '''
        if isinstance(autoscaling, dict):
            autoscaling = MskconnectConnectorCapacityAutoscaling(**autoscaling)
        if isinstance(provisioned_capacity, dict):
            provisioned_capacity = MskconnectConnectorCapacityProvisionedCapacity(**provisioned_capacity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf91c1f1df450e08abe63976d429fd7c56f061a802a9040625675aae5a10f9c)
            check_type(argname="argument autoscaling", value=autoscaling, expected_type=type_hints["autoscaling"])
            check_type(argname="argument provisioned_capacity", value=provisioned_capacity, expected_type=type_hints["provisioned_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscaling is not None:
            self._values["autoscaling"] = autoscaling
        if provisioned_capacity is not None:
            self._values["provisioned_capacity"] = provisioned_capacity

    @builtins.property
    def autoscaling(self) -> typing.Optional["MskconnectConnectorCapacityAutoscaling"]:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#autoscaling MskconnectConnector#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional["MskconnectConnectorCapacityAutoscaling"], result)

    @builtins.property
    def provisioned_capacity(
        self,
    ) -> typing.Optional["MskconnectConnectorCapacityProvisionedCapacity"]:
        '''provisioned_capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#provisioned_capacity MskconnectConnector#provisioned_capacity}
        '''
        result = self._values.get("provisioned_capacity")
        return typing.cast(typing.Optional["MskconnectConnectorCapacityProvisionedCapacity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityAutoscaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_worker_count": "maxWorkerCount",
        "min_worker_count": "minWorkerCount",
        "mcu_count": "mcuCount",
        "scale_in_policy": "scaleInPolicy",
        "scale_out_policy": "scaleOutPolicy",
    },
)
class MskconnectConnectorCapacityAutoscaling:
    def __init__(
        self,
        *,
        max_worker_count: jsii.Number,
        min_worker_count: jsii.Number,
        mcu_count: typing.Optional[jsii.Number] = None,
        scale_in_policy: typing.Optional[typing.Union["MskconnectConnectorCapacityAutoscalingScaleInPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        scale_out_policy: typing.Optional[typing.Union["MskconnectConnectorCapacityAutoscalingScaleOutPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#max_worker_count MskconnectConnector#max_worker_count}.
        :param min_worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#min_worker_count MskconnectConnector#min_worker_count}.
        :param mcu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#mcu_count MskconnectConnector#mcu_count}.
        :param scale_in_policy: scale_in_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#scale_in_policy MskconnectConnector#scale_in_policy}
        :param scale_out_policy: scale_out_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#scale_out_policy MskconnectConnector#scale_out_policy}
        '''
        if isinstance(scale_in_policy, dict):
            scale_in_policy = MskconnectConnectorCapacityAutoscalingScaleInPolicy(**scale_in_policy)
        if isinstance(scale_out_policy, dict):
            scale_out_policy = MskconnectConnectorCapacityAutoscalingScaleOutPolicy(**scale_out_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89352ced8eeefe4ef2f6e73e865a0b098294cc05490b3f12685e8707f4f643c)
            check_type(argname="argument max_worker_count", value=max_worker_count, expected_type=type_hints["max_worker_count"])
            check_type(argname="argument min_worker_count", value=min_worker_count, expected_type=type_hints["min_worker_count"])
            check_type(argname="argument mcu_count", value=mcu_count, expected_type=type_hints["mcu_count"])
            check_type(argname="argument scale_in_policy", value=scale_in_policy, expected_type=type_hints["scale_in_policy"])
            check_type(argname="argument scale_out_policy", value=scale_out_policy, expected_type=type_hints["scale_out_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_worker_count": max_worker_count,
            "min_worker_count": min_worker_count,
        }
        if mcu_count is not None:
            self._values["mcu_count"] = mcu_count
        if scale_in_policy is not None:
            self._values["scale_in_policy"] = scale_in_policy
        if scale_out_policy is not None:
            self._values["scale_out_policy"] = scale_out_policy

    @builtins.property
    def max_worker_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#max_worker_count MskconnectConnector#max_worker_count}.'''
        result = self._values.get("max_worker_count")
        assert result is not None, "Required property 'max_worker_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_worker_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#min_worker_count MskconnectConnector#min_worker_count}.'''
        result = self._values.get("min_worker_count")
        assert result is not None, "Required property 'min_worker_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def mcu_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#mcu_count MskconnectConnector#mcu_count}.'''
        result = self._values.get("mcu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_in_policy(
        self,
    ) -> typing.Optional["MskconnectConnectorCapacityAutoscalingScaleInPolicy"]:
        '''scale_in_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#scale_in_policy MskconnectConnector#scale_in_policy}
        '''
        result = self._values.get("scale_in_policy")
        return typing.cast(typing.Optional["MskconnectConnectorCapacityAutoscalingScaleInPolicy"], result)

    @builtins.property
    def scale_out_policy(
        self,
    ) -> typing.Optional["MskconnectConnectorCapacityAutoscalingScaleOutPolicy"]:
        '''scale_out_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#scale_out_policy MskconnectConnector#scale_out_policy}
        '''
        result = self._values.get("scale_out_policy")
        return typing.cast(typing.Optional["MskconnectConnectorCapacityAutoscalingScaleOutPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorCapacityAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorCapacityAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c612cf1480325665302788c556f0f887e84b404aec69e1a362bb2c47c81d9122)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScaleInPolicy")
    def put_scale_in_policy(
        self,
        *,
        cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_utilization_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cpu_utilization_percentage MskconnectConnector#cpu_utilization_percentage}.
        '''
        value = MskconnectConnectorCapacityAutoscalingScaleInPolicy(
            cpu_utilization_percentage=cpu_utilization_percentage
        )

        return typing.cast(None, jsii.invoke(self, "putScaleInPolicy", [value]))

    @jsii.member(jsii_name="putScaleOutPolicy")
    def put_scale_out_policy(
        self,
        *,
        cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_utilization_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cpu_utilization_percentage MskconnectConnector#cpu_utilization_percentage}.
        '''
        value = MskconnectConnectorCapacityAutoscalingScaleOutPolicy(
            cpu_utilization_percentage=cpu_utilization_percentage
        )

        return typing.cast(None, jsii.invoke(self, "putScaleOutPolicy", [value]))

    @jsii.member(jsii_name="resetMcuCount")
    def reset_mcu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMcuCount", []))

    @jsii.member(jsii_name="resetScaleInPolicy")
    def reset_scale_in_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleInPolicy", []))

    @jsii.member(jsii_name="resetScaleOutPolicy")
    def reset_scale_out_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleOutPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="scaleInPolicy")
    def scale_in_policy(
        self,
    ) -> "MskconnectConnectorCapacityAutoscalingScaleInPolicyOutputReference":
        return typing.cast("MskconnectConnectorCapacityAutoscalingScaleInPolicyOutputReference", jsii.get(self, "scaleInPolicy"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutPolicy")
    def scale_out_policy(
        self,
    ) -> "MskconnectConnectorCapacityAutoscalingScaleOutPolicyOutputReference":
        return typing.cast("MskconnectConnectorCapacityAutoscalingScaleOutPolicyOutputReference", jsii.get(self, "scaleOutPolicy"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkerCountInput")
    def max_worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="mcuCountInput")
    def mcu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mcuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minWorkerCountInput")
    def min_worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWorkerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInPolicyInput")
    def scale_in_policy_input(
        self,
    ) -> typing.Optional["MskconnectConnectorCapacityAutoscalingScaleInPolicy"]:
        return typing.cast(typing.Optional["MskconnectConnectorCapacityAutoscalingScaleInPolicy"], jsii.get(self, "scaleInPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutPolicyInput")
    def scale_out_policy_input(
        self,
    ) -> typing.Optional["MskconnectConnectorCapacityAutoscalingScaleOutPolicy"]:
        return typing.cast(typing.Optional["MskconnectConnectorCapacityAutoscalingScaleOutPolicy"], jsii.get(self, "scaleOutPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkerCount")
    def max_worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkerCount"))

    @max_worker_count.setter
    def max_worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b850ad888465324b9de85b277aff5be3d2b58a851a37fccbb5aea092b712a0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mcuCount")
    def mcu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mcuCount"))

    @mcu_count.setter
    def mcu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5234d485baf89823898f06f1952c350c048a85744ccac00b36cb8ad0cef229ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mcuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minWorkerCount")
    def min_worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minWorkerCount"))

    @min_worker_count.setter
    def min_worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a8323b0baf548b35216076881ba5abe361bc162fe0d4acdc0779dea35d5fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWorkerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskconnectConnectorCapacityAutoscaling]:
        return typing.cast(typing.Optional[MskconnectConnectorCapacityAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorCapacityAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9241d63ba1c1622d02a08b398594589011ab411348e5a99967c4f1b4e0479b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityAutoscalingScaleInPolicy",
    jsii_struct_bases=[],
    name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
)
class MskconnectConnectorCapacityAutoscalingScaleInPolicy:
    def __init__(
        self,
        *,
        cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_utilization_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cpu_utilization_percentage MskconnectConnector#cpu_utilization_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36e5f0cc7b61671f4831df2cb52d75fa37f1eafb12d6b8c975d0320f6d581b1)
            check_type(argname="argument cpu_utilization_percentage", value=cpu_utilization_percentage, expected_type=type_hints["cpu_utilization_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_utilization_percentage is not None:
            self._values["cpu_utilization_percentage"] = cpu_utilization_percentage

    @builtins.property
    def cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cpu_utilization_percentage MskconnectConnector#cpu_utilization_percentage}.'''
        result = self._values.get("cpu_utilization_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorCapacityAutoscalingScaleInPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorCapacityAutoscalingScaleInPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityAutoscalingScaleInPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0712cbca95d7843036607e669e53e2a60e85dd2a33dc79fcab49fa29764c1882)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuUtilizationPercentage")
    def reset_cpu_utilization_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuUtilizationPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationPercentageInput")
    def cpu_utilization_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuUtilizationPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationPercentage")
    def cpu_utilization_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuUtilizationPercentage"))

    @cpu_utilization_percentage.setter
    def cpu_utilization_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4d3471ecd4ceb5960afcb3b5d34d849869c72ecc0c2e089808dbeed2028aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuUtilizationPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorCapacityAutoscalingScaleInPolicy]:
        return typing.cast(typing.Optional[MskconnectConnectorCapacityAutoscalingScaleInPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorCapacityAutoscalingScaleInPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d8f4ba963bba4591b88449e0e89de0ef43eb322a570ff1e4d586167ef23e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityAutoscalingScaleOutPolicy",
    jsii_struct_bases=[],
    name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
)
class MskconnectConnectorCapacityAutoscalingScaleOutPolicy:
    def __init__(
        self,
        *,
        cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_utilization_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cpu_utilization_percentage MskconnectConnector#cpu_utilization_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1feded701bb020251afe6f30b70f36d04f94a2db7e84d5ba8b6afe18164fcc)
            check_type(argname="argument cpu_utilization_percentage", value=cpu_utilization_percentage, expected_type=type_hints["cpu_utilization_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_utilization_percentage is not None:
            self._values["cpu_utilization_percentage"] = cpu_utilization_percentage

    @builtins.property
    def cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cpu_utilization_percentage MskconnectConnector#cpu_utilization_percentage}.'''
        result = self._values.get("cpu_utilization_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorCapacityAutoscalingScaleOutPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorCapacityAutoscalingScaleOutPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityAutoscalingScaleOutPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8158b8b5c73253119a7f2c21ebf3e4df1c30737fbcb1b495271f0bdec356bad9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuUtilizationPercentage")
    def reset_cpu_utilization_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuUtilizationPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationPercentageInput")
    def cpu_utilization_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuUtilizationPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationPercentage")
    def cpu_utilization_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuUtilizationPercentage"))

    @cpu_utilization_percentage.setter
    def cpu_utilization_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f37a438227e8765c8c8d06181b27408bde85b8d2c752f499fe5fc465baade6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuUtilizationPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorCapacityAutoscalingScaleOutPolicy]:
        return typing.cast(typing.Optional[MskconnectConnectorCapacityAutoscalingScaleOutPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorCapacityAutoscalingScaleOutPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4aac134791d6a817df8d9926e530a467067ca41ce16570b712bbe1fe75ad218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskconnectConnectorCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc32f55278b88f75462229ce8b61455506376f473726dea254d2081af5f8854)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscaling")
    def put_autoscaling(
        self,
        *,
        max_worker_count: jsii.Number,
        min_worker_count: jsii.Number,
        mcu_count: typing.Optional[jsii.Number] = None,
        scale_in_policy: typing.Optional[typing.Union[MskconnectConnectorCapacityAutoscalingScaleInPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        scale_out_policy: typing.Optional[typing.Union[MskconnectConnectorCapacityAutoscalingScaleOutPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param max_worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#max_worker_count MskconnectConnector#max_worker_count}.
        :param min_worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#min_worker_count MskconnectConnector#min_worker_count}.
        :param mcu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#mcu_count MskconnectConnector#mcu_count}.
        :param scale_in_policy: scale_in_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#scale_in_policy MskconnectConnector#scale_in_policy}
        :param scale_out_policy: scale_out_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#scale_out_policy MskconnectConnector#scale_out_policy}
        '''
        value = MskconnectConnectorCapacityAutoscaling(
            max_worker_count=max_worker_count,
            min_worker_count=min_worker_count,
            mcu_count=mcu_count,
            scale_in_policy=scale_in_policy,
            scale_out_policy=scale_out_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putProvisionedCapacity")
    def put_provisioned_capacity(
        self,
        *,
        worker_count: jsii.Number,
        mcu_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_count MskconnectConnector#worker_count}.
        :param mcu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#mcu_count MskconnectConnector#mcu_count}.
        '''
        value = MskconnectConnectorCapacityProvisionedCapacity(
            worker_count=worker_count, mcu_count=mcu_count
        )

        return typing.cast(None, jsii.invoke(self, "putProvisionedCapacity", [value]))

    @jsii.member(jsii_name="resetAutoscaling")
    def reset_autoscaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaling", []))

    @jsii.member(jsii_name="resetProvisionedCapacity")
    def reset_provisioned_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="autoscaling")
    def autoscaling(self) -> MskconnectConnectorCapacityAutoscalingOutputReference:
        return typing.cast(MskconnectConnectorCapacityAutoscalingOutputReference, jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="provisionedCapacity")
    def provisioned_capacity(
        self,
    ) -> "MskconnectConnectorCapacityProvisionedCapacityOutputReference":
        return typing.cast("MskconnectConnectorCapacityProvisionedCapacityOutputReference", jsii.get(self, "provisionedCapacity"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingInput")
    def autoscaling_input(
        self,
    ) -> typing.Optional[MskconnectConnectorCapacityAutoscaling]:
        return typing.cast(typing.Optional[MskconnectConnectorCapacityAutoscaling], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedCapacityInput")
    def provisioned_capacity_input(
        self,
    ) -> typing.Optional["MskconnectConnectorCapacityProvisionedCapacity"]:
        return typing.cast(typing.Optional["MskconnectConnectorCapacityProvisionedCapacity"], jsii.get(self, "provisionedCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskconnectConnectorCapacity]:
        return typing.cast(typing.Optional[MskconnectConnectorCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0474dff3f2ac1b6fcb357191a29b68e46d13ff6a3c10b427ef83af0550e15039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityProvisionedCapacity",
    jsii_struct_bases=[],
    name_mapping={"worker_count": "workerCount", "mcu_count": "mcuCount"},
)
class MskconnectConnectorCapacityProvisionedCapacity:
    def __init__(
        self,
        *,
        worker_count: jsii.Number,
        mcu_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_count MskconnectConnector#worker_count}.
        :param mcu_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#mcu_count MskconnectConnector#mcu_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a6ab317e3236a55fbd5f1542ebd7c5feeb5a5d23150b8cc3b78e6630e46e76)
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            check_type(argname="argument mcu_count", value=mcu_count, expected_type=type_hints["mcu_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "worker_count": worker_count,
        }
        if mcu_count is not None:
            self._values["mcu_count"] = mcu_count

    @builtins.property
    def worker_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_count MskconnectConnector#worker_count}.'''
        result = self._values.get("worker_count")
        assert result is not None, "Required property 'worker_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def mcu_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#mcu_count MskconnectConnector#mcu_count}.'''
        result = self._values.get("mcu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorCapacityProvisionedCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorCapacityProvisionedCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorCapacityProvisionedCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab3744c2fd95c905c7d8faf8e85606bb9447f7bccf43fa084c6152f76ca16e9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMcuCount")
    def reset_mcu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMcuCount", []))

    @builtins.property
    @jsii.member(jsii_name="mcuCountInput")
    def mcu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mcuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCountInput")
    def worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="mcuCount")
    def mcu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mcuCount"))

    @mcu_count.setter
    def mcu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2807c90ae7686a17bcc86902e298d4d819a332cebebea923206881cb7f806d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mcuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @worker_count.setter
    def worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bb03f13e0dc528ea97b391c669c7548c74db7045f2e27fc1edb833f4c74657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorCapacityProvisionedCapacity]:
        return typing.cast(typing.Optional[MskconnectConnectorCapacityProvisionedCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorCapacityProvisionedCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17131faacdcb57a8271d51531d98e2754418788c6133c0dccaec8b4d660a8ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capacity": "capacity",
        "connector_configuration": "connectorConfiguration",
        "kafka_cluster": "kafkaCluster",
        "kafka_cluster_client_authentication": "kafkaClusterClientAuthentication",
        "kafka_cluster_encryption_in_transit": "kafkaClusterEncryptionInTransit",
        "kafkaconnect_version": "kafkaconnectVersion",
        "name": "name",
        "plugin": "plugin",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "description": "description",
        "id": "id",
        "log_delivery": "logDelivery",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "worker_configuration": "workerConfiguration",
    },
)
class MskconnectConnectorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity: typing.Union[MskconnectConnectorCapacity, typing.Dict[builtins.str, typing.Any]],
        connector_configuration: typing.Mapping[builtins.str, builtins.str],
        kafka_cluster: typing.Union["MskconnectConnectorKafkaCluster", typing.Dict[builtins.str, typing.Any]],
        kafka_cluster_client_authentication: typing.Union["MskconnectConnectorKafkaClusterClientAuthentication", typing.Dict[builtins.str, typing.Any]],
        kafka_cluster_encryption_in_transit: typing.Union["MskconnectConnectorKafkaClusterEncryptionInTransit", typing.Dict[builtins.str, typing.Any]],
        kafkaconnect_version: builtins.str,
        name: builtins.str,
        plugin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskconnectConnectorPlugin", typing.Dict[builtins.str, typing.Any]]]],
        service_execution_role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union["MskconnectConnectorLogDelivery", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MskconnectConnectorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_configuration: typing.Optional[typing.Union["MskconnectConnectorWorkerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#capacity MskconnectConnector#capacity}
        :param connector_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#connector_configuration MskconnectConnector#connector_configuration}.
        :param kafka_cluster: kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster MskconnectConnector#kafka_cluster}
        :param kafka_cluster_client_authentication: kafka_cluster_client_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster_client_authentication MskconnectConnector#kafka_cluster_client_authentication}
        :param kafka_cluster_encryption_in_transit: kafka_cluster_encryption_in_transit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster_encryption_in_transit MskconnectConnector#kafka_cluster_encryption_in_transit}
        :param kafkaconnect_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafkaconnect_version MskconnectConnector#kafkaconnect_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#name MskconnectConnector#name}.
        :param plugin: plugin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#plugin MskconnectConnector#plugin}
        :param service_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#service_execution_role_arn MskconnectConnector#service_execution_role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#description MskconnectConnector#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#id MskconnectConnector#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_delivery: log_delivery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#log_delivery MskconnectConnector#log_delivery}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#region MskconnectConnector#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#tags MskconnectConnector#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#tags_all MskconnectConnector#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#timeouts MskconnectConnector#timeouts}
        :param worker_configuration: worker_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_configuration MskconnectConnector#worker_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity, dict):
            capacity = MskconnectConnectorCapacity(**capacity)
        if isinstance(kafka_cluster, dict):
            kafka_cluster = MskconnectConnectorKafkaCluster(**kafka_cluster)
        if isinstance(kafka_cluster_client_authentication, dict):
            kafka_cluster_client_authentication = MskconnectConnectorKafkaClusterClientAuthentication(**kafka_cluster_client_authentication)
        if isinstance(kafka_cluster_encryption_in_transit, dict):
            kafka_cluster_encryption_in_transit = MskconnectConnectorKafkaClusterEncryptionInTransit(**kafka_cluster_encryption_in_transit)
        if isinstance(log_delivery, dict):
            log_delivery = MskconnectConnectorLogDelivery(**log_delivery)
        if isinstance(timeouts, dict):
            timeouts = MskconnectConnectorTimeouts(**timeouts)
        if isinstance(worker_configuration, dict):
            worker_configuration = MskconnectConnectorWorkerConfiguration(**worker_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4055dab2bb266918c58b3ed9e28f0aa1e7113ad3c55f3fe730b5c6af7a6d2e2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument connector_configuration", value=connector_configuration, expected_type=type_hints["connector_configuration"])
            check_type(argname="argument kafka_cluster", value=kafka_cluster, expected_type=type_hints["kafka_cluster"])
            check_type(argname="argument kafka_cluster_client_authentication", value=kafka_cluster_client_authentication, expected_type=type_hints["kafka_cluster_client_authentication"])
            check_type(argname="argument kafka_cluster_encryption_in_transit", value=kafka_cluster_encryption_in_transit, expected_type=type_hints["kafka_cluster_encryption_in_transit"])
            check_type(argname="argument kafkaconnect_version", value=kafkaconnect_version, expected_type=type_hints["kafkaconnect_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plugin", value=plugin, expected_type=type_hints["plugin"])
            check_type(argname="argument service_execution_role_arn", value=service_execution_role_arn, expected_type=type_hints["service_execution_role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity": capacity,
            "connector_configuration": connector_configuration,
            "kafka_cluster": kafka_cluster,
            "kafka_cluster_client_authentication": kafka_cluster_client_authentication,
            "kafka_cluster_encryption_in_transit": kafka_cluster_encryption_in_transit,
            "kafkaconnect_version": kafkaconnect_version,
            "name": name,
            "plugin": plugin,
            "service_execution_role_arn": service_execution_role_arn,
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
        if id is not None:
            self._values["id"] = id
        if log_delivery is not None:
            self._values["log_delivery"] = log_delivery
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if worker_configuration is not None:
            self._values["worker_configuration"] = worker_configuration

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
    def capacity(self) -> MskconnectConnectorCapacity:
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#capacity MskconnectConnector#capacity}
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(MskconnectConnectorCapacity, result)

    @builtins.property
    def connector_configuration(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#connector_configuration MskconnectConnector#connector_configuration}.'''
        result = self._values.get("connector_configuration")
        assert result is not None, "Required property 'connector_configuration' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def kafka_cluster(self) -> "MskconnectConnectorKafkaCluster":
        '''kafka_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster MskconnectConnector#kafka_cluster}
        '''
        result = self._values.get("kafka_cluster")
        assert result is not None, "Required property 'kafka_cluster' is missing"
        return typing.cast("MskconnectConnectorKafkaCluster", result)

    @builtins.property
    def kafka_cluster_client_authentication(
        self,
    ) -> "MskconnectConnectorKafkaClusterClientAuthentication":
        '''kafka_cluster_client_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster_client_authentication MskconnectConnector#kafka_cluster_client_authentication}
        '''
        result = self._values.get("kafka_cluster_client_authentication")
        assert result is not None, "Required property 'kafka_cluster_client_authentication' is missing"
        return typing.cast("MskconnectConnectorKafkaClusterClientAuthentication", result)

    @builtins.property
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> "MskconnectConnectorKafkaClusterEncryptionInTransit":
        '''kafka_cluster_encryption_in_transit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafka_cluster_encryption_in_transit MskconnectConnector#kafka_cluster_encryption_in_transit}
        '''
        result = self._values.get("kafka_cluster_encryption_in_transit")
        assert result is not None, "Required property 'kafka_cluster_encryption_in_transit' is missing"
        return typing.cast("MskconnectConnectorKafkaClusterEncryptionInTransit", result)

    @builtins.property
    def kafkaconnect_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#kafkaconnect_version MskconnectConnector#kafkaconnect_version}.'''
        result = self._values.get("kafkaconnect_version")
        assert result is not None, "Required property 'kafkaconnect_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#name MskconnectConnector#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskconnectConnectorPlugin"]]:
        '''plugin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#plugin MskconnectConnector#plugin}
        '''
        result = self._values.get("plugin")
        assert result is not None, "Required property 'plugin' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskconnectConnectorPlugin"]], result)

    @builtins.property
    def service_execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#service_execution_role_arn MskconnectConnector#service_execution_role_arn}.'''
        result = self._values.get("service_execution_role_arn")
        assert result is not None, "Required property 'service_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#description MskconnectConnector#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#id MskconnectConnector#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery(self) -> typing.Optional["MskconnectConnectorLogDelivery"]:
        '''log_delivery block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#log_delivery MskconnectConnector#log_delivery}
        '''
        result = self._values.get("log_delivery")
        return typing.cast(typing.Optional["MskconnectConnectorLogDelivery"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#region MskconnectConnector#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#tags MskconnectConnector#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#tags_all MskconnectConnector#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MskconnectConnectorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#timeouts MskconnectConnector#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MskconnectConnectorTimeouts"], result)

    @builtins.property
    def worker_configuration(
        self,
    ) -> typing.Optional["MskconnectConnectorWorkerConfiguration"]:
        '''worker_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_configuration MskconnectConnector#worker_configuration}
        '''
        result = self._values.get("worker_configuration")
        return typing.cast(typing.Optional["MskconnectConnectorWorkerConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaCluster",
    jsii_struct_bases=[],
    name_mapping={"apache_kafka_cluster": "apacheKafkaCluster"},
)
class MskconnectConnectorKafkaCluster:
    def __init__(
        self,
        *,
        apache_kafka_cluster: typing.Union["MskconnectConnectorKafkaClusterApacheKafkaCluster", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param apache_kafka_cluster: apache_kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#apache_kafka_cluster MskconnectConnector#apache_kafka_cluster}
        '''
        if isinstance(apache_kafka_cluster, dict):
            apache_kafka_cluster = MskconnectConnectorKafkaClusterApacheKafkaCluster(**apache_kafka_cluster)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e476d56542c89db3bf529f9a6e8a163ae67968b8fe06dcba9cd7a0a74d0454a)
            check_type(argname="argument apache_kafka_cluster", value=apache_kafka_cluster, expected_type=type_hints["apache_kafka_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "apache_kafka_cluster": apache_kafka_cluster,
        }

    @builtins.property
    def apache_kafka_cluster(
        self,
    ) -> "MskconnectConnectorKafkaClusterApacheKafkaCluster":
        '''apache_kafka_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#apache_kafka_cluster MskconnectConnector#apache_kafka_cluster}
        '''
        result = self._values.get("apache_kafka_cluster")
        assert result is not None, "Required property 'apache_kafka_cluster' is missing"
        return typing.cast("MskconnectConnectorKafkaClusterApacheKafkaCluster", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorKafkaCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterApacheKafkaCluster",
    jsii_struct_bases=[],
    name_mapping={"bootstrap_servers": "bootstrapServers", "vpc": "vpc"},
)
class MskconnectConnectorKafkaClusterApacheKafkaCluster:
    def __init__(
        self,
        *,
        bootstrap_servers: builtins.str,
        vpc: typing.Union["MskconnectConnectorKafkaClusterApacheKafkaClusterVpc", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param bootstrap_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#bootstrap_servers MskconnectConnector#bootstrap_servers}.
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#vpc MskconnectConnector#vpc}
        '''
        if isinstance(vpc, dict):
            vpc = MskconnectConnectorKafkaClusterApacheKafkaClusterVpc(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfaf370b3ba94c3681749e7607e89ec1c9e5392d506d4d5b4d18405a940ed3b3)
            check_type(argname="argument bootstrap_servers", value=bootstrap_servers, expected_type=type_hints["bootstrap_servers"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bootstrap_servers": bootstrap_servers,
            "vpc": vpc,
        }

    @builtins.property
    def bootstrap_servers(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#bootstrap_servers MskconnectConnector#bootstrap_servers}.'''
        result = self._values.get("bootstrap_servers")
        assert result is not None, "Required property 'bootstrap_servers' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> "MskconnectConnectorKafkaClusterApacheKafkaClusterVpc":
        '''vpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#vpc MskconnectConnector#vpc}
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("MskconnectConnectorKafkaClusterApacheKafkaClusterVpc", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorKafkaClusterApacheKafkaCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorKafkaClusterApacheKafkaClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterApacheKafkaClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4281f926358159d69ea38021b2e146b5b433082d0a7da554f9d6aef8e0c6a866)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVpc")
    def put_vpc(
        self,
        *,
        security_groups: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#security_groups MskconnectConnector#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#subnets MskconnectConnector#subnets}.
        '''
        value = MskconnectConnectorKafkaClusterApacheKafkaClusterVpc(
            security_groups=security_groups, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpc", [value]))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(
        self,
    ) -> "MskconnectConnectorKafkaClusterApacheKafkaClusterVpcOutputReference":
        return typing.cast("MskconnectConnectorKafkaClusterApacheKafkaClusterVpcOutputReference", jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapServersInput")
    def bootstrap_servers_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootstrapServersInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(
        self,
    ) -> typing.Optional["MskconnectConnectorKafkaClusterApacheKafkaClusterVpc"]:
        return typing.cast(typing.Optional["MskconnectConnectorKafkaClusterApacheKafkaClusterVpc"], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapServers")
    def bootstrap_servers(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootstrapServers"))

    @bootstrap_servers.setter
    def bootstrap_servers(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28d4addb24cbfdd7ed465ad1ddc7bca5a1a68c5f919feb15ba85915c5981d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrapServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaCluster]:
        return typing.cast(typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8836ddc675e2c89469144b70c4b350799bfa55e285a122981b73cd698df7dfee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterApacheKafkaClusterVpc",
    jsii_struct_bases=[],
    name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
)
class MskconnectConnectorKafkaClusterApacheKafkaClusterVpc:
    def __init__(
        self,
        *,
        security_groups: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#security_groups MskconnectConnector#security_groups}.
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#subnets MskconnectConnector#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34898f44fb6158e57b5e84e61f5f4b3b9bc0cab059c39359db6332c9d95e456)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_groups": security_groups,
            "subnets": subnets,
        }

    @builtins.property
    def security_groups(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#security_groups MskconnectConnector#security_groups}.'''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#subnets MskconnectConnector#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorKafkaClusterApacheKafkaClusterVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorKafkaClusterApacheKafkaClusterVpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterApacheKafkaClusterVpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeeabbaf9e91991e44000321529be6badbd76a9a9262aff3b10481d68b3bb269)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__ebae8ed389dd16d735dc5febb9539ff26edfbddd0709c50a9fa42e7190da2670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf06c1c39b4c9a7dd5eabec3071eb2fe9333154fbe1bc9553286dedb36a6037e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaClusterVpc]:
        return typing.cast(typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaClusterVpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaClusterVpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4337611bf558c6a53aff7f4022c55985f1220a831d204c01ae4ac5961867195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterClientAuthentication",
    jsii_struct_bases=[],
    name_mapping={"authentication_type": "authenticationType"},
)
class MskconnectConnectorKafkaClusterClientAuthentication:
    def __init__(
        self,
        *,
        authentication_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#authentication_type MskconnectConnector#authentication_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca42d59cdeddb3aa24cd837ad917e065db8d10b03b037cd9f960cd32d1a54a9)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#authentication_type MskconnectConnector#authentication_type}.'''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorKafkaClusterClientAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorKafkaClusterClientAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterClientAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeff5af85db3d9e13d07605428408398205dcbb909725ca109591d5cdf722b74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationType")
    def reset_authentication_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationType", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffae2eabb07c43558814b01a9406d3ca482f912accd6adf93ef60816099000e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorKafkaClusterClientAuthentication]:
        return typing.cast(typing.Optional[MskconnectConnectorKafkaClusterClientAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorKafkaClusterClientAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f654fcab20d8f28ba8c010ba5f8416975e7e4830d5775c72d9e0be809a9dccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterEncryptionInTransit",
    jsii_struct_bases=[],
    name_mapping={"encryption_type": "encryptionType"},
)
class MskconnectConnectorKafkaClusterEncryptionInTransit:
    def __init__(
        self,
        *,
        encryption_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#encryption_type MskconnectConnector#encryption_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e08324528daca6f641519181c1797d55b68beb0d08a65f0ecb7460515004cc)
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#encryption_type MskconnectConnector#encryption_type}.'''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorKafkaClusterEncryptionInTransit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorKafkaClusterEncryptionInTransitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterEncryptionInTransitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef97b1cfa28e07847d588f22ad5178e99401614df6f391ddcfa030ba0e9096e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfaf1c38cf11771a311eab8e71cdd5499cf1a8888fe40815f37976ca4033cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorKafkaClusterEncryptionInTransit]:
        return typing.cast(typing.Optional[MskconnectConnectorKafkaClusterEncryptionInTransit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorKafkaClusterEncryptionInTransit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd94a66a0c4fe9afe9abf62e35561fb77803c4376204e6d1098500bfee06455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskconnectConnectorKafkaClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorKafkaClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b79245117748f9bc5ec7deb2d0f5b85ba987eaec47adec72985ec7b6de7530b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApacheKafkaCluster")
    def put_apache_kafka_cluster(
        self,
        *,
        bootstrap_servers: builtins.str,
        vpc: typing.Union[MskconnectConnectorKafkaClusterApacheKafkaClusterVpc, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param bootstrap_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#bootstrap_servers MskconnectConnector#bootstrap_servers}.
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#vpc MskconnectConnector#vpc}
        '''
        value = MskconnectConnectorKafkaClusterApacheKafkaCluster(
            bootstrap_servers=bootstrap_servers, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "putApacheKafkaCluster", [value]))

    @builtins.property
    @jsii.member(jsii_name="apacheKafkaCluster")
    def apache_kafka_cluster(
        self,
    ) -> MskconnectConnectorKafkaClusterApacheKafkaClusterOutputReference:
        return typing.cast(MskconnectConnectorKafkaClusterApacheKafkaClusterOutputReference, jsii.get(self, "apacheKafkaCluster"))

    @builtins.property
    @jsii.member(jsii_name="apacheKafkaClusterInput")
    def apache_kafka_cluster_input(
        self,
    ) -> typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaCluster]:
        return typing.cast(typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaCluster], jsii.get(self, "apacheKafkaClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskconnectConnectorKafkaCluster]:
        return typing.cast(typing.Optional[MskconnectConnectorKafkaCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorKafkaCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21886e9e031b83609e8bd87bdafec4deb427b82bfec37504164385a05ec141ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDelivery",
    jsii_struct_bases=[],
    name_mapping={"worker_log_delivery": "workerLogDelivery"},
)
class MskconnectConnectorLogDelivery:
    def __init__(
        self,
        *,
        worker_log_delivery: typing.Union["MskconnectConnectorLogDeliveryWorkerLogDelivery", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param worker_log_delivery: worker_log_delivery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_log_delivery MskconnectConnector#worker_log_delivery}
        '''
        if isinstance(worker_log_delivery, dict):
            worker_log_delivery = MskconnectConnectorLogDeliveryWorkerLogDelivery(**worker_log_delivery)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b0b310cb415dde9337634bad861588b5b1ad01c1dd25cec8c1ab2ae6f0c23f)
            check_type(argname="argument worker_log_delivery", value=worker_log_delivery, expected_type=type_hints["worker_log_delivery"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "worker_log_delivery": worker_log_delivery,
        }

    @builtins.property
    def worker_log_delivery(self) -> "MskconnectConnectorLogDeliveryWorkerLogDelivery":
        '''worker_log_delivery block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#worker_log_delivery MskconnectConnector#worker_log_delivery}
        '''
        result = self._values.get("worker_log_delivery")
        assert result is not None, "Required property 'worker_log_delivery' is missing"
        return typing.cast("MskconnectConnectorLogDeliveryWorkerLogDelivery", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorLogDelivery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorLogDeliveryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18cd0fa1b14cacd0178af1c7fe238363d5a8f401d64d339253dbe8abb8bd83cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWorkerLogDelivery")
    def put_worker_log_delivery(
        self,
        *,
        cloudwatch_logs: typing.Optional[typing.Union["MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union["MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["MskconnectConnectorLogDeliveryWorkerLogDeliveryS3", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cloudwatch_logs MskconnectConnector#cloudwatch_logs}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#firehose MskconnectConnector#firehose}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#s3 MskconnectConnector#s3}
        '''
        value = MskconnectConnectorLogDeliveryWorkerLogDelivery(
            cloudwatch_logs=cloudwatch_logs, firehose=firehose, s3=s3
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerLogDelivery", [value]))

    @builtins.property
    @jsii.member(jsii_name="workerLogDelivery")
    def worker_log_delivery(
        self,
    ) -> "MskconnectConnectorLogDeliveryWorkerLogDeliveryOutputReference":
        return typing.cast("MskconnectConnectorLogDeliveryWorkerLogDeliveryOutputReference", jsii.get(self, "workerLogDelivery"))

    @builtins.property
    @jsii.member(jsii_name="workerLogDeliveryInput")
    def worker_log_delivery_input(
        self,
    ) -> typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDelivery"]:
        return typing.cast(typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDelivery"], jsii.get(self, "workerLogDeliveryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskconnectConnectorLogDelivery]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDelivery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorLogDelivery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52cb5fba16c68dfa91906eca161772415d8be0c4f678792557c72e0190cc0965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDelivery",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_logs": "cloudwatchLogs",
        "firehose": "firehose",
        "s3": "s3",
    },
)
class MskconnectConnectorLogDeliveryWorkerLogDelivery:
    def __init__(
        self,
        *,
        cloudwatch_logs: typing.Optional[typing.Union["MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union["MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["MskconnectConnectorLogDeliveryWorkerLogDeliveryS3", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cloudwatch_logs MskconnectConnector#cloudwatch_logs}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#firehose MskconnectConnector#firehose}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#s3 MskconnectConnector#s3}
        '''
        if isinstance(cloudwatch_logs, dict):
            cloudwatch_logs = MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs(**cloudwatch_logs)
        if isinstance(firehose, dict):
            firehose = MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose(**firehose)
        if isinstance(s3, dict):
            s3 = MskconnectConnectorLogDeliveryWorkerLogDeliveryS3(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb40436bd5562c1d2c2561fa4959c4033faef685307c23851a126a3fe429260)
            check_type(argname="argument cloudwatch_logs", value=cloudwatch_logs, expected_type=type_hints["cloudwatch_logs"])
            check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_logs is not None:
            self._values["cloudwatch_logs"] = cloudwatch_logs
        if firehose is not None:
            self._values["firehose"] = firehose
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def cloudwatch_logs(
        self,
    ) -> typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs"]:
        '''cloudwatch_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#cloudwatch_logs MskconnectConnector#cloudwatch_logs}
        '''
        result = self._values.get("cloudwatch_logs")
        return typing.cast(typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs"], result)

    @builtins.property
    def firehose(
        self,
    ) -> typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose"]:
        '''firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#firehose MskconnectConnector#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#s3 MskconnectConnector#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryS3"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorLogDeliveryWorkerLogDelivery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_group": "logGroup"},
)
class MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.
        :param log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#log_group MskconnectConnector#log_group}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc6045140c459c1f73413425a2047868f6a502ce0da7f9108c45eaaa2725b93)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if log_group is not None:
            self._values["log_group"] = log_group

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#log_group MskconnectConnector#log_group}.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33e8630ee3444312c3dcffa42acd444f4d3711f7278453ea3400cd6620ba067b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogGroup")
    def reset_log_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroup", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupInput")
    def log_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8e2aa04988e49de573ab1ccc657fb4849140c84c0430993bd4dbdb2215f18739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroup"))

    @log_group.setter
    def log_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d4cc42d72350ecae8b6c3173f2ad3700d9a197720b2666f0acfc96510caa50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3506c8e88c913807ce59dcb6843e572175c4a1002dccccf739c8dcad5510b3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "delivery_stream": "deliveryStream"},
)
class MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        delivery_stream: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.
        :param delivery_stream: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#delivery_stream MskconnectConnector#delivery_stream}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79149c1a5fa6246f8cb01ad6b0a7badb0d14efcdf3f5281e076a8d9d3f881fa5)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if delivery_stream is not None:
            self._values["delivery_stream"] = delivery_stream

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def delivery_stream(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#delivery_stream MskconnectConnector#delivery_stream}.'''
        result = self._values.get("delivery_stream")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd81d68e0bbf2b041b07162a66251b8c56c3174e8409bce55037d88d757ae27e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeliveryStream")
    def reset_delivery_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryStream", []))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamInput")
    def delivery_stream_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStream")
    def delivery_stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStream"))

    @delivery_stream.setter
    def delivery_stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7b8affed3b80ff963ebc0e09fb73acb3fd2ae5bd245799716bed09169821e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStream", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__e6bcaa90e63828f84fe15ab4483ff98d26250abded64d9f9fad2d44efa14d73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432f14ae059f7849e62e5a41487fba42ea8ac509bd9a3294f399524f390c7a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskconnectConnectorLogDeliveryWorkerLogDeliveryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8132efce950f054fab05d74d2617c3ee7945dde82a1546122c2c822a3cfe0614)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogs")
    def put_cloudwatch_logs(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.
        :param log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#log_group MskconnectConnector#log_group}.
        '''
        value = MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs(
            enabled=enabled, log_group=log_group
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogs", [value]))

    @jsii.member(jsii_name="putFirehose")
    def put_firehose(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        delivery_stream: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.
        :param delivery_stream: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#delivery_stream MskconnectConnector#delivery_stream}.
        '''
        value = MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose(
            enabled=enabled, delivery_stream=delivery_stream
        )

        return typing.cast(None, jsii.invoke(self, "putFirehose", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        bucket: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#bucket MskconnectConnector#bucket}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#prefix MskconnectConnector#prefix}.
        '''
        value = MskconnectConnectorLogDeliveryWorkerLogDeliveryS3(
            enabled=enabled, bucket=bucket, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogs")
    def reset_cloudwatch_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogs", []))

    @jsii.member(jsii_name="resetFirehose")
    def reset_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehose", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogs")
    def cloudwatch_logs(
        self,
    ) -> MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogsOutputReference:
        return typing.cast(MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogsOutputReference, jsii.get(self, "cloudwatchLogs"))

    @builtins.property
    @jsii.member(jsii_name="firehose")
    def firehose(
        self,
    ) -> MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehoseOutputReference:
        return typing.cast(MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehoseOutputReference, jsii.get(self, "firehose"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "MskconnectConnectorLogDeliveryWorkerLogDeliveryS3OutputReference":
        return typing.cast("MskconnectConnectorLogDeliveryWorkerLogDeliveryS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsInput")
    def cloudwatch_logs_input(
        self,
    ) -> typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs], jsii.get(self, "cloudwatchLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseInput")
    def firehose_input(
        self,
    ) -> typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose], jsii.get(self, "firehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryS3"]:
        return typing.cast(typing.Optional["MskconnectConnectorLogDeliveryWorkerLogDeliveryS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDelivery]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDelivery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDelivery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0b2c361193d07287961ff23a18aa6b4c595176db4edc63fd76a51467e8f272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryS3",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "bucket": "bucket", "prefix": "prefix"},
)
class MskconnectConnectorLogDeliveryWorkerLogDeliveryS3:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        bucket: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#bucket MskconnectConnector#bucket}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#prefix MskconnectConnector#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502d4aacc69e218f834ece3820d321fe2df52464e2fdbcbf5432f4efa4b29486)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#enabled MskconnectConnector#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#bucket MskconnectConnector#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#prefix MskconnectConnector#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorLogDeliveryWorkerLogDeliveryS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorLogDeliveryWorkerLogDeliveryS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorLogDeliveryWorkerLogDeliveryS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad19e12fab74578b7e7b5f0ef92d7bef88baafb22e41ba6593f533d0173b10b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06023d5ce2a1f48140c1f1fbcf1cc76572e00dde6456aca443458e7d21c4b826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1c7eb3c49dda27a045ff9cda7486d8618bb1a1c79a7867a669d597537a648b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644345e4087f0975713d33f7bfa5c55aec54a080362594359845fff7e141b3d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryS3]:
        return typing.cast(typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe33a8cc2323254e0bbe0d64fb22e5a6ef0d9c93605e98acb38afcb806ca23b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorPlugin",
    jsii_struct_bases=[],
    name_mapping={"custom_plugin": "customPlugin"},
)
class MskconnectConnectorPlugin:
    def __init__(
        self,
        *,
        custom_plugin: typing.Union["MskconnectConnectorPluginCustomPlugin", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param custom_plugin: custom_plugin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#custom_plugin MskconnectConnector#custom_plugin}
        '''
        if isinstance(custom_plugin, dict):
            custom_plugin = MskconnectConnectorPluginCustomPlugin(**custom_plugin)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3e14bee5d08b97f5666fa0de68859f86b5e740e7467df0a1206bc18c5cbf42)
            check_type(argname="argument custom_plugin", value=custom_plugin, expected_type=type_hints["custom_plugin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_plugin": custom_plugin,
        }

    @builtins.property
    def custom_plugin(self) -> "MskconnectConnectorPluginCustomPlugin":
        '''custom_plugin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#custom_plugin MskconnectConnector#custom_plugin}
        '''
        result = self._values.get("custom_plugin")
        assert result is not None, "Required property 'custom_plugin' is missing"
        return typing.cast("MskconnectConnectorPluginCustomPlugin", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorPlugin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorPluginCustomPlugin",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "revision": "revision"},
)
class MskconnectConnectorPluginCustomPlugin:
    def __init__(self, *, arn: builtins.str, revision: jsii.Number) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#arn MskconnectConnector#arn}.
        :param revision: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#revision MskconnectConnector#revision}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e1b18546f1f878e18e7e3d15138781d06772f882345ea05f9b36a2571e1873)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "revision": revision,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#arn MskconnectConnector#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def revision(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#revision MskconnectConnector#revision}.'''
        result = self._values.get("revision")
        assert result is not None, "Required property 'revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorPluginCustomPlugin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorPluginCustomPluginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorPluginCustomPluginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54326e4fdb922d218ca28f42c12ea80162e7a37b289f239d23a33dbcff386635)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2edeb8487e32c3d01d40109a395ef9d96f256873183dc904dd565df28e166e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcfc287ffa0c00a78e7ef8fc5c0248b2b6f233325f69fe2714fb8964e8955b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskconnectConnectorPluginCustomPlugin]:
        return typing.cast(typing.Optional[MskconnectConnectorPluginCustomPlugin], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorPluginCustomPlugin],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad2f497e7f172541ea7afe404a4ae9896de473e1f4e19f302c095411a4b075b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskconnectConnectorPluginList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorPluginList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0ee267b393c460364ef3cca355df7f4e8e8d6b62bece987dc5d0dff4b4b6e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MskconnectConnectorPluginOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37759f82a9872ea2954dd85b2e9b47632ba7ced6174644bb30131130cac58508)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskconnectConnectorPluginOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ee8f70bb3865f185acb9de9171649e0ca1dbea297673e5116fb7244c1effa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4a1df073dcc53fac395617d34384189ace72f188a228e03026eaeaaf71f0da0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda5e48731d472f99f6ce7ae8a28a05648a1b96984cd8ba5ce9213f75552f666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskconnectConnectorPlugin]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskconnectConnectorPlugin]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskconnectConnectorPlugin]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8925e232a76046301b651ea543e8fd43f422760aac66f4e77309cc3f3c16a829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskconnectConnectorPluginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorPluginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd70f21886db2079d58802b634f8b67ba3fb512121596073a035a40b78991da0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomPlugin")
    def put_custom_plugin(self, *, arn: builtins.str, revision: jsii.Number) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#arn MskconnectConnector#arn}.
        :param revision: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#revision MskconnectConnector#revision}.
        '''
        value = MskconnectConnectorPluginCustomPlugin(arn=arn, revision=revision)

        return typing.cast(None, jsii.invoke(self, "putCustomPlugin", [value]))

    @builtins.property
    @jsii.member(jsii_name="customPlugin")
    def custom_plugin(self) -> MskconnectConnectorPluginCustomPluginOutputReference:
        return typing.cast(MskconnectConnectorPluginCustomPluginOutputReference, jsii.get(self, "customPlugin"))

    @builtins.property
    @jsii.member(jsii_name="customPluginInput")
    def custom_plugin_input(
        self,
    ) -> typing.Optional[MskconnectConnectorPluginCustomPlugin]:
        return typing.cast(typing.Optional[MskconnectConnectorPluginCustomPlugin], jsii.get(self, "customPluginInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorPlugin]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorPlugin]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorPlugin]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13b53dc4b2f389ba3a047f87c677e0c9d2e0f3210a1359cdcc0aba3ed2b4551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MskconnectConnectorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#create MskconnectConnector#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#delete MskconnectConnector#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#update MskconnectConnector#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ebfcc1f8b1ec59655d4ecaebb0436e700d7f379e439ed270ce5ff07f5ccaf5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#create MskconnectConnector#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#delete MskconnectConnector#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#update MskconnectConnector#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2565b0bd171e82b89813b26a010c5c2d2f1fb56f0adbfc4ac130dbafb5923fdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3cf5702e3ef622334b384b809538bd499696e9ba0ad4b8fc4c0303491265c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d8a6d86179bb04dfb6531ef36865e5643c86e5e5ac206f3fca7f6e39236499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adbe885d00e1dc707fbd58944123cb27367aca26e8b96a4743639dd5f2b03b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776965d92a3e114660fbdbb2251f08e53205b9a3316069ca1b93559bec021ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorWorkerConfiguration",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "revision": "revision"},
)
class MskconnectConnectorWorkerConfiguration:
    def __init__(self, *, arn: builtins.str, revision: jsii.Number) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#arn MskconnectConnector#arn}.
        :param revision: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#revision MskconnectConnector#revision}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8403db3af1124d37c4fb9680e8c7e29a2320125ea0a5ffd55dd0bfdffcb4f3bc)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "revision": revision,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#arn MskconnectConnector#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def revision(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/mskconnect_connector#revision MskconnectConnector#revision}.'''
        result = self._values.get("revision")
        assert result is not None, "Required property 'revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskconnectConnectorWorkerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskconnectConnectorWorkerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskconnectConnector.MskconnectConnectorWorkerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38811cbec8b2ad5997d15ba143eead1c4847ab58af0847d3c0e3caa370361353)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a49e72b2a46fdf52b750e5e25294f6fbd3ffcadf36d3c8f00212aabf24896d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292c16891cf3a6c8a857e599b0ea130f3a255a9e9393aba3cb98475b8d8aa9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskconnectConnectorWorkerConfiguration]:
        return typing.cast(typing.Optional[MskconnectConnectorWorkerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskconnectConnectorWorkerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1336a4312befcb7d881942f5734cb983e5751fe49ff14aa8d79ff20108ca6f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MskconnectConnector",
    "MskconnectConnectorCapacity",
    "MskconnectConnectorCapacityAutoscaling",
    "MskconnectConnectorCapacityAutoscalingOutputReference",
    "MskconnectConnectorCapacityAutoscalingScaleInPolicy",
    "MskconnectConnectorCapacityAutoscalingScaleInPolicyOutputReference",
    "MskconnectConnectorCapacityAutoscalingScaleOutPolicy",
    "MskconnectConnectorCapacityAutoscalingScaleOutPolicyOutputReference",
    "MskconnectConnectorCapacityOutputReference",
    "MskconnectConnectorCapacityProvisionedCapacity",
    "MskconnectConnectorCapacityProvisionedCapacityOutputReference",
    "MskconnectConnectorConfig",
    "MskconnectConnectorKafkaCluster",
    "MskconnectConnectorKafkaClusterApacheKafkaCluster",
    "MskconnectConnectorKafkaClusterApacheKafkaClusterOutputReference",
    "MskconnectConnectorKafkaClusterApacheKafkaClusterVpc",
    "MskconnectConnectorKafkaClusterApacheKafkaClusterVpcOutputReference",
    "MskconnectConnectorKafkaClusterClientAuthentication",
    "MskconnectConnectorKafkaClusterClientAuthenticationOutputReference",
    "MskconnectConnectorKafkaClusterEncryptionInTransit",
    "MskconnectConnectorKafkaClusterEncryptionInTransitOutputReference",
    "MskconnectConnectorKafkaClusterOutputReference",
    "MskconnectConnectorLogDelivery",
    "MskconnectConnectorLogDeliveryOutputReference",
    "MskconnectConnectorLogDeliveryWorkerLogDelivery",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogsOutputReference",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehoseOutputReference",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryOutputReference",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryS3",
    "MskconnectConnectorLogDeliveryWorkerLogDeliveryS3OutputReference",
    "MskconnectConnectorPlugin",
    "MskconnectConnectorPluginCustomPlugin",
    "MskconnectConnectorPluginCustomPluginOutputReference",
    "MskconnectConnectorPluginList",
    "MskconnectConnectorPluginOutputReference",
    "MskconnectConnectorTimeouts",
    "MskconnectConnectorTimeoutsOutputReference",
    "MskconnectConnectorWorkerConfiguration",
    "MskconnectConnectorWorkerConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__dfddbe8a630b39d02b4e8dbbbf4fa6dc50a726b9ff8501991623ff341a085303(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity: typing.Union[MskconnectConnectorCapacity, typing.Dict[builtins.str, typing.Any]],
    connector_configuration: typing.Mapping[builtins.str, builtins.str],
    kafka_cluster: typing.Union[MskconnectConnectorKafkaCluster, typing.Dict[builtins.str, typing.Any]],
    kafka_cluster_client_authentication: typing.Union[MskconnectConnectorKafkaClusterClientAuthentication, typing.Dict[builtins.str, typing.Any]],
    kafka_cluster_encryption_in_transit: typing.Union[MskconnectConnectorKafkaClusterEncryptionInTransit, typing.Dict[builtins.str, typing.Any]],
    kafkaconnect_version: builtins.str,
    name: builtins.str,
    plugin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskconnectConnectorPlugin, typing.Dict[builtins.str, typing.Any]]]],
    service_execution_role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_delivery: typing.Optional[typing.Union[MskconnectConnectorLogDelivery, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MskconnectConnectorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_configuration: typing.Optional[typing.Union[MskconnectConnectorWorkerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8247dca66cfc7da7fc26d3c7ca5da63ecf5d4b5b1e01faeae3f045b3c4cbc336(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f393437701b55aabb5bf2de9b1662717a99d50f930690d69e0dd4f364a6073(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskconnectConnectorPlugin, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b157d18d405af6c880bd1e49ea699e29fa0cb5a0ffb370e3ec33ed74937af7c7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e696f87cbc7123848803299dddc7d6a64e723ffb14db32465416b3a4de0709d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cf8f6077e9f54421b520fa5677e4dca4a403627ec5f425511e69f070644e84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c63104c00c81f65bb397f9bf725e276a3c44608816653773512d3ee7f0079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a72b738286eba97dfd5c0a9fbff68d6b1579b84349e7ba103cc6a35f3631ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5c5852c1b6eadd963f71d6a821e5ef789f1ad5a416b1889abae6cea8993c0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfbd9d823e0ac46eea686e888da6f3ab566a531784d072cfbfb77488819a9c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d2373ca16cea4a25cb902c6e32400af8fbd13594729bd58d0ef4e4f07acfc9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a1dab380886114d16510e6efddf731cb59720a1b414b404f273c7d55c7e82b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf91c1f1df450e08abe63976d429fd7c56f061a802a9040625675aae5a10f9c(
    *,
    autoscaling: typing.Optional[typing.Union[MskconnectConnectorCapacityAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    provisioned_capacity: typing.Optional[typing.Union[MskconnectConnectorCapacityProvisionedCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89352ced8eeefe4ef2f6e73e865a0b098294cc05490b3f12685e8707f4f643c(
    *,
    max_worker_count: jsii.Number,
    min_worker_count: jsii.Number,
    mcu_count: typing.Optional[jsii.Number] = None,
    scale_in_policy: typing.Optional[typing.Union[MskconnectConnectorCapacityAutoscalingScaleInPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    scale_out_policy: typing.Optional[typing.Union[MskconnectConnectorCapacityAutoscalingScaleOutPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c612cf1480325665302788c556f0f887e84b404aec69e1a362bb2c47c81d9122(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b850ad888465324b9de85b277aff5be3d2b58a851a37fccbb5aea092b712a0f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5234d485baf89823898f06f1952c350c048a85744ccac00b36cb8ad0cef229ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a8323b0baf548b35216076881ba5abe361bc162fe0d4acdc0779dea35d5fdf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9241d63ba1c1622d02a08b398594589011ab411348e5a99967c4f1b4e0479b35(
    value: typing.Optional[MskconnectConnectorCapacityAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36e5f0cc7b61671f4831df2cb52d75fa37f1eafb12d6b8c975d0320f6d581b1(
    *,
    cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0712cbca95d7843036607e669e53e2a60e85dd2a33dc79fcab49fa29764c1882(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4d3471ecd4ceb5960afcb3b5d34d849869c72ecc0c2e089808dbeed2028aaa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d8f4ba963bba4591b88449e0e89de0ef43eb322a570ff1e4d586167ef23e53(
    value: typing.Optional[MskconnectConnectorCapacityAutoscalingScaleInPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1feded701bb020251afe6f30b70f36d04f94a2db7e84d5ba8b6afe18164fcc(
    *,
    cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8158b8b5c73253119a7f2c21ebf3e4df1c30737fbcb1b495271f0bdec356bad9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f37a438227e8765c8c8d06181b27408bde85b8d2c752f499fe5fc465baade6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4aac134791d6a817df8d9926e530a467067ca41ce16570b712bbe1fe75ad218(
    value: typing.Optional[MskconnectConnectorCapacityAutoscalingScaleOutPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc32f55278b88f75462229ce8b61455506376f473726dea254d2081af5f8854(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0474dff3f2ac1b6fcb357191a29b68e46d13ff6a3c10b427ef83af0550e15039(
    value: typing.Optional[MskconnectConnectorCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a6ab317e3236a55fbd5f1542ebd7c5feeb5a5d23150b8cc3b78e6630e46e76(
    *,
    worker_count: jsii.Number,
    mcu_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3744c2fd95c905c7d8faf8e85606bb9447f7bccf43fa084c6152f76ca16e9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2807c90ae7686a17bcc86902e298d4d819a332cebebea923206881cb7f806d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bb03f13e0dc528ea97b391c669c7548c74db7045f2e27fc1edb833f4c74657(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17131faacdcb57a8271d51531d98e2754418788c6133c0dccaec8b4d660a8ea8(
    value: typing.Optional[MskconnectConnectorCapacityProvisionedCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4055dab2bb266918c58b3ed9e28f0aa1e7113ad3c55f3fe730b5c6af7a6d2e2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity: typing.Union[MskconnectConnectorCapacity, typing.Dict[builtins.str, typing.Any]],
    connector_configuration: typing.Mapping[builtins.str, builtins.str],
    kafka_cluster: typing.Union[MskconnectConnectorKafkaCluster, typing.Dict[builtins.str, typing.Any]],
    kafka_cluster_client_authentication: typing.Union[MskconnectConnectorKafkaClusterClientAuthentication, typing.Dict[builtins.str, typing.Any]],
    kafka_cluster_encryption_in_transit: typing.Union[MskconnectConnectorKafkaClusterEncryptionInTransit, typing.Dict[builtins.str, typing.Any]],
    kafkaconnect_version: builtins.str,
    name: builtins.str,
    plugin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskconnectConnectorPlugin, typing.Dict[builtins.str, typing.Any]]]],
    service_execution_role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_delivery: typing.Optional[typing.Union[MskconnectConnectorLogDelivery, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MskconnectConnectorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_configuration: typing.Optional[typing.Union[MskconnectConnectorWorkerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e476d56542c89db3bf529f9a6e8a163ae67968b8fe06dcba9cd7a0a74d0454a(
    *,
    apache_kafka_cluster: typing.Union[MskconnectConnectorKafkaClusterApacheKafkaCluster, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfaf370b3ba94c3681749e7607e89ec1c9e5392d506d4d5b4d18405a940ed3b3(
    *,
    bootstrap_servers: builtins.str,
    vpc: typing.Union[MskconnectConnectorKafkaClusterApacheKafkaClusterVpc, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4281f926358159d69ea38021b2e146b5b433082d0a7da554f9d6aef8e0c6a866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28d4addb24cbfdd7ed465ad1ddc7bca5a1a68c5f919feb15ba85915c5981d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8836ddc675e2c89469144b70c4b350799bfa55e285a122981b73cd698df7dfee(
    value: typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34898f44fb6158e57b5e84e61f5f4b3b9bc0cab059c39359db6332c9d95e456(
    *,
    security_groups: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeeabbaf9e91991e44000321529be6badbd76a9a9262aff3b10481d68b3bb269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebae8ed389dd16d735dc5febb9539ff26edfbddd0709c50a9fa42e7190da2670(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf06c1c39b4c9a7dd5eabec3071eb2fe9333154fbe1bc9553286dedb36a6037e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4337611bf558c6a53aff7f4022c55985f1220a831d204c01ae4ac5961867195(
    value: typing.Optional[MskconnectConnectorKafkaClusterApacheKafkaClusterVpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca42d59cdeddb3aa24cd837ad917e065db8d10b03b037cd9f960cd32d1a54a9(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeff5af85db3d9e13d07605428408398205dcbb909725ca109591d5cdf722b74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffae2eabb07c43558814b01a9406d3ca482f912accd6adf93ef60816099000e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f654fcab20d8f28ba8c010ba5f8416975e7e4830d5775c72d9e0be809a9dccb(
    value: typing.Optional[MskconnectConnectorKafkaClusterClientAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e08324528daca6f641519181c1797d55b68beb0d08a65f0ecb7460515004cc(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef97b1cfa28e07847d588f22ad5178e99401614df6f391ddcfa030ba0e9096e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfaf1c38cf11771a311eab8e71cdd5499cf1a8888fe40815f37976ca4033cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd94a66a0c4fe9afe9abf62e35561fb77803c4376204e6d1098500bfee06455(
    value: typing.Optional[MskconnectConnectorKafkaClusterEncryptionInTransit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79245117748f9bc5ec7deb2d0f5b85ba987eaec47adec72985ec7b6de7530b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21886e9e031b83609e8bd87bdafec4deb427b82bfec37504164385a05ec141ec(
    value: typing.Optional[MskconnectConnectorKafkaCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b0b310cb415dde9337634bad861588b5b1ad01c1dd25cec8c1ab2ae6f0c23f(
    *,
    worker_log_delivery: typing.Union[MskconnectConnectorLogDeliveryWorkerLogDelivery, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cd0fa1b14cacd0178af1c7fe238363d5a8f401d64d339253dbe8abb8bd83cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cb5fba16c68dfa91906eca161772415d8be0c4f678792557c72e0190cc0965(
    value: typing.Optional[MskconnectConnectorLogDelivery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb40436bd5562c1d2c2561fa4959c4033faef685307c23851a126a3fe429260(
    *,
    cloudwatch_logs: typing.Optional[typing.Union[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[MskconnectConnectorLogDeliveryWorkerLogDeliveryS3, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc6045140c459c1f73413425a2047868f6a502ce0da7f9108c45eaaa2725b93(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e8630ee3444312c3dcffa42acd444f4d3711f7278453ea3400cd6620ba067b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2aa04988e49de573ab1ccc657fb4849140c84c0430993bd4dbdb2215f18739(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d4cc42d72350ecae8b6c3173f2ad3700d9a197720b2666f0acfc96510caa50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3506c8e88c913807ce59dcb6843e572175c4a1002dccccf739c8dcad5510b3df(
    value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryCloudwatchLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79149c1a5fa6246f8cb01ad6b0a7badb0d14efcdf3f5281e076a8d9d3f881fa5(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    delivery_stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd81d68e0bbf2b041b07162a66251b8c56c3174e8409bce55037d88d757ae27e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7b8affed3b80ff963ebc0e09fb73acb3fd2ae5bd245799716bed09169821e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6bcaa90e63828f84fe15ab4483ff98d26250abded64d9f9fad2d44efa14d73a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432f14ae059f7849e62e5a41487fba42ea8ac509bd9a3294f399524f390c7a82(
    value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8132efce950f054fab05d74d2617c3ee7945dde82a1546122c2c822a3cfe0614(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0b2c361193d07287961ff23a18aa6b4c595176db4edc63fd76a51467e8f272(
    value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDelivery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502d4aacc69e218f834ece3820d321fe2df52464e2fdbcbf5432f4efa4b29486(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    bucket: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad19e12fab74578b7e7b5f0ef92d7bef88baafb22e41ba6593f533d0173b10b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06023d5ce2a1f48140c1f1fbcf1cc76572e00dde6456aca443458e7d21c4b826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7eb3c49dda27a045ff9cda7486d8618bb1a1c79a7867a669d597537a648b06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644345e4087f0975713d33f7bfa5c55aec54a080362594359845fff7e141b3d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe33a8cc2323254e0bbe0d64fb22e5a6ef0d9c93605e98acb38afcb806ca23b5(
    value: typing.Optional[MskconnectConnectorLogDeliveryWorkerLogDeliveryS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3e14bee5d08b97f5666fa0de68859f86b5e740e7467df0a1206bc18c5cbf42(
    *,
    custom_plugin: typing.Union[MskconnectConnectorPluginCustomPlugin, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e1b18546f1f878e18e7e3d15138781d06772f882345ea05f9b36a2571e1873(
    *,
    arn: builtins.str,
    revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54326e4fdb922d218ca28f42c12ea80162e7a37b289f239d23a33dbcff386635(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2edeb8487e32c3d01d40109a395ef9d96f256873183dc904dd565df28e166e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfc287ffa0c00a78e7ef8fc5c0248b2b6f233325f69fe2714fb8964e8955b49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad2f497e7f172541ea7afe404a4ae9896de473e1f4e19f302c095411a4b075b(
    value: typing.Optional[MskconnectConnectorPluginCustomPlugin],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0ee267b393c460364ef3cca355df7f4e8e8d6b62bece987dc5d0dff4b4b6e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37759f82a9872ea2954dd85b2e9b47632ba7ced6174644bb30131130cac58508(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ee8f70bb3865f185acb9de9171649e0ca1dbea297673e5116fb7244c1effa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a1df073dcc53fac395617d34384189ace72f188a228e03026eaeaaf71f0da0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda5e48731d472f99f6ce7ae8a28a05648a1b96984cd8ba5ce9213f75552f666(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8925e232a76046301b651ea543e8fd43f422760aac66f4e77309cc3f3c16a829(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskconnectConnectorPlugin]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd70f21886db2079d58802b634f8b67ba3fb512121596073a035a40b78991da0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13b53dc4b2f389ba3a047f87c677e0c9d2e0f3210a1359cdcc0aba3ed2b4551(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorPlugin]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ebfcc1f8b1ec59655d4ecaebb0436e700d7f379e439ed270ce5ff07f5ccaf5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2565b0bd171e82b89813b26a010c5c2d2f1fb56f0adbfc4ac130dbafb5923fdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3cf5702e3ef622334b384b809538bd499696e9ba0ad4b8fc4c0303491265c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d8a6d86179bb04dfb6531ef36865e5643c86e5e5ac206f3fca7f6e39236499(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adbe885d00e1dc707fbd58944123cb27367aca26e8b96a4743639dd5f2b03b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776965d92a3e114660fbdbb2251f08e53205b9a3316069ca1b93559bec021ccf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskconnectConnectorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8403db3af1124d37c4fb9680e8c7e29a2320125ea0a5ffd55dd0bfdffcb4f3bc(
    *,
    arn: builtins.str,
    revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38811cbec8b2ad5997d15ba143eead1c4847ab58af0847d3c0e3caa370361353(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a49e72b2a46fdf52b750e5e25294f6fbd3ffcadf36d3c8f00212aabf24896d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292c16891cf3a6c8a857e599b0ea130f3a255a9e9393aba3cb98475b8d8aa9b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1336a4312befcb7d881942f5734cb983e5751fe49ff14aa8d79ff20108ca6f1c(
    value: typing.Optional[MskconnectConnectorWorkerConfiguration],
) -> None:
    """Type checking stubs"""
    pass
