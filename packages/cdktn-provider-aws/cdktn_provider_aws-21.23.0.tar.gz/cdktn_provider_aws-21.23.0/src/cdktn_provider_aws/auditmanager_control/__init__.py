r'''
# `aws_auditmanager_control`

Refer to the Terraform Registry for docs: [`aws_auditmanager_control`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control).
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


class AuditmanagerControl(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControl",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control aws_auditmanager_control}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        action_plan_instructions: typing.Optional[builtins.str] = None,
        action_plan_title: typing.Optional[builtins.str] = None,
        control_mapping_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditmanagerControlControlMappingSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        testing_information: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control aws_auditmanager_control} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#name AuditmanagerControl#name}.
        :param action_plan_instructions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#action_plan_instructions AuditmanagerControl#action_plan_instructions}.
        :param action_plan_title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#action_plan_title AuditmanagerControl#action_plan_title}.
        :param control_mapping_sources: control_mapping_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#control_mapping_sources AuditmanagerControl#control_mapping_sources}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#description AuditmanagerControl#description}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#region AuditmanagerControl#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#tags AuditmanagerControl#tags}.
        :param testing_information: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#testing_information AuditmanagerControl#testing_information}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2dbca546e536dc69c5fc7fc3e86ab3ed7c98192ec65c70efac18ff316dbe09)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AuditmanagerControlConfig(
            name=name,
            action_plan_instructions=action_plan_instructions,
            action_plan_title=action_plan_title,
            control_mapping_sources=control_mapping_sources,
            description=description,
            region=region,
            tags=tags,
            testing_information=testing_information,
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
        '''Generates CDKTF code for importing a AuditmanagerControl resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AuditmanagerControl to import.
        :param import_from_id: The id of the existing AuditmanagerControl that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AuditmanagerControl to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1adfef42ce813c2944b206603f348bd2091edf4602b6dadb886e1ffdd7b7eda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putControlMappingSources")
    def put_control_mapping_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditmanagerControlControlMappingSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e23d83bc6619c66f45462f5f7c09c5673f5d40c6092b9cd9ede775fb2c421a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putControlMappingSources", [value]))

    @jsii.member(jsii_name="resetActionPlanInstructions")
    def reset_action_plan_instructions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionPlanInstructions", []))

    @jsii.member(jsii_name="resetActionPlanTitle")
    def reset_action_plan_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionPlanTitle", []))

    @jsii.member(jsii_name="resetControlMappingSources")
    def reset_control_mapping_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlMappingSources", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTestingInformation")
    def reset_testing_information(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestingInformation", []))

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
    @jsii.member(jsii_name="controlMappingSources")
    def control_mapping_sources(self) -> "AuditmanagerControlControlMappingSourcesList":
        return typing.cast("AuditmanagerControlControlMappingSourcesList", jsii.get(self, "controlMappingSources"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="actionPlanInstructionsInput")
    def action_plan_instructions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionPlanInstructionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actionPlanTitleInput")
    def action_plan_title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionPlanTitleInput"))

    @builtins.property
    @jsii.member(jsii_name="controlMappingSourcesInput")
    def control_mapping_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSources"]]], jsii.get(self, "controlMappingSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="testingInformationInput")
    def testing_information_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "testingInformationInput"))

    @builtins.property
    @jsii.member(jsii_name="actionPlanInstructions")
    def action_plan_instructions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionPlanInstructions"))

    @action_plan_instructions.setter
    def action_plan_instructions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4837a22d9e6284c39fe84950e5b138ee418975b10844dceac62b24da69b3b859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionPlanInstructions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actionPlanTitle")
    def action_plan_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionPlanTitle"))

    @action_plan_title.setter
    def action_plan_title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6983d9690e92d1e3ec6ee826b943fa91fb1834843c90157551d45ac1b17a3601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionPlanTitle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421bf0abcc5ef8fba598939a5029e364609254633c1d5e9e5d30fe342791f12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbc50294705e6d34da8f33a91a136802f0b87171df739092090dce547c92dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__accc9c189deac13f7b0cdade83b00ca11b3e78364dc30fd6015025c56795777d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44306641a30717fe1c5ad036ee9387e36a78b448a51cc57e054d0989fc6e0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testingInformation")
    def testing_information(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testingInformation"))

    @testing_information.setter
    def testing_information(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e785df32b56a4df88d14b0c4fc3fc2535d7c4a632e0d6a6e5472a6d2bd4754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testingInformation", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlConfig",
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
        "action_plan_instructions": "actionPlanInstructions",
        "action_plan_title": "actionPlanTitle",
        "control_mapping_sources": "controlMappingSources",
        "description": "description",
        "region": "region",
        "tags": "tags",
        "testing_information": "testingInformation",
    },
)
class AuditmanagerControlConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action_plan_instructions: typing.Optional[builtins.str] = None,
        action_plan_title: typing.Optional[builtins.str] = None,
        control_mapping_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditmanagerControlControlMappingSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        testing_information: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#name AuditmanagerControl#name}.
        :param action_plan_instructions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#action_plan_instructions AuditmanagerControl#action_plan_instructions}.
        :param action_plan_title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#action_plan_title AuditmanagerControl#action_plan_title}.
        :param control_mapping_sources: control_mapping_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#control_mapping_sources AuditmanagerControl#control_mapping_sources}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#description AuditmanagerControl#description}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#region AuditmanagerControl#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#tags AuditmanagerControl#tags}.
        :param testing_information: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#testing_information AuditmanagerControl#testing_information}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fd393e8dcce079e162efb580a1c0518bf5c0c2e2c9c8cccf41466ce3c17409)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument action_plan_instructions", value=action_plan_instructions, expected_type=type_hints["action_plan_instructions"])
            check_type(argname="argument action_plan_title", value=action_plan_title, expected_type=type_hints["action_plan_title"])
            check_type(argname="argument control_mapping_sources", value=control_mapping_sources, expected_type=type_hints["control_mapping_sources"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument testing_information", value=testing_information, expected_type=type_hints["testing_information"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if action_plan_instructions is not None:
            self._values["action_plan_instructions"] = action_plan_instructions
        if action_plan_title is not None:
            self._values["action_plan_title"] = action_plan_title
        if control_mapping_sources is not None:
            self._values["control_mapping_sources"] = control_mapping_sources
        if description is not None:
            self._values["description"] = description
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if testing_information is not None:
            self._values["testing_information"] = testing_information

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#name AuditmanagerControl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_plan_instructions(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#action_plan_instructions AuditmanagerControl#action_plan_instructions}.'''
        result = self._values.get("action_plan_instructions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def action_plan_title(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#action_plan_title AuditmanagerControl#action_plan_title}.'''
        result = self._values.get("action_plan_title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_mapping_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSources"]]]:
        '''control_mapping_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#control_mapping_sources AuditmanagerControl#control_mapping_sources}
        '''
        result = self._values.get("control_mapping_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSources"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#description AuditmanagerControl#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#region AuditmanagerControl#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#tags AuditmanagerControl#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def testing_information(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#testing_information AuditmanagerControl#testing_information}.'''
        result = self._values.get("testing_information")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuditmanagerControlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlControlMappingSources",
    jsii_struct_bases=[],
    name_mapping={
        "source_name": "sourceName",
        "source_set_up_option": "sourceSetUpOption",
        "source_type": "sourceType",
        "source_description": "sourceDescription",
        "source_frequency": "sourceFrequency",
        "source_keyword": "sourceKeyword",
        "troubleshooting_text": "troubleshootingText",
    },
)
class AuditmanagerControlControlMappingSources:
    def __init__(
        self,
        *,
        source_name: builtins.str,
        source_set_up_option: builtins.str,
        source_type: builtins.str,
        source_description: typing.Optional[builtins.str] = None,
        source_frequency: typing.Optional[builtins.str] = None,
        source_keyword: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditmanagerControlControlMappingSourcesSourceKeyword", typing.Dict[builtins.str, typing.Any]]]]] = None,
        troubleshooting_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_name AuditmanagerControl#source_name}.
        :param source_set_up_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_set_up_option AuditmanagerControl#source_set_up_option}.
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_type AuditmanagerControl#source_type}.
        :param source_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_description AuditmanagerControl#source_description}.
        :param source_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_frequency AuditmanagerControl#source_frequency}.
        :param source_keyword: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_keyword AuditmanagerControl#source_keyword}.
        :param troubleshooting_text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#troubleshooting_text AuditmanagerControl#troubleshooting_text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ae316c3145609bb1e4c8f2f64940df082bc6652f0fc78daa1e7d722d5d3352)
            check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
            check_type(argname="argument source_set_up_option", value=source_set_up_option, expected_type=type_hints["source_set_up_option"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument source_description", value=source_description, expected_type=type_hints["source_description"])
            check_type(argname="argument source_frequency", value=source_frequency, expected_type=type_hints["source_frequency"])
            check_type(argname="argument source_keyword", value=source_keyword, expected_type=type_hints["source_keyword"])
            check_type(argname="argument troubleshooting_text", value=troubleshooting_text, expected_type=type_hints["troubleshooting_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_name": source_name,
            "source_set_up_option": source_set_up_option,
            "source_type": source_type,
        }
        if source_description is not None:
            self._values["source_description"] = source_description
        if source_frequency is not None:
            self._values["source_frequency"] = source_frequency
        if source_keyword is not None:
            self._values["source_keyword"] = source_keyword
        if troubleshooting_text is not None:
            self._values["troubleshooting_text"] = troubleshooting_text

    @builtins.property
    def source_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_name AuditmanagerControl#source_name}.'''
        result = self._values.get("source_name")
        assert result is not None, "Required property 'source_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_set_up_option(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_set_up_option AuditmanagerControl#source_set_up_option}.'''
        result = self._values.get("source_set_up_option")
        assert result is not None, "Required property 'source_set_up_option' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_type AuditmanagerControl#source_type}.'''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_description AuditmanagerControl#source_description}.'''
        result = self._values.get("source_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_frequency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_frequency AuditmanagerControl#source_frequency}.'''
        result = self._values.get("source_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_keyword(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSourcesSourceKeyword"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#source_keyword AuditmanagerControl#source_keyword}.'''
        result = self._values.get("source_keyword")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSourcesSourceKeyword"]]], result)

    @builtins.property
    def troubleshooting_text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#troubleshooting_text AuditmanagerControl#troubleshooting_text}.'''
        result = self._values.get("troubleshooting_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuditmanagerControlControlMappingSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuditmanagerControlControlMappingSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlControlMappingSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f50cdd6d8d00675e2af2ba589c2b580c0a3f913b8b76fcdb2f88f464b590fe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AuditmanagerControlControlMappingSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9707679ba43f13c65a86b9bb0972b257c7b185869317df8fb88b8e7ea908e0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AuditmanagerControlControlMappingSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c8f219932ff4946f7a94a2b7e61e607a7a4cfe05710c50182ada874a8dc80f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca96d6d0ff7547713c3f09c9ba7f8d1ecb38aa62c0e5a464ce7da4bb86f8331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd20ca490f542a45436a75b154c9dfc1f1dfaa089739162df9ee79ce8e0d11d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d7bd9dde418b290bdc033cc67d5c3e83ac98bfe0398170ec7e7e8000ee3d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AuditmanagerControlControlMappingSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlControlMappingSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb49edd63c7091a51216b5b96f9625a0ed35b95de64428f8f094ac4a0235d9c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSourceKeyword")
    def put_source_keyword(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditmanagerControlControlMappingSourcesSourceKeyword", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605aac341903818d1294b2c95df97db5d376b564a24fa07c7bb7669dcc9b49b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceKeyword", [value]))

    @jsii.member(jsii_name="resetSourceDescription")
    def reset_source_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDescription", []))

    @jsii.member(jsii_name="resetSourceFrequency")
    def reset_source_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFrequency", []))

    @jsii.member(jsii_name="resetSourceKeyword")
    def reset_source_keyword(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceKeyword", []))

    @jsii.member(jsii_name="resetTroubleshootingText")
    def reset_troubleshooting_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTroubleshootingText", []))

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @builtins.property
    @jsii.member(jsii_name="sourceKeyword")
    def source_keyword(
        self,
    ) -> "AuditmanagerControlControlMappingSourcesSourceKeywordList":
        return typing.cast("AuditmanagerControlControlMappingSourcesSourceKeywordList", jsii.get(self, "sourceKeyword"))

    @builtins.property
    @jsii.member(jsii_name="sourceDescriptionInput")
    def source_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFrequencyInput")
    def source_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKeywordInput")
    def source_keyword_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSourcesSourceKeyword"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditmanagerControlControlMappingSourcesSourceKeyword"]]], jsii.get(self, "sourceKeywordInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNameInput")
    def source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSetUpOptionInput")
    def source_set_up_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSetUpOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="troubleshootingTextInput")
    def troubleshooting_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "troubleshootingTextInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDescription")
    def source_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDescription"))

    @source_description.setter
    def source_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d331cab0c46fabed1484eb241e45054bcec8f0426a8154a77f27f86a0de10b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFrequency")
    def source_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFrequency"))

    @source_frequency.setter
    def source_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b2bc1078f29e410277c14c4a7b83402471641542630fc2686a7a1f4fdfada7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceName")
    def source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceName"))

    @source_name.setter
    def source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfb67091bebe3ef764becf77cd996ea30f31f824ef1dac87d27cbfd94ecde90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSetUpOption")
    def source_set_up_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSetUpOption"))

    @source_set_up_option.setter
    def source_set_up_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b865b97313ff07c640d4f1647231b229f6c7c55b8f79d649a8415a190e9419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSetUpOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f17687407c1f88921f8a015a356f0394a6118ea98f29bd4923155931f0e8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="troubleshootingText")
    def troubleshooting_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "troubleshootingText"))

    @troubleshooting_text.setter
    def troubleshooting_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7de29d6d945c78277f66d579a84de098c18bd8d3da2e620b685150e0db29773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "troubleshootingText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d947b0c1511a0feb1c96e1b2480f199985f02d335184ba904e295db7e57d57b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlControlMappingSourcesSourceKeyword",
    jsii_struct_bases=[],
    name_mapping={
        "keyword_input_type": "keywordInputType",
        "keyword_value": "keywordValue",
    },
)
class AuditmanagerControlControlMappingSourcesSourceKeyword:
    def __init__(
        self,
        *,
        keyword_input_type: typing.Optional[builtins.str] = None,
        keyword_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keyword_input_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#keyword_input_type AuditmanagerControl#keyword_input_type}.
        :param keyword_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#keyword_value AuditmanagerControl#keyword_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87751001525d78bebab66c7c7a4dab00870b5ad8b25fbc849c5d9fa6ee058154)
            check_type(argname="argument keyword_input_type", value=keyword_input_type, expected_type=type_hints["keyword_input_type"])
            check_type(argname="argument keyword_value", value=keyword_value, expected_type=type_hints["keyword_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if keyword_input_type is not None:
            self._values["keyword_input_type"] = keyword_input_type
        if keyword_value is not None:
            self._values["keyword_value"] = keyword_value

    @builtins.property
    def keyword_input_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#keyword_input_type AuditmanagerControl#keyword_input_type}.'''
        result = self._values.get("keyword_input_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keyword_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/auditmanager_control#keyword_value AuditmanagerControl#keyword_value}.'''
        result = self._values.get("keyword_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuditmanagerControlControlMappingSourcesSourceKeyword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuditmanagerControlControlMappingSourcesSourceKeywordList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlControlMappingSourcesSourceKeywordList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef1702af8a5c09c5dbc60817662a120fba93ada2288e8bfbb8ec07a04b6c1b56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AuditmanagerControlControlMappingSourcesSourceKeywordOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8bc0ce651e5c1e45d9d0ee986b55bf0c14dca1d193a148d8600835c9856e47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AuditmanagerControlControlMappingSourcesSourceKeywordOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2537a1f532a1225c067bf7c5198a65885753c916c5bbd2cb6165929dd5513b66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78373917d5c3b2b5d32b03aeb97986555d0d0e38e9616980cba95ba8c5fb1783)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2614726fde857f4c2fe8077a878e325932d5f4a0a2d2aed684dfe1c0515e4cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSourcesSourceKeyword]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSourcesSourceKeyword]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSourcesSourceKeyword]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fa613d1aff6fcdb441da56dc71a27e65ccaec4c030d0baacb259f0ef11d58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AuditmanagerControlControlMappingSourcesSourceKeywordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.auditmanagerControl.AuditmanagerControlControlMappingSourcesSourceKeywordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__980fb4102fa3ae3fc1c1421998cee79a9aa451f9a2b4a201134070bccc98922d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKeywordInputType")
    def reset_keyword_input_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeywordInputType", []))

    @jsii.member(jsii_name="resetKeywordValue")
    def reset_keyword_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeywordValue", []))

    @builtins.property
    @jsii.member(jsii_name="keywordInputTypeInput")
    def keyword_input_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keywordInputTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordValueInput")
    def keyword_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keywordValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordInputType")
    def keyword_input_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keywordInputType"))

    @keyword_input_type.setter
    def keyword_input_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9730112cdadbd7bdcef1201d176c78cd069e5b3eb5ae4a8d7a227a68108753ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywordInputType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keywordValue")
    def keyword_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keywordValue"))

    @keyword_value.setter
    def keyword_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8479828f97e23ebac8c90628b04d97f32a83dba78833c54d966066555b514d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywordValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSourcesSourceKeyword]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSourcesSourceKeyword]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSourcesSourceKeyword]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12aeac754fd3456403957cf108b494efa1639556554dec0ce780c7c1e04bb194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AuditmanagerControl",
    "AuditmanagerControlConfig",
    "AuditmanagerControlControlMappingSources",
    "AuditmanagerControlControlMappingSourcesList",
    "AuditmanagerControlControlMappingSourcesOutputReference",
    "AuditmanagerControlControlMappingSourcesSourceKeyword",
    "AuditmanagerControlControlMappingSourcesSourceKeywordList",
    "AuditmanagerControlControlMappingSourcesSourceKeywordOutputReference",
]

