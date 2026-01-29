r'''
# `aws_backup_plan`

Refer to the Terraform Registry for docs: [`aws_backup_plan`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan).
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


class BackupPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan aws_backup_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRule", typing.Dict[builtins.str, typing.Any]]]],
        advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanAdvancedBackupSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanScanSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan aws_backup_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#name BackupPlan#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#rule BackupPlan#rule}
        :param advanced_backup_setting: advanced_backup_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#advanced_backup_setting BackupPlan#advanced_backup_setting}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#id BackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#region BackupPlan#region}
        :param scan_setting: scan_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_setting BackupPlan#scan_setting}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#tags BackupPlan#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#tags_all BackupPlan#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73dca6f628a70035165e095b6d0b3f0ef4cf4e3ad65b494fc109ee061143ee3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BackupPlanConfig(
            name=name,
            rule=rule,
            advanced_backup_setting=advanced_backup_setting,
            id=id,
            region=region,
            scan_setting=scan_setting,
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
        '''Generates CDKTF code for importing a BackupPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BackupPlan to import.
        :param import_from_id: The id of the existing BackupPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BackupPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917842bde8c2d859deb2ee2d5cd3eaab290356fbecaefb28ab89b744a8430626)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedBackupSetting")
    def put_advanced_backup_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanAdvancedBackupSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5189a5e6ff17a1a4f95bb190f20645ff2c9d7c214e3e1e3f4bd7ee9dca4e94f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdvancedBackupSetting", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b8c26214071d471938c353e1dbe7be2af95dcb28d3d108e74a40c1858b0199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="putScanSetting")
    def put_scan_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanScanSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e5be7e3290ec194b9b045f7d30665905eb8e337d27e3ca8b5b8d278b586ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScanSetting", [value]))

    @jsii.member(jsii_name="resetAdvancedBackupSetting")
    def reset_advanced_backup_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedBackupSetting", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScanSetting")
    def reset_scan_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanSetting", []))

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
    @jsii.member(jsii_name="advancedBackupSetting")
    def advanced_backup_setting(self) -> "BackupPlanAdvancedBackupSettingList":
        return typing.cast("BackupPlanAdvancedBackupSettingList", jsii.get(self, "advancedBackupSetting"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "BackupPlanRuleList":
        return typing.cast("BackupPlanRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="scanSetting")
    def scan_setting(self) -> "BackupPlanScanSettingList":
        return typing.cast("BackupPlanScanSettingList", jsii.get(self, "scanSetting"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="advancedBackupSettingInput")
    def advanced_backup_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanAdvancedBackupSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanAdvancedBackupSetting"]]], jsii.get(self, "advancedBackupSettingInput"))

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
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="scanSettingInput")
    def scan_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]], jsii.get(self, "scanSettingInput"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea42a86c875d985ff775721e21c647c5f477a7cbb34af439eed88c461dafadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591c1aeafaab409d0b39c82c6d7de6f7bfb4844ae774640007077e7acecbd329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ce541c280efab51d0cced5888513e07848fe2d8e19b7e1fc36018a683f573a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9fd2a1e4a7c1d44f508fad535db95f50b51ca338abe7932c46077ba4a740a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2105404110ea8543bd6f1bd61dc240d70cb72915936a082fd8efecab2476f268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanAdvancedBackupSetting",
    jsii_struct_bases=[],
    name_mapping={"backup_options": "backupOptions", "resource_type": "resourceType"},
)
class BackupPlanAdvancedBackupSetting:
    def __init__(
        self,
        *,
        backup_options: typing.Mapping[builtins.str, builtins.str],
        resource_type: builtins.str,
    ) -> None:
        '''
        :param backup_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#backup_options BackupPlan#backup_options}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#resource_type BackupPlan#resource_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f4f287bfa63ae2e91b95d64825b541ab5f68f01969b2b688e69c4cecad9078)
            check_type(argname="argument backup_options", value=backup_options, expected_type=type_hints["backup_options"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_options": backup_options,
            "resource_type": resource_type,
        }

    @builtins.property
    def backup_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#backup_options BackupPlan#backup_options}.'''
        result = self._values.get("backup_options")
        assert result is not None, "Required property 'backup_options' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#resource_type BackupPlan#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanAdvancedBackupSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanAdvancedBackupSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanAdvancedBackupSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae73d01e7a7fe18c40d7aa0ad6a330e046cd841929840a438a4adb9fb0fd2177)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BackupPlanAdvancedBackupSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c128501013d93b30166220b5131e1f5949042cb8285aa92aa6ebf9a87a9869f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanAdvancedBackupSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c3116117d53b85d11eca2f62a592a2925b4e8d1914861f7422864d6b855db3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b7f054af2d8e507932cf5701e3c4907ef50110ec24177a5fc84eb2f2940b374)
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
            type_hints = typing.get_type_hints(_typecheckingstub__082d07440216c320f1505f044aa62cac3c67cf620084bde6ebd0af10de48fa64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc14001c2cf0dcdd244f743a6c4ca328f83ea34a2b96ee04b5b481af2a27565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanAdvancedBackupSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanAdvancedBackupSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7abdaf4c6c4160dd31271e86f93c53875cf5eb34dd85c0c4eb1b1f68869bf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="backupOptionsInput")
    def backup_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "backupOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupOptions")
    def backup_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "backupOptions"))

    @backup_options.setter
    def backup_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdbc63a3f85196a48f6fc552b467da4bb852020462fc0befd62ae8c3a239345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57269a4302bc21a69e6f06e840db70e04759485428161acd8f855753dbc25411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a1fc8332ec28eae5e8e9c3815c248e96aad23ff58e1fa9e0437b61ac495366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanConfig",
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
        "rule": "rule",
        "advanced_backup_setting": "advancedBackupSetting",
        "id": "id",
        "region": "region",
        "scan_setting": "scanSetting",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class BackupPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRule", typing.Dict[builtins.str, typing.Any]]]],
        advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanScanSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#name BackupPlan#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#rule BackupPlan#rule}
        :param advanced_backup_setting: advanced_backup_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#advanced_backup_setting BackupPlan#advanced_backup_setting}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#id BackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#region BackupPlan#region}
        :param scan_setting: scan_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_setting BackupPlan#scan_setting}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#tags BackupPlan#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#tags_all BackupPlan#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ec46b6f354dc8bd252f5c365d74318e9639a70b9ab6eb7bfa504687620774b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument advanced_backup_setting", value=advanced_backup_setting, expected_type=type_hints["advanced_backup_setting"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scan_setting", value=scan_setting, expected_type=type_hints["scan_setting"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rule": rule,
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
        if advanced_backup_setting is not None:
            self._values["advanced_backup_setting"] = advanced_backup_setting
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if scan_setting is not None:
            self._values["scan_setting"] = scan_setting
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#name BackupPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#rule BackupPlan#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]], result)

    @builtins.property
    def advanced_backup_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]]:
        '''advanced_backup_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#advanced_backup_setting BackupPlan#advanced_backup_setting}
        '''
        result = self._values.get("advanced_backup_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#id BackupPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#region BackupPlan#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]]:
        '''scan_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_setting BackupPlan#scan_setting}
        '''
        result = self._values.get("scan_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#tags BackupPlan#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#tags_all BackupPlan#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRule",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "target_vault_name": "targetVaultName",
        "completion_window": "completionWindow",
        "copy_action": "copyAction",
        "enable_continuous_backup": "enableContinuousBackup",
        "lifecycle": "lifecycle",
        "recovery_point_tags": "recoveryPointTags",
        "scan_action": "scanAction",
        "schedule": "schedule",
        "schedule_expression_timezone": "scheduleExpressionTimezone",
        "start_window": "startWindow",
        "target_logically_air_gapped_backup_vault_arn": "targetLogicallyAirGappedBackupVaultArn",
    },
)
class BackupPlanRule:
    def __init__(
        self,
        *,
        rule_name: builtins.str,
        target_vault_name: builtins.str,
        completion_window: typing.Optional[jsii.Number] = None,
        copy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRuleCopyAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_continuous_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lifecycle: typing.Optional[typing.Union["BackupPlanRuleLifecycle", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_point_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        scan_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRuleScanAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_expression_timezone: typing.Optional[builtins.str] = None,
        start_window: typing.Optional[jsii.Number] = None,
        target_logically_air_gapped_backup_vault_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#rule_name BackupPlan#rule_name}.
        :param target_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#target_vault_name BackupPlan#target_vault_name}.
        :param completion_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#completion_window BackupPlan#completion_window}.
        :param copy_action: copy_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#copy_action BackupPlan#copy_action}
        :param enable_continuous_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#enable_continuous_backup BackupPlan#enable_continuous_backup}.
        :param lifecycle: lifecycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        :param recovery_point_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#recovery_point_tags BackupPlan#recovery_point_tags}.
        :param scan_action: scan_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_action BackupPlan#scan_action}
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#schedule BackupPlan#schedule}.
        :param schedule_expression_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#schedule_expression_timezone BackupPlan#schedule_expression_timezone}.
        :param start_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#start_window BackupPlan#start_window}.
        :param target_logically_air_gapped_backup_vault_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#target_logically_air_gapped_backup_vault_arn BackupPlan#target_logically_air_gapped_backup_vault_arn}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = BackupPlanRuleLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0198e61956c2222b41d7b95890c300d360d0303d4c6eb11b1293cf266cdef8aa)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument target_vault_name", value=target_vault_name, expected_type=type_hints["target_vault_name"])
            check_type(argname="argument completion_window", value=completion_window, expected_type=type_hints["completion_window"])
            check_type(argname="argument copy_action", value=copy_action, expected_type=type_hints["copy_action"])
            check_type(argname="argument enable_continuous_backup", value=enable_continuous_backup, expected_type=type_hints["enable_continuous_backup"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument recovery_point_tags", value=recovery_point_tags, expected_type=type_hints["recovery_point_tags"])
            check_type(argname="argument scan_action", value=scan_action, expected_type=type_hints["scan_action"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schedule_expression_timezone", value=schedule_expression_timezone, expected_type=type_hints["schedule_expression_timezone"])
            check_type(argname="argument start_window", value=start_window, expected_type=type_hints["start_window"])
            check_type(argname="argument target_logically_air_gapped_backup_vault_arn", value=target_logically_air_gapped_backup_vault_arn, expected_type=type_hints["target_logically_air_gapped_backup_vault_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
            "target_vault_name": target_vault_name,
        }
        if completion_window is not None:
            self._values["completion_window"] = completion_window
        if copy_action is not None:
            self._values["copy_action"] = copy_action
        if enable_continuous_backup is not None:
            self._values["enable_continuous_backup"] = enable_continuous_backup
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if recovery_point_tags is not None:
            self._values["recovery_point_tags"] = recovery_point_tags
        if scan_action is not None:
            self._values["scan_action"] = scan_action
        if schedule is not None:
            self._values["schedule"] = schedule
        if schedule_expression_timezone is not None:
            self._values["schedule_expression_timezone"] = schedule_expression_timezone
        if start_window is not None:
            self._values["start_window"] = start_window
        if target_logically_air_gapped_backup_vault_arn is not None:
            self._values["target_logically_air_gapped_backup_vault_arn"] = target_logically_air_gapped_backup_vault_arn

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#rule_name BackupPlan#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#target_vault_name BackupPlan#target_vault_name}.'''
        result = self._values.get("target_vault_name")
        assert result is not None, "Required property 'target_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def completion_window(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#completion_window BackupPlan#completion_window}.'''
        result = self._values.get("completion_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def copy_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleCopyAction"]]]:
        '''copy_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#copy_action BackupPlan#copy_action}
        '''
        result = self._values.get("copy_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleCopyAction"]]], result)

    @builtins.property
    def enable_continuous_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#enable_continuous_backup BackupPlan#enable_continuous_backup}.'''
        result = self._values.get("enable_continuous_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional["BackupPlanRuleLifecycle"]:
        '''lifecycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional["BackupPlanRuleLifecycle"], result)

    @builtins.property
    def recovery_point_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#recovery_point_tags BackupPlan#recovery_point_tags}.'''
        result = self._values.get("recovery_point_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def scan_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]]:
        '''scan_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_action BackupPlan#scan_action}
        '''
        result = self._values.get("scan_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#schedule BackupPlan#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#schedule_expression_timezone BackupPlan#schedule_expression_timezone}.'''
        result = self._values.get("schedule_expression_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_window(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#start_window BackupPlan#start_window}.'''
        result = self._values.get("start_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_logically_air_gapped_backup_vault_arn(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#target_logically_air_gapped_backup_vault_arn BackupPlan#target_logically_air_gapped_backup_vault_arn}.'''
        result = self._values.get("target_logically_air_gapped_backup_vault_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleCopyAction",
    jsii_struct_bases=[],
    name_mapping={
        "destination_vault_arn": "destinationVaultArn",
        "lifecycle": "lifecycle",
    },
)
class BackupPlanRuleCopyAction:
    def __init__(
        self,
        *,
        destination_vault_arn: builtins.str,
        lifecycle: typing.Optional[typing.Union["BackupPlanRuleCopyActionLifecycle", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination_vault_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#destination_vault_arn BackupPlan#destination_vault_arn}.
        :param lifecycle: lifecycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = BackupPlanRuleCopyActionLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2f594f418c1bda0a47a51f85c772b71be4c9ac5a5ca3f659e6f800d6123d2c)
            check_type(argname="argument destination_vault_arn", value=destination_vault_arn, expected_type=type_hints["destination_vault_arn"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_vault_arn": destination_vault_arn,
        }
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle

    @builtins.property
    def destination_vault_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#destination_vault_arn BackupPlan#destination_vault_arn}.'''
        result = self._values.get("destination_vault_arn")
        assert result is not None, "Required property 'destination_vault_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lifecycle(self) -> typing.Optional["BackupPlanRuleCopyActionLifecycle"]:
        '''lifecycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional["BackupPlanRuleCopyActionLifecycle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleCopyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleCopyActionLifecycle",
    jsii_struct_bases=[],
    name_mapping={
        "cold_storage_after": "coldStorageAfter",
        "delete_after": "deleteAfter",
        "opt_in_to_archive_for_supported_resources": "optInToArchiveForSupportedResources",
    },
)
class BackupPlanRuleCopyActionLifecycle:
    def __init__(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b440daaf625345bac587e0ee3766789f657feb2b9b10c7b1ddb81ad738980d)
            check_type(argname="argument cold_storage_after", value=cold_storage_after, expected_type=type_hints["cold_storage_after"])
            check_type(argname="argument delete_after", value=delete_after, expected_type=type_hints["delete_after"])
            check_type(argname="argument opt_in_to_archive_for_supported_resources", value=opt_in_to_archive_for_supported_resources, expected_type=type_hints["opt_in_to_archive_for_supported_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cold_storage_after is not None:
            self._values["cold_storage_after"] = cold_storage_after
        if delete_after is not None:
            self._values["delete_after"] = delete_after
        if opt_in_to_archive_for_supported_resources is not None:
            self._values["opt_in_to_archive_for_supported_resources"] = opt_in_to_archive_for_supported_resources

    @builtins.property
    def cold_storage_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.'''
        result = self._values.get("cold_storage_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.'''
        result = self._values.get("delete_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.'''
        result = self._values.get("opt_in_to_archive_for_supported_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleCopyActionLifecycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRuleCopyActionLifecycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleCopyActionLifecycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__328c6891131453d1b8b81b2d1d6e270cc781428de10f181b5d8d4f5e729c5153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetColdStorageAfter")
    def reset_cold_storage_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColdStorageAfter", []))

    @jsii.member(jsii_name="resetDeleteAfter")
    def reset_delete_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfter", []))

    @jsii.member(jsii_name="resetOptInToArchiveForSupportedResources")
    def reset_opt_in_to_archive_for_supported_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptInToArchiveForSupportedResources", []))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfterInput")
    def cold_storage_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coldStorageAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterInput")
    def delete_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResourcesInput")
    def opt_in_to_archive_for_supported_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optInToArchiveForSupportedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfter")
    def cold_storage_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coldStorageAfter"))

    @cold_storage_after.setter
    def cold_storage_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65dbd9eb41eea41785803af040a852e8d1953905d5db8e8b788229bd43cfa22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coldStorageAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfter")
    def delete_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfter"))

    @delete_after.setter
    def delete_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03135762ea8272c8461757fbec2929d8654df46260856fbba951a3dc2b480da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResources")
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optInToArchiveForSupportedResources"))

    @opt_in_to_archive_for_supported_resources.setter
    def opt_in_to_archive_for_supported_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29874292d59cf2985acee732604720269a0cbe61b03b40861d292ebb50f35bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optInToArchiveForSupportedResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPlanRuleCopyActionLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleCopyActionLifecycle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPlanRuleCopyActionLifecycle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e5fe201c8541df8637c9fd7eaffaffcb5a5640852044e9dde611edc586ede0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleCopyActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleCopyActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90135da68905eb7fb36a7d2626fa911ff7fe73c9df331fe25140ac30890f36ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanRuleCopyActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e236bcfd28c8f1bd32fa4b0e233626bb48b7c9379147db78e6579d55a92f19ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanRuleCopyActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc52943c0ae625d59858a7353cca9f928e71a0819892b7725b8d1e8224bafea5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eaaed3330c4af06aa0851825475eb52e26dd2e2b248fc0aa28ca6f8f1999e0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5674162dc01b5618901021543e343d4bdada96395f92a692a8ca454967a09da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1385eedaacafac2a7bf1c4401536578283da8a14e733ca8c0acc67729336b514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleCopyActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleCopyActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02db24e102f6b6e89d5d5094afe51f33619d580d63ed7e5c25bb907fa05c2aa9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLifecycle")
    def put_lifecycle(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        value = BackupPlanRuleCopyActionLifecycle(
            cold_storage_after=cold_storage_after,
            delete_after=delete_after,
            opt_in_to_archive_for_supported_resources=opt_in_to_archive_for_supported_resources,
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycle", [value]))

    @jsii.member(jsii_name="resetLifecycle")
    def reset_lifecycle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycle", []))

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> BackupPlanRuleCopyActionLifecycleOutputReference:
        return typing.cast(BackupPlanRuleCopyActionLifecycleOutputReference, jsii.get(self, "lifecycle"))

    @builtins.property
    @jsii.member(jsii_name="destinationVaultArnInput")
    def destination_vault_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationVaultArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleInput")
    def lifecycle_input(self) -> typing.Optional[BackupPlanRuleCopyActionLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleCopyActionLifecycle], jsii.get(self, "lifecycleInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationVaultArn")
    def destination_vault_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationVaultArn"))

    @destination_vault_arn.setter
    def destination_vault_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6794abf4df07f61e5c67ec8bffb27d4ddef0b4a38e156b60c21e947e860977c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationVaultArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f251f0413f6ec1635a6aa9d999260b7bf1f1e92abf74a2ecb1903cddc17e40fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleLifecycle",
    jsii_struct_bases=[],
    name_mapping={
        "cold_storage_after": "coldStorageAfter",
        "delete_after": "deleteAfter",
        "opt_in_to_archive_for_supported_resources": "optInToArchiveForSupportedResources",
    },
)
class BackupPlanRuleLifecycle:
    def __init__(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ec685e572d74a7f467bd55ae4aac7a871d26d43474da45357dcdbcab8c571d)
            check_type(argname="argument cold_storage_after", value=cold_storage_after, expected_type=type_hints["cold_storage_after"])
            check_type(argname="argument delete_after", value=delete_after, expected_type=type_hints["delete_after"])
            check_type(argname="argument opt_in_to_archive_for_supported_resources", value=opt_in_to_archive_for_supported_resources, expected_type=type_hints["opt_in_to_archive_for_supported_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cold_storage_after is not None:
            self._values["cold_storage_after"] = cold_storage_after
        if delete_after is not None:
            self._values["delete_after"] = delete_after
        if opt_in_to_archive_for_supported_resources is not None:
            self._values["opt_in_to_archive_for_supported_resources"] = opt_in_to_archive_for_supported_resources

    @builtins.property
    def cold_storage_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.'''
        result = self._values.get("cold_storage_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.'''
        result = self._values.get("delete_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.'''
        result = self._values.get("opt_in_to_archive_for_supported_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleLifecycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRuleLifecycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleLifecycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e2ea3d2f5b4771829bcb2ba78a9687a639c0e60c0855e9f7d53ebe19aa9b47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetColdStorageAfter")
    def reset_cold_storage_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColdStorageAfter", []))

    @jsii.member(jsii_name="resetDeleteAfter")
    def reset_delete_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfter", []))

    @jsii.member(jsii_name="resetOptInToArchiveForSupportedResources")
    def reset_opt_in_to_archive_for_supported_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptInToArchiveForSupportedResources", []))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfterInput")
    def cold_storage_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coldStorageAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterInput")
    def delete_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResourcesInput")
    def opt_in_to_archive_for_supported_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optInToArchiveForSupportedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfter")
    def cold_storage_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coldStorageAfter"))

    @cold_storage_after.setter
    def cold_storage_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a54dfc6140e393b466464b2584480a27b18c1248d72681e0dd4aae5f9cd4277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coldStorageAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfter")
    def delete_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfter"))

    @delete_after.setter
    def delete_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289d748ea29d081476de7a28fbbceea00d77b0837fcfb9e32fd4efbcdd3b3b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResources")
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optInToArchiveForSupportedResources"))

    @opt_in_to_archive_for_supported_resources.setter
    def opt_in_to_archive_for_supported_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4c36bc937f212dbb9c62316d7ee7b9c52587664689da1186e918fc31ee71c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optInToArchiveForSupportedResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPlanRuleLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleLifecycle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BackupPlanRuleLifecycle]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37c8c488fa101ba68cca49302164930cacf7bc210cca30469fe4802107fd111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d81866f80b232a9cf0e5a7f0ffebaaf8b3637ce9fa8fac2606137ef7df7f77d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426308a2b0e318e6647626c335bf2d7db0e6fd6eaa9ee2541a10a9173b20e751)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1442b221d14805e13734bf03c9fbab1e29e51a2cf8d2affed4b045330a1c2fd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fe13527e6563b056b3230d46a32ffcf5c897c4d027f63056175059cb304f261)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c5e2a4afcc94026eab9b1962b472a2a3eaa4390e3e1243e2ea5b9a09f5cadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c504311af9ab3ffe25b120f7e24ac33e1a8cd1c5364c764dcd7b251f17a8dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1df079e99af67c3056a0751d96376a06013e7ab08f90b0b62fced4ab4fb3bf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCopyAction")
    def put_copy_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleCopyAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470b85b8e985196e685599f0e9d8ab44b80baf3b7305950b4856b28f7b79ee4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCopyAction", [value]))

    @jsii.member(jsii_name="putLifecycle")
    def put_lifecycle(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        value = BackupPlanRuleLifecycle(
            cold_storage_after=cold_storage_after,
            delete_after=delete_after,
            opt_in_to_archive_for_supported_resources=opt_in_to_archive_for_supported_resources,
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycle", [value]))

    @jsii.member(jsii_name="putScanAction")
    def put_scan_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRuleScanAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48d657591f658f4827ff6e0ac6277138c5c2b76c28f7d2d4b96bf878a476997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScanAction", [value]))

    @jsii.member(jsii_name="resetCompletionWindow")
    def reset_completion_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompletionWindow", []))

    @jsii.member(jsii_name="resetCopyAction")
    def reset_copy_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyAction", []))

    @jsii.member(jsii_name="resetEnableContinuousBackup")
    def reset_enable_continuous_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableContinuousBackup", []))

    @jsii.member(jsii_name="resetLifecycle")
    def reset_lifecycle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycle", []))

    @jsii.member(jsii_name="resetRecoveryPointTags")
    def reset_recovery_point_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryPointTags", []))

    @jsii.member(jsii_name="resetScanAction")
    def reset_scan_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanAction", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetScheduleExpressionTimezone")
    def reset_schedule_expression_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleExpressionTimezone", []))

    @jsii.member(jsii_name="resetStartWindow")
    def reset_start_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartWindow", []))

    @jsii.member(jsii_name="resetTargetLogicallyAirGappedBackupVaultArn")
    def reset_target_logically_air_gapped_backup_vault_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetLogicallyAirGappedBackupVaultArn", []))

    @builtins.property
    @jsii.member(jsii_name="copyAction")
    def copy_action(self) -> BackupPlanRuleCopyActionList:
        return typing.cast(BackupPlanRuleCopyActionList, jsii.get(self, "copyAction"))

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> BackupPlanRuleLifecycleOutputReference:
        return typing.cast(BackupPlanRuleLifecycleOutputReference, jsii.get(self, "lifecycle"))

    @builtins.property
    @jsii.member(jsii_name="scanAction")
    def scan_action(self) -> "BackupPlanRuleScanActionList":
        return typing.cast("BackupPlanRuleScanActionList", jsii.get(self, "scanAction"))

    @builtins.property
    @jsii.member(jsii_name="completionWindowInput")
    def completion_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "completionWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="copyActionInput")
    def copy_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]], jsii.get(self, "copyActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableContinuousBackupInput")
    def enable_continuous_backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableContinuousBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleInput")
    def lifecycle_input(self) -> typing.Optional[BackupPlanRuleLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleLifecycle], jsii.get(self, "lifecycleInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryPointTagsInput")
    def recovery_point_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "recoveryPointTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scanActionInput")
    def scan_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]], jsii.get(self, "scanActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionTimezoneInput")
    def schedule_expression_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleExpressionTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="startWindowInput")
    def start_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="targetLogicallyAirGappedBackupVaultArnInput")
    def target_logically_air_gapped_backup_vault_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetLogicallyAirGappedBackupVaultArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVaultNameInput")
    def target_vault_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVaultNameInput"))

    @builtins.property
    @jsii.member(jsii_name="completionWindow")
    def completion_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "completionWindow"))

    @completion_window.setter
    def completion_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebedcf267e088abc1e7a30b6929657e3f8cdc0c404271b88deac2e1a0f8cf123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "completionWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableContinuousBackup")
    def enable_continuous_backup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableContinuousBackup"))

    @enable_continuous_backup.setter
    def enable_continuous_backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c998a1a6bc786b50bff30d56bb0ba62d44bebe86b098829dea7049621669bb66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableContinuousBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryPointTags")
    def recovery_point_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "recoveryPointTags"))

    @recovery_point_tags.setter
    def recovery_point_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355770a57ccad9f662e2ed47b872040e02fd468d0834845c3bd661a010e2164d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryPointTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63571ea53366fbe6011c6952e8374c4ea80dc405d776140ce8959b7bcc2d565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d612d806d2e615ca7b3e7dfb4154bc9cd8bca95a0dd0bb6d11b116c7b4ef05ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionTimezone")
    def schedule_expression_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleExpressionTimezone"))

    @schedule_expression_timezone.setter
    def schedule_expression_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1acecac55288af21b075077e06c3b6ca3ade39d2bd31b888bed10f71b22421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpressionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startWindow")
    def start_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startWindow"))

    @start_window.setter
    def start_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5510aac4b3e221500eefd0f8a856880ae17a0749b232dccad0b1cd66e2792975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetLogicallyAirGappedBackupVaultArn")
    def target_logically_air_gapped_backup_vault_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetLogicallyAirGappedBackupVaultArn"))

    @target_logically_air_gapped_backup_vault_arn.setter
    def target_logically_air_gapped_backup_vault_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2197af245fe60d9a697eded0ea887d00964e2cd607806159fdae8f1b2f60701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetLogicallyAirGappedBackupVaultArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVaultName")
    def target_vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVaultName"))

    @target_vault_name.setter
    def target_vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3789a6a4bca9da130888315f43a4226d3bdb630109212e4046d98a710a0977e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVaultName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99a31d14e28c5807f4c91dcbb0ecef288f55caae2a7ea2c8ec935a857baadc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleScanAction",
    jsii_struct_bases=[],
    name_mapping={"malware_scanner": "malwareScanner", "scan_mode": "scanMode"},
)
class BackupPlanRuleScanAction:
    def __init__(
        self,
        *,
        malware_scanner: builtins.str,
        scan_mode: builtins.str,
    ) -> None:
        '''
        :param malware_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.
        :param scan_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_mode BackupPlan#scan_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6aefd871478a99b6c7830d990eb69210966034d9f2a7781d21f9572de450819)
            check_type(argname="argument malware_scanner", value=malware_scanner, expected_type=type_hints["malware_scanner"])
            check_type(argname="argument scan_mode", value=scan_mode, expected_type=type_hints["scan_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "malware_scanner": malware_scanner,
            "scan_mode": scan_mode,
        }

    @builtins.property
    def malware_scanner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.'''
        result = self._values.get("malware_scanner")
        assert result is not None, "Required property 'malware_scanner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scan_mode BackupPlan#scan_mode}.'''
        result = self._values.get("scan_mode")
        assert result is not None, "Required property 'scan_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleScanAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRuleScanActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleScanActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b09fad9df3262904882a88311a96c991e4d383e49e71429e66fe847781d9f2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanRuleScanActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26813f16ddac72021602d1c995c19aa8257a8f98896c73e553010989ac8a9fe4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanRuleScanActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae2ee06519f62f3cdc6cc41b27f8a96c612de2fb96aa0ab941aef1775985852)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f9e56296dfd384351f63b48fb3463a953abb682016bd037d85b32d0dfb0290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5f931d0c0778c10e40916040e6f32f2d0b25c8c34cd34b74778e4e0b6e49aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f333a58ccd817761d5f18644e7afeb4147718e2360ad389bd1326c4abf712d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleScanActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanRuleScanActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3584675bdde8360032c2b7e944eba38d312ac092e45f1e35f8ae938409ed8bac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="malwareScannerInput")
    def malware_scanner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "malwareScannerInput"))

    @builtins.property
    @jsii.member(jsii_name="scanModeInput")
    def scan_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scanModeInput"))

    @builtins.property
    @jsii.member(jsii_name="malwareScanner")
    def malware_scanner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "malwareScanner"))

    @malware_scanner.setter
    def malware_scanner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5dc6d634e4be62e41ca099c94a9a6c40014961d8e67b14484545973cadfdfef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "malwareScanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanMode")
    def scan_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanMode"))

    @scan_mode.setter
    def scan_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c81fbc278359a307839ea9215efeafbbde660ada7120c36eea0490e4abb948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e98fd37105ead5ec86ffdcf9ac584a77d9d8451f5651f8c84ea59f22b75ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanScanSetting",
    jsii_struct_bases=[],
    name_mapping={
        "malware_scanner": "malwareScanner",
        "resource_types": "resourceTypes",
        "scanner_role_arn": "scannerRoleArn",
    },
)
class BackupPlanScanSetting:
    def __init__(
        self,
        *,
        malware_scanner: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        scanner_role_arn: builtins.str,
    ) -> None:
        '''
        :param malware_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#resource_types BackupPlan#resource_types}.
        :param scanner_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scanner_role_arn BackupPlan#scanner_role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2701bd2c7043f68a8f40f916d9164584b7c21363ee8a5e1819ef56a0fed85a)
            check_type(argname="argument malware_scanner", value=malware_scanner, expected_type=type_hints["malware_scanner"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument scanner_role_arn", value=scanner_role_arn, expected_type=type_hints["scanner_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "malware_scanner": malware_scanner,
            "resource_types": resource_types,
            "scanner_role_arn": scanner_role_arn,
        }

    @builtins.property
    def malware_scanner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.'''
        result = self._values.get("malware_scanner")
        assert result is not None, "Required property 'malware_scanner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#resource_types BackupPlan#resource_types}.'''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scanner_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/backup_plan#scanner_role_arn BackupPlan#scanner_role_arn}.'''
        result = self._values.get("scanner_role_arn")
        assert result is not None, "Required property 'scanner_role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanScanSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanScanSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanScanSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__467657443fbd5da267597d7875c7dab95796594dc8925ea6168a898365b79302)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanScanSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697fada9b2648415e9bf205cb67f0e1839f27b7c4d107e04939ee00cce154681)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanScanSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d230a871087b894847993c331f7601d7d4b430e1004d9885214b1d9a5800d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9132ede90f0174bd8c5645084690d5c33d7071de2b22f094a2595a5c11bd851b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6f7b0fb095d66d7df1ef06bd59acba5e88463ee6888952afb0080f3fd11ebf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968b10ba4860127ad7622a9e58e99e521cdcce89db3079a66a71097543eaea9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanScanSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.backupPlan.BackupPlanScanSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00f60c3f279ff7754e734ec8ffc35efd28da4724aba19e70602c9ada752db00e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="malwareScannerInput")
    def malware_scanner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "malwareScannerInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="scannerRoleArnInput")
    def scanner_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scannerRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="malwareScanner")
    def malware_scanner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "malwareScanner"))

    @malware_scanner.setter
    def malware_scanner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81696a1f360f23d869ba1531e0f53cea11a301e1d2ec7aee1498ed35613a1317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "malwareScanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38ab178e036d8b2a4f87a2071842905157f693d6ecbbce268486d375611aa95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scannerRoleArn")
    def scanner_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scannerRoleArn"))

    @scanner_role_arn.setter
    def scanner_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ca7db83b3ab4c6b681f071d8795d1a87887f9cb8d0a2980c9216f00fe451a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scannerRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeecd8f0af2961f56ed5bad22b321f296725a53c2f5673931fde9fcf40657d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BackupPlan",
    "BackupPlanAdvancedBackupSetting",
    "BackupPlanAdvancedBackupSettingList",
    "BackupPlanAdvancedBackupSettingOutputReference",
    "BackupPlanConfig",
    "BackupPlanRule",
    "BackupPlanRuleCopyAction",
    "BackupPlanRuleCopyActionLifecycle",
    "BackupPlanRuleCopyActionLifecycleOutputReference",
    "BackupPlanRuleCopyActionList",
    "BackupPlanRuleCopyActionOutputReference",
    "BackupPlanRuleLifecycle",
    "BackupPlanRuleLifecycleOutputReference",
    "BackupPlanRuleList",
    "BackupPlanRuleOutputReference",
    "BackupPlanRuleScanAction",
    "BackupPlanRuleScanActionList",
    "BackupPlanRuleScanActionOutputReference",
    "BackupPlanScanSetting",
    "BackupPlanScanSettingList",
    "BackupPlanScanSettingOutputReference",
]

