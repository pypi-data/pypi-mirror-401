r'''
# `aws_keyspaces_table`

Refer to the Terraform Registry for docs: [`aws_keyspaces_table`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table).
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


class KeyspacesTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table aws_keyspaces_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        keyspace_name: builtins.str,
        schema_definition: typing.Union["KeyspacesTableSchemaDefinition", typing.Dict[builtins.str, typing.Any]],
        table_name: builtins.str,
        capacity_specification: typing.Optional[typing.Union["KeyspacesTableCapacitySpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        client_side_timestamps: typing.Optional[typing.Union["KeyspacesTableClientSideTimestamps", typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[typing.Union["KeyspacesTableComment", typing.Dict[builtins.str, typing.Any]]] = None,
        default_time_to_live: typing.Optional[jsii.Number] = None,
        encryption_specification: typing.Optional[typing.Union["KeyspacesTableEncryptionSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        point_in_time_recovery: typing.Optional[typing.Union["KeyspacesTablePointInTimeRecovery", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KeyspacesTableTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[typing.Union["KeyspacesTableTtl", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table aws_keyspaces_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param keyspace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#keyspace_name KeyspacesTable#keyspace_name}.
        :param schema_definition: schema_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#schema_definition KeyspacesTable#schema_definition}
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#table_name KeyspacesTable#table_name}.
        :param capacity_specification: capacity_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#capacity_specification KeyspacesTable#capacity_specification}
        :param client_side_timestamps: client_side_timestamps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#client_side_timestamps KeyspacesTable#client_side_timestamps}
        :param comment: comment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#comment KeyspacesTable#comment}
        :param default_time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#default_time_to_live KeyspacesTable#default_time_to_live}.
        :param encryption_specification: encryption_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#encryption_specification KeyspacesTable#encryption_specification}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#id KeyspacesTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param point_in_time_recovery: point_in_time_recovery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#point_in_time_recovery KeyspacesTable#point_in_time_recovery}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#region KeyspacesTable#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#tags KeyspacesTable#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#tags_all KeyspacesTable#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#timeouts KeyspacesTable#timeouts}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#ttl KeyspacesTable#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad311a4e22ec9a723b0b207247627f82a2ca740dd014c949f498831ab264dc5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KeyspacesTableConfig(
            keyspace_name=keyspace_name,
            schema_definition=schema_definition,
            table_name=table_name,
            capacity_specification=capacity_specification,
            client_side_timestamps=client_side_timestamps,
            comment=comment,
            default_time_to_live=default_time_to_live,
            encryption_specification=encryption_specification,
            id=id,
            point_in_time_recovery=point_in_time_recovery,
            region=region,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            ttl=ttl,
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
        '''Generates CDKTF code for importing a KeyspacesTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KeyspacesTable to import.
        :param import_from_id: The id of the existing KeyspacesTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KeyspacesTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7275b1fde81bb5695596da9f7286550494df217f124188dcaed28ba306c7da4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapacitySpecification")
    def put_capacity_specification(
        self,
        *,
        read_capacity_units: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
        write_capacity_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param read_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#read_capacity_units KeyspacesTable#read_capacity_units}.
        :param throughput_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#throughput_mode KeyspacesTable#throughput_mode}.
        :param write_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#write_capacity_units KeyspacesTable#write_capacity_units}.
        '''
        value = KeyspacesTableCapacitySpecification(
            read_capacity_units=read_capacity_units,
            throughput_mode=throughput_mode,
            write_capacity_units=write_capacity_units,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacitySpecification", [value]))

    @jsii.member(jsii_name="putClientSideTimestamps")
    def put_client_side_timestamps(self, *, status: builtins.str) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.
        '''
        value = KeyspacesTableClientSideTimestamps(status=status)

        return typing.cast(None, jsii.invoke(self, "putClientSideTimestamps", [value]))

    @jsii.member(jsii_name="putComment")
    def put_comment(self, *, message: typing.Optional[builtins.str] = None) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#message KeyspacesTable#message}.
        '''
        value = KeyspacesTableComment(message=message)

        return typing.cast(None, jsii.invoke(self, "putComment", [value]))

    @jsii.member(jsii_name="putEncryptionSpecification")
    def put_encryption_specification(
        self,
        *,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#kms_key_identifier KeyspacesTable#kms_key_identifier}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#type KeyspacesTable#type}.
        '''
        value = KeyspacesTableEncryptionSpecification(
            kms_key_identifier=kms_key_identifier, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionSpecification", [value]))

    @jsii.member(jsii_name="putPointInTimeRecovery")
    def put_point_in_time_recovery(
        self,
        *,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.
        '''
        value = KeyspacesTablePointInTimeRecovery(status=status)

        return typing.cast(None, jsii.invoke(self, "putPointInTimeRecovery", [value]))

    @jsii.member(jsii_name="putSchemaDefinition")
    def put_schema_definition(
        self,
        *,
        column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionColumn", typing.Dict[builtins.str, typing.Any]]]],
        partition_key: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionPartitionKey", typing.Dict[builtins.str, typing.Any]]]],
        clustering_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionClusteringKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        static_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionStaticColumn", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#column KeyspacesTable#column}
        :param partition_key: partition_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#partition_key KeyspacesTable#partition_key}
        :param clustering_key: clustering_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#clustering_key KeyspacesTable#clustering_key}
        :param static_column: static_column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#static_column KeyspacesTable#static_column}
        '''
        value = KeyspacesTableSchemaDefinition(
            column=column,
            partition_key=partition_key,
            clustering_key=clustering_key,
            static_column=static_column,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaDefinition", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#create KeyspacesTable#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#delete KeyspacesTable#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#update KeyspacesTable#update}.
        '''
        value = KeyspacesTableTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTtl")
    def put_ttl(self, *, status: builtins.str) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.
        '''
        value = KeyspacesTableTtl(status=status)

        return typing.cast(None, jsii.invoke(self, "putTtl", [value]))

    @jsii.member(jsii_name="resetCapacitySpecification")
    def reset_capacity_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacitySpecification", []))

    @jsii.member(jsii_name="resetClientSideTimestamps")
    def reset_client_side_timestamps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSideTimestamps", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDefaultTimeToLive")
    def reset_default_time_to_live(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTimeToLive", []))

    @jsii.member(jsii_name="resetEncryptionSpecification")
    def reset_encryption_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionSpecification", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPointInTimeRecovery")
    def reset_point_in_time_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeRecovery", []))

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

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

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
    @jsii.member(jsii_name="capacitySpecification")
    def capacity_specification(
        self,
    ) -> "KeyspacesTableCapacitySpecificationOutputReference":
        return typing.cast("KeyspacesTableCapacitySpecificationOutputReference", jsii.get(self, "capacitySpecification"))

    @builtins.property
    @jsii.member(jsii_name="clientSideTimestamps")
    def client_side_timestamps(
        self,
    ) -> "KeyspacesTableClientSideTimestampsOutputReference":
        return typing.cast("KeyspacesTableClientSideTimestampsOutputReference", jsii.get(self, "clientSideTimestamps"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> "KeyspacesTableCommentOutputReference":
        return typing.cast("KeyspacesTableCommentOutputReference", jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpecification")
    def encryption_specification(
        self,
    ) -> "KeyspacesTableEncryptionSpecificationOutputReference":
        return typing.cast("KeyspacesTableEncryptionSpecificationOutputReference", jsii.get(self, "encryptionSpecification"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecovery")
    def point_in_time_recovery(
        self,
    ) -> "KeyspacesTablePointInTimeRecoveryOutputReference":
        return typing.cast("KeyspacesTablePointInTimeRecoveryOutputReference", jsii.get(self, "pointInTimeRecovery"))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinition")
    def schema_definition(self) -> "KeyspacesTableSchemaDefinitionOutputReference":
        return typing.cast("KeyspacesTableSchemaDefinitionOutputReference", jsii.get(self, "schemaDefinition"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KeyspacesTableTimeoutsOutputReference":
        return typing.cast("KeyspacesTableTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> "KeyspacesTableTtlOutputReference":
        return typing.cast("KeyspacesTableTtlOutputReference", jsii.get(self, "ttl"))

    @builtins.property
    @jsii.member(jsii_name="capacitySpecificationInput")
    def capacity_specification_input(
        self,
    ) -> typing.Optional["KeyspacesTableCapacitySpecification"]:
        return typing.cast(typing.Optional["KeyspacesTableCapacitySpecification"], jsii.get(self, "capacitySpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSideTimestampsInput")
    def client_side_timestamps_input(
        self,
    ) -> typing.Optional["KeyspacesTableClientSideTimestamps"]:
        return typing.cast(typing.Optional["KeyspacesTableClientSideTimestamps"], jsii.get(self, "clientSideTimestampsInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional["KeyspacesTableComment"]:
        return typing.cast(typing.Optional["KeyspacesTableComment"], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTimeToLiveInput")
    def default_time_to_live_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTimeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpecificationInput")
    def encryption_specification_input(
        self,
    ) -> typing.Optional["KeyspacesTableEncryptionSpecification"]:
        return typing.cast(typing.Optional["KeyspacesTableEncryptionSpecification"], jsii.get(self, "encryptionSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyspaceNameInput")
    def keyspace_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyspaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoveryInput")
    def point_in_time_recovery_input(
        self,
    ) -> typing.Optional["KeyspacesTablePointInTimeRecovery"]:
        return typing.cast(typing.Optional["KeyspacesTablePointInTimeRecovery"], jsii.get(self, "pointInTimeRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaDefinitionInput")
    def schema_definition_input(
        self,
    ) -> typing.Optional["KeyspacesTableSchemaDefinition"]:
        return typing.cast(typing.Optional["KeyspacesTableSchemaDefinition"], jsii.get(self, "schemaDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeyspacesTableTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeyspacesTableTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional["KeyspacesTableTtl"]:
        return typing.cast(typing.Optional["KeyspacesTableTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTimeToLive")
    def default_time_to_live(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTimeToLive"))

    @default_time_to_live.setter
    def default_time_to_live(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba023622308621005f60e48f73651c0fe08738e5891daf317a38c0d15eef7d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTimeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8814022220127aafeda87ee0b3b0713823fe3e38d7bb953f2f8a68c7ab4dcf48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyspaceName")
    def keyspace_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyspaceName"))

    @keyspace_name.setter
    def keyspace_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe055a1c7e90939596a552d8cfeb7f321900c225c9b0bcae53addd097095196b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyspaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b332da123395aae3771126870373e9fb25483830f3ae0530e80da9d76a63963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1c976313d3c8655c45537a6583d680196e29562f27c16df71d2bbda75211c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1cd1ac5667cf41fb6937c55d958e08d4887dc13a5d1370a1c87c1b40d7a9fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c72b0d49fb7d0e26e24777d9d7a09570934a128ee074798787a71a010e115b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableCapacitySpecification",
    jsii_struct_bases=[],
    name_mapping={
        "read_capacity_units": "readCapacityUnits",
        "throughput_mode": "throughputMode",
        "write_capacity_units": "writeCapacityUnits",
    },
)
class KeyspacesTableCapacitySpecification:
    def __init__(
        self,
        *,
        read_capacity_units: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
        write_capacity_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param read_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#read_capacity_units KeyspacesTable#read_capacity_units}.
        :param throughput_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#throughput_mode KeyspacesTable#throughput_mode}.
        :param write_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#write_capacity_units KeyspacesTable#write_capacity_units}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ddf8044acd5cad88da29b824fe9df5c41e8e5a465ae398fec3d29d975f8b56c)
            check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
            check_type(argname="argument throughput_mode", value=throughput_mode, expected_type=type_hints["throughput_mode"])
            check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read_capacity_units is not None:
            self._values["read_capacity_units"] = read_capacity_units
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode
        if write_capacity_units is not None:
            self._values["write_capacity_units"] = write_capacity_units

    @builtins.property
    def read_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#read_capacity_units KeyspacesTable#read_capacity_units}.'''
        result = self._values.get("read_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#throughput_mode KeyspacesTable#throughput_mode}.'''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def write_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#write_capacity_units KeyspacesTable#write_capacity_units}.'''
        result = self._values.get("write_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableCapacitySpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableCapacitySpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableCapacitySpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__744ca7c40de7dbca5ff62b3ff17123ff000c04df7d6dc74ac1864004d48975a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadCapacityUnits")
    def reset_read_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadCapacityUnits", []))

    @jsii.member(jsii_name="resetThroughputMode")
    def reset_throughput_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputMode", []))

    @jsii.member(jsii_name="resetWriteCapacityUnits")
    def reset_write_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteCapacityUnits", []))

    @builtins.property
    @jsii.member(jsii_name="readCapacityUnitsInput")
    def read_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputModeInput")
    def throughput_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throughputModeInput"))

    @builtins.property
    @jsii.member(jsii_name="writeCapacityUnitsInput")
    def write_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="readCapacityUnits")
    def read_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readCapacityUnits"))

    @read_capacity_units.setter
    def read_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d90648d641ab56a46e0510b6051bcb844bd1bb13142e3e76d1b3e062feea548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throughputMode"))

    @throughput_mode.setter
    def throughput_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2d1efad787adc8c5d1a15b5ac79f95291e4ecd1ddc03223dd08558260edacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeCapacityUnits")
    def write_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "writeCapacityUnits"))

    @write_capacity_units.setter
    def write_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c760518118a769de9ba697c7cb237c00326bb27538bde3c3f984165f752985e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTableCapacitySpecification]:
        return typing.cast(typing.Optional[KeyspacesTableCapacitySpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyspacesTableCapacitySpecification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679e71cb61881b4fc91fe8e363fb2b58435063fe4eb16c137648d8aa3f14fb13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableClientSideTimestamps",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class KeyspacesTableClientSideTimestamps:
    def __init__(self, *, status: builtins.str) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe33f9ec5830fedcd854300405980e0955e913ed8a4371606d70ca5eb9ee086)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableClientSideTimestamps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableClientSideTimestampsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableClientSideTimestampsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e71acbb0068d7e7221c9d311e1290ab71b15a521f747ea095e2ed1a2abc54a40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90a717583e5084b7f8e6ef42c34c6994eb02f6043468eccc0b3fa2f15567cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTableClientSideTimestamps]:
        return typing.cast(typing.Optional[KeyspacesTableClientSideTimestamps], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyspacesTableClientSideTimestamps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d8202b5a67af5a4c619c541ca89c10949bcc85eb7bfd7930fec7d57e5ce496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableComment",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class KeyspacesTableComment:
    def __init__(self, *, message: typing.Optional[builtins.str] = None) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#message KeyspacesTable#message}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f809dd2e9bff4b75d9fa5c7d7ae7b4ca1bffa07f63826bfab55e9cadf5456930)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#message KeyspacesTable#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afeff1ae2508f0052254b85e665af22a411fc5d69119d818a5adbe8ef461f840)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34beec580c19a75dd2de2c5a7f8120de5402767961adba49ccbc5c868bfa937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTableComment]:
        return typing.cast(typing.Optional[KeyspacesTableComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KeyspacesTableComment]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e61bc4a479c49f8a5a727453c505aa87870dd646ec62f30210525479befecff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "keyspace_name": "keyspaceName",
        "schema_definition": "schemaDefinition",
        "table_name": "tableName",
        "capacity_specification": "capacitySpecification",
        "client_side_timestamps": "clientSideTimestamps",
        "comment": "comment",
        "default_time_to_live": "defaultTimeToLive",
        "encryption_specification": "encryptionSpecification",
        "id": "id",
        "point_in_time_recovery": "pointInTimeRecovery",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "ttl": "ttl",
    },
)
class KeyspacesTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        keyspace_name: builtins.str,
        schema_definition: typing.Union["KeyspacesTableSchemaDefinition", typing.Dict[builtins.str, typing.Any]],
        table_name: builtins.str,
        capacity_specification: typing.Optional[typing.Union[KeyspacesTableCapacitySpecification, typing.Dict[builtins.str, typing.Any]]] = None,
        client_side_timestamps: typing.Optional[typing.Union[KeyspacesTableClientSideTimestamps, typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[typing.Union[KeyspacesTableComment, typing.Dict[builtins.str, typing.Any]]] = None,
        default_time_to_live: typing.Optional[jsii.Number] = None,
        encryption_specification: typing.Optional[typing.Union["KeyspacesTableEncryptionSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        point_in_time_recovery: typing.Optional[typing.Union["KeyspacesTablePointInTimeRecovery", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KeyspacesTableTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[typing.Union["KeyspacesTableTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param keyspace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#keyspace_name KeyspacesTable#keyspace_name}.
        :param schema_definition: schema_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#schema_definition KeyspacesTable#schema_definition}
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#table_name KeyspacesTable#table_name}.
        :param capacity_specification: capacity_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#capacity_specification KeyspacesTable#capacity_specification}
        :param client_side_timestamps: client_side_timestamps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#client_side_timestamps KeyspacesTable#client_side_timestamps}
        :param comment: comment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#comment KeyspacesTable#comment}
        :param default_time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#default_time_to_live KeyspacesTable#default_time_to_live}.
        :param encryption_specification: encryption_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#encryption_specification KeyspacesTable#encryption_specification}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#id KeyspacesTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param point_in_time_recovery: point_in_time_recovery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#point_in_time_recovery KeyspacesTable#point_in_time_recovery}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#region KeyspacesTable#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#tags KeyspacesTable#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#tags_all KeyspacesTable#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#timeouts KeyspacesTable#timeouts}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#ttl KeyspacesTable#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schema_definition, dict):
            schema_definition = KeyspacesTableSchemaDefinition(**schema_definition)
        if isinstance(capacity_specification, dict):
            capacity_specification = KeyspacesTableCapacitySpecification(**capacity_specification)
        if isinstance(client_side_timestamps, dict):
            client_side_timestamps = KeyspacesTableClientSideTimestamps(**client_side_timestamps)
        if isinstance(comment, dict):
            comment = KeyspacesTableComment(**comment)
        if isinstance(encryption_specification, dict):
            encryption_specification = KeyspacesTableEncryptionSpecification(**encryption_specification)
        if isinstance(point_in_time_recovery, dict):
            point_in_time_recovery = KeyspacesTablePointInTimeRecovery(**point_in_time_recovery)
        if isinstance(timeouts, dict):
            timeouts = KeyspacesTableTimeouts(**timeouts)
        if isinstance(ttl, dict):
            ttl = KeyspacesTableTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff99caf1a35b1eab8e94a6307d83435e3498faa4f6b4952d482ceb389d51822d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument keyspace_name", value=keyspace_name, expected_type=type_hints["keyspace_name"])
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument capacity_specification", value=capacity_specification, expected_type=type_hints["capacity_specification"])
            check_type(argname="argument client_side_timestamps", value=client_side_timestamps, expected_type=type_hints["client_side_timestamps"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument default_time_to_live", value=default_time_to_live, expected_type=type_hints["default_time_to_live"])
            check_type(argname="argument encryption_specification", value=encryption_specification, expected_type=type_hints["encryption_specification"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument point_in_time_recovery", value=point_in_time_recovery, expected_type=type_hints["point_in_time_recovery"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keyspace_name": keyspace_name,
            "schema_definition": schema_definition,
            "table_name": table_name,
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
        if capacity_specification is not None:
            self._values["capacity_specification"] = capacity_specification
        if client_side_timestamps is not None:
            self._values["client_side_timestamps"] = client_side_timestamps
        if comment is not None:
            self._values["comment"] = comment
        if default_time_to_live is not None:
            self._values["default_time_to_live"] = default_time_to_live
        if encryption_specification is not None:
            self._values["encryption_specification"] = encryption_specification
        if id is not None:
            self._values["id"] = id
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if ttl is not None:
            self._values["ttl"] = ttl

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
    def keyspace_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#keyspace_name KeyspacesTable#keyspace_name}.'''
        result = self._values.get("keyspace_name")
        assert result is not None, "Required property 'keyspace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_definition(self) -> "KeyspacesTableSchemaDefinition":
        '''schema_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#schema_definition KeyspacesTable#schema_definition}
        '''
        result = self._values.get("schema_definition")
        assert result is not None, "Required property 'schema_definition' is missing"
        return typing.cast("KeyspacesTableSchemaDefinition", result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#table_name KeyspacesTable#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_specification(
        self,
    ) -> typing.Optional[KeyspacesTableCapacitySpecification]:
        '''capacity_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#capacity_specification KeyspacesTable#capacity_specification}
        '''
        result = self._values.get("capacity_specification")
        return typing.cast(typing.Optional[KeyspacesTableCapacitySpecification], result)

    @builtins.property
    def client_side_timestamps(
        self,
    ) -> typing.Optional[KeyspacesTableClientSideTimestamps]:
        '''client_side_timestamps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#client_side_timestamps KeyspacesTable#client_side_timestamps}
        '''
        result = self._values.get("client_side_timestamps")
        return typing.cast(typing.Optional[KeyspacesTableClientSideTimestamps], result)

    @builtins.property
    def comment(self) -> typing.Optional[KeyspacesTableComment]:
        '''comment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#comment KeyspacesTable#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[KeyspacesTableComment], result)

    @builtins.property
    def default_time_to_live(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#default_time_to_live KeyspacesTable#default_time_to_live}.'''
        result = self._values.get("default_time_to_live")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def encryption_specification(
        self,
    ) -> typing.Optional["KeyspacesTableEncryptionSpecification"]:
        '''encryption_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#encryption_specification KeyspacesTable#encryption_specification}
        '''
        result = self._values.get("encryption_specification")
        return typing.cast(typing.Optional["KeyspacesTableEncryptionSpecification"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#id KeyspacesTable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def point_in_time_recovery(
        self,
    ) -> typing.Optional["KeyspacesTablePointInTimeRecovery"]:
        '''point_in_time_recovery block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#point_in_time_recovery KeyspacesTable#point_in_time_recovery}
        '''
        result = self._values.get("point_in_time_recovery")
        return typing.cast(typing.Optional["KeyspacesTablePointInTimeRecovery"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#region KeyspacesTable#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#tags KeyspacesTable#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#tags_all KeyspacesTable#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KeyspacesTableTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#timeouts KeyspacesTable#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KeyspacesTableTimeouts"], result)

    @builtins.property
    def ttl(self) -> typing.Optional["KeyspacesTableTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#ttl KeyspacesTable#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["KeyspacesTableTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableEncryptionSpecification",
    jsii_struct_bases=[],
    name_mapping={"kms_key_identifier": "kmsKeyIdentifier", "type": "type"},
)
class KeyspacesTableEncryptionSpecification:
    def __init__(
        self,
        *,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#kms_key_identifier KeyspacesTable#kms_key_identifier}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#type KeyspacesTable#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f35384c9ec41b19fc276b116da0c00381c734c0ae7df830100b8dd9e67cdc2)
            check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_identifier is not None:
            self._values["kms_key_identifier"] = kms_key_identifier
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def kms_key_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#kms_key_identifier KeyspacesTable#kms_key_identifier}.'''
        result = self._values.get("kms_key_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#type KeyspacesTable#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableEncryptionSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableEncryptionSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableEncryptionSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67f25c07b6f0d789396b11987d88548e310d0151c2b4a55524b2f060896e605c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyIdentifier")
    def reset_kms_key_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyIdentifier", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifierInput")
    def kms_key_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyIdentifier"))

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab6b72a5c59e0fa89aa1b78f5638d9ce1935081e4ea113649816481c61e5dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21deabbf9ceddc5f9143205a562b80c453a32e149fc0e3607856b3f8e1f2be2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTableEncryptionSpecification]:
        return typing.cast(typing.Optional[KeyspacesTableEncryptionSpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyspacesTableEncryptionSpecification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4267d82da9b63292852485da132e496edef31defe38a27aa8f36f1553c7c4c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTablePointInTimeRecovery",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class KeyspacesTablePointInTimeRecovery:
    def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d353ba8c4baa6d3f68928dee706ddc7942d858feac3f583626026a55524f11)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTablePointInTimeRecovery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTablePointInTimeRecoveryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTablePointInTimeRecoveryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfbdfbdf299afdb090a090261ae6c965f9ac5c28680f6d0885df42934bbf6ff1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498c9eeb26556e02b96fe4bf67dbcbcb02a5cdc4aa0eb93bfb6e7127e05c96b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTablePointInTimeRecovery]:
        return typing.cast(typing.Optional[KeyspacesTablePointInTimeRecovery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyspacesTablePointInTimeRecovery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305ffa0c007b5d9a79e76014951b3913694ecfb7d04ec58a41223f3bf368f645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "partition_key": "partitionKey",
        "clustering_key": "clusteringKey",
        "static_column": "staticColumn",
    },
)
class KeyspacesTableSchemaDefinition:
    def __init__(
        self,
        *,
        column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionColumn", typing.Dict[builtins.str, typing.Any]]]],
        partition_key: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionPartitionKey", typing.Dict[builtins.str, typing.Any]]]],
        clustering_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionClusteringKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        static_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionStaticColumn", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#column KeyspacesTable#column}
        :param partition_key: partition_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#partition_key KeyspacesTable#partition_key}
        :param clustering_key: clustering_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#clustering_key KeyspacesTable#clustering_key}
        :param static_column: static_column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#static_column KeyspacesTable#static_column}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84f3e45946fa1468b7296dd672117e964d14e432f51c8207da557f92942cc95)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument clustering_key", value=clustering_key, expected_type=type_hints["clustering_key"])
            check_type(argname="argument static_column", value=static_column, expected_type=type_hints["static_column"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "partition_key": partition_key,
        }
        if clustering_key is not None:
            self._values["clustering_key"] = clustering_key
        if static_column is not None:
            self._values["static_column"] = static_column

    @builtins.property
    def column(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionColumn"]]:
        '''column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#column KeyspacesTable#column}
        '''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionColumn"]], result)

    @builtins.property
    def partition_key(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionPartitionKey"]]:
        '''partition_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#partition_key KeyspacesTable#partition_key}
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionPartitionKey"]], result)

    @builtins.property
    def clustering_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionClusteringKey"]]]:
        '''clustering_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#clustering_key KeyspacesTable#clustering_key}
        '''
        result = self._values.get("clustering_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionClusteringKey"]]], result)

    @builtins.property
    def static_column(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionStaticColumn"]]]:
        '''static_column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#static_column KeyspacesTable#static_column}
        '''
        result = self._values.get("static_column")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionStaticColumn"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableSchemaDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionClusteringKey",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "order_by": "orderBy"},
)
class KeyspacesTableSchemaDefinitionClusteringKey:
    def __init__(self, *, name: builtins.str, order_by: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.
        :param order_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#order_by KeyspacesTable#order_by}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27982153fbacd935c044eb63f87fbb4e96c3f3ca2dba0802afe72e0ed68463cf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order_by", value=order_by, expected_type=type_hints["order_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "order_by": order_by,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def order_by(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#order_by KeyspacesTable#order_by}.'''
        result = self._values.get("order_by")
        assert result is not None, "Required property 'order_by' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableSchemaDefinitionClusteringKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableSchemaDefinitionClusteringKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionClusteringKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99fa1d84e42f624d8630819a06da512855f3ea411d6c5df55af788cddf6609e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KeyspacesTableSchemaDefinitionClusteringKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e38295606920461416f9a39f707920ee9ef84915f1e0cbc7e818b9ab4bc8532)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KeyspacesTableSchemaDefinitionClusteringKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02e5ad00c8ed32f2d20168b656ae87ea178b9cf3e36006d7ee053773ea92aae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7a67c9fab16baf2923d3ef826e4521c941bd853ec35f57f9aac5efee6aacaa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bad2a4fe86ad06b03ae7f3dfdb14e61fe3ce9f673e70c97f96f63ea32298adcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionClusteringKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionClusteringKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionClusteringKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627443ee7b541c3522376a2f8c5afac3bfdc3fc06ab568009f3e8a5cd7a6c1de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyspacesTableSchemaDefinitionClusteringKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionClusteringKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ecd21dc4f1956fdc5f029d83096ab7f8e8d962bf0c88313b3fc5791f13f7588)
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
    @jsii.member(jsii_name="orderByInput")
    def order_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderByInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d5de665fa74adfc0069c3233e0102045b41e95bd8aa6768d6e6cea843b0ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orderBy")
    def order_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderBy"))

    @order_by.setter
    def order_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abde960c5af4ece7c32d1933281e486b2bdcdc03e5ada0dd896b1a91cb3dcdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionClusteringKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionClusteringKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionClusteringKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a6a3447d318fd15f43cd77b268531925a53c331d2c63da3929b1e39a5a6404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionColumn",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class KeyspacesTableSchemaDefinitionColumn:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#type KeyspacesTable#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e73353cceba7fc98493113cedb4004ec31702a541f20b7c7e221e0c7c060504)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#type KeyspacesTable#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableSchemaDefinitionColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableSchemaDefinitionColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3cffc048dd1e62c7c74a8cf0cad3d95e124557f2b6fd3daab0250362959cb30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KeyspacesTableSchemaDefinitionColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91db7d72f5cea9cfe6b9c81eadcc87ac25d8b1c6f190c6d18726eb1c7390c41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KeyspacesTableSchemaDefinitionColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec14eaaecc8d5c82d0e627b899627362d5bffea2e3cae7b352e66483a9459cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53356a420b41a045e63c3aa0ca36f9ae6830aad36fcdb26059bd5039a0acb9de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__159317427cab47f2bc9c0fe2c37d94f491831fbe91a695683eab744322438403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c28cbda99cce75b30338cf3ebb0caccd64c140bf01e3b3700f74bae3d9b483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyspacesTableSchemaDefinitionColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e8d275aef3414ca1a2689b00289416a660059dc20ba126010c5b59c6866b9c1)
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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fd963d18888083ab364c6e2019f549bcae1584ffff936f49348669a525bd1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aee966024ca918cb5f294b320270d39986f0694b5eef4f0c0777bcc3dcab09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6861ee8a96fbc3972b1d5a681723d84bb175d023340769d0923a4d67888dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyspacesTableSchemaDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29e6f62b65d2d6849ac6043476e133b18ddb27456c50b266b873215ec27c011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusteringKey")
    def put_clustering_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionClusteringKey, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1658f95075e3b13086599c9940c92928841f16f73d32fa23dfe29d31db5f3b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClusteringKey", [value]))

    @jsii.member(jsii_name="putColumn")
    def put_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionColumn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af4ef0189777b527f00164ffbc7bebc7da660f193deb6420f279fb023809e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumn", [value]))

    @jsii.member(jsii_name="putPartitionKey")
    def put_partition_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionPartitionKey", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf4d9b0c0637e5cbad8533d5dd4c55f4a09a232968088086620ec0f9bf56fac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPartitionKey", [value]))

    @jsii.member(jsii_name="putStaticColumn")
    def put_static_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KeyspacesTableSchemaDefinitionStaticColumn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3f86c4ad0a6f30ab23732b35b7640237a7af26159c75cf7b6e112d2df89089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStaticColumn", [value]))

    @jsii.member(jsii_name="resetClusteringKey")
    def reset_clustering_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusteringKey", []))

    @jsii.member(jsii_name="resetStaticColumn")
    def reset_static_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticColumn", []))

    @builtins.property
    @jsii.member(jsii_name="clusteringKey")
    def clustering_key(self) -> KeyspacesTableSchemaDefinitionClusteringKeyList:
        return typing.cast(KeyspacesTableSchemaDefinitionClusteringKeyList, jsii.get(self, "clusteringKey"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> KeyspacesTableSchemaDefinitionColumnList:
        return typing.cast(KeyspacesTableSchemaDefinitionColumnList, jsii.get(self, "column"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> "KeyspacesTableSchemaDefinitionPartitionKeyList":
        return typing.cast("KeyspacesTableSchemaDefinitionPartitionKeyList", jsii.get(self, "partitionKey"))

    @builtins.property
    @jsii.member(jsii_name="staticColumn")
    def static_column(self) -> "KeyspacesTableSchemaDefinitionStaticColumnList":
        return typing.cast("KeyspacesTableSchemaDefinitionStaticColumnList", jsii.get(self, "staticColumn"))

    @builtins.property
    @jsii.member(jsii_name="clusteringKeyInput")
    def clustering_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionClusteringKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionClusteringKey]]], jsii.get(self, "clusteringKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionColumn]]], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionPartitionKey"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionPartitionKey"]]], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="staticColumnInput")
    def static_column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionStaticColumn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KeyspacesTableSchemaDefinitionStaticColumn"]]], jsii.get(self, "staticColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTableSchemaDefinition]:
        return typing.cast(typing.Optional[KeyspacesTableSchemaDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KeyspacesTableSchemaDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac6265452e606d12a6b8d329d5c0a43ffdc5c84ab897faae101f0f15fed5be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionPartitionKey",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class KeyspacesTableSchemaDefinitionPartitionKey:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5b1be3fa037bc79dd531c29bf077f24d999ce0b4f67e9e43b2b466d5ee4cd3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableSchemaDefinitionPartitionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableSchemaDefinitionPartitionKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionPartitionKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a531a2acd914a3ad04f45f6fe13ad6361be1ef55333aafb7d5c72125c1f099c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KeyspacesTableSchemaDefinitionPartitionKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa15c69321a209eced442f74dc2253f2df742fc80a57cd17f5b0f9c6f42514cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KeyspacesTableSchemaDefinitionPartitionKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34a751f3a49da1b0d6c14089444145192a85b32867c539bae398192132f6541)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c917aa3057bfb9c4aab287c44386526409a4ccd7a6f4a6009e68fd5211457559)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f3d4132a7af4276f4b174134f27b244b40fafe5481bc5156d09fefdb4a5f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionPartitionKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionPartitionKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionPartitionKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d724ec52aff075c9d18229a74b7c7ac3dd100c4b046199218067a82ccbcfddbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyspacesTableSchemaDefinitionPartitionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionPartitionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4fc224e205108877037ee4c56ffe14377dcbb64444fe3d1548249d10eb0ce5b)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b290b489eae3bbc0147c4bd8eb093bca571d8a371bde23f97423fe8f826370e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionPartitionKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionPartitionKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionPartitionKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9dba4efb85fe8a7bdd209d7fd12218329a768455338360e90e43a9370dd36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionStaticColumn",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class KeyspacesTableSchemaDefinitionStaticColumn:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308712ee5502986980f5df61d3a939798536b3e85eb37c92139cbf2baeb6152a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#name KeyspacesTable#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableSchemaDefinitionStaticColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableSchemaDefinitionStaticColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionStaticColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c6ddfc6485601fa787b804fc43393d02be74ba8960d1731b7325786443064a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KeyspacesTableSchemaDefinitionStaticColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb049d67740c772d73ca25ada7b261c4f61ac7d1a04dbf6b49037fdfbc74c7c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KeyspacesTableSchemaDefinitionStaticColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52ef153e8bd128afcf234ff641fa437a4d8eeb77533e49b08839c09d0614f57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6494156315fa77f7eb6a22dd9277def5cbec5d9d7b2dce64fd700587ec264c7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2162fea7d4cba9534ec9030b813f7287a3a5821ce5e0775c63b5b1d9b8a3309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionStaticColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionStaticColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionStaticColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947d66482cc3ffec7c9f63dca65bb82aa3c7082905f08c437012c8a1ba96ee8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KeyspacesTableSchemaDefinitionStaticColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableSchemaDefinitionStaticColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__073cfe199db1c8b3ed6f02f8de4b6028ff83d3776da03f822277037e1cf9df83)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1fe17320c360c7e61c703ebc05bdc09e37ec4cb2380e7f71bc689439ef495e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionStaticColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionStaticColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionStaticColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17380c78233549bb23941d8f5927a509ae8891bd830a8069518249302e501df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KeyspacesTableTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#create KeyspacesTable#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#delete KeyspacesTable#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#update KeyspacesTable#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff23861c63717cd4afa068e810b2c66f87985465919491dbd367cd22800753e2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#create KeyspacesTable#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#delete KeyspacesTable#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#update KeyspacesTable#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9828091ab697981d5f3abc4328b0b654a06eb785dcab1120bdacd3093056756)
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
            type_hints = typing.get_type_hints(_typecheckingstub__456902e2c66c1d92587ea98e3180547f10417791df4807911df78a57adb62284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3233fc9126ef9aa35cbe312f6c9c0b033371f76a4984b1ff2c7891b97ef71355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf64bc714587bbce566beaa4579fb578edf285ee3594cee186e9e8e16e3677f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7946e45b3f0c2cbc4c011a8c6da4ba7b15163aa885d6da74bb16742eeb8abf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableTtl",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class KeyspacesTableTtl:
    def __init__(self, *, status: builtins.str) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8859b555e0740ed0fbd684ca563fd3d3370ec41a6c5cfb9d2e7d6afb7b225bd5)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/keyspaces_table#status KeyspacesTable#status}.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyspacesTableTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyspacesTableTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.keyspacesTable.KeyspacesTableTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fd54739252b7d1286a91efc7702d259e7044c7467adc5d2b89e5602aa3d24f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d9cb51ad854ed5f90584a9b448e7ae496ab4528eca66c14253f44dce66b018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeyspacesTableTtl]:
        return typing.cast(typing.Optional[KeyspacesTableTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KeyspacesTableTtl]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb5700bdd7e56958d3d0375934f9d263857d71fc7fbaa575b22a263873b565cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KeyspacesTable",
    "KeyspacesTableCapacitySpecification",
    "KeyspacesTableCapacitySpecificationOutputReference",
    "KeyspacesTableClientSideTimestamps",
    "KeyspacesTableClientSideTimestampsOutputReference",
    "KeyspacesTableComment",
    "KeyspacesTableCommentOutputReference",
    "KeyspacesTableConfig",
    "KeyspacesTableEncryptionSpecification",
    "KeyspacesTableEncryptionSpecificationOutputReference",
    "KeyspacesTablePointInTimeRecovery",
    "KeyspacesTablePointInTimeRecoveryOutputReference",
    "KeyspacesTableSchemaDefinition",
    "KeyspacesTableSchemaDefinitionClusteringKey",
    "KeyspacesTableSchemaDefinitionClusteringKeyList",
    "KeyspacesTableSchemaDefinitionClusteringKeyOutputReference",
    "KeyspacesTableSchemaDefinitionColumn",
    "KeyspacesTableSchemaDefinitionColumnList",
    "KeyspacesTableSchemaDefinitionColumnOutputReference",
    "KeyspacesTableSchemaDefinitionOutputReference",
    "KeyspacesTableSchemaDefinitionPartitionKey",
    "KeyspacesTableSchemaDefinitionPartitionKeyList",
    "KeyspacesTableSchemaDefinitionPartitionKeyOutputReference",
    "KeyspacesTableSchemaDefinitionStaticColumn",
    "KeyspacesTableSchemaDefinitionStaticColumnList",
    "KeyspacesTableSchemaDefinitionStaticColumnOutputReference",
    "KeyspacesTableTimeouts",
    "KeyspacesTableTimeoutsOutputReference",
    "KeyspacesTableTtl",
    "KeyspacesTableTtlOutputReference",
]

publication.publish()

def _typecheckingstub__ad311a4e22ec9a723b0b207247627f82a2ca740dd014c949f498831ab264dc5d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    keyspace_name: builtins.str,
    schema_definition: typing.Union[KeyspacesTableSchemaDefinition, typing.Dict[builtins.str, typing.Any]],
    table_name: builtins.str,
    capacity_specification: typing.Optional[typing.Union[KeyspacesTableCapacitySpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    client_side_timestamps: typing.Optional[typing.Union[KeyspacesTableClientSideTimestamps, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[typing.Union[KeyspacesTableComment, typing.Dict[builtins.str, typing.Any]]] = None,
    default_time_to_live: typing.Optional[jsii.Number] = None,
    encryption_specification: typing.Optional[typing.Union[KeyspacesTableEncryptionSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    point_in_time_recovery: typing.Optional[typing.Union[KeyspacesTablePointInTimeRecovery, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KeyspacesTableTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[typing.Union[KeyspacesTableTtl, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7275b1fde81bb5695596da9f7286550494df217f124188dcaed28ba306c7da4a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba023622308621005f60e48f73651c0fe08738e5891daf317a38c0d15eef7d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8814022220127aafeda87ee0b3b0713823fe3e38d7bb953f2f8a68c7ab4dcf48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe055a1c7e90939596a552d8cfeb7f321900c225c9b0bcae53addd097095196b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b332da123395aae3771126870373e9fb25483830f3ae0530e80da9d76a63963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1c976313d3c8655c45537a6583d680196e29562f27c16df71d2bbda75211c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1cd1ac5667cf41fb6937c55d958e08d4887dc13a5d1370a1c87c1b40d7a9fd3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c72b0d49fb7d0e26e24777d9d7a09570934a128ee074798787a71a010e115b2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddf8044acd5cad88da29b824fe9df5c41e8e5a465ae398fec3d29d975f8b56c(
    *,
    read_capacity_units: typing.Optional[jsii.Number] = None,
    throughput_mode: typing.Optional[builtins.str] = None,
    write_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744ca7c40de7dbca5ff62b3ff17123ff000c04df7d6dc74ac1864004d48975a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d90648d641ab56a46e0510b6051bcb844bd1bb13142e3e76d1b3e062feea548(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2d1efad787adc8c5d1a15b5ac79f95291e4ecd1ddc03223dd08558260edacd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c760518118a769de9ba697c7cb237c00326bb27538bde3c3f984165f752985e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679e71cb61881b4fc91fe8e363fb2b58435063fe4eb16c137648d8aa3f14fb13(
    value: typing.Optional[KeyspacesTableCapacitySpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe33f9ec5830fedcd854300405980e0955e913ed8a4371606d70ca5eb9ee086(
    *,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71acbb0068d7e7221c9d311e1290ab71b15a521f747ea095e2ed1a2abc54a40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90a717583e5084b7f8e6ef42c34c6994eb02f6043468eccc0b3fa2f15567cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d8202b5a67af5a4c619c541ca89c10949bcc85eb7bfd7930fec7d57e5ce496(
    value: typing.Optional[KeyspacesTableClientSideTimestamps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f809dd2e9bff4b75d9fa5c7d7ae7b4ca1bffa07f63826bfab55e9cadf5456930(
    *,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afeff1ae2508f0052254b85e665af22a411fc5d69119d818a5adbe8ef461f840(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34beec580c19a75dd2de2c5a7f8120de5402767961adba49ccbc5c868bfa937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e61bc4a479c49f8a5a727453c505aa87870dd646ec62f30210525479befecff(
    value: typing.Optional[KeyspacesTableComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff99caf1a35b1eab8e94a6307d83435e3498faa4f6b4952d482ceb389d51822d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    keyspace_name: builtins.str,
    schema_definition: typing.Union[KeyspacesTableSchemaDefinition, typing.Dict[builtins.str, typing.Any]],
    table_name: builtins.str,
    capacity_specification: typing.Optional[typing.Union[KeyspacesTableCapacitySpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    client_side_timestamps: typing.Optional[typing.Union[KeyspacesTableClientSideTimestamps, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[typing.Union[KeyspacesTableComment, typing.Dict[builtins.str, typing.Any]]] = None,
    default_time_to_live: typing.Optional[jsii.Number] = None,
    encryption_specification: typing.Optional[typing.Union[KeyspacesTableEncryptionSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    point_in_time_recovery: typing.Optional[typing.Union[KeyspacesTablePointInTimeRecovery, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KeyspacesTableTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[typing.Union[KeyspacesTableTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f35384c9ec41b19fc276b116da0c00381c734c0ae7df830100b8dd9e67cdc2(
    *,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f25c07b6f0d789396b11987d88548e310d0151c2b4a55524b2f060896e605c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab6b72a5c59e0fa89aa1b78f5638d9ce1935081e4ea113649816481c61e5dfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21deabbf9ceddc5f9143205a562b80c453a32e149fc0e3607856b3f8e1f2be2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4267d82da9b63292852485da132e496edef31defe38a27aa8f36f1553c7c4c2(
    value: typing.Optional[KeyspacesTableEncryptionSpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d353ba8c4baa6d3f68928dee706ddc7942d858feac3f583626026a55524f11(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbdfbdf299afdb090a090261ae6c965f9ac5c28680f6d0885df42934bbf6ff1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498c9eeb26556e02b96fe4bf67dbcbcb02a5cdc4aa0eb93bfb6e7127e05c96b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305ffa0c007b5d9a79e76014951b3913694ecfb7d04ec58a41223f3bf368f645(
    value: typing.Optional[KeyspacesTablePointInTimeRecovery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84f3e45946fa1468b7296dd672117e964d14e432f51c8207da557f92942cc95(
    *,
    column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionColumn, typing.Dict[builtins.str, typing.Any]]]],
    partition_key: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionPartitionKey, typing.Dict[builtins.str, typing.Any]]]],
    clustering_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionClusteringKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    static_column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionStaticColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27982153fbacd935c044eb63f87fbb4e96c3f3ca2dba0802afe72e0ed68463cf(
    *,
    name: builtins.str,
    order_by: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fa1d84e42f624d8630819a06da512855f3ea411d6c5df55af788cddf6609e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e38295606920461416f9a39f707920ee9ef84915f1e0cbc7e818b9ab4bc8532(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02e5ad00c8ed32f2d20168b656ae87ea178b9cf3e36006d7ee053773ea92aae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a67c9fab16baf2923d3ef826e4521c941bd853ec35f57f9aac5efee6aacaa8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad2a4fe86ad06b03ae7f3dfdb14e61fe3ce9f673e70c97f96f63ea32298adcb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627443ee7b541c3522376a2f8c5afac3bfdc3fc06ab568009f3e8a5cd7a6c1de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionClusteringKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecd21dc4f1956fdc5f029d83096ab7f8e8d962bf0c88313b3fc5791f13f7588(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d5de665fa74adfc0069c3233e0102045b41e95bd8aa6768d6e6cea843b0ffc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abde960c5af4ece7c32d1933281e486b2bdcdc03e5ada0dd896b1a91cb3dcdf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a6a3447d318fd15f43cd77b268531925a53c331d2c63da3929b1e39a5a6404(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionClusteringKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e73353cceba7fc98493113cedb4004ec31702a541f20b7c7e221e0c7c060504(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cffc048dd1e62c7c74a8cf0cad3d95e124557f2b6fd3daab0250362959cb30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91db7d72f5cea9cfe6b9c81eadcc87ac25d8b1c6f190c6d18726eb1c7390c41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec14eaaecc8d5c82d0e627b899627362d5bffea2e3cae7b352e66483a9459cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53356a420b41a045e63c3aa0ca36f9ae6830aad36fcdb26059bd5039a0acb9de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159317427cab47f2bc9c0fe2c37d94f491831fbe91a695683eab744322438403(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c28cbda99cce75b30338cf3ebb0caccd64c140bf01e3b3700f74bae3d9b483(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8d275aef3414ca1a2689b00289416a660059dc20ba126010c5b59c6866b9c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fd963d18888083ab364c6e2019f549bcae1584ffff936f49348669a525bd1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aee966024ca918cb5f294b320270d39986f0694b5eef4f0c0777bcc3dcab09a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6861ee8a96fbc3972b1d5a681723d84bb175d023340769d0923a4d67888dde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29e6f62b65d2d6849ac6043476e133b18ddb27456c50b266b873215ec27c011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1658f95075e3b13086599c9940c92928841f16f73d32fa23dfe29d31db5f3b2d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionClusteringKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af4ef0189777b527f00164ffbc7bebc7da660f193deb6420f279fb023809e9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf4d9b0c0637e5cbad8533d5dd4c55f4a09a232968088086620ec0f9bf56fac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionPartitionKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3f86c4ad0a6f30ab23732b35b7640237a7af26159c75cf7b6e112d2df89089(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KeyspacesTableSchemaDefinitionStaticColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac6265452e606d12a6b8d329d5c0a43ffdc5c84ab897faae101f0f15fed5be7(
    value: typing.Optional[KeyspacesTableSchemaDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5b1be3fa037bc79dd531c29bf077f24d999ce0b4f67e9e43b2b466d5ee4cd3(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a531a2acd914a3ad04f45f6fe13ad6361be1ef55333aafb7d5c72125c1f099c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa15c69321a209eced442f74dc2253f2df742fc80a57cd17f5b0f9c6f42514cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34a751f3a49da1b0d6c14089444145192a85b32867c539bae398192132f6541(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c917aa3057bfb9c4aab287c44386526409a4ccd7a6f4a6009e68fd5211457559(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f3d4132a7af4276f4b174134f27b244b40fafe5481bc5156d09fefdb4a5f78(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d724ec52aff075c9d18229a74b7c7ac3dd100c4b046199218067a82ccbcfddbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionPartitionKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fc224e205108877037ee4c56ffe14377dcbb64444fe3d1548249d10eb0ce5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b290b489eae3bbc0147c4bd8eb093bca571d8a371bde23f97423fe8f826370e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9dba4efb85fe8a7bdd209d7fd12218329a768455338360e90e43a9370dd36e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionPartitionKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308712ee5502986980f5df61d3a939798536b3e85eb37c92139cbf2baeb6152a(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6ddfc6485601fa787b804fc43393d02be74ba8960d1731b7325786443064a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb049d67740c772d73ca25ada7b261c4f61ac7d1a04dbf6b49037fdfbc74c7c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52ef153e8bd128afcf234ff641fa437a4d8eeb77533e49b08839c09d0614f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6494156315fa77f7eb6a22dd9277def5cbec5d9d7b2dce64fd700587ec264c7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2162fea7d4cba9534ec9030b813f7287a3a5821ce5e0775c63b5b1d9b8a3309(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947d66482cc3ffec7c9f63dca65bb82aa3c7082905f08c437012c8a1ba96ee8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KeyspacesTableSchemaDefinitionStaticColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073cfe199db1c8b3ed6f02f8de4b6028ff83d3776da03f822277037e1cf9df83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fe17320c360c7e61c703ebc05bdc09e37ec4cb2380e7f71bc689439ef495e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17380c78233549bb23941d8f5927a509ae8891bd830a8069518249302e501df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableSchemaDefinitionStaticColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff23861c63717cd4afa068e810b2c66f87985465919491dbd367cd22800753e2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9828091ab697981d5f3abc4328b0b654a06eb785dcab1120bdacd3093056756(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456902e2c66c1d92587ea98e3180547f10417791df4807911df78a57adb62284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3233fc9126ef9aa35cbe312f6c9c0b033371f76a4984b1ff2c7891b97ef71355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf64bc714587bbce566beaa4579fb578edf285ee3594cee186e9e8e16e3677f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7946e45b3f0c2cbc4c011a8c6da4ba7b15163aa885d6da74bb16742eeb8abf94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyspacesTableTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8859b555e0740ed0fbd684ca563fd3d3370ec41a6c5cfb9d2e7d6afb7b225bd5(
    *,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd54739252b7d1286a91efc7702d259e7044c7467adc5d2b89e5602aa3d24f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d9cb51ad854ed5f90584a9b448e7ae496ab4528eca66c14253f44dce66b018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5700bdd7e56958d3d0375934f9d263857d71fc7fbaa575b22a263873b565cd(
    value: typing.Optional[KeyspacesTableTtl],
) -> None:
    """Type checking stubs"""
    pass
