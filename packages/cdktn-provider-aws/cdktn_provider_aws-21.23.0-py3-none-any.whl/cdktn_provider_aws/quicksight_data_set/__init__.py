r'''
# `aws_quicksight_data_set`

Refer to the Terraform Registry for docs: [`aws_quicksight_data_set`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set).
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


class QuicksightDataSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set aws_quicksight_data_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_set_id: builtins.str,
        import_mode: builtins.str,
        name: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
        column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnLevelPermissionRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_set_usage_configuration: typing.Optional[typing.Union["QuicksightDataSetDataSetUsageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetFieldFolders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        refresh_properties: typing.Optional[typing.Union["QuicksightDataSetRefreshProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        row_level_permission_data_set: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionDataSet", typing.Dict[builtins.str, typing.Any]]] = None,
        row_level_permission_tag_configuration: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionTagConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set aws_quicksight_data_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_id QuicksightDataSet#data_set_id}.
        :param import_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#import_mode QuicksightDataSet#import_mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#aws_account_id QuicksightDataSet#aws_account_id}.
        :param column_groups: column_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_groups QuicksightDataSet#column_groups}
        :param column_level_permission_rules: column_level_permission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_level_permission_rules QuicksightDataSet#column_level_permission_rules}
        :param data_set_usage_configuration: data_set_usage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_usage_configuration QuicksightDataSet#data_set_usage_configuration}
        :param field_folders: field_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#field_folders QuicksightDataSet#field_folders}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#id QuicksightDataSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logical_table_map: logical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#logical_table_map QuicksightDataSet#logical_table_map}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#permissions QuicksightDataSet#permissions}
        :param physical_table_map: physical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_map QuicksightDataSet#physical_table_map}
        :param refresh_properties: refresh_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#refresh_properties QuicksightDataSet#refresh_properties}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#region QuicksightDataSet#region}
        :param row_level_permission_data_set: row_level_permission_data_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#row_level_permission_data_set QuicksightDataSet#row_level_permission_data_set}
        :param row_level_permission_tag_configuration: row_level_permission_tag_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#row_level_permission_tag_configuration QuicksightDataSet#row_level_permission_tag_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags_all QuicksightDataSet#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c5ca157865a70dada29aab6aff26e9cd2168c9d89e85ca1bb016273bf9f892)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightDataSetConfig(
            data_set_id=data_set_id,
            import_mode=import_mode,
            name=name,
            aws_account_id=aws_account_id,
            column_groups=column_groups,
            column_level_permission_rules=column_level_permission_rules,
            data_set_usage_configuration=data_set_usage_configuration,
            field_folders=field_folders,
            id=id,
            logical_table_map=logical_table_map,
            permissions=permissions,
            physical_table_map=physical_table_map,
            refresh_properties=refresh_properties,
            region=region,
            row_level_permission_data_set=row_level_permission_data_set,
            row_level_permission_tag_configuration=row_level_permission_tag_configuration,
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
        '''Generates CDKTF code for importing a QuicksightDataSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightDataSet to import.
        :param import_from_id: The id of the existing QuicksightDataSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightDataSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf05ccf2f787ca8171d44491e89d78875fc75e56ece3b9b22559afdb10345cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putColumnGroups")
    def put_column_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afec8b5b30c1275f8a5dac1492caa2c1a50f937fab23c1587a3c8410a363d45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumnGroups", [value]))

    @jsii.member(jsii_name="putColumnLevelPermissionRules")
    def put_column_level_permission_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnLevelPermissionRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2b8b5d0912d1fa41f512c5fb68e43beef1394f1e9d1e986fe966e83944670d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumnLevelPermissionRules", [value]))

    @jsii.member(jsii_name="putDataSetUsageConfiguration")
    def put_data_set_usage_configuration(
        self,
        *,
        disable_use_as_direct_query_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_use_as_imported_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_use_as_direct_query_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#disable_use_as_direct_query_source QuicksightDataSet#disable_use_as_direct_query_source}.
        :param disable_use_as_imported_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#disable_use_as_imported_source QuicksightDataSet#disable_use_as_imported_source}.
        '''
        value = QuicksightDataSetDataSetUsageConfiguration(
            disable_use_as_direct_query_source=disable_use_as_direct_query_source,
            disable_use_as_imported_source=disable_use_as_imported_source,
        )

        return typing.cast(None, jsii.invoke(self, "putDataSetUsageConfiguration", [value]))

    @jsii.member(jsii_name="putFieldFolders")
    def put_field_folders(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetFieldFolders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9905c18bb2f6452e3af351401e9fc7be5871d1a0e1cec974fd5dac11fc0eadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFieldFolders", [value]))

    @jsii.member(jsii_name="putLogicalTableMap")
    def put_logical_table_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421b93c1bc609d0f1116e6dd6d62621c6e984db3a7173ee5e7e15f89b18238ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogicalTableMap", [value]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23cd495ad713677230ba16b024c44dce4456790781cb308734fa070a78ce71f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="putPhysicalTableMap")
    def put_physical_table_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78187e4272733357db3abf893a22d49371774caa983b96c52f3bf2d811e2425f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPhysicalTableMap", [value]))

    @jsii.member(jsii_name="putRefreshProperties")
    def put_refresh_properties(
        self,
        *,
        refresh_configuration: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param refresh_configuration: refresh_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#refresh_configuration QuicksightDataSet#refresh_configuration}
        '''
        value = QuicksightDataSetRefreshProperties(
            refresh_configuration=refresh_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putRefreshProperties", [value]))

    @jsii.member(jsii_name="putRowLevelPermissionDataSet")
    def put_row_level_permission_data_set(
        self,
        *,
        arn: builtins.str,
        permission_policy: builtins.str,
        format_version: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#arn QuicksightDataSet#arn}.
        :param permission_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#permission_policy QuicksightDataSet#permission_policy}.
        :param format_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format_version QuicksightDataSet#format_version}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#namespace QuicksightDataSet#namespace}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        value = QuicksightDataSetRowLevelPermissionDataSet(
            arn=arn,
            permission_policy=permission_policy,
            format_version=format_version,
            namespace=namespace,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putRowLevelPermissionDataSet", [value]))

    @jsii.member(jsii_name="putRowLevelPermissionTagConfiguration")
    def put_row_level_permission_tag_configuration(
        self,
        *,
        tag_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules", typing.Dict[builtins.str, typing.Any]]]],
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tag_rules: tag_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_rules QuicksightDataSet#tag_rules}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        value = QuicksightDataSetRowLevelPermissionTagConfiguration(
            tag_rules=tag_rules, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putRowLevelPermissionTagConfiguration", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetColumnGroups")
    def reset_column_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnGroups", []))

    @jsii.member(jsii_name="resetColumnLevelPermissionRules")
    def reset_column_level_permission_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnLevelPermissionRules", []))

    @jsii.member(jsii_name="resetDataSetUsageConfiguration")
    def reset_data_set_usage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSetUsageConfiguration", []))

    @jsii.member(jsii_name="resetFieldFolders")
    def reset_field_folders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldFolders", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogicalTableMap")
    def reset_logical_table_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicalTableMap", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetPhysicalTableMap")
    def reset_physical_table_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalTableMap", []))

    @jsii.member(jsii_name="resetRefreshProperties")
    def reset_refresh_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshProperties", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRowLevelPermissionDataSet")
    def reset_row_level_permission_data_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowLevelPermissionDataSet", []))

    @jsii.member(jsii_name="resetRowLevelPermissionTagConfiguration")
    def reset_row_level_permission_tag_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowLevelPermissionTagConfiguration", []))

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
    @jsii.member(jsii_name="columnGroups")
    def column_groups(self) -> "QuicksightDataSetColumnGroupsList":
        return typing.cast("QuicksightDataSetColumnGroupsList", jsii.get(self, "columnGroups"))

    @builtins.property
    @jsii.member(jsii_name="columnLevelPermissionRules")
    def column_level_permission_rules(
        self,
    ) -> "QuicksightDataSetColumnLevelPermissionRulesList":
        return typing.cast("QuicksightDataSetColumnLevelPermissionRulesList", jsii.get(self, "columnLevelPermissionRules"))

    @builtins.property
    @jsii.member(jsii_name="dataSetUsageConfiguration")
    def data_set_usage_configuration(
        self,
    ) -> "QuicksightDataSetDataSetUsageConfigurationOutputReference":
        return typing.cast("QuicksightDataSetDataSetUsageConfigurationOutputReference", jsii.get(self, "dataSetUsageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="fieldFolders")
    def field_folders(self) -> "QuicksightDataSetFieldFoldersList":
        return typing.cast("QuicksightDataSetFieldFoldersList", jsii.get(self, "fieldFolders"))

    @builtins.property
    @jsii.member(jsii_name="logicalTableMap")
    def logical_table_map(self) -> "QuicksightDataSetLogicalTableMapList":
        return typing.cast("QuicksightDataSetLogicalTableMapList", jsii.get(self, "logicalTableMap"))

    @builtins.property
    @jsii.member(jsii_name="outputColumns")
    def output_columns(self) -> "QuicksightDataSetOutputColumnsList":
        return typing.cast("QuicksightDataSetOutputColumnsList", jsii.get(self, "outputColumns"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "QuicksightDataSetPermissionsList":
        return typing.cast("QuicksightDataSetPermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMap")
    def physical_table_map(self) -> "QuicksightDataSetPhysicalTableMapList":
        return typing.cast("QuicksightDataSetPhysicalTableMapList", jsii.get(self, "physicalTableMap"))

    @builtins.property
    @jsii.member(jsii_name="refreshProperties")
    def refresh_properties(self) -> "QuicksightDataSetRefreshPropertiesOutputReference":
        return typing.cast("QuicksightDataSetRefreshPropertiesOutputReference", jsii.get(self, "refreshProperties"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionDataSet")
    def row_level_permission_data_set(
        self,
    ) -> "QuicksightDataSetRowLevelPermissionDataSetOutputReference":
        return typing.cast("QuicksightDataSetRowLevelPermissionDataSetOutputReference", jsii.get(self, "rowLevelPermissionDataSet"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionTagConfiguration")
    def row_level_permission_tag_configuration(
        self,
    ) -> "QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference":
        return typing.cast("QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference", jsii.get(self, "rowLevelPermissionTagConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columnGroupsInput")
    def column_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnGroups"]]], jsii.get(self, "columnGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnLevelPermissionRulesInput")
    def column_level_permission_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnLevelPermissionRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnLevelPermissionRules"]]], jsii.get(self, "columnLevelPermissionRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetIdInput")
    def data_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetUsageConfigurationInput")
    def data_set_usage_configuration_input(
        self,
    ) -> typing.Optional["QuicksightDataSetDataSetUsageConfiguration"]:
        return typing.cast(typing.Optional["QuicksightDataSetDataSetUsageConfiguration"], jsii.get(self, "dataSetUsageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldFoldersInput")
    def field_folders_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]], jsii.get(self, "fieldFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importModeInput")
    def import_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalTableMapInput")
    def logical_table_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]], jsii.get(self, "logicalTableMapInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMapInput")
    def physical_table_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]], jsii.get(self, "physicalTableMapInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshPropertiesInput")
    def refresh_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRefreshProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSetRefreshProperties"], jsii.get(self, "refreshPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionDataSetInput")
    def row_level_permission_data_set_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"]:
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"], jsii.get(self, "rowLevelPermissionDataSetInput"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionTagConfigurationInput")
    def row_level_permission_tag_configuration_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"]:
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"], jsii.get(self, "rowLevelPermissionTagConfigurationInput"))

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
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d89222fd97ad188843b464cb2356e093323cee8e5e5d0d20eb4fcfacc24e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSetId")
    def data_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetId"))

    @data_set_id.setter
    def data_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00a986fd77dbc18cbe5d5350d7ef191a557812655d32c4d18676bb0ea59c93b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782bad3d629faf9f18d4b5a97b3e5e30a1e8b32954104a80de0218ddc5878675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importMode")
    def import_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importMode"))

    @import_mode.setter
    def import_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791aa59219100b68fafe9c8ab54fa42eed5afd6cd3165234f0dd92c62e1816f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a118f2faa80cc78b2579bb260710a9c9cf0de22d942032d6809d162e060c35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1596d0986886654f4ade60e19ecf6d7cd7f45fdacd7db9c185ad68cdaf6801de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beab084d3667114395a42a1482a2372b45f42356cdb84786029de016b5591b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11ae55903bc252658f859fccad668ff9a9c8978e33c93ac515ccdbe5cf4bc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroups",
    jsii_struct_bases=[],
    name_mapping={"geo_spatial_column_group": "geoSpatialColumnGroup"},
)
class QuicksightDataSetColumnGroups:
    def __init__(
        self,
        *,
        geo_spatial_column_group: typing.Optional[typing.Union["QuicksightDataSetColumnGroupsGeoSpatialColumnGroup", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param geo_spatial_column_group: geo_spatial_column_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#geo_spatial_column_group QuicksightDataSet#geo_spatial_column_group}
        '''
        if isinstance(geo_spatial_column_group, dict):
            geo_spatial_column_group = QuicksightDataSetColumnGroupsGeoSpatialColumnGroup(**geo_spatial_column_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac2418bb954011b35dfec5bd02a6994b950ab24539b02ee0bed1c5afa03c8ec)
            check_type(argname="argument geo_spatial_column_group", value=geo_spatial_column_group, expected_type=type_hints["geo_spatial_column_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if geo_spatial_column_group is not None:
            self._values["geo_spatial_column_group"] = geo_spatial_column_group

    @builtins.property
    def geo_spatial_column_group(
        self,
    ) -> typing.Optional["QuicksightDataSetColumnGroupsGeoSpatialColumnGroup"]:
        '''geo_spatial_column_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#geo_spatial_column_group QuicksightDataSet#geo_spatial_column_group}
        '''
        result = self._values.get("geo_spatial_column_group")
        return typing.cast(typing.Optional["QuicksightDataSetColumnGroupsGeoSpatialColumnGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetColumnGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsGeoSpatialColumnGroup",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns", "country_code": "countryCode", "name": "name"},
)
class QuicksightDataSetColumnGroupsGeoSpatialColumnGroup:
    def __init__(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        country_code: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#country_code QuicksightDataSet#country_code}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fe43687acb7c8c3b548a814d98dcf89f56c4091ece9accf9bb3a5e01ae0c44)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "country_code": country_code,
            "name": name,
        }

    @builtins.property
    def columns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.'''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def country_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#country_code QuicksightDataSet#country_code}.'''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetColumnGroupsGeoSpatialColumnGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26a4be56758b8c9cfb22f4ca8ce01d30156e02148481875f25166b8182114c16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d194e90fc695d37cd6b063b68fbd984bd715af36691468c5d91d669e8ad4844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f344767c9bb4d29cb5de5946711888c9bf3d540fb07a6b580e5a276c699761da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341e27bc2281a834ba729edb4a906d3c5343c298fe8ca014b2bf6e094113d158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup]:
        return typing.cast(typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be6ee03a4ebb63e4fac5e85af4fbe595abde4c3edf77ee85e0cc33cd08f6136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetColumnGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48422fa53512e05d361fe0f873fa759ca74e005546a5f96bbb0a142f2191f5af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightDataSetColumnGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d34a220a4980f9c61d9f972ccc589ce3660c57fc5526e60edb4d4fdc48f221)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetColumnGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946f5ae0d31edcfb7884f0fa4ad33d9fa4e8cdd00a41498eb9fb4845159553c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f014bc98a3804955ad7bbbd9745b3dd7dcf9c66262ff3f099e1a874d97df556e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd706cbe540c128b3f59a0c5b5c0d7b119d5c414cb78a6781218017d00c9d5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90817c36e318b31bbb4190621a648fdccf0635528c470829b93e40fb139522ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetColumnGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d613e1ac5e6644b0513e21c13edf0a3fe41daf4fc18fda31fbb3fda6f1106d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGeoSpatialColumnGroup")
    def put_geo_spatial_column_group(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        country_code: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#country_code QuicksightDataSet#country_code}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        '''
        value = QuicksightDataSetColumnGroupsGeoSpatialColumnGroup(
            columns=columns, country_code=country_code, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGeoSpatialColumnGroup", [value]))

    @jsii.member(jsii_name="resetGeoSpatialColumnGroup")
    def reset_geo_spatial_column_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoSpatialColumnGroup", []))

    @builtins.property
    @jsii.member(jsii_name="geoSpatialColumnGroup")
    def geo_spatial_column_group(
        self,
    ) -> QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference:
        return typing.cast(QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference, jsii.get(self, "geoSpatialColumnGroup"))

    @builtins.property
    @jsii.member(jsii_name="geoSpatialColumnGroupInput")
    def geo_spatial_column_group_input(
        self,
    ) -> typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup]:
        return typing.cast(typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup], jsii.get(self, "geoSpatialColumnGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c44be3a360a3dbd880204e71ea5b124f86860de6b2d8240ba51d40e572dab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnLevelPermissionRules",
    jsii_struct_bases=[],
    name_mapping={"column_names": "columnNames", "principals": "principals"},
)
class QuicksightDataSetColumnLevelPermissionRules:
    def __init__(
        self,
        *,
        column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param column_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_names QuicksightDataSet#column_names}.
        :param principals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#principals QuicksightDataSet#principals}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb96463707093275e17a0e8e245db98c3e814e8fd70605115e1822dc9d15c94d)
            check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column_names is not None:
            self._values["column_names"] = column_names
        if principals is not None:
            self._values["principals"] = principals

    @builtins.property
    def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_names QuicksightDataSet#column_names}.'''
        result = self._values.get("column_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#principals QuicksightDataSet#principals}.'''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetColumnLevelPermissionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetColumnLevelPermissionRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnLevelPermissionRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f8437919ec63bba0a1611d0c541ea4dc43696ea8582ea40848e053251eec98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetColumnLevelPermissionRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7cb405743e53a800d2e87bdbc72280a8db2db2c7ac9c40a0bb7413b998676b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetColumnLevelPermissionRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37de9703987e158afdeec31a19e83da799b0dbdde35fdceb6d4b050b6670349)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2366b3b64f778734c9fde0b8960db8f1f83e1112afee9f8450e7e1b9ddfb1480)
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
            type_hints = typing.get_type_hints(_typecheckingstub__813ba1d116fd1fd77a18448052702bf7be98917a32da16cf5d9920de4f2665b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3a7b85426d46c94504bc4b3a247af3bb821383841cbaceee86a073958da3c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetColumnLevelPermissionRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetColumnLevelPermissionRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__339ac9105b76149d9fef788524f8500795e82aa806a7b347dc28e49dfc5b90fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumnNames")
    def reset_column_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnNames", []))

    @jsii.member(jsii_name="resetPrincipals")
    def reset_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipals", []))

    @builtins.property
    @jsii.member(jsii_name="columnNamesInput")
    def column_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnNames")
    def column_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columnNames"))

    @column_names.setter
    def column_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8036c14f210c2d5a1b8d12da493088ecd258d237d762a04677065594d51c4a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1150ee3fa7e33161fa1b38ce46de1bae24cb7a8f83d59335178e827b8c8d0c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d060a1e9c05558fdee277385799786dda5072f7125e51130eada7b512d89b0c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_set_id": "dataSetId",
        "import_mode": "importMode",
        "name": "name",
        "aws_account_id": "awsAccountId",
        "column_groups": "columnGroups",
        "column_level_permission_rules": "columnLevelPermissionRules",
        "data_set_usage_configuration": "dataSetUsageConfiguration",
        "field_folders": "fieldFolders",
        "id": "id",
        "logical_table_map": "logicalTableMap",
        "permissions": "permissions",
        "physical_table_map": "physicalTableMap",
        "refresh_properties": "refreshProperties",
        "region": "region",
        "row_level_permission_data_set": "rowLevelPermissionDataSet",
        "row_level_permission_tag_configuration": "rowLevelPermissionTagConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class QuicksightDataSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_set_id: builtins.str,
        import_mode: builtins.str,
        name: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
        column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_set_usage_configuration: typing.Optional[typing.Union["QuicksightDataSetDataSetUsageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetFieldFolders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        refresh_properties: typing.Optional[typing.Union["QuicksightDataSetRefreshProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        row_level_permission_data_set: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionDataSet", typing.Dict[builtins.str, typing.Any]]] = None,
        row_level_permission_tag_configuration: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionTagConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param data_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_id QuicksightDataSet#data_set_id}.
        :param import_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#import_mode QuicksightDataSet#import_mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#aws_account_id QuicksightDataSet#aws_account_id}.
        :param column_groups: column_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_groups QuicksightDataSet#column_groups}
        :param column_level_permission_rules: column_level_permission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_level_permission_rules QuicksightDataSet#column_level_permission_rules}
        :param data_set_usage_configuration: data_set_usage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_usage_configuration QuicksightDataSet#data_set_usage_configuration}
        :param field_folders: field_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#field_folders QuicksightDataSet#field_folders}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#id QuicksightDataSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logical_table_map: logical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#logical_table_map QuicksightDataSet#logical_table_map}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#permissions QuicksightDataSet#permissions}
        :param physical_table_map: physical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_map QuicksightDataSet#physical_table_map}
        :param refresh_properties: refresh_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#refresh_properties QuicksightDataSet#refresh_properties}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#region QuicksightDataSet#region}
        :param row_level_permission_data_set: row_level_permission_data_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#row_level_permission_data_set QuicksightDataSet#row_level_permission_data_set}
        :param row_level_permission_tag_configuration: row_level_permission_tag_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#row_level_permission_tag_configuration QuicksightDataSet#row_level_permission_tag_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags_all QuicksightDataSet#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_set_usage_configuration, dict):
            data_set_usage_configuration = QuicksightDataSetDataSetUsageConfiguration(**data_set_usage_configuration)
        if isinstance(refresh_properties, dict):
            refresh_properties = QuicksightDataSetRefreshProperties(**refresh_properties)
        if isinstance(row_level_permission_data_set, dict):
            row_level_permission_data_set = QuicksightDataSetRowLevelPermissionDataSet(**row_level_permission_data_set)
        if isinstance(row_level_permission_tag_configuration, dict):
            row_level_permission_tag_configuration = QuicksightDataSetRowLevelPermissionTagConfiguration(**row_level_permission_tag_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7185323eac0f6e3c41c903bbd266360f9b96f79fdf03da8ee7dec323e91f2420)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_set_id", value=data_set_id, expected_type=type_hints["data_set_id"])
            check_type(argname="argument import_mode", value=import_mode, expected_type=type_hints["import_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument column_groups", value=column_groups, expected_type=type_hints["column_groups"])
            check_type(argname="argument column_level_permission_rules", value=column_level_permission_rules, expected_type=type_hints["column_level_permission_rules"])
            check_type(argname="argument data_set_usage_configuration", value=data_set_usage_configuration, expected_type=type_hints["data_set_usage_configuration"])
            check_type(argname="argument field_folders", value=field_folders, expected_type=type_hints["field_folders"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logical_table_map", value=logical_table_map, expected_type=type_hints["logical_table_map"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument physical_table_map", value=physical_table_map, expected_type=type_hints["physical_table_map"])
            check_type(argname="argument refresh_properties", value=refresh_properties, expected_type=type_hints["refresh_properties"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument row_level_permission_data_set", value=row_level_permission_data_set, expected_type=type_hints["row_level_permission_data_set"])
            check_type(argname="argument row_level_permission_tag_configuration", value=row_level_permission_tag_configuration, expected_type=type_hints["row_level_permission_tag_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_set_id": data_set_id,
            "import_mode": import_mode,
            "name": name,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if column_groups is not None:
            self._values["column_groups"] = column_groups
        if column_level_permission_rules is not None:
            self._values["column_level_permission_rules"] = column_level_permission_rules
        if data_set_usage_configuration is not None:
            self._values["data_set_usage_configuration"] = data_set_usage_configuration
        if field_folders is not None:
            self._values["field_folders"] = field_folders
        if id is not None:
            self._values["id"] = id
        if logical_table_map is not None:
            self._values["logical_table_map"] = logical_table_map
        if permissions is not None:
            self._values["permissions"] = permissions
        if physical_table_map is not None:
            self._values["physical_table_map"] = physical_table_map
        if refresh_properties is not None:
            self._values["refresh_properties"] = refresh_properties
        if region is not None:
            self._values["region"] = region
        if row_level_permission_data_set is not None:
            self._values["row_level_permission_data_set"] = row_level_permission_data_set
        if row_level_permission_tag_configuration is not None:
            self._values["row_level_permission_tag_configuration"] = row_level_permission_tag_configuration
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
    def data_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_id QuicksightDataSet#data_set_id}.'''
        result = self._values.get("data_set_id")
        assert result is not None, "Required property 'data_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def import_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#import_mode QuicksightDataSet#import_mode}.'''
        result = self._values.get("import_mode")
        assert result is not None, "Required property 'import_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#aws_account_id QuicksightDataSet#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]]:
        '''column_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_groups QuicksightDataSet#column_groups}
        '''
        result = self._values.get("column_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]], result)

    @builtins.property
    def column_level_permission_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]]:
        '''column_level_permission_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_level_permission_rules QuicksightDataSet#column_level_permission_rules}
        '''
        result = self._values.get("column_level_permission_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]], result)

    @builtins.property
    def data_set_usage_configuration(
        self,
    ) -> typing.Optional["QuicksightDataSetDataSetUsageConfiguration"]:
        '''data_set_usage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_usage_configuration QuicksightDataSet#data_set_usage_configuration}
        '''
        result = self._values.get("data_set_usage_configuration")
        return typing.cast(typing.Optional["QuicksightDataSetDataSetUsageConfiguration"], result)

    @builtins.property
    def field_folders(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]]:
        '''field_folders block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#field_folders QuicksightDataSet#field_folders}
        '''
        result = self._values.get("field_folders")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#id QuicksightDataSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logical_table_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]]:
        '''logical_table_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#logical_table_map QuicksightDataSet#logical_table_map}
        '''
        result = self._values.get("logical_table_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#permissions QuicksightDataSet#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]], result)

    @builtins.property
    def physical_table_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]]:
        '''physical_table_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_map QuicksightDataSet#physical_table_map}
        '''
        result = self._values.get("physical_table_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]], result)

    @builtins.property
    def refresh_properties(
        self,
    ) -> typing.Optional["QuicksightDataSetRefreshProperties"]:
        '''refresh_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#refresh_properties QuicksightDataSet#refresh_properties}
        '''
        result = self._values.get("refresh_properties")
        return typing.cast(typing.Optional["QuicksightDataSetRefreshProperties"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#region QuicksightDataSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def row_level_permission_data_set(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"]:
        '''row_level_permission_data_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#row_level_permission_data_set QuicksightDataSet#row_level_permission_data_set}
        '''
        result = self._values.get("row_level_permission_data_set")
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"], result)

    @builtins.property
    def row_level_permission_tag_configuration(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"]:
        '''row_level_permission_tag_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#row_level_permission_tag_configuration QuicksightDataSet#row_level_permission_tag_configuration}
        '''
        result = self._values.get("row_level_permission_tag_configuration")
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags_all QuicksightDataSet#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetDataSetUsageConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "disable_use_as_direct_query_source": "disableUseAsDirectQuerySource",
        "disable_use_as_imported_source": "disableUseAsImportedSource",
    },
)
class QuicksightDataSetDataSetUsageConfiguration:
    def __init__(
        self,
        *,
        disable_use_as_direct_query_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_use_as_imported_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_use_as_direct_query_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#disable_use_as_direct_query_source QuicksightDataSet#disable_use_as_direct_query_source}.
        :param disable_use_as_imported_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#disable_use_as_imported_source QuicksightDataSet#disable_use_as_imported_source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6967abe9adbf226f0b84cd7c2982e74d1ebaa383970831f162d801ca3933c82)
            check_type(argname="argument disable_use_as_direct_query_source", value=disable_use_as_direct_query_source, expected_type=type_hints["disable_use_as_direct_query_source"])
            check_type(argname="argument disable_use_as_imported_source", value=disable_use_as_imported_source, expected_type=type_hints["disable_use_as_imported_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_use_as_direct_query_source is not None:
            self._values["disable_use_as_direct_query_source"] = disable_use_as_direct_query_source
        if disable_use_as_imported_source is not None:
            self._values["disable_use_as_imported_source"] = disable_use_as_imported_source

    @builtins.property
    def disable_use_as_direct_query_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#disable_use_as_direct_query_source QuicksightDataSet#disable_use_as_direct_query_source}.'''
        result = self._values.get("disable_use_as_direct_query_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_use_as_imported_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#disable_use_as_imported_source QuicksightDataSet#disable_use_as_imported_source}.'''
        result = self._values.get("disable_use_as_imported_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetDataSetUsageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetDataSetUsageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetDataSetUsageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__650d85f682ff695c9bc49bcd37154cf0e83ae1f4ebbbcfee6d9f24a6e4cd4faf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableUseAsDirectQuerySource")
    def reset_disable_use_as_direct_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUseAsDirectQuerySource", []))

    @jsii.member(jsii_name="resetDisableUseAsImportedSource")
    def reset_disable_use_as_imported_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUseAsImportedSource", []))

    @builtins.property
    @jsii.member(jsii_name="disableUseAsDirectQuerySourceInput")
    def disable_use_as_direct_query_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUseAsDirectQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUseAsImportedSourceInput")
    def disable_use_as_imported_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUseAsImportedSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUseAsDirectQuerySource")
    def disable_use_as_direct_query_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUseAsDirectQuerySource"))

    @disable_use_as_direct_query_source.setter
    def disable_use_as_direct_query_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875218a502f8c75f1a3cdb902e26758d0a60b110381f87176141fef9b28db28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUseAsDirectQuerySource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableUseAsImportedSource")
    def disable_use_as_imported_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUseAsImportedSource"))

    @disable_use_as_imported_source.setter
    def disable_use_as_imported_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55078103845c8fd396475aacb4a9562209134ce32b0dd1cae965bf2e349675b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUseAsImportedSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetDataSetUsageConfiguration]:
        return typing.cast(typing.Optional[QuicksightDataSetDataSetUsageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetDataSetUsageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9280965192104159dd8606f99533991bd67f278149ee7561a5a660fd2819c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetFieldFolders",
    jsii_struct_bases=[],
    name_mapping={
        "field_folders_id": "fieldFoldersId",
        "columns": "columns",
        "description": "description",
    },
)
class QuicksightDataSetFieldFolders:
    def __init__(
        self,
        *,
        field_folders_id: builtins.str,
        columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param field_folders_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#field_folders_id QuicksightDataSet#field_folders_id}.
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#description QuicksightDataSet#description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2a4cbcb9e260c89d2ac2c4d61b293dc21d4f5ec18283c40e19566ae7a14b51)
            check_type(argname="argument field_folders_id", value=field_folders_id, expected_type=type_hints["field_folders_id"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_folders_id": field_folders_id,
        }
        if columns is not None:
            self._values["columns"] = columns
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def field_folders_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#field_folders_id QuicksightDataSet#field_folders_id}.'''
        result = self._values.get("field_folders_id")
        assert result is not None, "Required property 'field_folders_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def columns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.'''
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#description QuicksightDataSet#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetFieldFolders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetFieldFoldersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetFieldFoldersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90c0ac95dcacb0e4d9f73e03ea5f387b18409ad30c3f1b5ec689f78480b101a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightDataSetFieldFoldersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1250642eb9e9d8edc83e177a30e4cdd80e8e2c939c23668c2e4752e3c9817ddb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetFieldFoldersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d74b62048cedd30396e5cbf886000bf516da492531d7897b5104cd6ac3df4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc4e8692bfb4de9eac3e715b85f23841d2dc32bffbb35c26c00672b3c4c1add0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__351c8e61536cbf505a25a956b062c4453e5573d4f33e619c5958e72ec30a1e27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3c73a487a99dbd0de1300e62d3bc8a7161bfcb43ee4f859885d359d6e06595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetFieldFoldersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetFieldFoldersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9581d4eea622162aceb51028dee1fb10a1eef1ccf50684858a38306ab6be732b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumns")
    def reset_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumns", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldFoldersIdInput")
    def field_folders_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldFoldersIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b3157aed97a3c6390edeccb5f3e36a97e622291611615a1c6d953a0ada406c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295a57a1474721e73bfba0a938362950a0b7c1b0b78269ba512e940a6f9dcad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldFoldersId")
    def field_folders_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldFoldersId"))

    @field_folders_id.setter
    def field_folders_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396e4ed2f8f36f3a8e334be4b621bc88aceaf166da6335a0a9461a2e544af075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldFoldersId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319ce5a2498a85c4d9808dccf478bb4c8b52b6bc0929482b2414bb5f2dc5b969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMap",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "logical_table_map_id": "logicalTableMapId",
        "source": "source",
        "data_transforms": "dataTransforms",
    },
)
class QuicksightDataSetLogicalTableMap:
    def __init__(
        self,
        *,
        alias: builtins.str,
        logical_table_map_id: builtins.str,
        source: typing.Union["QuicksightDataSetLogicalTableMapSource", typing.Dict[builtins.str, typing.Any]],
        data_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#alias QuicksightDataSet#alias}.
        :param logical_table_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#logical_table_map_id QuicksightDataSet#logical_table_map_id}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#source QuicksightDataSet#source}
        :param data_transforms: data_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_transforms QuicksightDataSet#data_transforms}
        '''
        if isinstance(source, dict):
            source = QuicksightDataSetLogicalTableMapSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45bee23ff562f3394bd9f025a43021b541bbe20f47850e3a49cc77073e52c27)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument logical_table_map_id", value=logical_table_map_id, expected_type=type_hints["logical_table_map_id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument data_transforms", value=data_transforms, expected_type=type_hints["data_transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
            "logical_table_map_id": logical_table_map_id,
            "source": source,
        }
        if data_transforms is not None:
            self._values["data_transforms"] = data_transforms

    @builtins.property
    def alias(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#alias QuicksightDataSet#alias}.'''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logical_table_map_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#logical_table_map_id QuicksightDataSet#logical_table_map_id}.'''
        result = self._values.get("logical_table_map_id")
        assert result is not None, "Required property 'logical_table_map_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "QuicksightDataSetLogicalTableMapSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#source QuicksightDataSet#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("QuicksightDataSetLogicalTableMapSource", result)

    @builtins.property
    def data_transforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransforms"]]]:
        '''data_transforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_transforms QuicksightDataSet#data_transforms}
        '''
        result = self._values.get("data_transforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransforms"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransforms",
    jsii_struct_bases=[],
    name_mapping={
        "cast_column_type_operation": "castColumnTypeOperation",
        "create_columns_operation": "createColumnsOperation",
        "filter_operation": "filterOperation",
        "project_operation": "projectOperation",
        "rename_column_operation": "renameColumnOperation",
        "tag_column_operation": "tagColumnOperation",
        "untag_column_operation": "untagColumnOperation",
    },
)
class QuicksightDataSetLogicalTableMapDataTransforms:
    def __init__(
        self,
        *,
        cast_column_type_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        create_columns_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        filter_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsFilterOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        project_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        rename_column_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_column_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        untag_column_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cast_column_type_operation: cast_column_type_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#cast_column_type_operation QuicksightDataSet#cast_column_type_operation}
        :param create_columns_operation: create_columns_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#create_columns_operation QuicksightDataSet#create_columns_operation}
        :param filter_operation: filter_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#filter_operation QuicksightDataSet#filter_operation}
        :param project_operation: project_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#project_operation QuicksightDataSet#project_operation}
        :param rename_column_operation: rename_column_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#rename_column_operation QuicksightDataSet#rename_column_operation}
        :param tag_column_operation: tag_column_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_column_operation QuicksightDataSet#tag_column_operation}
        :param untag_column_operation: untag_column_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#untag_column_operation QuicksightDataSet#untag_column_operation}
        '''
        if isinstance(cast_column_type_operation, dict):
            cast_column_type_operation = QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation(**cast_column_type_operation)
        if isinstance(create_columns_operation, dict):
            create_columns_operation = QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation(**create_columns_operation)
        if isinstance(filter_operation, dict):
            filter_operation = QuicksightDataSetLogicalTableMapDataTransformsFilterOperation(**filter_operation)
        if isinstance(project_operation, dict):
            project_operation = QuicksightDataSetLogicalTableMapDataTransformsProjectOperation(**project_operation)
        if isinstance(rename_column_operation, dict):
            rename_column_operation = QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation(**rename_column_operation)
        if isinstance(tag_column_operation, dict):
            tag_column_operation = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation(**tag_column_operation)
        if isinstance(untag_column_operation, dict):
            untag_column_operation = QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation(**untag_column_operation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6854433b878e0767b928045d75605db15fe463316aeb81b3e3e4b638244e884c)
            check_type(argname="argument cast_column_type_operation", value=cast_column_type_operation, expected_type=type_hints["cast_column_type_operation"])
            check_type(argname="argument create_columns_operation", value=create_columns_operation, expected_type=type_hints["create_columns_operation"])
            check_type(argname="argument filter_operation", value=filter_operation, expected_type=type_hints["filter_operation"])
            check_type(argname="argument project_operation", value=project_operation, expected_type=type_hints["project_operation"])
            check_type(argname="argument rename_column_operation", value=rename_column_operation, expected_type=type_hints["rename_column_operation"])
            check_type(argname="argument tag_column_operation", value=tag_column_operation, expected_type=type_hints["tag_column_operation"])
            check_type(argname="argument untag_column_operation", value=untag_column_operation, expected_type=type_hints["untag_column_operation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cast_column_type_operation is not None:
            self._values["cast_column_type_operation"] = cast_column_type_operation
        if create_columns_operation is not None:
            self._values["create_columns_operation"] = create_columns_operation
        if filter_operation is not None:
            self._values["filter_operation"] = filter_operation
        if project_operation is not None:
            self._values["project_operation"] = project_operation
        if rename_column_operation is not None:
            self._values["rename_column_operation"] = rename_column_operation
        if tag_column_operation is not None:
            self._values["tag_column_operation"] = tag_column_operation
        if untag_column_operation is not None:
            self._values["untag_column_operation"] = untag_column_operation

    @builtins.property
    def cast_column_type_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation"]:
        '''cast_column_type_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#cast_column_type_operation QuicksightDataSet#cast_column_type_operation}
        '''
        result = self._values.get("cast_column_type_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation"], result)

    @builtins.property
    def create_columns_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation"]:
        '''create_columns_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#create_columns_operation QuicksightDataSet#create_columns_operation}
        '''
        result = self._values.get("create_columns_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation"], result)

    @builtins.property
    def filter_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsFilterOperation"]:
        '''filter_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#filter_operation QuicksightDataSet#filter_operation}
        '''
        result = self._values.get("filter_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsFilterOperation"], result)

    @builtins.property
    def project_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"]:
        '''project_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#project_operation QuicksightDataSet#project_operation}
        '''
        result = self._values.get("project_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"], result)

    @builtins.property
    def rename_column_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"]:
        '''rename_column_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#rename_column_operation QuicksightDataSet#rename_column_operation}
        '''
        result = self._values.get("rename_column_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"], result)

    @builtins.property
    def tag_column_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"]:
        '''tag_column_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_column_operation QuicksightDataSet#tag_column_operation}
        '''
        result = self._values.get("tag_column_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"], result)

    @builtins.property
    def untag_column_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"]:
        '''untag_column_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#untag_column_operation QuicksightDataSet#untag_column_operation}
        '''
        result = self._values.get("untag_column_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "new_column_type": "newColumnType",
        "format": "format",
    },
)
class QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        new_column_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#new_column_type QuicksightDataSet#new_column_type}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dff61c751823f90ac2d56f8cf3b84eb80fa7461ce90bb76f0615113a62906d8)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument new_column_type", value=new_column_type, expected_type=type_hints["new_column_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "new_column_type": new_column_type,
        }
        if format is not None:
            self._values["format"] = format

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_column_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#new_column_type QuicksightDataSet#new_column_type}.'''
        result = self._values.get("new_column_type")
        assert result is not None, "Required property 'new_column_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aa0dbace35f69d6ad55ef180fa7074af5035204cf89ba37c56439b351bdc103)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFormat")
    def reset_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormat", []))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="newColumnTypeInput")
    def new_column_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newColumnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117d536c5c3b0c4a2ae14701be27eced8387eec0543df802c0bff38659589b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3f7b06f3c5bdea992494b4b56e7454cab11487845fa2910e19c6a4f5958a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newColumnType")
    def new_column_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newColumnType"))

    @new_column_type.setter
    def new_column_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7dc38ab3c828b50023a542528f68bc36ae53cab667c83489c60a411765c964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newColumnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2550000c9685dc8951a2a66a5052125d1668a7e1dfec39a6c8e2f5d7c8ae9fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns"},
)
class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation:
    def __init__(
        self,
        *,
        columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd966ec7186fd449c02932e4d85cd6db005db55cdaebd80c582227de8e4d473)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
        }

    @builtins.property
    def columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns"]]:
        '''columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns",
    jsii_struct_bases=[],
    name_mapping={
        "column_id": "columnId",
        "column_name": "columnName",
        "expression": "expression",
    },
)
class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns:
    def __init__(
        self,
        *,
        column_id: builtins.str,
        column_name: builtins.str,
        expression: builtins.str,
    ) -> None:
        '''
        :param column_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_id QuicksightDataSet#column_id}.
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#expression QuicksightDataSet#expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5f0d3475415e138c014adb0b77b12c86aab22dd68e7a5964b7a0e06e340df7)
            check_type(argname="argument column_id", value=column_id, expected_type=type_hints["column_id"])
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_id": column_id,
            "column_name": column_name,
            "expression": expression,
        }

    @builtins.property
    def column_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_id QuicksightDataSet#column_id}.'''
        result = self._values.get("column_id")
        assert result is not None, "Required property 'column_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#expression QuicksightDataSet#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6d082942300d96ecced0ad0e67468d629b3e687ebd2590376600b9155551a92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b497272ce4402744973a48bb9fa1f44c1c47babda341d1133ab48a1b4843ec55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1ed22c0699fff9b0ab03256e6630a30d22bd223bea420248c14fe4711ce8e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed36cfb1a4f02b3dc945bf594930a6410e7f6bed6cfc21afdeeefe408bf238dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85f78d9f577ef2598c6c6ba541bff3dbfc2831f6f87be57e043c63bc0963c9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7615afa31f17ac979f9928d1a6bc5948d994a9cd0c2c6835de7e058dacf4f3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5aa93d91f2a1a2283dc9f8b5c3bbbf8a8a77afadce7ea989b6857aa1a3012bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="columnIdInput")
    def column_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="columnId")
    def column_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnId"))

    @column_id.setter
    def column_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c406652b3bf56a27ff343574030ca5bc171c7825161e5ad9c0909bc54681afa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce917b23c75ed3c87ada8c86ae9147d1453f8f32162cbc639c57fc993d49d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a9d64a705f8736be9e499fc45bf8f350e26b70a342424bf54c379bdf013021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f3caa993d96f7ab491119d8fae685fcaf9b61e5024445d09f746601ca20ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba93d993c1607f8d0998f0f3d473e5c9dac9f13bce8907f95b6f33a97c79c2f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putColumns")
    def put_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb79759213c15dceaf0bd0c3057c038c761d40b24b4c0f7616794c393974736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumns", [value]))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList, jsii.get(self, "columns"))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbe0dbc8fe76edfc0f2ec6ae7f259009f750c23d6c3bd01786d33c4c42a5028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsFilterOperation",
    jsii_struct_bases=[],
    name_mapping={"condition_expression": "conditionExpression"},
)
class QuicksightDataSetLogicalTableMapDataTransformsFilterOperation:
    def __init__(self, *, condition_expression: builtins.str) -> None:
        '''
        :param condition_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#condition_expression QuicksightDataSet#condition_expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846a7f09be22680efc23b4b509c60e179e8b2f21a7a94505fb254a05c4fbad28)
            check_type(argname="argument condition_expression", value=condition_expression, expected_type=type_hints["condition_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_expression": condition_expression,
        }

    @builtins.property
    def condition_expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#condition_expression QuicksightDataSet#condition_expression}.'''
        result = self._values.get("condition_expression")
        assert result is not None, "Required property 'condition_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsFilterOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eb9309c6bdc9f44b934adae89e88a2234346b27adcbc70051ff20c48b69cac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="conditionExpressionInput")
    def condition_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionExpression")
    def condition_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionExpression"))

    @condition_expression.setter
    def condition_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2170cc0376be8877823aee83bb1a4cf960375bf9debb71edebdea8fb89d845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de86c6319b720d0ac388bffb384725ef5dd3c307ff21057386fa37926894ed73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01555b0e1471820af099a95796ee7f4c02eab5008247307990dc1cbe65abdbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4237cb93ae9bafa5859ae80ddeacf46bb616ab87b49c4747f9837c3ce4f9f7c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7764b0f13f330b34f88017e8eb1d8fa799ef976d47e7d70993c92f737738d0b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5909e415954e94c4ee2c504b5cc130b37232ffb808764068bd4a9f2da371ae2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d72d1e6c16e528420f734aaaf4edc5924eb030d400bfe5291846de348b986b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0211a4b03e91e60009b11c8c09a330815c143a081c304d2316678ddf33fbffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f23137613e4057b8bb2b053f0fa34579e59906fa9229c4690d1fc4d921f238d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCastColumnTypeOperation")
    def put_cast_column_type_operation(
        self,
        *,
        column_name: builtins.str,
        new_column_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#new_column_type QuicksightDataSet#new_column_type}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation(
            column_name=column_name, new_column_type=new_column_type, format=format
        )

        return typing.cast(None, jsii.invoke(self, "putCastColumnTypeOperation", [value]))

    @jsii.member(jsii_name="putCreateColumnsOperation")
    def put_create_columns_operation(
        self,
        *,
        columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation(
            columns=columns
        )

        return typing.cast(None, jsii.invoke(self, "putCreateColumnsOperation", [value]))

    @jsii.member(jsii_name="putFilterOperation")
    def put_filter_operation(self, *, condition_expression: builtins.str) -> None:
        '''
        :param condition_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#condition_expression QuicksightDataSet#condition_expression}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsFilterOperation(
            condition_expression=condition_expression
        )

        return typing.cast(None, jsii.invoke(self, "putFilterOperation", [value]))

    @jsii.member(jsii_name="putProjectOperation")
    def put_project_operation(
        self,
        *,
        projected_columns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param projected_columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#projected_columns QuicksightDataSet#projected_columns}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsProjectOperation(
            projected_columns=projected_columns
        )

        return typing.cast(None, jsii.invoke(self, "putProjectOperation", [value]))

    @jsii.member(jsii_name="putRenameColumnOperation")
    def put_rename_column_operation(
        self,
        *,
        column_name: builtins.str,
        new_column_name: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#new_column_name QuicksightDataSet#new_column_name}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation(
            column_name=column_name, new_column_name=new_column_name
        )

        return typing.cast(None, jsii.invoke(self, "putRenameColumnOperation", [value]))

    @jsii.member(jsii_name="putTagColumnOperation")
    def put_tag_column_operation(
        self,
        *,
        column_name: builtins.str,
        tags: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation(
            column_name=column_name, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putTagColumnOperation", [value]))

    @jsii.member(jsii_name="putUntagColumnOperation")
    def put_untag_column_operation(
        self,
        *,
        column_name: builtins.str,
        tag_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tag_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_names QuicksightDataSet#tag_names}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation(
            column_name=column_name, tag_names=tag_names
        )

        return typing.cast(None, jsii.invoke(self, "putUntagColumnOperation", [value]))

    @jsii.member(jsii_name="resetCastColumnTypeOperation")
    def reset_cast_column_type_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCastColumnTypeOperation", []))

    @jsii.member(jsii_name="resetCreateColumnsOperation")
    def reset_create_columns_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateColumnsOperation", []))

    @jsii.member(jsii_name="resetFilterOperation")
    def reset_filter_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterOperation", []))

    @jsii.member(jsii_name="resetProjectOperation")
    def reset_project_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectOperation", []))

    @jsii.member(jsii_name="resetRenameColumnOperation")
    def reset_rename_column_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameColumnOperation", []))

    @jsii.member(jsii_name="resetTagColumnOperation")
    def reset_tag_column_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagColumnOperation", []))

    @jsii.member(jsii_name="resetUntagColumnOperation")
    def reset_untag_column_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUntagColumnOperation", []))

    @builtins.property
    @jsii.member(jsii_name="castColumnTypeOperation")
    def cast_column_type_operation(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference, jsii.get(self, "castColumnTypeOperation"))

    @builtins.property
    @jsii.member(jsii_name="createColumnsOperation")
    def create_columns_operation(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference, jsii.get(self, "createColumnsOperation"))

    @builtins.property
    @jsii.member(jsii_name="filterOperation")
    def filter_operation(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference, jsii.get(self, "filterOperation"))

    @builtins.property
    @jsii.member(jsii_name="projectOperation")
    def project_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference", jsii.get(self, "projectOperation"))

    @builtins.property
    @jsii.member(jsii_name="renameColumnOperation")
    def rename_column_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference", jsii.get(self, "renameColumnOperation"))

    @builtins.property
    @jsii.member(jsii_name="tagColumnOperation")
    def tag_column_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference", jsii.get(self, "tagColumnOperation"))

    @builtins.property
    @jsii.member(jsii_name="untagColumnOperation")
    def untag_column_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference", jsii.get(self, "untagColumnOperation"))

    @builtins.property
    @jsii.member(jsii_name="castColumnTypeOperationInput")
    def cast_column_type_operation_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation], jsii.get(self, "castColumnTypeOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="createColumnsOperationInput")
    def create_columns_operation_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation], jsii.get(self, "createColumnsOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterOperationInput")
    def filter_operation_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation], jsii.get(self, "filterOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectOperationInput")
    def project_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"], jsii.get(self, "projectOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="renameColumnOperationInput")
    def rename_column_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"], jsii.get(self, "renameColumnOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagColumnOperationInput")
    def tag_column_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"], jsii.get(self, "tagColumnOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="untagColumnOperationInput")
    def untag_column_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"], jsii.get(self, "untagColumnOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c578162b7f34b6d8073af5ced43a1a5b651d3042935d2b46a32f5ef7522e043b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsProjectOperation",
    jsii_struct_bases=[],
    name_mapping={"projected_columns": "projectedColumns"},
)
class QuicksightDataSetLogicalTableMapDataTransformsProjectOperation:
    def __init__(self, *, projected_columns: typing.Sequence[builtins.str]) -> None:
        '''
        :param projected_columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#projected_columns QuicksightDataSet#projected_columns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc12d7ec78867d14b64a4300d003c58fa3baa27ec2e2dec7a083f1aa142068cd)
            check_type(argname="argument projected_columns", value=projected_columns, expected_type=type_hints["projected_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "projected_columns": projected_columns,
        }

    @builtins.property
    def projected_columns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#projected_columns QuicksightDataSet#projected_columns}.'''
        result = self._values.get("projected_columns")
        assert result is not None, "Required property 'projected_columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsProjectOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c272ea8152512fb91216133b0f07e1b591b196696632a0c9db227058fe6634d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="projectedColumnsInput")
    def projected_columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectedColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectedColumns")
    def projected_columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectedColumns"))

    @projected_columns.setter
    def projected_columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1851c97c75abab2002ba768a9604aa96df40a368ee09d9237643c5dc2567f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectedColumns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c23ddabd0e6faa881a933019a250cc184d1f4bacbfaa203688292acbfc7553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "new_column_name": "newColumnName"},
)
class QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        new_column_name: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#new_column_name QuicksightDataSet#new_column_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375f79853a8be9579cc4059c7c19a6e59d00284709a2aeaffdf0c1ea6b5cc2ae)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument new_column_name", value=new_column_name, expected_type=type_hints["new_column_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "new_column_name": new_column_name,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#new_column_name QuicksightDataSet#new_column_name}.'''
        result = self._values.get("new_column_name")
        assert result is not None, "Required property 'new_column_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1023703c214324bac7305d0ecaaede9c167e0b0b2816f93cec075902c45f8972)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="newColumnNameInput")
    def new_column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newColumnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02358bbdcea20bbd92f57f9044851c7148992f3ab87a01ff199ab0f74c25e472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newColumnName")
    def new_column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newColumnName"))

    @new_column_name.setter
    def new_column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3e3732a8f670cddf67f7fb92836f938110ff1e209d300d7f05d4711823230f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newColumnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed5243f6af96637cc1e9af04f7fed5a70e9636537f69ca04f8771ddb6c37849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "tags": "tags"},
)
class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        tags: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d831f19201cb9b981d4da2b7d4ed750843738513687042b962f38d92a11bee5)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "tags": tags,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b0c1d7d9e2ec825824a7dbca3cca2d412951690dd8c762b57c12174355d6d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d99469c99e19f8e5f57cf42c7ee35fa82c0265f5071723104710d257507c163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214aedd14840070006a79ea4a434913332ed7ba0f2fd120d49f26e60be098d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8ac30abe52fc0a38d41c9f1ed114f8c4d711c88be77f0b10eab736a2348627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags",
    jsii_struct_bases=[],
    name_mapping={
        "column_description": "columnDescription",
        "column_geographic_role": "columnGeographicRole",
    },
)
class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags:
    def __init__(
        self,
        *,
        column_description: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        column_geographic_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_description: column_description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_description QuicksightDataSet#column_description}
        :param column_geographic_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_geographic_role QuicksightDataSet#column_geographic_role}.
        '''
        if isinstance(column_description, dict):
            column_description = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription(**column_description)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb4a2d294c93f28134b506f96f7ef167e846205c0d08545df1a936993668a96)
            check_type(argname="argument column_description", value=column_description, expected_type=type_hints["column_description"])
            check_type(argname="argument column_geographic_role", value=column_geographic_role, expected_type=type_hints["column_geographic_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column_description is not None:
            self._values["column_description"] = column_description
        if column_geographic_role is not None:
            self._values["column_geographic_role"] = column_geographic_role

    @builtins.property
    def column_description(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription"]:
        '''column_description block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_description QuicksightDataSet#column_description}
        '''
        result = self._values.get("column_description")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription"], result)

    @builtins.property
    def column_geographic_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_geographic_role QuicksightDataSet#column_geographic_role}.'''
        result = self._values.get("column_geographic_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription:
    def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#text QuicksightDataSet#text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d2945ada057afe460af94cd7b35d97ddb760a3928e96f74588dda5286a789d)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#text QuicksightDataSet#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5c791fa6bc9128815b2a30868b725d5c5b385dac5e9168738a2487a97b1b9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdecb059779cfa170859078d42a09967dba351516139b0d8eb2c6958ea2e1d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb02fcbb8215171699ebb0fe1bb212bd741237ba90d8ffedfedcf1fc28198109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__790d6bcd9d43a63aa94c6eee7f9d18c1891138e753a55ae04232c44e6d2851a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7809e352b8ff534a5637f8285170735ccc0c9ee271c99d060518ccf4936b39c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa04b58ed4e491df0ed21e685c128b81f2dd5134459207dd4b581ee3435304c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__439c2558ddcf992c2555b5bf7eec5704f41ddbbf8db2c8943db5728b1e41c970)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3654c31f524ea778bcde4890054b5bb020612cb557c6c1c292f03fb7272867b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d031f36e5e0f82ca40bbdc494dace47e4a65bd470f9c9bf01143ab6af739fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc4f51ea5b80e9e46a436604ca0425e917638b01912e9cef6c995a74ea4f0c73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putColumnDescription")
    def put_column_description(
        self,
        *,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#text QuicksightDataSet#text}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription(
            text=text
        )

        return typing.cast(None, jsii.invoke(self, "putColumnDescription", [value]))

    @jsii.member(jsii_name="resetColumnDescription")
    def reset_column_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnDescription", []))

    @jsii.member(jsii_name="resetColumnGeographicRole")
    def reset_column_geographic_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnGeographicRole", []))

    @builtins.property
    @jsii.member(jsii_name="columnDescription")
    def column_description(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference, jsii.get(self, "columnDescription"))

    @builtins.property
    @jsii.member(jsii_name="columnDescriptionInput")
    def column_description_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription], jsii.get(self, "columnDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="columnGeographicRoleInput")
    def column_geographic_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnGeographicRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="columnGeographicRole")
    def column_geographic_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnGeographicRole"))

    @column_geographic_role.setter
    def column_geographic_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e73397f205e8024ba999168e8372d896691b657eed40306010714d2b7d3f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnGeographicRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cec1b733bf91b926c8ad8648b95c63b8e996b3c98ee03c67c83c2ca048689ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "tag_names": "tagNames"},
)
class QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        tag_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tag_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_names QuicksightDataSet#tag_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee11deb8904f5528e6a3a1040fe71cc90e0296e6a46b3062bd809993ac596d5)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument tag_names", value=tag_names, expected_type=type_hints["tag_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "tag_names": tag_names,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_names QuicksightDataSet#tag_names}.'''
        result = self._values.get("tag_names")
        assert result is not None, "Required property 'tag_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea5b78b48f713909f37d5f3bda610cd3368985652b2cc8bf6285989d4ef87af4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNamesInput")
    def tag_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d388e9b6c2e6ba1b77d6eea21d68d8ba55cc0738b4a4c469bc86a21963e087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagNames")
    def tag_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagNames"))

    @tag_names.setter
    def tag_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938cad8c76ec4901446d0dd21fa004873f807ebbbe6597539975cdf8b7baecdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa4eafdf48ef7b0061268a62257dbb9f20af53b9aeec17be7d00399c54be521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8a8e7d2ad37d4214541f5634fca28b6bf23f377c136318bbd8b0b5c02b2d7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed30859a5c1ba93e5ed9d73cf72bf7cd11d8f956b147e3594e8e2fd7de557521)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cb71b9c4cc0bd8bc7ea4b498776f1b1d6e6825320d8e884482a1440653e559)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc786c28409cb5f28f9f67ce57c941d602f7b28dce12b6cd8237faa2aaee3cc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dce285fc113e81003b183dcac890dd34a240954bdfae16231f09761d3574d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec94d83c37936ad87d5d611a9eb574fc9081e443d50b4f836dde65035556726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__134015423020dabd208a573a46d38488035d2cfe0265fec90361e46433f40680)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataTransforms")
    def put_data_transforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransforms, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e246c63f006a4fdbe6578b5efcaa5905e292dcc06591ef24ac44eaf9637b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataTransforms", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        data_set_arn: typing.Optional[builtins.str] = None,
        join_instruction: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstruction", typing.Dict[builtins.str, typing.Any]]] = None,
        physical_table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_set_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_arn QuicksightDataSet#data_set_arn}.
        :param join_instruction: join_instruction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#join_instruction QuicksightDataSet#join_instruction}
        :param physical_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_id QuicksightDataSet#physical_table_id}.
        '''
        value = QuicksightDataSetLogicalTableMapSource(
            data_set_arn=data_set_arn,
            join_instruction=join_instruction,
            physical_table_id=physical_table_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetDataTransforms")
    def reset_data_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="dataTransforms")
    def data_transforms(self) -> QuicksightDataSetLogicalTableMapDataTransformsList:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsList, jsii.get(self, "dataTransforms"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "QuicksightDataSetLogicalTableMapSourceOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTransformsInput")
    def data_transforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]], jsii.get(self, "dataTransformsInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalTableMapIdInput")
    def logical_table_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalTableMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["QuicksightDataSetLogicalTableMapSource"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4c335c1fb50d329e5eccc33913da52b8a662a237b593e39128008008a3c556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicalTableMapId")
    def logical_table_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicalTableMapId"))

    @logical_table_map_id.setter
    def logical_table_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e32f38dc2f28584ab778aa0585269c7ce9fc1d08511ea99704fa7e87583f5dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicalTableMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fb9f7a0185fbc71ee6b364b5e5bdecea051fc4bd09adbd0a33f305b2f1826b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSource",
    jsii_struct_bases=[],
    name_mapping={
        "data_set_arn": "dataSetArn",
        "join_instruction": "joinInstruction",
        "physical_table_id": "physicalTableId",
    },
)
class QuicksightDataSetLogicalTableMapSource:
    def __init__(
        self,
        *,
        data_set_arn: typing.Optional[builtins.str] = None,
        join_instruction: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstruction", typing.Dict[builtins.str, typing.Any]]] = None,
        physical_table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_set_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_arn QuicksightDataSet#data_set_arn}.
        :param join_instruction: join_instruction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#join_instruction QuicksightDataSet#join_instruction}
        :param physical_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_id QuicksightDataSet#physical_table_id}.
        '''
        if isinstance(join_instruction, dict):
            join_instruction = QuicksightDataSetLogicalTableMapSourceJoinInstruction(**join_instruction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94144f6658501eb3df24ca0ab137b2c6a6b908a9757f2b5d649210cabbfc3554)
            check_type(argname="argument data_set_arn", value=data_set_arn, expected_type=type_hints["data_set_arn"])
            check_type(argname="argument join_instruction", value=join_instruction, expected_type=type_hints["join_instruction"])
            check_type(argname="argument physical_table_id", value=physical_table_id, expected_type=type_hints["physical_table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_set_arn is not None:
            self._values["data_set_arn"] = data_set_arn
        if join_instruction is not None:
            self._values["join_instruction"] = join_instruction
        if physical_table_id is not None:
            self._values["physical_table_id"] = physical_table_id

    @builtins.property
    def data_set_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_set_arn QuicksightDataSet#data_set_arn}.'''
        result = self._values.get("data_set_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_instruction(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstruction"]:
        '''join_instruction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#join_instruction QuicksightDataSet#join_instruction}
        '''
        result = self._values.get("join_instruction")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstruction"], result)

    @builtins.property
    def physical_table_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_id QuicksightDataSet#physical_table_id}.'''
        result = self._values.get("physical_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstruction",
    jsii_struct_bases=[],
    name_mapping={
        "left_operand": "leftOperand",
        "on_clause": "onClause",
        "right_operand": "rightOperand",
        "type": "type",
        "left_join_key_properties": "leftJoinKeyProperties",
        "right_join_key_properties": "rightJoinKeyProperties",
    },
)
class QuicksightDataSetLogicalTableMapSourceJoinInstruction:
    def __init__(
        self,
        *,
        left_operand: builtins.str,
        on_clause: builtins.str,
        right_operand: builtins.str,
        type: builtins.str,
        left_join_key_properties: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        right_join_key_properties: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param left_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#left_operand QuicksightDataSet#left_operand}.
        :param on_clause: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#on_clause QuicksightDataSet#on_clause}.
        :param right_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#right_operand QuicksightDataSet#right_operand}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        :param left_join_key_properties: left_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#left_join_key_properties QuicksightDataSet#left_join_key_properties}
        :param right_join_key_properties: right_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#right_join_key_properties QuicksightDataSet#right_join_key_properties}
        '''
        if isinstance(left_join_key_properties, dict):
            left_join_key_properties = QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties(**left_join_key_properties)
        if isinstance(right_join_key_properties, dict):
            right_join_key_properties = QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties(**right_join_key_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ed6d026567d6160c778408b2fa0a1c70ae95f716bd97f3eb58b297fcf6a30b)
            check_type(argname="argument left_operand", value=left_operand, expected_type=type_hints["left_operand"])
            check_type(argname="argument on_clause", value=on_clause, expected_type=type_hints["on_clause"])
            check_type(argname="argument right_operand", value=right_operand, expected_type=type_hints["right_operand"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument left_join_key_properties", value=left_join_key_properties, expected_type=type_hints["left_join_key_properties"])
            check_type(argname="argument right_join_key_properties", value=right_join_key_properties, expected_type=type_hints["right_join_key_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "left_operand": left_operand,
            "on_clause": on_clause,
            "right_operand": right_operand,
            "type": type,
        }
        if left_join_key_properties is not None:
            self._values["left_join_key_properties"] = left_join_key_properties
        if right_join_key_properties is not None:
            self._values["right_join_key_properties"] = right_join_key_properties

    @builtins.property
    def left_operand(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#left_operand QuicksightDataSet#left_operand}.'''
        result = self._values.get("left_operand")
        assert result is not None, "Required property 'left_operand' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_clause(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#on_clause QuicksightDataSet#on_clause}.'''
        result = self._values.get("on_clause")
        assert result is not None, "Required property 'on_clause' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def right_operand(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#right_operand QuicksightDataSet#right_operand}.'''
        result = self._values.get("right_operand")
        assert result is not None, "Required property 'right_operand' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def left_join_key_properties(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties"]:
        '''left_join_key_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#left_join_key_properties QuicksightDataSet#left_join_key_properties}
        '''
        result = self._values.get("left_join_key_properties")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties"], result)

    @builtins.property
    def right_join_key_properties(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"]:
        '''right_join_key_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#right_join_key_properties QuicksightDataSet#right_join_key_properties}
        '''
        result = self._values.get("right_join_key_properties")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSourceJoinInstruction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties",
    jsii_struct_bases=[],
    name_mapping={"unique_key": "uniqueKey"},
)
class QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties:
    def __init__(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8e5bead492084f09d06c4a298fe36c8af9952f645ddf925e31e5875d9eaad4)
            check_type(argname="argument unique_key", value=unique_key, expected_type=type_hints["unique_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unique_key is not None:
            self._values["unique_key"] = unique_key

    @builtins.property
    def unique_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.'''
        result = self._values.get("unique_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f594c7735ee519fded16d4e8fbd01fe8c126129927abbdd68423eb4a223c1e17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUniqueKey")
    def reset_unique_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueKey", []))

    @builtins.property
    @jsii.member(jsii_name="uniqueKeyInput")
    def unique_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniqueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKey")
    def unique_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "uniqueKey"))

    @unique_key.setter
    def unique_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158613f3504d727f39330c8143a392d38f4a9ce3dfabdf3bc5700e6df4284327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8388770bad05504b76ed3491e3781d5022d4a6aa8753f6bc243dd21f048131e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9cef5a8dbf227c5bf324c3ce14bb9ba2380bd31c51eef221a65a509a29ca6a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLeftJoinKeyProperties")
    def put_left_join_key_properties(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        value = QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties(
            unique_key=unique_key
        )

        return typing.cast(None, jsii.invoke(self, "putLeftJoinKeyProperties", [value]))

    @jsii.member(jsii_name="putRightJoinKeyProperties")
    def put_right_join_key_properties(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        value = QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties(
            unique_key=unique_key
        )

        return typing.cast(None, jsii.invoke(self, "putRightJoinKeyProperties", [value]))

    @jsii.member(jsii_name="resetLeftJoinKeyProperties")
    def reset_left_join_key_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeftJoinKeyProperties", []))

    @jsii.member(jsii_name="resetRightJoinKeyProperties")
    def reset_right_join_key_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRightJoinKeyProperties", []))

    @builtins.property
    @jsii.member(jsii_name="leftJoinKeyProperties")
    def left_join_key_properties(
        self,
    ) -> QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference, jsii.get(self, "leftJoinKeyProperties"))

    @builtins.property
    @jsii.member(jsii_name="rightJoinKeyProperties")
    def right_join_key_properties(
        self,
    ) -> "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference", jsii.get(self, "rightJoinKeyProperties"))

    @builtins.property
    @jsii.member(jsii_name="leftJoinKeyPropertiesInput")
    def left_join_key_properties_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties], jsii.get(self, "leftJoinKeyPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="leftOperandInput")
    def left_operand_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "leftOperandInput"))

    @builtins.property
    @jsii.member(jsii_name="onClauseInput")
    def on_clause_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onClauseInput"))

    @builtins.property
    @jsii.member(jsii_name="rightJoinKeyPropertiesInput")
    def right_join_key_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"], jsii.get(self, "rightJoinKeyPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="rightOperandInput")
    def right_operand_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rightOperandInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="leftOperand")
    def left_operand(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "leftOperand"))

    @left_operand.setter
    def left_operand(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15910d901ab10c1e9a2ba12eda91e7283277615631ff042933344497ca6d14d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leftOperand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onClause")
    def on_clause(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onClause"))

    @on_clause.setter
    def on_clause(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c18b72c521a74f6b4f27273336de6eb226ad33117f82350631950c88b4ecee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onClause", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rightOperand")
    def right_operand(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rightOperand"))

    @right_operand.setter
    def right_operand(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76803950923e4bebab6385fef3e195d76b577fe2cdb781974fd7074605ed6eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rightOperand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81821edda77f3a45f2b26110ff16cf6a56f2c503f1814cd2150565085c110083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce544b52a03bcf0917789ef6127925ad80a614de676ad16e0b6eca4448d93ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties",
    jsii_struct_bases=[],
    name_mapping={"unique_key": "uniqueKey"},
)
class QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties:
    def __init__(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8495b0347fb7d9a318d3792adff55144a55e8c59b6dd6f357db94d43ea53c67)
            check_type(argname="argument unique_key", value=unique_key, expected_type=type_hints["unique_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unique_key is not None:
            self._values["unique_key"] = unique_key

    @builtins.property
    def unique_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.'''
        result = self._values.get("unique_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8327c8b32ddd1b182bbef06cbf3983e8f06935a2f31a8e0c5566129207df493d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUniqueKey")
    def reset_unique_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueKey", []))

    @builtins.property
    @jsii.member(jsii_name="uniqueKeyInput")
    def unique_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniqueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKey")
    def unique_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "uniqueKey"))

    @unique_key.setter
    def unique_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76a69ac1f739e853cf3deb4c90d8d865986db75c9648eea7ae0b987aa06e9d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62a4ace8023071741a18ae04f4c001c5927f997ec26c4c45bdef718f4a6ab46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a43d19aacba117ced9088ff34bb58287d620645465a84e75dfe924d3b753587b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJoinInstruction")
    def put_join_instruction(
        self,
        *,
        left_operand: builtins.str,
        on_clause: builtins.str,
        right_operand: builtins.str,
        type: builtins.str,
        left_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
        right_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param left_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#left_operand QuicksightDataSet#left_operand}.
        :param on_clause: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#on_clause QuicksightDataSet#on_clause}.
        :param right_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#right_operand QuicksightDataSet#right_operand}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        :param left_join_key_properties: left_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#left_join_key_properties QuicksightDataSet#left_join_key_properties}
        :param right_join_key_properties: right_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#right_join_key_properties QuicksightDataSet#right_join_key_properties}
        '''
        value = QuicksightDataSetLogicalTableMapSourceJoinInstruction(
            left_operand=left_operand,
            on_clause=on_clause,
            right_operand=right_operand,
            type=type,
            left_join_key_properties=left_join_key_properties,
            right_join_key_properties=right_join_key_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putJoinInstruction", [value]))

    @jsii.member(jsii_name="resetDataSetArn")
    def reset_data_set_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSetArn", []))

    @jsii.member(jsii_name="resetJoinInstruction")
    def reset_join_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinInstruction", []))

    @jsii.member(jsii_name="resetPhysicalTableId")
    def reset_physical_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalTableId", []))

    @builtins.property
    @jsii.member(jsii_name="joinInstruction")
    def join_instruction(
        self,
    ) -> QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference, jsii.get(self, "joinInstruction"))

    @builtins.property
    @jsii.member(jsii_name="dataSetArnInput")
    def data_set_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="joinInstructionInput")
    def join_instruction_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction], jsii.get(self, "joinInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableIdInput")
    def physical_table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "physicalTableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetArn")
    def data_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetArn"))

    @data_set_arn.setter
    def data_set_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71b3d90295de54d38ad4ebf790003dc91c9590be98e27f873c633aed2f30c97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalTableId")
    def physical_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "physicalTableId"))

    @physical_table_id.setter
    def physical_table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94edb4a17ad3d74c57e3b5286db6235f98bac022645a14e397c52fe417dfc16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalTableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSetLogicalTableMapSource]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221a829e4dbd13ff2ef387b9bb39085ae007bd4a17757a8e69b0ddf26f4acb7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetOutputColumns",
    jsii_struct_bases=[],
    name_mapping={},
)
class QuicksightDataSetOutputColumns:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetOutputColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetOutputColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetOutputColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__017f0d7287f1999989cee177ff9fec3aa7f90ef47d919d8c7942df5713d8e039)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetOutputColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2842c436e7231e0e3bac8bfb03424ba348db7f0eb718df41bbf3deb1f762cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetOutputColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5705b030832d9f2317ef15410e92f1b27621eb279eaf8ad66adde112ff1d5786)
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
            type_hints = typing.get_type_hints(_typecheckingstub__425ab237fd475d56223211e4df83d345785b7ad6bdaf2e13fd59d8e24da62f0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e863f61884d3ee89643ec2d260c28b666258be5a92f8459407c71ede3c2ee139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetOutputColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetOutputColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60ab73346720b7a32c5b04915a61cded1f8cbeafa6ecd0afa6fc43020a30e999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSetOutputColumns]:
        return typing.cast(typing.Optional[QuicksightDataSetOutputColumns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetOutputColumns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587339e27fc049fc29887819a8d8d29ee4ef2fe742f506822718f589f877a0b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPermissions",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightDataSetPermissions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#actions QuicksightDataSet#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#principal QuicksightDataSet#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96886cac2b7f3037b8b6f687ea0e19fed7cbef9447f99af4e4342e2a25271ca3)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#actions QuicksightDataSet#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#principal QuicksightDataSet#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7272b691fee48faecf1cec6969cdc0e13f0be6bd9980b568810d966f6c8b6a36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightDataSetPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e219524ef6acd959a09faac3b51cdc9491ef2e7a620bdb47e4955ddece14c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84db83eb6234a9ae25590a9d6423b0238d71d84577fc0cf98e16a9e74cade810)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06430127d01d42864549fe2356579b3d43a008d0e33c2c95128b2a04dff70e8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4523ce8324a67d640bb0db7a63c2763f45a40c18636db7439b7c9ef6a7225c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b992bb218bc239e9e5f061c875fa5d1de7ea2d41eff6804eaceaefab7c6f0837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f89c5c56224027a93e18b5ca97d8f57023b6ade90e54ff34653b88010ac06f5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b160351ab0b89d80b77efb4c7d95616099f63b9f66ad1d62ad79b3a22aeef1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637aea9615b27ae1dfbe90d04ba1d795c74f74f3afa5cca5a8fe399f4a3e60a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0861390ffbb125a1f8a87f312bcfac5ebe4058e98834fc51dd4de847ab8a5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMap",
    jsii_struct_bases=[],
    name_mapping={
        "physical_table_map_id": "physicalTableMapId",
        "custom_sql": "customSql",
        "relational_table": "relationalTable",
        "s3_source": "s3Source",
    },
)
class QuicksightDataSetPhysicalTableMap:
    def __init__(
        self,
        *,
        physical_table_map_id: builtins.str,
        custom_sql: typing.Optional[typing.Union["QuicksightDataSetPhysicalTableMapCustomSql", typing.Dict[builtins.str, typing.Any]]] = None,
        relational_table: typing.Optional[typing.Union["QuicksightDataSetPhysicalTableMapRelationalTable", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_source: typing.Optional[typing.Union["QuicksightDataSetPhysicalTableMapS3Source", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param physical_table_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_map_id QuicksightDataSet#physical_table_map_id}.
        :param custom_sql: custom_sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#custom_sql QuicksightDataSet#custom_sql}
        :param relational_table: relational_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#relational_table QuicksightDataSet#relational_table}
        :param s3_source: s3_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#s3_source QuicksightDataSet#s3_source}
        '''
        if isinstance(custom_sql, dict):
            custom_sql = QuicksightDataSetPhysicalTableMapCustomSql(**custom_sql)
        if isinstance(relational_table, dict):
            relational_table = QuicksightDataSetPhysicalTableMapRelationalTable(**relational_table)
        if isinstance(s3_source, dict):
            s3_source = QuicksightDataSetPhysicalTableMapS3Source(**s3_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9cb44c65cbf4a2612f17831b00071838be354365c71b500e582357b1c149e0)
            check_type(argname="argument physical_table_map_id", value=physical_table_map_id, expected_type=type_hints["physical_table_map_id"])
            check_type(argname="argument custom_sql", value=custom_sql, expected_type=type_hints["custom_sql"])
            check_type(argname="argument relational_table", value=relational_table, expected_type=type_hints["relational_table"])
            check_type(argname="argument s3_source", value=s3_source, expected_type=type_hints["s3_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "physical_table_map_id": physical_table_map_id,
        }
        if custom_sql is not None:
            self._values["custom_sql"] = custom_sql
        if relational_table is not None:
            self._values["relational_table"] = relational_table
        if s3_source is not None:
            self._values["s3_source"] = s3_source

    @builtins.property
    def physical_table_map_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#physical_table_map_id QuicksightDataSet#physical_table_map_id}.'''
        result = self._values.get("physical_table_map_id")
        assert result is not None, "Required property 'physical_table_map_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_sql(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapCustomSql"]:
        '''custom_sql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#custom_sql QuicksightDataSet#custom_sql}
        '''
        result = self._values.get("custom_sql")
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapCustomSql"], result)

    @builtins.property
    def relational_table(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"]:
        '''relational_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#relational_table QuicksightDataSet#relational_table}
        '''
        result = self._values.get("relational_table")
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"], result)

    @builtins.property
    def s3_source(self) -> typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"]:
        '''s3_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#s3_source QuicksightDataSet#s3_source}
        '''
        result = self._values.get("s3_source")
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSql",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_arn": "dataSourceArn",
        "name": "name",
        "sql_query": "sqlQuery",
        "columns": "columns",
    },
)
class QuicksightDataSetPhysicalTableMapCustomSql:
    def __init__(
        self,
        *,
        data_source_arn: builtins.str,
        name: builtins.str,
        sql_query: builtins.str,
        columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapCustomSqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param sql_query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#sql_query QuicksightDataSet#sql_query}.
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b417045fc02fb477b93aa3ee5b9765b8193e9c568435670186ad964cdcb7bb)
            check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_query", value=sql_query, expected_type=type_hints["sql_query"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_arn": data_source_arn,
            "name": name,
            "sql_query": sql_query,
        }
        if columns is not None:
            self._values["columns"] = columns

    @builtins.property
    def data_source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.'''
        result = self._values.get("data_source_arn")
        assert result is not None, "Required property 'data_source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#sql_query QuicksightDataSet#sql_query}.'''
        result = self._values.get("sql_query")
        assert result is not None, "Required property 'sql_query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapCustomSqlColumns"]]]:
        '''columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapCustomSqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapCustomSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class QuicksightDataSetPhysicalTableMapCustomSqlColumns:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b358352c8d62e617a74428b7d027d11d59f56e7fd81cea20a0e72b9cd075aeba)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapCustomSqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapCustomSqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81f50a6a450e9b7cbabb04add9a455e195808168ae35d73a09223664184faeaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9daee33b4bc788fadb62f93f129a99f792afbb1b94f6e7b6d52fb0ef068a5aea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e190ff108d6ebf41019e0281e7f170d72dda5f8c10b177aa492f5d78b48ca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ccdf910594b2f7fdd707f7dd544459852102ef0a819975800496700793290c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f6c85c1f62839a1e3ee95e097bda4bc04cb2e214e261fbafbc62d1ad2fedff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee806658383bf24fffdb1967b0effe7b97c68a582fba3d154838c6ab0b672f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d6bc733450bddbb2d753d78764b36c36fe4b7a7cb9e436ffe29e767af501e1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aedc2b7ff0c724ad94193b94ac93d656a1e07595f41aa1b76ca3aaf2c26fbfd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520952401915d04390a3d9cf8293f4702b3178f135d4f253ce0d465f3742b0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb35cb6c32d77c5a2f1873f14439f99eb320d8a2db60908c0a0cf8d36136c7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapCustomSqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2811b9a2a705e92163037fa1be45d7535bfdec584ef8ba11f337c7bca4ff78eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putColumns")
    def put_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e494517a73353d6b5a01a46c03b2a59f2e80474eb7a1001866ff74ee3d59c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumns", [value]))

    @jsii.member(jsii_name="resetColumns")
    def reset_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumns", []))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> QuicksightDataSetPhysicalTableMapCustomSqlColumnsList:
        return typing.cast(QuicksightDataSetPhysicalTableMapCustomSqlColumnsList, jsii.get(self, "columns"))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArnInput")
    def data_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlQueryInput")
    def sql_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceArn"))

    @data_source_arn.setter
    def data_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d125b47f54f1558760aa7db122e538299d8811edabf9473c037caf4c6ce65b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f151179bb34653b5e5b2e538d353acfd927773f62b3e71a007bb1484c679128f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlQuery")
    def sql_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlQuery"))

    @sql_query.setter
    def sql_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f56833c25a367fbcf9e0d653a80e49cb9a23234527d05f4e1059338848f1caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4327b0f39b114c9491782655af7069be03fa78931d1da8d3b2f6d9c2ed288f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0fb961bfd74c1045c4988362fb124247e6a340dbde3cd757375e9ebad0d8fad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2789bf59948cf838a6b4e8e3a0716f87162c3bb4bfaeac3de4285d79c1571ea8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57863597594458797f47f98e8d8fd888e17fec202136a3023e1f552f2b5763cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9705775613ef208594e91f31b073df6f362843bc41d2ed7c21169c348290912)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95e6daa67d513b41463009b3bdb2a3d9d69570487a55a9863d6344b02a20057a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f362def38a042bdaac6295dc98582a1f17401f8614f3d2973101d73277829064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a296332b66f1834808c6af803e6f49383fe88a8cf498f3edc5a8dd3ecfda2ee9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomSql")
    def put_custom_sql(
        self,
        *,
        data_source_arn: builtins.str,
        name: builtins.str,
        sql_query: builtins.str,
        columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param sql_query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#sql_query QuicksightDataSet#sql_query}.
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        value = QuicksightDataSetPhysicalTableMapCustomSql(
            data_source_arn=data_source_arn,
            name=name,
            sql_query=sql_query,
            columns=columns,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomSql", [value]))

    @jsii.member(jsii_name="putRelationalTable")
    def put_relational_table(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#catalog QuicksightDataSet#catalog}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#schema QuicksightDataSet#schema}.
        '''
        value = QuicksightDataSetPhysicalTableMapRelationalTable(
            data_source_arn=data_source_arn,
            input_columns=input_columns,
            name=name,
            catalog=catalog,
            schema=schema,
        )

        return typing.cast(None, jsii.invoke(self, "putRelationalTable", [value]))

    @jsii.member(jsii_name="putS3Source")
    def put_s3_source(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapS3SourceInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        upload_settings: typing.Union["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param upload_settings: upload_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#upload_settings QuicksightDataSet#upload_settings}
        '''
        value = QuicksightDataSetPhysicalTableMapS3Source(
            data_source_arn=data_source_arn,
            input_columns=input_columns,
            upload_settings=upload_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Source", [value]))

    @jsii.member(jsii_name="resetCustomSql")
    def reset_custom_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSql", []))

    @jsii.member(jsii_name="resetRelationalTable")
    def reset_relational_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelationalTable", []))

    @jsii.member(jsii_name="resetS3Source")
    def reset_s3_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Source", []))

    @builtins.property
    @jsii.member(jsii_name="customSql")
    def custom_sql(self) -> QuicksightDataSetPhysicalTableMapCustomSqlOutputReference:
        return typing.cast(QuicksightDataSetPhysicalTableMapCustomSqlOutputReference, jsii.get(self, "customSql"))

    @builtins.property
    @jsii.member(jsii_name="relationalTable")
    def relational_table(
        self,
    ) -> "QuicksightDataSetPhysicalTableMapRelationalTableOutputReference":
        return typing.cast("QuicksightDataSetPhysicalTableMapRelationalTableOutputReference", jsii.get(self, "relationalTable"))

    @builtins.property
    @jsii.member(jsii_name="s3Source")
    def s3_source(self) -> "QuicksightDataSetPhysicalTableMapS3SourceOutputReference":
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceOutputReference", jsii.get(self, "s3Source"))

    @builtins.property
    @jsii.member(jsii_name="customSqlInput")
    def custom_sql_input(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql], jsii.get(self, "customSqlInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMapIdInput")
    def physical_table_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "physicalTableMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="relationalTableInput")
    def relational_table_input(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"]:
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"], jsii.get(self, "relationalTableInput"))

    @builtins.property
    @jsii.member(jsii_name="s3SourceInput")
    def s3_source_input(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"]:
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"], jsii.get(self, "s3SourceInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMapId")
    def physical_table_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "physicalTableMapId"))

    @physical_table_map_id.setter
    def physical_table_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cf14896f9bf81dd64ad21e4c56c4553e0a534b1d4730a1a50e475dc017f84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalTableMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bd54c8a4e88f6f0579134b758918d245148b8df5f66981d248dea323f8a3ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTable",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_arn": "dataSourceArn",
        "input_columns": "inputColumns",
        "name": "name",
        "catalog": "catalog",
        "schema": "schema",
    },
)
class QuicksightDataSetPhysicalTableMapRelationalTable:
    def __init__(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#catalog QuicksightDataSet#catalog}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#schema QuicksightDataSet#schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27d39e9e29def4d3aa69a0c4935de6193fb19e24e8e2e8b9a95c20db96cc375)
            check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
            check_type(argname="argument input_columns", value=input_columns, expected_type=type_hints["input_columns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_arn": data_source_arn,
            "input_columns": input_columns,
            "name": name,
        }
        if catalog is not None:
            self._values["catalog"] = catalog
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def data_source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.'''
        result = self._values.get("data_source_arn")
        assert result is not None, "Required property 'data_source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns"]]:
        '''input_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        '''
        result = self._values.get("input_columns")
        assert result is not None, "Required property 'input_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#catalog QuicksightDataSet#catalog}.'''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#schema QuicksightDataSet#schema}.'''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapRelationalTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableInputColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class QuicksightDataSetPhysicalTableMapRelationalTableInputColumns:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d811d13228990f86e0d27c79f2791706d522f8914745055f46021e57c9c2548f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapRelationalTableInputColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be33c4dbb177f2a3b3dc0bcbd7408b3c05a84de844b6e371870394fb3fd6b86b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbcc3f80d4b45a1132ef8124911aac488afedf4bc303bca8c87d7c2e76223cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf32641c5e15f4dc1879ab2ed66d5d8e902f9d13af91a97f549c8f16088ba3e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f969b870baf8ce351d7dee13187b02ef4f277723537f962031621300315c6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d66a579ba8fc9e239c66882995cb7608c5dc1d036f4e5c6fd7eb129dbce9019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf18f2820c5e4d8067d97ae8e9217728a1a6cbd29bb3dbda0b29ed99e81d832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d59ea5cab72c5c5572c12f2571088a33f1f430cdfd4763fed0872b7d6513651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f20c2a444f5eebc7c8b5be23e70c55d7a2211ec6e4149d33a573dbd4aba7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2515be6dfd7e0d3bfc8a99f1f42bbd2e202fdfca48fc57bf1979184f91101b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8ee1154c4d43a1f6e5ca410a68a440ca92033ec9a1800c2222ecea1dd9a996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapRelationalTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a295cea4a7d7386be180ee264c6d9e3720dedd9f95d885fb440b5a2fc924c03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInputColumns")
    def put_input_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6e4fcc5f9878378c8c353adfebb8606619e77a83c10f60ce36486cff6d67ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputColumns", [value]))

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="inputColumns")
    def input_columns(
        self,
    ) -> QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList:
        return typing.cast(QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList, jsii.get(self, "inputColumns"))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArnInput")
    def data_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="inputColumnsInput")
    def input_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]], jsii.get(self, "inputColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29aa187cc2b681ecf5f41c65942a1e533b3eabfe76a757f9394b0cd4dc7e820d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceArn"))

    @data_source_arn.setter
    def data_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0348e3c22e6fc8a7815933f2995f1447ad5ed4ffe7ad6eb72527576bfd6f969a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99ea317673b512d0722d641de3d178e22b6a061abc00246ac3a8397460b943a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e232a2b14c771634ba18e3ae0f2c3b4b88f8d5ee5b409ea1f1d4423ed1abc73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b3b6d52f561a42c5bd5a71042342637dbf5343e34fc7a41c5bd5fbd3129c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3Source",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_arn": "dataSourceArn",
        "input_columns": "inputColumns",
        "upload_settings": "uploadSettings",
    },
)
class QuicksightDataSetPhysicalTableMapS3Source:
    def __init__(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapS3SourceInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        upload_settings: typing.Union["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param upload_settings: upload_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#upload_settings QuicksightDataSet#upload_settings}
        '''
        if isinstance(upload_settings, dict):
            upload_settings = QuicksightDataSetPhysicalTableMapS3SourceUploadSettings(**upload_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54dd1f3550f9977fba768ba34c1fa55d460247c5f2d02ab03fb3afe6d55ccaaf)
            check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
            check_type(argname="argument input_columns", value=input_columns, expected_type=type_hints["input_columns"])
            check_type(argname="argument upload_settings", value=upload_settings, expected_type=type_hints["upload_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_arn": data_source_arn,
            "input_columns": input_columns,
            "upload_settings": upload_settings,
        }

    @builtins.property
    def data_source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.'''
        result = self._values.get("data_source_arn")
        assert result is not None, "Required property 'data_source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapS3SourceInputColumns"]]:
        '''input_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        '''
        result = self._values.get("input_columns")
        assert result is not None, "Required property 'input_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapS3SourceInputColumns"]], result)

    @builtins.property
    def upload_settings(
        self,
    ) -> "QuicksightDataSetPhysicalTableMapS3SourceUploadSettings":
        '''upload_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#upload_settings QuicksightDataSet#upload_settings}
        '''
        result = self._values.get("upload_settings")
        assert result is not None, "Required property 'upload_settings' is missing"
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceUploadSettings", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapS3Source(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceInputColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class QuicksightDataSetPhysicalTableMapS3SourceInputColumns:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60ded08ad3275731c113fff1b819d7d42d64aea969c1f819e5d27ed26034e3d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapS3SourceInputColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f00568564f7e6b9e6b45dd6545519d4513637eea3a638541db708627aefa9af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7c557f0942f501e64ad3a30a3fa68c5f670d3faeae3146d6e44b3cd636911b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944724cf57009cbe1aed654cebef0e4aa616f9c680cd07e508a947c6ed630020)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01541b6194390651ea2714243a03de11372286efbe98daef7f20a22c076ea021)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe5876d6c2f0218bad16b94b789aa3c00e877b35f7e093bfa0d382c5689a104d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fd91560aeed433c8a0cc560613fd0c71d8e21a1962d713bcf885d61f7068a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f615a9c33ab0796544d04b1a3d842dd2bbe2f9143e4e72eb1a2095bafbcd929)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c62aaa5a3fb6523ba7d362e7015d47aec7b66d2d4247cb02a68c2e76b706f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94777eff3eb4e17034124a868e6bbbc13f6360791e7451b1e6de72a6ba6dbc7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21fb3bab8c840b033183547ee69d9d1a12a26ef708840d8d7c11de6526c7b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapS3SourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a57240f98f7cfe670380be7f911a4e9f84ad54a0aa0257d75185dbf8d5bff4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInputColumns")
    def put_input_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapS3SourceInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f997b96d8198ba06b25f34a08b01be69d2512bab7baf52f0969fa71df32ac29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputColumns", [value]))

    @jsii.member(jsii_name="putUploadSettings")
    def put_upload_settings(
        self,
        *,
        contains_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        start_from_row: typing.Optional[jsii.Number] = None,
        text_qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#contains_header QuicksightDataSet#contains_header}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#delimiter QuicksightDataSet#delimiter}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        :param start_from_row: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#start_from_row QuicksightDataSet#start_from_row}.
        :param text_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#text_qualifier QuicksightDataSet#text_qualifier}.
        '''
        value = QuicksightDataSetPhysicalTableMapS3SourceUploadSettings(
            contains_header=contains_header,
            delimiter=delimiter,
            format=format,
            start_from_row=start_from_row,
            text_qualifier=text_qualifier,
        )

        return typing.cast(None, jsii.invoke(self, "putUploadSettings", [value]))

    @builtins.property
    @jsii.member(jsii_name="inputColumns")
    def input_columns(
        self,
    ) -> QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList:
        return typing.cast(QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList, jsii.get(self, "inputColumns"))

    @builtins.property
    @jsii.member(jsii_name="uploadSettings")
    def upload_settings(
        self,
    ) -> "QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference":
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference", jsii.get(self, "uploadSettings"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArnInput")
    def data_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="inputColumnsInput")
    def input_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]], jsii.get(self, "inputColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadSettingsInput")
    def upload_settings_input(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings"]:
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings"], jsii.get(self, "uploadSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceArn"))

    @data_source_arn.setter
    def data_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2557d47d731feebcc8a4faaedac88d0916be812c717d2604897d154dd1d95197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapS3Source]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapS3Source], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapS3Source],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef425201d6d8964f0696dd28b6787a600221bd6dfff40d5d6ccef224f8e63cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceUploadSettings",
    jsii_struct_bases=[],
    name_mapping={
        "contains_header": "containsHeader",
        "delimiter": "delimiter",
        "format": "format",
        "start_from_row": "startFromRow",
        "text_qualifier": "textQualifier",
    },
)
class QuicksightDataSetPhysicalTableMapS3SourceUploadSettings:
    def __init__(
        self,
        *,
        contains_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        start_from_row: typing.Optional[jsii.Number] = None,
        text_qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#contains_header QuicksightDataSet#contains_header}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#delimiter QuicksightDataSet#delimiter}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        :param start_from_row: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#start_from_row QuicksightDataSet#start_from_row}.
        :param text_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#text_qualifier QuicksightDataSet#text_qualifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90f713f0cedde691720474f19e32a426d19e79e6ea43de86b55778ad15af210)
            check_type(argname="argument contains_header", value=contains_header, expected_type=type_hints["contains_header"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument start_from_row", value=start_from_row, expected_type=type_hints["start_from_row"])
            check_type(argname="argument text_qualifier", value=text_qualifier, expected_type=type_hints["text_qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains_header is not None:
            self._values["contains_header"] = contains_header
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if format is not None:
            self._values["format"] = format
        if start_from_row is not None:
            self._values["start_from_row"] = start_from_row
        if text_qualifier is not None:
            self._values["text_qualifier"] = text_qualifier

    @builtins.property
    def contains_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#contains_header QuicksightDataSet#contains_header}.'''
        result = self._values.get("contains_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#delimiter QuicksightDataSet#delimiter}.'''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_from_row(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#start_from_row QuicksightDataSet#start_from_row}.'''
        result = self._values.get("start_from_row")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def text_qualifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#text_qualifier QuicksightDataSet#text_qualifier}.'''
        result = self._values.get("text_qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapS3SourceUploadSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfb7fd361b75e0f64833f90359529db63687f967fa602a76b702343b5f63e34e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainsHeader")
    def reset_contains_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainsHeader", []))

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetFormat")
    def reset_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormat", []))

    @jsii.member(jsii_name="resetStartFromRow")
    def reset_start_from_row(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartFromRow", []))

    @jsii.member(jsii_name="resetTextQualifier")
    def reset_text_qualifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextQualifier", []))

    @builtins.property
    @jsii.member(jsii_name="containsHeaderInput")
    def contains_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containsHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="startFromRowInput")
    def start_from_row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startFromRowInput"))

    @builtins.property
    @jsii.member(jsii_name="textQualifierInput")
    def text_qualifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textQualifierInput"))

    @builtins.property
    @jsii.member(jsii_name="containsHeader")
    def contains_header(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containsHeader"))

    @contains_header.setter
    def contains_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bfd2d3e664a5b2ae5eb8bdad7ad04be466e89d0c18e0af917ca3d33836a067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containsHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4be5a815573f37a7c466e6b2d927d56d3524175ffdaed1364f64fb8ca3eece0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7691709a0c73943619ed43bb89efd5e999bd70656d5f88d3c6b48b451b0c10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startFromRow")
    def start_from_row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startFromRow"))

    @start_from_row.setter
    def start_from_row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ca41f2a115ccde5a535f51edb2a42c76488b497b93d73422c25f88f6476128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startFromRow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textQualifier")
    def text_qualifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textQualifier"))

    @text_qualifier.setter
    def text_qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6777b6c935333c8a83a57ea9d7d37cb883fa9836dc509041f3b526a39b4dd8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textQualifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1278f9372d6693532085ef26b1ce3fd85c9e695de3d08500bcc838a68e11e426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshProperties",
    jsii_struct_bases=[],
    name_mapping={"refresh_configuration": "refreshConfiguration"},
)
class QuicksightDataSetRefreshProperties:
    def __init__(
        self,
        *,
        refresh_configuration: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param refresh_configuration: refresh_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#refresh_configuration QuicksightDataSet#refresh_configuration}
        '''
        if isinstance(refresh_configuration, dict):
            refresh_configuration = QuicksightDataSetRefreshPropertiesRefreshConfiguration(**refresh_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d09e6020455554317abb88130a39e5b223c57830a61cf8d8b2db0fd7c7db602)
            check_type(argname="argument refresh_configuration", value=refresh_configuration, expected_type=type_hints["refresh_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "refresh_configuration": refresh_configuration,
        }

    @builtins.property
    def refresh_configuration(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfiguration":
        '''refresh_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#refresh_configuration QuicksightDataSet#refresh_configuration}
        '''
        result = self._values.get("refresh_configuration")
        assert result is not None, "Required property 'refresh_configuration' is missing"
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfiguration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRefreshPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6756e6e0b31a26b09859d42ab105658d54893ee4fed4db87f1b9a6608e544ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRefreshConfiguration")
    def put_refresh_configuration(
        self,
        *,
        incremental_refresh: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param incremental_refresh: incremental_refresh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#incremental_refresh QuicksightDataSet#incremental_refresh}
        '''
        value = QuicksightDataSetRefreshPropertiesRefreshConfiguration(
            incremental_refresh=incremental_refresh
        )

        return typing.cast(None, jsii.invoke(self, "putRefreshConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="refreshConfiguration")
    def refresh_configuration(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference":
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference", jsii.get(self, "refreshConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="refreshConfigurationInput")
    def refresh_configuration_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRefreshPropertiesRefreshConfiguration"]:
        return typing.cast(typing.Optional["QuicksightDataSetRefreshPropertiesRefreshConfiguration"], jsii.get(self, "refreshConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSetRefreshProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edcdd40aa1f093709965638057ff4828d2176396cdcf2806dd4d05418d96de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfiguration",
    jsii_struct_bases=[],
    name_mapping={"incremental_refresh": "incrementalRefresh"},
)
class QuicksightDataSetRefreshPropertiesRefreshConfiguration:
    def __init__(
        self,
        *,
        incremental_refresh: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param incremental_refresh: incremental_refresh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#incremental_refresh QuicksightDataSet#incremental_refresh}
        '''
        if isinstance(incremental_refresh, dict):
            incremental_refresh = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh(**incremental_refresh)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a47a6bfafa9c589ed4fc229e42650741b930b7dc8f377392f9f81606f45d043)
            check_type(argname="argument incremental_refresh", value=incremental_refresh, expected_type=type_hints["incremental_refresh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "incremental_refresh": incremental_refresh,
        }

    @builtins.property
    def incremental_refresh(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh":
        '''incremental_refresh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#incremental_refresh QuicksightDataSet#incremental_refresh}
        '''
        result = self._values.get("incremental_refresh")
        assert result is not None, "Required property 'incremental_refresh' is missing"
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshPropertiesRefreshConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh",
    jsii_struct_bases=[],
    name_mapping={"lookback_window": "lookbackWindow"},
)
class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh:
    def __init__(
        self,
        *,
        lookback_window: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lookback_window: lookback_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#lookback_window QuicksightDataSet#lookback_window}
        '''
        if isinstance(lookback_window, dict):
            lookback_window = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow(**lookback_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f4600e5902cdf03ec181044b68dea0f6e90f1f5c13476a8811d201ef54ccca)
            check_type(argname="argument lookback_window", value=lookback_window, expected_type=type_hints["lookback_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookback_window": lookback_window,
        }

    @builtins.property
    def lookback_window(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow":
        '''lookback_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#lookback_window QuicksightDataSet#lookback_window}
        '''
        result = self._values.get("lookback_window")
        assert result is not None, "Required property 'lookback_window' is missing"
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "size": "size",
        "size_unit": "sizeUnit",
    },
)
class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        size: jsii.Number,
        size_unit: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#size QuicksightDataSet#size}.
        :param size_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#size_unit QuicksightDataSet#size_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6afa72fd3e4f38b4bcceec376887e476f47af9c634d621e4dddd4be5f33dc51)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument size_unit", value=size_unit, expected_type=type_hints["size_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "size": size,
            "size_unit": size_unit,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#size QuicksightDataSet#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#size_unit QuicksightDataSet#size_unit}.'''
        result = self._values.get("size_unit")
        assert result is not None, "Required property 'size_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cd9a9bb936fb79d12229c30be310c6679374b2b59c90d19583a41e05d72ba05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeUnitInput")
    def size_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a1a1eb48de5f266af95e270613a8f6c35347d5ca7f38659fc4f8537b0fc1cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b54252b53e15104eda1feb7169dab04805f79954dd05ab0d5e8d7193319ddc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeUnit")
    def size_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeUnit"))

    @size_unit.setter
    def size_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576776b4b0a490043e93f3819ef911edc298f40edb6e973ec8cf7de92967092a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2f9ca216b74ca2dbe383472e9ce9d8aeb41acf69b136b3aaabd0efabac1a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe963a53d6969936d5634b25ff490fcf947528f2a4b4c8d877219a2fa7bb5909)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLookbackWindow")
    def put_lookback_window(
        self,
        *,
        column_name: builtins.str,
        size: jsii.Number,
        size_unit: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#size QuicksightDataSet#size}.
        :param size_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#size_unit QuicksightDataSet#size_unit}.
        '''
        value = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow(
            column_name=column_name, size=size, size_unit=size_unit
        )

        return typing.cast(None, jsii.invoke(self, "putLookbackWindow", [value]))

    @builtins.property
    @jsii.member(jsii_name="lookbackWindow")
    def lookback_window(
        self,
    ) -> QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference:
        return typing.cast(QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference, jsii.get(self, "lookbackWindow"))

    @builtins.property
    @jsii.member(jsii_name="lookbackWindowInput")
    def lookback_window_input(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow], jsii.get(self, "lookbackWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3f15e5557b291505a7c9e7651e8188de49c892440dc6a842bee357096f0de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff55cf222b51b6c7d43b7875cbb8703a5c4d39b913c1c91f458098ee99878424)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncrementalRefresh")
    def put_incremental_refresh(
        self,
        *,
        lookback_window: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lookback_window: lookback_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#lookback_window QuicksightDataSet#lookback_window}
        '''
        value = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh(
            lookback_window=lookback_window
        )

        return typing.cast(None, jsii.invoke(self, "putIncrementalRefresh", [value]))

    @builtins.property
    @jsii.member(jsii_name="incrementalRefresh")
    def incremental_refresh(
        self,
    ) -> QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference:
        return typing.cast(QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference, jsii.get(self, "incrementalRefresh"))

    @builtins.property
    @jsii.member(jsii_name="incrementalRefreshInput")
    def incremental_refresh_input(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh], jsii.get(self, "incrementalRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d92282786058b304069fe3121c6ebd7dc04f6d6e6caf2cc4fb68a5c56834f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionDataSet",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "permission_policy": "permissionPolicy",
        "format_version": "formatVersion",
        "namespace": "namespace",
        "status": "status",
    },
)
class QuicksightDataSetRowLevelPermissionDataSet:
    def __init__(
        self,
        *,
        arn: builtins.str,
        permission_policy: builtins.str,
        format_version: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#arn QuicksightDataSet#arn}.
        :param permission_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#permission_policy QuicksightDataSet#permission_policy}.
        :param format_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format_version QuicksightDataSet#format_version}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#namespace QuicksightDataSet#namespace}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a76ce65afd36b8266cf3856c84acbe7b2eae1377ef1eee1f2dedaf67a260c8)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument permission_policy", value=permission_policy, expected_type=type_hints["permission_policy"])
            check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "permission_policy": permission_policy,
        }
        if format_version is not None:
            self._values["format_version"] = format_version
        if namespace is not None:
            self._values["namespace"] = namespace
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#arn QuicksightDataSet#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#permission_policy QuicksightDataSet#permission_policy}.'''
        result = self._values.get("permission_policy")
        assert result is not None, "Required property 'permission_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#format_version QuicksightDataSet#format_version}.'''
        result = self._values.get("format_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#namespace QuicksightDataSet#namespace}.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRowLevelPermissionDataSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRowLevelPermissionDataSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionDataSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33dc7e946e7be0507eb2b56e86510ff13d26e4e7b9920055cfbbadc3a36b47d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFormatVersion")
    def reset_format_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormatVersion", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="formatVersionInput")
    def format_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionPolicyInput")
    def permission_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea1cd91e6a704259693dcca9d7fdbd7e3486da2e1dc412edd58426681e3532b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatVersion")
    def format_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formatVersion"))

    @format_version.setter
    def format_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70142bd38a4c42cb7354634376ec3ce0d426c652f89989234f0fe6808d8d3615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f51ce6dc649102d35fed98d84013a2bebde4e59d483d39e7288f528cd05a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissionPolicy")
    def permission_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionPolicy"))

    @permission_policy.setter
    def permission_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc037893a2a82d9cce1885a1eb5abfd581351a3125170d13f777c989c82d9f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6be64390543edd0ff1be293e2a1adeec348040e89e0f1a14aa501d37f9f0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRowLevelPermissionDataSet]:
        return typing.cast(typing.Optional[QuicksightDataSetRowLevelPermissionDataSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRowLevelPermissionDataSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70f4c75f7c0046cdb0ba8fd0e8dd1e456d79b579d22bed7434b085841275ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfiguration",
    jsii_struct_bases=[],
    name_mapping={"tag_rules": "tagRules", "status": "status"},
)
class QuicksightDataSetRowLevelPermissionTagConfiguration:
    def __init__(
        self,
        *,
        tag_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules", typing.Dict[builtins.str, typing.Any]]]],
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tag_rules: tag_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_rules QuicksightDataSet#tag_rules}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332f0a253d8eb0809bff1117fad61c4c811219c051686a25e60ec0c1dd06b76f)
            check_type(argname="argument tag_rules", value=tag_rules, expected_type=type_hints["tag_rules"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag_rules": tag_rules,
        }
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def tag_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]]:
        '''tag_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_rules QuicksightDataSet#tag_rules}
        '''
        result = self._values.get("tag_rules")
        assert result is not None, "Required property 'tag_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRowLevelPermissionTagConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdd423c6150ae7d32fe8b75dda0dbc9c694af84fce63c589ed826c89a88971d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagRules")
    def put_tag_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf6e16db1bcbb23babf73c4483845a49563e80db3dda7aa22f0b1dfa1d2cbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagRules", [value]))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="tagRules")
    def tag_rules(
        self,
    ) -> "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList":
        return typing.cast("QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList", jsii.get(self, "tagRules"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagRulesInput")
    def tag_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]]], jsii.get(self, "tagRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd83682e379fd49f61179fdaebd99a9d57df7eeb7f1c8f416e173c5dd55579cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration]:
        return typing.cast(typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e15ea5d5d656e9f36ed22ecadf0bb792bd38910f7eecfd02f7229301af75f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationTagRules",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "tag_key": "tagKey",
        "match_all_value": "matchAllValue",
        "tag_multi_value_delimiter": "tagMultiValueDelimiter",
    },
)
class QuicksightDataSetRowLevelPermissionTagConfigurationTagRules:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        tag_key: builtins.str,
        match_all_value: typing.Optional[builtins.str] = None,
        tag_multi_value_delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_key QuicksightDataSet#tag_key}.
        :param match_all_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#match_all_value QuicksightDataSet#match_all_value}.
        :param tag_multi_value_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_multi_value_delimiter QuicksightDataSet#tag_multi_value_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50743f4f00ed09932897e0717887c10614d87f21823cfa3a4e334392b6b536d8)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument match_all_value", value=match_all_value, expected_type=type_hints["match_all_value"])
            check_type(argname="argument tag_multi_value_delimiter", value=tag_multi_value_delimiter, expected_type=type_hints["tag_multi_value_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "tag_key": tag_key,
        }
        if match_all_value is not None:
            self._values["match_all_value"] = match_all_value
        if tag_multi_value_delimiter is not None:
            self._values["tag_multi_value_delimiter"] = tag_multi_value_delimiter

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_key QuicksightDataSet#tag_key}.'''
        result = self._values.get("tag_key")
        assert result is not None, "Required property 'tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_all_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#match_all_value QuicksightDataSet#match_all_value}.'''
        result = self._values.get("match_all_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_multi_value_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_data_set#tag_multi_value_delimiter QuicksightDataSet#tag_multi_value_delimiter}.'''
        result = self._values.get("tag_multi_value_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRowLevelPermissionTagConfigurationTagRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fa606d7e5dd40b4059407a2ec43c8eca7d8c0111fd49308d459011a05c477fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d76764e0b6dd338c6b92c01eeac51828e27f1122ad90b650ee87b147d2a136)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e369916cb2bb0b837d77ba615fb81e6eae33232022c621ab96376b4dcb9e9ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__613b49f334c9335e56ef33056ba947da86c0cc5a97150ed72c9e287229e6191a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a73715db7ca6cf956216a7940853563efced2bc03936ea7f92b8ff0b49bd33c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d70bdc564587ebd4225e4436decf1920651bf0404d9773e2e49ce257b2fe84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a257684253f385ae9e61da103567d6b9300d0e3a803c33bbfaef2b5af1b7b9db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchAllValue")
    def reset_match_all_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchAllValue", []))

    @jsii.member(jsii_name="resetTagMultiValueDelimiter")
    def reset_tag_multi_value_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagMultiValueDelimiter", []))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="matchAllValueInput")
    def match_all_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchAllValueInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagMultiValueDelimiterInput")
    def tag_multi_value_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagMultiValueDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f693e280b4f3cfd8d1019078bc34e01f91fc174380667c25a4620ebd64cdd6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchAllValue")
    def match_all_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchAllValue"))

    @match_all_value.setter
    def match_all_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a659ad9e68c687c7545511435422327c4d5f2781aa8dfa13092f4ff6ea3167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchAllValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8640bb99c74e52c4440d41a816113ac9cf45a0270be7f2ca4f8db8d6d2ecc874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagMultiValueDelimiter")
    def tag_multi_value_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagMultiValueDelimiter"))

    @tag_multi_value_delimiter.setter
    def tag_multi_value_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f0780f61201466b294dfb2ebc1bbdcedbfc70467de572eec6c0eb6e29addff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagMultiValueDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9972135129a574e54a9fb51153288a35e748c766d127bac45754d0697f466a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightDataSet",
    "QuicksightDataSetColumnGroups",
    "QuicksightDataSetColumnGroupsGeoSpatialColumnGroup",
    "QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference",
    "QuicksightDataSetColumnGroupsList",
    "QuicksightDataSetColumnGroupsOutputReference",
    "QuicksightDataSetColumnLevelPermissionRules",
    "QuicksightDataSetColumnLevelPermissionRulesList",
    "QuicksightDataSetColumnLevelPermissionRulesOutputReference",
    "QuicksightDataSetConfig",
    "QuicksightDataSetDataSetUsageConfiguration",
    "QuicksightDataSetDataSetUsageConfigurationOutputReference",
    "QuicksightDataSetFieldFolders",
    "QuicksightDataSetFieldFoldersList",
    "QuicksightDataSetFieldFoldersOutputReference",
    "QuicksightDataSetLogicalTableMap",
    "QuicksightDataSetLogicalTableMapDataTransforms",
    "QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsFilterOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsList",
    "QuicksightDataSetLogicalTableMapDataTransformsOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsProjectOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference",
    "QuicksightDataSetLogicalTableMapList",
    "QuicksightDataSetLogicalTableMapOutputReference",
    "QuicksightDataSetLogicalTableMapSource",
    "QuicksightDataSetLogicalTableMapSourceJoinInstruction",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference",
    "QuicksightDataSetLogicalTableMapSourceOutputReference",
    "QuicksightDataSetOutputColumns",
    "QuicksightDataSetOutputColumnsList",
    "QuicksightDataSetOutputColumnsOutputReference",
    "QuicksightDataSetPermissions",
    "QuicksightDataSetPermissionsList",
    "QuicksightDataSetPermissionsOutputReference",
    "QuicksightDataSetPhysicalTableMap",
    "QuicksightDataSetPhysicalTableMapCustomSql",
    "QuicksightDataSetPhysicalTableMapCustomSqlColumns",
    "QuicksightDataSetPhysicalTableMapCustomSqlColumnsList",
    "QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference",
    "QuicksightDataSetPhysicalTableMapCustomSqlOutputReference",
    "QuicksightDataSetPhysicalTableMapList",
    "QuicksightDataSetPhysicalTableMapOutputReference",
    "QuicksightDataSetPhysicalTableMapRelationalTable",
    "QuicksightDataSetPhysicalTableMapRelationalTableInputColumns",
    "QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList",
    "QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference",
    "QuicksightDataSetPhysicalTableMapRelationalTableOutputReference",
    "QuicksightDataSetPhysicalTableMapS3Source",
    "QuicksightDataSetPhysicalTableMapS3SourceInputColumns",
    "QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList",
    "QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference",
    "QuicksightDataSetPhysicalTableMapS3SourceOutputReference",
    "QuicksightDataSetPhysicalTableMapS3SourceUploadSettings",
    "QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference",
    "QuicksightDataSetRefreshProperties",
    "QuicksightDataSetRefreshPropertiesOutputReference",
    "QuicksightDataSetRefreshPropertiesRefreshConfiguration",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference",
    "QuicksightDataSetRowLevelPermissionDataSet",
    "QuicksightDataSetRowLevelPermissionDataSetOutputReference",
    "QuicksightDataSetRowLevelPermissionTagConfiguration",
    "QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference",
    "QuicksightDataSetRowLevelPermissionTagConfigurationTagRules",
    "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList",
    "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference",
]

publication.publish()

def _typecheckingstub__77c5ca157865a70dada29aab6aff26e9cd2168c9d89e85ca1bb016273bf9f892(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_set_id: builtins.str,
    import_mode: builtins.str,
    name: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_set_usage_configuration: typing.Optional[typing.Union[QuicksightDataSetDataSetUsageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetFieldFolders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    refresh_properties: typing.Optional[typing.Union[QuicksightDataSetRefreshProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    row_level_permission_data_set: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionDataSet, typing.Dict[builtins.str, typing.Any]]] = None,
    row_level_permission_tag_configuration: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionTagConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4cf05ccf2f787ca8171d44491e89d78875fc75e56ece3b9b22559afdb10345cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afec8b5b30c1275f8a5dac1492caa2c1a50f937fab23c1587a3c8410a363d45c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2b8b5d0912d1fa41f512c5fb68e43beef1394f1e9d1e986fe966e83944670d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9905c18bb2f6452e3af351401e9fc7be5871d1a0e1cec974fd5dac11fc0eadf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetFieldFolders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421b93c1bc609d0f1116e6dd6d62621c6e984db3a7173ee5e7e15f89b18238ad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cd495ad713677230ba16b024c44dce4456790781cb308734fa070a78ce71f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78187e4272733357db3abf893a22d49371774caa983b96c52f3bf2d811e2425f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d89222fd97ad188843b464cb2356e093323cee8e5e5d0d20eb4fcfacc24e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00a986fd77dbc18cbe5d5350d7ef191a557812655d32c4d18676bb0ea59c93b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782bad3d629faf9f18d4b5a97b3e5e30a1e8b32954104a80de0218ddc5878675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791aa59219100b68fafe9c8ab54fa42eed5afd6cd3165234f0dd92c62e1816f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a118f2faa80cc78b2579bb260710a9c9cf0de22d942032d6809d162e060c35b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1596d0986886654f4ade60e19ecf6d7cd7f45fdacd7db9c185ad68cdaf6801de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beab084d3667114395a42a1482a2372b45f42356cdb84786029de016b5591b65(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11ae55903bc252658f859fccad668ff9a9c8978e33c93ac515ccdbe5cf4bc4d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac2418bb954011b35dfec5bd02a6994b950ab24539b02ee0bed1c5afa03c8ec(
    *,
    geo_spatial_column_group: typing.Optional[typing.Union[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fe43687acb7c8c3b548a814d98dcf89f56c4091ece9accf9bb3a5e01ae0c44(
    *,
    columns: typing.Sequence[builtins.str],
    country_code: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a4be56758b8c9cfb22f4ca8ce01d30156e02148481875f25166b8182114c16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d194e90fc695d37cd6b063b68fbd984bd715af36691468c5d91d669e8ad4844(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f344767c9bb4d29cb5de5946711888c9bf3d540fb07a6b580e5a276c699761da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341e27bc2281a834ba729edb4a906d3c5343c298fe8ca014b2bf6e094113d158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be6ee03a4ebb63e4fac5e85af4fbe595abde4c3edf77ee85e0cc33cd08f6136(
    value: typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48422fa53512e05d361fe0f873fa759ca74e005546a5f96bbb0a142f2191f5af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d34a220a4980f9c61d9f972ccc589ce3660c57fc5526e60edb4d4fdc48f221(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946f5ae0d31edcfb7884f0fa4ad33d9fa4e8cdd00a41498eb9fb4845159553c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f014bc98a3804955ad7bbbd9745b3dd7dcf9c66262ff3f099e1a874d97df556e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd706cbe540c128b3f59a0c5b5c0d7b119d5c414cb78a6781218017d00c9d5b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90817c36e318b31bbb4190621a648fdccf0635528c470829b93e40fb139522ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d613e1ac5e6644b0513e21c13edf0a3fe41daf4fc18fda31fbb3fda6f1106d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c44be3a360a3dbd880204e71ea5b124f86860de6b2d8240ba51d40e572dab0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb96463707093275e17a0e8e245db98c3e814e8fd70605115e1822dc9d15c94d(
    *,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f8437919ec63bba0a1611d0c541ea4dc43696ea8582ea40848e053251eec98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7cb405743e53a800d2e87bdbc72280a8db2db2c7ac9c40a0bb7413b998676b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37de9703987e158afdeec31a19e83da799b0dbdde35fdceb6d4b050b6670349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2366b3b64f778734c9fde0b8960db8f1f83e1112afee9f8450e7e1b9ddfb1480(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813ba1d116fd1fd77a18448052702bf7be98917a32da16cf5d9920de4f2665b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3a7b85426d46c94504bc4b3a247af3bb821383841cbaceee86a073958da3c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339ac9105b76149d9fef788524f8500795e82aa806a7b347dc28e49dfc5b90fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8036c14f210c2d5a1b8d12da493088ecd258d237d762a04677065594d51c4a8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1150ee3fa7e33161fa1b38ce46de1bae24cb7a8f83d59335178e827b8c8d0c6f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d060a1e9c05558fdee277385799786dda5072f7125e51130eada7b512d89b0c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7185323eac0f6e3c41c903bbd266360f9b96f79fdf03da8ee7dec323e91f2420(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_set_id: builtins.str,
    import_mode: builtins.str,
    name: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_set_usage_configuration: typing.Optional[typing.Union[QuicksightDataSetDataSetUsageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetFieldFolders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    refresh_properties: typing.Optional[typing.Union[QuicksightDataSetRefreshProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    row_level_permission_data_set: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionDataSet, typing.Dict[builtins.str, typing.Any]]] = None,
    row_level_permission_tag_configuration: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionTagConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6967abe9adbf226f0b84cd7c2982e74d1ebaa383970831f162d801ca3933c82(
    *,
    disable_use_as_direct_query_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_use_as_imported_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650d85f682ff695c9bc49bcd37154cf0e83ae1f4ebbbcfee6d9f24a6e4cd4faf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875218a502f8c75f1a3cdb902e26758d0a60b110381f87176141fef9b28db28a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55078103845c8fd396475aacb4a9562209134ce32b0dd1cae965bf2e349675b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9280965192104159dd8606f99533991bd67f278149ee7561a5a660fd2819c5(
    value: typing.Optional[QuicksightDataSetDataSetUsageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2a4cbcb9e260c89d2ac2c4d61b293dc21d4f5ec18283c40e19566ae7a14b51(
    *,
    field_folders_id: builtins.str,
    columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c0ac95dcacb0e4d9f73e03ea5f387b18409ad30c3f1b5ec689f78480b101a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1250642eb9e9d8edc83e177a30e4cdd80e8e2c939c23668c2e4752e3c9817ddb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d74b62048cedd30396e5cbf886000bf516da492531d7897b5104cd6ac3df4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4e8692bfb4de9eac3e715b85f23841d2dc32bffbb35c26c00672b3c4c1add0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351c8e61536cbf505a25a956b062c4453e5573d4f33e619c5958e72ec30a1e27(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3c73a487a99dbd0de1300e62d3bc8a7161bfcb43ee4f859885d359d6e06595(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9581d4eea622162aceb51028dee1fb10a1eef1ccf50684858a38306ab6be732b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b3157aed97a3c6390edeccb5f3e36a97e622291611615a1c6d953a0ada406c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295a57a1474721e73bfba0a938362950a0b7c1b0b78269ba512e940a6f9dcad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396e4ed2f8f36f3a8e334be4b621bc88aceaf166da6335a0a9461a2e544af075(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319ce5a2498a85c4d9808dccf478bb4c8b52b6bc0929482b2414bb5f2dc5b969(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45bee23ff562f3394bd9f025a43021b541bbe20f47850e3a49cc77073e52c27(
    *,
    alias: builtins.str,
    logical_table_map_id: builtins.str,
    source: typing.Union[QuicksightDataSetLogicalTableMapSource, typing.Dict[builtins.str, typing.Any]],
    data_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6854433b878e0767b928045d75605db15fe463316aeb81b3e3e4b638244e884c(
    *,
    cast_column_type_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    create_columns_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    filter_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    project_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    rename_column_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_column_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    untag_column_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dff61c751823f90ac2d56f8cf3b84eb80fa7461ce90bb76f0615113a62906d8(
    *,
    column_name: builtins.str,
    new_column_type: builtins.str,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa0dbace35f69d6ad55ef180fa7074af5035204cf89ba37c56439b351bdc103(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117d536c5c3b0c4a2ae14701be27eced8387eec0543df802c0bff38659589b64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3f7b06f3c5bdea992494b4b56e7454cab11487845fa2910e19c6a4f5958a56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7dc38ab3c828b50023a542528f68bc36ae53cab667c83489c60a411765c964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2550000c9685dc8951a2a66a5052125d1668a7e1dfec39a6c8e2f5d7c8ae9fe3(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd966ec7186fd449c02932e4d85cd6db005db55cdaebd80c582227de8e4d473(
    *,
    columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5f0d3475415e138c014adb0b77b12c86aab22dd68e7a5964b7a0e06e340df7(
    *,
    column_id: builtins.str,
    column_name: builtins.str,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d082942300d96ecced0ad0e67468d629b3e687ebd2590376600b9155551a92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b497272ce4402744973a48bb9fa1f44c1c47babda341d1133ab48a1b4843ec55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ed22c0699fff9b0ab03256e6630a30d22bd223bea420248c14fe4711ce8e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed36cfb1a4f02b3dc945bf594930a6410e7f6bed6cfc21afdeeefe408bf238dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f78d9f577ef2598c6c6ba541bff3dbfc2831f6f87be57e043c63bc0963c9df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7615afa31f17ac979f9928d1a6bc5948d994a9cd0c2c6835de7e058dacf4f3a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aa93d91f2a1a2283dc9f8b5c3bbbf8a8a77afadce7ea989b6857aa1a3012bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c406652b3bf56a27ff343574030ca5bc171c7825161e5ad9c0909bc54681afa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce917b23c75ed3c87ada8c86ae9147d1453f8f32162cbc639c57fc993d49d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a9d64a705f8736be9e499fc45bf8f350e26b70a342424bf54c379bdf013021(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f3caa993d96f7ab491119d8fae685fcaf9b61e5024445d09f746601ca20ad8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba93d993c1607f8d0998f0f3d473e5c9dac9f13bce8907f95b6f33a97c79c2f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb79759213c15dceaf0bd0c3057c038c761d40b24b4c0f7616794c393974736(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbe0dbc8fe76edfc0f2ec6ae7f259009f750c23d6c3bd01786d33c4c42a5028(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846a7f09be22680efc23b4b509c60e179e8b2f21a7a94505fb254a05c4fbad28(
    *,
    condition_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb9309c6bdc9f44b934adae89e88a2234346b27adcbc70051ff20c48b69cac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2170cc0376be8877823aee83bb1a4cf960375bf9debb71edebdea8fb89d845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de86c6319b720d0ac388bffb384725ef5dd3c307ff21057386fa37926894ed73(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01555b0e1471820af099a95796ee7f4c02eab5008247307990dc1cbe65abdbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4237cb93ae9bafa5859ae80ddeacf46bb616ab87b49c4747f9837c3ce4f9f7c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7764b0f13f330b34f88017e8eb1d8fa799ef976d47e7d70993c92f737738d0b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5909e415954e94c4ee2c504b5cc130b37232ffb808764068bd4a9f2da371ae2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72d1e6c16e528420f734aaaf4edc5924eb030d400bfe5291846de348b986b6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0211a4b03e91e60009b11c8c09a330815c143a081c304d2316678ddf33fbffe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23137613e4057b8bb2b053f0fa34579e59906fa9229c4690d1fc4d921f238d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c578162b7f34b6d8073af5ced43a1a5b651d3042935d2b46a32f5ef7522e043b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc12d7ec78867d14b64a4300d003c58fa3baa27ec2e2dec7a083f1aa142068cd(
    *,
    projected_columns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c272ea8152512fb91216133b0f07e1b591b196696632a0c9db227058fe6634d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1851c97c75abab2002ba768a9604aa96df40a368ee09d9237643c5dc2567f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c23ddabd0e6faa881a933019a250cc184d1f4bacbfaa203688292acbfc7553(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375f79853a8be9579cc4059c7c19a6e59d00284709a2aeaffdf0c1ea6b5cc2ae(
    *,
    column_name: builtins.str,
    new_column_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1023703c214324bac7305d0ecaaede9c167e0b0b2816f93cec075902c45f8972(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02358bbdcea20bbd92f57f9044851c7148992f3ab87a01ff199ab0f74c25e472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3e3732a8f670cddf67f7fb92836f938110ff1e209d300d7f05d4711823230f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed5243f6af96637cc1e9af04f7fed5a70e9636537f69ca04f8771ddb6c37849(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d831f19201cb9b981d4da2b7d4ed750843738513687042b962f38d92a11bee5(
    *,
    column_name: builtins.str,
    tags: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b0c1d7d9e2ec825824a7dbca3cca2d412951690dd8c762b57c12174355d6d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d99469c99e19f8e5f57cf42c7ee35fa82c0265f5071723104710d257507c163(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214aedd14840070006a79ea4a434913332ed7ba0f2fd120d49f26e60be098d81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8ac30abe52fc0a38d41c9f1ed114f8c4d711c88be77f0b10eab736a2348627(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb4a2d294c93f28134b506f96f7ef167e846205c0d08545df1a936993668a96(
    *,
    column_description: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription, typing.Dict[builtins.str, typing.Any]]] = None,
    column_geographic_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d2945ada057afe460af94cd7b35d97ddb760a3928e96f74588dda5286a789d(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5c791fa6bc9128815b2a30868b725d5c5b385dac5e9168738a2487a97b1b9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdecb059779cfa170859078d42a09967dba351516139b0d8eb2c6958ea2e1d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb02fcbb8215171699ebb0fe1bb212bd741237ba90d8ffedfedcf1fc28198109(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790d6bcd9d43a63aa94c6eee7f9d18c1891138e753a55ae04232c44e6d2851a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7809e352b8ff534a5637f8285170735ccc0c9ee271c99d060518ccf4936b39c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa04b58ed4e491df0ed21e685c128b81f2dd5134459207dd4b581ee3435304c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439c2558ddcf992c2555b5bf7eec5704f41ddbbf8db2c8943db5728b1e41c970(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3654c31f524ea778bcde4890054b5bb020612cb557c6c1c292f03fb7272867b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d031f36e5e0f82ca40bbdc494dace47e4a65bd470f9c9bf01143ab6af739fd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4f51ea5b80e9e46a436604ca0425e917638b01912e9cef6c995a74ea4f0c73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e73397f205e8024ba999168e8372d896691b657eed40306010714d2b7d3f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cec1b733bf91b926c8ad8648b95c63b8e996b3c98ee03c67c83c2ca048689ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee11deb8904f5528e6a3a1040fe71cc90e0296e6a46b3062bd809993ac596d5(
    *,
    column_name: builtins.str,
    tag_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5b78b48f713909f37d5f3bda610cd3368985652b2cc8bf6285989d4ef87af4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d388e9b6c2e6ba1b77d6eea21d68d8ba55cc0738b4a4c469bc86a21963e087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938cad8c76ec4901446d0dd21fa004873f807ebbbe6597539975cdf8b7baecdf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa4eafdf48ef7b0061268a62257dbb9f20af53b9aeec17be7d00399c54be521(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8a8e7d2ad37d4214541f5634fca28b6bf23f377c136318bbd8b0b5c02b2d7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed30859a5c1ba93e5ed9d73cf72bf7cd11d8f956b147e3594e8e2fd7de557521(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4cb71b9c4cc0bd8bc7ea4b498776f1b1d6e6825320d8e884482a1440653e559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc786c28409cb5f28f9f67ce57c941d602f7b28dce12b6cd8237faa2aaee3cc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dce285fc113e81003b183dcac890dd34a240954bdfae16231f09761d3574d6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec94d83c37936ad87d5d611a9eb574fc9081e443d50b4f836dde65035556726(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134015423020dabd208a573a46d38488035d2cfe0265fec90361e46433f40680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e246c63f006a4fdbe6578b5efcaa5905e292dcc06591ef24ac44eaf9637b76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4c335c1fb50d329e5eccc33913da52b8a662a237b593e39128008008a3c556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32f38dc2f28584ab778aa0585269c7ce9fc1d08511ea99704fa7e87583f5dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fb9f7a0185fbc71ee6b364b5e5bdecea051fc4bd09adbd0a33f305b2f1826b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94144f6658501eb3df24ca0ab137b2c6a6b908a9757f2b5d649210cabbfc3554(
    *,
    data_set_arn: typing.Optional[builtins.str] = None,
    join_instruction: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstruction, typing.Dict[builtins.str, typing.Any]]] = None,
    physical_table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ed6d026567d6160c778408b2fa0a1c70ae95f716bd97f3eb58b297fcf6a30b(
    *,
    left_operand: builtins.str,
    on_clause: builtins.str,
    right_operand: builtins.str,
    type: builtins.str,
    left_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    right_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8e5bead492084f09d06c4a298fe36c8af9952f645ddf925e31e5875d9eaad4(
    *,
    unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f594c7735ee519fded16d4e8fbd01fe8c126129927abbdd68423eb4a223c1e17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158613f3504d727f39330c8143a392d38f4a9ce3dfabdf3bc5700e6df4284327(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8388770bad05504b76ed3491e3781d5022d4a6aa8753f6bc243dd21f048131e0(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9cef5a8dbf227c5bf324c3ce14bb9ba2380bd31c51eef221a65a509a29ca6a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15910d901ab10c1e9a2ba12eda91e7283277615631ff042933344497ca6d14d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c18b72c521a74f6b4f27273336de6eb226ad33117f82350631950c88b4ecee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76803950923e4bebab6385fef3e195d76b577fe2cdb781974fd7074605ed6eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81821edda77f3a45f2b26110ff16cf6a56f2c503f1814cd2150565085c110083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce544b52a03bcf0917789ef6127925ad80a614de676ad16e0b6eca4448d93ebf(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8495b0347fb7d9a318d3792adff55144a55e8c59b6dd6f357db94d43ea53c67(
    *,
    unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8327c8b32ddd1b182bbef06cbf3983e8f06935a2f31a8e0c5566129207df493d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76a69ac1f739e853cf3deb4c90d8d865986db75c9648eea7ae0b987aa06e9d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62a4ace8023071741a18ae04f4c001c5927f997ec26c4c45bdef718f4a6ab46(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43d19aacba117ced9088ff34bb58287d620645465a84e75dfe924d3b753587b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71b3d90295de54d38ad4ebf790003dc91c9590be98e27f873c633aed2f30c97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94edb4a17ad3d74c57e3b5286db6235f98bac022645a14e397c52fe417dfc16e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221a829e4dbd13ff2ef387b9bb39085ae007bd4a17757a8e69b0ddf26f4acb7c(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017f0d7287f1999989cee177ff9fec3aa7f90ef47d919d8c7942df5713d8e039(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2842c436e7231e0e3bac8bfb03424ba348db7f0eb718df41bbf3deb1f762cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5705b030832d9f2317ef15410e92f1b27621eb279eaf8ad66adde112ff1d5786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425ab237fd475d56223211e4df83d345785b7ad6bdaf2e13fd59d8e24da62f0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e863f61884d3ee89643ec2d260c28b666258be5a92f8459407c71ede3c2ee139(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ab73346720b7a32c5b04915a61cded1f8cbeafa6ecd0afa6fc43020a30e999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587339e27fc049fc29887819a8d8d29ee4ef2fe742f506822718f589f877a0b2(
    value: typing.Optional[QuicksightDataSetOutputColumns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96886cac2b7f3037b8b6f687ea0e19fed7cbef9447f99af4e4342e2a25271ca3(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7272b691fee48faecf1cec6969cdc0e13f0be6bd9980b568810d966f6c8b6a36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e219524ef6acd959a09faac3b51cdc9491ef2e7a620bdb47e4955ddece14c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84db83eb6234a9ae25590a9d6423b0238d71d84577fc0cf98e16a9e74cade810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06430127d01d42864549fe2356579b3d43a008d0e33c2c95128b2a04dff70e8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4523ce8324a67d640bb0db7a63c2763f45a40c18636db7439b7c9ef6a7225c3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b992bb218bc239e9e5f061c875fa5d1de7ea2d41eff6804eaceaefab7c6f0837(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89c5c56224027a93e18b5ca97d8f57023b6ade90e54ff34653b88010ac06f5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b160351ab0b89d80b77efb4c7d95616099f63b9f66ad1d62ad79b3a22aeef1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637aea9615b27ae1dfbe90d04ba1d795c74f74f3afa5cca5a8fe399f4a3e60a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0861390ffbb125a1f8a87f312bcfac5ebe4058e98834fc51dd4de847ab8a5bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9cb44c65cbf4a2612f17831b00071838be354365c71b500e582357b1c149e0(
    *,
    physical_table_map_id: builtins.str,
    custom_sql: typing.Optional[typing.Union[QuicksightDataSetPhysicalTableMapCustomSql, typing.Dict[builtins.str, typing.Any]]] = None,
    relational_table: typing.Optional[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTable, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_source: typing.Optional[typing.Union[QuicksightDataSetPhysicalTableMapS3Source, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b417045fc02fb477b93aa3ee5b9765b8193e9c568435670186ad964cdcb7bb(
    *,
    data_source_arn: builtins.str,
    name: builtins.str,
    sql_query: builtins.str,
    columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b358352c8d62e617a74428b7d027d11d59f56e7fd81cea20a0e72b9cd075aeba(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f50a6a450e9b7cbabb04add9a455e195808168ae35d73a09223664184faeaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daee33b4bc788fadb62f93f129a99f792afbb1b94f6e7b6d52fb0ef068a5aea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e190ff108d6ebf41019e0281e7f170d72dda5f8c10b177aa492f5d78b48ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ccdf910594b2f7fdd707f7dd544459852102ef0a819975800496700793290c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f6c85c1f62839a1e3ee95e097bda4bc04cb2e214e261fbafbc62d1ad2fedff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee806658383bf24fffdb1967b0effe7b97c68a582fba3d154838c6ab0b672f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6bc733450bddbb2d753d78764b36c36fe4b7a7cb9e436ffe29e767af501e1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc2b7ff0c724ad94193b94ac93d656a1e07595f41aa1b76ca3aaf2c26fbfd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520952401915d04390a3d9cf8293f4702b3178f135d4f253ce0d465f3742b0b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb35cb6c32d77c5a2f1873f14439f99eb320d8a2db60908c0a0cf8d36136c7dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2811b9a2a705e92163037fa1be45d7535bfdec584ef8ba11f337c7bca4ff78eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e494517a73353d6b5a01a46c03b2a59f2e80474eb7a1001866ff74ee3d59c44(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d125b47f54f1558760aa7db122e538299d8811edabf9473c037caf4c6ce65b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f151179bb34653b5e5b2e538d353acfd927773f62b3e71a007bb1484c679128f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f56833c25a367fbcf9e0d653a80e49cb9a23234527d05f4e1059338848f1caf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4327b0f39b114c9491782655af7069be03fa78931d1da8d3b2f6d9c2ed288f89(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fb961bfd74c1045c4988362fb124247e6a340dbde3cd757375e9ebad0d8fad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2789bf59948cf838a6b4e8e3a0716f87162c3bb4bfaeac3de4285d79c1571ea8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57863597594458797f47f98e8d8fd888e17fec202136a3023e1f552f2b5763cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9705775613ef208594e91f31b073df6f362843bc41d2ed7c21169c348290912(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e6daa67d513b41463009b3bdb2a3d9d69570487a55a9863d6344b02a20057a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f362def38a042bdaac6295dc98582a1f17401f8614f3d2973101d73277829064(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a296332b66f1834808c6af803e6f49383fe88a8cf498f3edc5a8dd3ecfda2ee9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cf14896f9bf81dd64ad21e4c56c4553e0a534b1d4730a1a50e475dc017f84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bd54c8a4e88f6f0579134b758918d245148b8df5f66981d248dea323f8a3ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27d39e9e29def4d3aa69a0c4935de6193fb19e24e8e2e8b9a95c20db96cc375(
    *,
    data_source_arn: builtins.str,
    input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d811d13228990f86e0d27c79f2791706d522f8914745055f46021e57c9c2548f(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be33c4dbb177f2a3b3dc0bcbd7408b3c05a84de844b6e371870394fb3fd6b86b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbcc3f80d4b45a1132ef8124911aac488afedf4bc303bca8c87d7c2e76223cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf32641c5e15f4dc1879ab2ed66d5d8e902f9d13af91a97f549c8f16088ba3e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f969b870baf8ce351d7dee13187b02ef4f277723537f962031621300315c6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d66a579ba8fc9e239c66882995cb7608c5dc1d036f4e5c6fd7eb129dbce9019(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf18f2820c5e4d8067d97ae8e9217728a1a6cbd29bb3dbda0b29ed99e81d832(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d59ea5cab72c5c5572c12f2571088a33f1f430cdfd4763fed0872b7d6513651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f20c2a444f5eebc7c8b5be23e70c55d7a2211ec6e4149d33a573dbd4aba7ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2515be6dfd7e0d3bfc8a99f1f42bbd2e202fdfca48fc57bf1979184f91101b85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8ee1154c4d43a1f6e5ca410a68a440ca92033ec9a1800c2222ecea1dd9a996(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a295cea4a7d7386be180ee264c6d9e3720dedd9f95d885fb440b5a2fc924c03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6e4fcc5f9878378c8c353adfebb8606619e77a83c10f60ce36486cff6d67ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29aa187cc2b681ecf5f41c65942a1e533b3eabfe76a757f9394b0cd4dc7e820d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0348e3c22e6fc8a7815933f2995f1447ad5ed4ffe7ad6eb72527576bfd6f969a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99ea317673b512d0722d641de3d178e22b6a061abc00246ac3a8397460b943a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e232a2b14c771634ba18e3ae0f2c3b4b88f8d5ee5b409ea1f1d4423ed1abc73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b3b6d52f561a42c5bd5a71042342637dbf5343e34fc7a41c5bd5fbd3129c40(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dd1f3550f9977fba768ba34c1fa55d460247c5f2d02ab03fb3afe6d55ccaaf(
    *,
    data_source_arn: builtins.str,
    input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapS3SourceInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    upload_settings: typing.Union[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60ded08ad3275731c113fff1b819d7d42d64aea969c1f819e5d27ed26034e3d(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f00568564f7e6b9e6b45dd6545519d4513637eea3a638541db708627aefa9af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7c557f0942f501e64ad3a30a3fa68c5f670d3faeae3146d6e44b3cd636911b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944724cf57009cbe1aed654cebef0e4aa616f9c680cd07e508a947c6ed630020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01541b6194390651ea2714243a03de11372286efbe98daef7f20a22c076ea021(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5876d6c2f0218bad16b94b789aa3c00e877b35f7e093bfa0d382c5689a104d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fd91560aeed433c8a0cc560613fd0c71d8e21a1962d713bcf885d61f7068a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f615a9c33ab0796544d04b1a3d842dd2bbe2f9143e4e72eb1a2095bafbcd929(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c62aaa5a3fb6523ba7d362e7015d47aec7b66d2d4247cb02a68c2e76b706f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94777eff3eb4e17034124a868e6bbbc13f6360791e7451b1e6de72a6ba6dbc7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21fb3bab8c840b033183547ee69d9d1a12a26ef708840d8d7c11de6526c7b4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a57240f98f7cfe670380be7f911a4e9f84ad54a0aa0257d75185dbf8d5bff4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f997b96d8198ba06b25f34a08b01be69d2512bab7baf52f0969fa71df32ac29(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapS3SourceInputColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2557d47d731feebcc8a4faaedac88d0916be812c717d2604897d154dd1d95197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef425201d6d8964f0696dd28b6787a600221bd6dfff40d5d6ccef224f8e63cd(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapS3Source],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90f713f0cedde691720474f19e32a426d19e79e6ea43de86b55778ad15af210(
    *,
    contains_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    start_from_row: typing.Optional[jsii.Number] = None,
    text_qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb7fd361b75e0f64833f90359529db63687f967fa602a76b702343b5f63e34e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bfd2d3e664a5b2ae5eb8bdad7ad04be466e89d0c18e0af917ca3d33836a067(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4be5a815573f37a7c466e6b2d927d56d3524175ffdaed1364f64fb8ca3eece0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7691709a0c73943619ed43bb89efd5e999bd70656d5f88d3c6b48b451b0c10c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ca41f2a115ccde5a535f51edb2a42c76488b497b93d73422c25f88f6476128(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6777b6c935333c8a83a57ea9d7d37cb883fa9836dc509041f3b526a39b4dd8f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1278f9372d6693532085ef26b1ce3fd85c9e695de3d08500bcc838a68e11e426(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d09e6020455554317abb88130a39e5b223c57830a61cf8d8b2db0fd7c7db602(
    *,
    refresh_configuration: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfiguration, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6756e6e0b31a26b09859d42ab105658d54893ee4fed4db87f1b9a6608e544ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edcdd40aa1f093709965638057ff4828d2176396cdcf2806dd4d05418d96de9(
    value: typing.Optional[QuicksightDataSetRefreshProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a47a6bfafa9c589ed4fc229e42650741b930b7dc8f377392f9f81606f45d043(
    *,
    incremental_refresh: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f4600e5902cdf03ec181044b68dea0f6e90f1f5c13476a8811d201ef54ccca(
    *,
    lookback_window: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6afa72fd3e4f38b4bcceec376887e476f47af9c634d621e4dddd4be5f33dc51(
    *,
    column_name: builtins.str,
    size: jsii.Number,
    size_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd9a9bb936fb79d12229c30be310c6679374b2b59c90d19583a41e05d72ba05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a1a1eb48de5f266af95e270613a8f6c35347d5ca7f38659fc4f8537b0fc1cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b54252b53e15104eda1feb7169dab04805f79954dd05ab0d5e8d7193319ddc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576776b4b0a490043e93f3819ef911edc298f40edb6e973ec8cf7de92967092a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2f9ca216b74ca2dbe383472e9ce9d8aeb41acf69b136b3aaabd0efabac1a40(
    value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe963a53d6969936d5634b25ff490fcf947528f2a4b4c8d877219a2fa7bb5909(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3f15e5557b291505a7c9e7651e8188de49c892440dc6a842bee357096f0de9(
    value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff55cf222b51b6c7d43b7875cbb8703a5c4d39b913c1c91f458098ee99878424(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d92282786058b304069fe3121c6ebd7dc04f6d6e6caf2cc4fb68a5c56834f5(
    value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a76ce65afd36b8266cf3856c84acbe7b2eae1377ef1eee1f2dedaf67a260c8(
    *,
    arn: builtins.str,
    permission_policy: builtins.str,
    format_version: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dc7e946e7be0507eb2b56e86510ff13d26e4e7b9920055cfbbadc3a36b47d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea1cd91e6a704259693dcca9d7fdbd7e3486da2e1dc412edd58426681e3532b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70142bd38a4c42cb7354634376ec3ce0d426c652f89989234f0fe6808d8d3615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f51ce6dc649102d35fed98d84013a2bebde4e59d483d39e7288f528cd05a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc037893a2a82d9cce1885a1eb5abfd581351a3125170d13f777c989c82d9f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6be64390543edd0ff1be293e2a1adeec348040e89e0f1a14aa501d37f9f0c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70f4c75f7c0046cdb0ba8fd0e8dd1e456d79b579d22bed7434b085841275ba3(
    value: typing.Optional[QuicksightDataSetRowLevelPermissionDataSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332f0a253d8eb0809bff1117fad61c4c811219c051686a25e60ec0c1dd06b76f(
    *,
    tag_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules, typing.Dict[builtins.str, typing.Any]]]],
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd423c6150ae7d32fe8b75dda0dbc9c694af84fce63c589ed826c89a88971d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf6e16db1bcbb23babf73c4483845a49563e80db3dda7aa22f0b1dfa1d2cbb9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd83682e379fd49f61179fdaebd99a9d57df7eeb7f1c8f416e173c5dd55579cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e15ea5d5d656e9f36ed22ecadf0bb792bd38910f7eecfd02f7229301af75f68(
    value: typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50743f4f00ed09932897e0717887c10614d87f21823cfa3a4e334392b6b536d8(
    *,
    column_name: builtins.str,
    tag_key: builtins.str,
    match_all_value: typing.Optional[builtins.str] = None,
    tag_multi_value_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa606d7e5dd40b4059407a2ec43c8eca7d8c0111fd49308d459011a05c477fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d76764e0b6dd338c6b92c01eeac51828e27f1122ad90b650ee87b147d2a136(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e369916cb2bb0b837d77ba615fb81e6eae33232022c621ab96376b4dcb9e9ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613b49f334c9335e56ef33056ba947da86c0cc5a97150ed72c9e287229e6191a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a73715db7ca6cf956216a7940853563efced2bc03936ea7f92b8ff0b49bd33c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d70bdc564587ebd4225e4436decf1920651bf0404d9773e2e49ce257b2fe84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a257684253f385ae9e61da103567d6b9300d0e3a803c33bbfaef2b5af1b7b9db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f693e280b4f3cfd8d1019078bc34e01f91fc174380667c25a4620ebd64cdd6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a659ad9e68c687c7545511435422327c4d5f2781aa8dfa13092f4ff6ea3167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8640bb99c74e52c4440d41a816113ac9cf45a0270be7f2ca4f8db8d6d2ecc874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f0780f61201466b294dfb2ebc1bbdcedbfc70467de572eec6c0eb6e29addff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9972135129a574e54a9fb51153288a35e748c766d127bac45754d0697f466a98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]],
) -> None:
    """Type checking stubs"""
    pass
