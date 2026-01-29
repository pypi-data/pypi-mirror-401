r'''
# `aws_securityhub_automation_rule`

Refer to the Terraform Registry for docs: [`aws_securityhub_automation_rule`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule).
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


class SecurityhubAutomationRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule aws_securityhub_automation_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        rule_name: builtins.str,
        rule_order: jsii.Number,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_terminal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        rule_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule aws_securityhub_automation_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#description SecurityhubAutomationRule#description}.
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_name SecurityhubAutomationRule#rule_name}.
        :param rule_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_order SecurityhubAutomationRule#rule_order}.
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#actions SecurityhubAutomationRule#actions}
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criteria SecurityhubAutomationRule#criteria}
        :param is_terminal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#is_terminal SecurityhubAutomationRule#is_terminal}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#region SecurityhubAutomationRule#region}
        :param rule_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_status SecurityhubAutomationRule#rule_status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#tags SecurityhubAutomationRule#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eeb3ec78ea520ee4282e0d03beaf5d4cdf2f740d890c68a0c712ec029dec2e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SecurityhubAutomationRuleConfig(
            description=description,
            rule_name=rule_name,
            rule_order=rule_order,
            actions=actions,
            criteria=criteria,
            is_terminal=is_terminal,
            region=region,
            rule_status=rule_status,
            tags=tags,
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
        '''Generates CDKTF code for importing a SecurityhubAutomationRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecurityhubAutomationRule to import.
        :param import_from_id: The id of the existing SecurityhubAutomationRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecurityhubAutomationRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db812b48f8db9f14e677047fb32de624a31b14197f1cbc6dfa688b08b374d41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81eb622f813f07fbfb17b4bb88e2163fbe60868acebff13105232752a632bd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putCriteria")
    def put_criteria(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400c9b69cf6dbde6f9736be4e72275c9a9890c10ec62bf199a386f8ca71b08fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCriteria", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetCriteria")
    def reset_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriteria", []))

    @jsii.member(jsii_name="resetIsTerminal")
    def reset_is_terminal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsTerminal", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRuleStatus")
    def reset_rule_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleStatus", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> "SecurityhubAutomationRuleActionsList":
        return typing.cast("SecurityhubAutomationRuleActionsList", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> "SecurityhubAutomationRuleCriteriaList":
        return typing.cast("SecurityhubAutomationRuleCriteriaList", jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActions"]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteria"]]], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="isTerminalInput")
    def is_terminal_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isTerminalInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleOrderInput")
    def rule_order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleStatusInput")
    def rule_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f023931f8146dc1f43a1b4c8282ea050c092ab8a51d4a1752a8a689ff1de4283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isTerminal")
    def is_terminal(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isTerminal"))

    @is_terminal.setter
    def is_terminal(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ebc14eb6a9652082c9df33c67bc66dd923040abe0245d4465e0a64f2f976cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTerminal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44673460bfeaa91a7c4eb4ee7547095edb83b2831c58dc5750574e17062f1003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c0e5fff10ed6d2a772b02809ebff8ec603c3240130a4d9e8726f59fbf675e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleOrder")
    def rule_order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleOrder"))

    @rule_order.setter
    def rule_order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cc7df9f6495445e940d7edec08f73e4bbd6db60982f014e9bf5128d184a6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleStatus")
    def rule_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleStatus"))

    @rule_status.setter
    def rule_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0927e90d0bd49ad51d4ae92114812658c7a5af1ce782f109a889740ce53d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573b98cb22c4a147529ad8d7c14b2c120cd3169c6ab40f04ff7e8f6d7b6d1ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActions",
    jsii_struct_bases=[],
    name_mapping={"finding_fields_update": "findingFieldsUpdate", "type": "type"},
)
class SecurityhubAutomationRuleActions:
    def __init__(
        self,
        *,
        finding_fields_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param finding_fields_update: finding_fields_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#finding_fields_update SecurityhubAutomationRule#finding_fields_update}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#type SecurityhubAutomationRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bde57982a92d3d3ef0f29c0670eb9b4c73f7adb43bf3e579b69ee1e6919504)
            check_type(argname="argument finding_fields_update", value=finding_fields_update, expected_type=type_hints["finding_fields_update"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if finding_fields_update is not None:
            self._values["finding_fields_update"] = finding_fields_update
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def finding_fields_update(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdate"]]]:
        '''finding_fields_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#finding_fields_update SecurityhubAutomationRule#finding_fields_update}
        '''
        result = self._values.get("finding_fields_update")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdate"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#type SecurityhubAutomationRule#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdate",
    jsii_struct_bases=[],
    name_mapping={
        "confidence": "confidence",
        "criticality": "criticality",
        "note": "note",
        "related_findings": "relatedFindings",
        "severity": "severity",
        "types": "types",
        "user_defined_fields": "userDefinedFields",
        "verification_state": "verificationState",
        "workflow": "workflow",
    },
)
class SecurityhubAutomationRuleActionsFindingFieldsUpdate:
    def __init__(
        self,
        *,
        confidence: typing.Optional[jsii.Number] = None,
        criticality: typing.Optional[jsii.Number] = None,
        note: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateNote", typing.Dict[builtins.str, typing.Any]]]]] = None,
        related_findings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_defined_fields: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        verification_state: typing.Optional[builtins.str] = None,
        workflow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param confidence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#confidence SecurityhubAutomationRule#confidence}.
        :param criticality: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criticality SecurityhubAutomationRule#criticality}.
        :param note: note block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note SecurityhubAutomationRule#note}
        :param related_findings: related_findings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#related_findings SecurityhubAutomationRule#related_findings}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#severity SecurityhubAutomationRule#severity}
        :param types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#types SecurityhubAutomationRule#types}.
        :param user_defined_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#user_defined_fields SecurityhubAutomationRule#user_defined_fields}.
        :param verification_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#verification_state SecurityhubAutomationRule#verification_state}.
        :param workflow: workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#workflow SecurityhubAutomationRule#workflow}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62d737f838fbda4b759151bcfd26e7f9221bcba1c35abbd3da2378f9fff1e41)
            check_type(argname="argument confidence", value=confidence, expected_type=type_hints["confidence"])
            check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
            check_type(argname="argument note", value=note, expected_type=type_hints["note"])
            check_type(argname="argument related_findings", value=related_findings, expected_type=type_hints["related_findings"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
            check_type(argname="argument verification_state", value=verification_state, expected_type=type_hints["verification_state"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidence is not None:
            self._values["confidence"] = confidence
        if criticality is not None:
            self._values["criticality"] = criticality
        if note is not None:
            self._values["note"] = note
        if related_findings is not None:
            self._values["related_findings"] = related_findings
        if severity is not None:
            self._values["severity"] = severity
        if types is not None:
            self._values["types"] = types
        if user_defined_fields is not None:
            self._values["user_defined_fields"] = user_defined_fields
        if verification_state is not None:
            self._values["verification_state"] = verification_state
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def confidence(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#confidence SecurityhubAutomationRule#confidence}.'''
        result = self._values.get("confidence")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def criticality(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criticality SecurityhubAutomationRule#criticality}.'''
        result = self._values.get("criticality")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def note(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateNote"]]]:
        '''note block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note SecurityhubAutomationRule#note}
        '''
        result = self._values.get("note")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateNote"]]], result)

    @builtins.property
    def related_findings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings"]]]:
        '''related_findings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#related_findings SecurityhubAutomationRule#related_findings}
        '''
        result = self._values.get("related_findings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings"]]], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity"]]]:
        '''severity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#severity SecurityhubAutomationRule#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity"]]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#types SecurityhubAutomationRule#types}.'''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_defined_fields(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#user_defined_fields SecurityhubAutomationRule#user_defined_fields}.'''
        result = self._values.get("user_defined_fields")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def verification_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#verification_state SecurityhubAutomationRule#verification_state}.'''
        result = self._values.get("verification_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow"]]]:
        '''workflow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#workflow SecurityhubAutomationRule#workflow}
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleActionsFindingFieldsUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleActionsFindingFieldsUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b5aed5a102a632d47e9f9c7fe25900946e26b27ab8eb46b96f8dade1481c488)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d634a01de2ca55d17360cedaedcc7044e4d696c2209786922753b8ca9f50e4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de279e960f0025c69326a3b6e2195ac74acd79400aef73a14fabc5ec4ee05b51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1180d290c5ed6ab75e5339ad60f89094449e86602b0c723d8072cafd808dabe0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__456ce6888102561ca5622d0335af0537f51f2ca2f2b193cf3a642a41e854d61e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbf9080abc2ba435c7e58693449050a488f34f1eb9a539b868cee1c9a4b102a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateNote",
    jsii_struct_bases=[],
    name_mapping={"text": "text", "updated_by": "updatedBy"},
)
class SecurityhubAutomationRuleActionsFindingFieldsUpdateNote:
    def __init__(self, *, text: builtins.str, updated_by: builtins.str) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#text SecurityhubAutomationRule#text}.
        :param updated_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#updated_by SecurityhubAutomationRule#updated_by}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f615ec6fcaa5e3f12f2a28ad4a41f4827266669299cce160e22bc9249b9008)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument updated_by", value=updated_by, expected_type=type_hints["updated_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
            "updated_by": updated_by,
        }

    @builtins.property
    def text(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#text SecurityhubAutomationRule#text}.'''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def updated_by(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#updated_by SecurityhubAutomationRule#updated_by}.'''
        result = self._values.get("updated_by")
        assert result is not None, "Required property 'updated_by' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleActionsFindingFieldsUpdateNote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8036820f61da81a070a17b624bb8e961c7c5112b671473b9daf6744edc79c3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a51f34232f5abb2d04cb83cc3a31749d6d8d682a183cfd1bd86e32e9c6fc93e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892ca25129cbb76f803f4a2013a4ecdfd6052b4bf00a081ae69431afffa8bad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64cc1621270f337f8a84b3aac81e54ed6599efd6b397509124bba3aa438fdf72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2bc27488a2659515f5407f7f8e42e540a799dcc6a7563b400722e341e68b4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67f92333da43befa3ec26c9f80b3f7f862b2bc342a1525ab7043567a6223d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73d35663b51111665deb8ea5b28b6959694e2ec7bce8e2b9ffd9d78b4a1ff0ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedByInput")
    def updated_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedByInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30cead942f6598b3197a4f2f9f2333b7a6088839d6a66891936abf82763fa0b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedBy")
    def updated_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedBy"))

    @updated_by.setter
    def updated_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8db32fecd25a7a97b4287c42cabcc9d49f1dc08192f7b927c5fe80ec9f01f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fd43c486bcbb9363412d0efb8305007030f6ae8c605f8c245fe824f3147929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsFindingFieldsUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__850a4fd62726aacc4cada00f170645c243507cdcd9fb5d4fe4cd2a0516bdb4e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNote")
    def put_note(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67abc0df576459e5d99b4d8b40ed5ed1c29ef010aeff8e95e94bba5108d714a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNote", [value]))

    @jsii.member(jsii_name="putRelatedFindings")
    def put_related_findings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b404c0d1ec9a61f3812cb6caecf0c135e5fd3db3f4c65e1b8e1ce9c175a8272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRelatedFindings", [value]))

    @jsii.member(jsii_name="putSeverity")
    def put_severity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6e657b2e12a1e4b22e06da77e761eb60187e434b8d16817c15d5f38a33b35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeverity", [value]))

    @jsii.member(jsii_name="putWorkflow")
    def put_workflow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d59f0270a84bf16bec3b43c7b293ca8747c5b1f3840676258192061f7b365ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWorkflow", [value]))

    @jsii.member(jsii_name="resetConfidence")
    def reset_confidence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidence", []))

    @jsii.member(jsii_name="resetCriticality")
    def reset_criticality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriticality", []))

    @jsii.member(jsii_name="resetNote")
    def reset_note(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNote", []))

    @jsii.member(jsii_name="resetRelatedFindings")
    def reset_related_findings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedFindings", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @jsii.member(jsii_name="resetUserDefinedFields")
    def reset_user_defined_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedFields", []))

    @jsii.member(jsii_name="resetVerificationState")
    def reset_verification_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationState", []))

    @jsii.member(jsii_name="resetWorkflow")
    def reset_workflow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflow", []))

    @builtins.property
    @jsii.member(jsii_name="note")
    def note(self) -> SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteList:
        return typing.cast(SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteList, jsii.get(self, "note"))

    @builtins.property
    @jsii.member(jsii_name="relatedFindings")
    def related_findings(
        self,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsList":
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsList", jsii.get(self, "relatedFindings"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(
        self,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityList":
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityList", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(
        self,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowList":
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowList", jsii.get(self, "workflow"))

    @builtins.property
    @jsii.member(jsii_name="confidenceInput")
    def confidence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalityInput")
    def criticality_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "criticalityInput"))

    @builtins.property
    @jsii.member(jsii_name="noteInput")
    def note_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]], jsii.get(self, "noteInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedFindingsInput")
    def related_findings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings"]]], jsii.get(self, "relatedFindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity"]]], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFieldsInput")
    def user_defined_fields_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userDefinedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationStateInput")
    def verification_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verificationStateInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowInput")
    def workflow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow"]]], jsii.get(self, "workflowInput"))

    @builtins.property
    @jsii.member(jsii_name="confidence")
    def confidence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidence"))

    @confidence.setter
    def confidence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861e0f915da6966f543511d20b233e8bd0479b618589fde17e64a0ba44818b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="criticality")
    def criticality(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "criticality"))

    @criticality.setter
    def criticality(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe27524e682593fe95bc52230978e0f395242099639fe2dde5e9007ecd7962aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criticality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f513b880352f994fc0325d67d7353a67bfac4b239791eda72deb2805d9116201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDefinedFields")
    def user_defined_fields(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userDefinedFields"))

    @user_defined_fields.setter
    def user_defined_fields(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f98dddd980960039845e152574d2348338672f78dc7dbaca936f9827336251b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDefinedFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verificationState")
    def verification_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verificationState"))

    @verification_state.setter
    def verification_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a151dd7688dff98488d725d599b793bff399d8349a76e537e0ed66087e20df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verificationState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050b8375b40a5030e1a07528fd88f7edf1a09b9d9c63e835cab9e6108fb4b330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "product_arn": "productArn"},
)
class SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings:
    def __init__(self, *, id: builtins.str, product_arn: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#id SecurityhubAutomationRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param product_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product_arn SecurityhubAutomationRule#product_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bed1ce93a4cd8938aa3e83f1d7a6e284728cd8cb0bf87c41ba5a9e31e5794f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "product_arn": product_arn,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#id SecurityhubAutomationRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product_arn SecurityhubAutomationRule#product_arn}.'''
        result = self._values.get("product_arn")
        assert result is not None, "Required property 'product_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e75a43ae00f2aea7315f6f06b179f764b262c5d7a0bfbb943ac0352f00df4535)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a5042e6cc4ac41961fe521a37184577d10934eff8e52a8563cf2cad8d318b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fb188c41de6a7e72e700a90c2e9042f03a0819b542e05a2938d7c4f8f70e6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e2a844b3043502114a379005130a6cf4eaa0c5bb7f0370d0d27a958aa8488c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcb180bcfcdf6a4c0ef41e6d0638dbe74216cab4ab51e356f15d16b44e627f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c536037b91ce2e4bc05c83d189de82953192e545617b2de63743151fa7f705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cc2507dfb6e68518b4f83ac7c8a7b50cbd46f57c7a3bd9d391c31544184011f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="productArnInput")
    def product_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productArnInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898bd23b07f04c60bd6ece7a20bdc66fa14f3cebbe0d042db3561cc9dff5cf36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productArn")
    def product_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productArn"))

    @product_arn.setter
    def product_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0534f28977ff6f7943641a8c5bcd584780c791731aa41314c05d15e65433f545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecca1c3c571c60097b694a6648bbcfa615715062ea4afbe16eed3d0154e2883a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "product": "product"},
)
class SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity:
    def __init__(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        product: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#label SecurityhubAutomationRule#label}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product SecurityhubAutomationRule#product}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284f4affc5c99dba19b25db2f4d822566d50f0515a3c9a64d2d165831db9f017)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if label is not None:
            self._values["label"] = label
        if product is not None:
            self._values["product"] = product

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#label SecurityhubAutomationRule#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product SecurityhubAutomationRule#product}.'''
        result = self._values.get("product")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3010af418b11cf36d48d60b27a45b2217269aa7d5183471f40d4ed0349f20a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4830a2151ad0a46b1c3848da55a06a0961a0704d72406944447ee654d64b52e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61fb70d9c3f7e3513ec85557fe950761d04e912da4dc6208d7eaddb623601be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbdbfd5a8aafeead42c77d5532654b2539c9d4b4803b61fe586b763bc18741c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__718ad3b38999e8066126c11225147f19fd3912597174e448d3c96c1c3a5474f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef53fec22e40c1420ee891f47c425dd81e5b4df3ed2067b3fc9b53f064898435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__019db07d375dc046653122725d172eacba63baa0a5e97745d5d1799b66920c9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetProduct")
    def reset_product(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProduct", []))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="productInput")
    def product_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "productInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97d2da293848ace3a0c14657c66ec21de0bcf7adf7b5bcd76bcfd9ed782805b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="product")
    def product(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "product"))

    @product.setter
    def product(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24cf0f99a1b3a38df1d5c226809dc1876b3a53fde00bfa2ec49a713019e878c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "product", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc72da21b3fc0c33fdbeee32b77294c983584204573ee5023bdd71bd13830fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow:
    def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#status SecurityhubAutomationRule#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec22c3555b05e909b59e4c69f8a5ac1993c42fb154780b689a0171c99f5cd770)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#status SecurityhubAutomationRule#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d08dddd27314ff3d3138faf4e12c1d04768209d185f3db64ce75da6596b05e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b27dbf9ef119e20f1c0f18c8fdb345ea81b2ac1e8daa743e6b59c0d4336bf17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438c78ec2ff361d9fe9c6ece351ef017115efe344a7763c84145d944acec98c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ffb65ec482201b330650e12029e68e8976caa1659448afbdc6e60971fd5497c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5e3849225e151cac4a467e4ce801c87b2a25ad9ac2f05557dd7fd9ffc18885a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8998c45d53ac831783890dc38a128e02a2a3d8b54d1c31b66051481363d481b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3758c8641a8364c6811308bb5e79cf066d27c879b06ecb31e2dbf7315f2b21d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d6d7b25a571f147de2589f97c6746a80bad0417b5ffe281c984be895fce98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2fa46735c3116ca9d6cff991388de6ae7001bdcaac1252b3f0b7a662d0f7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ae7fc6cdf741ff92572e8f7a6494b10e7fc3091e3e0ed48a2faf322d3204d82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41484329168b3370d0760f93018e3f5cc2fa747b4e86f4d9fed041bca1ff585)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbcdcebc98ce6926b6f4b7ef5ced8f54eaecb06606cd1374dcbe9d9a27e3cc33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6edca70a196324ba09a7e6feb6ac4c4a294d073112e055eb97f224bdb23d9222)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c435b6498996ce7aa8321166edaf16f6f82f16f36bc11a49ae512b2fec0b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af13ada39e8cb458f871400af5b621b44f95749613f30de98994df66e9d0676b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__011198c8224fa2390d2af7cf4d0addae544d1b43c337db184b13c2981332b9c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFindingFieldsUpdate")
    def put_finding_fields_update(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf637b6353a87d3d9beed08fddefb4bb3255ce0d26644df3eee3f22f3f34c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFindingFieldsUpdate", [value]))

    @jsii.member(jsii_name="resetFindingFieldsUpdate")
    def reset_finding_fields_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFindingFieldsUpdate", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="findingFieldsUpdate")
    def finding_fields_update(
        self,
    ) -> SecurityhubAutomationRuleActionsFindingFieldsUpdateList:
        return typing.cast(SecurityhubAutomationRuleActionsFindingFieldsUpdateList, jsii.get(self, "findingFieldsUpdate"))

    @builtins.property
    @jsii.member(jsii_name="findingFieldsUpdateInput")
    def finding_fields_update_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdate]]], jsii.get(self, "findingFieldsUpdateInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5c389ec11f1be3b697f0266d7b2f3027137782aaea2b65ff515279b565c7f96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc784cc561777a1076cff1b7d43dd9a6c3e20c0f6bcd4d52d30a63ff60f2a38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "rule_name": "ruleName",
        "rule_order": "ruleOrder",
        "actions": "actions",
        "criteria": "criteria",
        "is_terminal": "isTerminal",
        "region": "region",
        "rule_status": "ruleStatus",
        "tags": "tags",
    },
)
class SecurityhubAutomationRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        rule_name: builtins.str,
        rule_order: jsii.Number,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_terminal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        rule_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#description SecurityhubAutomationRule#description}.
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_name SecurityhubAutomationRule#rule_name}.
        :param rule_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_order SecurityhubAutomationRule#rule_order}.
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#actions SecurityhubAutomationRule#actions}
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criteria SecurityhubAutomationRule#criteria}
        :param is_terminal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#is_terminal SecurityhubAutomationRule#is_terminal}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#region SecurityhubAutomationRule#region}
        :param rule_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_status SecurityhubAutomationRule#rule_status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#tags SecurityhubAutomationRule#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8321edea23b5d2817efd15e671f4935364c63c2ce3da2ea636871dc89a9f5f8f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument is_terminal", value=is_terminal, expected_type=type_hints["is_terminal"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rule_status", value=rule_status, expected_type=type_hints["rule_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "rule_name": rule_name,
            "rule_order": rule_order,
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
        if actions is not None:
            self._values["actions"] = actions
        if criteria is not None:
            self._values["criteria"] = criteria
        if is_terminal is not None:
            self._values["is_terminal"] = is_terminal
        if region is not None:
            self._values["region"] = region
        if rule_status is not None:
            self._values["rule_status"] = rule_status
        if tags is not None:
            self._values["tags"] = tags

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
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#description SecurityhubAutomationRule#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_name SecurityhubAutomationRule#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_order(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_order SecurityhubAutomationRule#rule_order}.'''
        result = self._values.get("rule_order")
        assert result is not None, "Required property 'rule_order' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActions]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#actions SecurityhubAutomationRule#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActions]]], result)

    @builtins.property
    def criteria(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteria"]]]:
        '''criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criteria SecurityhubAutomationRule#criteria}
        '''
        result = self._values.get("criteria")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteria"]]], result)

    @builtins.property
    def is_terminal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#is_terminal SecurityhubAutomationRule#is_terminal}.'''
        result = self._values.get("is_terminal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#region SecurityhubAutomationRule#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#rule_status SecurityhubAutomationRule#rule_status}.'''
        result = self._values.get("rule_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#tags SecurityhubAutomationRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "aws_account_id": "awsAccountId",
        "aws_account_name": "awsAccountName",
        "company_name": "companyName",
        "compliance_associated_standards_id": "complianceAssociatedStandardsId",
        "compliance_security_control_id": "complianceSecurityControlId",
        "compliance_status": "complianceStatus",
        "confidence": "confidence",
        "created_at": "createdAt",
        "criticality": "criticality",
        "description": "description",
        "first_observed_at": "firstObservedAt",
        "generator_id": "generatorId",
        "id": "id",
        "last_observed_at": "lastObservedAt",
        "note_text": "noteText",
        "note_updated_at": "noteUpdatedAt",
        "note_updated_by": "noteUpdatedBy",
        "product_arn": "productArn",
        "product_name": "productName",
        "record_state": "recordState",
        "related_findings_id": "relatedFindingsId",
        "related_findings_product_arn": "relatedFindingsProductArn",
        "resource_application_arn": "resourceApplicationArn",
        "resource_application_name": "resourceApplicationName",
        "resource_details_other": "resourceDetailsOther",
        "resource_id": "resourceId",
        "resource_partition": "resourcePartition",
        "resource_region": "resourceRegion",
        "resource_tags": "resourceTags",
        "resource_type": "resourceType",
        "severity_label": "severityLabel",
        "source_url": "sourceUrl",
        "title": "title",
        "type": "type",
        "updated_at": "updatedAt",
        "user_defined_fields": "userDefinedFields",
        "verification_state": "verificationState",
        "workflow_status": "workflowStatus",
    },
)
class SecurityhubAutomationRuleCriteria:
    def __init__(
        self,
        *,
        aws_account_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaAwsAccountId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aws_account_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaAwsAccountName", typing.Dict[builtins.str, typing.Any]]]]] = None,
        company_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaCompanyName", typing.Dict[builtins.str, typing.Any]]]]] = None,
        compliance_associated_standards_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        compliance_security_control_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaComplianceSecurityControlId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        compliance_status: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaComplianceStatus", typing.Dict[builtins.str, typing.Any]]]]] = None,
        confidence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaConfidence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        created_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaCreatedAt", typing.Dict[builtins.str, typing.Any]]]]] = None,
        criticality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaCriticality", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaDescription", typing.Dict[builtins.str, typing.Any]]]]] = None,
        first_observed_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaFirstObservedAt", typing.Dict[builtins.str, typing.Any]]]]] = None,
        generator_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaGeneratorId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        last_observed_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaLastObservedAt", typing.Dict[builtins.str, typing.Any]]]]] = None,
        note_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaNoteText", typing.Dict[builtins.str, typing.Any]]]]] = None,
        note_updated_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaNoteUpdatedAt", typing.Dict[builtins.str, typing.Any]]]]] = None,
        note_updated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaNoteUpdatedBy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        product_arn: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaProductArn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        product_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaProductName", typing.Dict[builtins.str, typing.Any]]]]] = None,
        record_state: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaRecordState", typing.Dict[builtins.str, typing.Any]]]]] = None,
        related_findings_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaRelatedFindingsId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        related_findings_product_arn: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_application_arn: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceApplicationArn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_application_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceApplicationName", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_details_other: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceDetailsOther", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceId", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_partition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourcePartition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_region: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceRegion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceType", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity_label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaSeverityLabel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaSourceUrl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        title: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaTitle", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaType", typing.Dict[builtins.str, typing.Any]]]]] = None,
        updated_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaUpdatedAt", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        verification_state: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaVerificationState", typing.Dict[builtins.str, typing.Any]]]]] = None,
        workflow_status: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaWorkflowStatus", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param aws_account_id: aws_account_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#aws_account_id SecurityhubAutomationRule#aws_account_id}
        :param aws_account_name: aws_account_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#aws_account_name SecurityhubAutomationRule#aws_account_name}
        :param company_name: company_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#company_name SecurityhubAutomationRule#company_name}
        :param compliance_associated_standards_id: compliance_associated_standards_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#compliance_associated_standards_id SecurityhubAutomationRule#compliance_associated_standards_id}
        :param compliance_security_control_id: compliance_security_control_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#compliance_security_control_id SecurityhubAutomationRule#compliance_security_control_id}
        :param compliance_status: compliance_status block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#compliance_status SecurityhubAutomationRule#compliance_status}
        :param confidence: confidence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#confidence SecurityhubAutomationRule#confidence}
        :param created_at: created_at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#created_at SecurityhubAutomationRule#created_at}
        :param criticality: criticality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criticality SecurityhubAutomationRule#criticality}
        :param description: description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#description SecurityhubAutomationRule#description}
        :param first_observed_at: first_observed_at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#first_observed_at SecurityhubAutomationRule#first_observed_at}
        :param generator_id: generator_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#generator_id SecurityhubAutomationRule#generator_id}
        :param id: id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#id SecurityhubAutomationRule#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_observed_at: last_observed_at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#last_observed_at SecurityhubAutomationRule#last_observed_at}
        :param note_text: note_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note_text SecurityhubAutomationRule#note_text}
        :param note_updated_at: note_updated_at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note_updated_at SecurityhubAutomationRule#note_updated_at}
        :param note_updated_by: note_updated_by block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note_updated_by SecurityhubAutomationRule#note_updated_by}
        :param product_arn: product_arn block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product_arn SecurityhubAutomationRule#product_arn}
        :param product_name: product_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product_name SecurityhubAutomationRule#product_name}
        :param record_state: record_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#record_state SecurityhubAutomationRule#record_state}
        :param related_findings_id: related_findings_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#related_findings_id SecurityhubAutomationRule#related_findings_id}
        :param related_findings_product_arn: related_findings_product_arn block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#related_findings_product_arn SecurityhubAutomationRule#related_findings_product_arn}
        :param resource_application_arn: resource_application_arn block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_application_arn SecurityhubAutomationRule#resource_application_arn}
        :param resource_application_name: resource_application_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_application_name SecurityhubAutomationRule#resource_application_name}
        :param resource_details_other: resource_details_other block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_details_other SecurityhubAutomationRule#resource_details_other}
        :param resource_id: resource_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_id SecurityhubAutomationRule#resource_id}
        :param resource_partition: resource_partition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_partition SecurityhubAutomationRule#resource_partition}
        :param resource_region: resource_region block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_region SecurityhubAutomationRule#resource_region}
        :param resource_tags: resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_tags SecurityhubAutomationRule#resource_tags}
        :param resource_type: resource_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_type SecurityhubAutomationRule#resource_type}
        :param severity_label: severity_label block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#severity_label SecurityhubAutomationRule#severity_label}
        :param source_url: source_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#source_url SecurityhubAutomationRule#source_url}
        :param title: title block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#title SecurityhubAutomationRule#title}
        :param type: type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#type SecurityhubAutomationRule#type}
        :param updated_at: updated_at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#updated_at SecurityhubAutomationRule#updated_at}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#user_defined_fields SecurityhubAutomationRule#user_defined_fields}
        :param verification_state: verification_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#verification_state SecurityhubAutomationRule#verification_state}
        :param workflow_status: workflow_status block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#workflow_status SecurityhubAutomationRule#workflow_status}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b62d539f4de9ca4f8dca2f5bdbfb5c21ab3568550f39a8583fbb84fc8423fd6)
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_account_name", value=aws_account_name, expected_type=type_hints["aws_account_name"])
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
            check_type(argname="argument compliance_associated_standards_id", value=compliance_associated_standards_id, expected_type=type_hints["compliance_associated_standards_id"])
            check_type(argname="argument compliance_security_control_id", value=compliance_security_control_id, expected_type=type_hints["compliance_security_control_id"])
            check_type(argname="argument compliance_status", value=compliance_status, expected_type=type_hints["compliance_status"])
            check_type(argname="argument confidence", value=confidence, expected_type=type_hints["confidence"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument first_observed_at", value=first_observed_at, expected_type=type_hints["first_observed_at"])
            check_type(argname="argument generator_id", value=generator_id, expected_type=type_hints["generator_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument last_observed_at", value=last_observed_at, expected_type=type_hints["last_observed_at"])
            check_type(argname="argument note_text", value=note_text, expected_type=type_hints["note_text"])
            check_type(argname="argument note_updated_at", value=note_updated_at, expected_type=type_hints["note_updated_at"])
            check_type(argname="argument note_updated_by", value=note_updated_by, expected_type=type_hints["note_updated_by"])
            check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
            check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
            check_type(argname="argument record_state", value=record_state, expected_type=type_hints["record_state"])
            check_type(argname="argument related_findings_id", value=related_findings_id, expected_type=type_hints["related_findings_id"])
            check_type(argname="argument related_findings_product_arn", value=related_findings_product_arn, expected_type=type_hints["related_findings_product_arn"])
            check_type(argname="argument resource_application_arn", value=resource_application_arn, expected_type=type_hints["resource_application_arn"])
            check_type(argname="argument resource_application_name", value=resource_application_name, expected_type=type_hints["resource_application_name"])
            check_type(argname="argument resource_details_other", value=resource_details_other, expected_type=type_hints["resource_details_other"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_partition", value=resource_partition, expected_type=type_hints["resource_partition"])
            check_type(argname="argument resource_region", value=resource_region, expected_type=type_hints["resource_region"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument severity_label", value=severity_label, expected_type=type_hints["severity_label"])
            check_type(argname="argument source_url", value=source_url, expected_type=type_hints["source_url"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
            check_type(argname="argument verification_state", value=verification_state, expected_type=type_hints["verification_state"])
            check_type(argname="argument workflow_status", value=workflow_status, expected_type=type_hints["workflow_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if aws_account_name is not None:
            self._values["aws_account_name"] = aws_account_name
        if company_name is not None:
            self._values["company_name"] = company_name
        if compliance_associated_standards_id is not None:
            self._values["compliance_associated_standards_id"] = compliance_associated_standards_id
        if compliance_security_control_id is not None:
            self._values["compliance_security_control_id"] = compliance_security_control_id
        if compliance_status is not None:
            self._values["compliance_status"] = compliance_status
        if confidence is not None:
            self._values["confidence"] = confidence
        if created_at is not None:
            self._values["created_at"] = created_at
        if criticality is not None:
            self._values["criticality"] = criticality
        if description is not None:
            self._values["description"] = description
        if first_observed_at is not None:
            self._values["first_observed_at"] = first_observed_at
        if generator_id is not None:
            self._values["generator_id"] = generator_id
        if id is not None:
            self._values["id"] = id
        if last_observed_at is not None:
            self._values["last_observed_at"] = last_observed_at
        if note_text is not None:
            self._values["note_text"] = note_text
        if note_updated_at is not None:
            self._values["note_updated_at"] = note_updated_at
        if note_updated_by is not None:
            self._values["note_updated_by"] = note_updated_by
        if product_arn is not None:
            self._values["product_arn"] = product_arn
        if product_name is not None:
            self._values["product_name"] = product_name
        if record_state is not None:
            self._values["record_state"] = record_state
        if related_findings_id is not None:
            self._values["related_findings_id"] = related_findings_id
        if related_findings_product_arn is not None:
            self._values["related_findings_product_arn"] = related_findings_product_arn
        if resource_application_arn is not None:
            self._values["resource_application_arn"] = resource_application_arn
        if resource_application_name is not None:
            self._values["resource_application_name"] = resource_application_name
        if resource_details_other is not None:
            self._values["resource_details_other"] = resource_details_other
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_partition is not None:
            self._values["resource_partition"] = resource_partition
        if resource_region is not None:
            self._values["resource_region"] = resource_region
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if severity_label is not None:
            self._values["severity_label"] = severity_label
        if source_url is not None:
            self._values["source_url"] = source_url
        if title is not None:
            self._values["title"] = title
        if type is not None:
            self._values["type"] = type
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if user_defined_fields is not None:
            self._values["user_defined_fields"] = user_defined_fields
        if verification_state is not None:
            self._values["verification_state"] = verification_state
        if workflow_status is not None:
            self._values["workflow_status"] = workflow_status

    @builtins.property
    def aws_account_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaAwsAccountId"]]]:
        '''aws_account_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#aws_account_id SecurityhubAutomationRule#aws_account_id}
        '''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaAwsAccountId"]]], result)

    @builtins.property
    def aws_account_name(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaAwsAccountName"]]]:
        '''aws_account_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#aws_account_name SecurityhubAutomationRule#aws_account_name}
        '''
        result = self._values.get("aws_account_name")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaAwsAccountName"]]], result)

    @builtins.property
    def company_name(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCompanyName"]]]:
        '''company_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#company_name SecurityhubAutomationRule#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCompanyName"]]], result)

    @builtins.property
    def compliance_associated_standards_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId"]]]:
        '''compliance_associated_standards_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#compliance_associated_standards_id SecurityhubAutomationRule#compliance_associated_standards_id}
        '''
        result = self._values.get("compliance_associated_standards_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId"]]], result)

    @builtins.property
    def compliance_security_control_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaComplianceSecurityControlId"]]]:
        '''compliance_security_control_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#compliance_security_control_id SecurityhubAutomationRule#compliance_security_control_id}
        '''
        result = self._values.get("compliance_security_control_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaComplianceSecurityControlId"]]], result)

    @builtins.property
    def compliance_status(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaComplianceStatus"]]]:
        '''compliance_status block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#compliance_status SecurityhubAutomationRule#compliance_status}
        '''
        result = self._values.get("compliance_status")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaComplianceStatus"]]], result)

    @builtins.property
    def confidence(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaConfidence"]]]:
        '''confidence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#confidence SecurityhubAutomationRule#confidence}
        '''
        result = self._values.get("confidence")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaConfidence"]]], result)

    @builtins.property
    def created_at(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCreatedAt"]]]:
        '''created_at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#created_at SecurityhubAutomationRule#created_at}
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCreatedAt"]]], result)

    @builtins.property
    def criticality(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCriticality"]]]:
        '''criticality block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#criticality SecurityhubAutomationRule#criticality}
        '''
        result = self._values.get("criticality")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCriticality"]]], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaDescription"]]]:
        '''description block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#description SecurityhubAutomationRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaDescription"]]], result)

    @builtins.property
    def first_observed_at(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaFirstObservedAt"]]]:
        '''first_observed_at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#first_observed_at SecurityhubAutomationRule#first_observed_at}
        '''
        result = self._values.get("first_observed_at")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaFirstObservedAt"]]], result)

    @builtins.property
    def generator_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaGeneratorId"]]]:
        '''generator_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#generator_id SecurityhubAutomationRule#generator_id}
        '''
        result = self._values.get("generator_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaGeneratorId"]]], result)

    @builtins.property
    def id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaId"]]]:
        '''id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#id SecurityhubAutomationRule#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaId"]]], result)

    @builtins.property
    def last_observed_at(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaLastObservedAt"]]]:
        '''last_observed_at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#last_observed_at SecurityhubAutomationRule#last_observed_at}
        '''
        result = self._values.get("last_observed_at")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaLastObservedAt"]]], result)

    @builtins.property
    def note_text(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteText"]]]:
        '''note_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note_text SecurityhubAutomationRule#note_text}
        '''
        result = self._values.get("note_text")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteText"]]], result)

    @builtins.property
    def note_updated_at(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteUpdatedAt"]]]:
        '''note_updated_at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note_updated_at SecurityhubAutomationRule#note_updated_at}
        '''
        result = self._values.get("note_updated_at")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteUpdatedAt"]]], result)

    @builtins.property
    def note_updated_by(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteUpdatedBy"]]]:
        '''note_updated_by block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#note_updated_by SecurityhubAutomationRule#note_updated_by}
        '''
        result = self._values.get("note_updated_by")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteUpdatedBy"]]], result)

    @builtins.property
    def product_arn(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductArn"]]]:
        '''product_arn block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product_arn SecurityhubAutomationRule#product_arn}
        '''
        result = self._values.get("product_arn")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductArn"]]], result)

    @builtins.property
    def product_name(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductName"]]]:
        '''product_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#product_name SecurityhubAutomationRule#product_name}
        '''
        result = self._values.get("product_name")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductName"]]], result)

    @builtins.property
    def record_state(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRecordState"]]]:
        '''record_state block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#record_state SecurityhubAutomationRule#record_state}
        '''
        result = self._values.get("record_state")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRecordState"]]], result)

    @builtins.property
    def related_findings_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsId"]]]:
        '''related_findings_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#related_findings_id SecurityhubAutomationRule#related_findings_id}
        '''
        result = self._values.get("related_findings_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsId"]]], result)

    @builtins.property
    def related_findings_product_arn(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn"]]]:
        '''related_findings_product_arn block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#related_findings_product_arn SecurityhubAutomationRule#related_findings_product_arn}
        '''
        result = self._values.get("related_findings_product_arn")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn"]]], result)

    @builtins.property
    def resource_application_arn(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationArn"]]]:
        '''resource_application_arn block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_application_arn SecurityhubAutomationRule#resource_application_arn}
        '''
        result = self._values.get("resource_application_arn")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationArn"]]], result)

    @builtins.property
    def resource_application_name(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationName"]]]:
        '''resource_application_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_application_name SecurityhubAutomationRule#resource_application_name}
        '''
        result = self._values.get("resource_application_name")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationName"]]], result)

    @builtins.property
    def resource_details_other(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceDetailsOther"]]]:
        '''resource_details_other block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_details_other SecurityhubAutomationRule#resource_details_other}
        '''
        result = self._values.get("resource_details_other")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceDetailsOther"]]], result)

    @builtins.property
    def resource_id(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceId"]]]:
        '''resource_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_id SecurityhubAutomationRule#resource_id}
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceId"]]], result)

    @builtins.property
    def resource_partition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourcePartition"]]]:
        '''resource_partition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_partition SecurityhubAutomationRule#resource_partition}
        '''
        result = self._values.get("resource_partition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourcePartition"]]], result)

    @builtins.property
    def resource_region(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceRegion"]]]:
        '''resource_region block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_region SecurityhubAutomationRule#resource_region}
        '''
        result = self._values.get("resource_region")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceRegion"]]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceTags"]]]:
        '''resource_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_tags SecurityhubAutomationRule#resource_tags}
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceTags"]]], result)

    @builtins.property
    def resource_type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceType"]]]:
        '''resource_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#resource_type SecurityhubAutomationRule#resource_type}
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceType"]]], result)

    @builtins.property
    def severity_label(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSeverityLabel"]]]:
        '''severity_label block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#severity_label SecurityhubAutomationRule#severity_label}
        '''
        result = self._values.get("severity_label")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSeverityLabel"]]], result)

    @builtins.property
    def source_url(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSourceUrl"]]]:
        '''source_url block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#source_url SecurityhubAutomationRule#source_url}
        '''
        result = self._values.get("source_url")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSourceUrl"]]], result)

    @builtins.property
    def title(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaTitle"]]]:
        '''title block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#title SecurityhubAutomationRule#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaTitle"]]], result)

    @builtins.property
    def type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaType"]]]:
        '''type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#type SecurityhubAutomationRule#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaType"]]], result)

    @builtins.property
    def updated_at(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUpdatedAt"]]]:
        '''updated_at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#updated_at SecurityhubAutomationRule#updated_at}
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUpdatedAt"]]], result)

    @builtins.property
    def user_defined_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUserDefinedFields"]]]:
        '''user_defined_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#user_defined_fields SecurityhubAutomationRule#user_defined_fields}
        '''
        result = self._values.get("user_defined_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUserDefinedFields"]]], result)

    @builtins.property
    def verification_state(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaVerificationState"]]]:
        '''verification_state block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#verification_state SecurityhubAutomationRule#verification_state}
        '''
        result = self._values.get("verification_state")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaVerificationState"]]], result)

    @builtins.property
    def workflow_status(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaWorkflowStatus"]]]:
        '''workflow_status block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#workflow_status SecurityhubAutomationRule#workflow_status}
        '''
        result = self._values.get("workflow_status")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaWorkflowStatus"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaAwsAccountId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaAwsAccountId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990a59df2d40081a02df9bb34b8b6ac0a9c23bd47c340004acd2d021ac23af29)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaAwsAccountId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaAwsAccountIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaAwsAccountIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdcb3a1013f9a882a77a8e59f907b53cb156c90d6a3c49fbd6b86aee024ed996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaAwsAccountIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e3471de7066b84794862a8071e4c82bc594da0d20f997cf4f5c06d2fc5dbc5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaAwsAccountIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a681759164ca3b180c53c527aaaf7813a0c6ee9e4dde1afa3e7952414bf81e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2391c193d627a10e3800ae4d269d7ec912b89176e1d5215bfb795dd7c7170ac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d3c9a2a601ab04977ca4f14b1e1c398ae6531af7629e106375228cfed9e8945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564ec8fdfd4ccc5a893e606c26fd2c83e0955ac08bc17d1f780b910a1aad1c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaAwsAccountIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaAwsAccountIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06a47ae0fed5927dd6ef48a1a063c2d13b75288dd8ef8ac008d3b60d8a692d21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712740cf4056ef4d8be75b5a403c3bf61827756f0d99a2d2522629874cd8e82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ebc25b2531d4f95ad021207a5c34823b2fa5004b00680891eb0830bbc00317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64fe86ee22539858fba605bda16dd57c7cbb8bbe47f57f7e0bedf2ec7845fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaAwsAccountName",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaAwsAccountName:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c3b438d481ca82df63dabd5be65088254781f23315d996977f7f9a41755b86)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaAwsAccountName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaAwsAccountNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaAwsAccountNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fbbba3da11c8c7849b3ff8b4654647d8c8498def3eb8eca43ff09c0d4e4de8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaAwsAccountNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18dcc1682bf92a8bf7048c0dc9abdb5de753a0f10039c2e0a9fc828e70256ad7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaAwsAccountNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4af37298d58ef4caf6053ae28ea6c43e05d3060b7f539ace1d677b41955ee45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab5c46242a960a1f677be18cee6a01b7913d171d9a513672aa3deb3c02c5ac7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6c20ec0a90cf2be67fc719c0c02351614bf3a6c325e771beed7f7fd05563217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountName]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountName]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236a77141d94e64db4376b2e8af891f3e0f58254ee98849562958759c5335a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaAwsAccountNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaAwsAccountNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a02758425fb712bd9c7ef025891b66b09a83aa2cd5b188e7e62a27e5ed87e19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270dd72816945c6a73e732408e16d90ddbfbc687eb09e3d74c7bc26c8d62eb5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b074ef1ee901ae5818628bc3305a4e416bcd11c24da9534e6180529dcd27fc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountName]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountName]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountName]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea2e6b3932f9dbf4cd13ebd9edcf5922208c0085fecc311296dbdce579cf95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCompanyName",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaCompanyName:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab2cc74969507f2d9d2d923cde5f9cd9bf77ea4a2c5f9fb65b4dc4716cbcc50)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaCompanyName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaCompanyNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCompanyNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__681ce5916797e65862762f13226449b2d609bc49975a123e48b2f3d62eceab26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaCompanyNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c657747494b13d09f063f91252518be3d710ac827876420c3f4781605b4a6eb3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaCompanyNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021e89220aeed679f527a883e68d309611d6ec63ec2a0a8204f566b2bc1c65ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73809f6b3c4be37e4ad186f3d6c1511533d070baaf54ae2659d6c0a06f941707)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d35b03e2eecbe7aba622bef569950208ac689da64014dca63a44c050c2ab2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCompanyName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCompanyName]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCompanyName]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667a95636e860ae2802fc6e73c7a0d288b550ced154e09751e0ede1e5f9c5c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaCompanyNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCompanyNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a23cdc9a74ff8651b1266e70cece9543caa640c488c14e76789ffea7e3c3810)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f489aa02458c2d01c49b09b67486d9583d00c0ae7fd6f18dc3d17851595f4bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aef79471696ee6848b7fe90083dadb5dfd5e2dc0796a53479700cda231152dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCompanyName]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCompanyName]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCompanyName]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053b18ece107eb329c9757888e4cb3f286086158325e5e5c09853090f1311ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3248a66d82ad3755d784bdb04a476d4c6a1039b7e1b82642d1916f7b36f39e)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34137fde73741c9a84dbbb7fb412e9583952a7b9bd2e4a87b712afa91812c100)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9328ebd7058aaa719810512e76a3f0c104e2e9c9c9ba39a0f6f3ed951386d19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202f3cc06c0e5fd867298bf82704d18f1be233a22087d5057524082d44be5baa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af1ca34c77fda329a81a5d3897b1f48e1d61acad77bb8d4cac0829c9fa7a0683)
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
            type_hints = typing.get_type_hints(_typecheckingstub__522aa65889d3b559fd949b0321bbc9bc25c773fdc838d0c843aec625d10786b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f696a5feee91c6764433d658d4bb5a6bb95e8e8a31ae7463d45edcbacfef3a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b9f2b6327c568681c2b78fc2581c5c5141e3c5605dfd6b5df5f7830019c34a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd8e56da7118c689f6351397625638139c1a95580b24be3939625fe1fd1a3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5b26ab4154e8262a3cfb826e1cff8ea72cda67df85f9dcda8b89060146b285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b62c3edce8db05aeb90fd64a3ab1d59b3066b8fe5e93f8b7fcce026053779fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceSecurityControlId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaComplianceSecurityControlId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16829c07de7ee297804134d47c99451c94002890a638ea3885b5d8d952c5b9e7)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaComplianceSecurityControlId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9865f5a021b5cfb946ea9b3160c663ff95eb306459b6ab2dde583b321b6d1e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2ba0ec6706f7854182e72544805fa278c59ccd622f17a7fd7b0fcdba9e97fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e9d0d7afddf58b850eb43e7e70de788796b21411d2f4a98f4deee8a7d1b54d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abbaa3d2a004137318690055b4191364b72aa3cdec354444edd349ebab6a6101)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa7c935981394b2fb765763893e56bbab94b49fda3715b67391f6d35d7379d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed2349353f219615e80b7d550ff6a961578399e63fd8aa4c993f8b7d0c7d9f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e943347488487d3877ac7c3f772f3437d7228eec33abd2ffdc42b32a47bf60b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f97c0d2e832f5c290fbe9c4d7cf5d76c38f30f6eb0080d6856bd63217c0d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4399de82f471a4a3050b7a874079bc619964c5f3e9ba5238ee0d12565e8b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4b9897587da42d86024771bffeadd960e9bd16e32c5799ec10fd96fe296b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceStatus",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaComplianceStatus:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d949f2a852d8945ff54e770fb22a29728d18c991e9341be6017174ec803b99eb)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaComplianceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaComplianceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c16242ea3430067447a76e75e9b576bd7182dbfbce3e3f300155ac3c1169468d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaComplianceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d70263455d15d0ef9ea814589b0243ebbe3810c7caaaab0d33aaa2944f4428)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaComplianceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31e884f16bfd039e51c40a721bad4f22e0feafae0031411f17600c4dd35eb83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b173dba24bbe51e5381fbd7d522b59d68159fbca6e8a0dbb58d0b5f1e7afd29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb1fa5c84226264d774905a48cb214a3e8e25edcb510fd753f0ccd406a52ef01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceStatus]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceStatus]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceStatus]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4813d2c866c10728ed08486d6bbdb6fb658e2a9ffa7fe00e178b546562e282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaComplianceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaComplianceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71b8772f7ac64de472dab474526dd40b003de23c7d46b4b670134d450f0a5db6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7edb2f57b09cdfa6f646c08159331160943147087fa0e53a70b65713a908d9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0283ae1b73c317a568340942334b02e327e727e0e4128e079c3c76f80cecbec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec2ccdd0e0334c9d58800b9bf237052e4c2a94436121bbd7dd7d67952fdcd6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaConfidence",
    jsii_struct_bases=[],
    name_mapping={"eq": "eq", "gt": "gt", "gte": "gte", "lt": "lt", "lte": "lte"},
)
class SecurityhubAutomationRuleCriteriaConfidence:
    def __init__(
        self,
        *,
        eq: typing.Optional[jsii.Number] = None,
        gt: typing.Optional[jsii.Number] = None,
        gte: typing.Optional[jsii.Number] = None,
        lt: typing.Optional[jsii.Number] = None,
        lte: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param eq: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#eq SecurityhubAutomationRule#eq}.
        :param gt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gt SecurityhubAutomationRule#gt}.
        :param gte: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gte SecurityhubAutomationRule#gte}.
        :param lt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lt SecurityhubAutomationRule#lt}.
        :param lte: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lte SecurityhubAutomationRule#lte}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc903b89cfd5f820461e611b21e45f6537151eb63ee0aaa939c99469a25b3631)
            check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
            check_type(argname="argument gt", value=gt, expected_type=type_hints["gt"])
            check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
            check_type(argname="argument lt", value=lt, expected_type=type_hints["lt"])
            check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if eq is not None:
            self._values["eq"] = eq
        if gt is not None:
            self._values["gt"] = gt
        if gte is not None:
            self._values["gte"] = gte
        if lt is not None:
            self._values["lt"] = lt
        if lte is not None:
            self._values["lte"] = lte

    @builtins.property
    def eq(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#eq SecurityhubAutomationRule#eq}.'''
        result = self._values.get("eq")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gt(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gt SecurityhubAutomationRule#gt}.'''
        result = self._values.get("gt")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gte(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gte SecurityhubAutomationRule#gte}.'''
        result = self._values.get("gte")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lt(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lt SecurityhubAutomationRule#lt}.'''
        result = self._values.get("lt")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lte(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lte SecurityhubAutomationRule#lte}.'''
        result = self._values.get("lte")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaConfidence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaConfidenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaConfidenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a233f5c0eaa005ce78a549095db411ff7a9f2ec32121d45609e04a987bb7bfca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaConfidenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9202ac878ddcae5e82b56658254be83c94abd31679e82a2b24a303816a4d698b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaConfidenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19358c26d270844116cd89679ad87c3e880be16c5a74ff4a2db861ee34795c87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd8324835f94ec376b41f6de3ff866e7578b9e6038cdfdb02cfa8a3787d45e48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__418257d464565113ead1d448f5837113476f86e1b0dec856f3d158c8fe0b7feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaConfidence]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaConfidence]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaConfidence]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b603569d7954cd324af788913730e71f3428aabbcb2e9ba203f97b0dab5866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaConfidenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaConfidenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83998e744e5d39aaa635d5b98e4bd1bac030799752b8e7196b78a411b9040043)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEq")
    def reset_eq(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEq", []))

    @jsii.member(jsii_name="resetGt")
    def reset_gt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGt", []))

    @jsii.member(jsii_name="resetGte")
    def reset_gte(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGte", []))

    @jsii.member(jsii_name="resetLt")
    def reset_lt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLt", []))

    @jsii.member(jsii_name="resetLte")
    def reset_lte(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLte", []))

    @builtins.property
    @jsii.member(jsii_name="eqInput")
    def eq_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "eqInput"))

    @builtins.property
    @jsii.member(jsii_name="gteInput")
    def gte_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gteInput"))

    @builtins.property
    @jsii.member(jsii_name="gtInput")
    def gt_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gtInput"))

    @builtins.property
    @jsii.member(jsii_name="lteInput")
    def lte_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lteInput"))

    @builtins.property
    @jsii.member(jsii_name="ltInput")
    def lt_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ltInput"))

    @builtins.property
    @jsii.member(jsii_name="eq")
    def eq(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eq"))

    @eq.setter
    def eq(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5be94dc3e1ffed2f5362a3b420f4ede6b1e7fcd85a64fc65d541e6c6edd727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eq", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gt")
    def gt(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gt"))

    @gt.setter
    def gt(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636795c73a3b014d6a8fd1c423793e7ead1ec761c833f07a31ad18134755c968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gte")
    def gte(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gte"))

    @gte.setter
    def gte(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b27a13cfc3b765d97132ae713a06a8e5216ebf72beb8c974448b170c2190082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gte", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lt")
    def lt(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lt"))

    @lt.setter
    def lt(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2dbf4c20d5bc89b4738c7137ebd62439d1487612810ecd2bade659d74f52e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lte")
    def lte(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lte"))

    @lte.setter
    def lte(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33ea92849dc994070636606d74765bcac2d498cccb4c91c697ce2c044942552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lte", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaConfidence]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaConfidence]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaConfidence]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5551cab8e6a967989dbd7c20b663a280f33fb7acb7f6a094185694781725105f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCreatedAt",
    jsii_struct_bases=[],
    name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
)
class SecurityhubAutomationRuleCriteriaCreatedAt:
    def __init__(
        self,
        *,
        date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaCreatedAtDateRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_range: date_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703ea6cf93aa6e854f58425cdc9012db4e0dc0d1796d13ced3494c1302f06a26)
            check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_range is not None:
            self._values["date_range"] = date_range
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def date_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCreatedAtDateRange"]]]:
        '''date_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        '''
        result = self._values.get("date_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaCreatedAtDateRange"]]], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.'''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.'''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaCreatedAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCreatedAtDateRange",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaCreatedAtDateRange:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f60f050a679b2f919321afde54cccd9fe6efe750159f2f4a448eb834e90b706)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaCreatedAtDateRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaCreatedAtDateRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCreatedAtDateRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f888d31a4d11f55e081a9e6a26fd2d166a9da53619fd112baa56a23b7265549)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaCreatedAtDateRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc7e2ca9af72466d4af287f2f3b068300d3d315c4d8486c01e00519af6630ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaCreatedAtDateRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538447f2b4622220cd794665d7942a2fa8fc51f77765bcfd4affd8241764e692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b2483b1f8b03671151b1a0da26a7e300d1a0574f7dce37acd2031c10f1b8e70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5341162baccccce2dc4038b3e437f19319e3eecb7a3cb97604f640052e32748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2cbb66fd54f185bea6d93c4c1a10c8559535c9e0122bdd59173291e2805b501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaCreatedAtDateRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCreatedAtDateRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3182d49a7eff79ba8bac8898c365aa948fb6d2317d9514bc2e171fdf1d838cf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f9a30f82acbae59face8e2cf9b4a856b9771ec6956ce3972636a0b689a1ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e1d70d2e74fabd47481c36c30847e3dfe29cf4732698fa83b1cfefcf6fc584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAtDateRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAtDateRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3296df6f4a53121d6bbaf8a19c9699c46b7b5b3b47333b7d4f1c61ae6d42fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaCreatedAtList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCreatedAtList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d84c300c1511a2d6aa32c0d105d04c4fd149040393d12954055591bfcc060ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaCreatedAtOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca631aec72b5931d40ce5bffd9f0ad8e98e7927883bb9c0cc46eaef39aec9354)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaCreatedAtOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa6c419d084be76e779229bb2f6503543785705918eb318012938c313312a0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3a1759828c5074bfe96d9434ae7da3cc3100d142782bb37b9b93246e0a53ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b464331b895f69a56b3f9ed4dbd529cef727adcb6d685b7f1e6595ae789d10d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1d28a38ae93e5af38136e9fc46fc086cfcc934efcdd01d7d1ee53675399f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaCreatedAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCreatedAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21be4d01218a09ca64d1da902685caabe720181607066b81c1ba94674bbe3de1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateRange")
    def put_date_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCreatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a04fe93a7f58de7086fec7eace3c57325a27ef2da3a5f7d8694714957581f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateRange", [value]))

    @jsii.member(jsii_name="resetDateRange")
    def reset_date_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRange", []))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="dateRange")
    def date_range(self) -> SecurityhubAutomationRuleCriteriaCreatedAtDateRangeList:
        return typing.cast(SecurityhubAutomationRuleCriteriaCreatedAtDateRangeList, jsii.get(self, "dateRange"))

    @builtins.property
    @jsii.member(jsii_name="dateRangeInput")
    def date_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]], jsii.get(self, "dateRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f528441dd42588b3cf67b993989cc062e50b9a9b06b830481adade3e7cfde296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181d9b9505153d1dac20edb240f54e889d1dd3931811522b2ee3f1b05090a55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840e7c48bb61c3d75f53abeab90a92ad44fdf493e3a9fb916f968b4f8ab51ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCriticality",
    jsii_struct_bases=[],
    name_mapping={"eq": "eq", "gt": "gt", "gte": "gte", "lt": "lt", "lte": "lte"},
)
class SecurityhubAutomationRuleCriteriaCriticality:
    def __init__(
        self,
        *,
        eq: typing.Optional[jsii.Number] = None,
        gt: typing.Optional[jsii.Number] = None,
        gte: typing.Optional[jsii.Number] = None,
        lt: typing.Optional[jsii.Number] = None,
        lte: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param eq: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#eq SecurityhubAutomationRule#eq}.
        :param gt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gt SecurityhubAutomationRule#gt}.
        :param gte: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gte SecurityhubAutomationRule#gte}.
        :param lt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lt SecurityhubAutomationRule#lt}.
        :param lte: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lte SecurityhubAutomationRule#lte}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c667e12f4968ffb040b1d2c938319b00112d21f2974d19ebc1abe71e38584bd)
            check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
            check_type(argname="argument gt", value=gt, expected_type=type_hints["gt"])
            check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
            check_type(argname="argument lt", value=lt, expected_type=type_hints["lt"])
            check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if eq is not None:
            self._values["eq"] = eq
        if gt is not None:
            self._values["gt"] = gt
        if gte is not None:
            self._values["gte"] = gte
        if lt is not None:
            self._values["lt"] = lt
        if lte is not None:
            self._values["lte"] = lte

    @builtins.property
    def eq(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#eq SecurityhubAutomationRule#eq}.'''
        result = self._values.get("eq")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gt(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gt SecurityhubAutomationRule#gt}.'''
        result = self._values.get("gt")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gte(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#gte SecurityhubAutomationRule#gte}.'''
        result = self._values.get("gte")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lt(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lt SecurityhubAutomationRule#lt}.'''
        result = self._values.get("lt")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lte(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#lte SecurityhubAutomationRule#lte}.'''
        result = self._values.get("lte")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaCriticality(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaCriticalityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCriticalityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f373861920983adf7042c32d907d980d433ac5492d3394fa8a8c77d144443d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaCriticalityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b97b9b7ec8067ee38db9c18df2dc95b275ff1e6e170176c8a155ed5a7fc3a1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaCriticalityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b60ab02165c45daa485fbbeec4f4438fdd281515b128165056ba45402bffaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a71bf3d5f5d6d89346e2c408b42d10d41678780d0ac96c8b32266b1800c50d63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af8aabbe41978a5b035d20a1c1a5b11667d4f38786b5e930ac26ae98154be0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCriticality]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCriticality]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCriticality]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945ed3b33595dc7b0f6698a788d7ec51ca89be07826b80d5a2896e66306261de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaCriticalityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaCriticalityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__482e71135449136200c1267b9a463513986e1e1a19e4ce88b17812813abefc8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEq")
    def reset_eq(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEq", []))

    @jsii.member(jsii_name="resetGt")
    def reset_gt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGt", []))

    @jsii.member(jsii_name="resetGte")
    def reset_gte(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGte", []))

    @jsii.member(jsii_name="resetLt")
    def reset_lt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLt", []))

    @jsii.member(jsii_name="resetLte")
    def reset_lte(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLte", []))

    @builtins.property
    @jsii.member(jsii_name="eqInput")
    def eq_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "eqInput"))

    @builtins.property
    @jsii.member(jsii_name="gteInput")
    def gte_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gteInput"))

    @builtins.property
    @jsii.member(jsii_name="gtInput")
    def gt_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gtInput"))

    @builtins.property
    @jsii.member(jsii_name="lteInput")
    def lte_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lteInput"))

    @builtins.property
    @jsii.member(jsii_name="ltInput")
    def lt_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ltInput"))

    @builtins.property
    @jsii.member(jsii_name="eq")
    def eq(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eq"))

    @eq.setter
    def eq(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cc7a72e7884937a76c28efde1a791912ec44e2c4afb9116f2e1a870583b9ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eq", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gt")
    def gt(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gt"))

    @gt.setter
    def gt(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30eadbc5cf896f104eb2a67892b19393561e1c73181b7f8b5e77d71fbacd1250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gte")
    def gte(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gte"))

    @gte.setter
    def gte(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e7cec4d40a4b347334f7f7d4f36863946351fecd7bbcda2f912e1171508f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gte", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lt")
    def lt(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lt"))

    @lt.setter
    def lt(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ca2a99f703a62a40445697f14cef3abcc074c42d6705f5d2eb018aec7e5497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lte")
    def lte(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lte"))

    @lte.setter
    def lte(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f6ab918a669902cab257f221c9a40790626ef946f5fba7a0fea8885fd6186d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lte", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCriticality]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCriticality]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCriticality]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b713b1850504152ec9651f7e7d666bdf66979e73701d43c36db38666259302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaDescription",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaDescription:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1956be046d51069cf5ac014a4dc4949e3b2b1600e5a3e13cc5e479f9cfbc0f6e)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaDescriptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaDescriptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38cabd1d1242133f1a4005a85f27620a0ff1e95b11b842f3ee6eb5fff2105f31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaDescriptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bceb89af2e6cb80cbd4908e4bbc9986ca14b0624275661205b5c065ca6cbef9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaDescriptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375605ab9a15d6907600db1d80a28b466b3637de0d30719e514439994baa4891)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdb61833e9ef470da7ba653f7eb0b22833b193bd0f2b988a3aa125d05bcb1e7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b61434130275de0e5ff328db1d36914a414f35e03e5145bee2d903f5b9a781f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaDescription]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaDescription]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaDescription]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf5519a90eebd7edd2b28446865084d4668afdd50f5103062cf8789272bbfdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5947be57611479938098ec29065506d51fa9ad453efbfa47e1db64365ab265d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed153a4dea9efedf69ca35ec07e9b1c44b6eb08168a9794131db60a3ee407ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e691092b0e62f02d7235241f91524ff2e908fb5fadad3c3ea79065e9bfe9828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaDescription]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaDescription]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaDescription]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678b3a495bd1f40c57f43d4cf72cb1444466756d3a5b109efa136e743f3fd152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaFirstObservedAt",
    jsii_struct_bases=[],
    name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
)
class SecurityhubAutomationRuleCriteriaFirstObservedAt:
    def __init__(
        self,
        *,
        date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_range: date_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3aa3b5a8ee8055c62a2670ac031a92a03f00a98d3ec3d06ce185bc315bc8db)
            check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_range is not None:
            self._values["date_range"] = date_range
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def date_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange"]]]:
        '''date_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        '''
        result = self._values.get("date_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange"]]], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.'''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.'''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaFirstObservedAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9fdecdcb309e34c6df979727ab5c19b4fea101c6128a462f89e57dced00161)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ccd6b1e66875daab17626741641182118136f7e010b5f2059e6f763d396a60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421e425d36b9d9b6ecb88b186ca229d7edfcaf16140aae6cf5b23d0d48b3ae2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430943f815ec88efb7cf5601b600f0c9b43edd44e9b9982c8ab8bfda8b5dab23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fb621cc0cb98ff381faa7b569ac217d1284f0129b0dfc333a1c2fdfcf02b60a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a81a3d37d4cf368ac79caec0a52838ee06342662ec7c7dd5d2e8826504cd028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f2824ab6d67b86fcc3c47b9ad56861c9d02cb4ada411c97cc4632d6b31870c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9964f54ab4c1235c4f6fa1ae38a4a5e3d371fff0a54e5b86a508a074b7bdef55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a346aa556a487ee5ca4238b4ae16634cce862ce8ec591b8d8659d6ba2689da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12a62bb42fdc6f2f9bfcbc76177853e079ce3881991e9e040974ffbab79fd64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a08cc06f9751400bcacf9f8e6d039860d2256696ba965607817fb2b629a028e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaFirstObservedAtList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaFirstObservedAtList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5140803febf95b44b87c556e97ac6831ba0dbea2cb92d43cdccf7b9a70b89b2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaFirstObservedAtOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156b4f12013d29ee87918b3992516a08815fb7eb47be2ccbb37cb90a8af961ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaFirstObservedAtOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b158638986090ac6e691007a773f09bfc7cd2d43e7d7fc4658d47b9d15acf99f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__514560fcaf9f567bdcdd56337e4d0c842d98901dd562ae4a743d17d6e33be9cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__720d93821ef575fdf411f339eb81ba1881a79f2e2ed213c100749666473a0fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5efc0f0d723eaadfc0223ba1ca15934614447f3b15759e280f9e8ea5debd2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaFirstObservedAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaFirstObservedAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca6a17f98370716d07f919f28cbf67f9846c58408acc65e5d0aa370f18cc45b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateRange")
    def put_date_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2bdea5694d626cfbe56bc1f4ff09bdfa751d9d72b223245fb9571dbd3c42ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateRange", [value]))

    @jsii.member(jsii_name="resetDateRange")
    def reset_date_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRange", []))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="dateRange")
    def date_range(
        self,
    ) -> SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeList:
        return typing.cast(SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeList, jsii.get(self, "dateRange"))

    @builtins.property
    @jsii.member(jsii_name="dateRangeInput")
    def date_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]], jsii.get(self, "dateRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2e6f57110df0febc5df02f58e05ff15edceab685879651a19ee53f35199cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451c7589bb40d3624fd4b3406185980c56d83118392f83e49c0a2db1259fcbcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624dc6037b0483606bfebd2717ae7067ff084b7acb8cb3c08a088d6516cc484a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaGeneratorId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaGeneratorId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f3ca32c96f3e0d6f171cec0679bd8df7b739cc3d78011c34714bf3e81a53bc)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaGeneratorId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaGeneratorIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaGeneratorIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd11ad6d2d9862e951cda0bf0572e90f27ce2e50edfc62a7067e31622447ac6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaGeneratorIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888dd2bf54447d4fffed35f9f1e3f86272a60ce939c4766037a9e0697ef67768)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaGeneratorIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96180b701f7717c22e6ef735b63d772c3ab0e6e25de8b28af903f03799005ce1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc6ece8cedee653a6ac1e1198deb379010d22429e42d39590d9ef49aeabd0a98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3be894ce610daa4a4c5b9de6afc351256c67ad20f11851e3b588b53e27b7584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaGeneratorId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaGeneratorId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaGeneratorId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe2bfd17d37fbe3e61e31f1dd757e2618f8eef452897e774e1b10c024add975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaGeneratorIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaGeneratorIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfc581ff4c31fd41299a210362236482b894006a504bf1dcb0a445d5e06f45cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8752c082411499a127abb4229d80feda48fa10ed5d18bc657abf760e65df76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5dfb2042f3b923a38a78011faf27fcd6f453f61ecdb2af7033e01145dd65c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaGeneratorId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaGeneratorId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaGeneratorId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08ea4efaea1d81bc3fc2af1b0a912082a44d1eb1cc9c80000073bed33a71598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc34ccb0aac97cc5e01129361c5cb3adf5eaaa6543017515fe609b37543476a)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43019b5461e4ad3aa3f33195e5ed37bc7066003ee7500d220cf964f47de0df8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17aadf6f8b2abc4c5ced07e21a09b3c43a9129edbf54e9955578d61dcec68c1b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a9aace32ed9ff7c7c4db28670cf9fe8314a290c698ae4a6d6080928727c78c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed0fd9366fee2bf06fe6a874fe707e4953e1df51301d29a65d0ed056b9e142f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5665fa0fd6193328b2271fff05e2cff246a35fb1f35ff023cd70cce3fb40408e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a76e24d4de114c685e9bf042f44cb52be6701fabf534147b1cdb424fe686fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c00ec62b5ac98d87da3b87a93edb48acfae4023ec0014f7ebf2fff68e0ef9359)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac437a79713b671899ce861ca06585f783b2aad8d4375bcefe9079f242b072f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ed7d03f94be8249f761f36464b1dd05e2beabd98e0426ac9e4533409c66b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765b39934308569b12c490b0e5d44ec28dc1898f80a9826d0969ade7a81b249a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaLastObservedAt",
    jsii_struct_bases=[],
    name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
)
class SecurityhubAutomationRuleCriteriaLastObservedAt:
    def __init__(
        self,
        *,
        date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaLastObservedAtDateRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_range: date_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95eb2ce9e8caab421998cfd525235c724667c0b14e4680c2cc4acd929f6ecd89)
            check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_range is not None:
            self._values["date_range"] = date_range
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def date_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaLastObservedAtDateRange"]]]:
        '''date_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        '''
        result = self._values.get("date_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaLastObservedAtDateRange"]]], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.'''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.'''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaLastObservedAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaLastObservedAtDateRange",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaLastObservedAtDateRange:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb196058109f51c9f3bd87a847f3dd480f1715e456cbcc4cd6308dfb308b7e3b)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaLastObservedAtDateRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48944f3e4ef1ee4254e2fb723caa80d53f1fa55704076369c427e9e204caa790)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4c5403fb014eb63f95400429811c2b8b7562be8714ba4e34589946a6591e1d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac23d645b7cf869f22206a41f8d5261e740b11dfe69f3678f51eb27dc402173)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f94ad7dbf8bf30c7d61a7a7f1fc53e45959b904c34cff73eb84ef0ae445e24a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6c674410d694de2f52889f73f1b98ba0ddf0ab4b4c510991ceb308303741e4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8556af9127e0f846853fba8dfc2b726cb73b21ee3864873dbfce3972f088ee30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28f0a8a19e074124136bc70d8cb0c897effc81ea4d8acdea16f5ba3085142819)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433fdcb91240b150ff243cec79aeadada0345496e9a814c715b603a83efb9f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa92eee85ba52b1ac4cbe84f9572304d3e867749c14bb7559639fd7a54d5a862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2290cfa461920b87bab8456cb78ba0cef6aa17cf2163fe3c5a7782051220a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaLastObservedAtList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaLastObservedAtList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__464a7cd324114d23e7f56641011c7f789470f75299bdf3e9c2b15161c6d9f7f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaLastObservedAtOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7217eeb0b1e52db6655014af0e00b10b3e8f51da7828c4fb3cd1dabb02689dbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaLastObservedAtOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbab3a16d22ad7f1735af55511a4e60611d1799662222f7df74628f28b257ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45e3cc29bbe4b5c46a2ff8e84e51cf45deb5a34f950395226d618273ea59c7af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd4d7002bb57a073005840dbe228241f7ad16269b6b5ed4114d2ec69a27a421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb93cb0c024ab53dd984e6aa193e1bc45e7a2957413031535f195b128c1bc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaLastObservedAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaLastObservedAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__257cc60f312d3e09dffdcc76f41280c52220a257a0233c2fa9c33d9cdb5c5751)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateRange")
    def put_date_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a4c75e9a25d9f19191b313b756ad2cf3a89ba1164b33da2910f0db83a33dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateRange", [value]))

    @jsii.member(jsii_name="resetDateRange")
    def reset_date_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRange", []))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="dateRange")
    def date_range(
        self,
    ) -> SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeList:
        return typing.cast(SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeList, jsii.get(self, "dateRange"))

    @builtins.property
    @jsii.member(jsii_name="dateRangeInput")
    def date_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]], jsii.get(self, "dateRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22a8d82cbb72b13c29b762e00888222e1a1c00acc83b9f7627a79815f67342f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b83358332017696f40183aa57cc1f94bac3d13b59dd2389612ddb238e8a7b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c780b184f32dc25a6d9972e7edd90cb33cb8487fef7ac6bcc1c39fb927ec6afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04dbe44abf4e9f68fa1d7a54e75d40fd3d450f2df0c98c01cc958b2b1d7f1121)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fe9f04a07f69a4c750825798a01a5ec73b6014d877602068f584f4319be314)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7da83f4d02da8f3e8e2c71f5c6829b5f32fa5a49e4123380525f8de1a01f25f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c909344cc775ea62bdb7432def7ea2901ea0f070728cc576a09829cc4dffb32f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c473095a2ef711b2cee708bc37a3900f1824acc7a1c00ce5bd8fcfdd5f985095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d67c1c5c669afc1684f460d1d9e67fd6681000dcdc384e7385d1af4068a103f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteText",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaNoteText:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927f70870dea57c12445ddc83d040ba6ca41a0eddecbbd11ea0f99d037a00c9a)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaNoteText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaNoteTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f72f4879be2ef4800e6997c7aa2cec9e3a644147ed36e885d41a0f8921443f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaNoteTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdcb2fd4fb2440a84d4b14dfd0c71aea537591edee36d5e5e203246f8c064b3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaNoteTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c589c0d7cb5f78a420ae078147cc86c849f869793cf6d14b299c5107e9977b94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__460518d55f5adb6b292dfd98e4e6908abe3a9dc651c68a1fd0c9ceddbb698003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf7a0f4c3c811943131c9d2045097ac2ba663b8b26bb1f24eba01b522043ecc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteText]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteText]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18071a7d1d82a59421b55eb2ef73e91134d7718d8363a37477c3d0f7ced060a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaNoteTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1236c92510e391a4235076e8ca39a24061cc2d114284383abb456e5201b16f63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cd468f8bae3dfac62dcd116fa6b77ff657b7acb30e2e0498f21e8a439f51b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8163c274c3acbe23dfcc2c7a3eac10996ed51be451d9cfe99b4eb62c1e4c025d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteText]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteText]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteText]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4824b0857d665c4d361947268e98b24e3bae5453dfbb3ee7dbde56ce1b867b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedAt",
    jsii_struct_bases=[],
    name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
)
class SecurityhubAutomationRuleCriteriaNoteUpdatedAt:
    def __init__(
        self,
        *,
        date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_range: date_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbe5362796567116360185213fade95a858a3359d4345d29efe7354de2071c3)
            check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_range is not None:
            self._values["date_range"] = date_range
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def date_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange"]]]:
        '''date_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        '''
        result = self._values.get("date_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange"]]], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.'''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.'''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaNoteUpdatedAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d28c5e121e0342a10fd4da94a11ea3c59df3a3b3b3fd7dcd19e7f7f7b5a3b81)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cdf2de0465fa48e908837627cfbdcee737e8a2fdc8296dcf1c43b7db0e9192f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c1b1648e38de55a3f239a8669b9781d565bd4c147cb87dcc5ccb0ffca8105b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d356a0aca029715d701e55e1702004242bb31da6c538b9709675b8d157da5454)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e139ae8fb4fde83a254dd0eb7d23d694bd0152a43adbe96715b4b0e5b0b76cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed6be151781c90f4e3c402c7969c6f49165f33b9910a25e2ed78a58a9c3286d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f734301fd52581ab69e2ceb7e7e380f55d56fcab42cd68aedffbc4b532c531d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba2dcb7f69bbe92e41ce9c64ac15dab87654bdd04e35140052959e423d8a41d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ade993a0aedad3baa53584bb6832453f04b4624e737b4695e02c451e6038cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adce83ff873b7b3140d61d366bdb3bcef9347eb12f64b17b531a0ac794c4d727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ef09c469e849510814342d6fa1c931ff603fc726850041ad754c508758b743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaNoteUpdatedAtList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedAtList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__406dd73df6e6c53d7471b96fe4e1f8212ea0ae223c45247e5967e03f2c19ce17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaNoteUpdatedAtOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7809cd5125561f0fd8e5380535479e7f641a5f36a22e66dca02962e0e991c325)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaNoteUpdatedAtOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd742bc2c9c12b6f1a911685036227ee751264badbc32c10122cccaecb2a356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec655f242abb0a858ed4bc4cb28f72380d234a03775d47a0efd172e033863de7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__849073bdffbfd70511766418df3e01429b241899a9e25815d0eeb0006b3eb7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb5e553e1dc3eb84ff127e0caad7320561678e4665b06e2b579d4c41559d99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaNoteUpdatedAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d77db68ff1507adc9f5ca3b3a9334a906473ccf6cebc8763d6434f48f3ecdf3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateRange")
    def put_date_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83333b1700168dfb43f1723b071cd23296c41e3ecd8330555831587063d4408e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateRange", [value]))

    @jsii.member(jsii_name="resetDateRange")
    def reset_date_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRange", []))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="dateRange")
    def date_range(self) -> SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeList:
        return typing.cast(SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeList, jsii.get(self, "dateRange"))

    @builtins.property
    @jsii.member(jsii_name="dateRangeInput")
    def date_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]], jsii.get(self, "dateRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b3da3c1bb8b1934e80d78c73e64ad894c0fdee0809a93811b5cb4f2034c315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e23e057ee17eb3869e005ebf830b5a8b50b34f026601bb7774a9847af7f02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db52cf48c44aeefbaba0f635d085b6e55b35be1217dce6edfe29a99ea3cd967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedBy",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaNoteUpdatedBy:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c392b7b9fcb0120d670e5bb2d426c279a7af4b28c3ff2751ca3b44129e10bb)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaNoteUpdatedBy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaNoteUpdatedByList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedByList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fb6e1663200e7bb7d2a060b002230b4ff3daca69693947414c048e84536c10d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaNoteUpdatedByOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298c6e45f34aa79cf1970b37358f467ff22bbe462d287e8d91d1c817fecb8066)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaNoteUpdatedByOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea4c9175a80c6d32aa9de92795470fdb1c858d34cb881f9e965aa75b5398ecd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef3020a0719415a97420453b8c8439beb740ed3756b0edc40f39a7c1742149a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0578ecfc58b2ea5e80758f676d77b69a6bd2cd3c122f9ff8bbee1b48ad607175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fd0c54591b83647206047d41c14739e40559b692076cd7cb020e7b8eee5020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaNoteUpdatedByOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaNoteUpdatedByOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef2ff72f4a853706afce722505ff01e3c8ef7f4d5800d6516775e317d365800)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df909ea6863491fb350884b5e51ae3b270991754363b57a4cf3039f04f7490ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5e5852d831f99a47363aaffbc0ecf316a9226a173480ab3603ce5a208bf8c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedBy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedBy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b50a66ba71df9d42cfab593b3699d975eab7c4f2e0565ccc00b5d3f3842be14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbdbd03ef1f63bc8871bb2666c7b2bbafc050d90b993845a7721958b2fc51577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAwsAccountId")
    def put_aws_account_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaAwsAccountId, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60fab7752add9517459d40173f501ced49c775ed74ef9fb9d19835ef7c24fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAwsAccountId", [value]))

    @jsii.member(jsii_name="putAwsAccountName")
    def put_aws_account_name(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaAwsAccountName, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87911ce0c9ad29e4bdf018e6e6879cb412082c34becbcf3839dc3ec8798190d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAwsAccountName", [value]))

    @jsii.member(jsii_name="putCompanyName")
    def put_company_name(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCompanyName, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbbaf50e08a9f573548f764f0be37cbf1fe7cd9349ea60b26e2c09d5264baa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCompanyName", [value]))

    @jsii.member(jsii_name="putComplianceAssociatedStandardsId")
    def put_compliance_associated_standards_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f29f958f41be77c2a956b13d1a0272b4319b38d441f8821ebd1514d0a578fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComplianceAssociatedStandardsId", [value]))

    @jsii.member(jsii_name="putComplianceSecurityControlId")
    def put_compliance_security_control_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d07fa0f98eb9c66a74a867df6b50c7134b966ad05a139de33402f00e281fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComplianceSecurityControlId", [value]))

    @jsii.member(jsii_name="putComplianceStatus")
    def put_compliance_status(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceStatus, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb71fe283c549a4b3810a1209148ae1c6a9085ab41b2e56f22e7ce4500453be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComplianceStatus", [value]))

    @jsii.member(jsii_name="putConfidence")
    def put_confidence(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaConfidence, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acebe9da1879ecba5fa61e3e78ffb65a85b5aa83770f85addaec7b7fc921cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfidence", [value]))

    @jsii.member(jsii_name="putCreatedAt")
    def put_created_at(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCreatedAt, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2f70319edf5e05f779691205ba64b32f81bf847fe58a8c777a1d78993a475c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCreatedAt", [value]))

    @jsii.member(jsii_name="putCriticality")
    def put_criticality(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCriticality, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb7d31867574f5fe4f6656905b640a084a1f62b197a96ed9ceefdb1ac43d8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCriticality", [value]))

    @jsii.member(jsii_name="putDescription")
    def put_description(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaDescription, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6bf2c83ceeec5a992b1d5b5cf378e164454388484784608ae2b108a9ba506f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDescription", [value]))

    @jsii.member(jsii_name="putFirstObservedAt")
    def put_first_observed_at(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaFirstObservedAt, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb07696f4b5817f715c3be7097ef4ac51ffc169048cbe70e2e778ec0a71455ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFirstObservedAt", [value]))

    @jsii.member(jsii_name="putGeneratorId")
    def put_generator_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaGeneratorId, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987762528d8ca5783e7662fde8da0c8ce301cdac3208de988518b9323e4c94af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeneratorId", [value]))

    @jsii.member(jsii_name="putId")
    def put_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaId, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c0a4c764d63deebaf60becb728648f79e937cb65f3bec30b10c33bc351681d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putId", [value]))

    @jsii.member(jsii_name="putLastObservedAt")
    def put_last_observed_at(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaLastObservedAt, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bd7e2eb14aacde8a08516ea1735aa4284144c287f0afb9c2cdb8a1fe73535a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLastObservedAt", [value]))

    @jsii.member(jsii_name="putNoteText")
    def put_note_text(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteText, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501547fd9fb39fcc6f20c70d849d198ae24195bb027b173455df5da039b22e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNoteText", [value]))

    @jsii.member(jsii_name="putNoteUpdatedAt")
    def put_note_updated_at(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedAt, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1495266092da51b70b587f9f0b3033b609694f1e13ae0067d7552569b0f29ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNoteUpdatedAt", [value]))

    @jsii.member(jsii_name="putNoteUpdatedBy")
    def put_note_updated_by(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedBy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bded19b4fea44623340003d54acd0a1aeeca520a38626ab8925eacb6ccaa4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNoteUpdatedBy", [value]))

    @jsii.member(jsii_name="putProductArn")
    def put_product_arn(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaProductArn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adab5a710b8741d73978010ffdd9a57166d75500f8ff6d0bb27a368560c9594d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProductArn", [value]))

    @jsii.member(jsii_name="putProductName")
    def put_product_name(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaProductName", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e874f66b50c1b3d78723721207780e4134b1ca10db2df0dba90835dc022e3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProductName", [value]))

    @jsii.member(jsii_name="putRecordState")
    def put_record_state(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaRecordState", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d20bd4c75f3197dacb681db62057a59eed89c92b4d86167a927fc1e30663908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecordState", [value]))

    @jsii.member(jsii_name="putRelatedFindingsId")
    def put_related_findings_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaRelatedFindingsId", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1714574da56f87e00d2539943224fbb302fd31448e07e8ba3b8c709e157954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRelatedFindingsId", [value]))

    @jsii.member(jsii_name="putRelatedFindingsProductArn")
    def put_related_findings_product_arn(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00205b99ff8c842173442c9dd80a19ecf878d07755cf1e7d5f28eb740ceaa17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRelatedFindingsProductArn", [value]))

    @jsii.member(jsii_name="putResourceApplicationArn")
    def put_resource_application_arn(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceApplicationArn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146fd7eb84be80c7706eff64190b4f923e6b6578777737b6c89b42d950d33b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceApplicationArn", [value]))

    @jsii.member(jsii_name="putResourceApplicationName")
    def put_resource_application_name(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceApplicationName", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e316e678e1249b4fb778293de3722c6cd49f84ab3a0ed35bc66b15092ca8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceApplicationName", [value]))

    @jsii.member(jsii_name="putResourceDetailsOther")
    def put_resource_details_other(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceDetailsOther", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5388226fd4531fec6cf87c5d1d66bfe223744960ee8797cb25b4df7798239e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceDetailsOther", [value]))

    @jsii.member(jsii_name="putResourceId")
    def put_resource_id(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceId", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b963cbb721d2f3d8edbb87f76490f1ae67c9a88704c98a459c2fb7a69956d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceId", [value]))

    @jsii.member(jsii_name="putResourcePartition")
    def put_resource_partition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourcePartition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f333f4718094d8d9eed7e1bc7269e0146a0e240ddeaf8713e0e7f71e96b3a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourcePartition", [value]))

    @jsii.member(jsii_name="putResourceRegion")
    def put_resource_region(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceRegion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470fa56287cf1d5574f14443ee49ccbe30726681eb173c911d31b0010f97459c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceRegion", [value]))

    @jsii.member(jsii_name="putResourceTags")
    def put_resource_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4563b56d4ecc95ba0da6ef69daa4b4b8b0fc968804d9aa4df8e48c0937be4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceTags", [value]))

    @jsii.member(jsii_name="putResourceType")
    def put_resource_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaResourceType", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198de3d2a99a76dc994c113c82f9c31b4ac6aba801e990f5fd6515e86a0662ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceType", [value]))

    @jsii.member(jsii_name="putSeverityLabel")
    def put_severity_label(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaSeverityLabel", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4307d798b7dbc329ca731411e934967986a00eb88b113521b49436f06313e53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeverityLabel", [value]))

    @jsii.member(jsii_name="putSourceUrl")
    def put_source_url(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaSourceUrl", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8d625fff5944387f397c19b69e934a5c21828dfd146370e4ba5684f8998c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSourceUrl", [value]))

    @jsii.member(jsii_name="putTitle")
    def put_title(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaTitle", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae2d723184889ee3e9ec8d29c082121c1c82eff7153d9213d938b68319d7720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTitle", [value]))

    @jsii.member(jsii_name="putType")
    def put_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaType", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a715e893e8a00c8eddd51b6ad92f917d4f99dfb2ec25247eccb5864a92db24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putType", [value]))

    @jsii.member(jsii_name="putUpdatedAt")
    def put_updated_at(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaUpdatedAt", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9900d08a032f8f8da1f1f0545ef55cabee7563b49e8f698c5fadb6c62699f686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpdatedAt", [value]))

    @jsii.member(jsii_name="putUserDefinedFields")
    def put_user_defined_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125b8b91ffa5993b1442f7de633bc3a5f4a662b7559ead61dff4c82bc0b528f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserDefinedFields", [value]))

    @jsii.member(jsii_name="putVerificationState")
    def put_verification_state(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaVerificationState", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a34365832328ce98a0b3c970697ba6d8d0fdfa56281339d0d7bc70a0ad28e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVerificationState", [value]))

    @jsii.member(jsii_name="putWorkflowStatus")
    def put_workflow_status(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaWorkflowStatus", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f114fafd25aa2668142af20267fbbacc6ee5f5591ab8e17ab04188c159e308fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWorkflowStatus", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetAwsAccountName")
    def reset_aws_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountName", []))

    @jsii.member(jsii_name="resetCompanyName")
    def reset_company_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompanyName", []))

    @jsii.member(jsii_name="resetComplianceAssociatedStandardsId")
    def reset_compliance_associated_standards_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceAssociatedStandardsId", []))

    @jsii.member(jsii_name="resetComplianceSecurityControlId")
    def reset_compliance_security_control_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceSecurityControlId", []))

    @jsii.member(jsii_name="resetComplianceStatus")
    def reset_compliance_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceStatus", []))

    @jsii.member(jsii_name="resetConfidence")
    def reset_confidence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidence", []))

    @jsii.member(jsii_name="resetCreatedAt")
    def reset_created_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAt", []))

    @jsii.member(jsii_name="resetCriticality")
    def reset_criticality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriticality", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFirstObservedAt")
    def reset_first_observed_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstObservedAt", []))

    @jsii.member(jsii_name="resetGeneratorId")
    def reset_generator_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneratorId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLastObservedAt")
    def reset_last_observed_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastObservedAt", []))

    @jsii.member(jsii_name="resetNoteText")
    def reset_note_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoteText", []))

    @jsii.member(jsii_name="resetNoteUpdatedAt")
    def reset_note_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoteUpdatedAt", []))

    @jsii.member(jsii_name="resetNoteUpdatedBy")
    def reset_note_updated_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoteUpdatedBy", []))

    @jsii.member(jsii_name="resetProductArn")
    def reset_product_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductArn", []))

    @jsii.member(jsii_name="resetProductName")
    def reset_product_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductName", []))

    @jsii.member(jsii_name="resetRecordState")
    def reset_record_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordState", []))

    @jsii.member(jsii_name="resetRelatedFindingsId")
    def reset_related_findings_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedFindingsId", []))

    @jsii.member(jsii_name="resetRelatedFindingsProductArn")
    def reset_related_findings_product_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedFindingsProductArn", []))

    @jsii.member(jsii_name="resetResourceApplicationArn")
    def reset_resource_application_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceApplicationArn", []))

    @jsii.member(jsii_name="resetResourceApplicationName")
    def reset_resource_application_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceApplicationName", []))

    @jsii.member(jsii_name="resetResourceDetailsOther")
    def reset_resource_details_other(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceDetailsOther", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourcePartition")
    def reset_resource_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePartition", []))

    @jsii.member(jsii_name="resetResourceRegion")
    def reset_resource_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceRegion", []))

    @jsii.member(jsii_name="resetResourceTags")
    def reset_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTags", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetSeverityLabel")
    def reset_severity_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverityLabel", []))

    @jsii.member(jsii_name="resetSourceUrl")
    def reset_source_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceUrl", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUpdatedAt")
    def reset_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAt", []))

    @jsii.member(jsii_name="resetUserDefinedFields")
    def reset_user_defined_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedFields", []))

    @jsii.member(jsii_name="resetVerificationState")
    def reset_verification_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationState", []))

    @jsii.member(jsii_name="resetWorkflowStatus")
    def reset_workflow_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkflowStatus", []))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> SecurityhubAutomationRuleCriteriaAwsAccountIdList:
        return typing.cast(SecurityhubAutomationRuleCriteriaAwsAccountIdList, jsii.get(self, "awsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountName")
    def aws_account_name(self) -> SecurityhubAutomationRuleCriteriaAwsAccountNameList:
        return typing.cast(SecurityhubAutomationRuleCriteriaAwsAccountNameList, jsii.get(self, "awsAccountName"))

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> SecurityhubAutomationRuleCriteriaCompanyNameList:
        return typing.cast(SecurityhubAutomationRuleCriteriaCompanyNameList, jsii.get(self, "companyName"))

    @builtins.property
    @jsii.member(jsii_name="complianceAssociatedStandardsId")
    def compliance_associated_standards_id(
        self,
    ) -> SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdList:
        return typing.cast(SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdList, jsii.get(self, "complianceAssociatedStandardsId"))

    @builtins.property
    @jsii.member(jsii_name="complianceSecurityControlId")
    def compliance_security_control_id(
        self,
    ) -> SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdList:
        return typing.cast(SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdList, jsii.get(self, "complianceSecurityControlId"))

    @builtins.property
    @jsii.member(jsii_name="complianceStatus")
    def compliance_status(
        self,
    ) -> SecurityhubAutomationRuleCriteriaComplianceStatusList:
        return typing.cast(SecurityhubAutomationRuleCriteriaComplianceStatusList, jsii.get(self, "complianceStatus"))

    @builtins.property
    @jsii.member(jsii_name="confidence")
    def confidence(self) -> SecurityhubAutomationRuleCriteriaConfidenceList:
        return typing.cast(SecurityhubAutomationRuleCriteriaConfidenceList, jsii.get(self, "confidence"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> SecurityhubAutomationRuleCriteriaCreatedAtList:
        return typing.cast(SecurityhubAutomationRuleCriteriaCreatedAtList, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="criticality")
    def criticality(self) -> SecurityhubAutomationRuleCriteriaCriticalityList:
        return typing.cast(SecurityhubAutomationRuleCriteriaCriticalityList, jsii.get(self, "criticality"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> SecurityhubAutomationRuleCriteriaDescriptionList:
        return typing.cast(SecurityhubAutomationRuleCriteriaDescriptionList, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="firstObservedAt")
    def first_observed_at(self) -> SecurityhubAutomationRuleCriteriaFirstObservedAtList:
        return typing.cast(SecurityhubAutomationRuleCriteriaFirstObservedAtList, jsii.get(self, "firstObservedAt"))

    @builtins.property
    @jsii.member(jsii_name="generatorId")
    def generator_id(self) -> SecurityhubAutomationRuleCriteriaGeneratorIdList:
        return typing.cast(SecurityhubAutomationRuleCriteriaGeneratorIdList, jsii.get(self, "generatorId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> SecurityhubAutomationRuleCriteriaIdList:
        return typing.cast(SecurityhubAutomationRuleCriteriaIdList, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastObservedAt")
    def last_observed_at(self) -> SecurityhubAutomationRuleCriteriaLastObservedAtList:
        return typing.cast(SecurityhubAutomationRuleCriteriaLastObservedAtList, jsii.get(self, "lastObservedAt"))

    @builtins.property
    @jsii.member(jsii_name="noteText")
    def note_text(self) -> SecurityhubAutomationRuleCriteriaNoteTextList:
        return typing.cast(SecurityhubAutomationRuleCriteriaNoteTextList, jsii.get(self, "noteText"))

    @builtins.property
    @jsii.member(jsii_name="noteUpdatedAt")
    def note_updated_at(self) -> SecurityhubAutomationRuleCriteriaNoteUpdatedAtList:
        return typing.cast(SecurityhubAutomationRuleCriteriaNoteUpdatedAtList, jsii.get(self, "noteUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="noteUpdatedBy")
    def note_updated_by(self) -> SecurityhubAutomationRuleCriteriaNoteUpdatedByList:
        return typing.cast(SecurityhubAutomationRuleCriteriaNoteUpdatedByList, jsii.get(self, "noteUpdatedBy"))

    @builtins.property
    @jsii.member(jsii_name="productArn")
    def product_arn(self) -> "SecurityhubAutomationRuleCriteriaProductArnList":
        return typing.cast("SecurityhubAutomationRuleCriteriaProductArnList", jsii.get(self, "productArn"))

    @builtins.property
    @jsii.member(jsii_name="productName")
    def product_name(self) -> "SecurityhubAutomationRuleCriteriaProductNameList":
        return typing.cast("SecurityhubAutomationRuleCriteriaProductNameList", jsii.get(self, "productName"))

    @builtins.property
    @jsii.member(jsii_name="recordState")
    def record_state(self) -> "SecurityhubAutomationRuleCriteriaRecordStateList":
        return typing.cast("SecurityhubAutomationRuleCriteriaRecordStateList", jsii.get(self, "recordState"))

    @builtins.property
    @jsii.member(jsii_name="relatedFindingsId")
    def related_findings_id(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaRelatedFindingsIdList":
        return typing.cast("SecurityhubAutomationRuleCriteriaRelatedFindingsIdList", jsii.get(self, "relatedFindingsId"))

    @builtins.property
    @jsii.member(jsii_name="relatedFindingsProductArn")
    def related_findings_product_arn(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnList":
        return typing.cast("SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnList", jsii.get(self, "relatedFindingsProductArn"))

    @builtins.property
    @jsii.member(jsii_name="resourceApplicationArn")
    def resource_application_arn(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaResourceApplicationArnList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceApplicationArnList", jsii.get(self, "resourceApplicationArn"))

    @builtins.property
    @jsii.member(jsii_name="resourceApplicationName")
    def resource_application_name(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaResourceApplicationNameList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceApplicationNameList", jsii.get(self, "resourceApplicationName"))

    @builtins.property
    @jsii.member(jsii_name="resourceDetailsOther")
    def resource_details_other(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaResourceDetailsOtherList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceDetailsOtherList", jsii.get(self, "resourceDetailsOther"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> "SecurityhubAutomationRuleCriteriaResourceIdList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceIdList", jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resourcePartition")
    def resource_partition(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaResourcePartitionList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourcePartitionList", jsii.get(self, "resourcePartition"))

    @builtins.property
    @jsii.member(jsii_name="resourceRegion")
    def resource_region(self) -> "SecurityhubAutomationRuleCriteriaResourceRegionList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceRegionList", jsii.get(self, "resourceRegion"))

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(self) -> "SecurityhubAutomationRuleCriteriaResourceTagsList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceTagsList", jsii.get(self, "resourceTags"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> "SecurityhubAutomationRuleCriteriaResourceTypeList":
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceTypeList", jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="severityLabel")
    def severity_label(self) -> "SecurityhubAutomationRuleCriteriaSeverityLabelList":
        return typing.cast("SecurityhubAutomationRuleCriteriaSeverityLabelList", jsii.get(self, "severityLabel"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> "SecurityhubAutomationRuleCriteriaSourceUrlList":
        return typing.cast("SecurityhubAutomationRuleCriteriaSourceUrlList", jsii.get(self, "sourceUrl"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> "SecurityhubAutomationRuleCriteriaTitleList":
        return typing.cast("SecurityhubAutomationRuleCriteriaTitleList", jsii.get(self, "title"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "SecurityhubAutomationRuleCriteriaTypeList":
        return typing.cast("SecurityhubAutomationRuleCriteriaTypeList", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> "SecurityhubAutomationRuleCriteriaUpdatedAtList":
        return typing.cast("SecurityhubAutomationRuleCriteriaUpdatedAtList", jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFields")
    def user_defined_fields(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaUserDefinedFieldsList":
        return typing.cast("SecurityhubAutomationRuleCriteriaUserDefinedFieldsList", jsii.get(self, "userDefinedFields"))

    @builtins.property
    @jsii.member(jsii_name="verificationState")
    def verification_state(
        self,
    ) -> "SecurityhubAutomationRuleCriteriaVerificationStateList":
        return typing.cast("SecurityhubAutomationRuleCriteriaVerificationStateList", jsii.get(self, "verificationState"))

    @builtins.property
    @jsii.member(jsii_name="workflowStatus")
    def workflow_status(self) -> "SecurityhubAutomationRuleCriteriaWorkflowStatusList":
        return typing.cast("SecurityhubAutomationRuleCriteriaWorkflowStatusList", jsii.get(self, "workflowStatus"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountId]]], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountNameInput")
    def aws_account_name_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountName]]], jsii.get(self, "awsAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="companyNameInput")
    def company_name_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCompanyName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCompanyName]]], jsii.get(self, "companyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="complianceAssociatedStandardsIdInput")
    def compliance_associated_standards_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]], jsii.get(self, "complianceAssociatedStandardsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="complianceSecurityControlIdInput")
    def compliance_security_control_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]], jsii.get(self, "complianceSecurityControlIdInput"))

    @builtins.property
    @jsii.member(jsii_name="complianceStatusInput")
    def compliance_status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceStatus]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceStatus]]], jsii.get(self, "complianceStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceInput")
    def confidence_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaConfidence]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaConfidence]]], jsii.get(self, "confidenceInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAtInput")
    def created_at_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAt]]], jsii.get(self, "createdAtInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalityInput")
    def criticality_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCriticality]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCriticality]]], jsii.get(self, "criticalityInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaDescription]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaDescription]]], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="firstObservedAtInput")
    def first_observed_at_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAt]]], jsii.get(self, "firstObservedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="generatorIdInput")
    def generator_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaGeneratorId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaGeneratorId]]], jsii.get(self, "generatorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaId]]], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lastObservedAtInput")
    def last_observed_at_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAt]]], jsii.get(self, "lastObservedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="noteTextInput")
    def note_text_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteText]]], jsii.get(self, "noteTextInput"))

    @builtins.property
    @jsii.member(jsii_name="noteUpdatedAtInput")
    def note_updated_at_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]], jsii.get(self, "noteUpdatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="noteUpdatedByInput")
    def note_updated_by_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]], jsii.get(self, "noteUpdatedByInput"))

    @builtins.property
    @jsii.member(jsii_name="productArnInput")
    def product_arn_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductArn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductArn"]]], jsii.get(self, "productArnInput"))

    @builtins.property
    @jsii.member(jsii_name="productNameInput")
    def product_name_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductName"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaProductName"]]], jsii.get(self, "productNameInput"))

    @builtins.property
    @jsii.member(jsii_name="recordStateInput")
    def record_state_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRecordState"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRecordState"]]], jsii.get(self, "recordStateInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedFindingsIdInput")
    def related_findings_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsId"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsId"]]], jsii.get(self, "relatedFindingsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedFindingsProductArnInput")
    def related_findings_product_arn_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn"]]], jsii.get(self, "relatedFindingsProductArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceApplicationArnInput")
    def resource_application_arn_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationArn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationArn"]]], jsii.get(self, "resourceApplicationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceApplicationNameInput")
    def resource_application_name_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationName"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceApplicationName"]]], jsii.get(self, "resourceApplicationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceDetailsOtherInput")
    def resource_details_other_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceDetailsOther"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceDetailsOther"]]], jsii.get(self, "resourceDetailsOtherInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceId"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceId"]]], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePartitionInput")
    def resource_partition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourcePartition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourcePartition"]]], jsii.get(self, "resourcePartitionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceRegionInput")
    def resource_region_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceRegion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceRegion"]]], jsii.get(self, "resourceRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagsInput")
    def resource_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceTags"]]], jsii.get(self, "resourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceType"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaResourceType"]]], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="severityLabelInput")
    def severity_label_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSeverityLabel"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSeverityLabel"]]], jsii.get(self, "severityLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrlInput")
    def source_url_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSourceUrl"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaSourceUrl"]]], jsii.get(self, "sourceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaTitle"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaTitle"]]], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaType"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaType"]]], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAtInput")
    def updated_at_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUpdatedAt"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUpdatedAt"]]], jsii.get(self, "updatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFieldsInput")
    def user_defined_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUserDefinedFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUserDefinedFields"]]], jsii.get(self, "userDefinedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationStateInput")
    def verification_state_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaVerificationState"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaVerificationState"]]], jsii.get(self, "verificationStateInput"))

    @builtins.property
    @jsii.member(jsii_name="workflowStatusInput")
    def workflow_status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaWorkflowStatus"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaWorkflowStatus"]]], jsii.get(self, "workflowStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee07d2e693931b221fa288f56ee995bbd43f47458142bd13acb3aa8d12c9d1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaProductArn",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaProductArn:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__becaae9bdbc35675f019944ceceebc4882e7d86724339f60356ba654030a8efb)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaProductArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaProductArnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaProductArnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__495c6247ef56bbb2437d1a7a57531a97b5a22659e90f5e9f4fb1bc441c0561c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaProductArnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42520f0fb6027055a5025248af493a809bdb2a95931da62ebca1af0dba004a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaProductArnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64735ae34a615f57da7cb2bff66c9abd4c2acafada96ca09472d35d8b73ab96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bab78eaca5561eea9be5c5582726c1054257bb38d981ed3c1e86f57041f53b52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__346cf42abd79258432933cf4313f4fdfbb78115f33d0b276772f2f50369ee5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductArn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductArn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductArn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf3887bb2fc2b2d0f4ba7193c967027e58699514ceb14597f0abd4270c11dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaProductArnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaProductArnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3abad041d96ecfde798a55f23885ae646601b46582b3d5b6bfd7d45d05ea813e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb713b578f447ff8f9e8cb6110ee0af697549982741bc6e8b812f59ee4e1429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c454b3977226c44948a0644bdd34fbed79b3b62f3100ed8fc1bec66e9cc3a519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductArn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductArn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductArn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ac8599fbc323f6825e6a4c90b3f27ec6b19321b9e91c775b95d026ee1afd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaProductName",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaProductName:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff34be70c7946e1f24bb08a9de8f8ebeeb24a0ac502702c09d2e5a69afeecf7)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaProductName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaProductNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaProductNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9585bfbf503fe222c0fbd6fbbb87b60cf15b1c88b6d79ece9c810c05da9779)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaProductNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d2f2cfa25356ca6392bead0a9ab267e368b7dab78f5d35c97760b7cc13f0e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaProductNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3454b1220040e93879c9d853523853e52aad4e4710261affc7d493d363e05743)
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
            type_hints = typing.get_type_hints(_typecheckingstub__714cba70ccc02be55cc929a71ae80f2894369997ab55187a459750890877aa43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e103e104180473b89b87ae3ca73e5f4d77a4b750ac5e5691071a2433f4994303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductName]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductName]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba215490308e6d0e5049a918edcb9bc6c2e30d370890b77ed1189e5a6f426ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaProductNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaProductNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda93808bb98379aeda7558c3b9455c143d68f18ebf4347095e1937cd13d9aca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70936fd69439e6f4b3c995d441ca88e7571effe9308b0f884ac4375e91ce374f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81d499008397efcb68975e0c94b40f03ed48498fcf7ccba6917b0bbb05184a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductName]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductName]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductName]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be52fcc58b7cf96f3f0adf70110bc4f311e86890e2f852289a7c335924f1b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRecordState",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaRecordState:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4ea47433a92a91082dab8a8c10befc9340c557388df5a278034a13a6ac93d2)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaRecordState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaRecordStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRecordStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3814748ce62825347d572ee20eadd5d14c31c2f65778dd208000ca3e78da25d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaRecordStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8207982ce3e236eed57827d771d3621ff265e2504ea2a37f50b122dcde5f7342)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaRecordStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95d6cab57688640f5e7ef860326ed1f354e7d781345774e9d46bfbf2283b6f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__443d1933f89374b776f6380f9faf5151f671c6f40434cdf2918da51644db1a64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9874abb04891a075a13f03c3e27982a5e2ebbda72a7811e989ee4ce4eca7b415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRecordState]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRecordState]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRecordState]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55f0164597a8bf6445cfd98be24f05fe9bd5cddb74eec462ece9f508a11845f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaRecordStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRecordStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac98d3a2981ede8ec7c35e54255f3b48d7e87f5da49cca3a488b917ff6ca93d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b850cb2155068971fa80855a61504ab914b5c45b032c8a58c73df8e6ae052af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e225bd04821431873032bbc07f9c9966f3af22b097615a6ad03bf7e4f7dad23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRecordState]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRecordState]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRecordState]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ad3fbcbf0523bc01519408b2de805d80ce29d9ba4e809ff5dc5076829df805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRelatedFindingsId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaRelatedFindingsId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29a67ae72d8c36505a5d859701652616410011db6e5fdfa9010813f3cbdc7a4)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaRelatedFindingsId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaRelatedFindingsIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRelatedFindingsIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__806aa5beb6a15a4b5b235da6ad2427d6398f1e8f5fb479c04284431e3c471fd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaRelatedFindingsIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ccf4038116757230cb3a272951403ca8102bdb7a62184b5240d5f7512c2514)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaRelatedFindingsIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59de4757ce5527da414579c6a483fc79a8f21307e45569e1ac2467f8a80aeea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0781feabe4a05ff799192aff8392a1223b8fe7fc4430affa1d6dd4341d79746a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73d1329a1a87e934701c5ac78917e5b8052ca49bf7b12825856e11b20b6ec1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4aa14aceaa20a604a4269a508ccad05a39e0ed9fd3c400c508cd8809ccf35c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaRelatedFindingsIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRelatedFindingsIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e27b3c2b412e18e3e5d9b456ddcf191b485bcf4aa17db6e05c5b05d1f59a772b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ac0ae644b7bedc5722d183aa257913c9eb5858d9d3e95404eb18ced4344c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b609790a22cd59465e7c5ff9dccac56d2a482c25baff57386ecf806ad55f554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4f4c9d2fc280846806cf4585b42e4c7a3afcdf158050f6c0ac9f22eb4eb175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5902d005eae572599f72a2acdff454b33808b77211a83d83bdffaf767b1d5f)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6aa0137d57a8bc433238e3879cb53445cf0d00b583c1d68bc7d72a6a7c8d4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d511df9f3ba56f6d651ba8e3096722e73838ffddb6e5ab916f58c0898ecaaca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0d77f044e3136e3b6e8af125b801fe2fc3d8d7ab0f81863ba1491945661b24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d52cb420e63d71f4424f3db860d3c9dbde4d0bea8dc3da6342da89956eb8fc00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e823741052dda71ec0761c81dc3ecfb70e8d8eb966902912e18b1e4f72562ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799ab364afdec6e775217a4645b00c529c8d0cdc18800cc2e4009d55cfc356c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54cbf0ebddf508b631e8ce53524f4eda6c0e00363894ffddf774d6f2387301a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4111133fa261701c12e3d79813babf22b8fd8cc29d91468b3a68b280fb778be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b16400707e9aacc598fae8f5f90ac19d1c7800a00763bb200fb96cf701036a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739d687a4b7fc697b39f4d170db8e796b793f6e55e8c49550bdca53344fcb213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceApplicationArn",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceApplicationArn:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c0ece931a737d74bf60f1b81ee620de4c58edbfd5f19a2c2a8528df0123de0)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceApplicationArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceApplicationArnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceApplicationArnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d754df6bba99dca21232b365864eb9504d534a87bd687a92999225fecccb7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceApplicationArnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8eef3e6d9d6a8b8c57d228546929c5475d6a5bc65f09d27fd3f8d3c929a0032)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceApplicationArnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201f5a8e1d724b4898f375a021cd2cc10d70c9e553fe0f7184abbd5c3eda1d24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1fc7cc84ae71d08bd884e136786b8e6c1d28211732315c91672deb0b339f041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ecfdbe268690fd51c35059dac40e899d62ae9f88fcb81e9c1b444d1111a79db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationArn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationArn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationArn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f969a64382114ae2066a925c87027fff390a1777e1f86f5fb63a4269956904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceApplicationArnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceApplicationArnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60384bbce8d2545f60d54d408c886732bb16759af7f05087292cdfd6ce955df8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501bb18f5b2d7b98aaf83ccea84f089587f4e11ccc07198e23ca241511c80c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b19756f036343f6e728d05ec41410747d7b96884fddb5845eba1d3f23dcc43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationArn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationArn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationArn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b682637defb12c57b8f00fbc82ec8fd7ea9ee1a8631423e4ac9d76006d9ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceApplicationName",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceApplicationName:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24a1f773fb4de4c4881665617f57e9d259794ff02dd0ec462f20896b8295003)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceApplicationName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceApplicationNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceApplicationNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18d166236147819995051a98b4a4f79d5871e8b8863458fdb156c0cdc4b98665)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceApplicationNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c13f1685f06ab761db2037696a505a231f4b3d75f26cd46c1e8831f6b45d0d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceApplicationNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25a3ae065a8db0f3bef8cec3298bab6aaebab43d8832d59a8b289836c5ca975)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4a9f794e3b6a2fe3f28425ace2da9ba12cdb4c6c6fb399ff745e1081c2aaa76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__166bdff8cacee423bb559d0edbadaee828361ea7dd0a207379f4922511dcf3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationName]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationName]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationName]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c6d5a06d78a22c71ff228a0f72ce5f5e689405719a5fbb0d4ca15da22c74ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceApplicationNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceApplicationNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__968eb8d2048cd7bea43461a76d33673cc9ab462fd3decffb700e9178e82ce454)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5977a751c497ad0a4976fda21a617c2e24def56dbc697d8afb551508356f0ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95ba2fd485e88e9aee569a72e43517ec3ffc45b8097cb21552b6bc8d308a12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationName]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationName]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationName]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc8a4417621179f67d30e05b8f0cd14c87938ccb9507956fd9b1431a6fa057c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceDetailsOther",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceDetailsOther:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#key SecurityhubAutomationRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824e81035ca8e2b0e453ba800258ce80899b1fd8aa4b4b8600d15fdc58e1bb79)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "key": key,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#key SecurityhubAutomationRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceDetailsOther(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceDetailsOtherList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceDetailsOtherList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37ba0de307fad8f7823ff51b560c535f8aa3822738504705eb8acc9c6853fdb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceDetailsOtherOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913fb504bac5ab9fb7a3af25e207df535cace52bdcc0ad902e2a5457e72cfb0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceDetailsOtherOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a15a2b96b7dce61030f4072278a99325dc92a9a6caeb5acc374d5dcd4e20a1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74bdd17e4ceaf000777a59fbd6947e81246fae76c6d64e2d918a8efe4e0f171e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de7a867932e33bdd5e71605822e57dd80a1b8aeff1b448401c179119a9245f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceDetailsOther]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceDetailsOther]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceDetailsOther]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01856d10bd3783c9785f015082ce08cf07faf30f6dcc594fbfb460d4619ef56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceDetailsOtherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceDetailsOtherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f27d796ceae02168172f2af679c62976f40f58b78ef41ed04c38c0fcf25d66a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b85b92c1d3a5bd4462b5ca752edb55c52c9d1ebbfe3287ebda57d6073c5875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d54d70cfdf50f127c974b9bc68693565456178391b72839d6cb6f3ad41db15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c062c5af16b6aa13b8108aafb89d2f090eb9ccb97b876fe86cae80187509d8c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceDetailsOther]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceDetailsOther]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceDetailsOther]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b883b3f0ffedb3e7f88b87c360dac6eb3f240be41e8fe59007d51199726545fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceId",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceId:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0791dd722710cb32bf141500351670a3cd765df4d27e1d67d45ffd43b31609bd)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3af61048db78a5fe369ce8c12de43f667d435a59ba1bb36e398df770426678b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e82c3dce85c29a5d322548cd265abbc378f5e8006f82a519ec06c2686375aa4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebafad6fd7dae1c993daecabfa7d0ae25621bbbcd5a4023eb126c67300a6185)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8cf8342e8e4e50c4edf81ff2b6d26eef7dcfc73b14bf6ddb0b59d77c5b2be11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af9a8815ad2bbb0784c17f62123e6d7d8f77000968b199fb43a0c8c95248d41f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceId]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceId]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceId]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b561f2737028c0f44c54784ad745b8c610669bf36d3584d0e1650f0c4035b095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa880d73fe33255326fa1a61e6f7a582958100a8ddd1492d9babb4e71a8ea790)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e298ae046917eab9c62108aabc334852ec3380abf5af6d11f1cfaff957d998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d463e5f666d69544003ff8f329466580ed59b044913fdce60a3897de20c1b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceId]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceId]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceId]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288846eeaff3c31e8b7b22752ea098afc565a5aa1aca7a3bf91d32281adc3a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourcePartition",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourcePartition:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8fea332acee36957017e6404fc0732be94482046bb95e10be08983e040894c)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourcePartition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourcePartitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourcePartitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad8bab761ae0fc1bc9c7a6bf06d18fc66c76204b60feb859af22a2c611eadc36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourcePartitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c79d9842210b9025f1ee3f9ff253e9d12ad7542eccddba8afb5522fe64a6507)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourcePartitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b9e317e4154f88c9ae3020cc52a5854a4547d8b73c4af89caae605d05e0858)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e1dcf8b5953c653c3daeea459c316d44501938ef2d56134d7185610e6b6316d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ee28df5920a0bc8149278a96bd5e537701915019e2adf4be8b84cbf8d0e7acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourcePartition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourcePartition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourcePartition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bf15cd9e14c82776209b62d3efc6d0ffb14f13e32d9c83ce1d052691cc7498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourcePartitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourcePartitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33144dba71c2f3a873fcd00292e4c60e2421e1eb2130dd73c8beb6ef97a5791a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01b83df43e6f62a7638779a1dbba3bf05c488e4a40dc30c9aebeefc9080fed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6edc1d1c9ed5182f8f5a198c5638ebe4d853ce8d46efc12e1ab0a3287ee5376d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourcePartition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourcePartition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourcePartition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e492be506afa8e7965f03245bb40bdaa41cc4cfcc020d2fe985c432e813457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceRegion",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceRegion:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016ae44727fcfbd30166bed8830fbee6032b9a5e24d361cfd22c8808988307fe)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceRegion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceRegionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceRegionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b730ecb954464bcf05f2f927313009db74ea132ef3adf6144f7bc381e680721d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceRegionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051239f76875e55b86b637933e4ade20b06fbac956f23cbcf9e71c74769ca799)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceRegionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137d6598ab6f44c636a43719c2aec62aed88c420f0bf2e8b911ac286fa04f085)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1707ee5596c1a83180543d2ba55f11feeb89f2c91f088c20eee7539ec0a1678)
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
            type_hints = typing.get_type_hints(_typecheckingstub__423708f2b83063d9ef2bb32ee05972fb904fb4079ae537a7b3b952739c94846f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceRegion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceRegion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceRegion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6779e783d602cbde607fe9d10677267a65a5c57b1d3c96abd5e907456ceb2c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceRegionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceRegionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fcb26b32d7270fb52dd2aa515508fbbedecb9763dfbadf6d27ac227a658b7e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d0368c03baeb7ac6ee17a785d3db9559254b89c6fd270cfc82deefc6ece7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bea1f08093ac4a3a3fd00bd2a0019cd59bf706373ebcae5627009f7080cf33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceRegion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceRegion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceRegion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fedd377dcaccea3fde055ed69692f2055783d7c6e7997d5dab8d1e95788d4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceTags",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceTags:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#key SecurityhubAutomationRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e880fa463e243cdf56839dedee6f51fa7b9440225683506608ddd0503e0680)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "key": key,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#key SecurityhubAutomationRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db025782326da00e9e920f42999964abc818029aad3aee793c5ab96a51910946)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca546ff4136063e8ae67c344d59dda6e436f5c2f4f5235356ce853e3e6b57538)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd6efe67d4d1d4a9e6f4ee6584bd961c5fe8992ec133ac270a60da352afc086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf9dcb4bd18db5790415c775fb5d322eb672b19e44c4d28bebfdbdfdb9c5d7e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f2b76399b63d72e5d83fa935fb9cb11e505fcf9aaf502ece5fbab65ec662b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae8e6019545b98a1912f0581c33fdef42b7a3e67a79cd586966de0abde2798a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6adb0a32ab0cdd2bc0fd066b0432d5085af567a568e83537d09945fa4a3ac16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0973976c085e0a4839b9069a74d5aa39cb90ed32e02fa443eb10426374d58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80ff0a9f6466430890bcbe48c1421f3804099d7611649b8ba379150b63a7941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcd72ff8134db31ce2d46651f5c48402bf96782bd8042aa1c7fc7e8658dbc51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09571687268c8cc0a25589546539ffc785945f9398b8e50e1feaa29a9a4b0e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceType",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaResourceType:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4be44c994c937aee162b4cab53539d3e60ea311911a4b47329449a8bbe9cce4)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaResourceType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaResourceTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87c52cc926ebeaf80cd7b0bf77ff5283ffb74b8e4c543cd751945ec12648e96c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaResourceTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6a1161b67494bb03aff0ae146cd7afdf4abbf3c12146c4a62e05400d4bc4f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaResourceTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12c46891bcc0978e54497a62662cf7652121fad29c3f25a7c452396f15b8e08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3b7b057139bb0e41aa64e13550447cb441aa0da16eb7f6b8388c02b7f5180e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3edadd307cb3ae1c7284aed108f8dac9fdceac6f1e5dab2e0e9dd13b602ca53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb464c65db7cc4aae703f0c3f5ac6dae4e0d6400f1b63f744eeef0022eba017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaResourceTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaResourceTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4ec30090af859d402aacf5ffa4fc003f4c6e485a38fbfa4b1ea9554ff0770d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b919627a477f940db9092f7ebd976dcc63bcb3c2a570aff80b824575cbea47ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee917d0ddaa50ba901a803dfaab097e82b27880e45dc12b69629e0e2f077879f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e25b2f31804b965b83fdc6de5e707389831196128d5ff5514f7f4e6ca1e487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaSeverityLabel",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaSeverityLabel:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85640790e2c1041facd58b24992bcce3f3fce94ef8e4b4efae8f5a9c69dcf5e)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaSeverityLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaSeverityLabelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaSeverityLabelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57388570b1cad118ba7105f33904794c7a3cbd70f92de03684461a77ec5dabb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaSeverityLabelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff970be83387e6c988c7670f860f5b7045d30e951e9d177a45d3ba9c45968dd1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaSeverityLabelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98c06898db5c80662d331d39d15d222f89ceeeab0521f82484f528e0bcdcdc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c1c51e91ee8ee9b8d8c0edcef06644333c94f8873fe369f13f766fc76997937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd55443493fefc02f90eee29f1d6667b9b49ede449cf352264783519a7d6ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSeverityLabel]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSeverityLabel]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSeverityLabel]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8037bd9ac5a335f429a930cc930242d5affdfb32827cc1d0897103f52cfb74f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaSeverityLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaSeverityLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b0cde6238c742c1726b79a9199e81ec94dfed5cb8ac316f13f496081a9e5c4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52548b335f0feb5bcb8d3085babdabd7bcf86babef758405d408d7aa636216d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f2d2964bd9d1377c1bea3200b0aa74b1de0d1b5b1e6429307034955b38899b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSeverityLabel]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSeverityLabel]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSeverityLabel]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1330acf909826817aef56bcd355ca260de22fbc288806ac490de9c5dc9f063d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaSourceUrl",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaSourceUrl:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf04c9f939ee1ec043d68cdbb02114e8d27916e30ebbc68aa35fcc851af4e749)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaSourceUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaSourceUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaSourceUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__154da1dea2bf8b37e6667edd1cd5d91c7caa34df9418a7c0696327801c290ec2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaSourceUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070af6465178b512e601a0032370c26dfaf1bc2906cd47bf7d5955ae5fc39b82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaSourceUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0c86d57b24b7e185288f83330605694a87025f4c6294c120b3503bbcb64717)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fc708348eeb1026be3d75038af7a23c22226a5dd1ab3ea3d8c28f435f67cc2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fe8e2f86d3a6d5c98a7fd153ad6cb05c85c4c6295485f6f56cd0555ed177044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSourceUrl]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSourceUrl]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSourceUrl]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4f2690068b887439c7257833bf3f4f3f79a1210b65bd0a8a875906af743728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaSourceUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaSourceUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ee69237b5f3d3d2c8f301ae580ea124da33779a73d74f5d62cb819c1bffbd5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24555d1472a1d64c410dd1a111da3696f3bdeb68aaccb14dff149211267dacb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8c78850224b5934354fd827d2d9af53111fd5d3d3dff17a9fc55817d51f675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSourceUrl]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSourceUrl]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSourceUrl]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ad5ef5b1ef8e11d77b0967e08ffe582da45bb08c256a7276d368ed6f582b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaTitle",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaTitle:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b17927aac5b26176da33f50919e727d762656ce837dcac65ac874b855b28c5)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaTitle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaTitleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaTitleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bfe49ddf9cad4752a983a8b9ac7f87f082525d39e913c48afb3eb4f98f16de6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaTitleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204be127c5ad3bf7c93ae31d686eb6fd25b2c433a3f815ae98b4df1acaa50091)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaTitleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc593266748d0ce2ddf7414422438f1b51b6fb6936a5040791e3f7d49dea532)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae19a925bd61ddeb0af6cf812b31fa3d6e34da5f5e1a65ee73cc0458c9b7ae05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4f26e3178857ec9b910f1cf2ca80f7f53e0e3cc2cd739fdfd52167506ab1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaTitle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaTitle]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaTitle]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b4b046b56ac37c974dc0d85ee76a5986e24bf0464c1449ac03c7b649bc58cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaTitleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaTitleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d8747272667c694c937e6e045b4b3bfb4d0d1698f0fafa6fcf777c09cdbb434)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3aa1d74ca7744d2507fdd03095d1b5fc00472cf27c8812b10b3166a81fb71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f18287ef731b0b8c27e485e94cfb1e0600b61aa4415647c9d9858ff27163b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaTitle]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaTitle]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaTitle]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed9f1636eb7b564efc405618c706cde5fc0a52e21e37190232e5c28ae43e170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaType",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaType:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17fc0894f828e82b41be6ca265f0b66fd93216c4863123e676e2fd5ed1e20dc)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fcab67b8422a601e6b1e5f3152fd5b5acf8c17c2700fd745ae94700ee3476a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6817a3065b5377284ea9b5789c10e5cd4116b07396433079aac8505465ec42ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b1580134d68320f889dd1abbac4192c7c806c1453f42f1156f00b37023dbb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93f0a7361d1eb35ddaaef4c96780b1b65de3b0cc1056b4bdb48438e461195723)
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
            type_hints = typing.get_type_hints(_typecheckingstub__526e5764d678a3612f23cdb46d4a1deed2954af3df224b6adee0a337cc7d3d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a9d0a0b3aa3cabbf22e4f79b30c7063ea008dfdd9f6cad4ecfdf5c8dbdbe58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2c491c8ff106190afe72bc3a2c570a85342c0ea2ea5763cf1b139646274cd09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dae0d70d10cd6f617287756537412ab94cb987f4634eb398bb9db779cc1ceb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2144a5b16e6b755e19e273641778ec93604a425655e28d19e01362e194593bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86fef41b87d8184cf9f89185c7350f74ed6f9016ac65eb7f12b29d8f93cf0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUpdatedAt",
    jsii_struct_bases=[],
    name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
)
class SecurityhubAutomationRuleCriteriaUpdatedAt:
    def __init__(
        self,
        *,
        date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityhubAutomationRuleCriteriaUpdatedAtDateRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        end: typing.Optional[builtins.str] = None,
        start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_range: date_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ee3c01a74906ff49252f48800ca3c39adb45436dde95258c67733b52ab3db0)
            check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_range is not None:
            self._values["date_range"] = date_range
        if end is not None:
            self._values["end"] = end
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def date_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUpdatedAtDateRange"]]]:
        '''date_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#date_range SecurityhubAutomationRule#date_range}
        '''
        result = self._values.get("date_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityhubAutomationRuleCriteriaUpdatedAtDateRange"]]], result)

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#end SecurityhubAutomationRule#end}.'''
        result = self._values.get("end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#start SecurityhubAutomationRule#start}.'''
        result = self._values.get("start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaUpdatedAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUpdatedAtDateRange",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaUpdatedAtDateRange:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0aaf9cf5aaa07986df59dbba39dd456bfa4d1fc439df5e8a0f862e1cca8342d)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#unit SecurityhubAutomationRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaUpdatedAtDateRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44a7ca4779992755577275d8072867f6a22760f791458efb371562a21bc978be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb8b8d05e9920487160742ea2527dc99a0d37da10f647c54f41a24162fe3663)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3243f74668772a178bf9aec884d07dddd2ec3a663e4478255759df72719f35b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47c20715cdbb10f0cf63c73a704d5f090786b4e37847150345b346e6cadf092)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b26e7792c966182c204a00dac5d958118868379a3f71518e4ba998c52d45000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4587ccb674e9c8ff172bf57ee1f5c2f5564ad3eba3a97afdb99ad3477651e15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25002a25d9c5f726e0cf69f0f93bf00a436bddec5052b56b681b6570063db636)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f54f948647e140828dfaf1da9096c9bac8796029bc02daf6cb096aa8515ca5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a655936e3d75e17fdd39f1efe831036bb08e59066902d5f85c9b4bfa82b4409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c78c9c13c2813498b2777d9534e00380813a82d361d0f32d899f1678bdd9a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaUpdatedAtList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUpdatedAtList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b9886fe86f5188ecd4e9ba62371638caf6e0b414c27d42039587ee16c7a9a3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaUpdatedAtOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd50509be6b695834ec00715c0e80c6f46f7b223953fef752be68530780eb95)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaUpdatedAtOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49aa1b211fa6a9ac3fae9a0971e5ec08069b2b1abb120178cc86be01615a4254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e10f8ee42590ac84f231d9879d20800900e3f5c46c6d1fd2d17dc4736ae1ec4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a9fc4c1ae87fde0e587186be0b4cc30ebedd52b11c3c9a0f6898b44be41fb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cec38ba4f670f99df4bf9b327637a4213097df1f59c753263699be2a46f4c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaUpdatedAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUpdatedAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee8e610034d7aa8ba1c1580d3383c3d855fb2181d12fbe1b12315bcfbf88f795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateRange")
    def put_date_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf34161507d188a65569a2d573c12321b8a32df6afef066ea44a36b4f4aeddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateRange", [value]))

    @jsii.member(jsii_name="resetDateRange")
    def reset_date_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRange", []))

    @jsii.member(jsii_name="resetEnd")
    def reset_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnd", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @builtins.property
    @jsii.member(jsii_name="dateRange")
    def date_range(self) -> SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeList:
        return typing.cast(SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeList, jsii.get(self, "dateRange"))

    @builtins.property
    @jsii.member(jsii_name="dateRangeInput")
    def date_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]], jsii.get(self, "dateRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97e81aadfc934affc7341f7d0a792fa4ae2d1483da75018568fb231430aef11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d802adc68bbef164c91ce6db10111e16c9540ae816289db167b10187810f7cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b0a50fb2d750bea869ef2c293f345b61cf119bd96a3fb2d5883d07b06e9071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUserDefinedFields",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaUserDefinedFields:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#key SecurityhubAutomationRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6567a02df2318bcb208d1b484ec9369f827680c3791ec76721ecd58f2f82c23b)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "key": key,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#key SecurityhubAutomationRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaUserDefinedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaUserDefinedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUserDefinedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d06dbe74a541f997903d5ee42e7b60407d705489cfce7451b0c855b676243f7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaUserDefinedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f464fc47fea14a9683845788649ed65944c1e8eb64915b5411b39531080c888)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaUserDefinedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2b4e5c2b97afce8c41fcb8149f9d8ac8ffb1b928617fa86366d3693b422140)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfd2243781a60d0c53e58de6dd1671ca5386817e35f5b144c3ba1bd6ff27d903)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee0d8d43e4351319c5e3f34049c242408756d354a28a7ed33dbf7f2319bb064f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUserDefinedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUserDefinedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUserDefinedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46a52ea087f34c9a45bc9ac5df24cdf645a765af753cb06b3d5e1f4bf97a223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaUserDefinedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaUserDefinedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__783d750e0432fe55dbd68bb639ca104c0d99c7e2d288f878741d5963282456ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8be81b84488693c461d49980146e2acf409eeb20823922bfccc6bb4914df9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400e1daca2d9e0f4dd73f54a1557908436e4acee71e5b86ded55b3cc62a35ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc6385645424fcf27a5f93f44f49b3ef0655ebd2d1781451d563196bc83b079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUserDefinedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUserDefinedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUserDefinedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11037badc89c27f1bff296583405c9609ee00e426865adf72ef3940afba8246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaVerificationState",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaVerificationState:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d9d8f33ed064cbba006ad232c4d1566ab090899199018403030118357f4ff8)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaVerificationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaVerificationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaVerificationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbb11b67432512f2c29faa54c7d227be147b52636b5df7a2127c3e40adbe7c75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaVerificationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a654fc9757bed3088c77f85e63f00253ef8c1829c4a6aa8f7a21ded63144ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaVerificationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42adcff481003f11fd81163639f10e687173bf4ec67afc193915cfa8c37c088b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7adc9174aec4186eb6318389011a2affd2fbb79e80e82d0449eceb81077fed5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3472fab951d5229adba1b7f4bf62887ca815dd14769d7e334b1a6cf1afa85481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaVerificationState]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaVerificationState]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaVerificationState]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81820bef6ca5dcebd8c27d9d0692c7e74f2152cc43219f93043215c5abebef9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaVerificationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaVerificationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c973c070320b80ab03d701867322f023fc04ddb6477c73a49b07eb5865acbb31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c709bc9353aac454fef536a8f6e78f6967b0e76227365a05a30bc8097d7ea2b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e91e324b03cf1aedb7489cedd94eab88290cc5485e4f9ae8fafc45149ab99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaVerificationState]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaVerificationState]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaVerificationState]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb3091186a24bfd4b8b7e3e57a0c938b65f57e4686687759ea2be9afe2e1d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaWorkflowStatus",
    jsii_struct_bases=[],
    name_mapping={"comparison": "comparison", "value": "value"},
)
class SecurityhubAutomationRuleCriteriaWorkflowStatus:
    def __init__(self, *, comparison: builtins.str, value: builtins.str) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cf23737c84e6489eadbb6b062be2e7b83d6f07aeac0d921e72f667104201fc)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "value": value,
        }

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#comparison SecurityhubAutomationRule#comparison}.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/securityhub_automation_rule#value SecurityhubAutomationRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityhubAutomationRuleCriteriaWorkflowStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityhubAutomationRuleCriteriaWorkflowStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaWorkflowStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e5eb5dc2c4b4e00f49e661f2839b1be3110d7ee203bebc9fe2f3ad1880d9ada)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityhubAutomationRuleCriteriaWorkflowStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e938bf5e66bcfee027e4437f8023654fff4d0ca917c599a203f375699d6113)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityhubAutomationRuleCriteriaWorkflowStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96fa894df59f73dc874b7c83af73561f7289595cd60cea22bb893c89ce366dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba8cc46fee2dfccf0880ee307336cee773779732cdc0608eeeb8845a062978d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39ba90dee3d37d7fbfcc4631cb5f02b10073a5a389a3e39f837862829e3c051c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaWorkflowStatus]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaWorkflowStatus]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaWorkflowStatus]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24f42130f4c290417b47f84daefaf9a02244dd9b37155e682e69285e0b2da96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityhubAutomationRuleCriteriaWorkflowStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.securityhubAutomationRule.SecurityhubAutomationRuleCriteriaWorkflowStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f195268db0109d99925ea06f65ced772974070226397068a7a2b90892d60d65c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141ca429ec3bbe526b7e7006c19fb273cb55546985d9298142c1b05574669362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103b14370cd411ebc3e560d7297be6802a1b59c0fd8b22098f264353fcde7e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaWorkflowStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaWorkflowStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaWorkflowStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85d660efcf481af48b56ed16029b755b011a435ffb8ffdaf3a3e541798db7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecurityhubAutomationRule",
    "SecurityhubAutomationRuleActions",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdate",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateList",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateNote",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteList",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateNoteOutputReference",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateOutputReference",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsList",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindingsOutputReference",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityList",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverityOutputReference",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowList",
    "SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflowOutputReference",
    "SecurityhubAutomationRuleActionsList",
    "SecurityhubAutomationRuleActionsOutputReference",
    "SecurityhubAutomationRuleConfig",
    "SecurityhubAutomationRuleCriteria",
    "SecurityhubAutomationRuleCriteriaAwsAccountId",
    "SecurityhubAutomationRuleCriteriaAwsAccountIdList",
    "SecurityhubAutomationRuleCriteriaAwsAccountIdOutputReference",
    "SecurityhubAutomationRuleCriteriaAwsAccountName",
    "SecurityhubAutomationRuleCriteriaAwsAccountNameList",
    "SecurityhubAutomationRuleCriteriaAwsAccountNameOutputReference",
    "SecurityhubAutomationRuleCriteriaCompanyName",
    "SecurityhubAutomationRuleCriteriaCompanyNameList",
    "SecurityhubAutomationRuleCriteriaCompanyNameOutputReference",
    "SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId",
    "SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdList",
    "SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsIdOutputReference",
    "SecurityhubAutomationRuleCriteriaComplianceSecurityControlId",
    "SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdList",
    "SecurityhubAutomationRuleCriteriaComplianceSecurityControlIdOutputReference",
    "SecurityhubAutomationRuleCriteriaComplianceStatus",
    "SecurityhubAutomationRuleCriteriaComplianceStatusList",
    "SecurityhubAutomationRuleCriteriaComplianceStatusOutputReference",
    "SecurityhubAutomationRuleCriteriaConfidence",
    "SecurityhubAutomationRuleCriteriaConfidenceList",
    "SecurityhubAutomationRuleCriteriaConfidenceOutputReference",
    "SecurityhubAutomationRuleCriteriaCreatedAt",
    "SecurityhubAutomationRuleCriteriaCreatedAtDateRange",
    "SecurityhubAutomationRuleCriteriaCreatedAtDateRangeList",
    "SecurityhubAutomationRuleCriteriaCreatedAtDateRangeOutputReference",
    "SecurityhubAutomationRuleCriteriaCreatedAtList",
    "SecurityhubAutomationRuleCriteriaCreatedAtOutputReference",
    "SecurityhubAutomationRuleCriteriaCriticality",
    "SecurityhubAutomationRuleCriteriaCriticalityList",
    "SecurityhubAutomationRuleCriteriaCriticalityOutputReference",
    "SecurityhubAutomationRuleCriteriaDescription",
    "SecurityhubAutomationRuleCriteriaDescriptionList",
    "SecurityhubAutomationRuleCriteriaDescriptionOutputReference",
    "SecurityhubAutomationRuleCriteriaFirstObservedAt",
    "SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange",
    "SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeList",
    "SecurityhubAutomationRuleCriteriaFirstObservedAtDateRangeOutputReference",
    "SecurityhubAutomationRuleCriteriaFirstObservedAtList",
    "SecurityhubAutomationRuleCriteriaFirstObservedAtOutputReference",
    "SecurityhubAutomationRuleCriteriaGeneratorId",
    "SecurityhubAutomationRuleCriteriaGeneratorIdList",
    "SecurityhubAutomationRuleCriteriaGeneratorIdOutputReference",
    "SecurityhubAutomationRuleCriteriaId",
    "SecurityhubAutomationRuleCriteriaIdList",
    "SecurityhubAutomationRuleCriteriaIdOutputReference",
    "SecurityhubAutomationRuleCriteriaLastObservedAt",
    "SecurityhubAutomationRuleCriteriaLastObservedAtDateRange",
    "SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeList",
    "SecurityhubAutomationRuleCriteriaLastObservedAtDateRangeOutputReference",
    "SecurityhubAutomationRuleCriteriaLastObservedAtList",
    "SecurityhubAutomationRuleCriteriaLastObservedAtOutputReference",
    "SecurityhubAutomationRuleCriteriaList",
    "SecurityhubAutomationRuleCriteriaNoteText",
    "SecurityhubAutomationRuleCriteriaNoteTextList",
    "SecurityhubAutomationRuleCriteriaNoteTextOutputReference",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedAt",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeList",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRangeOutputReference",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedAtList",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedAtOutputReference",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedBy",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedByList",
    "SecurityhubAutomationRuleCriteriaNoteUpdatedByOutputReference",
    "SecurityhubAutomationRuleCriteriaOutputReference",
    "SecurityhubAutomationRuleCriteriaProductArn",
    "SecurityhubAutomationRuleCriteriaProductArnList",
    "SecurityhubAutomationRuleCriteriaProductArnOutputReference",
    "SecurityhubAutomationRuleCriteriaProductName",
    "SecurityhubAutomationRuleCriteriaProductNameList",
    "SecurityhubAutomationRuleCriteriaProductNameOutputReference",
    "SecurityhubAutomationRuleCriteriaRecordState",
    "SecurityhubAutomationRuleCriteriaRecordStateList",
    "SecurityhubAutomationRuleCriteriaRecordStateOutputReference",
    "SecurityhubAutomationRuleCriteriaRelatedFindingsId",
    "SecurityhubAutomationRuleCriteriaRelatedFindingsIdList",
    "SecurityhubAutomationRuleCriteriaRelatedFindingsIdOutputReference",
    "SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn",
    "SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnList",
    "SecurityhubAutomationRuleCriteriaRelatedFindingsProductArnOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceApplicationArn",
    "SecurityhubAutomationRuleCriteriaResourceApplicationArnList",
    "SecurityhubAutomationRuleCriteriaResourceApplicationArnOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceApplicationName",
    "SecurityhubAutomationRuleCriteriaResourceApplicationNameList",
    "SecurityhubAutomationRuleCriteriaResourceApplicationNameOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceDetailsOther",
    "SecurityhubAutomationRuleCriteriaResourceDetailsOtherList",
    "SecurityhubAutomationRuleCriteriaResourceDetailsOtherOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceId",
    "SecurityhubAutomationRuleCriteriaResourceIdList",
    "SecurityhubAutomationRuleCriteriaResourceIdOutputReference",
    "SecurityhubAutomationRuleCriteriaResourcePartition",
    "SecurityhubAutomationRuleCriteriaResourcePartitionList",
    "SecurityhubAutomationRuleCriteriaResourcePartitionOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceRegion",
    "SecurityhubAutomationRuleCriteriaResourceRegionList",
    "SecurityhubAutomationRuleCriteriaResourceRegionOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceTags",
    "SecurityhubAutomationRuleCriteriaResourceTagsList",
    "SecurityhubAutomationRuleCriteriaResourceTagsOutputReference",
    "SecurityhubAutomationRuleCriteriaResourceType",
    "SecurityhubAutomationRuleCriteriaResourceTypeList",
    "SecurityhubAutomationRuleCriteriaResourceTypeOutputReference",
    "SecurityhubAutomationRuleCriteriaSeverityLabel",
    "SecurityhubAutomationRuleCriteriaSeverityLabelList",
    "SecurityhubAutomationRuleCriteriaSeverityLabelOutputReference",
    "SecurityhubAutomationRuleCriteriaSourceUrl",
    "SecurityhubAutomationRuleCriteriaSourceUrlList",
    "SecurityhubAutomationRuleCriteriaSourceUrlOutputReference",
    "SecurityhubAutomationRuleCriteriaTitle",
    "SecurityhubAutomationRuleCriteriaTitleList",
    "SecurityhubAutomationRuleCriteriaTitleOutputReference",
    "SecurityhubAutomationRuleCriteriaType",
    "SecurityhubAutomationRuleCriteriaTypeList",
    "SecurityhubAutomationRuleCriteriaTypeOutputReference",
    "SecurityhubAutomationRuleCriteriaUpdatedAt",
    "SecurityhubAutomationRuleCriteriaUpdatedAtDateRange",
    "SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeList",
    "SecurityhubAutomationRuleCriteriaUpdatedAtDateRangeOutputReference",
    "SecurityhubAutomationRuleCriteriaUpdatedAtList",
    "SecurityhubAutomationRuleCriteriaUpdatedAtOutputReference",
    "SecurityhubAutomationRuleCriteriaUserDefinedFields",
    "SecurityhubAutomationRuleCriteriaUserDefinedFieldsList",
    "SecurityhubAutomationRuleCriteriaUserDefinedFieldsOutputReference",
    "SecurityhubAutomationRuleCriteriaVerificationState",
    "SecurityhubAutomationRuleCriteriaVerificationStateList",
    "SecurityhubAutomationRuleCriteriaVerificationStateOutputReference",
    "SecurityhubAutomationRuleCriteriaWorkflowStatus",
    "SecurityhubAutomationRuleCriteriaWorkflowStatusList",
    "SecurityhubAutomationRuleCriteriaWorkflowStatusOutputReference",
]

