r'''
# `aws_rbin_rule`

Refer to the Terraform Registry for docs: [`aws_rbin_rule`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule).
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


class RbinRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule aws_rbin_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        resource_type: builtins.str,
        retention_period: typing.Union["RbinRuleRetentionPeriod", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        exclude_resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleExcludeResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lock_configuration: typing.Optional[typing.Union["RbinRuleLockConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RbinRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule aws_rbin_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_type RbinRule#resource_type}.
        :param retention_period: retention_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period RbinRule#retention_period}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#description RbinRule#description}.
        :param exclude_resource_tags: exclude_resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#exclude_resource_tags RbinRule#exclude_resource_tags}
        :param lock_configuration: lock_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#lock_configuration RbinRule#lock_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#region RbinRule#region}
        :param resource_tags: resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tags RbinRule#resource_tags}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#tags RbinRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#tags_all RbinRule#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#timeouts RbinRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4dd2a58618685120453a7d3f22426254e1c16aaf91600e2cbcbeba0ea9b1f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = RbinRuleConfig(
            resource_type=resource_type,
            retention_period=retention_period,
            description=description,
            exclude_resource_tags=exclude_resource_tags,
            lock_configuration=lock_configuration,
            region=region,
            resource_tags=resource_tags,
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

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a RbinRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RbinRule to import.
        :param import_from_id: The id of the existing RbinRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RbinRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715aa4f253dae0222655f1cf34d8025a3b8b1c63de9be9ea2a83624e77bb4a48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExcludeResourceTags")
    def put_exclude_resource_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleExcludeResourceTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbb71098ca7894be2b7bf87f1bac02231cc29bc3d91a4225390c455024ba71b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludeResourceTags", [value]))

    @jsii.member(jsii_name="putLockConfiguration")
    def put_lock_configuration(
        self,
        *,
        unlock_delay: typing.Union["RbinRuleLockConfigurationUnlockDelay", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param unlock_delay: unlock_delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay RbinRule#unlock_delay}
        '''
        value = RbinRuleLockConfiguration(unlock_delay=unlock_delay)

        return typing.cast(None, jsii.invoke(self, "putLockConfiguration", [value]))

    @jsii.member(jsii_name="putResourceTags")
    def put_resource_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleResourceTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a11ee68d0053ef81be98fbe9f68116b863abe184df965dc6b388a4977c44b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceTags", [value]))

    @jsii.member(jsii_name="putRetentionPeriod")
    def put_retention_period(
        self,
        *,
        retention_period_unit: builtins.str,
        retention_period_value: jsii.Number,
    ) -> None:
        '''
        :param retention_period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period_unit RbinRule#retention_period_unit}.
        :param retention_period_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period_value RbinRule#retention_period_value}.
        '''
        value = RbinRuleRetentionPeriod(
            retention_period_unit=retention_period_unit,
            retention_period_value=retention_period_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPeriod", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#create RbinRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#delete RbinRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#update RbinRule#update}.
        '''
        value = RbinRuleTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExcludeResourceTags")
    def reset_exclude_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeResourceTags", []))

    @jsii.member(jsii_name="resetLockConfiguration")
    def reset_lock_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResourceTags")
    def reset_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTags", []))

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
    @jsii.member(jsii_name="excludeResourceTags")
    def exclude_resource_tags(self) -> "RbinRuleExcludeResourceTagsList":
        return typing.cast("RbinRuleExcludeResourceTagsList", jsii.get(self, "excludeResourceTags"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lockConfiguration")
    def lock_configuration(self) -> "RbinRuleLockConfigurationOutputReference":
        return typing.cast("RbinRuleLockConfigurationOutputReference", jsii.get(self, "lockConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lockEndTime")
    def lock_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockEndTime"))

    @builtins.property
    @jsii.member(jsii_name="lockState")
    def lock_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockState"))

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(self) -> "RbinRuleResourceTagsList":
        return typing.cast("RbinRuleResourceTagsList", jsii.get(self, "resourceTags"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> "RbinRuleRetentionPeriodOutputReference":
        return typing.cast("RbinRuleRetentionPeriodOutputReference", jsii.get(self, "retentionPeriod"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RbinRuleTimeoutsOutputReference":
        return typing.cast("RbinRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeResourceTagsInput")
    def exclude_resource_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleExcludeResourceTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleExcludeResourceTags"]]], jsii.get(self, "excludeResourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="lockConfigurationInput")
    def lock_configuration_input(self) -> typing.Optional["RbinRuleLockConfiguration"]:
        return typing.cast(typing.Optional["RbinRuleLockConfiguration"], jsii.get(self, "lockConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagsInput")
    def resource_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]], jsii.get(self, "resourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(self) -> typing.Optional["RbinRuleRetentionPeriod"]:
        return typing.cast(typing.Optional["RbinRuleRetentionPeriod"], jsii.get(self, "retentionPeriodInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RbinRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RbinRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552353b8ce34b394da9ef24325b7ecbe3a9cae13667bbe48ad8a11610e4101e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db0febc301097ef64afc799f95c0ef2cb3fa2dc684d3d04cc6ab55cf25689d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c69416bd1e9430b71cf5fb54a8a1c7e181ec170ba6a8c96ab67c8d89414d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bb22ad5160af0ae76a87f4cdb5c3ec640c3838d352cd5d07afd94d5319defd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9e4aaa6c63bc2f7866ae2bddd4f51cad5362b4cac9953da2acee07b6479b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "resource_type": "resourceType",
        "retention_period": "retentionPeriod",
        "description": "description",
        "exclude_resource_tags": "excludeResourceTags",
        "lock_configuration": "lockConfiguration",
        "region": "region",
        "resource_tags": "resourceTags",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class RbinRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resource_type: builtins.str,
        retention_period: typing.Union["RbinRuleRetentionPeriod", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        exclude_resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleExcludeResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lock_configuration: typing.Optional[typing.Union["RbinRuleLockConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RbinRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_type RbinRule#resource_type}.
        :param retention_period: retention_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period RbinRule#retention_period}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#description RbinRule#description}.
        :param exclude_resource_tags: exclude_resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#exclude_resource_tags RbinRule#exclude_resource_tags}
        :param lock_configuration: lock_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#lock_configuration RbinRule#lock_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#region RbinRule#region}
        :param resource_tags: resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tags RbinRule#resource_tags}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#tags RbinRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#tags_all RbinRule#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#timeouts RbinRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(retention_period, dict):
            retention_period = RbinRuleRetentionPeriod(**retention_period)
        if isinstance(lock_configuration, dict):
            lock_configuration = RbinRuleLockConfiguration(**lock_configuration)
        if isinstance(timeouts, dict):
            timeouts = RbinRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455ed8811d549758cb62add3b62d4cc3f603d958fb6a5098ac36a39eb9fc0c04)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclude_resource_tags", value=exclude_resource_tags, expected_type=type_hints["exclude_resource_tags"])
            check_type(argname="argument lock_configuration", value=lock_configuration, expected_type=type_hints["lock_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_type": resource_type,
            "retention_period": retention_period,
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
        if exclude_resource_tags is not None:
            self._values["exclude_resource_tags"] = exclude_resource_tags
        if lock_configuration is not None:
            self._values["lock_configuration"] = lock_configuration
        if region is not None:
            self._values["region"] = region
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
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
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_type RbinRule#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period(self) -> "RbinRuleRetentionPeriod":
        '''retention_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period RbinRule#retention_period}
        '''
        result = self._values.get("retention_period")
        assert result is not None, "Required property 'retention_period' is missing"
        return typing.cast("RbinRuleRetentionPeriod", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#description RbinRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleExcludeResourceTags"]]]:
        '''exclude_resource_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#exclude_resource_tags RbinRule#exclude_resource_tags}
        '''
        result = self._values.get("exclude_resource_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleExcludeResourceTags"]]], result)

    @builtins.property
    def lock_configuration(self) -> typing.Optional["RbinRuleLockConfiguration"]:
        '''lock_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#lock_configuration RbinRule#lock_configuration}
        '''
        result = self._values.get("lock_configuration")
        return typing.cast(typing.Optional["RbinRuleLockConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#region RbinRule#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]]:
        '''resource_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tags RbinRule#resource_tags}
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#tags RbinRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#tags_all RbinRule#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RbinRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#timeouts RbinRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RbinRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleExcludeResourceTags",
    jsii_struct_bases=[],
    name_mapping={
        "resource_tag_key": "resourceTagKey",
        "resource_tag_value": "resourceTagValue",
    },
)
class RbinRuleExcludeResourceTags:
    def __init__(
        self,
        *,
        resource_tag_key: builtins.str,
        resource_tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_key RbinRule#resource_tag_key}.
        :param resource_tag_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_value RbinRule#resource_tag_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ddd08350d2cf21fd7202ff8fe2a0751aeb367ba66c168d5990106b9ba6391d)
            check_type(argname="argument resource_tag_key", value=resource_tag_key, expected_type=type_hints["resource_tag_key"])
            check_type(argname="argument resource_tag_value", value=resource_tag_value, expected_type=type_hints["resource_tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_tag_key": resource_tag_key,
        }
        if resource_tag_value is not None:
            self._values["resource_tag_value"] = resource_tag_value

    @builtins.property
    def resource_tag_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_key RbinRule#resource_tag_key}.'''
        result = self._values.get("resource_tag_key")
        assert result is not None, "Required property 'resource_tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_tag_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_value RbinRule#resource_tag_value}.'''
        result = self._values.get("resource_tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleExcludeResourceTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleExcludeResourceTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleExcludeResourceTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__058a3a383b5e6545db494e2e343e4395f1888f708a6c4bcf06bdd11d044def68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RbinRuleExcludeResourceTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758f5cc71e8d6b841b19a91bee6088449d38d901efa7962dc59e12e016d5e9af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RbinRuleExcludeResourceTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53a1e369ab462a81492a262a5f38d8f4cf9fbd19a624d5e9e1fe04025e1d28b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d461e8500e57d319c865ab3bf986d7e336bb602838e5e8a07074705e4084efd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99801b840aafe76cdd37ace1f9be958d6cf56ccd80a9a4157189cbbf6e5bfe2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleExcludeResourceTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleExcludeResourceTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleExcludeResourceTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fe3efac7b38f88894fa7facdbbbbb70b383089a0b0219b7e84468b8b5e445a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RbinRuleExcludeResourceTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleExcludeResourceTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a380f09a34db6053becf06c5c4c28ff91a8a97e97d4247e98862b6ea4f032911)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceTagValue")
    def reset_resource_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="resourceTagKeyInput")
    def resource_tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagValueInput")
    def resource_tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagKey")
    def resource_tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTagKey"))

    @resource_tag_key.setter
    def resource_tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aada8ddbcf80b3cac7ecd53095c1a2fd71466f840d3ba56d21388bfb1dfb747e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTagValue")
    def resource_tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTagValue"))

    @resource_tag_value.setter
    def resource_tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ea0c79f08b1ab90e4becb169b6eb26273e99ef095c5ec436094be5eaa8894d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleExcludeResourceTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleExcludeResourceTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleExcludeResourceTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128f482be8d7bf0b5c38f6b149a970c3c8c64be9c8b8a5997fdbb376da445755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleLockConfiguration",
    jsii_struct_bases=[],
    name_mapping={"unlock_delay": "unlockDelay"},
)
class RbinRuleLockConfiguration:
    def __init__(
        self,
        *,
        unlock_delay: typing.Union["RbinRuleLockConfigurationUnlockDelay", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param unlock_delay: unlock_delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay RbinRule#unlock_delay}
        '''
        if isinstance(unlock_delay, dict):
            unlock_delay = RbinRuleLockConfigurationUnlockDelay(**unlock_delay)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f4dbde718adc81a5b542a4c1c6cb1f105d82ca8014d89d7d52282d1e2fc089)
            check_type(argname="argument unlock_delay", value=unlock_delay, expected_type=type_hints["unlock_delay"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unlock_delay": unlock_delay,
        }

    @builtins.property
    def unlock_delay(self) -> "RbinRuleLockConfigurationUnlockDelay":
        '''unlock_delay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay RbinRule#unlock_delay}
        '''
        result = self._values.get("unlock_delay")
        assert result is not None, "Required property 'unlock_delay' is missing"
        return typing.cast("RbinRuleLockConfigurationUnlockDelay", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleLockConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleLockConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleLockConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32566986f37e86c67581d234e4696abd88d1471d88ed143f3ef36d553b3bfa66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUnlockDelay")
    def put_unlock_delay(
        self,
        *,
        unlock_delay_unit: builtins.str,
        unlock_delay_value: jsii.Number,
    ) -> None:
        '''
        :param unlock_delay_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay_unit RbinRule#unlock_delay_unit}.
        :param unlock_delay_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay_value RbinRule#unlock_delay_value}.
        '''
        value = RbinRuleLockConfigurationUnlockDelay(
            unlock_delay_unit=unlock_delay_unit, unlock_delay_value=unlock_delay_value
        )

        return typing.cast(None, jsii.invoke(self, "putUnlockDelay", [value]))

    @builtins.property
    @jsii.member(jsii_name="unlockDelay")
    def unlock_delay(self) -> "RbinRuleLockConfigurationUnlockDelayOutputReference":
        return typing.cast("RbinRuleLockConfigurationUnlockDelayOutputReference", jsii.get(self, "unlockDelay"))

    @builtins.property
    @jsii.member(jsii_name="unlockDelayInput")
    def unlock_delay_input(
        self,
    ) -> typing.Optional["RbinRuleLockConfigurationUnlockDelay"]:
        return typing.cast(typing.Optional["RbinRuleLockConfigurationUnlockDelay"], jsii.get(self, "unlockDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RbinRuleLockConfiguration]:
        return typing.cast(typing.Optional[RbinRuleLockConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RbinRuleLockConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cbdafc02679e58f90874a2e3f6ff8596dae241e5a604c3e4d59dfbfcc38fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleLockConfigurationUnlockDelay",
    jsii_struct_bases=[],
    name_mapping={
        "unlock_delay_unit": "unlockDelayUnit",
        "unlock_delay_value": "unlockDelayValue",
    },
)
class RbinRuleLockConfigurationUnlockDelay:
    def __init__(
        self,
        *,
        unlock_delay_unit: builtins.str,
        unlock_delay_value: jsii.Number,
    ) -> None:
        '''
        :param unlock_delay_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay_unit RbinRule#unlock_delay_unit}.
        :param unlock_delay_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay_value RbinRule#unlock_delay_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bef0ea2670db79bf0822fcfcd5719ed3be54bef7124292f9228413df75380cc)
            check_type(argname="argument unlock_delay_unit", value=unlock_delay_unit, expected_type=type_hints["unlock_delay_unit"])
            check_type(argname="argument unlock_delay_value", value=unlock_delay_value, expected_type=type_hints["unlock_delay_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unlock_delay_unit": unlock_delay_unit,
            "unlock_delay_value": unlock_delay_value,
        }

    @builtins.property
    def unlock_delay_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay_unit RbinRule#unlock_delay_unit}.'''
        result = self._values.get("unlock_delay_unit")
        assert result is not None, "Required property 'unlock_delay_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unlock_delay_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#unlock_delay_value RbinRule#unlock_delay_value}.'''
        result = self._values.get("unlock_delay_value")
        assert result is not None, "Required property 'unlock_delay_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleLockConfigurationUnlockDelay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleLockConfigurationUnlockDelayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleLockConfigurationUnlockDelayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cc23a49515d9fcc48fc8bdb056302f91a0373c9cbd3571b604a0cbc973fa828)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unlockDelayUnitInput")
    def unlock_delay_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unlockDelayUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="unlockDelayValueInput")
    def unlock_delay_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unlockDelayValueInput"))

    @builtins.property
    @jsii.member(jsii_name="unlockDelayUnit")
    def unlock_delay_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unlockDelayUnit"))

    @unlock_delay_unit.setter
    def unlock_delay_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527e6759291df44f05fcecfb4d04de500ad2ff963306ba39e87ee6f495f8a6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unlockDelayUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unlockDelayValue")
    def unlock_delay_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unlockDelayValue"))

    @unlock_delay_value.setter
    def unlock_delay_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909708a266231c7c760eef6fe933452946e4fce06847bbb7cdf9efc8a2c0e431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unlockDelayValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RbinRuleLockConfigurationUnlockDelay]:
        return typing.cast(typing.Optional[RbinRuleLockConfigurationUnlockDelay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RbinRuleLockConfigurationUnlockDelay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e3c3849d887207be539b2505242d0e584b527729bb00fef3fded496deec069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleResourceTags",
    jsii_struct_bases=[],
    name_mapping={
        "resource_tag_key": "resourceTagKey",
        "resource_tag_value": "resourceTagValue",
    },
)
class RbinRuleResourceTags:
    def __init__(
        self,
        *,
        resource_tag_key: builtins.str,
        resource_tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_key RbinRule#resource_tag_key}.
        :param resource_tag_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_value RbinRule#resource_tag_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c853e21cff1fdf9c1c8fc2f3880a34c1d3436aa82344e730eaf821a80b2484)
            check_type(argname="argument resource_tag_key", value=resource_tag_key, expected_type=type_hints["resource_tag_key"])
            check_type(argname="argument resource_tag_value", value=resource_tag_value, expected_type=type_hints["resource_tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_tag_key": resource_tag_key,
        }
        if resource_tag_value is not None:
            self._values["resource_tag_value"] = resource_tag_value

    @builtins.property
    def resource_tag_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_key RbinRule#resource_tag_key}.'''
        result = self._values.get("resource_tag_key")
        assert result is not None, "Required property 'resource_tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_tag_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#resource_tag_value RbinRule#resource_tag_value}.'''
        result = self._values.get("resource_tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleResourceTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleResourceTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleResourceTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69723c043c17ce9daf3b57628ce39cf074b7783c92d7d778ab3e4a695e3473e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RbinRuleResourceTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe87f9d8309194dd7d56d240c7a993906bdf15304d665750489b27389f7851d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RbinRuleResourceTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12956d601b8e5f8fa4892228841c2d0b95446fa531530c5134740cd2c4383065)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0738cd35c28cf43b79f27482db85fc3d5304d5afd852504761057ca648fbb33a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0226aaef0d14d94bf21c4e692936b6eb77b687c6c8a8f925e633591520bc99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f172ac26b1aacab749ed4590bab2e882603f36aba5215f1f1733ffc2600e82a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RbinRuleResourceTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleResourceTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32078251ae3629bedc223117883daf8b1471b4c7a042d07d3a40ce1a5e747ce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceTagValue")
    def reset_resource_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="resourceTagKeyInput")
    def resource_tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagValueInput")
    def resource_tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagKey")
    def resource_tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTagKey"))

    @resource_tag_key.setter
    def resource_tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4507e7eb83e18bbdbcfb84bb10c10cc9285e55032074eb0c5711e6fd6dc3b48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTagValue")
    def resource_tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTagValue"))

    @resource_tag_value.setter
    def resource_tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a4793b6d8bd9fe8c0aa323918ca7b80b4b06b695d5855760ad4291476d1326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9093e07b897f3e0407da3b2f0b2b9fc163954758cdb34bebba667c38e6e91891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleRetentionPeriod",
    jsii_struct_bases=[],
    name_mapping={
        "retention_period_unit": "retentionPeriodUnit",
        "retention_period_value": "retentionPeriodValue",
    },
)
class RbinRuleRetentionPeriod:
    def __init__(
        self,
        *,
        retention_period_unit: builtins.str,
        retention_period_value: jsii.Number,
    ) -> None:
        '''
        :param retention_period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period_unit RbinRule#retention_period_unit}.
        :param retention_period_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period_value RbinRule#retention_period_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d9985e3ecccc7730b64b027535ef52c181cdadc3a41ccc7131bd2d997df233)
            check_type(argname="argument retention_period_unit", value=retention_period_unit, expected_type=type_hints["retention_period_unit"])
            check_type(argname="argument retention_period_value", value=retention_period_value, expected_type=type_hints["retention_period_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_period_unit": retention_period_unit,
            "retention_period_value": retention_period_value,
        }

    @builtins.property
    def retention_period_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period_unit RbinRule#retention_period_unit}.'''
        result = self._values.get("retention_period_unit")
        assert result is not None, "Required property 'retention_period_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#retention_period_value RbinRule#retention_period_value}.'''
        result = self._values.get("retention_period_value")
        assert result is not None, "Required property 'retention_period_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleRetentionPeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleRetentionPeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleRetentionPeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__814cca9a25b0505d86cece474af124223aff0f65a3201c15be87c3964fcce29e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodUnitInput")
    def retention_period_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPeriodUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodValueInput")
    def retention_period_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodValueInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodUnit")
    def retention_period_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPeriodUnit"))

    @retention_period_unit.setter
    def retention_period_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed4955583dacffafb82aa15e2451a08043f3ac9b2601d0d844352e47a8d2d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodValue")
    def retention_period_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodValue"))

    @retention_period_value.setter
    def retention_period_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4511350459f7376bbdee416af306cc6fdd797b1d65f1a0415650878039705d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RbinRuleRetentionPeriod]:
        return typing.cast(typing.Optional[RbinRuleRetentionPeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RbinRuleRetentionPeriod]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a7bdbe2d64cd602560d1d672ee4b99ccf18407d4dc23b465a240dda713bf70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RbinRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#create RbinRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#delete RbinRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#update RbinRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5ebbe455f7c2cb579dddbc7e4e13279273bd062b823ea4f46df7656822afd8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#create RbinRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#delete RbinRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/rbin_rule#update RbinRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.rbinRule.RbinRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56db63f0a4440ea9deff461e1e97e9409dcb10a34111a0dea6ceacfe768a66b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91c7f989bd307c30f5c16c948b923787b2d2bb4998cbd4c4e0ddaeff8f26954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55035739de93167d9b9968b64b76759db05524fc56e881eeb65f680ded015c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3cd2389365e7dd881f75ed9a50a3ee480cb62efb4d467a6e94a6d393b1b89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f617fb819a82d59c6a74df923889ffd5cbcf63bafcf0892b56e09a907fcb7d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RbinRule",
    "RbinRuleConfig",
    "RbinRuleExcludeResourceTags",
    "RbinRuleExcludeResourceTagsList",
    "RbinRuleExcludeResourceTagsOutputReference",
    "RbinRuleLockConfiguration",
    "RbinRuleLockConfigurationOutputReference",
    "RbinRuleLockConfigurationUnlockDelay",
    "RbinRuleLockConfigurationUnlockDelayOutputReference",
    "RbinRuleResourceTags",
    "RbinRuleResourceTagsList",
    "RbinRuleResourceTagsOutputReference",
    "RbinRuleRetentionPeriod",
    "RbinRuleRetentionPeriodOutputReference",
    "RbinRuleTimeouts",
    "RbinRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6c4dd2a58618685120453a7d3f22426254e1c16aaf91600e2cbcbeba0ea9b1f7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    resource_type: builtins.str,
    retention_period: typing.Union[RbinRuleRetentionPeriod, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    exclude_resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleExcludeResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lock_configuration: typing.Optional[typing.Union[RbinRuleLockConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RbinRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__715aa4f253dae0222655f1cf34d8025a3b8b1c63de9be9ea2a83624e77bb4a48(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbb71098ca7894be2b7bf87f1bac02231cc29bc3d91a4225390c455024ba71b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleExcludeResourceTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a11ee68d0053ef81be98fbe9f68116b863abe184df965dc6b388a4977c44b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleResourceTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552353b8ce34b394da9ef24325b7ecbe3a9cae13667bbe48ad8a11610e4101e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db0febc301097ef64afc799f95c0ef2cb3fa2dc684d3d04cc6ab55cf25689d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c69416bd1e9430b71cf5fb54a8a1c7e181ec170ba6a8c96ab67c8d89414d3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bb22ad5160af0ae76a87f4cdb5c3ec640c3838d352cd5d07afd94d5319defd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9e4aaa6c63bc2f7866ae2bddd4f51cad5362b4cac9953da2acee07b6479b17(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455ed8811d549758cb62add3b62d4cc3f603d958fb6a5098ac36a39eb9fc0c04(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_type: builtins.str,
    retention_period: typing.Union[RbinRuleRetentionPeriod, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    exclude_resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleExcludeResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lock_configuration: typing.Optional[typing.Union[RbinRuleLockConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RbinRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ddd08350d2cf21fd7202ff8fe2a0751aeb367ba66c168d5990106b9ba6391d(
    *,
    resource_tag_key: builtins.str,
    resource_tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058a3a383b5e6545db494e2e343e4395f1888f708a6c4bcf06bdd11d044def68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758f5cc71e8d6b841b19a91bee6088449d38d901efa7962dc59e12e016d5e9af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53a1e369ab462a81492a262a5f38d8f4cf9fbd19a624d5e9e1fe04025e1d28b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d461e8500e57d319c865ab3bf986d7e336bb602838e5e8a07074705e4084efd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99801b840aafe76cdd37ace1f9be958d6cf56ccd80a9a4157189cbbf6e5bfe2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fe3efac7b38f88894fa7facdbbbbb70b383089a0b0219b7e84468b8b5e445a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleExcludeResourceTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a380f09a34db6053becf06c5c4c28ff91a8a97e97d4247e98862b6ea4f032911(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aada8ddbcf80b3cac7ecd53095c1a2fd71466f840d3ba56d21388bfb1dfb747e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ea0c79f08b1ab90e4becb169b6eb26273e99ef095c5ec436094be5eaa8894d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128f482be8d7bf0b5c38f6b149a970c3c8c64be9c8b8a5997fdbb376da445755(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleExcludeResourceTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f4dbde718adc81a5b542a4c1c6cb1f105d82ca8014d89d7d52282d1e2fc089(
    *,
    unlock_delay: typing.Union[RbinRuleLockConfigurationUnlockDelay, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32566986f37e86c67581d234e4696abd88d1471d88ed143f3ef36d553b3bfa66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cbdafc02679e58f90874a2e3f6ff8596dae241e5a604c3e4d59dfbfcc38fef(
    value: typing.Optional[RbinRuleLockConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bef0ea2670db79bf0822fcfcd5719ed3be54bef7124292f9228413df75380cc(
    *,
    unlock_delay_unit: builtins.str,
    unlock_delay_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc23a49515d9fcc48fc8bdb056302f91a0373c9cbd3571b604a0cbc973fa828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527e6759291df44f05fcecfb4d04de500ad2ff963306ba39e87ee6f495f8a6ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909708a266231c7c760eef6fe933452946e4fce06847bbb7cdf9efc8a2c0e431(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e3c3849d887207be539b2505242d0e584b527729bb00fef3fded496deec069(
    value: typing.Optional[RbinRuleLockConfigurationUnlockDelay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c853e21cff1fdf9c1c8fc2f3880a34c1d3436aa82344e730eaf821a80b2484(
    *,
    resource_tag_key: builtins.str,
    resource_tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69723c043c17ce9daf3b57628ce39cf074b7783c92d7d778ab3e4a695e3473e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe87f9d8309194dd7d56d240c7a993906bdf15304d665750489b27389f7851d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12956d601b8e5f8fa4892228841c2d0b95446fa531530c5134740cd2c4383065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0738cd35c28cf43b79f27482db85fc3d5304d5afd852504761057ca648fbb33a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0226aaef0d14d94bf21c4e692936b6eb77b687c6c8a8f925e633591520bc99c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f172ac26b1aacab749ed4590bab2e882603f36aba5215f1f1733ffc2600e82a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32078251ae3629bedc223117883daf8b1471b4c7a042d07d3a40ce1a5e747ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4507e7eb83e18bbdbcfb84bb10c10cc9285e55032074eb0c5711e6fd6dc3b48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a4793b6d8bd9fe8c0aa323918ca7b80b4b06b695d5855760ad4291476d1326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9093e07b897f3e0407da3b2f0b2b9fc163954758cdb34bebba667c38e6e91891(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d9985e3ecccc7730b64b027535ef52c181cdadc3a41ccc7131bd2d997df233(
    *,
    retention_period_unit: builtins.str,
    retention_period_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814cca9a25b0505d86cece474af124223aff0f65a3201c15be87c3964fcce29e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed4955583dacffafb82aa15e2451a08043f3ac9b2601d0d844352e47a8d2d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4511350459f7376bbdee416af306cc6fdd797b1d65f1a0415650878039705d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a7bdbe2d64cd602560d1d672ee4b99ccf18407d4dc23b465a240dda713bf70(
    value: typing.Optional[RbinRuleRetentionPeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5ebbe455f7c2cb579dddbc7e4e13279273bd062b823ea4f46df7656822afd8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56db63f0a4440ea9deff461e1e97e9409dcb10a34111a0dea6ceacfe768a66b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91c7f989bd307c30f5c16c948b923787b2d2bb4998cbd4c4e0ddaeff8f26954(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55035739de93167d9b9968b64b76759db05524fc56e881eeb65f680ded015c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3cd2389365e7dd881f75ed9a50a3ee480cb62efb4d467a6e94a6d393b1b89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f617fb819a82d59c6a74df923889ffd5cbcf63bafcf0892b56e09a907fcb7d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
