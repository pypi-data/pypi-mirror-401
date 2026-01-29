r'''
# `aws_kendra_index`

Refer to the Terraform Registry for docs: [`aws_kendra_index`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index).
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


class KendraIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index aws_kendra_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        capacity_units: typing.Optional[typing.Union["KendraIndexCapacityUnits", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraIndexDocumentMetadataConfigurationUpdates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union["KendraIndexServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_group_resolution_configuration: typing.Optional[typing.Union["KendraIndexUserGroupResolutionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        user_token_configurations: typing.Optional[typing.Union["KendraIndexUserTokenConfigurations", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index aws_kendra_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#name KendraIndex#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#role_arn KendraIndex#role_arn}.
        :param capacity_units: capacity_units block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#capacity_units KendraIndex#capacity_units}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#description KendraIndex#description}.
        :param document_metadata_configuration_updates: document_metadata_configuration_updates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#document_metadata_configuration_updates KendraIndex#document_metadata_configuration_updates}
        :param edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#edition KendraIndex#edition}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#id KendraIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#region KendraIndex#region}
        :param server_side_encryption_configuration: server_side_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#server_side_encryption_configuration KendraIndex#server_side_encryption_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#tags KendraIndex#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#tags_all KendraIndex#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#timeouts KendraIndex#timeouts}
        :param user_context_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_context_policy KendraIndex#user_context_policy}.
        :param user_group_resolution_configuration: user_group_resolution_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_group_resolution_configuration KendraIndex#user_group_resolution_configuration}
        :param user_token_configurations: user_token_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_token_configurations KendraIndex#user_token_configurations}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d57116481ba58231085cc41552c60c8d98f72c43aaf64a1d9062499f476960)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KendraIndexConfig(
            name=name,
            role_arn=role_arn,
            capacity_units=capacity_units,
            description=description,
            document_metadata_configuration_updates=document_metadata_configuration_updates,
            edition=edition,
            id=id,
            region=region,
            server_side_encryption_configuration=server_side_encryption_configuration,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            user_context_policy=user_context_policy,
            user_group_resolution_configuration=user_group_resolution_configuration,
            user_token_configurations=user_token_configurations,
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
        '''Generates CDKTF code for importing a KendraIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KendraIndex to import.
        :param import_from_id: The id of the existing KendraIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KendraIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4401ad0533d29987e406cda06b517f758a9a0893c46b7789307214714fa575)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapacityUnits")
    def put_capacity_units(
        self,
        *,
        query_capacity_units: typing.Optional[jsii.Number] = None,
        storage_capacity_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#query_capacity_units KendraIndex#query_capacity_units}.
        :param storage_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#storage_capacity_units KendraIndex#storage_capacity_units}.
        '''
        value = KendraIndexCapacityUnits(
            query_capacity_units=query_capacity_units,
            storage_capacity_units=storage_capacity_units,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityUnits", [value]))

    @jsii.member(jsii_name="putDocumentMetadataConfigurationUpdates")
    def put_document_metadata_configuration_updates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraIndexDocumentMetadataConfigurationUpdates", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1218b3ab47dcb61ae1a32e2373165c7801516519a4230606bd311425ac892f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDocumentMetadataConfigurationUpdates", [value]))

    @jsii.member(jsii_name="putServerSideEncryptionConfiguration")
    def put_server_side_encryption_configuration(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#kms_key_id KendraIndex#kms_key_id}.
        '''
        value = KendraIndexServerSideEncryptionConfiguration(kms_key_id=kms_key_id)

        return typing.cast(None, jsii.invoke(self, "putServerSideEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#create KendraIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#delete KendraIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#update KendraIndex#update}.
        '''
        value = KendraIndexTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserGroupResolutionConfiguration")
    def put_user_group_resolution_configuration(
        self,
        *,
        user_group_resolution_mode: builtins.str,
    ) -> None:
        '''
        :param user_group_resolution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_group_resolution_mode KendraIndex#user_group_resolution_mode}.
        '''
        value = KendraIndexUserGroupResolutionConfiguration(
            user_group_resolution_mode=user_group_resolution_mode
        )

        return typing.cast(None, jsii.invoke(self, "putUserGroupResolutionConfiguration", [value]))

    @jsii.member(jsii_name="putUserTokenConfigurations")
    def put_user_token_configurations(
        self,
        *,
        json_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param json_token_type_configuration: json_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#json_token_type_configuration KendraIndex#json_token_type_configuration}
        :param jwt_token_type_configuration: jwt_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#jwt_token_type_configuration KendraIndex#jwt_token_type_configuration}
        '''
        value = KendraIndexUserTokenConfigurations(
            json_token_type_configuration=json_token_type_configuration,
            jwt_token_type_configuration=jwt_token_type_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putUserTokenConfigurations", [value]))

    @jsii.member(jsii_name="resetCapacityUnits")
    def reset_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityUnits", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentMetadataConfigurationUpdates")
    def reset_document_metadata_configuration_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentMetadataConfigurationUpdates", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServerSideEncryptionConfiguration")
    def reset_server_side_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserContextPolicy")
    def reset_user_context_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserContextPolicy", []))

    @jsii.member(jsii_name="resetUserGroupResolutionConfiguration")
    def reset_user_group_resolution_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserGroupResolutionConfiguration", []))

    @jsii.member(jsii_name="resetUserTokenConfigurations")
    def reset_user_token_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTokenConfigurations", []))

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
    @jsii.member(jsii_name="capacityUnits")
    def capacity_units(self) -> "KendraIndexCapacityUnitsOutputReference":
        return typing.cast("KendraIndexCapacityUnitsOutputReference", jsii.get(self, "capacityUnits"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="documentMetadataConfigurationUpdates")
    def document_metadata_configuration_updates(
        self,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesList":
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesList", jsii.get(self, "documentMetadataConfigurationUpdates"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="indexStatistics")
    def index_statistics(self) -> "KendraIndexIndexStatisticsList":
        return typing.cast("KendraIndexIndexStatisticsList", jsii.get(self, "indexStatistics"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> "KendraIndexServerSideEncryptionConfigurationOutputReference":
        return typing.cast("KendraIndexServerSideEncryptionConfigurationOutputReference", jsii.get(self, "serverSideEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KendraIndexTimeoutsOutputReference":
        return typing.cast("KendraIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionConfiguration")
    def user_group_resolution_configuration(
        self,
    ) -> "KendraIndexUserGroupResolutionConfigurationOutputReference":
        return typing.cast("KendraIndexUserGroupResolutionConfigurationOutputReference", jsii.get(self, "userGroupResolutionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="userTokenConfigurations")
    def user_token_configurations(
        self,
    ) -> "KendraIndexUserTokenConfigurationsOutputReference":
        return typing.cast("KendraIndexUserTokenConfigurationsOutputReference", jsii.get(self, "userTokenConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="capacityUnitsInput")
    def capacity_units_input(self) -> typing.Optional["KendraIndexCapacityUnits"]:
        return typing.cast(typing.Optional["KendraIndexCapacityUnits"], jsii.get(self, "capacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="documentMetadataConfigurationUpdatesInput")
    def document_metadata_configuration_updates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]], jsii.get(self, "documentMetadataConfigurationUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfigurationInput")
    def server_side_encryption_configuration_input(
        self,
    ) -> typing.Optional["KendraIndexServerSideEncryptionConfiguration"]:
        return typing.cast(typing.Optional["KendraIndexServerSideEncryptionConfiguration"], jsii.get(self, "serverSideEncryptionConfigurationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userContextPolicyInput")
    def user_context_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userContextPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionConfigurationInput")
    def user_group_resolution_configuration_input(
        self,
    ) -> typing.Optional["KendraIndexUserGroupResolutionConfiguration"]:
        return typing.cast(typing.Optional["KendraIndexUserGroupResolutionConfiguration"], jsii.get(self, "userGroupResolutionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenConfigurationsInput")
    def user_token_configurations_input(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurations"]:
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurations"], jsii.get(self, "userTokenConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3f67880f410590622a2e1b9ab98fab4912657a5f58d5f9390bc723429d12a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9b6f03ae6ffa4c21f3a23c9bb65373aabde2e5fca44a1dc28f9391cbd82d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018d2626baa4dac2fff43ae21a0e0007f8d800bc4662d471712631ba89c0f043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f516a4f1b6dcae9feb661dcd43994b2334c3bb4d57d7458d361ee3ed8faa0d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de358ff2f2a24a221ef4f9d64ff43ffb16b21ed8b970a21793879b5ee5969adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5a32e7a065b3ce4031ff1e8201b7b35fcc82aaea071cb50e32cfd24dbd8398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41811b7c6672150f1462059dbaa33b79f3134e9330632d43ab34dd716367384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41063dee5a8da294c445e31b6375d9c40e9755f093b03f59dc4e333371d52b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userContextPolicy")
    def user_context_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userContextPolicy"))

    @user_context_policy.setter
    def user_context_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea25d3f7931827609cf9cc69f65ac3476faf946c6a231a7c0a2d8c923c86fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userContextPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexCapacityUnits",
    jsii_struct_bases=[],
    name_mapping={
        "query_capacity_units": "queryCapacityUnits",
        "storage_capacity_units": "storageCapacityUnits",
    },
)
class KendraIndexCapacityUnits:
    def __init__(
        self,
        *,
        query_capacity_units: typing.Optional[jsii.Number] = None,
        storage_capacity_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#query_capacity_units KendraIndex#query_capacity_units}.
        :param storage_capacity_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#storage_capacity_units KendraIndex#storage_capacity_units}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aebe77d931230c1dde252f3610df25d35476cce382b12ffcb6dee6f0426331b)
            check_type(argname="argument query_capacity_units", value=query_capacity_units, expected_type=type_hints["query_capacity_units"])
            check_type(argname="argument storage_capacity_units", value=storage_capacity_units, expected_type=type_hints["storage_capacity_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_capacity_units is not None:
            self._values["query_capacity_units"] = query_capacity_units
        if storage_capacity_units is not None:
            self._values["storage_capacity_units"] = storage_capacity_units

    @builtins.property
    def query_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#query_capacity_units KendraIndex#query_capacity_units}.'''
        result = self._values.get("query_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_capacity_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#storage_capacity_units KendraIndex#storage_capacity_units}.'''
        result = self._values.get("storage_capacity_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexCapacityUnits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexCapacityUnitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexCapacityUnitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86f0aa73b9e8527c07a11cd4821f8bb426c44c8b5fea3eb7d6d004956fa82130)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueryCapacityUnits")
    def reset_query_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryCapacityUnits", []))

    @jsii.member(jsii_name="resetStorageCapacityUnits")
    def reset_storage_capacity_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageCapacityUnits", []))

    @builtins.property
    @jsii.member(jsii_name="queryCapacityUnitsInput")
    def query_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageCapacityUnitsInput")
    def storage_capacity_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageCapacityUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryCapacityUnits")
    def query_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryCapacityUnits"))

    @query_capacity_units.setter
    def query_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27a78818e0b721fa46617467d7cdfd87229d1a5ef4476e3e03c13d98c7b2e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageCapacityUnits")
    def storage_capacity_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageCapacityUnits"))

    @storage_capacity_units.setter
    def storage_capacity_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53842234c9bcfa9ca3b317938df074aea176e0640629bcf6f955573af899e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCapacityUnits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraIndexCapacityUnits]:
        return typing.cast(typing.Optional[KendraIndexCapacityUnits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KendraIndexCapacityUnits]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4005f9508adc8d97e71a5a626fd3159dbae8baed0e7b398840cf2c354f44bc73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "role_arn": "roleArn",
        "capacity_units": "capacityUnits",
        "description": "description",
        "document_metadata_configuration_updates": "documentMetadataConfigurationUpdates",
        "edition": "edition",
        "id": "id",
        "region": "region",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "user_context_policy": "userContextPolicy",
        "user_group_resolution_configuration": "userGroupResolutionConfiguration",
        "user_token_configurations": "userTokenConfigurations",
    },
)
class KendraIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        role_arn: builtins.str,
        capacity_units: typing.Optional[typing.Union[KendraIndexCapacityUnits, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraIndexDocumentMetadataConfigurationUpdates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union["KendraIndexServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_group_resolution_configuration: typing.Optional[typing.Union["KendraIndexUserGroupResolutionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        user_token_configurations: typing.Optional[typing.Union["KendraIndexUserTokenConfigurations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#name KendraIndex#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#role_arn KendraIndex#role_arn}.
        :param capacity_units: capacity_units block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#capacity_units KendraIndex#capacity_units}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#description KendraIndex#description}.
        :param document_metadata_configuration_updates: document_metadata_configuration_updates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#document_metadata_configuration_updates KendraIndex#document_metadata_configuration_updates}
        :param edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#edition KendraIndex#edition}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#id KendraIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#region KendraIndex#region}
        :param server_side_encryption_configuration: server_side_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#server_side_encryption_configuration KendraIndex#server_side_encryption_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#tags KendraIndex#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#tags_all KendraIndex#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#timeouts KendraIndex#timeouts}
        :param user_context_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_context_policy KendraIndex#user_context_policy}.
        :param user_group_resolution_configuration: user_group_resolution_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_group_resolution_configuration KendraIndex#user_group_resolution_configuration}
        :param user_token_configurations: user_token_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_token_configurations KendraIndex#user_token_configurations}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity_units, dict):
            capacity_units = KendraIndexCapacityUnits(**capacity_units)
        if isinstance(server_side_encryption_configuration, dict):
            server_side_encryption_configuration = KendraIndexServerSideEncryptionConfiguration(**server_side_encryption_configuration)
        if isinstance(timeouts, dict):
            timeouts = KendraIndexTimeouts(**timeouts)
        if isinstance(user_group_resolution_configuration, dict):
            user_group_resolution_configuration = KendraIndexUserGroupResolutionConfiguration(**user_group_resolution_configuration)
        if isinstance(user_token_configurations, dict):
            user_token_configurations = KendraIndexUserTokenConfigurations(**user_token_configurations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf0e545de7b71f4936d74a6a78b7615f60f35998c8d2f6384579cc6b74ea6dd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument capacity_units", value=capacity_units, expected_type=type_hints["capacity_units"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document_metadata_configuration_updates", value=document_metadata_configuration_updates, expected_type=type_hints["document_metadata_configuration_updates"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_context_policy", value=user_context_policy, expected_type=type_hints["user_context_policy"])
            check_type(argname="argument user_group_resolution_configuration", value=user_group_resolution_configuration, expected_type=type_hints["user_group_resolution_configuration"])
            check_type(argname="argument user_token_configurations", value=user_token_configurations, expected_type=type_hints["user_token_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if capacity_units is not None:
            self._values["capacity_units"] = capacity_units
        if description is not None:
            self._values["description"] = description
        if document_metadata_configuration_updates is not None:
            self._values["document_metadata_configuration_updates"] = document_metadata_configuration_updates
        if edition is not None:
            self._values["edition"] = edition
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_context_policy is not None:
            self._values["user_context_policy"] = user_context_policy
        if user_group_resolution_configuration is not None:
            self._values["user_group_resolution_configuration"] = user_group_resolution_configuration
        if user_token_configurations is not None:
            self._values["user_token_configurations"] = user_token_configurations

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#name KendraIndex#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#role_arn KendraIndex#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_units(self) -> typing.Optional[KendraIndexCapacityUnits]:
        '''capacity_units block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#capacity_units KendraIndex#capacity_units}
        '''
        result = self._values.get("capacity_units")
        return typing.cast(typing.Optional[KendraIndexCapacityUnits], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#description KendraIndex#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_metadata_configuration_updates(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]]:
        '''document_metadata_configuration_updates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#document_metadata_configuration_updates KendraIndex#document_metadata_configuration_updates}
        '''
        result = self._values.get("document_metadata_configuration_updates")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraIndexDocumentMetadataConfigurationUpdates"]]], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#edition KendraIndex#edition}.'''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#id KendraIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#region KendraIndex#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional["KendraIndexServerSideEncryptionConfiguration"]:
        '''server_side_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#server_side_encryption_configuration KendraIndex#server_side_encryption_configuration}
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional["KendraIndexServerSideEncryptionConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#tags KendraIndex#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#tags_all KendraIndex#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KendraIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#timeouts KendraIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KendraIndexTimeouts"], result)

    @builtins.property
    def user_context_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_context_policy KendraIndex#user_context_policy}.'''
        result = self._values.get("user_context_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_group_resolution_configuration(
        self,
    ) -> typing.Optional["KendraIndexUserGroupResolutionConfiguration"]:
        '''user_group_resolution_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_group_resolution_configuration KendraIndex#user_group_resolution_configuration}
        '''
        result = self._values.get("user_group_resolution_configuration")
        return typing.cast(typing.Optional["KendraIndexUserGroupResolutionConfiguration"], result)

    @builtins.property
    def user_token_configurations(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurations"]:
        '''user_token_configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_token_configurations KendraIndex#user_token_configurations}
        '''
        result = self._values.get("user_token_configurations")
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdates",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "relevance": "relevance",
        "search": "search",
    },
)
class KendraIndexDocumentMetadataConfigurationUpdates:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        relevance: typing.Optional[typing.Union["KendraIndexDocumentMetadataConfigurationUpdatesRelevance", typing.Dict[builtins.str, typing.Any]]] = None,
        search: typing.Optional[typing.Union["KendraIndexDocumentMetadataConfigurationUpdatesSearch", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#name KendraIndex#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#type KendraIndex#type}.
        :param relevance: relevance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#relevance KendraIndex#relevance}
        :param search: search block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#search KendraIndex#search}
        '''
        if isinstance(relevance, dict):
            relevance = KendraIndexDocumentMetadataConfigurationUpdatesRelevance(**relevance)
        if isinstance(search, dict):
            search = KendraIndexDocumentMetadataConfigurationUpdatesSearch(**search)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e73cab1efd63ff495c144cd86c39c8854c7c773000cc1370ad5005711fc10dc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument relevance", value=relevance, expected_type=type_hints["relevance"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if relevance is not None:
            self._values["relevance"] = relevance
        if search is not None:
            self._values["search"] = search

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#name KendraIndex#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#type KendraIndex#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relevance(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"]:
        '''relevance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#relevance KendraIndex#relevance}
        '''
        result = self._values.get("relevance")
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"], result)

    @builtins.property
    def search(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"]:
        '''search block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#search KendraIndex#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexDocumentMetadataConfigurationUpdates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexDocumentMetadataConfigurationUpdatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd743057fd57e27de111e6417a6f535eaf68a8734bfe808c1587323480799577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1a20f7d053ea8a8b924eacf1af65267684f1dd7e10ec0079495303e8faaac0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b426ab1902e4f7d2db0d720fa39d3ca1ff9317d40b6d4a9fda63e7f29ca6063a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33643460fbd666c3ef7327832e2f59283fa2c457a9adc944abeed895b58835a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ee8641968c42581aa0c9d6ae5a828209508ccddaebac3382df3c5c0ee3fd04e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f89a127da8dbbca4b5b54014c2a5e272c94911910573c0f173f82a39ecad4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraIndexDocumentMetadataConfigurationUpdatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1959ecc0fbf18677fefaa8673e051df1f06fcf9290522cfaa5ffbed26ec4666)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRelevance")
    def put_relevance(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        freshness: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        importance: typing.Optional[jsii.Number] = None,
        rank_order: typing.Optional[builtins.str] = None,
        values_importance_map: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#duration KendraIndex#duration}.
        :param freshness: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#freshness KendraIndex#freshness}.
        :param importance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#importance KendraIndex#importance}.
        :param rank_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#rank_order KendraIndex#rank_order}.
        :param values_importance_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#values_importance_map KendraIndex#values_importance_map}.
        '''
        value = KendraIndexDocumentMetadataConfigurationUpdatesRelevance(
            duration=duration,
            freshness=freshness,
            importance=importance,
            rank_order=rank_order,
            values_importance_map=values_importance_map,
        )

        return typing.cast(None, jsii.invoke(self, "putRelevance", [value]))

    @jsii.member(jsii_name="putSearch")
    def put_search(
        self,
        *,
        displayable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        facetable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sortable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param displayable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#displayable KendraIndex#displayable}.
        :param facetable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#facetable KendraIndex#facetable}.
        :param searchable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#searchable KendraIndex#searchable}.
        :param sortable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#sortable KendraIndex#sortable}.
        '''
        value = KendraIndexDocumentMetadataConfigurationUpdatesSearch(
            displayable=displayable,
            facetable=facetable,
            searchable=searchable,
            sortable=sortable,
        )

        return typing.cast(None, jsii.invoke(self, "putSearch", [value]))

    @jsii.member(jsii_name="resetRelevance")
    def reset_relevance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelevance", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @builtins.property
    @jsii.member(jsii_name="relevance")
    def relevance(
        self,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference":
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference", jsii.get(self, "relevance"))

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(
        self,
    ) -> "KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference":
        return typing.cast("KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference", jsii.get(self, "search"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="relevanceInput")
    def relevance_input(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"]:
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesRelevance"], jsii.get(self, "relevanceInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(
        self,
    ) -> typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"]:
        return typing.cast(typing.Optional["KendraIndexDocumentMetadataConfigurationUpdatesSearch"], jsii.get(self, "searchInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__db1d4a8cd9ad08a43c1d315fbddc0585eede5f2440425aa292712febcbdd75ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5371595a1067528bdfe3c84473c61683d2a211c3f4b5a4e3e0d10de5d91fea0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d88cc68bf3760bc868b957c426dc2b53bf886d4b6d9814899433c24a222258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesRelevance",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "freshness": "freshness",
        "importance": "importance",
        "rank_order": "rankOrder",
        "values_importance_map": "valuesImportanceMap",
    },
)
class KendraIndexDocumentMetadataConfigurationUpdatesRelevance:
    def __init__(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        freshness: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        importance: typing.Optional[jsii.Number] = None,
        rank_order: typing.Optional[builtins.str] = None,
        values_importance_map: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#duration KendraIndex#duration}.
        :param freshness: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#freshness KendraIndex#freshness}.
        :param importance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#importance KendraIndex#importance}.
        :param rank_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#rank_order KendraIndex#rank_order}.
        :param values_importance_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#values_importance_map KendraIndex#values_importance_map}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1450eca4b48d9f2801a75bb9d00405e0241df714452dc326ff669fed4b91340d)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument freshness", value=freshness, expected_type=type_hints["freshness"])
            check_type(argname="argument importance", value=importance, expected_type=type_hints["importance"])
            check_type(argname="argument rank_order", value=rank_order, expected_type=type_hints["rank_order"])
            check_type(argname="argument values_importance_map", value=values_importance_map, expected_type=type_hints["values_importance_map"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if freshness is not None:
            self._values["freshness"] = freshness
        if importance is not None:
            self._values["importance"] = importance
        if rank_order is not None:
            self._values["rank_order"] = rank_order
        if values_importance_map is not None:
            self._values["values_importance_map"] = values_importance_map

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#duration KendraIndex#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def freshness(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#freshness KendraIndex#freshness}.'''
        result = self._values.get("freshness")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def importance(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#importance KendraIndex#importance}.'''
        result = self._values.get("importance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rank_order(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#rank_order KendraIndex#rank_order}.'''
        result = self._values.get("rank_order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values_importance_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#values_importance_map KendraIndex#values_importance_map}.'''
        result = self._values.get("values_importance_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexDocumentMetadataConfigurationUpdatesRelevance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd07d47cae512548f579151fc1ba1d7e8614de6543aa11c0719504ba80637d78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetFreshness")
    def reset_freshness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFreshness", []))

    @jsii.member(jsii_name="resetImportance")
    def reset_importance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportance", []))

    @jsii.member(jsii_name="resetRankOrder")
    def reset_rank_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRankOrder", []))

    @jsii.member(jsii_name="resetValuesImportanceMap")
    def reset_values_importance_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValuesImportanceMap", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="freshnessInput")
    def freshness_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "freshnessInput"))

    @builtins.property
    @jsii.member(jsii_name="importanceInput")
    def importance_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "importanceInput"))

    @builtins.property
    @jsii.member(jsii_name="rankOrderInput")
    def rank_order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rankOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesImportanceMapInput")
    def values_importance_map_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "valuesImportanceMapInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7e20a69ec7dd274188dddf5163703d9e56e64b8317ce35d419debb58a7dca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="freshness")
    def freshness(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "freshness"))

    @freshness.setter
    def freshness(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c448069691424f6a2a62b2a43b790f5f95bb1359329d11a77c279f4e118c85b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "freshness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importance")
    def importance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "importance"))

    @importance.setter
    def importance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670485c5aea547061d5166ebf7e7d1a39a82c5afeef994a5c42efdf3a82b947c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rankOrder")
    def rank_order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rankOrder"))

    @rank_order.setter
    def rank_order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f946cdac005a3eddf1445703273dbe11be6b9b328159f14ae1399d47d584abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rankOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valuesImportanceMap")
    def values_importance_map(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "valuesImportanceMap"))

    @values_importance_map.setter
    def values_importance_map(
        self,
        value: typing.Mapping[builtins.str, jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f124ce0e379138382acbf2e4142e18a7d284c80a6b2552a537792bc395c32c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valuesImportanceMap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance]:
        return typing.cast(typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5bfbd91a3121c0fa683ef1926a4a8bb454fb165d2c64dab45b39db3b0e3342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesSearch",
    jsii_struct_bases=[],
    name_mapping={
        "displayable": "displayable",
        "facetable": "facetable",
        "searchable": "searchable",
        "sortable": "sortable",
    },
)
class KendraIndexDocumentMetadataConfigurationUpdatesSearch:
    def __init__(
        self,
        *,
        displayable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        facetable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sortable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param displayable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#displayable KendraIndex#displayable}.
        :param facetable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#facetable KendraIndex#facetable}.
        :param searchable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#searchable KendraIndex#searchable}.
        :param sortable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#sortable KendraIndex#sortable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38550c6c89adbc9bfdd118850eac19deb62d401eeabacfbe545da3432fcf9d72)
            check_type(argname="argument displayable", value=displayable, expected_type=type_hints["displayable"])
            check_type(argname="argument facetable", value=facetable, expected_type=type_hints["facetable"])
            check_type(argname="argument searchable", value=searchable, expected_type=type_hints["searchable"])
            check_type(argname="argument sortable", value=sortable, expected_type=type_hints["sortable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if displayable is not None:
            self._values["displayable"] = displayable
        if facetable is not None:
            self._values["facetable"] = facetable
        if searchable is not None:
            self._values["searchable"] = searchable
        if sortable is not None:
            self._values["sortable"] = sortable

    @builtins.property
    def displayable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#displayable KendraIndex#displayable}.'''
        result = self._values.get("displayable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def facetable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#facetable KendraIndex#facetable}.'''
        result = self._values.get("facetable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def searchable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#searchable KendraIndex#searchable}.'''
        result = self._values.get("searchable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sortable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#sortable KendraIndex#sortable}.'''
        result = self._values.get("sortable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexDocumentMetadataConfigurationUpdatesSearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59f71e00687937c9a829879a7669cf8468783c4b4796fa0831dca4dd0986e088)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayable")
    def reset_displayable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayable", []))

    @jsii.member(jsii_name="resetFacetable")
    def reset_facetable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFacetable", []))

    @jsii.member(jsii_name="resetSearchable")
    def reset_searchable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchable", []))

    @jsii.member(jsii_name="resetSortable")
    def reset_sortable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortable", []))

    @builtins.property
    @jsii.member(jsii_name="displayableInput")
    def displayable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "displayableInput"))

    @builtins.property
    @jsii.member(jsii_name="facetableInput")
    def facetable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "facetableInput"))

    @builtins.property
    @jsii.member(jsii_name="searchableInput")
    def searchable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "searchableInput"))

    @builtins.property
    @jsii.member(jsii_name="sortableInput")
    def sortable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sortableInput"))

    @builtins.property
    @jsii.member(jsii_name="displayable")
    def displayable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "displayable"))

    @displayable.setter
    def displayable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba4cc85e7699812ba55ba3106e27ef8777bc9293826647600686d803224f361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="facetable")
    def facetable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "facetable"))

    @facetable.setter
    def facetable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b4f0c8c30eb8221f94364c5d43507dc14ccb67d70534ccd80de7b07cf4899a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "facetable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchable")
    def searchable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "searchable"))

    @searchable.setter
    def searchable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424775d881ff5eda81ee2318d50f02b3f51e8e89e31f81414b5e079453302f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortable")
    def sortable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sortable"))

    @sortable.setter
    def sortable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b7bf46febcfbecf9863ab32dc87aeaacfc6be31641c0853c6cee0bfad31b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch]:
        return typing.cast(typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84789c27e852a5bb4bb8ce936602a821b4e03116aef7ba19f99641293855eedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatistics",
    jsii_struct_bases=[],
    name_mapping={},
)
class KendraIndexIndexStatistics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexIndexStatistics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsFaqStatistics",
    jsii_struct_bases=[],
    name_mapping={},
)
class KendraIndexIndexStatisticsFaqStatistics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexIndexStatisticsFaqStatistics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexIndexStatisticsFaqStatisticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsFaqStatisticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__484f80e39c59da8c24bce8235d4e3678177d47e01a1fa15b9f76bd167b9cf2a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraIndexIndexStatisticsFaqStatisticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a867bbcaa908aaf2994f740ac4581f26a0e82f19680697ece2fe974519eb2a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexIndexStatisticsFaqStatisticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2bcb262952410be9d18de9433b15f4682ec2049d979f24fe952a25b75c38b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94cbc34e4bdd0cdc033fd0ad34f21efc44a60d153725f972cb8279a635eb8d24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03e832e3742936445654ecb6931caaf8558a4e097e505820a017bee9006bbb7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsFaqStatisticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsFaqStatisticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1645fcbec20bde5b999ac7b135e772837d776d1ec94c85f2082cd49dae756da4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="indexedQuestionAnswersCount")
    def indexed_question_answers_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indexedQuestionAnswersCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexIndexStatisticsFaqStatistics]:
        return typing.cast(typing.Optional[KendraIndexIndexStatisticsFaqStatistics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexIndexStatisticsFaqStatistics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652b5e49f8b3fecbc41c720941e53ba55d2e391f518d04a9238fdde02ad71ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99c13f08e48b7f590ba5e734f9a684a08d14b9c5c92e5106bb4c0166758092b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "KendraIndexIndexStatisticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80c82294e84de435603f5482c1594fa87182892de461abf887692c12a4843dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexIndexStatisticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb2b3f12badbf2f48b9fc04920ef77ede635a7af7130481cada36905dde0518)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c567e29be5482df43ae3718da67485d92065217608386f319742f62b83f769d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__498662b871e07f0abafa82f5721cae08435a3d320675663bd826d59da5cc28af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af240bd2891e31451fc55411e91fea5bf69acfb151af95f9ac3ce393fe302c54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="faqStatistics")
    def faq_statistics(self) -> KendraIndexIndexStatisticsFaqStatisticsList:
        return typing.cast(KendraIndexIndexStatisticsFaqStatisticsList, jsii.get(self, "faqStatistics"))

    @builtins.property
    @jsii.member(jsii_name="textDocumentStatistics")
    def text_document_statistics(
        self,
    ) -> "KendraIndexIndexStatisticsTextDocumentStatisticsList":
        return typing.cast("KendraIndexIndexStatisticsTextDocumentStatisticsList", jsii.get(self, "textDocumentStatistics"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraIndexIndexStatistics]:
        return typing.cast(typing.Optional[KendraIndexIndexStatistics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexIndexStatistics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85521ae0fa7059c9d42e78079e92ebdb9ba308b95809321bae684702ca8cb7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsTextDocumentStatistics",
    jsii_struct_bases=[],
    name_mapping={},
)
class KendraIndexIndexStatisticsTextDocumentStatistics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexIndexStatisticsTextDocumentStatistics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexIndexStatisticsTextDocumentStatisticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsTextDocumentStatisticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5e6f7e5c1f59cf33c553de54e29f745eaa244c14d8856efe92414807f8917e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253e940d4c463127b17286b23918f2bddc24ff9acbe2f2e1315501168cf09979)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6d3c53108a7bb855a7fa573e679bc323627e5c0e00ae9f40beecad274b53e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c65b28df1fdbd15342abbb521bba1eb537142f1eafa1351d91cf39f475ce62d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d0f247d8a7bd5eb5f5857977c719981afe4b1c88eea0fe12391fe2354cd211e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__feb1ace206e6ba2ac348e2c13f99161ef507b7f9a6825b0aa60518f8f72f4a46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="indexedTextBytes")
    def indexed_text_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indexedTextBytes"))

    @builtins.property
    @jsii.member(jsii_name="indexedTextDocumentsCount")
    def indexed_text_documents_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indexedTextDocumentsCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics]:
        return typing.cast(typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02d998a28242ace0bd488a25caad14964f17faf1b64980952bf353b4589c94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexServerSideEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_id": "kmsKeyId"},
)
class KendraIndexServerSideEncryptionConfiguration:
    def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#kms_key_id KendraIndex#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80198e3075e616dc7e4d660de8772d5ea67e3d263149089642d4d383505cb974)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#kms_key_id KendraIndex#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexServerSideEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexServerSideEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexServerSideEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc075b3967640c2808be74856180d354a5c874381483571a40e89ad7946be05e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8289658d2ef6855f119c5c7b601d4cb8a76ab0938fa8e66702a2e5e4753b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexServerSideEncryptionConfiguration]:
        return typing.cast(typing.Optional[KendraIndexServerSideEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexServerSideEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08826c5962a1c24efeab2d372b9e63a2ce8976471fe437d7d8e6ead155fcdd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KendraIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#create KendraIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#delete KendraIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#update KendraIndex#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21cf4cd758a65bfcb3eb55c2b88a74a9b904d3b790fec8b4025a025542dc834)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#create KendraIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#delete KendraIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#update KendraIndex#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2755eb7f5db573fe5bd5e3b2b7f25c30dd2a4ae67b245ca54a9f5a96d1513258)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49eb844aadda76fd571de0e4b75cd0deb8de645ff0d14f2c59e8c67ac2822757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6b95b678504d608f858f5bc05532a3a9a09a5537407d33cac615e7692d6c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c34245a7acef24affd800ee99964b26b538ac5321fbbacc993416c7d7332d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241e6ac8eef8fcff3a6d11e744b195bb8fc4d8ebaafdcefe4adc565ebdc54d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserGroupResolutionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"user_group_resolution_mode": "userGroupResolutionMode"},
)
class KendraIndexUserGroupResolutionConfiguration:
    def __init__(self, *, user_group_resolution_mode: builtins.str) -> None:
        '''
        :param user_group_resolution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_group_resolution_mode KendraIndex#user_group_resolution_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c8e0400aa01e18ad3118f2ff865b13ea8eef6b2fd90b7de7a60e2e99baefaf)
            check_type(argname="argument user_group_resolution_mode", value=user_group_resolution_mode, expected_type=type_hints["user_group_resolution_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_group_resolution_mode": user_group_resolution_mode,
        }

    @builtins.property
    def user_group_resolution_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_group_resolution_mode KendraIndex#user_group_resolution_mode}.'''
        result = self._values.get("user_group_resolution_mode")
        assert result is not None, "Required property 'user_group_resolution_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserGroupResolutionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexUserGroupResolutionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserGroupResolutionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54ee4a06bfc0c614a57c5b40c2307c2967f3b05d14c0101489ad10568ee8616e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionModeInput")
    def user_group_resolution_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userGroupResolutionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="userGroupResolutionMode")
    def user_group_resolution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userGroupResolutionMode"))

    @user_group_resolution_mode.setter
    def user_group_resolution_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6527a835512ec2cc6c4afaca827b7f6e60ea0155b96113a3d124bf81921ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroupResolutionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexUserGroupResolutionConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserGroupResolutionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserGroupResolutionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86171d84c86c09d4f7158643668e6d6a40892d2b978fad751a7bf8c5608c816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserTokenConfigurations",
    jsii_struct_bases=[],
    name_mapping={
        "json_token_type_configuration": "jsonTokenTypeConfiguration",
        "jwt_token_type_configuration": "jwtTokenTypeConfiguration",
    },
)
class KendraIndexUserTokenConfigurations:
    def __init__(
        self,
        *,
        json_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_token_type_configuration: typing.Optional[typing.Union["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param json_token_type_configuration: json_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#json_token_type_configuration KendraIndex#json_token_type_configuration}
        :param jwt_token_type_configuration: jwt_token_type_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#jwt_token_type_configuration KendraIndex#jwt_token_type_configuration}
        '''
        if isinstance(json_token_type_configuration, dict):
            json_token_type_configuration = KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration(**json_token_type_configuration)
        if isinstance(jwt_token_type_configuration, dict):
            jwt_token_type_configuration = KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration(**jwt_token_type_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767ff9b0726061e8d966848f1ab59451993b8e1e509c5539feede918a9195e1d)
            check_type(argname="argument json_token_type_configuration", value=json_token_type_configuration, expected_type=type_hints["json_token_type_configuration"])
            check_type(argname="argument jwt_token_type_configuration", value=jwt_token_type_configuration, expected_type=type_hints["jwt_token_type_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if json_token_type_configuration is not None:
            self._values["json_token_type_configuration"] = json_token_type_configuration
        if jwt_token_type_configuration is not None:
            self._values["jwt_token_type_configuration"] = jwt_token_type_configuration

    @builtins.property
    def json_token_type_configuration(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration"]:
        '''json_token_type_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#json_token_type_configuration KendraIndex#json_token_type_configuration}
        '''
        result = self._values.get("json_token_type_configuration")
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration"], result)

    @builtins.property
    def jwt_token_type_configuration(
        self,
    ) -> typing.Optional["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration"]:
        '''jwt_token_type_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#jwt_token_type_configuration KendraIndex#jwt_token_type_configuration}
        '''
        result = self._values.get("jwt_token_type_configuration")
        return typing.cast(typing.Optional["KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserTokenConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "group_attribute_field": "groupAttributeField",
        "user_name_attribute_field": "userNameAttributeField",
    },
)
class KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration:
    def __init__(
        self,
        *,
        group_attribute_field: builtins.str,
        user_name_attribute_field: builtins.str,
    ) -> None:
        '''
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba0a6c2d827b3a5638efe631bc3b6593d409b99ab7e8a927328a4448de4984e)
            check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
            check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_attribute_field": group_attribute_field,
            "user_name_attribute_field": user_name_attribute_field,
        }

    @builtins.property
    def group_attribute_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.'''
        result = self._values.get("group_attribute_field")
        assert result is not None, "Required property 'group_attribute_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name_attribute_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.'''
        result = self._values.get("user_name_attribute_field")
        assert result is not None, "Required property 'user_name_attribute_field' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__699d6498196f766619b55e97b9879d89d5346176e0c921214a6ad2226d184e98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="groupAttributeFieldInput")
    def group_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeFieldInput")
    def user_name_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAttributeField")
    def group_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupAttributeField"))

    @group_attribute_field.setter
    def group_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f316a41d1d8cf97f173c43ac489b6d56ff8abb9f12b9810bfd972dc3f8d6d820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeField")
    def user_name_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameAttributeField"))

    @user_name_attribute_field.setter
    def user_name_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5b7dba3a47e2da28ac0098a287fa2966ea8d276c1253f08dfefd4527077815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee1e07bfd3d9018d02e4c08a04fc99b87cd753edbbe4fafecfd8dc8b0778b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "key_location": "keyLocation",
        "claim_regex": "claimRegex",
        "group_attribute_field": "groupAttributeField",
        "issuer": "issuer",
        "secrets_manager_arn": "secretsManagerArn",
        "url": "url",
        "user_name_attribute_field": "userNameAttributeField",
    },
)
class KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration:
    def __init__(
        self,
        *,
        key_location: builtins.str,
        claim_regex: typing.Optional[builtins.str] = None,
        group_attribute_field: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user_name_attribute_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#key_location KendraIndex#key_location}.
        :param claim_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#claim_regex KendraIndex#claim_regex}.
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#issuer KendraIndex#issuer}.
        :param secrets_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#secrets_manager_arn KendraIndex#secrets_manager_arn}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#url KendraIndex#url}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65988be800b6164d23734feeffbac8bd05effa6f4c27f6703a3a60e664aa6378)
            check_type(argname="argument key_location", value=key_location, expected_type=type_hints["key_location"])
            check_type(argname="argument claim_regex", value=claim_regex, expected_type=type_hints["claim_regex"])
            check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument secrets_manager_arn", value=secrets_manager_arn, expected_type=type_hints["secrets_manager_arn"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_location": key_location,
        }
        if claim_regex is not None:
            self._values["claim_regex"] = claim_regex
        if group_attribute_field is not None:
            self._values["group_attribute_field"] = group_attribute_field
        if issuer is not None:
            self._values["issuer"] = issuer
        if secrets_manager_arn is not None:
            self._values["secrets_manager_arn"] = secrets_manager_arn
        if url is not None:
            self._values["url"] = url
        if user_name_attribute_field is not None:
            self._values["user_name_attribute_field"] = user_name_attribute_field

    @builtins.property
    def key_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#key_location KendraIndex#key_location}.'''
        result = self._values.get("key_location")
        assert result is not None, "Required property 'key_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def claim_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#claim_regex KendraIndex#claim_regex}.'''
        result = self._values.get("claim_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_attribute_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.'''
        result = self._values.get("group_attribute_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#issuer KendraIndex#issuer}.'''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_manager_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#secrets_manager_arn KendraIndex#secrets_manager_arn}.'''
        result = self._values.get("secrets_manager_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#url KendraIndex#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_attribute_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.'''
        result = self._values.get("user_name_attribute_field")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7dba220f0ba33ba48facc04b96c3a294c277a215eebb4e9cc521c6cc44528d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClaimRegex")
    def reset_claim_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClaimRegex", []))

    @jsii.member(jsii_name="resetGroupAttributeField")
    def reset_group_attribute_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupAttributeField", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetSecretsManagerArn")
    def reset_secrets_manager_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsManagerArn", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="resetUserNameAttributeField")
    def reset_user_name_attribute_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserNameAttributeField", []))

    @builtins.property
    @jsii.member(jsii_name="claimRegexInput")
    def claim_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "claimRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAttributeFieldInput")
    def group_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="keyLocationInput")
    def key_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsManagerArnInput")
    def secrets_manager_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsManagerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeFieldInput")
    def user_name_attribute_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameAttributeFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="claimRegex")
    def claim_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "claimRegex"))

    @claim_regex.setter
    def claim_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef23afe3a4ab491776a547122ecf19b3eb1043ece2ea16d070eda577de29c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "claimRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupAttributeField")
    def group_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupAttributeField"))

    @group_attribute_field.setter
    def group_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333e6c29e697ff38e2c49d110ff7b0c5e75b4830c7258a0bfe3a17b9bc77057e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f988832b4898572724b24076695891c9858bf6976fbf53328f72dc3d1430e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyLocation")
    def key_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyLocation"))

    @key_location.setter
    def key_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6d1f08bc1a737034ff820fec55711aad009cb264735a8ba79b6820f8ae3f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretsManagerArn")
    def secrets_manager_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsManagerArn"))

    @secrets_manager_arn.setter
    def secrets_manager_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfda53f402e6a9f3215aabfe56d615ee9e307da33d9996ae6cd1c764620bf669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretsManagerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7739af694e8338ef03c35461e4cb606dc8e9b1f6ea1871cbedc1753dd1bc5880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userNameAttributeField")
    def user_name_attribute_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameAttributeField"))

    @user_name_attribute_field.setter
    def user_name_attribute_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbba4142d065930014daa00c5642335f5271fdfacec24d61fe6e53e19a4476be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameAttributeField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98660d6827a8275c08f4029ec052146b5e1399993e9d7d25419f2d545ca89cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraIndexUserTokenConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kendraIndex.KendraIndexUserTokenConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e0fcdacdb888044c8a7678d49608928260e917ad3b337023b5350e3b42beda5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJsonTokenTypeConfiguration")
    def put_json_token_type_configuration(
        self,
        *,
        group_attribute_field: builtins.str,
        user_name_attribute_field: builtins.str,
    ) -> None:
        '''
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        value = KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration(
            group_attribute_field=group_attribute_field,
            user_name_attribute_field=user_name_attribute_field,
        )

        return typing.cast(None, jsii.invoke(self, "putJsonTokenTypeConfiguration", [value]))

    @jsii.member(jsii_name="putJwtTokenTypeConfiguration")
    def put_jwt_token_type_configuration(
        self,
        *,
        key_location: builtins.str,
        claim_regex: typing.Optional[builtins.str] = None,
        group_attribute_field: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        user_name_attribute_field: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#key_location KendraIndex#key_location}.
        :param claim_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#claim_regex KendraIndex#claim_regex}.
        :param group_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#group_attribute_field KendraIndex#group_attribute_field}.
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#issuer KendraIndex#issuer}.
        :param secrets_manager_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#secrets_manager_arn KendraIndex#secrets_manager_arn}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#url KendraIndex#url}.
        :param user_name_attribute_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kendra_index#user_name_attribute_field KendraIndex#user_name_attribute_field}.
        '''
        value = KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration(
            key_location=key_location,
            claim_regex=claim_regex,
            group_attribute_field=group_attribute_field,
            issuer=issuer,
            secrets_manager_arn=secrets_manager_arn,
            url=url,
            user_name_attribute_field=user_name_attribute_field,
        )

        return typing.cast(None, jsii.invoke(self, "putJwtTokenTypeConfiguration", [value]))

    @jsii.member(jsii_name="resetJsonTokenTypeConfiguration")
    def reset_json_token_type_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonTokenTypeConfiguration", []))

    @jsii.member(jsii_name="resetJwtTokenTypeConfiguration")
    def reset_jwt_token_type_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtTokenTypeConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="jsonTokenTypeConfiguration")
    def json_token_type_configuration(
        self,
    ) -> KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference:
        return typing.cast(KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference, jsii.get(self, "jsonTokenTypeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="jwtTokenTypeConfiguration")
    def jwt_token_type_configuration(
        self,
    ) -> KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference:
        return typing.cast(KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference, jsii.get(self, "jwtTokenTypeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="jsonTokenTypeConfigurationInput")
    def json_token_type_configuration_input(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration], jsii.get(self, "jsonTokenTypeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtTokenTypeConfigurationInput")
    def jwt_token_type_configuration_input(
        self,
    ) -> typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration], jsii.get(self, "jwtTokenTypeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraIndexUserTokenConfigurations]:
        return typing.cast(typing.Optional[KendraIndexUserTokenConfigurations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraIndexUserTokenConfigurations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9bf79141aa32f6b6909ea0182f4d455fee96d19b817f1c0eccd07c614a48e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KendraIndex",
    "KendraIndexCapacityUnits",
    "KendraIndexCapacityUnitsOutputReference",
    "KendraIndexConfig",
    "KendraIndexDocumentMetadataConfigurationUpdates",
    "KendraIndexDocumentMetadataConfigurationUpdatesList",
    "KendraIndexDocumentMetadataConfigurationUpdatesOutputReference",
    "KendraIndexDocumentMetadataConfigurationUpdatesRelevance",
    "KendraIndexDocumentMetadataConfigurationUpdatesRelevanceOutputReference",
    "KendraIndexDocumentMetadataConfigurationUpdatesSearch",
    "KendraIndexDocumentMetadataConfigurationUpdatesSearchOutputReference",
    "KendraIndexIndexStatistics",
    "KendraIndexIndexStatisticsFaqStatistics",
    "KendraIndexIndexStatisticsFaqStatisticsList",
    "KendraIndexIndexStatisticsFaqStatisticsOutputReference",
    "KendraIndexIndexStatisticsList",
    "KendraIndexIndexStatisticsOutputReference",
    "KendraIndexIndexStatisticsTextDocumentStatistics",
    "KendraIndexIndexStatisticsTextDocumentStatisticsList",
    "KendraIndexIndexStatisticsTextDocumentStatisticsOutputReference",
    "KendraIndexServerSideEncryptionConfiguration",
    "KendraIndexServerSideEncryptionConfigurationOutputReference",
    "KendraIndexTimeouts",
    "KendraIndexTimeoutsOutputReference",
    "KendraIndexUserGroupResolutionConfiguration",
    "KendraIndexUserGroupResolutionConfigurationOutputReference",
    "KendraIndexUserTokenConfigurations",
    "KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration",
    "KendraIndexUserTokenConfigurationsJsonTokenTypeConfigurationOutputReference",
    "KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration",
    "KendraIndexUserTokenConfigurationsJwtTokenTypeConfigurationOutputReference",
    "KendraIndexUserTokenConfigurationsOutputReference",
]

publication.publish()

def _typecheckingstub__23d57116481ba58231085cc41552c60c8d98f72c43aaf64a1d9062499f476960(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    role_arn: builtins.str,
    capacity_units: typing.Optional[typing.Union[KendraIndexCapacityUnits, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraIndexDocumentMetadataConfigurationUpdates, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[KendraIndexServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_group_resolution_configuration: typing.Optional[typing.Union[KendraIndexUserGroupResolutionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    user_token_configurations: typing.Optional[typing.Union[KendraIndexUserTokenConfigurations, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bd4401ad0533d29987e406cda06b517f758a9a0893c46b7789307214714fa575(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1218b3ab47dcb61ae1a32e2373165c7801516519a4230606bd311425ac892f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraIndexDocumentMetadataConfigurationUpdates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3f67880f410590622a2e1b9ab98fab4912657a5f58d5f9390bc723429d12a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9b6f03ae6ffa4c21f3a23c9bb65373aabde2e5fca44a1dc28f9391cbd82d84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018d2626baa4dac2fff43ae21a0e0007f8d800bc4662d471712631ba89c0f043(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f516a4f1b6dcae9feb661dcd43994b2334c3bb4d57d7458d361ee3ed8faa0d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de358ff2f2a24a221ef4f9d64ff43ffb16b21ed8b970a21793879b5ee5969adb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5a32e7a065b3ce4031ff1e8201b7b35fcc82aaea071cb50e32cfd24dbd8398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41811b7c6672150f1462059dbaa33b79f3134e9330632d43ab34dd716367384(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41063dee5a8da294c445e31b6375d9c40e9755f093b03f59dc4e333371d52b4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea25d3f7931827609cf9cc69f65ac3476faf946c6a231a7c0a2d8c923c86fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aebe77d931230c1dde252f3610df25d35476cce382b12ffcb6dee6f0426331b(
    *,
    query_capacity_units: typing.Optional[jsii.Number] = None,
    storage_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f0aa73b9e8527c07a11cd4821f8bb426c44c8b5fea3eb7d6d004956fa82130(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27a78818e0b721fa46617467d7cdfd87229d1a5ef4476e3e03c13d98c7b2e56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53842234c9bcfa9ca3b317938df074aea176e0640629bcf6f955573af899e10(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4005f9508adc8d97e71a5a626fd3159dbae8baed0e7b398840cf2c354f44bc73(
    value: typing.Optional[KendraIndexCapacityUnits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf0e545de7b71f4936d74a6a78b7615f60f35998c8d2f6384579cc6b74ea6dd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    role_arn: builtins.str,
    capacity_units: typing.Optional[typing.Union[KendraIndexCapacityUnits, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configuration_updates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraIndexDocumentMetadataConfigurationUpdates, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[KendraIndexServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_group_resolution_configuration: typing.Optional[typing.Union[KendraIndexUserGroupResolutionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    user_token_configurations: typing.Optional[typing.Union[KendraIndexUserTokenConfigurations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e73cab1efd63ff495c144cd86c39c8854c7c773000cc1370ad5005711fc10dc(
    *,
    name: builtins.str,
    type: builtins.str,
    relevance: typing.Optional[typing.Union[KendraIndexDocumentMetadataConfigurationUpdatesRelevance, typing.Dict[builtins.str, typing.Any]]] = None,
    search: typing.Optional[typing.Union[KendraIndexDocumentMetadataConfigurationUpdatesSearch, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd743057fd57e27de111e6417a6f535eaf68a8734bfe808c1587323480799577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1a20f7d053ea8a8b924eacf1af65267684f1dd7e10ec0079495303e8faaac0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b426ab1902e4f7d2db0d720fa39d3ca1ff9317d40b6d4a9fda63e7f29ca6063a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33643460fbd666c3ef7327832e2f59283fa2c457a9adc944abeed895b58835a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee8641968c42581aa0c9d6ae5a828209508ccddaebac3382df3c5c0ee3fd04e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f89a127da8dbbca4b5b54014c2a5e272c94911910573c0f173f82a39ecad4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraIndexDocumentMetadataConfigurationUpdates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1959ecc0fbf18677fefaa8673e051df1f06fcf9290522cfaa5ffbed26ec4666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1d4a8cd9ad08a43c1d315fbddc0585eede5f2440425aa292712febcbdd75ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5371595a1067528bdfe3c84473c61683d2a211c3f4b5a4e3e0d10de5d91fea0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d88cc68bf3760bc868b957c426dc2b53bf886d4b6d9814899433c24a222258(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexDocumentMetadataConfigurationUpdates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1450eca4b48d9f2801a75bb9d00405e0241df714452dc326ff669fed4b91340d(
    *,
    duration: typing.Optional[builtins.str] = None,
    freshness: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    importance: typing.Optional[jsii.Number] = None,
    rank_order: typing.Optional[builtins.str] = None,
    values_importance_map: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd07d47cae512548f579151fc1ba1d7e8614de6543aa11c0719504ba80637d78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7e20a69ec7dd274188dddf5163703d9e56e64b8317ce35d419debb58a7dca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c448069691424f6a2a62b2a43b790f5f95bb1359329d11a77c279f4e118c85b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670485c5aea547061d5166ebf7e7d1a39a82c5afeef994a5c42efdf3a82b947c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f946cdac005a3eddf1445703273dbe11be6b9b328159f14ae1399d47d584abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f124ce0e379138382acbf2e4142e18a7d284c80a6b2552a537792bc395c32c3(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5bfbd91a3121c0fa683ef1926a4a8bb454fb165d2c64dab45b39db3b0e3342(
    value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesRelevance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38550c6c89adbc9bfdd118850eac19deb62d401eeabacfbe545da3432fcf9d72(
    *,
    displayable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    facetable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sortable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f71e00687937c9a829879a7669cf8468783c4b4796fa0831dca4dd0986e088(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba4cc85e7699812ba55ba3106e27ef8777bc9293826647600686d803224f361(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b4f0c8c30eb8221f94364c5d43507dc14ccb67d70534ccd80de7b07cf4899a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424775d881ff5eda81ee2318d50f02b3f51e8e89e31f81414b5e079453302f40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b7bf46febcfbecf9863ab32dc87aeaacfc6be31641c0853c6cee0bfad31b4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84789c27e852a5bb4bb8ce936602a821b4e03116aef7ba19f99641293855eedb(
    value: typing.Optional[KendraIndexDocumentMetadataConfigurationUpdatesSearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484f80e39c59da8c24bce8235d4e3678177d47e01a1fa15b9f76bd167b9cf2a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a867bbcaa908aaf2994f740ac4581f26a0e82f19680697ece2fe974519eb2a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2bcb262952410be9d18de9433b15f4682ec2049d979f24fe952a25b75c38b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cbc34e4bdd0cdc033fd0ad34f21efc44a60d153725f972cb8279a635eb8d24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e832e3742936445654ecb6931caaf8558a4e097e505820a017bee9006bbb7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1645fcbec20bde5b999ac7b135e772837d776d1ec94c85f2082cd49dae756da4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652b5e49f8b3fecbc41c720941e53ba55d2e391f518d04a9238fdde02ad71ca3(
    value: typing.Optional[KendraIndexIndexStatisticsFaqStatistics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c13f08e48b7f590ba5e734f9a684a08d14b9c5c92e5106bb4c0166758092b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80c82294e84de435603f5482c1594fa87182892de461abf887692c12a4843dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb2b3f12badbf2f48b9fc04920ef77ede635a7af7130481cada36905dde0518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c567e29be5482df43ae3718da67485d92065217608386f319742f62b83f769d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498662b871e07f0abafa82f5721cae08435a3d320675663bd826d59da5cc28af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af240bd2891e31451fc55411e91fea5bf69acfb151af95f9ac3ce393fe302c54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85521ae0fa7059c9d42e78079e92ebdb9ba308b95809321bae684702ca8cb7a7(
    value: typing.Optional[KendraIndexIndexStatistics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e6f7e5c1f59cf33c553de54e29f745eaa244c14d8856efe92414807f8917e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253e940d4c463127b17286b23918f2bddc24ff9acbe2f2e1315501168cf09979(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6d3c53108a7bb855a7fa573e679bc323627e5c0e00ae9f40beecad274b53e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65b28df1fdbd15342abbb521bba1eb537142f1eafa1351d91cf39f475ce62d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0f247d8a7bd5eb5f5857977c719981afe4b1c88eea0fe12391fe2354cd211e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb1ace206e6ba2ac348e2c13f99161ef507b7f9a6825b0aa60518f8f72f4a46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02d998a28242ace0bd488a25caad14964f17faf1b64980952bf353b4589c94d(
    value: typing.Optional[KendraIndexIndexStatisticsTextDocumentStatistics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80198e3075e616dc7e4d660de8772d5ea67e3d263149089642d4d383505cb974(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc075b3967640c2808be74856180d354a5c874381483571a40e89ad7946be05e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8289658d2ef6855f119c5c7b601d4cb8a76ab0938fa8e66702a2e5e4753b2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08826c5962a1c24efeab2d372b9e63a2ce8976471fe437d7d8e6ead155fcdd0(
    value: typing.Optional[KendraIndexServerSideEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21cf4cd758a65bfcb3eb55c2b88a74a9b904d3b790fec8b4025a025542dc834(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2755eb7f5db573fe5bd5e3b2b7f25c30dd2a4ae67b245ca54a9f5a96d1513258(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49eb844aadda76fd571de0e4b75cd0deb8de645ff0d14f2c59e8c67ac2822757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6b95b678504d608f858f5bc05532a3a9a09a5537407d33cac615e7692d6c2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c34245a7acef24affd800ee99964b26b538ac5321fbbacc993416c7d7332d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241e6ac8eef8fcff3a6d11e744b195bb8fc4d8ebaafdcefe4adc565ebdc54d83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c8e0400aa01e18ad3118f2ff865b13ea8eef6b2fd90b7de7a60e2e99baefaf(
    *,
    user_group_resolution_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ee4a06bfc0c614a57c5b40c2307c2967f3b05d14c0101489ad10568ee8616e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6527a835512ec2cc6c4afaca827b7f6e60ea0155b96113a3d124bf81921ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86171d84c86c09d4f7158643668e6d6a40892d2b978fad751a7bf8c5608c816(
    value: typing.Optional[KendraIndexUserGroupResolutionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767ff9b0726061e8d966848f1ab59451993b8e1e509c5539feede918a9195e1d(
    *,
    json_token_type_configuration: typing.Optional[typing.Union[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt_token_type_configuration: typing.Optional[typing.Union[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba0a6c2d827b3a5638efe631bc3b6593d409b99ab7e8a927328a4448de4984e(
    *,
    group_attribute_field: builtins.str,
    user_name_attribute_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699d6498196f766619b55e97b9879d89d5346176e0c921214a6ad2226d184e98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f316a41d1d8cf97f173c43ac489b6d56ff8abb9f12b9810bfd972dc3f8d6d820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5b7dba3a47e2da28ac0098a287fa2966ea8d276c1253f08dfefd4527077815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee1e07bfd3d9018d02e4c08a04fc99b87cd753edbbe4fafecfd8dc8b0778b1d(
    value: typing.Optional[KendraIndexUserTokenConfigurationsJsonTokenTypeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65988be800b6164d23734feeffbac8bd05effa6f4c27f6703a3a60e664aa6378(
    *,
    key_location: builtins.str,
    claim_regex: typing.Optional[builtins.str] = None,
    group_attribute_field: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    secrets_manager_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    user_name_attribute_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dba220f0ba33ba48facc04b96c3a294c277a215eebb4e9cc521c6cc44528d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef23afe3a4ab491776a547122ecf19b3eb1043ece2ea16d070eda577de29c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333e6c29e697ff38e2c49d110ff7b0c5e75b4830c7258a0bfe3a17b9bc77057e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f988832b4898572724b24076695891c9858bf6976fbf53328f72dc3d1430e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6d1f08bc1a737034ff820fec55711aad009cb264735a8ba79b6820f8ae3f79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfda53f402e6a9f3215aabfe56d615ee9e307da33d9996ae6cd1c764620bf669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7739af694e8338ef03c35461e4cb606dc8e9b1f6ea1871cbedc1753dd1bc5880(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbba4142d065930014daa00c5642335f5271fdfacec24d61fe6e53e19a4476be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98660d6827a8275c08f4029ec052146b5e1399993e9d7d25419f2d545ca89cf8(
    value: typing.Optional[KendraIndexUserTokenConfigurationsJwtTokenTypeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0fcdacdb888044c8a7678d49608928260e917ad3b337023b5350e3b42beda5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9bf79141aa32f6b6909ea0182f4d455fee96d19b817f1c0eccd07c614a48e9(
    value: typing.Optional[KendraIndexUserTokenConfigurations],
) -> None:
    """Type checking stubs"""
    pass
