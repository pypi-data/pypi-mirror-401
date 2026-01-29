r'''
# `aws_quicksight_theme`

Refer to the Terraform Registry for docs: [`aws_quicksight_theme`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme).
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


class QuicksightTheme(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightTheme",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme aws_quicksight_theme}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        base_theme_id: builtins.str,
        name: builtins.str,
        theme_id: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union["QuicksightThemeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemePermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["QuicksightThemeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_description: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme aws_quicksight_theme} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#base_theme_id QuicksightTheme#base_theme_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#name QuicksightTheme#name}.
        :param theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#theme_id QuicksightTheme#theme_id}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#aws_account_id QuicksightTheme#aws_account_id}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#configuration QuicksightTheme#configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#id QuicksightTheme#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#permissions QuicksightTheme#permissions}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#region QuicksightTheme#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tags QuicksightTheme#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tags_all QuicksightTheme#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#timeouts QuicksightTheme#timeouts}
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#version_description QuicksightTheme#version_description}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772be6d7f751e3355ac480fe17e3d3450cd4fc6165a37aa2b4063ce798d1ac39)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightThemeConfig(
            base_theme_id=base_theme_id,
            name=name,
            theme_id=theme_id,
            aws_account_id=aws_account_id,
            configuration=configuration,
            id=id,
            permissions=permissions,
            region=region,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            version_description=version_description,
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
        '''Generates CDKTF code for importing a QuicksightTheme resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightTheme to import.
        :param import_from_id: The id of the existing QuicksightTheme that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightTheme to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd3dfccc06282fb74dce826a5d894cfc9db9994e1b9809095299c9144181dd1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        data_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationDataColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet: typing.Optional[typing.Union["QuicksightThemeConfigurationSheet", typing.Dict[builtins.str, typing.Any]]] = None,
        typography: typing.Optional[typing.Union["QuicksightThemeConfigurationTypography", typing.Dict[builtins.str, typing.Any]]] = None,
        ui_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationUiColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_color_palette: data_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#data_color_palette QuicksightTheme#data_color_palette}
        :param sheet: sheet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#sheet QuicksightTheme#sheet}
        :param typography: typography block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#typography QuicksightTheme#typography}
        :param ui_color_palette: ui_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#ui_color_palette QuicksightTheme#ui_color_palette}
        '''
        value = QuicksightThemeConfiguration(
            data_color_palette=data_color_palette,
            sheet=sheet,
            typography=typography,
            ui_color_palette=ui_color_palette,
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemePermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b237f2749f33d0e4744d4644411e8d3395d7c82d01daaca8c9eae5a037acaa4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#create QuicksightTheme#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#delete QuicksightTheme#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#update QuicksightTheme#update}.
        '''
        value = QuicksightThemeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

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

    @jsii.member(jsii_name="resetVersionDescription")
    def reset_version_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionDescription", []))

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
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "QuicksightThemeConfigurationOutputReference":
        return typing.cast("QuicksightThemeConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedTime")
    def last_updated_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "QuicksightThemePermissionsList":
        return typing.cast("QuicksightThemePermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "QuicksightThemeTimeoutsOutputReference":
        return typing.cast("QuicksightThemeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionNumber")
    def version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "versionNumber"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="baseThemeIdInput")
    def base_theme_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseThemeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["QuicksightThemeConfiguration"]:
        return typing.cast(typing.Optional["QuicksightThemeConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]], jsii.get(self, "permissionsInput"))

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
    @jsii.member(jsii_name="themeIdInput")
    def theme_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "themeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightThemeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightThemeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionDescriptionInput")
    def version_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725a10f4ff73d8c7664d764c02761d201911a26efa7c5c3ec54dd580de8bc20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseThemeId")
    def base_theme_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseThemeId"))

    @base_theme_id.setter
    def base_theme_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11dc6d5184f33bb514a4db706a942441529568a1d5604d3e0fd4e1724d4b87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseThemeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334e03845170e4b7086a08ae1fcc14014a37f7f9cc449cdbe96766bc98420c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8ad125d36dfc4671698dccddab967cc9bfc80b6da0b807516af84cac0f73a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8538ebd379f88734275e935dce8cd766ecf1ea0e028bccf91b6ca34fc96e36d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0529355c1b00ce5fe33bad6a8f418773a436b89867a0f0ec3256c58fa5e617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe4cb44426f6347f2f4db5b3573492c565a1aa198180f3b365c6979786cf228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="themeId")
    def theme_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "themeId"))

    @theme_id.setter
    def theme_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f829630ca303dfb7377b4923b41633071903ef8b03df78604e504fdeabe3457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "themeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd7431689975c5fb560cb88e609c81af0ebd219e550be481499abce490f8d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "base_theme_id": "baseThemeId",
        "name": "name",
        "theme_id": "themeId",
        "aws_account_id": "awsAccountId",
        "configuration": "configuration",
        "id": "id",
        "permissions": "permissions",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "version_description": "versionDescription",
    },
)
class QuicksightThemeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        base_theme_id: builtins.str,
        name: builtins.str,
        theme_id: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union["QuicksightThemeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemePermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["QuicksightThemeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param base_theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#base_theme_id QuicksightTheme#base_theme_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#name QuicksightTheme#name}.
        :param theme_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#theme_id QuicksightTheme#theme_id}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#aws_account_id QuicksightTheme#aws_account_id}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#configuration QuicksightTheme#configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#id QuicksightTheme#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#permissions QuicksightTheme#permissions}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#region QuicksightTheme#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tags QuicksightTheme#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tags_all QuicksightTheme#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#timeouts QuicksightTheme#timeouts}
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#version_description QuicksightTheme#version_description}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = QuicksightThemeConfiguration(**configuration)
        if isinstance(timeouts, dict):
            timeouts = QuicksightThemeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7c5a320bb8a61a2b38207ca96140d9b6fce064b6ff7e35862bd23c844536e9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument base_theme_id", value=base_theme_id, expected_type=type_hints["base_theme_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument theme_id", value=theme_id, expected_type=type_hints["theme_id"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_theme_id": base_theme_id,
            "name": name,
            "theme_id": theme_id,
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
        if configuration is not None:
            self._values["configuration"] = configuration
        if id is not None:
            self._values["id"] = id
        if permissions is not None:
            self._values["permissions"] = permissions
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_description is not None:
            self._values["version_description"] = version_description

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
    def base_theme_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#base_theme_id QuicksightTheme#base_theme_id}.'''
        result = self._values.get("base_theme_id")
        assert result is not None, "Required property 'base_theme_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#name QuicksightTheme#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def theme_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#theme_id QuicksightTheme#theme_id}.'''
        result = self._values.get("theme_id")
        assert result is not None, "Required property 'theme_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#aws_account_id QuicksightTheme#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(self) -> typing.Optional["QuicksightThemeConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#configuration QuicksightTheme#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["QuicksightThemeConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#id QuicksightTheme#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#permissions QuicksightTheme#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemePermissions"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#region QuicksightTheme#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tags QuicksightTheme#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tags_all QuicksightTheme#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["QuicksightThemeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#timeouts QuicksightTheme#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["QuicksightThemeTimeouts"], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#version_description QuicksightTheme#version_description}.'''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "data_color_palette": "dataColorPalette",
        "sheet": "sheet",
        "typography": "typography",
        "ui_color_palette": "uiColorPalette",
    },
)
class QuicksightThemeConfiguration:
    def __init__(
        self,
        *,
        data_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationDataColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet: typing.Optional[typing.Union["QuicksightThemeConfigurationSheet", typing.Dict[builtins.str, typing.Any]]] = None,
        typography: typing.Optional[typing.Union["QuicksightThemeConfigurationTypography", typing.Dict[builtins.str, typing.Any]]] = None,
        ui_color_palette: typing.Optional[typing.Union["QuicksightThemeConfigurationUiColorPalette", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_color_palette: data_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#data_color_palette QuicksightTheme#data_color_palette}
        :param sheet: sheet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#sheet QuicksightTheme#sheet}
        :param typography: typography block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#typography QuicksightTheme#typography}
        :param ui_color_palette: ui_color_palette block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#ui_color_palette QuicksightTheme#ui_color_palette}
        '''
        if isinstance(data_color_palette, dict):
            data_color_palette = QuicksightThemeConfigurationDataColorPalette(**data_color_palette)
        if isinstance(sheet, dict):
            sheet = QuicksightThemeConfigurationSheet(**sheet)
        if isinstance(typography, dict):
            typography = QuicksightThemeConfigurationTypography(**typography)
        if isinstance(ui_color_palette, dict):
            ui_color_palette = QuicksightThemeConfigurationUiColorPalette(**ui_color_palette)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3428c4adfba7c0cf96cc8afc711c889a5c4fecdda3665865dc61264cdb579587)
            check_type(argname="argument data_color_palette", value=data_color_palette, expected_type=type_hints["data_color_palette"])
            check_type(argname="argument sheet", value=sheet, expected_type=type_hints["sheet"])
            check_type(argname="argument typography", value=typography, expected_type=type_hints["typography"])
            check_type(argname="argument ui_color_palette", value=ui_color_palette, expected_type=type_hints["ui_color_palette"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_color_palette is not None:
            self._values["data_color_palette"] = data_color_palette
        if sheet is not None:
            self._values["sheet"] = sheet
        if typography is not None:
            self._values["typography"] = typography
        if ui_color_palette is not None:
            self._values["ui_color_palette"] = ui_color_palette

    @builtins.property
    def data_color_palette(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationDataColorPalette"]:
        '''data_color_palette block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#data_color_palette QuicksightTheme#data_color_palette}
        '''
        result = self._values.get("data_color_palette")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationDataColorPalette"], result)

    @builtins.property
    def sheet(self) -> typing.Optional["QuicksightThemeConfigurationSheet"]:
        '''sheet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#sheet QuicksightTheme#sheet}
        '''
        result = self._values.get("sheet")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheet"], result)

    @builtins.property
    def typography(self) -> typing.Optional["QuicksightThemeConfigurationTypography"]:
        '''typography block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#typography QuicksightTheme#typography}
        '''
        result = self._values.get("typography")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationTypography"], result)

    @builtins.property
    def ui_color_palette(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationUiColorPalette"]:
        '''ui_color_palette block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#ui_color_palette QuicksightTheme#ui_color_palette}
        '''
        result = self._values.get("ui_color_palette")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationUiColorPalette"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationDataColorPalette",
    jsii_struct_bases=[],
    name_mapping={
        "colors": "colors",
        "empty_fill_color": "emptyFillColor",
        "min_max_gradient": "minMaxGradient",
    },
)
class QuicksightThemeConfigurationDataColorPalette:
    def __init__(
        self,
        *,
        colors: typing.Optional[typing.Sequence[builtins.str]] = None,
        empty_fill_color: typing.Optional[builtins.str] = None,
        min_max_gradient: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param colors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#colors QuicksightTheme#colors}.
        :param empty_fill_color: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#empty_fill_color QuicksightTheme#empty_fill_color}.
        :param min_max_gradient: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#min_max_gradient QuicksightTheme#min_max_gradient}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00aa6b3ba58756dd9e8eee23007063a3436abedc8a53f1613263f6f48f41dffd)
            check_type(argname="argument colors", value=colors, expected_type=type_hints["colors"])
            check_type(argname="argument empty_fill_color", value=empty_fill_color, expected_type=type_hints["empty_fill_color"])
            check_type(argname="argument min_max_gradient", value=min_max_gradient, expected_type=type_hints["min_max_gradient"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if colors is not None:
            self._values["colors"] = colors
        if empty_fill_color is not None:
            self._values["empty_fill_color"] = empty_fill_color
        if min_max_gradient is not None:
            self._values["min_max_gradient"] = min_max_gradient

    @builtins.property
    def colors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#colors QuicksightTheme#colors}.'''
        result = self._values.get("colors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def empty_fill_color(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#empty_fill_color QuicksightTheme#empty_fill_color}.'''
        result = self._values.get("empty_fill_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_max_gradient(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#min_max_gradient QuicksightTheme#min_max_gradient}.'''
        result = self._values.get("min_max_gradient")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationDataColorPalette(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationDataColorPaletteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationDataColorPaletteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b671adc4a8420e67c38017155e21c7bb51a11f8a6e4fb2d9311b6c56e728f72a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetColors")
    def reset_colors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColors", []))

    @jsii.member(jsii_name="resetEmptyFillColor")
    def reset_empty_fill_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyFillColor", []))

    @jsii.member(jsii_name="resetMinMaxGradient")
    def reset_min_max_gradient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinMaxGradient", []))

    @builtins.property
    @jsii.member(jsii_name="colorsInput")
    def colors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "colorsInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyFillColorInput")
    def empty_fill_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emptyFillColorInput"))

    @builtins.property
    @jsii.member(jsii_name="minMaxGradientInput")
    def min_max_gradient_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "minMaxGradientInput"))

    @builtins.property
    @jsii.member(jsii_name="colors")
    def colors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "colors"))

    @colors.setter
    def colors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c850919875fa99d9ee901a0e3e9eb43182bfe78548164828b4719917f8483725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "colors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emptyFillColor")
    def empty_fill_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emptyFillColor"))

    @empty_fill_color.setter
    def empty_fill_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98d1cd14155e4c0cc4acad007bef782f50dd6f630031139ce953273125e28bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emptyFillColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minMaxGradient")
    def min_max_gradient(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "minMaxGradient"))

    @min_max_gradient.setter
    def min_max_gradient(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec634f662c4c4244d39ad3ba6b7dc562dc5ad650e216c590f4aa8c992470928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minMaxGradient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationDataColorPalette]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationDataColorPalette], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationDataColorPalette],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733adebf86fdaacc9a814fa358a415771315e28885c7f2893aaa1dfe00093e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f2d08868d804a22b30d677d7c22215de21edafcc53ac6ce6142a8f15ee03b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataColorPalette")
    def put_data_color_palette(
        self,
        *,
        colors: typing.Optional[typing.Sequence[builtins.str]] = None,
        empty_fill_color: typing.Optional[builtins.str] = None,
        min_max_gradient: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param colors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#colors QuicksightTheme#colors}.
        :param empty_fill_color: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#empty_fill_color QuicksightTheme#empty_fill_color}.
        :param min_max_gradient: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#min_max_gradient QuicksightTheme#min_max_gradient}.
        '''
        value = QuicksightThemeConfigurationDataColorPalette(
            colors=colors,
            empty_fill_color=empty_fill_color,
            min_max_gradient=min_max_gradient,
        )

        return typing.cast(None, jsii.invoke(self, "putDataColorPalette", [value]))

    @jsii.member(jsii_name="putSheet")
    def put_sheet(
        self,
        *,
        tile: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTile", typing.Dict[builtins.str, typing.Any]]] = None,
        tile_layout: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tile: tile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tile QuicksightTheme#tile}
        :param tile_layout: tile_layout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tile_layout QuicksightTheme#tile_layout}
        '''
        value = QuicksightThemeConfigurationSheet(tile=tile, tile_layout=tile_layout)

        return typing.cast(None, jsii.invoke(self, "putSheet", [value]))

    @jsii.member(jsii_name="putTypography")
    def put_typography(
        self,
        *,
        font_families: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemeConfigurationTypographyFontFamilies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param font_families: font_families block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#font_families QuicksightTheme#font_families}
        '''
        value = QuicksightThemeConfigurationTypography(font_families=font_families)

        return typing.cast(None, jsii.invoke(self, "putTypography", [value]))

    @jsii.member(jsii_name="putUiColorPalette")
    def put_ui_color_palette(
        self,
        *,
        accent: typing.Optional[builtins.str] = None,
        accent_foreground: typing.Optional[builtins.str] = None,
        danger: typing.Optional[builtins.str] = None,
        danger_foreground: typing.Optional[builtins.str] = None,
        dimension: typing.Optional[builtins.str] = None,
        dimension_foreground: typing.Optional[builtins.str] = None,
        measure: typing.Optional[builtins.str] = None,
        measure_foreground: typing.Optional[builtins.str] = None,
        primary_background: typing.Optional[builtins.str] = None,
        primary_foreground: typing.Optional[builtins.str] = None,
        secondary_background: typing.Optional[builtins.str] = None,
        secondary_foreground: typing.Optional[builtins.str] = None,
        success: typing.Optional[builtins.str] = None,
        success_foreground: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
        warning_foreground: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#accent QuicksightTheme#accent}.
        :param accent_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#accent_foreground QuicksightTheme#accent_foreground}.
        :param danger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#danger QuicksightTheme#danger}.
        :param danger_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#danger_foreground QuicksightTheme#danger_foreground}.
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#dimension QuicksightTheme#dimension}.
        :param dimension_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#dimension_foreground QuicksightTheme#dimension_foreground}.
        :param measure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#measure QuicksightTheme#measure}.
        :param measure_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#measure_foreground QuicksightTheme#measure_foreground}.
        :param primary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#primary_background QuicksightTheme#primary_background}.
        :param primary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#primary_foreground QuicksightTheme#primary_foreground}.
        :param secondary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#secondary_background QuicksightTheme#secondary_background}.
        :param secondary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#secondary_foreground QuicksightTheme#secondary_foreground}.
        :param success: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#success QuicksightTheme#success}.
        :param success_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#success_foreground QuicksightTheme#success_foreground}.
        :param warning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#warning QuicksightTheme#warning}.
        :param warning_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#warning_foreground QuicksightTheme#warning_foreground}.
        '''
        value = QuicksightThemeConfigurationUiColorPalette(
            accent=accent,
            accent_foreground=accent_foreground,
            danger=danger,
            danger_foreground=danger_foreground,
            dimension=dimension,
            dimension_foreground=dimension_foreground,
            measure=measure,
            measure_foreground=measure_foreground,
            primary_background=primary_background,
            primary_foreground=primary_foreground,
            secondary_background=secondary_background,
            secondary_foreground=secondary_foreground,
            success=success,
            success_foreground=success_foreground,
            warning=warning,
            warning_foreground=warning_foreground,
        )

        return typing.cast(None, jsii.invoke(self, "putUiColorPalette", [value]))

    @jsii.member(jsii_name="resetDataColorPalette")
    def reset_data_color_palette(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataColorPalette", []))

    @jsii.member(jsii_name="resetSheet")
    def reset_sheet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSheet", []))

    @jsii.member(jsii_name="resetTypography")
    def reset_typography(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypography", []))

    @jsii.member(jsii_name="resetUiColorPalette")
    def reset_ui_color_palette(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUiColorPalette", []))

    @builtins.property
    @jsii.member(jsii_name="dataColorPalette")
    def data_color_palette(
        self,
    ) -> QuicksightThemeConfigurationDataColorPaletteOutputReference:
        return typing.cast(QuicksightThemeConfigurationDataColorPaletteOutputReference, jsii.get(self, "dataColorPalette"))

    @builtins.property
    @jsii.member(jsii_name="sheet")
    def sheet(self) -> "QuicksightThemeConfigurationSheetOutputReference":
        return typing.cast("QuicksightThemeConfigurationSheetOutputReference", jsii.get(self, "sheet"))

    @builtins.property
    @jsii.member(jsii_name="typography")
    def typography(self) -> "QuicksightThemeConfigurationTypographyOutputReference":
        return typing.cast("QuicksightThemeConfigurationTypographyOutputReference", jsii.get(self, "typography"))

    @builtins.property
    @jsii.member(jsii_name="uiColorPalette")
    def ui_color_palette(
        self,
    ) -> "QuicksightThemeConfigurationUiColorPaletteOutputReference":
        return typing.cast("QuicksightThemeConfigurationUiColorPaletteOutputReference", jsii.get(self, "uiColorPalette"))

    @builtins.property
    @jsii.member(jsii_name="dataColorPaletteInput")
    def data_color_palette_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationDataColorPalette]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationDataColorPalette], jsii.get(self, "dataColorPaletteInput"))

    @builtins.property
    @jsii.member(jsii_name="sheetInput")
    def sheet_input(self) -> typing.Optional["QuicksightThemeConfigurationSheet"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheet"], jsii.get(self, "sheetInput"))

    @builtins.property
    @jsii.member(jsii_name="typographyInput")
    def typography_input(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationTypography"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationTypography"], jsii.get(self, "typographyInput"))

    @builtins.property
    @jsii.member(jsii_name="uiColorPaletteInput")
    def ui_color_palette_input(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationUiColorPalette"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationUiColorPalette"], jsii.get(self, "uiColorPaletteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfiguration]:
        return typing.cast(typing.Optional[QuicksightThemeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3e588f6e57b494cd5900bac5d42af8e06c7525d2f301223f6ce3ff00661455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheet",
    jsii_struct_bases=[],
    name_mapping={"tile": "tile", "tile_layout": "tileLayout"},
)
class QuicksightThemeConfigurationSheet:
    def __init__(
        self,
        *,
        tile: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTile", typing.Dict[builtins.str, typing.Any]]] = None,
        tile_layout: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tile: tile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tile QuicksightTheme#tile}
        :param tile_layout: tile_layout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tile_layout QuicksightTheme#tile_layout}
        '''
        if isinstance(tile, dict):
            tile = QuicksightThemeConfigurationSheetTile(**tile)
        if isinstance(tile_layout, dict):
            tile_layout = QuicksightThemeConfigurationSheetTileLayout(**tile_layout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4bb469775a4a4d9e56c9bf5d96a1e40ad441b584af1202973937c01c8ec2fc)
            check_type(argname="argument tile", value=tile, expected_type=type_hints["tile"])
            check_type(argname="argument tile_layout", value=tile_layout, expected_type=type_hints["tile_layout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tile is not None:
            self._values["tile"] = tile
        if tile_layout is not None:
            self._values["tile_layout"] = tile_layout

    @builtins.property
    def tile(self) -> typing.Optional["QuicksightThemeConfigurationSheetTile"]:
        '''tile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tile QuicksightTheme#tile}
        '''
        result = self._values.get("tile")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTile"], result)

    @builtins.property
    def tile_layout(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayout"]:
        '''tile_layout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#tile_layout QuicksightTheme#tile_layout}
        '''
        result = self._values.get("tile_layout")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e419e820e22d7f16316a6b30ecac4877960624527f0ed79032b1a0828d8969e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTile")
    def put_tile(
        self,
        *,
        border: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileBorder", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param border: border block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#border QuicksightTheme#border}
        '''
        value = QuicksightThemeConfigurationSheetTile(border=border)

        return typing.cast(None, jsii.invoke(self, "putTile", [value]))

    @jsii.member(jsii_name="putTileLayout")
    def put_tile_layout(
        self,
        *,
        gutter: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutGutter", typing.Dict[builtins.str, typing.Any]]] = None,
        margin: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutMargin", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gutter: gutter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#gutter QuicksightTheme#gutter}
        :param margin: margin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#margin QuicksightTheme#margin}
        '''
        value = QuicksightThemeConfigurationSheetTileLayout(
            gutter=gutter, margin=margin
        )

        return typing.cast(None, jsii.invoke(self, "putTileLayout", [value]))

    @jsii.member(jsii_name="resetTile")
    def reset_tile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTile", []))

    @jsii.member(jsii_name="resetTileLayout")
    def reset_tile_layout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTileLayout", []))

    @builtins.property
    @jsii.member(jsii_name="tile")
    def tile(self) -> "QuicksightThemeConfigurationSheetTileOutputReference":
        return typing.cast("QuicksightThemeConfigurationSheetTileOutputReference", jsii.get(self, "tile"))

    @builtins.property
    @jsii.member(jsii_name="tileLayout")
    def tile_layout(
        self,
    ) -> "QuicksightThemeConfigurationSheetTileLayoutOutputReference":
        return typing.cast("QuicksightThemeConfigurationSheetTileLayoutOutputReference", jsii.get(self, "tileLayout"))

    @builtins.property
    @jsii.member(jsii_name="tileInput")
    def tile_input(self) -> typing.Optional["QuicksightThemeConfigurationSheetTile"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTile"], jsii.get(self, "tileInput"))

    @builtins.property
    @jsii.member(jsii_name="tileLayoutInput")
    def tile_layout_input(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayout"]:
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayout"], jsii.get(self, "tileLayoutInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfigurationSheet]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cda6a7def02ed2dc0b4af65ea38b1658f5a254f5e24da357215967b42ce6f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTile",
    jsii_struct_bases=[],
    name_mapping={"border": "border"},
)
class QuicksightThemeConfigurationSheetTile:
    def __init__(
        self,
        *,
        border: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileBorder", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param border: border block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#border QuicksightTheme#border}
        '''
        if isinstance(border, dict):
            border = QuicksightThemeConfigurationSheetTileBorder(**border)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362002f0dfd6db1b21b5971ed92f26233ab7b5f4bc20afaa2d8d689eaeee58fd)
            check_type(argname="argument border", value=border, expected_type=type_hints["border"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if border is not None:
            self._values["border"] = border

    @builtins.property
    def border(self) -> typing.Optional["QuicksightThemeConfigurationSheetTileBorder"]:
        '''border block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#border QuicksightTheme#border}
        '''
        result = self._values.get("border")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileBorder"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileBorder",
    jsii_struct_bases=[],
    name_mapping={"show": "show"},
)
class QuicksightThemeConfigurationSheetTileBorder:
    def __init__(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f0350d306c7b31c6f905df4c8ed719451e7121d9163f9b31cdf06a9212a26a)
            check_type(argname="argument show", value=show, expected_type=type_hints["show"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if show is not None:
            self._values["show"] = show

    @builtins.property
    def show(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.'''
        result = self._values.get("show")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileBorder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetTileBorderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileBorderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f3f956d2c63c8491ef07c46ad35540f003519833cb56125cd010441db3f190f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetShow")
    def reset_show(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShow", []))

    @builtins.property
    @jsii.member(jsii_name="showInput")
    def show_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInput"))

    @builtins.property
    @jsii.member(jsii_name="show")
    def show(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "show"))

    @show.setter
    def show(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7717c2071970373ed2fc0f450a1618090ee52150635cb9dea6cd3125ea96ee71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "show", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileBorder]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileBorder], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileBorder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a394e7fc8e0587593f0a076084d6c37d96196e6857ee40b99761a8b94a14237d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayout",
    jsii_struct_bases=[],
    name_mapping={"gutter": "gutter", "margin": "margin"},
)
class QuicksightThemeConfigurationSheetTileLayout:
    def __init__(
        self,
        *,
        gutter: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutGutter", typing.Dict[builtins.str, typing.Any]]] = None,
        margin: typing.Optional[typing.Union["QuicksightThemeConfigurationSheetTileLayoutMargin", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gutter: gutter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#gutter QuicksightTheme#gutter}
        :param margin: margin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#margin QuicksightTheme#margin}
        '''
        if isinstance(gutter, dict):
            gutter = QuicksightThemeConfigurationSheetTileLayoutGutter(**gutter)
        if isinstance(margin, dict):
            margin = QuicksightThemeConfigurationSheetTileLayoutMargin(**margin)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8997186b2158b522d77ae391f4f7c605c0c90bbdf92f618c1fb92173bc57e710)
            check_type(argname="argument gutter", value=gutter, expected_type=type_hints["gutter"])
            check_type(argname="argument margin", value=margin, expected_type=type_hints["margin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gutter is not None:
            self._values["gutter"] = gutter
        if margin is not None:
            self._values["margin"] = margin

    @builtins.property
    def gutter(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayoutGutter"]:
        '''gutter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#gutter QuicksightTheme#gutter}
        '''
        result = self._values.get("gutter")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayoutGutter"], result)

    @builtins.property
    def margin(
        self,
    ) -> typing.Optional["QuicksightThemeConfigurationSheetTileLayoutMargin"]:
        '''margin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#margin QuicksightTheme#margin}
        '''
        result = self._values.get("margin")
        return typing.cast(typing.Optional["QuicksightThemeConfigurationSheetTileLayoutMargin"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileLayout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutGutter",
    jsii_struct_bases=[],
    name_mapping={"show": "show"},
)
class QuicksightThemeConfigurationSheetTileLayoutGutter:
    def __init__(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21347ef5832ace329e1276b142e8f84bfd3cf92ef56d1ff68b7bf3769d8b70c)
            check_type(argname="argument show", value=show, expected_type=type_hints["show"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if show is not None:
            self._values["show"] = show

    @builtins.property
    def show(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.'''
        result = self._values.get("show")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileLayoutGutter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcfe38ec4b88c8fbd346bdcb0a14f7623ac0fb8fb9d9737578c402fb9dc89d2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetShow")
    def reset_show(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShow", []))

    @builtins.property
    @jsii.member(jsii_name="showInput")
    def show_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInput"))

    @builtins.property
    @jsii.member(jsii_name="show")
    def show(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "show"))

    @show.setter
    def show(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0789cf29b9f47730974ac18c8136229b8eb86b00a15ae8641c444faeeb63414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "show", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728cf3a56c65565ce0271fd97c4b6390c2887390066632effb5bb55e04a2289d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutMargin",
    jsii_struct_bases=[],
    name_mapping={"show": "show"},
)
class QuicksightThemeConfigurationSheetTileLayoutMargin:
    def __init__(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159b44a9831117999e3c4336de3f54178a10f0a9045fc9dcbb156244d8655924)
            check_type(argname="argument show", value=show, expected_type=type_hints["show"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if show is not None:
            self._values["show"] = show

    @builtins.property
    def show(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.'''
        result = self._values.get("show")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationSheetTileLayoutMargin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8238763fe5e48b343830553f5ec3a5652457dcd5d2b9c9b345eb4d335d5b05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetShow")
    def reset_show(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShow", []))

    @builtins.property
    @jsii.member(jsii_name="showInput")
    def show_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInput"))

    @builtins.property
    @jsii.member(jsii_name="show")
    def show(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "show"))

    @show.setter
    def show(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12e5c31b241a74955485ef14639295ff3005b2e1da5e8d2cd947776087c5a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "show", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94477cc5e75e7a61ec9e82c16fb57c33f3dcec1983bc5a87058f021470b2824c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationSheetTileLayoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileLayoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59bb9b3524daa606e48d4a11ffc4f70c23fa22e3c1ad8926eb41ed132cd6c53f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGutter")
    def put_gutter(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        value = QuicksightThemeConfigurationSheetTileLayoutGutter(show=show)

        return typing.cast(None, jsii.invoke(self, "putGutter", [value]))

    @jsii.member(jsii_name="putMargin")
    def put_margin(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        value = QuicksightThemeConfigurationSheetTileLayoutMargin(show=show)

        return typing.cast(None, jsii.invoke(self, "putMargin", [value]))

    @jsii.member(jsii_name="resetGutter")
    def reset_gutter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGutter", []))

    @jsii.member(jsii_name="resetMargin")
    def reset_margin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMargin", []))

    @builtins.property
    @jsii.member(jsii_name="gutter")
    def gutter(
        self,
    ) -> QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference:
        return typing.cast(QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference, jsii.get(self, "gutter"))

    @builtins.property
    @jsii.member(jsii_name="margin")
    def margin(
        self,
    ) -> QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference:
        return typing.cast(QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference, jsii.get(self, "margin"))

    @builtins.property
    @jsii.member(jsii_name="gutterInput")
    def gutter_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter], jsii.get(self, "gutterInput"))

    @builtins.property
    @jsii.member(jsii_name="marginInput")
    def margin_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin], jsii.get(self, "marginInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileLayout]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileLayout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTileLayout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce06a9613921e648f351cbf8e8bfc3216ba9e73e904a7fac10f92ef410ea0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationSheetTileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationSheetTileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a82a79c5e4778a878711fc27e19e1da0f03a60c1fb65857b6df4833372cf07e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBorder")
    def put_border(
        self,
        *,
        show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param show: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#show QuicksightTheme#show}.
        '''
        value = QuicksightThemeConfigurationSheetTileBorder(show=show)

        return typing.cast(None, jsii.invoke(self, "putBorder", [value]))

    @jsii.member(jsii_name="resetBorder")
    def reset_border(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBorder", []))

    @builtins.property
    @jsii.member(jsii_name="border")
    def border(self) -> QuicksightThemeConfigurationSheetTileBorderOutputReference:
        return typing.cast(QuicksightThemeConfigurationSheetTileBorderOutputReference, jsii.get(self, "border"))

    @builtins.property
    @jsii.member(jsii_name="borderInput")
    def border_input(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationSheetTileBorder]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTileBorder], jsii.get(self, "borderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfigurationSheetTile]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationSheetTile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationSheetTile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68409a362d2ef3de5f5a909c79cf6febb06e75324fbfa15d18d3fe7d07173bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypography",
    jsii_struct_bases=[],
    name_mapping={"font_families": "fontFamilies"},
)
class QuicksightThemeConfigurationTypography:
    def __init__(
        self,
        *,
        font_families: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightThemeConfigurationTypographyFontFamilies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param font_families: font_families block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#font_families QuicksightTheme#font_families}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55ec4282f7d32576b641c450c4e6cfb59e81105c02da60a90c41b0e218bfb03)
            check_type(argname="argument font_families", value=font_families, expected_type=type_hints["font_families"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if font_families is not None:
            self._values["font_families"] = font_families

    @builtins.property
    def font_families(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemeConfigurationTypographyFontFamilies"]]]:
        '''font_families block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#font_families QuicksightTheme#font_families}
        '''
        result = self._values.get("font_families")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightThemeConfigurationTypographyFontFamilies"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationTypography(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyFontFamilies",
    jsii_struct_bases=[],
    name_mapping={"font_family": "fontFamily"},
)
class QuicksightThemeConfigurationTypographyFontFamilies:
    def __init__(self, *, font_family: typing.Optional[builtins.str] = None) -> None:
        '''
        :param font_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#font_family QuicksightTheme#font_family}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943019b76160b2b6a496b84a4b53cfb0b527f424ea70b97ddd3aa5a60788d177)
            check_type(argname="argument font_family", value=font_family, expected_type=type_hints["font_family"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if font_family is not None:
            self._values["font_family"] = font_family

    @builtins.property
    def font_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#font_family QuicksightTheme#font_family}.'''
        result = self._values.get("font_family")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationTypographyFontFamilies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationTypographyFontFamiliesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyFontFamiliesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51978e3fa8d8f9df509114804896f923cb00eaf21e1ab979d5e5207fa2cad751)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightThemeConfigurationTypographyFontFamiliesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438ea4bdf690c301223b004db474d5a112e56a8264b8ada0d44198a57efbad13)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightThemeConfigurationTypographyFontFamiliesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dc1276801a60116b09e212a5388ebfee353495de5d51fe2cdfa853b732b1bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0e92542c71335e9943a819c9cbddaeda4aa7f9e7b3a3b0b67a82cb552c4612)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae2df755490d4053f176844f5a055bed7c67f402c3b3abdd7e4540e55ac638d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1550131e7fb5cb8a16b863e9e1f0f79e2a1df3154ca25879441fee72e2fb07f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationTypographyFontFamiliesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyFontFamiliesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1956da8331786715477b91b64a57ae0caeddbf0f0ea41d1c10f3ab26e87bcd01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFontFamily")
    def reset_font_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFontFamily", []))

    @builtins.property
    @jsii.member(jsii_name="fontFamilyInput")
    def font_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fontFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="fontFamily")
    def font_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fontFamily"))

    @font_family.setter
    def font_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444e41f45da3be3fb8365c5d0d084a7a238ca2d483434c8b54865ca5d8f8e9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fontFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62808a4cd153ad8151b5674251868b6a74ac68123abfa80aa0f3bc4be388610a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemeConfigurationTypographyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationTypographyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d928e8c0e1e2969f54e35e59944b139f839cccaec4e3d9de4eb4ed6bd5a1b8ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFontFamilies")
    def put_font_families(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemeConfigurationTypographyFontFamilies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf8a33858538b51c4148d2a3846624024b24e21c936e43d870597c70e0f371b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFontFamilies", [value]))

    @jsii.member(jsii_name="resetFontFamilies")
    def reset_font_families(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFontFamilies", []))

    @builtins.property
    @jsii.member(jsii_name="fontFamilies")
    def font_families(self) -> QuicksightThemeConfigurationTypographyFontFamiliesList:
        return typing.cast(QuicksightThemeConfigurationTypographyFontFamiliesList, jsii.get(self, "fontFamilies"))

    @builtins.property
    @jsii.member(jsii_name="fontFamiliesInput")
    def font_families_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]], jsii.get(self, "fontFamiliesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightThemeConfigurationTypography]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationTypography], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationTypography],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f17ebdd9f65c5c68f04839c19cb5fff1d7e7424f543b29ac753fb528031220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationUiColorPalette",
    jsii_struct_bases=[],
    name_mapping={
        "accent": "accent",
        "accent_foreground": "accentForeground",
        "danger": "danger",
        "danger_foreground": "dangerForeground",
        "dimension": "dimension",
        "dimension_foreground": "dimensionForeground",
        "measure": "measure",
        "measure_foreground": "measureForeground",
        "primary_background": "primaryBackground",
        "primary_foreground": "primaryForeground",
        "secondary_background": "secondaryBackground",
        "secondary_foreground": "secondaryForeground",
        "success": "success",
        "success_foreground": "successForeground",
        "warning": "warning",
        "warning_foreground": "warningForeground",
    },
)
class QuicksightThemeConfigurationUiColorPalette:
    def __init__(
        self,
        *,
        accent: typing.Optional[builtins.str] = None,
        accent_foreground: typing.Optional[builtins.str] = None,
        danger: typing.Optional[builtins.str] = None,
        danger_foreground: typing.Optional[builtins.str] = None,
        dimension: typing.Optional[builtins.str] = None,
        dimension_foreground: typing.Optional[builtins.str] = None,
        measure: typing.Optional[builtins.str] = None,
        measure_foreground: typing.Optional[builtins.str] = None,
        primary_background: typing.Optional[builtins.str] = None,
        primary_foreground: typing.Optional[builtins.str] = None,
        secondary_background: typing.Optional[builtins.str] = None,
        secondary_foreground: typing.Optional[builtins.str] = None,
        success: typing.Optional[builtins.str] = None,
        success_foreground: typing.Optional[builtins.str] = None,
        warning: typing.Optional[builtins.str] = None,
        warning_foreground: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#accent QuicksightTheme#accent}.
        :param accent_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#accent_foreground QuicksightTheme#accent_foreground}.
        :param danger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#danger QuicksightTheme#danger}.
        :param danger_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#danger_foreground QuicksightTheme#danger_foreground}.
        :param dimension: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#dimension QuicksightTheme#dimension}.
        :param dimension_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#dimension_foreground QuicksightTheme#dimension_foreground}.
        :param measure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#measure QuicksightTheme#measure}.
        :param measure_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#measure_foreground QuicksightTheme#measure_foreground}.
        :param primary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#primary_background QuicksightTheme#primary_background}.
        :param primary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#primary_foreground QuicksightTheme#primary_foreground}.
        :param secondary_background: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#secondary_background QuicksightTheme#secondary_background}.
        :param secondary_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#secondary_foreground QuicksightTheme#secondary_foreground}.
        :param success: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#success QuicksightTheme#success}.
        :param success_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#success_foreground QuicksightTheme#success_foreground}.
        :param warning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#warning QuicksightTheme#warning}.
        :param warning_foreground: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#warning_foreground QuicksightTheme#warning_foreground}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b695da53e43dc1943ba8bf1062a6c57dccc7cd0591b356c8ab0c7eeed19d9af0)
            check_type(argname="argument accent", value=accent, expected_type=type_hints["accent"])
            check_type(argname="argument accent_foreground", value=accent_foreground, expected_type=type_hints["accent_foreground"])
            check_type(argname="argument danger", value=danger, expected_type=type_hints["danger"])
            check_type(argname="argument danger_foreground", value=danger_foreground, expected_type=type_hints["danger_foreground"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument dimension_foreground", value=dimension_foreground, expected_type=type_hints["dimension_foreground"])
            check_type(argname="argument measure", value=measure, expected_type=type_hints["measure"])
            check_type(argname="argument measure_foreground", value=measure_foreground, expected_type=type_hints["measure_foreground"])
            check_type(argname="argument primary_background", value=primary_background, expected_type=type_hints["primary_background"])
            check_type(argname="argument primary_foreground", value=primary_foreground, expected_type=type_hints["primary_foreground"])
            check_type(argname="argument secondary_background", value=secondary_background, expected_type=type_hints["secondary_background"])
            check_type(argname="argument secondary_foreground", value=secondary_foreground, expected_type=type_hints["secondary_foreground"])
            check_type(argname="argument success", value=success, expected_type=type_hints["success"])
            check_type(argname="argument success_foreground", value=success_foreground, expected_type=type_hints["success_foreground"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
            check_type(argname="argument warning_foreground", value=warning_foreground, expected_type=type_hints["warning_foreground"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accent is not None:
            self._values["accent"] = accent
        if accent_foreground is not None:
            self._values["accent_foreground"] = accent_foreground
        if danger is not None:
            self._values["danger"] = danger
        if danger_foreground is not None:
            self._values["danger_foreground"] = danger_foreground
        if dimension is not None:
            self._values["dimension"] = dimension
        if dimension_foreground is not None:
            self._values["dimension_foreground"] = dimension_foreground
        if measure is not None:
            self._values["measure"] = measure
        if measure_foreground is not None:
            self._values["measure_foreground"] = measure_foreground
        if primary_background is not None:
            self._values["primary_background"] = primary_background
        if primary_foreground is not None:
            self._values["primary_foreground"] = primary_foreground
        if secondary_background is not None:
            self._values["secondary_background"] = secondary_background
        if secondary_foreground is not None:
            self._values["secondary_foreground"] = secondary_foreground
        if success is not None:
            self._values["success"] = success
        if success_foreground is not None:
            self._values["success_foreground"] = success_foreground
        if warning is not None:
            self._values["warning"] = warning
        if warning_foreground is not None:
            self._values["warning_foreground"] = warning_foreground

    @builtins.property
    def accent(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#accent QuicksightTheme#accent}.'''
        result = self._values.get("accent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accent_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#accent_foreground QuicksightTheme#accent_foreground}.'''
        result = self._values.get("accent_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def danger(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#danger QuicksightTheme#danger}.'''
        result = self._values.get("danger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def danger_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#danger_foreground QuicksightTheme#danger_foreground}.'''
        result = self._values.get("danger_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimension(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#dimension QuicksightTheme#dimension}.'''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimension_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#dimension_foreground QuicksightTheme#dimension_foreground}.'''
        result = self._values.get("dimension_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def measure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#measure QuicksightTheme#measure}.'''
        result = self._values.get("measure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def measure_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#measure_foreground QuicksightTheme#measure_foreground}.'''
        result = self._values.get("measure_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_background(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#primary_background QuicksightTheme#primary_background}.'''
        result = self._values.get("primary_background")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#primary_foreground QuicksightTheme#primary_foreground}.'''
        result = self._values.get("primary_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_background(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#secondary_background QuicksightTheme#secondary_background}.'''
        result = self._values.get("secondary_background")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#secondary_foreground QuicksightTheme#secondary_foreground}.'''
        result = self._values.get("secondary_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#success QuicksightTheme#success}.'''
        result = self._values.get("success")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#success_foreground QuicksightTheme#success_foreground}.'''
        result = self._values.get("success_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#warning QuicksightTheme#warning}.'''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warning_foreground(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#warning_foreground QuicksightTheme#warning_foreground}.'''
        result = self._values.get("warning_foreground")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeConfigurationUiColorPalette(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeConfigurationUiColorPaletteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeConfigurationUiColorPaletteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c5d4501df6378140e795a587e5f62c87fc4583316e0403aaa8fedf9a6800976)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccent")
    def reset_accent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccent", []))

    @jsii.member(jsii_name="resetAccentForeground")
    def reset_accent_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccentForeground", []))

    @jsii.member(jsii_name="resetDanger")
    def reset_danger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDanger", []))

    @jsii.member(jsii_name="resetDangerForeground")
    def reset_danger_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDangerForeground", []))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetDimensionForeground")
    def reset_dimension_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensionForeground", []))

    @jsii.member(jsii_name="resetMeasure")
    def reset_measure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeasure", []))

    @jsii.member(jsii_name="resetMeasureForeground")
    def reset_measure_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeasureForeground", []))

    @jsii.member(jsii_name="resetPrimaryBackground")
    def reset_primary_background(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryBackground", []))

    @jsii.member(jsii_name="resetPrimaryForeground")
    def reset_primary_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryForeground", []))

    @jsii.member(jsii_name="resetSecondaryBackground")
    def reset_secondary_background(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryBackground", []))

    @jsii.member(jsii_name="resetSecondaryForeground")
    def reset_secondary_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryForeground", []))

    @jsii.member(jsii_name="resetSuccess")
    def reset_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccess", []))

    @jsii.member(jsii_name="resetSuccessForeground")
    def reset_success_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessForeground", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @jsii.member(jsii_name="resetWarningForeground")
    def reset_warning_foreground(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarningForeground", []))

    @builtins.property
    @jsii.member(jsii_name="accentForegroundInput")
    def accent_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accentForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="accentInput")
    def accent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accentInput"))

    @builtins.property
    @jsii.member(jsii_name="dangerForegroundInput")
    def danger_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dangerForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="dangerInput")
    def danger_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dangerInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionForegroundInput")
    def dimension_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="measureForegroundInput")
    def measure_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "measureForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="measureInput")
    def measure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "measureInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackgroundInput")
    def primary_background_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryBackgroundInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryForegroundInput")
    def primary_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBackgroundInput")
    def secondary_background_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryBackgroundInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryForegroundInput")
    def secondary_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="successForegroundInput")
    def success_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="successInput")
    def success_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successInput"))

    @builtins.property
    @jsii.member(jsii_name="warningForegroundInput")
    def warning_foreground_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningForegroundInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="accent")
    def accent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accent"))

    @accent.setter
    def accent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca2f4fb1dc60aea5c48d645db402e821fcc57842074baa0bd4c47648e1ac2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accentForeground")
    def accent_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accentForeground"))

    @accent_foreground.setter
    def accent_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c4a3fc5814b2677d7ff952ea14ad3e6fc83cf3b8c1bc4bb341e2668f8b9845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accentForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="danger")
    def danger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "danger"))

    @danger.setter
    def danger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780234f88260f5afb466bbbddf063c86077ce5bc964bd3885527aae4aaddfe3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "danger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dangerForeground")
    def danger_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dangerForeground"))

    @danger_foreground.setter
    def danger_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe4e16d12aad191f3fc6f8b4da4d3252e10d19b255f0311701937b784d7a56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dangerForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimension"))

    @dimension.setter
    def dimension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94eddb123b58abbde25f414a5a717f41257e1f693b4ae84ea54977f20685b130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensionForeground")
    def dimension_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionForeground"))

    @dimension_foreground.setter
    def dimension_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140547e234deb2bc9a46d640095660cf4ae09a16c0a3189e279b9077405dc681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="measure")
    def measure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "measure"))

    @measure.setter
    def measure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b9af75d2f71cc349835b9427f08a90a36de13737d29143ad52e6ba31b28ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "measure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="measureForeground")
    def measure_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "measureForeground"))

    @measure_foreground.setter
    def measure_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6957ea3f96c19c70b84f67eac3cc641f306e44f54750612619f53bcd6f0902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "measureForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryBackground")
    def primary_background(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBackground"))

    @primary_background.setter
    def primary_background(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6505843d9878963ed6685fa27ec96cc9a5141f6ce1cb69831845509340448a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryBackground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryForeground")
    def primary_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryForeground"))

    @primary_foreground.setter
    def primary_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4c93389f221c7a2ce25a3c2dbd401a7a7db2b225df39878a1a369ce912f529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryBackground")
    def secondary_background(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBackground"))

    @secondary_background.setter
    def secondary_background(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1c398f7813f927a1a9c5b32e818ef87c8d23ae981a65696412bb57736a8c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryBackground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryForeground")
    def secondary_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryForeground"))

    @secondary_foreground.setter
    def secondary_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efde5862bba0e3b11d1abc18634db8c299d6ed6295095699a8006d16f4309bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="success")
    def success(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "success"))

    @success.setter
    def success(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef270e4b44e077e5f4628f7e86a02ce474f024d1480fbaaaf18cb844ae65d912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "success", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successForeground")
    def success_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successForeground"))

    @success_foreground.setter
    def success_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895af290689fd6d48702bfb67dbf41c5fec629736fc78d7e63767a4f1b6ed956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d887275cfe8377d9a058e11bff00414313f84ad61e4cc930458a90a8352ec24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warningForeground")
    def warning_foreground(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warningForeground"))

    @warning_foreground.setter
    def warning_foreground(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a534df5ba6d2226095c21f3f452e3e288881febba978499ec3826bd967b2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warningForeground", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightThemeConfigurationUiColorPalette]:
        return typing.cast(typing.Optional[QuicksightThemeConfigurationUiColorPalette], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightThemeConfigurationUiColorPalette],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7926f1b2e4e4a9586e05119be542f428fe0119596f00cdfee8baf301eac54db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemePermissions",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightThemePermissions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#actions QuicksightTheme#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#principal QuicksightTheme#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4934dc33752d566037c911e9b5a7f336de30130e3f932fdd93570c84e0d90493)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#actions QuicksightTheme#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#principal QuicksightTheme#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemePermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemePermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemePermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b91eb8d70c7ec37f99995cc63ce29eb635f3940ced9ce205ceff9ffaba3f1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightThemePermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1888e6b88c2f3f97a577ba1bc6214c9d4e9b03e77bd06653e161d397bece6846)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightThemePermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b34432fbd17e92bff106756dd23f42d3c032defbcb6871f4cdee2cb1a83061)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65a8945248a8e64f2da3c3473a59b09d486c04dc6aa5e4ff239d739291966083)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68bfb508ab1635847df99812a488d3d4ed44370613464888222e7857abe46249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1958b45912786ca39350f426faa354abcbd290c388dd53f0968db525cdd0c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightThemePermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemePermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eeafd1146e060a9a968e912275be6b714208cab8d5bf90b3008a37e2614163b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f6938dbc6184acbd2f532765b01953f437b2361851050e92ea2ff11f8237c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6cee4aa457d6629b2152d0185d2225ede73092a5c41c1402d4a219876cd0d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be51455b46d47c06f77b8af72d4ced46f4a294be87acc23c3619d77dd9b257f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class QuicksightThemeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#create QuicksightTheme#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#delete QuicksightTheme#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#update QuicksightTheme#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97fbc89eb5061ba4f584128fb8c720443fcd09225eae60fb0846fb4d4abe9b4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#create QuicksightTheme#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#delete QuicksightTheme#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_theme#update QuicksightTheme#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightThemeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightThemeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightTheme.QuicksightThemeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5d02cdc7cf5ed0a317aacd294a53e4431fd4ee892ca53324dc63f28dcbd245b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef83b45c4da51e29f36187c234e392bb1596b771de497883dde28bd85b69b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c1acc3816980ecc350d695046b19917f8618085355abda1fa24da7bbee653e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3936711805fea2070f85b653f50673918b14126c87d01af6aac02491772f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19498f4b75789021ddc14a40b35ce715263519b20eeab9bfbd3674736529d04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightTheme",
    "QuicksightThemeConfig",
    "QuicksightThemeConfiguration",
    "QuicksightThemeConfigurationDataColorPalette",
    "QuicksightThemeConfigurationDataColorPaletteOutputReference",
    "QuicksightThemeConfigurationOutputReference",
    "QuicksightThemeConfigurationSheet",
    "QuicksightThemeConfigurationSheetOutputReference",
    "QuicksightThemeConfigurationSheetTile",
    "QuicksightThemeConfigurationSheetTileBorder",
    "QuicksightThemeConfigurationSheetTileBorderOutputReference",
    "QuicksightThemeConfigurationSheetTileLayout",
    "QuicksightThemeConfigurationSheetTileLayoutGutter",
    "QuicksightThemeConfigurationSheetTileLayoutGutterOutputReference",
    "QuicksightThemeConfigurationSheetTileLayoutMargin",
    "QuicksightThemeConfigurationSheetTileLayoutMarginOutputReference",
    "QuicksightThemeConfigurationSheetTileLayoutOutputReference",
    "QuicksightThemeConfigurationSheetTileOutputReference",
    "QuicksightThemeConfigurationTypography",
    "QuicksightThemeConfigurationTypographyFontFamilies",
    "QuicksightThemeConfigurationTypographyFontFamiliesList",
    "QuicksightThemeConfigurationTypographyFontFamiliesOutputReference",
    "QuicksightThemeConfigurationTypographyOutputReference",
    "QuicksightThemeConfigurationUiColorPalette",
    "QuicksightThemeConfigurationUiColorPaletteOutputReference",
    "QuicksightThemePermissions",
    "QuicksightThemePermissionsList",
    "QuicksightThemePermissionsOutputReference",
    "QuicksightThemeTimeouts",
    "QuicksightThemeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__772be6d7f751e3355ac480fe17e3d3450cd4fc6165a37aa2b4063ce798d1ac39(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    base_theme_id: builtins.str,
    name: builtins.str,
    theme_id: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[QuicksightThemeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemePermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[QuicksightThemeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_description: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0cd3dfccc06282fb74dce826a5d894cfc9db9994e1b9809095299c9144181dd1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b237f2749f33d0e4744d4644411e8d3395d7c82d01daaca8c9eae5a037acaa4d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemePermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725a10f4ff73d8c7664d764c02761d201911a26efa7c5c3ec54dd580de8bc20e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11dc6d5184f33bb514a4db706a942441529568a1d5604d3e0fd4e1724d4b87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334e03845170e4b7086a08ae1fcc14014a37f7f9cc449cdbe96766bc98420c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8ad125d36dfc4671698dccddab967cc9bfc80b6da0b807516af84cac0f73a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8538ebd379f88734275e935dce8cd766ecf1ea0e028bccf91b6ca34fc96e36d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0529355c1b00ce5fe33bad6a8f418773a436b89867a0f0ec3256c58fa5e617(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe4cb44426f6347f2f4db5b3573492c565a1aa198180f3b365c6979786cf228(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f829630ca303dfb7377b4923b41633071903ef8b03df78604e504fdeabe3457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd7431689975c5fb560cb88e609c81af0ebd219e550be481499abce490f8d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7c5a320bb8a61a2b38207ca96140d9b6fce064b6ff7e35862bd23c844536e9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    base_theme_id: builtins.str,
    name: builtins.str,
    theme_id: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[QuicksightThemeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemePermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[QuicksightThemeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3428c4adfba7c0cf96cc8afc711c889a5c4fecdda3665865dc61264cdb579587(
    *,
    data_color_palette: typing.Optional[typing.Union[QuicksightThemeConfigurationDataColorPalette, typing.Dict[builtins.str, typing.Any]]] = None,
    sheet: typing.Optional[typing.Union[QuicksightThemeConfigurationSheet, typing.Dict[builtins.str, typing.Any]]] = None,
    typography: typing.Optional[typing.Union[QuicksightThemeConfigurationTypography, typing.Dict[builtins.str, typing.Any]]] = None,
    ui_color_palette: typing.Optional[typing.Union[QuicksightThemeConfigurationUiColorPalette, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00aa6b3ba58756dd9e8eee23007063a3436abedc8a53f1613263f6f48f41dffd(
    *,
    colors: typing.Optional[typing.Sequence[builtins.str]] = None,
    empty_fill_color: typing.Optional[builtins.str] = None,
    min_max_gradient: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b671adc4a8420e67c38017155e21c7bb51a11f8a6e4fb2d9311b6c56e728f72a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c850919875fa99d9ee901a0e3e9eb43182bfe78548164828b4719917f8483725(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98d1cd14155e4c0cc4acad007bef782f50dd6f630031139ce953273125e28bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec634f662c4c4244d39ad3ba6b7dc562dc5ad650e216c590f4aa8c992470928(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733adebf86fdaacc9a814fa358a415771315e28885c7f2893aaa1dfe00093e86(
    value: typing.Optional[QuicksightThemeConfigurationDataColorPalette],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f2d08868d804a22b30d677d7c22215de21edafcc53ac6ce6142a8f15ee03b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3e588f6e57b494cd5900bac5d42af8e06c7525d2f301223f6ce3ff00661455(
    value: typing.Optional[QuicksightThemeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4bb469775a4a4d9e56c9bf5d96a1e40ad441b584af1202973937c01c8ec2fc(
    *,
    tile: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTile, typing.Dict[builtins.str, typing.Any]]] = None,
    tile_layout: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileLayout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e419e820e22d7f16316a6b30ecac4877960624527f0ed79032b1a0828d8969e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cda6a7def02ed2dc0b4af65ea38b1658f5a254f5e24da357215967b42ce6f2e(
    value: typing.Optional[QuicksightThemeConfigurationSheet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362002f0dfd6db1b21b5971ed92f26233ab7b5f4bc20afaa2d8d689eaeee58fd(
    *,
    border: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileBorder, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f0350d306c7b31c6f905df4c8ed719451e7121d9163f9b31cdf06a9212a26a(
    *,
    show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3f956d2c63c8491ef07c46ad35540f003519833cb56125cd010441db3f190f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7717c2071970373ed2fc0f450a1618090ee52150635cb9dea6cd3125ea96ee71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a394e7fc8e0587593f0a076084d6c37d96196e6857ee40b99761a8b94a14237d(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileBorder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8997186b2158b522d77ae391f4f7c605c0c90bbdf92f618c1fb92173bc57e710(
    *,
    gutter: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileLayoutGutter, typing.Dict[builtins.str, typing.Any]]] = None,
    margin: typing.Optional[typing.Union[QuicksightThemeConfigurationSheetTileLayoutMargin, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21347ef5832ace329e1276b142e8f84bfd3cf92ef56d1ff68b7bf3769d8b70c(
    *,
    show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfe38ec4b88c8fbd346bdcb0a14f7623ac0fb8fb9d9737578c402fb9dc89d2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0789cf29b9f47730974ac18c8136229b8eb86b00a15ae8641c444faeeb63414(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728cf3a56c65565ce0271fd97c4b6390c2887390066632effb5bb55e04a2289d(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutGutter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159b44a9831117999e3c4336de3f54178a10f0a9045fc9dcbb156244d8655924(
    *,
    show: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8238763fe5e48b343830553f5ec3a5652457dcd5d2b9c9b345eb4d335d5b05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12e5c31b241a74955485ef14639295ff3005b2e1da5e8d2cd947776087c5a87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94477cc5e75e7a61ec9e82c16fb57c33f3dcec1983bc5a87058f021470b2824c(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileLayoutMargin],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bb9b3524daa606e48d4a11ffc4f70c23fa22e3c1ad8926eb41ed132cd6c53f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce06a9613921e648f351cbf8e8bfc3216ba9e73e904a7fac10f92ef410ea0c1(
    value: typing.Optional[QuicksightThemeConfigurationSheetTileLayout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a82a79c5e4778a878711fc27e19e1da0f03a60c1fb65857b6df4833372cf07e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68409a362d2ef3de5f5a909c79cf6febb06e75324fbfa15d18d3fe7d07173bcb(
    value: typing.Optional[QuicksightThemeConfigurationSheetTile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55ec4282f7d32576b641c450c4e6cfb59e81105c02da60a90c41b0e218bfb03(
    *,
    font_families: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemeConfigurationTypographyFontFamilies, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943019b76160b2b6a496b84a4b53cfb0b527f424ea70b97ddd3aa5a60788d177(
    *,
    font_family: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51978e3fa8d8f9df509114804896f923cb00eaf21e1ab979d5e5207fa2cad751(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438ea4bdf690c301223b004db474d5a112e56a8264b8ada0d44198a57efbad13(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dc1276801a60116b09e212a5388ebfee353495de5d51fe2cdfa853b732b1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0e92542c71335e9943a819c9cbddaeda4aa7f9e7b3a3b0b67a82cb552c4612(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2df755490d4053f176844f5a055bed7c67f402c3b3abdd7e4540e55ac638d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1550131e7fb5cb8a16b863e9e1f0f79e2a1df3154ca25879441fee72e2fb07f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemeConfigurationTypographyFontFamilies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1956da8331786715477b91b64a57ae0caeddbf0f0ea41d1c10f3ab26e87bcd01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444e41f45da3be3fb8365c5d0d084a7a238ca2d483434c8b54865ca5d8f8e9ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62808a4cd153ad8151b5674251868b6a74ac68123abfa80aa0f3bc4be388610a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeConfigurationTypographyFontFamilies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d928e8c0e1e2969f54e35e59944b139f839cccaec4e3d9de4eb4ed6bd5a1b8ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf8a33858538b51c4148d2a3846624024b24e21c936e43d870597c70e0f371b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightThemeConfigurationTypographyFontFamilies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f17ebdd9f65c5c68f04839c19cb5fff1d7e7424f543b29ac753fb528031220(
    value: typing.Optional[QuicksightThemeConfigurationTypography],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b695da53e43dc1943ba8bf1062a6c57dccc7cd0591b356c8ab0c7eeed19d9af0(
    *,
    accent: typing.Optional[builtins.str] = None,
    accent_foreground: typing.Optional[builtins.str] = None,
    danger: typing.Optional[builtins.str] = None,
    danger_foreground: typing.Optional[builtins.str] = None,
    dimension: typing.Optional[builtins.str] = None,
    dimension_foreground: typing.Optional[builtins.str] = None,
    measure: typing.Optional[builtins.str] = None,
    measure_foreground: typing.Optional[builtins.str] = None,
    primary_background: typing.Optional[builtins.str] = None,
    primary_foreground: typing.Optional[builtins.str] = None,
    secondary_background: typing.Optional[builtins.str] = None,
    secondary_foreground: typing.Optional[builtins.str] = None,
    success: typing.Optional[builtins.str] = None,
    success_foreground: typing.Optional[builtins.str] = None,
    warning: typing.Optional[builtins.str] = None,
    warning_foreground: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5d4501df6378140e795a587e5f62c87fc4583316e0403aaa8fedf9a6800976(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca2f4fb1dc60aea5c48d645db402e821fcc57842074baa0bd4c47648e1ac2ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c4a3fc5814b2677d7ff952ea14ad3e6fc83cf3b8c1bc4bb341e2668f8b9845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780234f88260f5afb466bbbddf063c86077ce5bc964bd3885527aae4aaddfe3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe4e16d12aad191f3fc6f8b4da4d3252e10d19b255f0311701937b784d7a56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94eddb123b58abbde25f414a5a717f41257e1f693b4ae84ea54977f20685b130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140547e234deb2bc9a46d640095660cf4ae09a16c0a3189e279b9077405dc681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b9af75d2f71cc349835b9427f08a90a36de13737d29143ad52e6ba31b28ffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6957ea3f96c19c70b84f67eac3cc641f306e44f54750612619f53bcd6f0902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6505843d9878963ed6685fa27ec96cc9a5141f6ce1cb69831845509340448a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4c93389f221c7a2ce25a3c2dbd401a7a7db2b225df39878a1a369ce912f529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1c398f7813f927a1a9c5b32e818ef87c8d23ae981a65696412bb57736a8c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efde5862bba0e3b11d1abc18634db8c299d6ed6295095699a8006d16f4309bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef270e4b44e077e5f4628f7e86a02ce474f024d1480fbaaaf18cb844ae65d912(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895af290689fd6d48702bfb67dbf41c5fec629736fc78d7e63767a4f1b6ed956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d887275cfe8377d9a058e11bff00414313f84ad61e4cc930458a90a8352ec24e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a534df5ba6d2226095c21f3f452e3e288881febba978499ec3826bd967b2a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7926f1b2e4e4a9586e05119be542f428fe0119596f00cdfee8baf301eac54db4(
    value: typing.Optional[QuicksightThemeConfigurationUiColorPalette],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4934dc33752d566037c911e9b5a7f336de30130e3f932fdd93570c84e0d90493(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b91eb8d70c7ec37f99995cc63ce29eb635f3940ced9ce205ceff9ffaba3f1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1888e6b88c2f3f97a577ba1bc6214c9d4e9b03e77bd06653e161d397bece6846(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b34432fbd17e92bff106756dd23f42d3c032defbcb6871f4cdee2cb1a83061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a8945248a8e64f2da3c3473a59b09d486c04dc6aa5e4ff239d739291966083(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bfb508ab1635847df99812a488d3d4ed44370613464888222e7857abe46249(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1958b45912786ca39350f426faa354abcbd290c388dd53f0968db525cdd0c3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightThemePermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eeafd1146e060a9a968e912275be6b714208cab8d5bf90b3008a37e2614163b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6938dbc6184acbd2f532765b01953f437b2361851050e92ea2ff11f8237c87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6cee4aa457d6629b2152d0185d2225ede73092a5c41c1402d4a219876cd0d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be51455b46d47c06f77b8af72d4ced46f4a294be87acc23c3619d77dd9b257f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemePermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97fbc89eb5061ba4f584128fb8c720443fcd09225eae60fb0846fb4d4abe9b4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d02cdc7cf5ed0a317aacd294a53e4431fd4ee892ca53324dc63f28dcbd245b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef83b45c4da51e29f36187c234e392bb1596b771de497883dde28bd85b69b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c1acc3816980ecc350d695046b19917f8618085355abda1fa24da7bbee653e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3936711805fea2070f85b653f50673918b14126c87d01af6aac02491772f71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19498f4b75789021ddc14a40b35ce715263519b20eeab9bfbd3674736529d04d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightThemeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