publication.publish()

def _typecheckingstub__7eeb3ec78ea520ee4282e0d03beaf5d4cdf2f740d890c68a0c712ec029dec2e0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    rule_name: builtins.str,
    rule_order: jsii.Number,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_terminal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    rule_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__8db812b48f8db9f14e677047fb32de624a31b14197f1cbc6dfa688b08b374d41(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81eb622f813f07fbfb17b4bb88e2163fbe60868acebff13105232752a632bd71(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400c9b69cf6dbde6f9736be4e72275c9a9890c10ec62bf199a386f8ca71b08fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f023931f8146dc1f43a1b4c8282ea050c092ab8a51d4a1752a8a689ff1de4283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ebc14eb6a9652082c9df33c67bc66dd923040abe0245d4465e0a64f2f976cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44673460bfeaa91a7c4eb4ee7547095edb83b2831c58dc5750574e17062f1003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c0e5fff10ed6d2a772b02809ebff8ec603c3240130a4d9e8726f59fbf675e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cc7df9f6495445e940d7edec08f73e4bbd6db60982f014e9bf5128d184a6f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0927e90d0bd49ad51d4ae92114812658c7a5af1ce782f109a889740ce53d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573b98cb22c4a147529ad8d7c14b2c120cd3169c6ab40f04ff7e8f6d7b6d1ed2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bde57982a92d3d3ef0f29c0670eb9b4c73f7adb43bf3e579b69ee1e6919504(
    *,
    finding_fields_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62d737f838fbda4b759151bcfd26e7f9221bcba1c35abbd3da2378f9fff1e41(
    *,
    confidence: typing.Optional[jsii.Number] = None,
    criticality: typing.Optional[jsii.Number] = None,
    note: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote, typing.Dict[builtins.str, typing.Any]]]]] = None,
    related_findings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_defined_fields: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    verification_state: typing.Optional[builtins.str] = None,
    workflow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5aed5a102a632d47e9f9c7fe25900946e26b27ab8eb46b96f8dade1481c488(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d634a01de2ca55d17360cedaedcc7044e4d696c2209786922753b8ca9f50e4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de279e960f0025c69326a3b6e2195ac74acd79400aef73a14fabc5ec4ee05b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1180d290c5ed6ab75e5339ad60f89094449e86602b0c723d8072cafd808dabe0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456ce6888102561ca5622d0335af0537f51f2ca2f2b193cf3a642a41e854d61e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbf9080abc2ba435c7e58693449050a488f34f1eb9a539b868cee1c9a4b102a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f615ec6fcaa5e3f12f2a28ad4a41f4827266669299cce160e22bc9249b9008(
    *,
    text: builtins.str,
    updated_by: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8036820f61da81a070a17b624bb8e961c7c5112b671473b9daf6744edc79c3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a51f34232f5abb2d04cb83cc3a31749d6d8d682a183cfd1bd86e32e9c6fc93e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892ca25129cbb76f803f4a2013a4ecdfd6052b4bf00a081ae69431afffa8bad0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cc1621270f337f8a84b3aac81e54ed6599efd6b397509124bba3aa438fdf72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bc27488a2659515f5407f7f8e42e540a799dcc6a7563b400722e341e68b4be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67f92333da43befa3ec26c9f80b3f7f862b2bc342a1525ab7043567a6223d11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d35663b51111665deb8ea5b28b6959694e2ec7bce8e2b9ffd9d78b4a1ff0ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30cead942f6598b3197a4f2f9f2333b7a6088839d6a66891936abf82763fa0b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8db32fecd25a7a97b4287c42cabcc9d49f1dc08192f7b927c5fe80ec9f01f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fd43c486bcbb9363412d0efb8305007030f6ae8c605f8c245fe824f3147929(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateNote]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850a4fd62726aacc4cada00f170645c243507cdcd9fb5d4fe4cd2a0516bdb4e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67abc0df576459e5d99b4d8b40ed5ed1c29ef010aeff8e95e94bba5108d714a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateNote, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b404c0d1ec9a61f3812cb6caecf0c135e5fd3db3f4c65e1b8e1ce9c175a8272(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6e657b2e12a1e4b22e06da77e761eb60187e434b8d16817c15d5f38a33b35d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d59f0270a84bf16bec3b43c7b293ca8747c5b1f3840676258192061f7b365ee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861e0f915da6966f543511d20b233e8bd0479b618589fde17e64a0ba44818b9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe27524e682593fe95bc52230978e0f395242099639fe2dde5e9007ecd7962aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f513b880352f994fc0325d67d7353a67bfac4b239791eda72deb2805d9116201(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f98dddd980960039845e152574d2348338672f78dc7dbaca936f9827336251b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a151dd7688dff98488d725d599b793bff399d8349a76e537e0ed66087e20df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050b8375b40a5030e1a07528fd88f7edf1a09b9d9c63e835cab9e6108fb4b330(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bed1ce93a4cd8938aa3e83f1d7a6e284728cd8cb0bf87c41ba5a9e31e5794f(
    *,
    id: builtins.str,
    product_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75a43ae00f2aea7315f6f06b179f764b262c5d7a0bfbb943ac0352f00df4535(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a5042e6cc4ac41961fe521a37184577d10934eff8e52a8563cf2cad8d318b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fb188c41de6a7e72e700a90c2e9042f03a0819b542e05a2938d7c4f8f70e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e2a844b3043502114a379005130a6cf4eaa0c5bb7f0370d0d27a958aa8488c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb180bcfcdf6a4c0ef41e6d0638dbe74216cab4ab51e356f15d16b44e627f38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c536037b91ce2e4bc05c83d189de82953192e545617b2de63743151fa7f705(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc2507dfb6e68518b4f83ac7c8a7b50cbd46f57c7a3bd9d391c31544184011f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898bd23b07f04c60bd6ece7a20bdc66fa14f3cebbe0d042db3561cc9dff5cf36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0534f28977ff6f7943641a8c5bcd584780c791731aa41314c05d15e65433f545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecca1c3c571c60097b694a6648bbcfa615715062ea4afbe16eed3d0154e2883a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateRelatedFindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284f4affc5c99dba19b25db2f4d822566d50f0515a3c9a64d2d165831db9f017(
    *,
    label: typing.Optional[builtins.str] = None,
    product: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3010af418b11cf36d48d60b27a45b2217269aa7d5183471f40d4ed0349f20a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4830a2151ad0a46b1c3848da55a06a0961a0704d72406944447ee654d64b52e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61fb70d9c3f7e3513ec85557fe950761d04e912da4dc6208d7eaddb623601be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdbfd5a8aafeead42c77d5532654b2539c9d4b4803b61fe586b763bc18741c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718ad3b38999e8066126c11225147f19fd3912597174e448d3c96c1c3a5474f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef53fec22e40c1420ee891f47c425dd81e5b4df3ed2067b3fc9b53f064898435(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019db07d375dc046653122725d172eacba63baa0a5e97745d5d1799b66920c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97d2da293848ace3a0c14657c66ec21de0bcf7adf7b5bcd76bcfd9ed782805b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24cf0f99a1b3a38df1d5c226809dc1876b3a53fde00bfa2ec49a713019e878c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc72da21b3fc0c33fdbeee32b77294c983584204573ee5023bdd71bd13830fb0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateSeverity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec22c3555b05e909b59e4c69f8a5ac1993c42fb154780b689a0171c99f5cd770(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08dddd27314ff3d3138faf4e12c1d04768209d185f3db64ce75da6596b05e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b27dbf9ef119e20f1c0f18c8fdb345ea81b2ac1e8daa743e6b59c0d4336bf17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438c78ec2ff361d9fe9c6ece351ef017115efe344a7763c84145d944acec98c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffb65ec482201b330650e12029e68e8976caa1659448afbdc6e60971fd5497c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e3849225e151cac4a467e4ce801c87b2a25ad9ac2f05557dd7fd9ffc18885a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8998c45d53ac831783890dc38a128e02a2a3d8b54d1c31b66051481363d481b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3758c8641a8364c6811308bb5e79cf066d27c879b06ecb31e2dbf7315f2b21d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d6d7b25a571f147de2589f97c6746a80bad0417b5ffe281c984be895fce98c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2fa46735c3116ca9d6cff991388de6ae7001bdcaac1252b3f0b7a662d0f7bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActionsFindingFieldsUpdateWorkflow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae7fc6cdf741ff92572e8f7a6494b10e7fc3091e3e0ed48a2faf322d3204d82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41484329168b3370d0760f93018e3f5cc2fa747b4e86f4d9fed041bca1ff585(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcdcebc98ce6926b6f4b7ef5ced8f54eaecb06606cd1374dcbe9d9a27e3cc33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6edca70a196324ba09a7e6feb6ac4c4a294d073112e055eb97f224bdb23d9222(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c435b6498996ce7aa8321166edaf16f6f82f16f36bc11a49ae512b2fec0b0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af13ada39e8cb458f871400af5b621b44f95749613f30de98994df66e9d0676b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011198c8224fa2390d2af7cf4d0addae544d1b43c337db184b13c2981332b9c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf637b6353a87d3d9beed08fddefb4bb3255ce0d26644df3eee3f22f3f34c10(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActionsFindingFieldsUpdate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c389ec11f1be3b697f0266d7b2f3027137782aaea2b65ff515279b565c7f96f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc784cc561777a1076cff1b7d43dd9a6c3e20c0f6bcd4d52d30a63ff60f2a38b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8321edea23b5d2817efd15e671f4935364c63c2ce3da2ea636871dc89a9f5f8f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    rule_name: builtins.str,
    rule_order: jsii.Number,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_terminal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    rule_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b62d539f4de9ca4f8dca2f5bdbfb5c21ab3568550f39a8583fbb84fc8423fd6(
    *,
    aws_account_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaAwsAccountId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aws_account_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaAwsAccountName, typing.Dict[builtins.str, typing.Any]]]]] = None,
    company_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCompanyName, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compliance_associated_standards_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compliance_security_control_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compliance_status: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceStatus, typing.Dict[builtins.str, typing.Any]]]]] = None,
    confidence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaConfidence, typing.Dict[builtins.str, typing.Any]]]]] = None,
    created_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCreatedAt, typing.Dict[builtins.str, typing.Any]]]]] = None,
    criticality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCriticality, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaDescription, typing.Dict[builtins.str, typing.Any]]]]] = None,
    first_observed_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaFirstObservedAt, typing.Dict[builtins.str, typing.Any]]]]] = None,
    generator_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaGeneratorId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    last_observed_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaLastObservedAt, typing.Dict[builtins.str, typing.Any]]]]] = None,
    note_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteText, typing.Dict[builtins.str, typing.Any]]]]] = None,
    note_updated_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedAt, typing.Dict[builtins.str, typing.Any]]]]] = None,
    note_updated_by: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedBy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    product_arn: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaProductArn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    product_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaProductName, typing.Dict[builtins.str, typing.Any]]]]] = None,
    record_state: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaRecordState, typing.Dict[builtins.str, typing.Any]]]]] = None,
    related_findings_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaRelatedFindingsId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    related_findings_product_arn: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_application_arn: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceApplicationArn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_application_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceApplicationName, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_details_other: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceDetailsOther, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_id: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceId, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_partition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourcePartition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_region: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceRegion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity_label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaSeverityLabel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaSourceUrl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    title: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaTitle, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    updated_at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUpdatedAt, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    verification_state: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaVerificationState, typing.Dict[builtins.str, typing.Any]]]]] = None,
    workflow_status: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaWorkflowStatus, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990a59df2d40081a02df9bb34b8b6ac0a9c23bd47c340004acd2d021ac23af29(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcb3a1013f9a882a77a8e59f907b53cb156c90d6a3c49fbd6b86aee024ed996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e3471de7066b84794862a8071e4c82bc594da0d20f997cf4f5c06d2fc5dbc5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a681759164ca3b180c53c527aaaf7813a0c6ee9e4dde1afa3e7952414bf81e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2391c193d627a10e3800ae4d269d7ec912b89176e1d5215bfb795dd7c7170ac8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3c9a2a601ab04977ca4f14b1e1c398ae6531af7629e106375228cfed9e8945(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564ec8fdfd4ccc5a893e606c26fd2c83e0955ac08bc17d1f780b910a1aad1c3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a47ae0fed5927dd6ef48a1a063c2d13b75288dd8ef8ac008d3b60d8a692d21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712740cf4056ef4d8be75b5a403c3bf61827756f0d99a2d2522629874cd8e82c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ebc25b2531d4f95ad021207a5c34823b2fa5004b00680891eb0830bbc00317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64fe86ee22539858fba605bda16dd57c7cbb8bbe47f57f7e0bedf2ec7845fc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c3b438d481ca82df63dabd5be65088254781f23315d996977f7f9a41755b86(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbbba3da11c8c7849b3ff8b4654647d8c8498def3eb8eca43ff09c0d4e4de8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dcc1682bf92a8bf7048c0dc9abdb5de753a0f10039c2e0a9fc828e70256ad7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4af37298d58ef4caf6053ae28ea6c43e05d3060b7f539ace1d677b41955ee45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab5c46242a960a1f677be18cee6a01b7913d171d9a513672aa3deb3c02c5ac7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c20ec0a90cf2be67fc719c0c02351614bf3a6c325e771beed7f7fd05563217(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236a77141d94e64db4376b2e8af891f3e0f58254ee98849562958759c5335a77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaAwsAccountName]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a02758425fb712bd9c7ef025891b66b09a83aa2cd5b188e7e62a27e5ed87e19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270dd72816945c6a73e732408e16d90ddbfbc687eb09e3d74c7bc26c8d62eb5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b074ef1ee901ae5818628bc3305a4e416bcd11c24da9534e6180529dcd27fc5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea2e6b3932f9dbf4cd13ebd9edcf5922208c0085fecc311296dbdce579cf95a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaAwsAccountName]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab2cc74969507f2d9d2d923cde5f9cd9bf77ea4a2c5f9fb65b4dc4716cbcc50(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681ce5916797e65862762f13226449b2d609bc49975a123e48b2f3d62eceab26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c657747494b13d09f063f91252518be3d710ac827876420c3f4781605b4a6eb3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021e89220aeed679f527a883e68d309611d6ec63ec2a0a8204f566b2bc1c65ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73809f6b3c4be37e4ad186f3d6c1511533d070baaf54ae2659d6c0a06f941707(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d35b03e2eecbe7aba622bef569950208ac689da64014dca63a44c050c2ab2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667a95636e860ae2802fc6e73c7a0d288b550ced154e09751e0ede1e5f9c5c96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCompanyName]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a23cdc9a74ff8651b1266e70cece9543caa640c488c14e76789ffea7e3c3810(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f489aa02458c2d01c49b09b67486d9583d00c0ae7fd6f18dc3d17851595f4bba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aef79471696ee6848b7fe90083dadb5dfd5e2dc0796a53479700cda231152dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053b18ece107eb329c9757888e4cb3f286086158325e5e5c09853090f1311ca9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCompanyName]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3248a66d82ad3755d784bdb04a476d4c6a1039b7e1b82642d1916f7b36f39e(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34137fde73741c9a84dbbb7fb412e9583952a7b9bd2e4a87b712afa91812c100(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9328ebd7058aaa719810512e76a3f0c104e2e9c9c9ba39a0f6f3ed951386d19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202f3cc06c0e5fd867298bf82704d18f1be233a22087d5057524082d44be5baa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1ca34c77fda329a81a5d3897b1f48e1d61acad77bb8d4cac0829c9fa7a0683(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522aa65889d3b559fd949b0321bbc9bc25c773fdc838d0c843aec625d10786b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f696a5feee91c6764433d658d4bb5a6bb95e8e8a31ae7463d45edcbacfef3a4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b9f2b6327c568681c2b78fc2581c5c5141e3c5605dfd6b5df5f7830019c34a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd8e56da7118c689f6351397625638139c1a95580b24be3939625fe1fd1a3d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5b26ab4154e8262a3cfb826e1cff8ea72cda67df85f9dcda8b89060146b285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b62c3edce8db05aeb90fd64a3ab1d59b3066b8fe5e93f8b7fcce026053779fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16829c07de7ee297804134d47c99451c94002890a638ea3885b5d8d952c5b9e7(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9865f5a021b5cfb946ea9b3160c663ff95eb306459b6ab2dde583b321b6d1e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2ba0ec6706f7854182e72544805fa278c59ccd622f17a7fd7b0fcdba9e97fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e9d0d7afddf58b850eb43e7e70de788796b21411d2f4a98f4deee8a7d1b54d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbaa3d2a004137318690055b4191364b72aa3cdec354444edd349ebab6a6101(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7c935981394b2fb765763893e56bbab94b49fda3715b67391f6d35d7379d4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed2349353f219615e80b7d550ff6a961578399e63fd8aa4c993f8b7d0c7d9f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e943347488487d3877ac7c3f772f3437d7228eec33abd2ffdc42b32a47bf60b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f97c0d2e832f5c290fbe9c4d7cf5d76c38f30f6eb0080d6856bd63217c0d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4399de82f471a4a3050b7a874079bc619964c5f3e9ba5238ee0d12565e8b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4b9897587da42d86024771bffeadd960e9bd16e32c5799ec10fd96fe296b24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceSecurityControlId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d949f2a852d8945ff54e770fb22a29728d18c991e9341be6017174ec803b99eb(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16242ea3430067447a76e75e9b576bd7182dbfbce3e3f300155ac3c1169468d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d70263455d15d0ef9ea814589b0243ebbe3810c7caaaab0d33aaa2944f4428(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31e884f16bfd039e51c40a721bad4f22e0feafae0031411f17600c4dd35eb83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b173dba24bbe51e5381fbd7d522b59d68159fbca6e8a0dbb58d0b5f1e7afd29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1fa5c84226264d774905a48cb214a3e8e25edcb510fd753f0ccd406a52ef01(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4813d2c866c10728ed08486d6bbdb6fb658e2a9ffa7fe00e178b546562e282(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaComplianceStatus]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b8772f7ac64de472dab474526dd40b003de23c7d46b4b670134d450f0a5db6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7edb2f57b09cdfa6f646c08159331160943147087fa0e53a70b65713a908d9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0283ae1b73c317a568340942334b02e327e727e0e4128e079c3c76f80cecbec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec2ccdd0e0334c9d58800b9bf237052e4c2a94436121bbd7dd7d67952fdcd6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaComplianceStatus]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc903b89cfd5f820461e611b21e45f6537151eb63ee0aaa939c99469a25b3631(
    *,
    eq: typing.Optional[jsii.Number] = None,
    gt: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    lt: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a233f5c0eaa005ce78a549095db411ff7a9f2ec32121d45609e04a987bb7bfca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9202ac878ddcae5e82b56658254be83c94abd31679e82a2b24a303816a4d698b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19358c26d270844116cd89679ad87c3e880be16c5a74ff4a2db861ee34795c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8324835f94ec376b41f6de3ff866e7578b9e6038cdfdb02cfa8a3787d45e48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418257d464565113ead1d448f5837113476f86e1b0dec856f3d158c8fe0b7feb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b603569d7954cd324af788913730e71f3428aabbcb2e9ba203f97b0dab5866(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaConfidence]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83998e744e5d39aaa635d5b98e4bd1bac030799752b8e7196b78a411b9040043(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5be94dc3e1ffed2f5362a3b420f4ede6b1e7fcd85a64fc65d541e6c6edd727(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636795c73a3b014d6a8fd1c423793e7ead1ec761c833f07a31ad18134755c968(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b27a13cfc3b765d97132ae713a06a8e5216ebf72beb8c974448b170c2190082(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2dbf4c20d5bc89b4738c7137ebd62439d1487612810ecd2bade659d74f52e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33ea92849dc994070636606d74765bcac2d498cccb4c91c697ce2c044942552(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5551cab8e6a967989dbd7c20b663a280f33fb7acb7f6a094185694781725105f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaConfidence]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703ea6cf93aa6e854f58425cdc9012db4e0dc0d1796d13ced3494c1302f06a26(
    *,
    date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCreatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f60f050a679b2f919321afde54cccd9fe6efe750159f2f4a448eb834e90b706(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f888d31a4d11f55e081a9e6a26fd2d166a9da53619fd112baa56a23b7265549(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc7e2ca9af72466d4af287f2f3b068300d3d315c4d8486c01e00519af6630ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538447f2b4622220cd794665d7942a2fa8fc51f77765bcfd4affd8241764e692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2483b1f8b03671151b1a0da26a7e300d1a0574f7dce37acd2031c10f1b8e70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5341162baccccce2dc4038b3e437f19319e3eecb7a3cb97604f640052e32748(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2cbb66fd54f185bea6d93c4c1a10c8559535c9e0122bdd59173291e2805b501(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAtDateRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3182d49a7eff79ba8bac8898c365aa948fb6d2317d9514bc2e171fdf1d838cf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f9a30f82acbae59face8e2cf9b4a856b9771ec6956ce3972636a0b689a1ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e1d70d2e74fabd47481c36c30847e3dfe29cf4732698fa83b1cfefcf6fc584(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3296df6f4a53121d6bbaf8a19c9699c46b7b5b3b47333b7d4f1c61ae6d42fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAtDateRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d84c300c1511a2d6aa32c0d105d04c4fd149040393d12954055591bfcc060ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca631aec72b5931d40ce5bffd9f0ad8e98e7927883bb9c0cc46eaef39aec9354(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa6c419d084be76e779229bb2f6503543785705918eb318012938c313312a0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3a1759828c5074bfe96d9434ae7da3cc3100d142782bb37b9b93246e0a53ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b464331b895f69a56b3f9ed4dbd529cef727adcb6d685b7f1e6595ae789d10d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1d28a38ae93e5af38136e9fc46fc086cfcc934efcdd01d7d1ee53675399f80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCreatedAt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21be4d01218a09ca64d1da902685caabe720181607066b81c1ba94674bbe3de1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a04fe93a7f58de7086fec7eace3c57325a27ef2da3a5f7d8694714957581f99(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCreatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f528441dd42588b3cf67b993989cc062e50b9a9b06b830481adade3e7cfde296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181d9b9505153d1dac20edb240f54e889d1dd3931811522b2ee3f1b05090a55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840e7c48bb61c3d75f53abeab90a92ad44fdf493e3a9fb916f968b4f8ab51ba9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCreatedAt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c667e12f4968ffb040b1d2c938319b00112d21f2974d19ebc1abe71e38584bd(
    *,
    eq: typing.Optional[jsii.Number] = None,
    gt: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    lt: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f373861920983adf7042c32d907d980d433ac5492d3394fa8a8c77d144443d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b97b9b7ec8067ee38db9c18df2dc95b275ff1e6e170176c8a155ed5a7fc3a1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b60ab02165c45daa485fbbeec4f4438fdd281515b128165056ba45402bffaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71bf3d5f5d6d89346e2c408b42d10d41678780d0ac96c8b32266b1800c50d63(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af8aabbe41978a5b035d20a1c1a5b11667d4f38786b5e930ac26ae98154be0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945ed3b33595dc7b0f6698a788d7ec51ca89be07826b80d5a2896e66306261de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaCriticality]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482e71135449136200c1267b9a463513986e1e1a19e4ce88b17812813abefc8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cc7a72e7884937a76c28efde1a791912ec44e2c4afb9116f2e1a870583b9ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30eadbc5cf896f104eb2a67892b19393561e1c73181b7f8b5e77d71fbacd1250(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e7cec4d40a4b347334f7f7d4f36863946351fecd7bbcda2f912e1171508f50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ca2a99f703a62a40445697f14cef3abcc074c42d6705f5d2eb018aec7e5497(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f6ab918a669902cab257f221c9a40790626ef946f5fba7a0fea8885fd6186d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b713b1850504152ec9651f7e7d666bdf66979e73701d43c36db38666259302(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaCriticality]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1956be046d51069cf5ac014a4dc4949e3b2b1600e5a3e13cc5e479f9cfbc0f6e(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38cabd1d1242133f1a4005a85f27620a0ff1e95b11b842f3ee6eb5fff2105f31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bceb89af2e6cb80cbd4908e4bbc9986ca14b0624275661205b5c065ca6cbef9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375605ab9a15d6907600db1d80a28b466b3637de0d30719e514439994baa4891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb61833e9ef470da7ba653f7eb0b22833b193bd0f2b988a3aa125d05bcb1e7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b61434130275de0e5ff328db1d36914a414f35e03e5145bee2d903f5b9a781f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf5519a90eebd7edd2b28446865084d4668afdd50f5103062cf8789272bbfdf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaDescription]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5947be57611479938098ec29065506d51fa9ad453efbfa47e1db64365ab265d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed153a4dea9efedf69ca35ec07e9b1c44b6eb08168a9794131db60a3ee407ebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e691092b0e62f02d7235241f91524ff2e908fb5fadad3c3ea79065e9bfe9828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678b3a495bd1f40c57f43d4cf72cb1444466756d3a5b109efa136e743f3fd152(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaDescription]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3aa3b5a8ee8055c62a2670ac031a92a03f00a98d3ec3d06ce185bc315bc8db(
    *,
    date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9fdecdcb309e34c6df979727ab5c19b4fea101c6128a462f89e57dced00161(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ccd6b1e66875daab17626741641182118136f7e010b5f2059e6f763d396a60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421e425d36b9d9b6ecb88b186ca229d7edfcaf16140aae6cf5b23d0d48b3ae2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430943f815ec88efb7cf5601b600f0c9b43edd44e9b9982c8ab8bfda8b5dab23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb621cc0cb98ff381faa7b569ac217d1284f0129b0dfc333a1c2fdfcf02b60a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a81a3d37d4cf368ac79caec0a52838ee06342662ec7c7dd5d2e8826504cd028(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f2824ab6d67b86fcc3c47b9ad56861c9d02cb4ada411c97cc4632d6b31870c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9964f54ab4c1235c4f6fa1ae38a4a5e3d371fff0a54e5b86a508a074b7bdef55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a346aa556a487ee5ca4238b4ae16634cce862ce8ec591b8d8659d6ba2689da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12a62bb42fdc6f2f9bfcbc76177853e079ce3881991e9e040974ffbab79fd64(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a08cc06f9751400bcacf9f8e6d039860d2256696ba965607817fb2b629a028e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5140803febf95b44b87c556e97ac6831ba0dbea2cb92d43cdccf7b9a70b89b2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156b4f12013d29ee87918b3992516a08815fb7eb47be2ccbb37cb90a8af961ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b158638986090ac6e691007a773f09bfc7cd2d43e7d7fc4658d47b9d15acf99f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514560fcaf9f567bdcdd56337e4d0c842d98901dd562ae4a743d17d6e33be9cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720d93821ef575fdf411f339eb81ba1881a79f2e2ed213c100749666473a0fe7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5efc0f0d723eaadfc0223ba1ca15934614447f3b15759e280f9e8ea5debd2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaFirstObservedAt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6a17f98370716d07f919f28cbf67f9846c58408acc65e5d0aa370f18cc45b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2bdea5694d626cfbe56bc1f4ff09bdfa751d9d72b223245fb9571dbd3c42ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaFirstObservedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2e6f57110df0febc5df02f58e05ff15edceab685879651a19ee53f35199cd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451c7589bb40d3624fd4b3406185980c56d83118392f83e49c0a2db1259fcbcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624dc6037b0483606bfebd2717ae7067ff084b7acb8cb3c08a088d6516cc484a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaFirstObservedAt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f3ca32c96f3e0d6f171cec0679bd8df7b739cc3d78011c34714bf3e81a53bc(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd11ad6d2d9862e951cda0bf0572e90f27ce2e50edfc62a7067e31622447ac6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888dd2bf54447d4fffed35f9f1e3f86272a60ce939c4766037a9e0697ef67768(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96180b701f7717c22e6ef735b63d772c3ab0e6e25de8b28af903f03799005ce1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6ece8cedee653a6ac1e1198deb379010d22429e42d39590d9ef49aeabd0a98(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3be894ce610daa4a4c5b9de6afc351256c67ad20f11851e3b588b53e27b7584(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe2bfd17d37fbe3e61e31f1dd757e2618f8eef452897e774e1b10c024add975(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaGeneratorId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc581ff4c31fd41299a210362236482b894006a504bf1dcb0a445d5e06f45cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8752c082411499a127abb4229d80feda48fa10ed5d18bc657abf760e65df76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5dfb2042f3b923a38a78011faf27fcd6f453f61ecdb2af7033e01145dd65c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08ea4efaea1d81bc3fc2af1b0a912082a44d1eb1cc9c80000073bed33a71598(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaGeneratorId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc34ccb0aac97cc5e01129361c5cb3adf5eaaa6543017515fe609b37543476a(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43019b5461e4ad3aa3f33195e5ed37bc7066003ee7500d220cf964f47de0df8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aadf6f8b2abc4c5ced07e21a09b3c43a9129edbf54e9955578d61dcec68c1b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a9aace32ed9ff7c7c4db28670cf9fe8314a290c698ae4a6d6080928727c78c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0fd9366fee2bf06fe6a874fe707e4953e1df51301d29a65d0ed056b9e142f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5665fa0fd6193328b2271fff05e2cff246a35fb1f35ff023cd70cce3fb40408e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a76e24d4de114c685e9bf042f44cb52be6701fabf534147b1cdb424fe686fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00ec62b5ac98d87da3b87a93edb48acfae4023ec0014f7ebf2fff68e0ef9359(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac437a79713b671899ce861ca06585f783b2aad8d4375bcefe9079f242b072f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ed7d03f94be8249f761f36464b1dd05e2beabd98e0426ac9e4533409c66b59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765b39934308569b12c490b0e5d44ec28dc1898f80a9826d0969ade7a81b249a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95eb2ce9e8caab421998cfd525235c724667c0b14e4680c2cc4acd929f6ecd89(
    *,
    date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb196058109f51c9f3bd87a847f3dd480f1715e456cbcc4cd6308dfb308b7e3b(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48944f3e4ef1ee4254e2fb723caa80d53f1fa55704076369c427e9e204caa790(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4c5403fb014eb63f95400429811c2b8b7562be8714ba4e34589946a6591e1d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac23d645b7cf869f22206a41f8d5261e740b11dfe69f3678f51eb27dc402173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f94ad7dbf8bf30c7d61a7a7f1fc53e45959b904c34cff73eb84ef0ae445e24a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c674410d694de2f52889f73f1b98ba0ddf0ab4b4c510991ceb308303741e4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8556af9127e0f846853fba8dfc2b726cb73b21ee3864873dbfce3972f088ee30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f0a8a19e074124136bc70d8cb0c897effc81ea4d8acdea16f5ba3085142819(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433fdcb91240b150ff243cec79aeadada0345496e9a814c715b603a83efb9f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa92eee85ba52b1ac4cbe84f9572304d3e867749c14bb7559639fd7a54d5a862(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2290cfa461920b87bab8456cb78ba0cef6aa17cf2163fe3c5a7782051220a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAtDateRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464a7cd324114d23e7f56641011c7f789470f75299bdf3e9c2b15161c6d9f7f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7217eeb0b1e52db6655014af0e00b10b3e8f51da7828c4fb3cd1dabb02689dbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbab3a16d22ad7f1735af55511a4e60611d1799662222f7df74628f28b257ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e3cc29bbe4b5c46a2ff8e84e51cf45deb5a34f950395226d618273ea59c7af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd4d7002bb57a073005840dbe228241f7ad16269b6b5ed4114d2ec69a27a421(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb93cb0c024ab53dd984e6aa193e1bc45e7a2957413031535f195b128c1bc24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaLastObservedAt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257cc60f312d3e09dffdcc76f41280c52220a257a0233c2fa9c33d9cdb5c5751(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a4c75e9a25d9f19191b313b756ad2cf3a89ba1164b33da2910f0db83a33dfc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaLastObservedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22a8d82cbb72b13c29b762e00888222e1a1c00acc83b9f7627a79815f67342f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b83358332017696f40183aa57cc1f94bac3d13b59dd2389612ddb238e8a7b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c780b184f32dc25a6d9972e7edd90cb33cb8487fef7ac6bcc1c39fb927ec6afe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaLastObservedAt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dbe44abf4e9f68fa1d7a54e75d40fd3d450f2df0c98c01cc958b2b1d7f1121(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fe9f04a07f69a4c750825798a01a5ec73b6014d877602068f584f4319be314(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7da83f4d02da8f3e8e2c71f5c6829b5f32fa5a49e4123380525f8de1a01f25f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c909344cc775ea62bdb7432def7ea2901ea0f070728cc576a09829cc4dffb32f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c473095a2ef711b2cee708bc37a3900f1824acc7a1c00ce5bd8fcfdd5f985095(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d67c1c5c669afc1684f460d1d9e67fd6681000dcdc384e7385d1af4068a103f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927f70870dea57c12445ddc83d040ba6ca41a0eddecbbd11ea0f99d037a00c9a(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f72f4879be2ef4800e6997c7aa2cec9e3a644147ed36e885d41a0f8921443f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcb2fd4fb2440a84d4b14dfd0c71aea537591edee36d5e5e203246f8c064b3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c589c0d7cb5f78a420ae078147cc86c849f869793cf6d14b299c5107e9977b94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460518d55f5adb6b292dfd98e4e6908abe3a9dc651c68a1fd0c9ceddbb698003(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7a0f4c3c811943131c9d2045097ac2ba663b8b26bb1f24eba01b522043ecc2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18071a7d1d82a59421b55eb2ef73e91134d7718d8363a37477c3d0f7ced060a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteText]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1236c92510e391a4235076e8ca39a24061cc2d114284383abb456e5201b16f63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cd468f8bae3dfac62dcd116fa6b77ff657b7acb30e2e0498f21e8a439f51b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8163c274c3acbe23dfcc2c7a3eac10996ed51be451d9cfe99b4eb62c1e4c025d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4824b0857d665c4d361947268e98b24e3bae5453dfbb3ee7dbde56ce1b867b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteText]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbe5362796567116360185213fade95a858a3359d4345d29efe7354de2071c3(
    *,
    date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d28c5e121e0342a10fd4da94a11ea3c59df3a3b3b3fd7dcd19e7f7f7b5a3b81(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdf2de0465fa48e908837627cfbdcee737e8a2fdc8296dcf1c43b7db0e9192f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c1b1648e38de55a3f239a8669b9781d565bd4c147cb87dcc5ccb0ffca8105b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d356a0aca029715d701e55e1702004242bb31da6c538b9709675b8d157da5454(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e139ae8fb4fde83a254dd0eb7d23d694bd0152a43adbe96715b4b0e5b0b76cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6be151781c90f4e3c402c7969c6f49165f33b9910a25e2ed78a58a9c3286d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f734301fd52581ab69e2ceb7e7e380f55d56fcab42cd68aedffbc4b532c531d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2dcb7f69bbe92e41ce9c64ac15dab87654bdd04e35140052959e423d8a41d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ade993a0aedad3baa53584bb6832453f04b4624e737b4695e02c451e6038cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adce83ff873b7b3140d61d366bdb3bcef9347eb12f64b17b531a0ac794c4d727(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ef09c469e849510814342d6fa1c931ff603fc726850041ad754c508758b743(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406dd73df6e6c53d7471b96fe4e1f8212ea0ae223c45247e5967e03f2c19ce17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7809cd5125561f0fd8e5380535479e7f641a5f36a22e66dca02962e0e991c325(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd742bc2c9c12b6f1a911685036227ee751264badbc32c10122cccaecb2a356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec655f242abb0a858ed4bc4cb28f72380d234a03775d47a0efd172e033863de7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849073bdffbfd70511766418df3e01429b241899a9e25815d0eeb0006b3eb7fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb5e553e1dc3eb84ff127e0caad7320561678e4665b06e2b579d4c41559d99e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedAt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d77db68ff1507adc9f5ca3b3a9334a906473ccf6cebc8763d6434f48f3ecdf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83333b1700168dfb43f1723b071cd23296c41e3ecd8330555831587063d4408e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b3da3c1bb8b1934e80d78c73e64ad894c0fdee0809a93811b5cb4f2034c315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e23e057ee17eb3869e005ebf830b5a8b50b34f026601bb7774a9847af7f02d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db52cf48c44aeefbaba0f635d085b6e55b35be1217dce6edfe29a99ea3cd967(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedAt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c392b7b9fcb0120d670e5bb2d426c279a7af4b28c3ff2751ca3b44129e10bb(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb6e1663200e7bb7d2a060b002230b4ff3daca69693947414c048e84536c10d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298c6e45f34aa79cf1970b37358f467ff22bbe462d287e8d91d1c817fecb8066(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea4c9175a80c6d32aa9de92795470fdb1c858d34cb881f9e965aa75b5398ecd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef3020a0719415a97420453b8c8439beb740ed3756b0edc40f39a7c1742149a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0578ecfc58b2ea5e80758f676d77b69a6bd2cd3c122f9ff8bbee1b48ad607175(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fd0c54591b83647206047d41c14739e40559b692076cd7cb020e7b8eee5020(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaNoteUpdatedBy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef2ff72f4a853706afce722505ff01e3c8ef7f4d5800d6516775e317d365800(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df909ea6863491fb350884b5e51ae3b270991754363b57a4cf3039f04f7490ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5e5852d831f99a47363aaffbc0ecf316a9226a173480ab3603ce5a208bf8c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b50a66ba71df9d42cfab593b3699d975eab7c4f2e0565ccc00b5d3f3842be14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaNoteUpdatedBy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdbd03ef1f63bc8871bb2666c7b2bbafc050d90b993845a7721958b2fc51577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60fab7752add9517459d40173f501ced49c775ed74ef9fb9d19835ef7c24fd0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaAwsAccountId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87911ce0c9ad29e4bdf018e6e6879cb412082c34becbcf3839dc3ec8798190d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaAwsAccountName, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbbaf50e08a9f573548f764f0be37cbf1fe7cd9349ea60b26e2c09d5264baa6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCompanyName, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f29f958f41be77c2a956b13d1a0272b4319b38d441f8821ebd1514d0a578fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceAssociatedStandardsId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d07fa0f98eb9c66a74a867df6b50c7134b966ad05a139de33402f00e281fd9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceSecurityControlId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb71fe283c549a4b3810a1209148ae1c6a9085ab41b2e56f22e7ce4500453be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaComplianceStatus, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acebe9da1879ecba5fa61e3e78ffb65a85b5aa83770f85addaec7b7fc921cc9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaConfidence, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2f70319edf5e05f779691205ba64b32f81bf847fe58a8c777a1d78993a475c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCreatedAt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb7d31867574f5fe4f6656905b640a084a1f62b197a96ed9ceefdb1ac43d8e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaCriticality, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6bf2c83ceeec5a992b1d5b5cf378e164454388484784608ae2b108a9ba506f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaDescription, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb07696f4b5817f715c3be7097ef4ac51ffc169048cbe70e2e778ec0a71455ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaFirstObservedAt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987762528d8ca5783e7662fde8da0c8ce301cdac3208de988518b9323e4c94af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaGeneratorId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c0a4c764d63deebaf60becb728648f79e937cb65f3bec30b10c33bc351681d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bd7e2eb14aacde8a08516ea1735aa4284144c287f0afb9c2cdb8a1fe73535a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaLastObservedAt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501547fd9fb39fcc6f20c70d849d198ae24195bb027b173455df5da039b22e36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteText, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1495266092da51b70b587f9f0b3033b609694f1e13ae0067d7552569b0f29ce0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedAt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bded19b4fea44623340003d54acd0a1aeeca520a38626ab8925eacb6ccaa4c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaNoteUpdatedBy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adab5a710b8741d73978010ffdd9a57166d75500f8ff6d0bb27a368560c9594d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaProductArn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e874f66b50c1b3d78723721207780e4134b1ca10db2df0dba90835dc022e3e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaProductName, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d20bd4c75f3197dacb681db62057a59eed89c92b4d86167a927fc1e30663908(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaRecordState, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1714574da56f87e00d2539943224fbb302fd31448e07e8ba3b8c709e157954(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaRelatedFindingsId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00205b99ff8c842173442c9dd80a19ecf878d07755cf1e7d5f28eb740ceaa17(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146fd7eb84be80c7706eff64190b4f923e6b6578777737b6c89b42d950d33b3c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceApplicationArn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e316e678e1249b4fb778293de3722c6cd49f84ab3a0ed35bc66b15092ca8b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceApplicationName, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5388226fd4531fec6cf87c5d1d66bfe223744960ee8797cb25b4df7798239e90(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceDetailsOther, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b963cbb721d2f3d8edbb87f76490f1ae67c9a88704c98a459c2fb7a69956d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceId, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f333f4718094d8d9eed7e1bc7269e0146a0e240ddeaf8713e0e7f71e96b3a16(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourcePartition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470fa56287cf1d5574f14443ee49ccbe30726681eb173c911d31b0010f97459c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceRegion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4563b56d4ecc95ba0da6ef69daa4b4b8b0fc968804d9aa4df8e48c0937be4b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198de3d2a99a76dc994c113c82f9c31b4ac6aba801e990f5fd6515e86a0662ad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaResourceType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4307d798b7dbc329ca731411e934967986a00eb88b113521b49436f06313e53c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaSeverityLabel, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8d625fff5944387f397c19b69e934a5c21828dfd146370e4ba5684f8998c54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaSourceUrl, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae2d723184889ee3e9ec8d29c082121c1c82eff7153d9213d938b68319d7720(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaTitle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a715e893e8a00c8eddd51b6ad92f917d4f99dfb2ec25247eccb5864a92db24(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9900d08a032f8f8da1f1f0545ef55cabee7563b49e8f698c5fadb6c62699f686(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUpdatedAt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125b8b91ffa5993b1442f7de633bc3a5f4a662b7559ead61dff4c82bc0b528f5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a34365832328ce98a0b3c970697ba6d8d0fdfa56281339d0d7bc70a0ad28e54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaVerificationState, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f114fafd25aa2668142af20267fbbacc6ee5f5591ab8e17ab04188c159e308fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaWorkflowStatus, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee07d2e693931b221fa288f56ee995bbd43f47458142bd13acb3aa8d12c9d1f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becaae9bdbc35675f019944ceceebc4882e7d86724339f60356ba654030a8efb(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495c6247ef56bbb2437d1a7a57531a97b5a22659e90f5e9f4fb1bc441c0561c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42520f0fb6027055a5025248af493a809bdb2a95931da62ebca1af0dba004a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64735ae34a615f57da7cb2bff66c9abd4c2acafada96ca09472d35d8b73ab96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab78eaca5561eea9be5c5582726c1054257bb38d981ed3c1e86f57041f53b52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346cf42abd79258432933cf4313f4fdfbb78115f33d0b276772f2f50369ee5e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf3887bb2fc2b2d0f4ba7193c967027e58699514ceb14597f0abd4270c11dc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductArn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abad041d96ecfde798a55f23885ae646601b46582b3d5b6bfd7d45d05ea813e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb713b578f447ff8f9e8cb6110ee0af697549982741bc6e8b812f59ee4e1429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c454b3977226c44948a0644bdd34fbed79b3b62f3100ed8fc1bec66e9cc3a519(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ac8599fbc323f6825e6a4c90b3f27ec6b19321b9e91c775b95d026ee1afd43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductArn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff34be70c7946e1f24bb08a9de8f8ebeeb24a0ac502702c09d2e5a69afeecf7(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9585bfbf503fe222c0fbd6fbbb87b60cf15b1c88b6d79ece9c810c05da9779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d2f2cfa25356ca6392bead0a9ab267e368b7dab78f5d35c97760b7cc13f0e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3454b1220040e93879c9d853523853e52aad4e4710261affc7d493d363e05743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714cba70ccc02be55cc929a71ae80f2894369997ab55187a459750890877aa43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e103e104180473b89b87ae3ca73e5f4d77a4b750ac5e5691071a2433f4994303(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba215490308e6d0e5049a918edcb9bc6c2e30d370890b77ed1189e5a6f426ecc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaProductName]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda93808bb98379aeda7558c3b9455c143d68f18ebf4347095e1937cd13d9aca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70936fd69439e6f4b3c995d441ca88e7571effe9308b0f884ac4375e91ce374f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81d499008397efcb68975e0c94b40f03ed48498fcf7ccba6917b0bbb05184a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be52fcc58b7cf96f3f0adf70110bc4f311e86890e2f852289a7c335924f1b8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaProductName]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4ea47433a92a91082dab8a8c10befc9340c557388df5a278034a13a6ac93d2(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3814748ce62825347d572ee20eadd5d14c31c2f65778dd208000ca3e78da25d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8207982ce3e236eed57827d771d3621ff265e2504ea2a37f50b122dcde5f7342(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95d6cab57688640f5e7ef860326ed1f354e7d781345774e9d46bfbf2283b6f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443d1933f89374b776f6380f9faf5151f671c6f40434cdf2918da51644db1a64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9874abb04891a075a13f03c3e27982a5e2ebbda72a7811e989ee4ce4eca7b415(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55f0164597a8bf6445cfd98be24f05fe9bd5cddb74eec462ece9f508a11845f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRecordState]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac98d3a2981ede8ec7c35e54255f3b48d7e87f5da49cca3a488b917ff6ca93d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b850cb2155068971fa80855a61504ab914b5c45b032c8a58c73df8e6ae052af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e225bd04821431873032bbc07f9c9966f3af22b097615a6ad03bf7e4f7dad23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ad3fbcbf0523bc01519408b2de805d80ce29d9ba4e809ff5dc5076829df805(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRecordState]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29a67ae72d8c36505a5d859701652616410011db6e5fdfa9010813f3cbdc7a4(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806aa5beb6a15a4b5b235da6ad2427d6398f1e8f5fb479c04284431e3c471fd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ccf4038116757230cb3a272951403ca8102bdb7a62184b5240d5f7512c2514(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59de4757ce5527da414579c6a483fc79a8f21307e45569e1ac2467f8a80aeea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0781feabe4a05ff799192aff8392a1223b8fe7fc4430affa1d6dd4341d79746a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d1329a1a87e934701c5ac78917e5b8052ca49bf7b12825856e11b20b6ec1d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4aa14aceaa20a604a4269a508ccad05a39e0ed9fd3c400c508cd8809ccf35c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27b3c2b412e18e3e5d9b456ddcf191b485bcf4aa17db6e05c5b05d1f59a772b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ac0ae644b7bedc5722d183aa257913c9eb5858d9d3e95404eb18ced4344c03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b609790a22cd59465e7c5ff9dccac56d2a482c25baff57386ecf806ad55f554(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4f4c9d2fc280846806cf4585b42e4c7a3afcdf158050f6c0ac9f22eb4eb175(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5902d005eae572599f72a2acdff454b33808b77211a83d83bdffaf767b1d5f(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6aa0137d57a8bc433238e3879cb53445cf0d00b583c1d68bc7d72a6a7c8d4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d511df9f3ba56f6d651ba8e3096722e73838ffddb6e5ab916f58c0898ecaaca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0d77f044e3136e3b6e8af125b801fe2fc3d8d7ab0f81863ba1491945661b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52cb420e63d71f4424f3db860d3c9dbde4d0bea8dc3da6342da89956eb8fc00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e823741052dda71ec0761c81dc3ecfb70e8d8eb966902912e18b1e4f72562ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799ab364afdec6e775217a4645b00c529c8d0cdc18800cc2e4009d55cfc356c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cbf0ebddf508b631e8ce53524f4eda6c0e00363894ffddf774d6f2387301a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4111133fa261701c12e3d79813babf22b8fd8cc29d91468b3a68b280fb778be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b16400707e9aacc598fae8f5f90ac19d1c7800a00763bb200fb96cf701036a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739d687a4b7fc697b39f4d170db8e796b793f6e55e8c49550bdca53344fcb213(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaRelatedFindingsProductArn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c0ece931a737d74bf60f1b81ee620de4c58edbfd5f19a2c2a8528df0123de0(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d754df6bba99dca21232b365864eb9504d534a87bd687a92999225fecccb7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8eef3e6d9d6a8b8c57d228546929c5475d6a5bc65f09d27fd3f8d3c929a0032(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201f5a8e1d724b4898f375a021cd2cc10d70c9e553fe0f7184abbd5c3eda1d24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fc7cc84ae71d08bd884e136786b8e6c1d28211732315c91672deb0b339f041(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecfdbe268690fd51c35059dac40e899d62ae9f88fcb81e9c1b444d1111a79db(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f969a64382114ae2066a925c87027fff390a1777e1f86f5fb63a4269956904(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationArn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60384bbce8d2545f60d54d408c886732bb16759af7f05087292cdfd6ce955df8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501bb18f5b2d7b98aaf83ccea84f089587f4e11ccc07198e23ca241511c80c6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b19756f036343f6e728d05ec41410747d7b96884fddb5845eba1d3f23dcc43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b682637defb12c57b8f00fbc82ec8fd7ea9ee1a8631423e4ac9d76006d9ed5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationArn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24a1f773fb4de4c4881665617f57e9d259794ff02dd0ec462f20896b8295003(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d166236147819995051a98b4a4f79d5871e8b8863458fdb156c0cdc4b98665(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c13f1685f06ab761db2037696a505a231f4b3d75f26cd46c1e8831f6b45d0d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25a3ae065a8db0f3bef8cec3298bab6aaebab43d8832d59a8b289836c5ca975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a9f794e3b6a2fe3f28425ace2da9ba12cdb4c6c6fb399ff745e1081c2aaa76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166bdff8cacee423bb559d0edbadaee828361ea7dd0a207379f4922511dcf3ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c6d5a06d78a22c71ff228a0f72ce5f5e689405719a5fbb0d4ca15da22c74ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceApplicationName]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968eb8d2048cd7bea43461a76d33673cc9ab462fd3decffb700e9178e82ce454(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5977a751c497ad0a4976fda21a617c2e24def56dbc697d8afb551508356f0ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95ba2fd485e88e9aee569a72e43517ec3ffc45b8097cb21552b6bc8d308a12a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc8a4417621179f67d30e05b8f0cd14c87938ccb9507956fd9b1431a6fa057c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceApplicationName]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824e81035ca8e2b0e453ba800258ce80899b1fd8aa4b4b8600d15fdc58e1bb79(
    *,
    comparison: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ba0de307fad8f7823ff51b560c535f8aa3822738504705eb8acc9c6853fdb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913fb504bac5ab9fb7a3af25e207df535cace52bdcc0ad902e2a5457e72cfb0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a15a2b96b7dce61030f4072278a99325dc92a9a6caeb5acc374d5dcd4e20a1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bdd17e4ceaf000777a59fbd6947e81246fae76c6d64e2d918a8efe4e0f171e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7a867932e33bdd5e71605822e57dd80a1b8aeff1b448401c179119a9245f27(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01856d10bd3783c9785f015082ce08cf07faf30f6dcc594fbfb460d4619ef56e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceDetailsOther]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27d796ceae02168172f2af679c62976f40f58b78ef41ed04c38c0fcf25d66a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b85b92c1d3a5bd4462b5ca752edb55c52c9d1ebbfe3287ebda57d6073c5875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d54d70cfdf50f127c974b9bc68693565456178391b72839d6cb6f3ad41db15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c062c5af16b6aa13b8108aafb89d2f090eb9ccb97b876fe86cae80187509d8c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b883b3f0ffedb3e7f88b87c360dac6eb3f240be41e8fe59007d51199726545fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceDetailsOther]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0791dd722710cb32bf141500351670a3cd765df4d27e1d67d45ffd43b31609bd(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3af61048db78a5fe369ce8c12de43f667d435a59ba1bb36e398df770426678b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e82c3dce85c29a5d322548cd265abbc378f5e8006f82a519ec06c2686375aa4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebafad6fd7dae1c993daecabfa7d0ae25621bbbcd5a4023eb126c67300a6185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cf8342e8e4e50c4edf81ff2b6d26eef7dcfc73b14bf6ddb0b59d77c5b2be11(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9a8815ad2bbb0784c17f62123e6d7d8f77000968b199fb43a0c8c95248d41f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b561f2737028c0f44c54784ad745b8c610669bf36d3584d0e1650f0c4035b095(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceId]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa880d73fe33255326fa1a61e6f7a582958100a8ddd1492d9babb4e71a8ea790(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e298ae046917eab9c62108aabc334852ec3380abf5af6d11f1cfaff957d998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d463e5f666d69544003ff8f329466580ed59b044913fdce60a3897de20c1b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288846eeaff3c31e8b7b22752ea098afc565a5aa1aca7a3bf91d32281adc3a87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceId]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8fea332acee36957017e6404fc0732be94482046bb95e10be08983e040894c(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8bab761ae0fc1bc9c7a6bf06d18fc66c76204b60feb859af22a2c611eadc36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c79d9842210b9025f1ee3f9ff253e9d12ad7542eccddba8afb5522fe64a6507(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b9e317e4154f88c9ae3020cc52a5854a4547d8b73c4af89caae605d05e0858(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1dcf8b5953c653c3daeea459c316d44501938ef2d56134d7185610e6b6316d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee28df5920a0bc8149278a96bd5e537701915019e2adf4be8b84cbf8d0e7acf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bf15cd9e14c82776209b62d3efc6d0ffb14f13e32d9c83ce1d052691cc7498(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourcePartition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33144dba71c2f3a873fcd00292e4c60e2421e1eb2130dd73c8beb6ef97a5791a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01b83df43e6f62a7638779a1dbba3bf05c488e4a40dc30c9aebeefc9080fed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6edc1d1c9ed5182f8f5a198c5638ebe4d853ce8d46efc12e1ab0a3287ee5376d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e492be506afa8e7965f03245bb40bdaa41cc4cfcc020d2fe985c432e813457(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourcePartition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016ae44727fcfbd30166bed8830fbee6032b9a5e24d361cfd22c8808988307fe(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b730ecb954464bcf05f2f927313009db74ea132ef3adf6144f7bc381e680721d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051239f76875e55b86b637933e4ade20b06fbac956f23cbcf9e71c74769ca799(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137d6598ab6f44c636a43719c2aec62aed88c420f0bf2e8b911ac286fa04f085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1707ee5596c1a83180543d2ba55f11feeb89f2c91f088c20eee7539ec0a1678(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423708f2b83063d9ef2bb32ee05972fb904fb4079ae537a7b3b952739c94846f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6779e783d602cbde607fe9d10677267a65a5c57b1d3c96abd5e907456ceb2c60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceRegion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcb26b32d7270fb52dd2aa515508fbbedecb9763dfbadf6d27ac227a658b7e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d0368c03baeb7ac6ee17a785d3db9559254b89c6fd270cfc82deefc6ece7b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bea1f08093ac4a3a3fd00bd2a0019cd59bf706373ebcae5627009f7080cf33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fedd377dcaccea3fde055ed69692f2055783d7c6e7997d5dab8d1e95788d4de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceRegion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e880fa463e243cdf56839dedee6f51fa7b9440225683506608ddd0503e0680(
    *,
    comparison: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db025782326da00e9e920f42999964abc818029aad3aee793c5ab96a51910946(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca546ff4136063e8ae67c344d59dda6e436f5c2f4f5235356ce853e3e6b57538(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd6efe67d4d1d4a9e6f4ee6584bd961c5fe8992ec133ac270a60da352afc086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9dcb4bd18db5790415c775fb5d322eb672b19e44c4d28bebfdbdfdb9c5d7e1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f2b76399b63d72e5d83fa935fb9cb11e505fcf9aaf502ece5fbab65ec662b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae8e6019545b98a1912f0581c33fdef42b7a3e67a79cd586966de0abde2798a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6adb0a32ab0cdd2bc0fd066b0432d5085af567a568e83537d09945fa4a3ac16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0973976c085e0a4839b9069a74d5aa39cb90ed32e02fa443eb10426374d58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80ff0a9f6466430890bcbe48c1421f3804099d7611649b8ba379150b63a7941(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcd72ff8134db31ce2d46651f5c48402bf96782bd8042aa1c7fc7e8658dbc51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09571687268c8cc0a25589546539ffc785945f9398b8e50e1feaa29a9a4b0e7e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4be44c994c937aee162b4cab53539d3e60ea311911a4b47329449a8bbe9cce4(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c52cc926ebeaf80cd7b0bf77ff5283ffb74b8e4c543cd751945ec12648e96c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6a1161b67494bb03aff0ae146cd7afdf4abbf3c12146c4a62e05400d4bc4f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12c46891bcc0978e54497a62662cf7652121fad29c3f25a7c452396f15b8e08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b7b057139bb0e41aa64e13550447cb441aa0da16eb7f6b8388c02b7f5180e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3edadd307cb3ae1c7284aed108f8dac9fdceac6f1e5dab2e0e9dd13b602ca53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb464c65db7cc4aae703f0c3f5ac6dae4e0d6400f1b63f744eeef0022eba017(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaResourceType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ec30090af859d402aacf5ffa4fc003f4c6e485a38fbfa4b1ea9554ff0770d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b919627a477f940db9092f7ebd976dcc63bcb3c2a570aff80b824575cbea47ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee917d0ddaa50ba901a803dfaab097e82b27880e45dc12b69629e0e2f077879f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e25b2f31804b965b83fdc6de5e707389831196128d5ff5514f7f4e6ca1e487(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaResourceType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85640790e2c1041facd58b24992bcce3f3fce94ef8e4b4efae8f5a9c69dcf5e(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57388570b1cad118ba7105f33904794c7a3cbd70f92de03684461a77ec5dabb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff970be83387e6c988c7670f860f5b7045d30e951e9d177a45d3ba9c45968dd1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98c06898db5c80662d331d39d15d222f89ceeeab0521f82484f528e0bcdcdc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1c51e91ee8ee9b8d8c0edcef06644333c94f8873fe369f13f766fc76997937(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd55443493fefc02f90eee29f1d6667b9b49ede449cf352264783519a7d6ef8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8037bd9ac5a335f429a930cc930242d5affdfb32827cc1d0897103f52cfb74f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSeverityLabel]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0cde6238c742c1726b79a9199e81ec94dfed5cb8ac316f13f496081a9e5c4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52548b335f0feb5bcb8d3085babdabd7bcf86babef758405d408d7aa636216d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f2d2964bd9d1377c1bea3200b0aa74b1de0d1b5b1e6429307034955b38899b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1330acf909826817aef56bcd355ca260de22fbc288806ac490de9c5dc9f063d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSeverityLabel]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf04c9f939ee1ec043d68cdbb02114e8d27916e30ebbc68aa35fcc851af4e749(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154da1dea2bf8b37e6667edd1cd5d91c7caa34df9418a7c0696327801c290ec2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070af6465178b512e601a0032370c26dfaf1bc2906cd47bf7d5955ae5fc39b82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0c86d57b24b7e185288f83330605694a87025f4c6294c120b3503bbcb64717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc708348eeb1026be3d75038af7a23c22226a5dd1ab3ea3d8c28f435f67cc2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe8e2f86d3a6d5c98a7fd153ad6cb05c85c4c6295485f6f56cd0555ed177044(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4f2690068b887439c7257833bf3f4f3f79a1210b65bd0a8a875906af743728(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaSourceUrl]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee69237b5f3d3d2c8f301ae580ea124da33779a73d74f5d62cb819c1bffbd5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24555d1472a1d64c410dd1a111da3696f3bdeb68aaccb14dff149211267dacb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8c78850224b5934354fd827d2d9af53111fd5d3d3dff17a9fc55817d51f675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ad5ef5b1ef8e11d77b0967e08ffe582da45bb08c256a7276d368ed6f582b4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaSourceUrl]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b17927aac5b26176da33f50919e727d762656ce837dcac65ac874b855b28c5(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfe49ddf9cad4752a983a8b9ac7f87f082525d39e913c48afb3eb4f98f16de6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204be127c5ad3bf7c93ae31d686eb6fd25b2c433a3f815ae98b4df1acaa50091(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc593266748d0ce2ddf7414422438f1b51b6fb6936a5040791e3f7d49dea532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae19a925bd61ddeb0af6cf812b31fa3d6e34da5f5e1a65ee73cc0458c9b7ae05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4f26e3178857ec9b910f1cf2ca80f7f53e0e3cc2cd739fdfd52167506ab1ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b4b046b56ac37c974dc0d85ee76a5986e24bf0464c1449ac03c7b649bc58cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaTitle]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8747272667c694c937e6e045b4b3bfb4d0d1698f0fafa6fcf777c09cdbb434(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3aa1d74ca7744d2507fdd03095d1b5fc00472cf27c8812b10b3166a81fb71f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f18287ef731b0b8c27e485e94cfb1e0600b61aa4415647c9d9858ff27163b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed9f1636eb7b564efc405618c706cde5fc0a52e21e37190232e5c28ae43e170(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaTitle]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17fc0894f828e82b41be6ca265f0b66fd93216c4863123e676e2fd5ed1e20dc(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcab67b8422a601e6b1e5f3152fd5b5acf8c17c2700fd745ae94700ee3476a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6817a3065b5377284ea9b5789c10e5cd4116b07396433079aac8505465ec42ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b1580134d68320f889dd1abbac4192c7c806c1453f42f1156f00b37023dbb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f0a7361d1eb35ddaaef4c96780b1b65de3b0cc1056b4bdb48438e461195723(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526e5764d678a3612f23cdb46d4a1deed2954af3df224b6adee0a337cc7d3d5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a9d0a0b3aa3cabbf22e4f79b30c7063ea008dfdd9f6cad4ecfdf5c8dbdbe58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c491c8ff106190afe72bc3a2c570a85342c0ea2ea5763cf1b139646274cd09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dae0d70d10cd6f617287756537412ab94cb987f4634eb398bb9db779cc1ceb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2144a5b16e6b755e19e273641778ec93604a425655e28d19e01362e194593bb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86fef41b87d8184cf9f89185c7350f74ed6f9016ac65eb7f12b29d8f93cf0c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ee3c01a74906ff49252f48800ca3c39adb45436dde95258c67733b52ab3db0(
    *,
    date_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0aaf9cf5aaa07986df59dbba39dd456bfa4d1fc439df5e8a0f862e1cca8342d(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a7ca4779992755577275d8072867f6a22760f791458efb371562a21bc978be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb8b8d05e9920487160742ea2527dc99a0d37da10f647c54f41a24162fe3663(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3243f74668772a178bf9aec884d07dddd2ec3a663e4478255759df72719f35b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47c20715cdbb10f0cf63c73a704d5f090786b4e37847150345b346e6cadf092(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b26e7792c966182c204a00dac5d958118868379a3f71518e4ba998c52d45000(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4587ccb674e9c8ff172bf57ee1f5c2f5564ad3eba3a97afdb99ad3477651e15a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25002a25d9c5f726e0cf69f0f93bf00a436bddec5052b56b681b6570063db636(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f54f948647e140828dfaf1da9096c9bac8796029bc02daf6cb096aa8515ca5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a655936e3d75e17fdd39f1efe831036bb08e59066902d5f85c9b4bfa82b4409(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c78c9c13c2813498b2777d9534e00380813a82d361d0f32d899f1678bdd9a5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAtDateRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9886fe86f5188ecd4e9ba62371638caf6e0b414c27d42039587ee16c7a9a3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd50509be6b695834ec00715c0e80c6f46f7b223953fef752be68530780eb95(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aa1b211fa6a9ac3fae9a0971e5ec08069b2b1abb120178cc86be01615a4254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e10f8ee42590ac84f231d9879d20800900e3f5c46c6d1fd2d17dc4736ae1ec4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9fc4c1ae87fde0e587186be0b4cc30ebedd52b11c3c9a0f6898b44be41fb71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cec38ba4f670f99df4bf9b327637a4213097df1f59c753263699be2a46f4c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUpdatedAt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8e610034d7aa8ba1c1580d3383c3d855fb2181d12fbe1b12315bcfbf88f795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf34161507d188a65569a2d573c12321b8a32df6afef066ea44a36b4f4aeddd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityhubAutomationRuleCriteriaUpdatedAtDateRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97e81aadfc934affc7341f7d0a792fa4ae2d1483da75018568fb231430aef11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d802adc68bbef164c91ce6db10111e16c9540ae816289db167b10187810f7cf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b0a50fb2d750bea869ef2c293f345b61cf119bd96a3fb2d5883d07b06e9071(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUpdatedAt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6567a02df2318bcb208d1b484ec9369f827680c3791ec76721ecd58f2f82c23b(
    *,
    comparison: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06dbe74a541f997903d5ee42e7b60407d705489cfce7451b0c855b676243f7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f464fc47fea14a9683845788649ed65944c1e8eb64915b5411b39531080c888(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2b4e5c2b97afce8c41fcb8149f9d8ac8ffb1b928617fa86366d3693b422140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd2243781a60d0c53e58de6dd1671ca5386817e35f5b144c3ba1bd6ff27d903(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0d8d43e4351319c5e3f34049c242408756d354a28a7ed33dbf7f2319bb064f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46a52ea087f34c9a45bc9ac5df24cdf645a765af753cb06b3d5e1f4bf97a223(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaUserDefinedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783d750e0432fe55dbd68bb639ca104c0d99c7e2d288f878741d5963282456ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8be81b84488693c461d49980146e2acf409eeb20823922bfccc6bb4914df9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400e1daca2d9e0f4dd73f54a1557908436e4acee71e5b86ded55b3cc62a35ac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc6385645424fcf27a5f93f44f49b3ef0655ebd2d1781451d563196bc83b079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11037badc89c27f1bff296583405c9609ee00e426865adf72ef3940afba8246(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaUserDefinedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d9d8f33ed064cbba006ad232c4d1566ab090899199018403030118357f4ff8(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb11b67432512f2c29faa54c7d227be147b52636b5df7a2127c3e40adbe7c75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a654fc9757bed3088c77f85e63f00253ef8c1829c4a6aa8f7a21ded63144ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42adcff481003f11fd81163639f10e687173bf4ec67afc193915cfa8c37c088b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adc9174aec4186eb6318389011a2affd2fbb79e80e82d0449eceb81077fed5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3472fab951d5229adba1b7f4bf62887ca815dd14769d7e334b1a6cf1afa85481(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81820bef6ca5dcebd8c27d9d0692c7e74f2152cc43219f93043215c5abebef9e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaVerificationState]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c973c070320b80ab03d701867322f023fc04ddb6477c73a49b07eb5865acbb31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c709bc9353aac454fef536a8f6e78f6967b0e76227365a05a30bc8097d7ea2b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e91e324b03cf1aedb7489cedd94eab88290cc5485e4f9ae8fafc45149ab99c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb3091186a24bfd4b8b7e3e57a0c938b65f57e4686687759ea2be9afe2e1d77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaVerificationState]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cf23737c84e6489eadbb6b062be2e7b83d6f07aeac0d921e72f667104201fc(
    *,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5eb5dc2c4b4e00f49e661f2839b1be3110d7ee203bebc9fe2f3ad1880d9ada(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e938bf5e66bcfee027e4437f8023654fff4d0ca917c599a203f375699d6113(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96fa894df59f73dc874b7c83af73561f7289595cd60cea22bb893c89ce366dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8cc46fee2dfccf0880ee307336cee773779732cdc0608eeeb8845a062978d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ba90dee3d37d7fbfcc4631cb5f02b10073a5a389a3e39f837862829e3c051c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24f42130f4c290417b47f84daefaf9a02244dd9b37155e682e69285e0b2da96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityhubAutomationRuleCriteriaWorkflowStatus]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f195268db0109d99925ea06f65ced772974070226397068a7a2b90892d60d65c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141ca429ec3bbe526b7e7006c19fb273cb55546985d9298142c1b05574669362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103b14370cd411ebc3e560d7297be6802a1b59c0fd8b22098f264353fcde7e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85d660efcf481af48b56ed16029b755b011a435ffb8ffdaf3a3e541798db7f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityhubAutomationRuleCriteriaWorkflowStatus]],
) -> None:
    """Type checking stubs"""
    pass