publication.publish()

def _typecheckingstub__73dca6f628a70035165e095b6d0b3f0ef4cf4e3ad65b494fc109ee061143ee3c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRule, typing.Dict[builtins.str, typing.Any]]]],
    advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanScanSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__917842bde8c2d859deb2ee2d5cd3eaab290356fbecaefb28ab89b744a8430626(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5189a5e6ff17a1a4f95bb190f20645ff2c9d7c214e3e1e3f4bd7ee9dca4e94f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b8c26214071d471938c353e1dbe7be2af95dcb28d3d108e74a40c1858b0199(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e5be7e3290ec194b9b045f7d30665905eb8e337d27e3ca8b5b8d278b586ded(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanScanSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea42a86c875d985ff775721e21c647c5f477a7cbb34af439eed88c461dafadc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591c1aeafaab409d0b39c82c6d7de6f7bfb4844ae774640007077e7acecbd329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ce541c280efab51d0cced5888513e07848fe2d8e19b7e1fc36018a683f573a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9fd2a1e4a7c1d44f508fad535db95f50b51ca338abe7932c46077ba4a740a6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2105404110ea8543bd6f1bd61dc240d70cb72915936a082fd8efecab2476f268(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f4f287bfa63ae2e91b95d64825b541ab5f68f01969b2b688e69c4cecad9078(
    *,
    backup_options: typing.Mapping[builtins.str, builtins.str],
    resource_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae73d01e7a7fe18c40d7aa0ad6a330e046cd841929840a438a4adb9fb0fd2177(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c128501013d93b30166220b5131e1f5949042cb8285aa92aa6ebf9a87a9869f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c3116117d53b85d11eca2f62a592a2925b4e8d1914861f7422864d6b855db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7f054af2d8e507932cf5701e3c4907ef50110ec24177a5fc84eb2f2940b374(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082d07440216c320f1505f044aa62cac3c67cf620084bde6ebd0af10de48fa64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc14001c2cf0dcdd244f743a6c4ca328f83ea34a2b96ee04b5b481af2a27565(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7abdaf4c6c4160dd31271e86f93c53875cf5eb34dd85c0c4eb1b1f68869bf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdbc63a3f85196a48f6fc552b467da4bb852020462fc0befd62ae8c3a239345(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57269a4302bc21a69e6f06e840db70e04759485428161acd8f855753dbc25411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a1fc8332ec28eae5e8e9c3815c248e96aad23ff58e1fa9e0437b61ac495366(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ec46b6f354dc8bd252f5c365d74318e9639a70b9ab6eb7bfa504687620774b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRule, typing.Dict[builtins.str, typing.Any]]]],
    advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanScanSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0198e61956c2222b41d7b95890c300d360d0303d4c6eb11b1293cf266cdef8aa(
    *,
    rule_name: builtins.str,
    target_vault_name: builtins.str,
    completion_window: typing.Optional[jsii.Number] = None,
    copy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleCopyAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_continuous_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lifecycle: typing.Optional[typing.Union[BackupPlanRuleLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_point_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    scan_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleScanAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_window: typing.Optional[jsii.Number] = None,
    target_logically_air_gapped_backup_vault_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2f594f418c1bda0a47a51f85c772b71be4c9ac5a5ca3f659e6f800d6123d2c(
    *,
    destination_vault_arn: builtins.str,
    lifecycle: typing.Optional[typing.Union[BackupPlanRuleCopyActionLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b440daaf625345bac587e0ee3766789f657feb2b9b10c7b1ddb81ad738980d(
    *,
    cold_storage_after: typing.Optional[jsii.Number] = None,
    delete_after: typing.Optional[jsii.Number] = None,
    opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328c6891131453d1b8b81b2d1d6e270cc781428de10f181b5d8d4f5e729c5153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65dbd9eb41eea41785803af040a852e8d1953905d5db8e8b788229bd43cfa22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03135762ea8272c8461757fbec2929d8654df46260856fbba951a3dc2b480da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29874292d59cf2985acee732604720269a0cbe61b03b40861d292ebb50f35bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e5fe201c8541df8637c9fd7eaffaffcb5a5640852044e9dde611edc586ede0(
    value: typing.Optional[BackupPlanRuleCopyActionLifecycle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90135da68905eb7fb36a7d2626fa911ff7fe73c9df331fe25140ac30890f36ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e236bcfd28c8f1bd32fa4b0e233626bb48b7c9379147db78e6579d55a92f19ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc52943c0ae625d59858a7353cca9f928e71a0819892b7725b8d1e8224bafea5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eaaed3330c4af06aa0851825475eb52e26dd2e2b248fc0aa28ca6f8f1999e0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5674162dc01b5618901021543e343d4bdada96395f92a692a8ca454967a09da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1385eedaacafac2a7bf1c4401536578283da8a14e733ca8c0acc67729336b514(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02db24e102f6b6e89d5d5094afe51f33619d580d63ed7e5c25bb907fa05c2aa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6794abf4df07f61e5c67ec8bffb27d4ddef0b4a38e156b60c21e947e860977c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f251f0413f6ec1635a6aa9d999260b7bf1f1e92abf74a2ecb1903cddc17e40fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ec685e572d74a7f467bd55ae4aac7a871d26d43474da45357dcdbcab8c571d(
    *,
    cold_storage_after: typing.Optional[jsii.Number] = None,
    delete_after: typing.Optional[jsii.Number] = None,
    opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e2ea3d2f5b4771829bcb2ba78a9687a639c0e60c0855e9f7d53ebe19aa9b47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a54dfc6140e393b466464b2584480a27b18c1248d72681e0dd4aae5f9cd4277(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289d748ea29d081476de7a28fbbceea00d77b0837fcfb9e32fd4efbcdd3b3b42(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4c36bc937f212dbb9c62316d7ee7b9c52587664689da1186e918fc31ee71c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37c8c488fa101ba68cca49302164930cacf7bc210cca30469fe4802107fd111(
    value: typing.Optional[BackupPlanRuleLifecycle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81866f80b232a9cf0e5a7f0ffebaaf8b3637ce9fa8fac2606137ef7df7f77d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426308a2b0e318e6647626c335bf2d7db0e6fd6eaa9ee2541a10a9173b20e751(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1442b221d14805e13734bf03c9fbab1e29e51a2cf8d2affed4b045330a1c2fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe13527e6563b056b3230d46a32ffcf5c897c4d027f63056175059cb304f261(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c5e2a4afcc94026eab9b1962b472a2a3eaa4390e3e1243e2ea5b9a09f5cadc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c504311af9ab3ffe25b120f7e24ac33e1a8cd1c5364c764dcd7b251f17a8dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1df079e99af67c3056a0751d96376a06013e7ab08f90b0b62fced4ab4fb3bf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470b85b8e985196e685599f0e9d8ab44b80baf3b7305950b4856b28f7b79ee4f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleCopyAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48d657591f658f4827ff6e0ac6277138c5c2b76c28f7d2d4b96bf878a476997(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleScanAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebedcf267e088abc1e7a30b6929657e3f8cdc0c404271b88deac2e1a0f8cf123(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c998a1a6bc786b50bff30d56bb0ba62d44bebe86b098829dea7049621669bb66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355770a57ccad9f662e2ed47b872040e02fd468d0834845c3bd661a010e2164d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63571ea53366fbe6011c6952e8374c4ea80dc405d776140ce8959b7bcc2d565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d612d806d2e615ca7b3e7dfb4154bc9cd8bca95a0dd0bb6d11b116c7b4ef05ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1acecac55288af21b075077e06c3b6ca3ade39d2bd31b888bed10f71b22421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5510aac4b3e221500eefd0f8a856880ae17a0749b232dccad0b1cd66e2792975(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2197af245fe60d9a697eded0ea887d00964e2cd607806159fdae8f1b2f60701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3789a6a4bca9da130888315f43a4226d3bdb630109212e4046d98a710a0977e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99a31d14e28c5807f4c91dcbb0ecef288f55caae2a7ea2c8ec935a857baadc8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6aefd871478a99b6c7830d990eb69210966034d9f2a7781d21f9572de450819(
    *,
    malware_scanner: builtins.str,
    scan_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b09fad9df3262904882a88311a96c991e4d383e49e71429e66fe847781d9f2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26813f16ddac72021602d1c995c19aa8257a8f98896c73e553010989ac8a9fe4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae2ee06519f62f3cdc6cc41b27f8a96c612de2fb96aa0ab941aef1775985852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f9e56296dfd384351f63b48fb3463a953abb682016bd037d85b32d0dfb0290(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f931d0c0778c10e40916040e6f32f2d0b25c8c34cd34b74778e4e0b6e49aea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f333a58ccd817761d5f18644e7afeb4147718e2360ad389bd1326c4abf712d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3584675bdde8360032c2b7e944eba38d312ac092e45f1e35f8ae938409ed8bac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5dc6d634e4be62e41ca099c94a9a6c40014961d8e67b14484545973cadfdfef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c81fbc278359a307839ea9215efeafbbde660ada7120c36eea0490e4abb948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e98fd37105ead5ec86ffdcf9ac584a77d9d8451f5651f8c84ea59f22b75ceb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2701bd2c7043f68a8f40f916d9164584b7c21363ee8a5e1819ef56a0fed85a(
    *,
    malware_scanner: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    scanner_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467657443fbd5da267597d7875c7dab95796594dc8925ea6168a898365b79302(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697fada9b2648415e9bf205cb67f0e1839f27b7c4d107e04939ee00cce154681(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d230a871087b894847993c331f7601d7d4b430e1004d9885214b1d9a5800d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9132ede90f0174bd8c5645084690d5c33d7071de2b22f094a2595a5c11bd851b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f7b0fb095d66d7df1ef06bd59acba5e88463ee6888952afb0080f3fd11ebf2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968b10ba4860127ad7622a9e58e99e521cdcce89db3079a66a71097543eaea9d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f60c3f279ff7754e734ec8ffc35efd28da4724aba19e70602c9ada752db00e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81696a1f360f23d869ba1531e0f53cea11a301e1d2ec7aee1498ed35613a1317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38ab178e036d8b2a4f87a2071842905157f693d6ecbbce268486d375611aa95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ca7db83b3ab4c6b681f071d8795d1a87887f9cb8d0a2980c9216f00fe451a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeecd8f0af2961f56ed5bad22b321f296725a53c2f5673931fde9fcf40657d44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]],
) -> None:
    """Type checking stubs"""
    pass