publication.publish()

def _typecheckingstub__fe2dbca546e536dc69c5fc7fc3e86ab3ed7c98192ec65c70efac18ff316dbe09(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    action_plan_instructions: typing.Optional[builtins.str] = None,
    action_plan_title: typing.Optional[builtins.str] = None,
    control_mapping_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditmanagerControlControlMappingSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    testing_information: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e1adfef42ce813c2944b206603f348bd2091edf4602b6dadb886e1ffdd7b7eda(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e23d83bc6619c66f45462f5f7c09c5673f5d40c6092b9cd9ede775fb2c421a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditmanagerControlControlMappingSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4837a22d9e6284c39fe84950e5b138ee418975b10844dceac62b24da69b3b859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6983d9690e92d1e3ec6ee826b943fa91fb1834843c90157551d45ac1b17a3601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421bf0abcc5ef8fba598939a5029e364609254633c1d5e9e5d30fe342791f12d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbc50294705e6d34da8f33a91a136802f0b87171df739092090dce547c92dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accc9c189deac13f7b0cdade83b00ca11b3e78364dc30fd6015025c56795777d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44306641a30717fe1c5ad036ee9387e36a78b448a51cc57e054d0989fc6e0aa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e785df32b56a4df88d14b0c4fc3fc2535d7c4a632e0d6a6e5472a6d2bd4754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fd393e8dcce079e162efb580a1c0518bf5c0c2e2c9c8cccf41466ce3c17409(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    action_plan_instructions: typing.Optional[builtins.str] = None,
    action_plan_title: typing.Optional[builtins.str] = None,
    control_mapping_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditmanagerControlControlMappingSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    testing_information: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ae316c3145609bb1e4c8f2f64940df082bc6652f0fc78daa1e7d722d5d3352(
    *,
    source_name: builtins.str,
    source_set_up_option: builtins.str,
    source_type: builtins.str,
    source_description: typing.Optional[builtins.str] = None,
    source_frequency: typing.Optional[builtins.str] = None,
    source_keyword: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditmanagerControlControlMappingSourcesSourceKeyword, typing.Dict[builtins.str, typing.Any]]]]] = None,
    troubleshooting_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f50cdd6d8d00675e2af2ba589c2b580c0a3f913b8b76fcdb2f88f464b590fe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9707679ba43f13c65a86b9bb0972b257c7b185869317df8fb88b8e7ea908e0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c8f219932ff4946f7a94a2b7e61e607a7a4cfe05710c50182ada874a8dc80f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca96d6d0ff7547713c3f09c9ba7f8d1ecb38aa62c0e5a464ce7da4bb86f8331(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd20ca490f542a45436a75b154c9dfc1f1dfaa089739162df9ee79ce8e0d11d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d7bd9dde418b290bdc033cc67d5c3e83ac98bfe0398170ec7e7e8000ee3d43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb49edd63c7091a51216b5b96f9625a0ed35b95de64428f8f094ac4a0235d9c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605aac341903818d1294b2c95df97db5d376b564a24fa07c7bb7669dcc9b49b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditmanagerControlControlMappingSourcesSourceKeyword, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d331cab0c46fabed1484eb241e45054bcec8f0426a8154a77f27f86a0de10b3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b2bc1078f29e410277c14c4a7b83402471641542630fc2686a7a1f4fdfada7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfb67091bebe3ef764becf77cd996ea30f31f824ef1dac87d27cbfd94ecde90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b865b97313ff07c640d4f1647231b229f6c7c55b8f79d649a8415a190e9419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f17687407c1f88921f8a015a356f0394a6118ea98f29bd4923155931f0e8e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7de29d6d945c78277f66d579a84de098c18bd8d3da2e620b685150e0db29773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d947b0c1511a0feb1c96e1b2480f199985f02d335184ba904e295db7e57d57b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87751001525d78bebab66c7c7a4dab00870b5ad8b25fbc849c5d9fa6ee058154(
    *,
    keyword_input_type: typing.Optional[builtins.str] = None,
    keyword_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1702af8a5c09c5dbc60817662a120fba93ada2288e8bfbb8ec07a04b6c1b56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8bc0ce651e5c1e45d9d0ee986b55bf0c14dca1d193a148d8600835c9856e47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2537a1f532a1225c067bf7c5198a65885753c916c5bbd2cb6165929dd5513b66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78373917d5c3b2b5d32b03aeb97986555d0d0e38e9616980cba95ba8c5fb1783(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2614726fde857f4c2fe8077a878e325932d5f4a0a2d2aed684dfe1c0515e4cf9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fa613d1aff6fcdb441da56dc71a27e65ccaec4c030d0baacb259f0ef11d58f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditmanagerControlControlMappingSourcesSourceKeyword]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980fb4102fa3ae3fc1c1421998cee79a9aa451f9a2b4a201134070bccc98922d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9730112cdadbd7bdcef1201d176c78cd069e5b3eb5ae4a8d7a227a68108753ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8479828f97e23ebac8c90628b04d97f32a83dba78833c54d966066555b514d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12aeac754fd3456403957cf108b494efa1639556554dec0ce780c7c1e04bb194(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditmanagerControlControlMappingSourcesSourceKeyword]],
) -> None:
    """Type checking stubs"""
    pass
