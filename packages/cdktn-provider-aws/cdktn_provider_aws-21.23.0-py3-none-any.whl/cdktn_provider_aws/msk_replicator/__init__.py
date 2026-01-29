r'''
# `aws_msk_replicator`

Refer to the Terraform Registry for docs: [`aws_msk_replicator`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator).
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


class MskReplicator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicator",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator aws_msk_replicator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorKafkaCluster", typing.Dict[builtins.str, typing.Any]]]],
        replication_info_list: typing.Union["MskReplicatorReplicationInfoListStruct", typing.Dict[builtins.str, typing.Any]],
        replicator_name: builtins.str,
        service_execution_role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MskReplicatorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator aws_msk_replicator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param kafka_cluster: kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#kafka_cluster MskReplicator#kafka_cluster}
        :param replication_info_list: replication_info_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#replication_info_list MskReplicator#replication_info_list}
        :param replicator_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#replicator_name MskReplicator#replicator_name}.
        :param service_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#service_execution_role_arn MskReplicator#service_execution_role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#description MskReplicator#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#id MskReplicator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#region MskReplicator#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#tags MskReplicator#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#tags_all MskReplicator#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#timeouts MskReplicator#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79c04a15bfb1773b6d0f40c66aa59d12d26095fcbdac833bb0c14db8ce6729e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MskReplicatorConfig(
            kafka_cluster=kafka_cluster,
            replication_info_list=replication_info_list,
            replicator_name=replicator_name,
            service_execution_role_arn=service_execution_role_arn,
            description=description,
            id=id,
            region=region,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a MskReplicator resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MskReplicator to import.
        :param import_from_id: The id of the existing MskReplicator that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MskReplicator to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b989502bd901aba7503e931a14511b3d2144437ff23c54d7794aec1759a0d2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKafkaCluster")
    def put_kafka_cluster(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorKafkaCluster", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def7db039c1cb871ad0db1a82aa34fce7af9a4f4ac9da4d5ef4830b7ea7499e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKafkaCluster", [value]))

    @jsii.member(jsii_name="putReplicationInfoList")
    def put_replication_info_list(
        self,
        *,
        consumer_group_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListConsumerGroupReplication", typing.Dict[builtins.str, typing.Any]]]],
        source_kafka_cluster_arn: builtins.str,
        target_compression_type: builtins.str,
        target_kafka_cluster_arn: builtins.str,
        topic_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListTopicReplication", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param consumer_group_replication: consumer_group_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_group_replication MskReplicator#consumer_group_replication}
        :param source_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#source_kafka_cluster_arn MskReplicator#source_kafka_cluster_arn}.
        :param target_compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#target_compression_type MskReplicator#target_compression_type}.
        :param target_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#target_kafka_cluster_arn MskReplicator#target_kafka_cluster_arn}.
        :param topic_replication: topic_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topic_replication MskReplicator#topic_replication}
        '''
        value = MskReplicatorReplicationInfoListStruct(
            consumer_group_replication=consumer_group_replication,
            source_kafka_cluster_arn=source_kafka_cluster_arn,
            target_compression_type=target_compression_type,
            target_kafka_cluster_arn=target_kafka_cluster_arn,
            topic_replication=topic_replication,
        )

        return typing.cast(None, jsii.invoke(self, "putReplicationInfoList", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#create MskReplicator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#delete MskReplicator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#update MskReplicator#update}.
        '''
        value = MskReplicatorTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="currentVersion")
    def current_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentVersion"))

    @builtins.property
    @jsii.member(jsii_name="kafkaCluster")
    def kafka_cluster(self) -> "MskReplicatorKafkaClusterList":
        return typing.cast("MskReplicatorKafkaClusterList", jsii.get(self, "kafkaCluster"))

    @builtins.property
    @jsii.member(jsii_name="replicationInfoList")
    def replication_info_list(
        self,
    ) -> "MskReplicatorReplicationInfoListStructOutputReference":
        return typing.cast("MskReplicatorReplicationInfoListStructOutputReference", jsii.get(self, "replicationInfoList"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MskReplicatorTimeoutsOutputReference":
        return typing.cast("MskReplicatorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterInput")
    def kafka_cluster_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]]], jsii.get(self, "kafkaClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationInfoListInput")
    def replication_info_list_input(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListStruct"]:
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListStruct"], jsii.get(self, "replicationInfoListInput"))

    @builtins.property
    @jsii.member(jsii_name="replicatorNameInput")
    def replicator_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicatorNameInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MskReplicatorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MskReplicatorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ba028230fe5930be51121cf5669677b1b02b3b6ef4a1fa77ede64f6dd8a00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda74d8e7742e4e789c1a5862e678351cf3d96d6290c8733671baed70ad635cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc754e3de6ea9fcf4c3a55c9eec87e601ef48c7e74153f1afff23c2f9e14ead1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicatorName")
    def replicator_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicatorName"))

    @replicator_name.setter
    def replicator_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81f69773453ca7182ee276ac7d642fdb172ddbbcf08780fb598daa739520a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicatorName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceExecutionRoleArn"))

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52ebfcacfb76362f23103e2bd69b4e806f11899cb37ede342cb70e04978b22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceExecutionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2926ea3d921a27d429c6d40ae57bb46cf26acece066a6053128269676dad529c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6262924fdab3f4702133b8623f1d204bd7d38a0ab6fd1d2a1cd4c94f7105ad94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "kafka_cluster": "kafkaCluster",
        "replication_info_list": "replicationInfoList",
        "replicator_name": "replicatorName",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "description": "description",
        "id": "id",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class MskReplicatorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorKafkaCluster", typing.Dict[builtins.str, typing.Any]]]],
        replication_info_list: typing.Union["MskReplicatorReplicationInfoListStruct", typing.Dict[builtins.str, typing.Any]],
        replicator_name: builtins.str,
        service_execution_role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MskReplicatorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param kafka_cluster: kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#kafka_cluster MskReplicator#kafka_cluster}
        :param replication_info_list: replication_info_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#replication_info_list MskReplicator#replication_info_list}
        :param replicator_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#replicator_name MskReplicator#replicator_name}.
        :param service_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#service_execution_role_arn MskReplicator#service_execution_role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#description MskReplicator#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#id MskReplicator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#region MskReplicator#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#tags MskReplicator#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#tags_all MskReplicator#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#timeouts MskReplicator#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(replication_info_list, dict):
            replication_info_list = MskReplicatorReplicationInfoListStruct(**replication_info_list)
        if isinstance(timeouts, dict):
            timeouts = MskReplicatorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52808610d5953c220c4b97c4482df91449a04aba594e48c126e46ecd88163e59)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument kafka_cluster", value=kafka_cluster, expected_type=type_hints["kafka_cluster"])
            check_type(argname="argument replication_info_list", value=replication_info_list, expected_type=type_hints["replication_info_list"])
            check_type(argname="argument replicator_name", value=replicator_name, expected_type=type_hints["replicator_name"])
            check_type(argname="argument service_execution_role_arn", value=service_execution_role_arn, expected_type=type_hints["service_execution_role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kafka_cluster": kafka_cluster,
            "replication_info_list": replication_info_list,
            "replicator_name": replicator_name,
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
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def kafka_cluster(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]]:
        '''kafka_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#kafka_cluster MskReplicator#kafka_cluster}
        '''
        result = self._values.get("kafka_cluster")
        assert result is not None, "Required property 'kafka_cluster' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]], result)

    @builtins.property
    def replication_info_list(self) -> "MskReplicatorReplicationInfoListStruct":
        '''replication_info_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#replication_info_list MskReplicator#replication_info_list}
        '''
        result = self._values.get("replication_info_list")
        assert result is not None, "Required property 'replication_info_list' is missing"
        return typing.cast("MskReplicatorReplicationInfoListStruct", result)

    @builtins.property
    def replicator_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#replicator_name MskReplicator#replicator_name}.'''
        result = self._values.get("replicator_name")
        assert result is not None, "Required property 'replicator_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#service_execution_role_arn MskReplicator#service_execution_role_arn}.'''
        result = self._values.get("service_execution_role_arn")
        assert result is not None, "Required property 'service_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#description MskReplicator#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#id MskReplicator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#region MskReplicator#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#tags MskReplicator#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#tags_all MskReplicator#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MskReplicatorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#timeouts MskReplicator#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MskReplicatorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaCluster",
    jsii_struct_bases=[],
    name_mapping={"amazon_msk_cluster": "amazonMskCluster", "vpc_config": "vpcConfig"},
)
class MskReplicatorKafkaCluster:
    def __init__(
        self,
        *,
        amazon_msk_cluster: typing.Union["MskReplicatorKafkaClusterAmazonMskCluster", typing.Dict[builtins.str, typing.Any]],
        vpc_config: typing.Union["MskReplicatorKafkaClusterVpcConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param amazon_msk_cluster: amazon_msk_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#amazon_msk_cluster MskReplicator#amazon_msk_cluster}
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#vpc_config MskReplicator#vpc_config}
        '''
        if isinstance(amazon_msk_cluster, dict):
            amazon_msk_cluster = MskReplicatorKafkaClusterAmazonMskCluster(**amazon_msk_cluster)
        if isinstance(vpc_config, dict):
            vpc_config = MskReplicatorKafkaClusterVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e1719d102c594a2b575d3b7b2a51f07d0dccb947e813e865a07b1ade74df03)
            check_type(argname="argument amazon_msk_cluster", value=amazon_msk_cluster, expected_type=type_hints["amazon_msk_cluster"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amazon_msk_cluster": amazon_msk_cluster,
            "vpc_config": vpc_config,
        }

    @builtins.property
    def amazon_msk_cluster(self) -> "MskReplicatorKafkaClusterAmazonMskCluster":
        '''amazon_msk_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#amazon_msk_cluster MskReplicator#amazon_msk_cluster}
        '''
        result = self._values.get("amazon_msk_cluster")
        assert result is not None, "Required property 'amazon_msk_cluster' is missing"
        return typing.cast("MskReplicatorKafkaClusterAmazonMskCluster", result)

    @builtins.property
    def vpc_config(self) -> "MskReplicatorKafkaClusterVpcConfig":
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#vpc_config MskReplicator#vpc_config}
        '''
        result = self._values.get("vpc_config")
        assert result is not None, "Required property 'vpc_config' is missing"
        return typing.cast("MskReplicatorKafkaClusterVpcConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorKafkaCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaClusterAmazonMskCluster",
    jsii_struct_bases=[],
    name_mapping={"msk_cluster_arn": "mskClusterArn"},
)
class MskReplicatorKafkaClusterAmazonMskCluster:
    def __init__(self, *, msk_cluster_arn: builtins.str) -> None:
        '''
        :param msk_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#msk_cluster_arn MskReplicator#msk_cluster_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf48a7b750de3f53869c3ca66c5da2085d098500c2ad47dda0f3e66d4f59ffa)
            check_type(argname="argument msk_cluster_arn", value=msk_cluster_arn, expected_type=type_hints["msk_cluster_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "msk_cluster_arn": msk_cluster_arn,
        }

    @builtins.property
    def msk_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#msk_cluster_arn MskReplicator#msk_cluster_arn}.'''
        result = self._values.get("msk_cluster_arn")
        assert result is not None, "Required property 'msk_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorKafkaClusterAmazonMskCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorKafkaClusterAmazonMskClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaClusterAmazonMskClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b54f24c2779a14a4585eba12d7e596658a1dd12272099d3a2d07f5d066610fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="mskClusterArnInput")
    def msk_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mskClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="mskClusterArn")
    def msk_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mskClusterArn"))

    @msk_cluster_arn.setter
    def msk_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ba522628c12083e82ba97211a216d1050f94a8985614d2fd194d33568af224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mskClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster]:
        return typing.cast(typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05894117865e5fda2a3ba0135bbe2abf15ba99ea7cc33139125ef3ae52b12f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorKafkaClusterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaClusterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc34b8796ea0a1ed53a5ab05eee4393be93e80cf43129cc2350e9a0311a8eb5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MskReplicatorKafkaClusterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699c1c6e1c696bddce35bb8ae3c4d9a946d15c0d20f742584b73ba87c61cb961)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskReplicatorKafkaClusterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3563f7e3278d178b4d9e819bb43b64d56e6a211f4022f9bdf080fef755e0fd69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1e1b5d5a65df68cc73be318455983966138f0edd1b13efdc7cf3a74041bbf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__baf355930a410f8100c4fca5c5f3c55a897846c2a093583432012e32c77d2a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b65da4207036aeb54af6dfd38656ccdfc27a1316d1a9d532f0e8a0cacb12a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorKafkaClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55b4b0abbccdace67a7487bb3c8e4dc1003a46587a2b0661aae7a02ab8d91bee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAmazonMskCluster")
    def put_amazon_msk_cluster(self, *, msk_cluster_arn: builtins.str) -> None:
        '''
        :param msk_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#msk_cluster_arn MskReplicator#msk_cluster_arn}.
        '''
        value = MskReplicatorKafkaClusterAmazonMskCluster(
            msk_cluster_arn=msk_cluster_arn
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonMskCluster", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        security_groups_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#subnet_ids MskReplicator#subnet_ids}.
        :param security_groups_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#security_groups_ids MskReplicator#security_groups_ids}.
        '''
        value = MskReplicatorKafkaClusterVpcConfig(
            subnet_ids=subnet_ids, security_groups_ids=security_groups_ids
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="amazonMskCluster")
    def amazon_msk_cluster(
        self,
    ) -> MskReplicatorKafkaClusterAmazonMskClusterOutputReference:
        return typing.cast(MskReplicatorKafkaClusterAmazonMskClusterOutputReference, jsii.get(self, "amazonMskCluster"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "MskReplicatorKafkaClusterVpcConfigOutputReference":
        return typing.cast("MskReplicatorKafkaClusterVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="amazonMskClusterInput")
    def amazon_msk_cluster_input(
        self,
    ) -> typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster]:
        return typing.cast(typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster], jsii.get(self, "amazonMskClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["MskReplicatorKafkaClusterVpcConfig"]:
        return typing.cast(typing.Optional["MskReplicatorKafkaClusterVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea496b7c45351fe7c83c009638afc540287c483572fd70cb26d1a8f8e4624102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaClusterVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_ids": "subnetIds",
        "security_groups_ids": "securityGroupsIds",
    },
)
class MskReplicatorKafkaClusterVpcConfig:
    def __init__(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        security_groups_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#subnet_ids MskReplicator#subnet_ids}.
        :param security_groups_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#security_groups_ids MskReplicator#security_groups_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b1fc2e60e47a02e23fdc84f0182dac78e80b09972d8987b67ed89ab0534b82)
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument security_groups_ids", value=security_groups_ids, expected_type=type_hints["security_groups_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_ids": subnet_ids,
        }
        if security_groups_ids is not None:
            self._values["security_groups_ids"] = security_groups_ids

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#subnet_ids MskReplicator#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_groups_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#security_groups_ids MskReplicator#security_groups_ids}.'''
        result = self._values.get("security_groups_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorKafkaClusterVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorKafkaClusterVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorKafkaClusterVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68dc82eca709c94cb4c6c1e9ba9b6c1c5f949b859db8d9944d1ab3ff84b2b301)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroupsIds")
    def reset_security_groups_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupsIds", []))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsIdsInput")
    def security_groups_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsIds")
    def security_groups_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupsIds"))

    @security_groups_ids.setter
    def security_groups_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63247a57c3bb46ca02e2c6d76b4a5f3b36f68508e5adc1db83f6910e6832cac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupsIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe94d210910ce0dbbd6df520f4ba34aacdb81248a5f3945dae4b8416bdbdc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskReplicatorKafkaClusterVpcConfig]:
        return typing.cast(typing.Optional[MskReplicatorKafkaClusterVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorKafkaClusterVpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925b831c93be6c588298a3de038a538e0cc68df09bea745e8242f56e0959ac50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListConsumerGroupReplication",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_groups_to_replicate": "consumerGroupsToReplicate",
        "consumer_groups_to_exclude": "consumerGroupsToExclude",
        "detect_and_copy_new_consumer_groups": "detectAndCopyNewConsumerGroups",
        "synchronise_consumer_group_offsets": "synchroniseConsumerGroupOffsets",
    },
)
class MskReplicatorReplicationInfoListConsumerGroupReplication:
    def __init__(
        self,
        *,
        consumer_groups_to_replicate: typing.Sequence[builtins.str],
        consumer_groups_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        detect_and_copy_new_consumer_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        synchronise_consumer_group_offsets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param consumer_groups_to_replicate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_groups_to_replicate MskReplicator#consumer_groups_to_replicate}.
        :param consumer_groups_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_groups_to_exclude MskReplicator#consumer_groups_to_exclude}.
        :param detect_and_copy_new_consumer_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#detect_and_copy_new_consumer_groups MskReplicator#detect_and_copy_new_consumer_groups}.
        :param synchronise_consumer_group_offsets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#synchronise_consumer_group_offsets MskReplicator#synchronise_consumer_group_offsets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efe5d0491620e3829681917b7ed43bdf3283ad03f1a6cd87296d0108fee035c)
            check_type(argname="argument consumer_groups_to_replicate", value=consumer_groups_to_replicate, expected_type=type_hints["consumer_groups_to_replicate"])
            check_type(argname="argument consumer_groups_to_exclude", value=consumer_groups_to_exclude, expected_type=type_hints["consumer_groups_to_exclude"])
            check_type(argname="argument detect_and_copy_new_consumer_groups", value=detect_and_copy_new_consumer_groups, expected_type=type_hints["detect_and_copy_new_consumer_groups"])
            check_type(argname="argument synchronise_consumer_group_offsets", value=synchronise_consumer_group_offsets, expected_type=type_hints["synchronise_consumer_group_offsets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_groups_to_replicate": consumer_groups_to_replicate,
        }
        if consumer_groups_to_exclude is not None:
            self._values["consumer_groups_to_exclude"] = consumer_groups_to_exclude
        if detect_and_copy_new_consumer_groups is not None:
            self._values["detect_and_copy_new_consumer_groups"] = detect_and_copy_new_consumer_groups
        if synchronise_consumer_group_offsets is not None:
            self._values["synchronise_consumer_group_offsets"] = synchronise_consumer_group_offsets

    @builtins.property
    def consumer_groups_to_replicate(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_groups_to_replicate MskReplicator#consumer_groups_to_replicate}.'''
        result = self._values.get("consumer_groups_to_replicate")
        assert result is not None, "Required property 'consumer_groups_to_replicate' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def consumer_groups_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_groups_to_exclude MskReplicator#consumer_groups_to_exclude}.'''
        result = self._values.get("consumer_groups_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def detect_and_copy_new_consumer_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#detect_and_copy_new_consumer_groups MskReplicator#detect_and_copy_new_consumer_groups}.'''
        result = self._values.get("detect_and_copy_new_consumer_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def synchronise_consumer_group_offsets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#synchronise_consumer_group_offsets MskReplicator#synchronise_consumer_group_offsets}.'''
        result = self._values.get("synchronise_consumer_group_offsets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListConsumerGroupReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListConsumerGroupReplicationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListConsumerGroupReplicationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9865fcae4a6953180fcf9e6df20c476cce8b206d18ee62c05c245d867419b0ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e16652a25396b5a775d003ca7dd12ca664e3175bb53d1b9e62272c5a21db01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573539f0b3589105ba8c95c3eefd34bfa1c1d47155cec45e011a480cddbf53ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dbeaa2d7b4491ac8a665d07ea895627f390e741d31f35752901c18b64deabcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__861378ade661bc2bfdfb4c88df84e7cb135dcc32ee34228677252ca25fed75be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cbf3aafe61e22d27a4aa6a36504a13e1503f48e9473c92cc4d09fbe483c7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d66d41ae0001fbbe6104cfce9c74fbeb9deb339c291f746c7d81347d1fcb3e6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConsumerGroupsToExclude")
    def reset_consumer_groups_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupsToExclude", []))

    @jsii.member(jsii_name="resetDetectAndCopyNewConsumerGroups")
    def reset_detect_and_copy_new_consumer_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectAndCopyNewConsumerGroups", []))

    @jsii.member(jsii_name="resetSynchroniseConsumerGroupOffsets")
    def reset_synchronise_consumer_group_offsets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSynchroniseConsumerGroupOffsets", []))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToExcludeInput")
    def consumer_groups_to_exclude_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "consumerGroupsToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToReplicateInput")
    def consumer_groups_to_replicate_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "consumerGroupsToReplicateInput"))

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewConsumerGroupsInput")
    def detect_and_copy_new_consumer_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "detectAndCopyNewConsumerGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="synchroniseConsumerGroupOffsetsInput")
    def synchronise_consumer_group_offsets_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "synchroniseConsumerGroupOffsetsInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToExclude")
    def consumer_groups_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "consumerGroupsToExclude"))

    @consumer_groups_to_exclude.setter
    def consumer_groups_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3214e258b7e3d4a55f26c4ed1a796f6b4c2ea751f43c54241914e92414ceaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupsToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToReplicate")
    def consumer_groups_to_replicate(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "consumerGroupsToReplicate"))

    @consumer_groups_to_replicate.setter
    def consumer_groups_to_replicate(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363f4ce3f8d80d686d041bc5c4334beb577370f8a24afe4003faca66287a50b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupsToReplicate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewConsumerGroups")
    def detect_and_copy_new_consumer_groups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "detectAndCopyNewConsumerGroups"))

    @detect_and_copy_new_consumer_groups.setter
    def detect_and_copy_new_consumer_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b381fc833ce5a7893114596c3a5d1aff04031451b91663d4ef2271aa5bc89078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectAndCopyNewConsumerGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="synchroniseConsumerGroupOffsets")
    def synchronise_consumer_group_offsets(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "synchroniseConsumerGroupOffsets"))

    @synchronise_consumer_group_offsets.setter
    def synchronise_consumer_group_offsets(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8afd76c57cd632c3b0e4da9d72d6f318ee34ec86b681afbe748dc0882d17b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synchroniseConsumerGroupOffsets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c86dfb253932c2b4464a9ff477ed586b6b50963d771aafd0bea80d769118c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListStruct",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_group_replication": "consumerGroupReplication",
        "source_kafka_cluster_arn": "sourceKafkaClusterArn",
        "target_compression_type": "targetCompressionType",
        "target_kafka_cluster_arn": "targetKafkaClusterArn",
        "topic_replication": "topicReplication",
    },
)
class MskReplicatorReplicationInfoListStruct:
    def __init__(
        self,
        *,
        consumer_group_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
        source_kafka_cluster_arn: builtins.str,
        target_compression_type: builtins.str,
        target_kafka_cluster_arn: builtins.str,
        topic_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListTopicReplication", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param consumer_group_replication: consumer_group_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_group_replication MskReplicator#consumer_group_replication}
        :param source_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#source_kafka_cluster_arn MskReplicator#source_kafka_cluster_arn}.
        :param target_compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#target_compression_type MskReplicator#target_compression_type}.
        :param target_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#target_kafka_cluster_arn MskReplicator#target_kafka_cluster_arn}.
        :param topic_replication: topic_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topic_replication MskReplicator#topic_replication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe9f15c6483cd856931f651bdf20e4f4a888a97a80172e68b4479c7047ccc1c)
            check_type(argname="argument consumer_group_replication", value=consumer_group_replication, expected_type=type_hints["consumer_group_replication"])
            check_type(argname="argument source_kafka_cluster_arn", value=source_kafka_cluster_arn, expected_type=type_hints["source_kafka_cluster_arn"])
            check_type(argname="argument target_compression_type", value=target_compression_type, expected_type=type_hints["target_compression_type"])
            check_type(argname="argument target_kafka_cluster_arn", value=target_kafka_cluster_arn, expected_type=type_hints["target_kafka_cluster_arn"])
            check_type(argname="argument topic_replication", value=topic_replication, expected_type=type_hints["topic_replication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_group_replication": consumer_group_replication,
            "source_kafka_cluster_arn": source_kafka_cluster_arn,
            "target_compression_type": target_compression_type,
            "target_kafka_cluster_arn": target_kafka_cluster_arn,
            "topic_replication": topic_replication,
        }

    @builtins.property
    def consumer_group_replication(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]:
        '''consumer_group_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#consumer_group_replication MskReplicator#consumer_group_replication}
        '''
        result = self._values.get("consumer_group_replication")
        assert result is not None, "Required property 'consumer_group_replication' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]], result)

    @builtins.property
    def source_kafka_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#source_kafka_cluster_arn MskReplicator#source_kafka_cluster_arn}.'''
        result = self._values.get("source_kafka_cluster_arn")
        assert result is not None, "Required property 'source_kafka_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_compression_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#target_compression_type MskReplicator#target_compression_type}.'''
        result = self._values.get("target_compression_type")
        assert result is not None, "Required property 'target_compression_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_kafka_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#target_kafka_cluster_arn MskReplicator#target_kafka_cluster_arn}.'''
        result = self._values.get("target_kafka_cluster_arn")
        assert result is not None, "Required property 'target_kafka_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_replication(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]]:
        '''topic_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topic_replication MskReplicator#topic_replication}
        '''
        result = self._values.get("topic_replication")
        assert result is not None, "Required property 'topic_replication' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd44ff898236ae7749279647b264ea5ca06a0a3dd876bb877663e048e991404f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConsumerGroupReplication")
    def put_consumer_group_replication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6641306103580b43651e2ffe57213cd56fb05f135d3615cd3db574a50c51072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConsumerGroupReplication", [value]))

    @jsii.member(jsii_name="putTopicReplication")
    def put_topic_replication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListTopicReplication", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8697f8883af475413532018ebd7180b494109e6c26d4c860c7c44924b71ab307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopicReplication", [value]))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupReplication")
    def consumer_group_replication(
        self,
    ) -> MskReplicatorReplicationInfoListConsumerGroupReplicationList:
        return typing.cast(MskReplicatorReplicationInfoListConsumerGroupReplicationList, jsii.get(self, "consumerGroupReplication"))

    @builtins.property
    @jsii.member(jsii_name="sourceKafkaClusterAlias")
    def source_kafka_cluster_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceKafkaClusterAlias"))

    @builtins.property
    @jsii.member(jsii_name="targetKafkaClusterAlias")
    def target_kafka_cluster_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetKafkaClusterAlias"))

    @builtins.property
    @jsii.member(jsii_name="topicReplication")
    def topic_replication(
        self,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationList":
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationList", jsii.get(self, "topicReplication"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupReplicationInput")
    def consumer_group_replication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]], jsii.get(self, "consumerGroupReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKafkaClusterArnInput")
    def source_kafka_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceKafkaClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCompressionTypeInput")
    def target_compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetCompressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetKafkaClusterArnInput")
    def target_kafka_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetKafkaClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicReplicationInput")
    def topic_replication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]]], jsii.get(self, "topicReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKafkaClusterArn")
    def source_kafka_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceKafkaClusterArn"))

    @source_kafka_cluster_arn.setter
    def source_kafka_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9aca7ec3a3594e6018fbb82ac01bd6653b43f4641b2316020f79bdd23134302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceKafkaClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCompressionType")
    def target_compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetCompressionType"))

    @target_compression_type.setter
    def target_compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380f073276577a6ab7032f77cb376038bdff56c2dbbda6bc1e45c97871933a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCompressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetKafkaClusterArn")
    def target_kafka_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetKafkaClusterArn"))

    @target_kafka_cluster_arn.setter
    def target_kafka_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2e2a132eb33d3ed3b3d2c5aeab9eed36bb3e7efe1ff3127b63482e32828b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetKafkaClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskReplicatorReplicationInfoListStruct]:
        return typing.cast(typing.Optional[MskReplicatorReplicationInfoListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorReplicationInfoListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5819166c7560a7ba0d63e1ab53badf1981b88da1f14aead01c749266c4d20fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplication",
    jsii_struct_bases=[],
    name_mapping={
        "topics_to_replicate": "topicsToReplicate",
        "copy_access_control_lists_for_topics": "copyAccessControlListsForTopics",
        "copy_topic_configurations": "copyTopicConfigurations",
        "detect_and_copy_new_topics": "detectAndCopyNewTopics",
        "starting_position": "startingPosition",
        "topic_name_configuration": "topicNameConfiguration",
        "topics_to_exclude": "topicsToExclude",
    },
)
class MskReplicatorReplicationInfoListTopicReplication:
    def __init__(
        self,
        *,
        topics_to_replicate: typing.Sequence[builtins.str],
        copy_access_control_lists_for_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        copy_topic_configurations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        detect_and_copy_new_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        starting_position: typing.Optional[typing.Union["MskReplicatorReplicationInfoListTopicReplicationStartingPosition", typing.Dict[builtins.str, typing.Any]]] = None,
        topic_name_configuration: typing.Optional[typing.Union["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        topics_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param topics_to_replicate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topics_to_replicate MskReplicator#topics_to_replicate}.
        :param copy_access_control_lists_for_topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#copy_access_control_lists_for_topics MskReplicator#copy_access_control_lists_for_topics}.
        :param copy_topic_configurations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#copy_topic_configurations MskReplicator#copy_topic_configurations}.
        :param detect_and_copy_new_topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#detect_and_copy_new_topics MskReplicator#detect_and_copy_new_topics}.
        :param starting_position: starting_position block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#starting_position MskReplicator#starting_position}
        :param topic_name_configuration: topic_name_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topic_name_configuration MskReplicator#topic_name_configuration}
        :param topics_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topics_to_exclude MskReplicator#topics_to_exclude}.
        '''
        if isinstance(starting_position, dict):
            starting_position = MskReplicatorReplicationInfoListTopicReplicationStartingPosition(**starting_position)
        if isinstance(topic_name_configuration, dict):
            topic_name_configuration = MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration(**topic_name_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfa8fbf6e00ccb9087cf40e72344fad2087417ca843e4058174296684579116)
            check_type(argname="argument topics_to_replicate", value=topics_to_replicate, expected_type=type_hints["topics_to_replicate"])
            check_type(argname="argument copy_access_control_lists_for_topics", value=copy_access_control_lists_for_topics, expected_type=type_hints["copy_access_control_lists_for_topics"])
            check_type(argname="argument copy_topic_configurations", value=copy_topic_configurations, expected_type=type_hints["copy_topic_configurations"])
            check_type(argname="argument detect_and_copy_new_topics", value=detect_and_copy_new_topics, expected_type=type_hints["detect_and_copy_new_topics"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument topic_name_configuration", value=topic_name_configuration, expected_type=type_hints["topic_name_configuration"])
            check_type(argname="argument topics_to_exclude", value=topics_to_exclude, expected_type=type_hints["topics_to_exclude"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topics_to_replicate": topics_to_replicate,
        }
        if copy_access_control_lists_for_topics is not None:
            self._values["copy_access_control_lists_for_topics"] = copy_access_control_lists_for_topics
        if copy_topic_configurations is not None:
            self._values["copy_topic_configurations"] = copy_topic_configurations
        if detect_and_copy_new_topics is not None:
            self._values["detect_and_copy_new_topics"] = detect_and_copy_new_topics
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if topic_name_configuration is not None:
            self._values["topic_name_configuration"] = topic_name_configuration
        if topics_to_exclude is not None:
            self._values["topics_to_exclude"] = topics_to_exclude

    @builtins.property
    def topics_to_replicate(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topics_to_replicate MskReplicator#topics_to_replicate}.'''
        result = self._values.get("topics_to_replicate")
        assert result is not None, "Required property 'topics_to_replicate' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def copy_access_control_lists_for_topics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#copy_access_control_lists_for_topics MskReplicator#copy_access_control_lists_for_topics}.'''
        result = self._values.get("copy_access_control_lists_for_topics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def copy_topic_configurations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#copy_topic_configurations MskReplicator#copy_topic_configurations}.'''
        result = self._values.get("copy_topic_configurations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def detect_and_copy_new_topics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#detect_and_copy_new_topics MskReplicator#detect_and_copy_new_topics}.'''
        result = self._values.get("detect_and_copy_new_topics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def starting_position(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"]:
        '''starting_position block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#starting_position MskReplicator#starting_position}
        '''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"], result)

    @builtins.property
    def topic_name_configuration(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"]:
        '''topic_name_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topic_name_configuration MskReplicator#topic_name_configuration}
        '''
        result = self._values.get("topic_name_configuration")
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"], result)

    @builtins.property
    def topics_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#topics_to_exclude MskReplicator#topics_to_exclude}.'''
        result = self._values.get("topics_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListTopicReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListTopicReplicationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e037ab4dbce8bca9b584dd3834c1fe2ea48d81463bc29e3a500f3ee4e42e8a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e162a17f4d7f275bbe2fbffe4f42ae11380f540acbd96e26ed63bcf805c1e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4525fc799c200cab57b239a01815b758326e9ff7433dfc9594bf590d63c58a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e3fef856885ebca3760432d676939b5e392665e60b7d265dc664c87938d212e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e39d0d9ac6467b5b76ca5d1c11bfc359c5046e92d709d2c8d7560bbf50585d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d46976fea46a211cc6520fa2f6b8163ad52071538ecad0150028e52c50f2d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorReplicationInfoListTopicReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb475d551c2f15600181c542fc4696fdc8049bdebd7a08aedb7e9e9a0b439410)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStartingPosition")
    def put_starting_position(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        value = MskReplicatorReplicationInfoListTopicReplicationStartingPosition(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putStartingPosition", [value]))

    @jsii.member(jsii_name="putTopicNameConfiguration")
    def put_topic_name_configuration(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        value = MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putTopicNameConfiguration", [value]))

    @jsii.member(jsii_name="resetCopyAccessControlListsForTopics")
    def reset_copy_access_control_lists_for_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyAccessControlListsForTopics", []))

    @jsii.member(jsii_name="resetCopyTopicConfigurations")
    def reset_copy_topic_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTopicConfigurations", []))

    @jsii.member(jsii_name="resetDetectAndCopyNewTopics")
    def reset_detect_and_copy_new_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectAndCopyNewTopics", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetTopicNameConfiguration")
    def reset_topic_name_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicNameConfiguration", []))

    @jsii.member(jsii_name="resetTopicsToExclude")
    def reset_topics_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicsToExclude", []))

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(
        self,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference":
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference", jsii.get(self, "startingPosition"))

    @builtins.property
    @jsii.member(jsii_name="topicNameConfiguration")
    def topic_name_configuration(
        self,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference":
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference", jsii.get(self, "topicNameConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="copyAccessControlListsForTopicsInput")
    def copy_access_control_lists_for_topics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyAccessControlListsForTopicsInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTopicConfigurationsInput")
    def copy_topic_configurations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTopicConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewTopicsInput")
    def detect_and_copy_new_topics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "detectAndCopyNewTopicsInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"]:
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameConfigurationInput")
    def topic_name_configuration_input(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"]:
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"], jsii.get(self, "topicNameConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsToExcludeInput")
    def topics_to_exclude_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsToReplicateInput")
    def topics_to_replicate_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsToReplicateInput"))

    @builtins.property
    @jsii.member(jsii_name="copyAccessControlListsForTopics")
    def copy_access_control_lists_for_topics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyAccessControlListsForTopics"))

    @copy_access_control_lists_for_topics.setter
    def copy_access_control_lists_for_topics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b239009eadc8f577ad3200e2bed95f932b7282d988191c12c75735cbb3432c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyAccessControlListsForTopics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyTopicConfigurations")
    def copy_topic_configurations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTopicConfigurations"))

    @copy_topic_configurations.setter
    def copy_topic_configurations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f95f72d0f84df4dcae60e669ccf00b7ac6f1be3ffbe9882bab9ba929d8511d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTopicConfigurations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewTopics")
    def detect_and_copy_new_topics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "detectAndCopyNewTopics"))

    @detect_and_copy_new_topics.setter
    def detect_and_copy_new_topics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c153b1dbb1503e408702ec1b6211bf8782b94ac3acfd5faa311e62ece1a929e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectAndCopyNewTopics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicsToExclude")
    def topics_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topicsToExclude"))

    @topics_to_exclude.setter
    def topics_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bac4bdd51c4ea80f4f6f99fd8436ac6f66c8ccd0b6ac80ee3dc16f4a552eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicsToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicsToReplicate")
    def topics_to_replicate(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topicsToReplicate"))

    @topics_to_replicate.setter
    def topics_to_replicate(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80d221759815300b2d336443b0a271aa609d5407821e78e2175504a9783e1a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicsToReplicate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efa25e634132f6a838a63c07cff95991c2a74588b447f78f9cbdfee2e53b475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationStartingPosition",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class MskReplicatorReplicationInfoListTopicReplicationStartingPosition:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848dc1083e6aa5401638ce9df57f71eddaedab1bd59fb72989008d8bdab05b33)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#type MskReplicator#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListTopicReplicationStartingPosition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d655a62211eb26e6dd2793c1cc536a3787fc71492b437db824c21b30ba00f1ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2d660ab731f537802019f05d790610d473a419d7534a702e18bfbcf7adc0e694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition]:
        return typing.cast(typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03d57497f40abdb4cd10808deb4d9480d69ae646b342e03d8b171833906f970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ea1748ad11f7cd7a46894abeba4c7db1d13d03d206864c1d7bd2a8c94370ce)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#type MskReplicator#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28c512215fc4da2f44458704ffdc761bbe4ea355a7013053ad265a356de5dc12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__235348cf06a929f3b0331f5f149e8369c02786bb90ac4b9674b78b80ee9cfa20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration]:
        return typing.cast(typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cedbcb01bd1148b4ea1511660d0ae548e3bfbef587b0c71d1ac12286bf9185b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MskReplicatorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#create MskReplicator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#delete MskReplicator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#update MskReplicator#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5810e6a40b24632390e02a70da423e38227373f0696693a35a446a3603cceac6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#create MskReplicator#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#delete MskReplicator#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/msk_replicator#update MskReplicator#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.mskReplicator.MskReplicatorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c26ac361e3460d30b1feee876f0a3d9eb24fa1385acb120acb0171c60ab486b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5777b442b42f0d49dcbc33cb5d84d8cd70560ebe158287c38d4b654e6ce437c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544c216cc705d23a403fe921fcb279f90cd1f858c50ce221ed6a99160f5da962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73821b22f61b004d3fb469babf4715acfc09cfec1cba134191297a5a80fbe0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a79550ba06674bd7c4b3a2f64450df756cbd04595f53eaf7934e6e753c3965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MskReplicator",
    "MskReplicatorConfig",
    "MskReplicatorKafkaCluster",
    "MskReplicatorKafkaClusterAmazonMskCluster",
    "MskReplicatorKafkaClusterAmazonMskClusterOutputReference",
    "MskReplicatorKafkaClusterList",
    "MskReplicatorKafkaClusterOutputReference",
    "MskReplicatorKafkaClusterVpcConfig",
    "MskReplicatorKafkaClusterVpcConfigOutputReference",
    "MskReplicatorReplicationInfoListConsumerGroupReplication",
    "MskReplicatorReplicationInfoListConsumerGroupReplicationList",
    "MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference",
    "MskReplicatorReplicationInfoListStruct",
    "MskReplicatorReplicationInfoListStructOutputReference",
    "MskReplicatorReplicationInfoListTopicReplication",
    "MskReplicatorReplicationInfoListTopicReplicationList",
    "MskReplicatorReplicationInfoListTopicReplicationOutputReference",
    "MskReplicatorReplicationInfoListTopicReplicationStartingPosition",
    "MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference",
    "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration",
    "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference",
    "MskReplicatorTimeouts",
    "MskReplicatorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f79c04a15bfb1773b6d0f40c66aa59d12d26095fcbdac833bb0c14db8ce6729e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorKafkaCluster, typing.Dict[builtins.str, typing.Any]]]],
    replication_info_list: typing.Union[MskReplicatorReplicationInfoListStruct, typing.Dict[builtins.str, typing.Any]],
    replicator_name: builtins.str,
    service_execution_role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MskReplicatorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3b989502bd901aba7503e931a14511b3d2144437ff23c54d7794aec1759a0d2e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def7db039c1cb871ad0db1a82aa34fce7af9a4f4ac9da4d5ef4830b7ea7499e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorKafkaCluster, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ba028230fe5930be51121cf5669677b1b02b3b6ef4a1fa77ede64f6dd8a00a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda74d8e7742e4e789c1a5862e678351cf3d96d6290c8733671baed70ad635cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc754e3de6ea9fcf4c3a55c9eec87e601ef48c7e74153f1afff23c2f9e14ead1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81f69773453ca7182ee276ac7d642fdb172ddbbcf08780fb598daa739520a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52ebfcacfb76362f23103e2bd69b4e806f11899cb37ede342cb70e04978b22b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2926ea3d921a27d429c6d40ae57bb46cf26acece066a6053128269676dad529c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6262924fdab3f4702133b8623f1d204bd7d38a0ab6fd1d2a1cd4c94f7105ad94(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52808610d5953c220c4b97c4482df91449a04aba594e48c126e46ecd88163e59(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorKafkaCluster, typing.Dict[builtins.str, typing.Any]]]],
    replication_info_list: typing.Union[MskReplicatorReplicationInfoListStruct, typing.Dict[builtins.str, typing.Any]],
    replicator_name: builtins.str,
    service_execution_role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MskReplicatorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e1719d102c594a2b575d3b7b2a51f07d0dccb947e813e865a07b1ade74df03(
    *,
    amazon_msk_cluster: typing.Union[MskReplicatorKafkaClusterAmazonMskCluster, typing.Dict[builtins.str, typing.Any]],
    vpc_config: typing.Union[MskReplicatorKafkaClusterVpcConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf48a7b750de3f53869c3ca66c5da2085d098500c2ad47dda0f3e66d4f59ffa(
    *,
    msk_cluster_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b54f24c2779a14a4585eba12d7e596658a1dd12272099d3a2d07f5d066610fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ba522628c12083e82ba97211a216d1050f94a8985614d2fd194d33568af224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05894117865e5fda2a3ba0135bbe2abf15ba99ea7cc33139125ef3ae52b12f0(
    value: typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc34b8796ea0a1ed53a5ab05eee4393be93e80cf43129cc2350e9a0311a8eb5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699c1c6e1c696bddce35bb8ae3c4d9a946d15c0d20f742584b73ba87c61cb961(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3563f7e3278d178b4d9e819bb43b64d56e6a211f4022f9bdf080fef755e0fd69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1e1b5d5a65df68cc73be318455983966138f0edd1b13efdc7cf3a74041bbf5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf355930a410f8100c4fca5c5f3c55a897846c2a093583432012e32c77d2a24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b65da4207036aeb54af6dfd38656ccdfc27a1316d1a9d532f0e8a0cacb12a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b4b0abbccdace67a7487bb3c8e4dc1003a46587a2b0661aae7a02ab8d91bee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea496b7c45351fe7c83c009638afc540287c483572fd70cb26d1a8f8e4624102(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b1fc2e60e47a02e23fdc84f0182dac78e80b09972d8987b67ed89ab0534b82(
    *,
    subnet_ids: typing.Sequence[builtins.str],
    security_groups_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dc82eca709c94cb4c6c1e9ba9b6c1c5f949b859db8d9944d1ab3ff84b2b301(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63247a57c3bb46ca02e2c6d76b4a5f3b36f68508e5adc1db83f6910e6832cac1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe94d210910ce0dbbd6df520f4ba34aacdb81248a5f3945dae4b8416bdbdc86(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925b831c93be6c588298a3de038a538e0cc68df09bea745e8242f56e0959ac50(
    value: typing.Optional[MskReplicatorKafkaClusterVpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efe5d0491620e3829681917b7ed43bdf3283ad03f1a6cd87296d0108fee035c(
    *,
    consumer_groups_to_replicate: typing.Sequence[builtins.str],
    consumer_groups_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    detect_and_copy_new_consumer_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    synchronise_consumer_group_offsets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9865fcae4a6953180fcf9e6df20c476cce8b206d18ee62c05c245d867419b0ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e16652a25396b5a775d003ca7dd12ca664e3175bb53d1b9e62272c5a21db01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573539f0b3589105ba8c95c3eefd34bfa1c1d47155cec45e011a480cddbf53ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbeaa2d7b4491ac8a665d07ea895627f390e741d31f35752901c18b64deabcc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861378ade661bc2bfdfb4c88df84e7cb135dcc32ee34228677252ca25fed75be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cbf3aafe61e22d27a4aa6a36504a13e1503f48e9473c92cc4d09fbe483c7b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66d41ae0001fbbe6104cfce9c74fbeb9deb339c291f746c7d81347d1fcb3e6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3214e258b7e3d4a55f26c4ed1a796f6b4c2ea751f43c54241914e92414ceaa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363f4ce3f8d80d686d041bc5c4334beb577370f8a24afe4003faca66287a50b7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b381fc833ce5a7893114596c3a5d1aff04031451b91663d4ef2271aa5bc89078(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8afd76c57cd632c3b0e4da9d72d6f318ee34ec86b681afbe748dc0882d17b3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c86dfb253932c2b4464a9ff477ed586b6b50963d771aafd0bea80d769118c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe9f15c6483cd856931f651bdf20e4f4a888a97a80172e68b4479c7047ccc1c(
    *,
    consumer_group_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
    source_kafka_cluster_arn: builtins.str,
    target_compression_type: builtins.str,
    target_kafka_cluster_arn: builtins.str,
    topic_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListTopicReplication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd44ff898236ae7749279647b264ea5ca06a0a3dd876bb877663e048e991404f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6641306103580b43651e2ffe57213cd56fb05f135d3615cd3db574a50c51072(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8697f8883af475413532018ebd7180b494109e6c26d4c860c7c44924b71ab307(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListTopicReplication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9aca7ec3a3594e6018fbb82ac01bd6653b43f4641b2316020f79bdd23134302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380f073276577a6ab7032f77cb376038bdff56c2dbbda6bc1e45c97871933a1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2e2a132eb33d3ed3b3d2c5aeab9eed36bb3e7efe1ff3127b63482e32828b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5819166c7560a7ba0d63e1ab53badf1981b88da1f14aead01c749266c4d20fcc(
    value: typing.Optional[MskReplicatorReplicationInfoListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfa8fbf6e00ccb9087cf40e72344fad2087417ca843e4058174296684579116(
    *,
    topics_to_replicate: typing.Sequence[builtins.str],
    copy_access_control_lists_for_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    copy_topic_configurations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    detect_and_copy_new_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    starting_position: typing.Optional[typing.Union[MskReplicatorReplicationInfoListTopicReplicationStartingPosition, typing.Dict[builtins.str, typing.Any]]] = None,
    topic_name_configuration: typing.Optional[typing.Union[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    topics_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e037ab4dbce8bca9b584dd3834c1fe2ea48d81463bc29e3a500f3ee4e42e8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e162a17f4d7f275bbe2fbffe4f42ae11380f540acbd96e26ed63bcf805c1e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4525fc799c200cab57b239a01815b758326e9ff7433dfc9594bf590d63c58a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3fef856885ebca3760432d676939b5e392665e60b7d265dc664c87938d212e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39d0d9ac6467b5b76ca5d1c11bfc359c5046e92d709d2c8d7560bbf50585d50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d46976fea46a211cc6520fa2f6b8163ad52071538ecad0150028e52c50f2d58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb475d551c2f15600181c542fc4696fdc8049bdebd7a08aedb7e9e9a0b439410(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b239009eadc8f577ad3200e2bed95f932b7282d988191c12c75735cbb3432c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f95f72d0f84df4dcae60e669ccf00b7ac6f1be3ffbe9882bab9ba929d8511d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c153b1dbb1503e408702ec1b6211bf8782b94ac3acfd5faa311e62ece1a929e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bac4bdd51c4ea80f4f6f99fd8436ac6f66c8ccd0b6ac80ee3dc16f4a552eb7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80d221759815300b2d336443b0a271aa609d5407821e78e2175504a9783e1a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efa25e634132f6a838a63c07cff95991c2a74588b447f78f9cbdfee2e53b475(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848dc1083e6aa5401638ce9df57f71eddaedab1bd59fb72989008d8bdab05b33(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d655a62211eb26e6dd2793c1cc536a3787fc71492b437db824c21b30ba00f1ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d660ab731f537802019f05d790610d473a419d7534a702e18bfbcf7adc0e694(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03d57497f40abdb4cd10808deb4d9480d69ae646b342e03d8b171833906f970(
    value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ea1748ad11f7cd7a46894abeba4c7db1d13d03d206864c1d7bd2a8c94370ce(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c512215fc4da2f44458704ffdc761bbe4ea355a7013053ad265a356de5dc12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235348cf06a929f3b0331f5f149e8369c02786bb90ac4b9674b78b80ee9cfa20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cedbcb01bd1148b4ea1511660d0ae548e3bfbef587b0c71d1ac12286bf9185b(
    value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5810e6a40b24632390e02a70da423e38227373f0696693a35a446a3603cceac6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26ac361e3460d30b1feee876f0a3d9eb24fa1385acb120acb0171c60ab486b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5777b442b42f0d49dcbc33cb5d84d8cd70560ebe158287c38d4b654e6ce437c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544c216cc705d23a403fe921fcb279f90cd1f858c50ce221ed6a99160f5da962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73821b22f61b004d3fb469babf4715acfc09cfec1cba134191297a5a80fbe0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a79550ba06674bd7c4b3a2f64450df756cbd04595f53eaf7934e6e753c3965(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
