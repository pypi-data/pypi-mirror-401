r'''
# `aws_budgets_budget_action`

Refer to the Terraform Registry for docs: [`aws_budgets_budget_action`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action).
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


class BudgetsBudgetAction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetAction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action aws_budgets_budget_action}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action_threshold: typing.Union["BudgetsBudgetActionActionThreshold", typing.Dict[builtins.str, typing.Any]],
        action_type: builtins.str,
        approval_model: builtins.str,
        budget_name: builtins.str,
        definition: typing.Union["BudgetsBudgetActionDefinition", typing.Dict[builtins.str, typing.Any]],
        execution_role_arn: builtins.str,
        notification_type: builtins.str,
        subscriber: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetActionSubscriber", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BudgetsBudgetActionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action aws_budgets_budget_action} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_threshold: action_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold BudgetsBudgetAction#action_threshold}
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_type BudgetsBudgetAction#action_type}.
        :param approval_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#approval_model BudgetsBudgetAction#approval_model}.
        :param budget_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#budget_name BudgetsBudgetAction#budget_name}.
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#definition BudgetsBudgetAction#definition}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#execution_role_arn BudgetsBudgetAction#execution_role_arn}.
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#notification_type BudgetsBudgetAction#notification_type}.
        :param subscriber: subscriber block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#subscriber BudgetsBudgetAction#subscriber}
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#account_id BudgetsBudgetAction#account_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#id BudgetsBudgetAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#tags BudgetsBudgetAction#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#tags_all BudgetsBudgetAction#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#timeouts BudgetsBudgetAction#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc4614ac9377b337ca59a5b7d0ec386bc57e3af9804dcba7b716a52f07397f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BudgetsBudgetActionConfig(
            action_threshold=action_threshold,
            action_type=action_type,
            approval_model=approval_model,
            budget_name=budget_name,
            definition=definition,
            execution_role_arn=execution_role_arn,
            notification_type=notification_type,
            subscriber=subscriber,
            account_id=account_id,
            id=id,
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
        '''Generates CDKTF code for importing a BudgetsBudgetAction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BudgetsBudgetAction to import.
        :param import_from_id: The id of the existing BudgetsBudgetAction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BudgetsBudgetAction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3d4c5000b211d117292a99216e73406444bc1d23bce5f056e9c3551627ecf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActionThreshold")
    def put_action_threshold(
        self,
        *,
        action_threshold_type: builtins.str,
        action_threshold_value: jsii.Number,
    ) -> None:
        '''
        :param action_threshold_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold_type BudgetsBudgetAction#action_threshold_type}.
        :param action_threshold_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold_value BudgetsBudgetAction#action_threshold_value}.
        '''
        value = BudgetsBudgetActionActionThreshold(
            action_threshold_type=action_threshold_type,
            action_threshold_value=action_threshold_value,
        )

        return typing.cast(None, jsii.invoke(self, "putActionThreshold", [value]))

    @jsii.member(jsii_name="putDefinition")
    def put_definition(
        self,
        *,
        iam_action_definition: typing.Optional[typing.Union["BudgetsBudgetActionDefinitionIamActionDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        scp_action_definition: typing.Optional[typing.Union["BudgetsBudgetActionDefinitionScpActionDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        ssm_action_definition: typing.Optional[typing.Union["BudgetsBudgetActionDefinitionSsmActionDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_action_definition: iam_action_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#iam_action_definition BudgetsBudgetAction#iam_action_definition}
        :param scp_action_definition: scp_action_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#scp_action_definition BudgetsBudgetAction#scp_action_definition}
        :param ssm_action_definition: ssm_action_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#ssm_action_definition BudgetsBudgetAction#ssm_action_definition}
        '''
        value = BudgetsBudgetActionDefinition(
            iam_action_definition=iam_action_definition,
            scp_action_definition=scp_action_definition,
            ssm_action_definition=ssm_action_definition,
        )

        return typing.cast(None, jsii.invoke(self, "putDefinition", [value]))

    @jsii.member(jsii_name="putSubscriber")
    def put_subscriber(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetActionSubscriber", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ca070abc7d5d4338eb3e28238adf9129dba09b9e36123c746d3f77ecec6e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubscriber", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#create BudgetsBudgetAction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#delete BudgetsBudgetAction#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#update BudgetsBudgetAction#update}.
        '''
        value = BudgetsBudgetActionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="actionId")
    def action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionId"))

    @builtins.property
    @jsii.member(jsii_name="actionThreshold")
    def action_threshold(self) -> "BudgetsBudgetActionActionThresholdOutputReference":
        return typing.cast("BudgetsBudgetActionActionThresholdOutputReference", jsii.get(self, "actionThreshold"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> "BudgetsBudgetActionDefinitionOutputReference":
        return typing.cast("BudgetsBudgetActionDefinitionOutputReference", jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="subscriber")
    def subscriber(self) -> "BudgetsBudgetActionSubscriberList":
        return typing.cast("BudgetsBudgetActionSubscriberList", jsii.get(self, "subscriber"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BudgetsBudgetActionTimeoutsOutputReference":
        return typing.cast("BudgetsBudgetActionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionThresholdInput")
    def action_threshold_input(
        self,
    ) -> typing.Optional["BudgetsBudgetActionActionThreshold"]:
        return typing.cast(typing.Optional["BudgetsBudgetActionActionThreshold"], jsii.get(self, "actionThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionTypeInput")
    def action_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalModelInput")
    def approval_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "approvalModelInput"))

    @builtins.property
    @jsii.member(jsii_name="budgetNameInput")
    def budget_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "budgetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(self) -> typing.Optional["BudgetsBudgetActionDefinition"]:
        return typing.cast(typing.Optional["BudgetsBudgetActionDefinition"], jsii.get(self, "definitionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationTypeInput")
    def notification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriberInput")
    def subscriber_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetActionSubscriber"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetActionSubscriber"]]], jsii.get(self, "subscriberInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BudgetsBudgetActionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BudgetsBudgetActionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d81ac225f7232a09c72255e3ae580a7d882e8ce688eaf45fdd8f9a7b87f21e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionType"))

    @action_type.setter
    def action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0303fc267d98dfc5a69e9e6e915bd3294954cf8f81ea958c135c46faed849d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approvalModel")
    def approval_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "approvalModel"))

    @approval_model.setter
    def approval_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230e95006d76beb029eea0bcd6f268a1b5559aff0f9605f489eb9d6ec59144b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="budgetName")
    def budget_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "budgetName"))

    @budget_name.setter
    def budget_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082d971da1fb5059ff56f2b33f5b42d1f75f4c6fde66ba5ab22bf27c35fa4476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "budgetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aae4d668e3abba07ed32a5a46fd0b7511b210fb7f2938dce6c5a8c21120af54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ac2303d8526c6ddcb208b866e0b46cda67716f8cd1cd12935749b6d70db900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationType"))

    @notification_type.setter
    def notification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce012f987676c68c9fca25d00f8d4598eee84f9444a0350aa2c5e914477dd8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74eff3a29eac5fbfad8bb07341ae88f0065539b3181db38f3fc35a04b9d6b773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee4c19c5c5e92c8554a3a0b3d3614bac3ebf095f1bcce7975f7c2c8921dd5dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionActionThreshold",
    jsii_struct_bases=[],
    name_mapping={
        "action_threshold_type": "actionThresholdType",
        "action_threshold_value": "actionThresholdValue",
    },
)
class BudgetsBudgetActionActionThreshold:
    def __init__(
        self,
        *,
        action_threshold_type: builtins.str,
        action_threshold_value: jsii.Number,
    ) -> None:
        '''
        :param action_threshold_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold_type BudgetsBudgetAction#action_threshold_type}.
        :param action_threshold_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold_value BudgetsBudgetAction#action_threshold_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969ad55b4f569798a08b7fd4d3232a99c156e7b9b911524cb2fc868d14de29cb)
            check_type(argname="argument action_threshold_type", value=action_threshold_type, expected_type=type_hints["action_threshold_type"])
            check_type(argname="argument action_threshold_value", value=action_threshold_value, expected_type=type_hints["action_threshold_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_threshold_type": action_threshold_type,
            "action_threshold_value": action_threshold_value,
        }

    @builtins.property
    def action_threshold_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold_type BudgetsBudgetAction#action_threshold_type}.'''
        result = self._values.get("action_threshold_type")
        assert result is not None, "Required property 'action_threshold_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_threshold_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold_value BudgetsBudgetAction#action_threshold_value}.'''
        result = self._values.get("action_threshold_value")
        assert result is not None, "Required property 'action_threshold_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionActionThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetActionActionThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionActionThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__728fb85665a947b2849bbc21009cae8bdae3cd50864642dee9d999550bfb25cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="actionThresholdTypeInput")
    def action_threshold_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionThresholdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="actionThresholdValueInput")
    def action_threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "actionThresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="actionThresholdType")
    def action_threshold_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionThresholdType"))

    @action_threshold_type.setter
    def action_threshold_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64eb8aa35c604d649324269e6b32c6d47ace582e93baea3bc4a0614d94eba80e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionThresholdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actionThresholdValue")
    def action_threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "actionThresholdValue"))

    @action_threshold_value.setter
    def action_threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657a8375609eb068b04eda9a4a3cf4cc582131bb823b38fe1726274188785152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionThresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BudgetsBudgetActionActionThreshold]:
        return typing.cast(typing.Optional[BudgetsBudgetActionActionThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetActionActionThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374d192628d6a5116facd30b4b9d8b7ba456ee56a952293fed7dcd8fbefd486d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_threshold": "actionThreshold",
        "action_type": "actionType",
        "approval_model": "approvalModel",
        "budget_name": "budgetName",
        "definition": "definition",
        "execution_role_arn": "executionRoleArn",
        "notification_type": "notificationType",
        "subscriber": "subscriber",
        "account_id": "accountId",
        "id": "id",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class BudgetsBudgetActionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action_threshold: typing.Union[BudgetsBudgetActionActionThreshold, typing.Dict[builtins.str, typing.Any]],
        action_type: builtins.str,
        approval_model: builtins.str,
        budget_name: builtins.str,
        definition: typing.Union["BudgetsBudgetActionDefinition", typing.Dict[builtins.str, typing.Any]],
        execution_role_arn: builtins.str,
        notification_type: builtins.str,
        subscriber: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetActionSubscriber", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BudgetsBudgetActionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action_threshold: action_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold BudgetsBudgetAction#action_threshold}
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_type BudgetsBudgetAction#action_type}.
        :param approval_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#approval_model BudgetsBudgetAction#approval_model}.
        :param budget_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#budget_name BudgetsBudgetAction#budget_name}.
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#definition BudgetsBudgetAction#definition}
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#execution_role_arn BudgetsBudgetAction#execution_role_arn}.
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#notification_type BudgetsBudgetAction#notification_type}.
        :param subscriber: subscriber block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#subscriber BudgetsBudgetAction#subscriber}
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#account_id BudgetsBudgetAction#account_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#id BudgetsBudgetAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#tags BudgetsBudgetAction#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#tags_all BudgetsBudgetAction#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#timeouts BudgetsBudgetAction#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(action_threshold, dict):
            action_threshold = BudgetsBudgetActionActionThreshold(**action_threshold)
        if isinstance(definition, dict):
            definition = BudgetsBudgetActionDefinition(**definition)
        if isinstance(timeouts, dict):
            timeouts = BudgetsBudgetActionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83079e3e89641d434e327b6fadf9df8ac24bec06d87cab175e28149a9320bf87)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action_threshold", value=action_threshold, expected_type=type_hints["action_threshold"])
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument approval_model", value=approval_model, expected_type=type_hints["approval_model"])
            check_type(argname="argument budget_name", value=budget_name, expected_type=type_hints["budget_name"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
            check_type(argname="argument subscriber", value=subscriber, expected_type=type_hints["subscriber"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_threshold": action_threshold,
            "action_type": action_type,
            "approval_model": approval_model,
            "budget_name": budget_name,
            "definition": definition,
            "execution_role_arn": execution_role_arn,
            "notification_type": notification_type,
            "subscriber": subscriber,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if id is not None:
            self._values["id"] = id
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
    def action_threshold(self) -> BudgetsBudgetActionActionThreshold:
        '''action_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_threshold BudgetsBudgetAction#action_threshold}
        '''
        result = self._values.get("action_threshold")
        assert result is not None, "Required property 'action_threshold' is missing"
        return typing.cast(BudgetsBudgetActionActionThreshold, result)

    @builtins.property
    def action_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_type BudgetsBudgetAction#action_type}.'''
        result = self._values.get("action_type")
        assert result is not None, "Required property 'action_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def approval_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#approval_model BudgetsBudgetAction#approval_model}.'''
        result = self._values.get("approval_model")
        assert result is not None, "Required property 'approval_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def budget_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#budget_name BudgetsBudgetAction#budget_name}.'''
        result = self._values.get("budget_name")
        assert result is not None, "Required property 'budget_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition(self) -> "BudgetsBudgetActionDefinition":
        '''definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#definition BudgetsBudgetAction#definition}
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast("BudgetsBudgetActionDefinition", result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#execution_role_arn BudgetsBudgetAction#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#notification_type BudgetsBudgetAction#notification_type}.'''
        result = self._values.get("notification_type")
        assert result is not None, "Required property 'notification_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscriber(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetActionSubscriber"]]:
        '''subscriber block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#subscriber BudgetsBudgetAction#subscriber}
        '''
        result = self._values.get("subscriber")
        assert result is not None, "Required property 'subscriber' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetActionSubscriber"]], result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#account_id BudgetsBudgetAction#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#id BudgetsBudgetAction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#tags BudgetsBudgetAction#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#tags_all BudgetsBudgetAction#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BudgetsBudgetActionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#timeouts BudgetsBudgetAction#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BudgetsBudgetActionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "iam_action_definition": "iamActionDefinition",
        "scp_action_definition": "scpActionDefinition",
        "ssm_action_definition": "ssmActionDefinition",
    },
)
class BudgetsBudgetActionDefinition:
    def __init__(
        self,
        *,
        iam_action_definition: typing.Optional[typing.Union["BudgetsBudgetActionDefinitionIamActionDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        scp_action_definition: typing.Optional[typing.Union["BudgetsBudgetActionDefinitionScpActionDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
        ssm_action_definition: typing.Optional[typing.Union["BudgetsBudgetActionDefinitionSsmActionDefinition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_action_definition: iam_action_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#iam_action_definition BudgetsBudgetAction#iam_action_definition}
        :param scp_action_definition: scp_action_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#scp_action_definition BudgetsBudgetAction#scp_action_definition}
        :param ssm_action_definition: ssm_action_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#ssm_action_definition BudgetsBudgetAction#ssm_action_definition}
        '''
        if isinstance(iam_action_definition, dict):
            iam_action_definition = BudgetsBudgetActionDefinitionIamActionDefinition(**iam_action_definition)
        if isinstance(scp_action_definition, dict):
            scp_action_definition = BudgetsBudgetActionDefinitionScpActionDefinition(**scp_action_definition)
        if isinstance(ssm_action_definition, dict):
            ssm_action_definition = BudgetsBudgetActionDefinitionSsmActionDefinition(**ssm_action_definition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca62c8f9bd7bc06d3b70c86edc661bbca6ecdedf4d890ce46f2de0bcb311b40)
            check_type(argname="argument iam_action_definition", value=iam_action_definition, expected_type=type_hints["iam_action_definition"])
            check_type(argname="argument scp_action_definition", value=scp_action_definition, expected_type=type_hints["scp_action_definition"])
            check_type(argname="argument ssm_action_definition", value=ssm_action_definition, expected_type=type_hints["ssm_action_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam_action_definition is not None:
            self._values["iam_action_definition"] = iam_action_definition
        if scp_action_definition is not None:
            self._values["scp_action_definition"] = scp_action_definition
        if ssm_action_definition is not None:
            self._values["ssm_action_definition"] = ssm_action_definition

    @builtins.property
    def iam_action_definition(
        self,
    ) -> typing.Optional["BudgetsBudgetActionDefinitionIamActionDefinition"]:
        '''iam_action_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#iam_action_definition BudgetsBudgetAction#iam_action_definition}
        '''
        result = self._values.get("iam_action_definition")
        return typing.cast(typing.Optional["BudgetsBudgetActionDefinitionIamActionDefinition"], result)

    @builtins.property
    def scp_action_definition(
        self,
    ) -> typing.Optional["BudgetsBudgetActionDefinitionScpActionDefinition"]:
        '''scp_action_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#scp_action_definition BudgetsBudgetAction#scp_action_definition}
        '''
        result = self._values.get("scp_action_definition")
        return typing.cast(typing.Optional["BudgetsBudgetActionDefinitionScpActionDefinition"], result)

    @builtins.property
    def ssm_action_definition(
        self,
    ) -> typing.Optional["BudgetsBudgetActionDefinitionSsmActionDefinition"]:
        '''ssm_action_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#ssm_action_definition BudgetsBudgetAction#ssm_action_definition}
        '''
        result = self._values.get("ssm_action_definition")
        return typing.cast(typing.Optional["BudgetsBudgetActionDefinitionSsmActionDefinition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionIamActionDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "policy_arn": "policyArn",
        "groups": "groups",
        "roles": "roles",
        "users": "users",
    },
)
class BudgetsBudgetActionDefinitionIamActionDefinition:
    def __init__(
        self,
        *,
        policy_arn: builtins.str,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param policy_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#policy_arn BudgetsBudgetAction#policy_arn}.
        :param groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#groups BudgetsBudgetAction#groups}.
        :param roles: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#roles BudgetsBudgetAction#roles}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#users BudgetsBudgetAction#users}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b356ac953972fb4bcdd57859b09bfc473a994dbfcfdbf2591775dbd4d2b2f69f)
            check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_arn": policy_arn,
        }
        if groups is not None:
            self._values["groups"] = groups
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def policy_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#policy_arn BudgetsBudgetAction#policy_arn}.'''
        result = self._values.get("policy_arn")
        assert result is not None, "Required property 'policy_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#groups BudgetsBudgetAction#groups}.'''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#roles BudgetsBudgetAction#roles}.'''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#users BudgetsBudgetAction#users}.'''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionDefinitionIamActionDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetActionDefinitionIamActionDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionIamActionDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a21158b0ce188949e59f18ac4daa4f8715edcd711f71ea757f2dca249c3cf6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @jsii.member(jsii_name="resetUsers")
    def reset_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsers", []))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyArnInput")
    def policy_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6cbd448dc395dcb85d58a4e4d303f91bd3ecd43c241beb86cb2356f36e9370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyArn")
    def policy_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyArn"))

    @policy_arn.setter
    def policy_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2deadcee54111b6e66ca2c20a36b5c48daacc500d9472219c21069c48bc5871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95bf8cc9652dc6812cc9fa3cef3852d5ed9d8e2d63a6d77290a11ad7934ee2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2953a8ebabcc91c859673feb9ce3184851bdb557fee32da9ec8a9074b8616f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BudgetsBudgetActionDefinitionIamActionDefinition]:
        return typing.cast(typing.Optional[BudgetsBudgetActionDefinitionIamActionDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetActionDefinitionIamActionDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e48851aa76f6d42c06aeff08e27b94c1c11eb85c16f5e989589811a99570f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BudgetsBudgetActionDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a61cbbcaf8f8b37b76ccc780d17bc4b35e86ff4042968fd3663eff7e032c3fe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIamActionDefinition")
    def put_iam_action_definition(
        self,
        *,
        policy_arn: builtins.str,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param policy_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#policy_arn BudgetsBudgetAction#policy_arn}.
        :param groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#groups BudgetsBudgetAction#groups}.
        :param roles: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#roles BudgetsBudgetAction#roles}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#users BudgetsBudgetAction#users}.
        '''
        value = BudgetsBudgetActionDefinitionIamActionDefinition(
            policy_arn=policy_arn, groups=groups, roles=roles, users=users
        )

        return typing.cast(None, jsii.invoke(self, "putIamActionDefinition", [value]))

    @jsii.member(jsii_name="putScpActionDefinition")
    def put_scp_action_definition(
        self,
        *,
        policy_id: builtins.str,
        target_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#policy_id BudgetsBudgetAction#policy_id}.
        :param target_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#target_ids BudgetsBudgetAction#target_ids}.
        '''
        value = BudgetsBudgetActionDefinitionScpActionDefinition(
            policy_id=policy_id, target_ids=target_ids
        )

        return typing.cast(None, jsii.invoke(self, "putScpActionDefinition", [value]))

    @jsii.member(jsii_name="putSsmActionDefinition")
    def put_ssm_action_definition(
        self,
        *,
        action_sub_type: builtins.str,
        instance_ids: typing.Sequence[builtins.str],
        region: builtins.str,
    ) -> None:
        '''
        :param action_sub_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_sub_type BudgetsBudgetAction#action_sub_type}.
        :param instance_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#instance_ids BudgetsBudgetAction#instance_ids}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#region BudgetsBudgetAction#region}.
        '''
        value = BudgetsBudgetActionDefinitionSsmActionDefinition(
            action_sub_type=action_sub_type, instance_ids=instance_ids, region=region
        )

        return typing.cast(None, jsii.invoke(self, "putSsmActionDefinition", [value]))

    @jsii.member(jsii_name="resetIamActionDefinition")
    def reset_iam_action_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamActionDefinition", []))

    @jsii.member(jsii_name="resetScpActionDefinition")
    def reset_scp_action_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScpActionDefinition", []))

    @jsii.member(jsii_name="resetSsmActionDefinition")
    def reset_ssm_action_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsmActionDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="iamActionDefinition")
    def iam_action_definition(
        self,
    ) -> BudgetsBudgetActionDefinitionIamActionDefinitionOutputReference:
        return typing.cast(BudgetsBudgetActionDefinitionIamActionDefinitionOutputReference, jsii.get(self, "iamActionDefinition"))

    @builtins.property
    @jsii.member(jsii_name="scpActionDefinition")
    def scp_action_definition(
        self,
    ) -> "BudgetsBudgetActionDefinitionScpActionDefinitionOutputReference":
        return typing.cast("BudgetsBudgetActionDefinitionScpActionDefinitionOutputReference", jsii.get(self, "scpActionDefinition"))

    @builtins.property
    @jsii.member(jsii_name="ssmActionDefinition")
    def ssm_action_definition(
        self,
    ) -> "BudgetsBudgetActionDefinitionSsmActionDefinitionOutputReference":
        return typing.cast("BudgetsBudgetActionDefinitionSsmActionDefinitionOutputReference", jsii.get(self, "ssmActionDefinition"))

    @builtins.property
    @jsii.member(jsii_name="iamActionDefinitionInput")
    def iam_action_definition_input(
        self,
    ) -> typing.Optional[BudgetsBudgetActionDefinitionIamActionDefinition]:
        return typing.cast(typing.Optional[BudgetsBudgetActionDefinitionIamActionDefinition], jsii.get(self, "iamActionDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="scpActionDefinitionInput")
    def scp_action_definition_input(
        self,
    ) -> typing.Optional["BudgetsBudgetActionDefinitionScpActionDefinition"]:
        return typing.cast(typing.Optional["BudgetsBudgetActionDefinitionScpActionDefinition"], jsii.get(self, "scpActionDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="ssmActionDefinitionInput")
    def ssm_action_definition_input(
        self,
    ) -> typing.Optional["BudgetsBudgetActionDefinitionSsmActionDefinition"]:
        return typing.cast(typing.Optional["BudgetsBudgetActionDefinitionSsmActionDefinition"], jsii.get(self, "ssmActionDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BudgetsBudgetActionDefinition]:
        return typing.cast(typing.Optional[BudgetsBudgetActionDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetActionDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e89efe3094f8cbb59b469b69072178fdf98ff3aec463357bef30713cbf9ef33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionScpActionDefinition",
    jsii_struct_bases=[],
    name_mapping={"policy_id": "policyId", "target_ids": "targetIds"},
)
class BudgetsBudgetActionDefinitionScpActionDefinition:
    def __init__(
        self,
        *,
        policy_id: builtins.str,
        target_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#policy_id BudgetsBudgetAction#policy_id}.
        :param target_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#target_ids BudgetsBudgetAction#target_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5acaac0d5bd2c2475ded464cac23241c8f214bacb4a7d89cc3c0074d68a52ed4)
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_id": policy_id,
            "target_ids": target_ids,
        }

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#policy_id BudgetsBudgetAction#policy_id}.'''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#target_ids BudgetsBudgetAction#target_ids}.'''
        result = self._values.get("target_ids")
        assert result is not None, "Required property 'target_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionDefinitionScpActionDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetActionDefinitionScpActionDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionScpActionDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45d6407c31970516c8e85d7815a9192b6e5e3e292cad462d0e670430b6604cb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIdsInput")
    def target_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11dfb25232f1e4a7ceea6994a91f8d96fb34c051f0aa1fcd4320fa7ac7b8ce64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetIds")
    def target_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetIds"))

    @target_ids.setter
    def target_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f604532448e3ebcdbb48a5d2d5b48a9daf5d6359cc142a6f97b64d367e16d8fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BudgetsBudgetActionDefinitionScpActionDefinition]:
        return typing.cast(typing.Optional[BudgetsBudgetActionDefinitionScpActionDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetActionDefinitionScpActionDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12c0241fd4c64d47f5be5d950ef4905cb054868d42d3bbec92fe858f98bd43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionSsmActionDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "action_sub_type": "actionSubType",
        "instance_ids": "instanceIds",
        "region": "region",
    },
)
class BudgetsBudgetActionDefinitionSsmActionDefinition:
    def __init__(
        self,
        *,
        action_sub_type: builtins.str,
        instance_ids: typing.Sequence[builtins.str],
        region: builtins.str,
    ) -> None:
        '''
        :param action_sub_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_sub_type BudgetsBudgetAction#action_sub_type}.
        :param instance_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#instance_ids BudgetsBudgetAction#instance_ids}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#region BudgetsBudgetAction#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8215d1bd4d21cc7102eb56c221eb801be0269eefe2a7ba43e6ee28cd07a639a0)
            check_type(argname="argument action_sub_type", value=action_sub_type, expected_type=type_hints["action_sub_type"])
            check_type(argname="argument instance_ids", value=instance_ids, expected_type=type_hints["instance_ids"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_sub_type": action_sub_type,
            "instance_ids": instance_ids,
            "region": region,
        }

    @builtins.property
    def action_sub_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#action_sub_type BudgetsBudgetAction#action_sub_type}.'''
        result = self._values.get("action_sub_type")
        assert result is not None, "Required property 'action_sub_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#instance_ids BudgetsBudgetAction#instance_ids}.'''
        result = self._values.get("instance_ids")
        assert result is not None, "Required property 'instance_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#region BudgetsBudgetAction#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionDefinitionSsmActionDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetActionDefinitionSsmActionDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionDefinitionSsmActionDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__644810482673aeece703f9e3293305edd9409f33122fd00523530be990724695)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="actionSubTypeInput")
    def action_sub_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionSubTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdsInput")
    def instance_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="actionSubType")
    def action_sub_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionSubType"))

    @action_sub_type.setter
    def action_sub_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e818772b2a4d2c299059ceb743f4d5f48157aab5eaa71b383554304b0c53548b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionSubType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceIds")
    def instance_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceIds"))

    @instance_ids.setter
    def instance_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bc0fef9eee3bb1652f6a91294e6aefadcda3d7f3f66e39d057fda6718b566f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a94bcaea3eae72c3e7fb157a1536a4761e22a0262fa662c6fb4a68ee14424c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BudgetsBudgetActionDefinitionSsmActionDefinition]:
        return typing.cast(typing.Optional[BudgetsBudgetActionDefinitionSsmActionDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetActionDefinitionSsmActionDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9267d338e741d49d53fa4aa5f5e973f85fc74173347fe0a4972f4295e7ae183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionSubscriber",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "subscription_type": "subscriptionType"},
)
class BudgetsBudgetActionSubscriber:
    def __init__(
        self,
        *,
        address: builtins.str,
        subscription_type: builtins.str,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#address BudgetsBudgetAction#address}.
        :param subscription_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#subscription_type BudgetsBudgetAction#subscription_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a5b8ff2e5d90cde37dcd685b78b8538b03dce760acbeedfa1ce26973be8d2a)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument subscription_type", value=subscription_type, expected_type=type_hints["subscription_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "subscription_type": subscription_type,
        }

    @builtins.property
    def address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#address BudgetsBudgetAction#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscription_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#subscription_type BudgetsBudgetAction#subscription_type}.'''
        result = self._values.get("subscription_type")
        assert result is not None, "Required property 'subscription_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionSubscriber(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetActionSubscriberList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionSubscriberList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fb95bdbcfefe4fdf64f58fedb48353c337fc80294f3b9c5cfd83f7c7471f368)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BudgetsBudgetActionSubscriberOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617d0fc8cbd930d23e3105958781ef967137186b6370e3cf06e68fe87deb7fac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BudgetsBudgetActionSubscriberOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772df9e95a5545e97417630fdfc937df37cdcecaf5663b3cabe0c8ff79b18165)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32433b6c6c6cdc44acb9c36a5cf8c85a447044ecd3796fe034c7c2917aa130af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__544cc8e4c2eb187e9d1e36c5544b34d2b06e123f1c58c15637f4ebb24dc07a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetActionSubscriber]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetActionSubscriber]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetActionSubscriber]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf5277e924bab1da4ac97363053dd17c7810615efc0d88530ebae909a2d2d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BudgetsBudgetActionSubscriberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionSubscriberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac48f2ceeb47a2235ee3928258e62834d7d1a6d5daf71dc0f658e2fa5c2e9b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionTypeInput")
    def subscription_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8880a7d0360859b3fe046e6d54e02dff9e743697ec2bd568ab846bebbd2488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionType")
    def subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionType"))

    @subscription_type.setter
    def subscription_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37335349e6c8baa0cf7bee90d14b2942583223ff3a7dc3cd2233c3258a52648f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionSubscriber]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionSubscriber]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionSubscriber]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da4206914422f5cd5bf999ed4c616c4465ae789a65597937fe5f1263af12422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BudgetsBudgetActionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#create BudgetsBudgetAction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#delete BudgetsBudgetAction#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#update BudgetsBudgetAction#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb373ad4989d67cae81ea38eb8be9e2194ddf00a821b328f49a333624b53e91e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#create BudgetsBudgetAction#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#delete BudgetsBudgetAction#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget_action#update BudgetsBudgetAction#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetActionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetActionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudgetAction.BudgetsBudgetActionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bdbfc5fcf9b66f8e9fe6b641bf077f93577a1e17e22fcfd613d7e2b6eff4d23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b691e46d43edf4169f98587fed7ed9043d73039c15aa36480b4fc798bf62a5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b69d3421b31a496605cc8b9333a9d2ef078796d5aa86a30eb86f379ccfbf9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0b98b818a0d3c1e87be5cd7c38b168a5b9d4675bea336f7b3f66feb1676dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaefdb40468bea4a54b4db2d8d6ce5d0eede268ca001d074e0b14678ff2f030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BudgetsBudgetAction",
    "BudgetsBudgetActionActionThreshold",
    "BudgetsBudgetActionActionThresholdOutputReference",
    "BudgetsBudgetActionConfig",
    "BudgetsBudgetActionDefinition",
    "BudgetsBudgetActionDefinitionIamActionDefinition",
    "BudgetsBudgetActionDefinitionIamActionDefinitionOutputReference",
    "BudgetsBudgetActionDefinitionOutputReference",
    "BudgetsBudgetActionDefinitionScpActionDefinition",
    "BudgetsBudgetActionDefinitionScpActionDefinitionOutputReference",
    "BudgetsBudgetActionDefinitionSsmActionDefinition",
    "BudgetsBudgetActionDefinitionSsmActionDefinitionOutputReference",
    "BudgetsBudgetActionSubscriber",
    "BudgetsBudgetActionSubscriberList",
    "BudgetsBudgetActionSubscriberOutputReference",
    "BudgetsBudgetActionTimeouts",
    "BudgetsBudgetActionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5cc4614ac9377b337ca59a5b7d0ec386bc57e3af9804dcba7b716a52f07397f9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action_threshold: typing.Union[BudgetsBudgetActionActionThreshold, typing.Dict[builtins.str, typing.Any]],
    action_type: builtins.str,
    approval_model: builtins.str,
    budget_name: builtins.str,
    definition: typing.Union[BudgetsBudgetActionDefinition, typing.Dict[builtins.str, typing.Any]],
    execution_role_arn: builtins.str,
    notification_type: builtins.str,
    subscriber: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetActionSubscriber, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BudgetsBudgetActionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ed3d4c5000b211d117292a99216e73406444bc1d23bce5f056e9c3551627ecf7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ca070abc7d5d4338eb3e28238adf9129dba09b9e36123c746d3f77ecec6e75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetActionSubscriber, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d81ac225f7232a09c72255e3ae580a7d882e8ce688eaf45fdd8f9a7b87f21e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0303fc267d98dfc5a69e9e6e915bd3294954cf8f81ea958c135c46faed849d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230e95006d76beb029eea0bcd6f268a1b5559aff0f9605f489eb9d6ec59144b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082d971da1fb5059ff56f2b33f5b42d1f75f4c6fde66ba5ab22bf27c35fa4476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aae4d668e3abba07ed32a5a46fd0b7511b210fb7f2938dce6c5a8c21120af54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ac2303d8526c6ddcb208b866e0b46cda67716f8cd1cd12935749b6d70db900(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce012f987676c68c9fca25d00f8d4598eee84f9444a0350aa2c5e914477dd8ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74eff3a29eac5fbfad8bb07341ae88f0065539b3181db38f3fc35a04b9d6b773(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee4c19c5c5e92c8554a3a0b3d3614bac3ebf095f1bcce7975f7c2c8921dd5dd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969ad55b4f569798a08b7fd4d3232a99c156e7b9b911524cb2fc868d14de29cb(
    *,
    action_threshold_type: builtins.str,
    action_threshold_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728fb85665a947b2849bbc21009cae8bdae3cd50864642dee9d999550bfb25cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64eb8aa35c604d649324269e6b32c6d47ace582e93baea3bc4a0614d94eba80e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657a8375609eb068b04eda9a4a3cf4cc582131bb823b38fe1726274188785152(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374d192628d6a5116facd30b4b9d8b7ba456ee56a952293fed7dcd8fbefd486d(
    value: typing.Optional[BudgetsBudgetActionActionThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83079e3e89641d434e327b6fadf9df8ac24bec06d87cab175e28149a9320bf87(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_threshold: typing.Union[BudgetsBudgetActionActionThreshold, typing.Dict[builtins.str, typing.Any]],
    action_type: builtins.str,
    approval_model: builtins.str,
    budget_name: builtins.str,
    definition: typing.Union[BudgetsBudgetActionDefinition, typing.Dict[builtins.str, typing.Any]],
    execution_role_arn: builtins.str,
    notification_type: builtins.str,
    subscriber: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetActionSubscriber, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BudgetsBudgetActionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca62c8f9bd7bc06d3b70c86edc661bbca6ecdedf4d890ce46f2de0bcb311b40(
    *,
    iam_action_definition: typing.Optional[typing.Union[BudgetsBudgetActionDefinitionIamActionDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    scp_action_definition: typing.Optional[typing.Union[BudgetsBudgetActionDefinitionScpActionDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
    ssm_action_definition: typing.Optional[typing.Union[BudgetsBudgetActionDefinitionSsmActionDefinition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b356ac953972fb4bcdd57859b09bfc473a994dbfcfdbf2591775dbd4d2b2f69f(
    *,
    policy_arn: builtins.str,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a21158b0ce188949e59f18ac4daa4f8715edcd711f71ea757f2dca249c3cf6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6cbd448dc395dcb85d58a4e4d303f91bd3ecd43c241beb86cb2356f36e9370(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2deadcee54111b6e66ca2c20a36b5c48daacc500d9472219c21069c48bc5871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95bf8cc9652dc6812cc9fa3cef3852d5ed9d8e2d63a6d77290a11ad7934ee2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2953a8ebabcc91c859673feb9ce3184851bdb557fee32da9ec8a9074b8616f93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e48851aa76f6d42c06aeff08e27b94c1c11eb85c16f5e989589811a99570f4(
    value: typing.Optional[BudgetsBudgetActionDefinitionIamActionDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61cbbcaf8f8b37b76ccc780d17bc4b35e86ff4042968fd3663eff7e032c3fe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e89efe3094f8cbb59b469b69072178fdf98ff3aec463357bef30713cbf9ef33(
    value: typing.Optional[BudgetsBudgetActionDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acaac0d5bd2c2475ded464cac23241c8f214bacb4a7d89cc3c0074d68a52ed4(
    *,
    policy_id: builtins.str,
    target_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d6407c31970516c8e85d7815a9192b6e5e3e292cad462d0e670430b6604cb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11dfb25232f1e4a7ceea6994a91f8d96fb34c051f0aa1fcd4320fa7ac7b8ce64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f604532448e3ebcdbb48a5d2d5b48a9daf5d6359cc142a6f97b64d367e16d8fc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12c0241fd4c64d47f5be5d950ef4905cb054868d42d3bbec92fe858f98bd43e(
    value: typing.Optional[BudgetsBudgetActionDefinitionScpActionDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8215d1bd4d21cc7102eb56c221eb801be0269eefe2a7ba43e6ee28cd07a639a0(
    *,
    action_sub_type: builtins.str,
    instance_ids: typing.Sequence[builtins.str],
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644810482673aeece703f9e3293305edd9409f33122fd00523530be990724695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e818772b2a4d2c299059ceb743f4d5f48157aab5eaa71b383554304b0c53548b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bc0fef9eee3bb1652f6a91294e6aefadcda3d7f3f66e39d057fda6718b566f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a94bcaea3eae72c3e7fb157a1536a4761e22a0262fa662c6fb4a68ee14424c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9267d338e741d49d53fa4aa5f5e973f85fc74173347fe0a4972f4295e7ae183(
    value: typing.Optional[BudgetsBudgetActionDefinitionSsmActionDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a5b8ff2e5d90cde37dcd685b78b8538b03dce760acbeedfa1ce26973be8d2a(
    *,
    address: builtins.str,
    subscription_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb95bdbcfefe4fdf64f58fedb48353c337fc80294f3b9c5cfd83f7c7471f368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617d0fc8cbd930d23e3105958781ef967137186b6370e3cf06e68fe87deb7fac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772df9e95a5545e97417630fdfc937df37cdcecaf5663b3cabe0c8ff79b18165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32433b6c6c6cdc44acb9c36a5cf8c85a447044ecd3796fe034c7c2917aa130af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544cc8e4c2eb187e9d1e36c5544b34d2b06e123f1c58c15637f4ebb24dc07a10(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf5277e924bab1da4ac97363053dd17c7810615efc0d88530ebae909a2d2d2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetActionSubscriber]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac48f2ceeb47a2235ee3928258e62834d7d1a6d5daf71dc0f658e2fa5c2e9b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8880a7d0360859b3fe046e6d54e02dff9e743697ec2bd568ab846bebbd2488(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37335349e6c8baa0cf7bee90d14b2942583223ff3a7dc3cd2233c3258a52648f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da4206914422f5cd5bf999ed4c616c4465ae789a65597937fe5f1263af12422(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionSubscriber]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb373ad4989d67cae81ea38eb8be9e2194ddf00a821b328f49a333624b53e91e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdbfc5fcf9b66f8e9fe6b641bf077f93577a1e17e22fcfd613d7e2b6eff4d23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b691e46d43edf4169f98587fed7ed9043d73039c15aa36480b4fc798bf62a5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b69d3421b31a496605cc8b9333a9d2ef078796d5aa86a30eb86f379ccfbf9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0b98b818a0d3c1e87be5cd7c38b168a5b9d4675bea336f7b3f66feb1676dfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaefdb40468bea4a54b4db2d8d6ce5d0eede268ca001d074e0b14678ff2f030(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetActionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
