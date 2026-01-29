r'''
# `aws_budgets_budget`

Refer to the Terraform Registry for docs: [`aws_budgets_budget`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget).
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


class BudgetsBudget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudget",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget aws_budgets_budget}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        budget_type: builtins.str,
        time_unit: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        auto_adjust_data: typing.Optional[typing.Union["BudgetsBudgetAutoAdjustData", typing.Dict[builtins.str, typing.Any]]] = None,
        billing_view_arn: typing.Optional[builtins.str] = None,
        cost_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetCostFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cost_types: typing.Optional[typing.Union["BudgetsBudgetCostTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        limit_amount: typing.Optional[builtins.str] = None,
        limit_unit: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        notification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetNotification", typing.Dict[builtins.str, typing.Any]]]]] = None,
        planned_limit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetPlannedLimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        time_period_end: typing.Optional[builtins.str] = None,
        time_period_start: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget aws_budgets_budget} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param budget_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#budget_type BudgetsBudget#budget_type}.
        :param time_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_unit BudgetsBudget#time_unit}.
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#account_id BudgetsBudget#account_id}.
        :param auto_adjust_data: auto_adjust_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#auto_adjust_data BudgetsBudget#auto_adjust_data}
        :param billing_view_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#billing_view_arn BudgetsBudget#billing_view_arn}.
        :param cost_filter: cost_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#cost_filter BudgetsBudget#cost_filter}
        :param cost_types: cost_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#cost_types BudgetsBudget#cost_types}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#id BudgetsBudget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param limit_amount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#limit_amount BudgetsBudget#limit_amount}.
        :param limit_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#limit_unit BudgetsBudget#limit_unit}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name BudgetsBudget#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name_prefix BudgetsBudget#name_prefix}.
        :param notification: notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#notification BudgetsBudget#notification}
        :param planned_limit: planned_limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#planned_limit BudgetsBudget#planned_limit}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#tags BudgetsBudget#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#tags_all BudgetsBudget#tags_all}.
        :param time_period_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_period_end BudgetsBudget#time_period_end}.
        :param time_period_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_period_start BudgetsBudget#time_period_start}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76737ca33fc598975c9af917298840a9a3dae7ae89c8e21c49d6df52621ee629)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BudgetsBudgetConfig(
            budget_type=budget_type,
            time_unit=time_unit,
            account_id=account_id,
            auto_adjust_data=auto_adjust_data,
            billing_view_arn=billing_view_arn,
            cost_filter=cost_filter,
            cost_types=cost_types,
            id=id,
            limit_amount=limit_amount,
            limit_unit=limit_unit,
            name=name,
            name_prefix=name_prefix,
            notification=notification,
            planned_limit=planned_limit,
            tags=tags,
            tags_all=tags_all,
            time_period_end=time_period_end,
            time_period_start=time_period_start,
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
        '''Generates CDKTF code for importing a BudgetsBudget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BudgetsBudget to import.
        :param import_from_id: The id of the existing BudgetsBudget that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BudgetsBudget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a6c480fd0be4b86e8ca514da985515e5532fb88c8fca8eed6278de2aed6429)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoAdjustData")
    def put_auto_adjust_data(
        self,
        *,
        auto_adjust_type: builtins.str,
        historical_options: typing.Optional[typing.Union["BudgetsBudgetAutoAdjustDataHistoricalOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_adjust_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#auto_adjust_type BudgetsBudget#auto_adjust_type}.
        :param historical_options: historical_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#historical_options BudgetsBudget#historical_options}
        '''
        value = BudgetsBudgetAutoAdjustData(
            auto_adjust_type=auto_adjust_type, historical_options=historical_options
        )

        return typing.cast(None, jsii.invoke(self, "putAutoAdjustData", [value]))

    @jsii.member(jsii_name="putCostFilter")
    def put_cost_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetCostFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f06341089f78ff988a122044eeeb601250760fb4824a80066c4a6d5664092f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCostFilter", [value]))

    @jsii.member(jsii_name="putCostTypes")
    def put_cost_types(
        self,
        *,
        include_credit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_discount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_other_subscription: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_recurring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_refund: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_subscription: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_tax: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_upfront: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_amortized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_blended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param include_credit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_credit BudgetsBudget#include_credit}.
        :param include_discount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_discount BudgetsBudget#include_discount}.
        :param include_other_subscription: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_other_subscription BudgetsBudget#include_other_subscription}.
        :param include_recurring: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_recurring BudgetsBudget#include_recurring}.
        :param include_refund: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_refund BudgetsBudget#include_refund}.
        :param include_subscription: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_subscription BudgetsBudget#include_subscription}.
        :param include_support: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_support BudgetsBudget#include_support}.
        :param include_tax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_tax BudgetsBudget#include_tax}.
        :param include_upfront: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_upfront BudgetsBudget#include_upfront}.
        :param use_amortized: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#use_amortized BudgetsBudget#use_amortized}.
        :param use_blended: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#use_blended BudgetsBudget#use_blended}.
        '''
        value = BudgetsBudgetCostTypes(
            include_credit=include_credit,
            include_discount=include_discount,
            include_other_subscription=include_other_subscription,
            include_recurring=include_recurring,
            include_refund=include_refund,
            include_subscription=include_subscription,
            include_support=include_support,
            include_tax=include_tax,
            include_upfront=include_upfront,
            use_amortized=use_amortized,
            use_blended=use_blended,
        )

        return typing.cast(None, jsii.invoke(self, "putCostTypes", [value]))

    @jsii.member(jsii_name="putNotification")
    def put_notification(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetNotification", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaa8adeb5bbefa30aaabfa06ce5161ad331d218407dca82a39edb36dfb9b3d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotification", [value]))

    @jsii.member(jsii_name="putPlannedLimit")
    def put_planned_limit(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetPlannedLimit", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a84a1be9bf0d1d2fd703292a428d3a5b855f00efd09eeafea74af295aa152d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlannedLimit", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAutoAdjustData")
    def reset_auto_adjust_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoAdjustData", []))

    @jsii.member(jsii_name="resetBillingViewArn")
    def reset_billing_view_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingViewArn", []))

    @jsii.member(jsii_name="resetCostFilter")
    def reset_cost_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostFilter", []))

    @jsii.member(jsii_name="resetCostTypes")
    def reset_cost_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostTypes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLimitAmount")
    def reset_limit_amount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitAmount", []))

    @jsii.member(jsii_name="resetLimitUnit")
    def reset_limit_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitUnit", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetNotification")
    def reset_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotification", []))

    @jsii.member(jsii_name="resetPlannedLimit")
    def reset_planned_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlannedLimit", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimePeriodEnd")
    def reset_time_period_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimePeriodEnd", []))

    @jsii.member(jsii_name="resetTimePeriodStart")
    def reset_time_period_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimePeriodStart", []))

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
    @jsii.member(jsii_name="autoAdjustData")
    def auto_adjust_data(self) -> "BudgetsBudgetAutoAdjustDataOutputReference":
        return typing.cast("BudgetsBudgetAutoAdjustDataOutputReference", jsii.get(self, "autoAdjustData"))

    @builtins.property
    @jsii.member(jsii_name="costFilter")
    def cost_filter(self) -> "BudgetsBudgetCostFilterList":
        return typing.cast("BudgetsBudgetCostFilterList", jsii.get(self, "costFilter"))

    @builtins.property
    @jsii.member(jsii_name="costTypes")
    def cost_types(self) -> "BudgetsBudgetCostTypesOutputReference":
        return typing.cast("BudgetsBudgetCostTypesOutputReference", jsii.get(self, "costTypes"))

    @builtins.property
    @jsii.member(jsii_name="notification")
    def notification(self) -> "BudgetsBudgetNotificationList":
        return typing.cast("BudgetsBudgetNotificationList", jsii.get(self, "notification"))

    @builtins.property
    @jsii.member(jsii_name="plannedLimit")
    def planned_limit(self) -> "BudgetsBudgetPlannedLimitList":
        return typing.cast("BudgetsBudgetPlannedLimitList", jsii.get(self, "plannedLimit"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoAdjustDataInput")
    def auto_adjust_data_input(self) -> typing.Optional["BudgetsBudgetAutoAdjustData"]:
        return typing.cast(typing.Optional["BudgetsBudgetAutoAdjustData"], jsii.get(self, "autoAdjustDataInput"))

    @builtins.property
    @jsii.member(jsii_name="billingViewArnInput")
    def billing_view_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingViewArnInput"))

    @builtins.property
    @jsii.member(jsii_name="budgetTypeInput")
    def budget_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "budgetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="costFilterInput")
    def cost_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetCostFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetCostFilter"]]], jsii.get(self, "costFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="costTypesInput")
    def cost_types_input(self) -> typing.Optional["BudgetsBudgetCostTypes"]:
        return typing.cast(typing.Optional["BudgetsBudgetCostTypes"], jsii.get(self, "costTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="limitAmountInput")
    def limit_amount_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitAmountInput"))

    @builtins.property
    @jsii.member(jsii_name="limitUnitInput")
    def limit_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationInput")
    def notification_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetNotification"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetNotification"]]], jsii.get(self, "notificationInput"))

    @builtins.property
    @jsii.member(jsii_name="plannedLimitInput")
    def planned_limit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetPlannedLimit"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetPlannedLimit"]]], jsii.get(self, "plannedLimitInput"))

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
    @jsii.member(jsii_name="timePeriodEndInput")
    def time_period_end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timePeriodEndInput"))

    @builtins.property
    @jsii.member(jsii_name="timePeriodStartInput")
    def time_period_start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timePeriodStartInput"))

    @builtins.property
    @jsii.member(jsii_name="timeUnitInput")
    def time_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15ef7362a1b4ee88090b0ce5b34f9c80b21b459d8d350f676f281ccf03fb0a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingViewArn")
    def billing_view_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingViewArn"))

    @billing_view_arn.setter
    def billing_view_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6543176334b8509d714f690eb78ed806c5bb8eb59675ab2e9a4cddc877ca61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingViewArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="budgetType")
    def budget_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "budgetType"))

    @budget_type.setter
    def budget_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459833eb52ac22cbf5c49e72ab3e64a813d7013855e20ec96f2291d538229590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "budgetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f956ff886821d71349fcb826645aed0b2a1d1943d05938340217caa95d4ca0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitAmount")
    def limit_amount(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limitAmount"))

    @limit_amount.setter
    def limit_amount(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feca239b57be2b84ca570bdf77d06b697cdaac99bc549b9a63108964b20c24fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitAmount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitUnit")
    def limit_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limitUnit"))

    @limit_unit.setter
    def limit_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520ca7be74e31347b70efc6c827b7fe8b2b1a4dada5d758698ce0fa8c531862d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b8d5cfa6cc5239bacb9252f8ac63f336cb4bd278216348d5f5a1b90dde138b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af50a3ab536ca79153bf01e2c8d20de347355e60f272935458f37d189f94e2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16711ce551710d1209d1175e4282ef7d60c2f836002ae0c5a80f3b3cc3e8cb56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e219b2c0bfdefe532c5c6bfdefbeef6fec428314f75686ad6d704eab60e195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timePeriodEnd")
    def time_period_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timePeriodEnd"))

    @time_period_end.setter
    def time_period_end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d69601081ba3ec7ea08d28c68fb13af9c4e6b4dff11bee4dec3929c52f73a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timePeriodEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timePeriodStart")
    def time_period_start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timePeriodStart"))

    @time_period_start.setter
    def time_period_start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f611651ed4ca9d92147fce08c1f857961f2bd2e161d2766a682f8208abcad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timePeriodStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfd96ab9cb4301eb5223a2635bf114f81c64a69ab72a4c20785281a22ecf67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetAutoAdjustData",
    jsii_struct_bases=[],
    name_mapping={
        "auto_adjust_type": "autoAdjustType",
        "historical_options": "historicalOptions",
    },
)
class BudgetsBudgetAutoAdjustData:
    def __init__(
        self,
        *,
        auto_adjust_type: builtins.str,
        historical_options: typing.Optional[typing.Union["BudgetsBudgetAutoAdjustDataHistoricalOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_adjust_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#auto_adjust_type BudgetsBudget#auto_adjust_type}.
        :param historical_options: historical_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#historical_options BudgetsBudget#historical_options}
        '''
        if isinstance(historical_options, dict):
            historical_options = BudgetsBudgetAutoAdjustDataHistoricalOptions(**historical_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b9aa0f916ddcca9e02671f6e003215d9445086e4c84660cac834a7381c0b61)
            check_type(argname="argument auto_adjust_type", value=auto_adjust_type, expected_type=type_hints["auto_adjust_type"])
            check_type(argname="argument historical_options", value=historical_options, expected_type=type_hints["historical_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_adjust_type": auto_adjust_type,
        }
        if historical_options is not None:
            self._values["historical_options"] = historical_options

    @builtins.property
    def auto_adjust_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#auto_adjust_type BudgetsBudget#auto_adjust_type}.'''
        result = self._values.get("auto_adjust_type")
        assert result is not None, "Required property 'auto_adjust_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def historical_options(
        self,
    ) -> typing.Optional["BudgetsBudgetAutoAdjustDataHistoricalOptions"]:
        '''historical_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#historical_options BudgetsBudget#historical_options}
        '''
        result = self._values.get("historical_options")
        return typing.cast(typing.Optional["BudgetsBudgetAutoAdjustDataHistoricalOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetAutoAdjustData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetAutoAdjustDataHistoricalOptions",
    jsii_struct_bases=[],
    name_mapping={"budget_adjustment_period": "budgetAdjustmentPeriod"},
)
class BudgetsBudgetAutoAdjustDataHistoricalOptions:
    def __init__(self, *, budget_adjustment_period: jsii.Number) -> None:
        '''
        :param budget_adjustment_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#budget_adjustment_period BudgetsBudget#budget_adjustment_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5883c1eef5d51bc7120c4feb15744d8a108c87a5e71c188d698b5ca56d86375)
            check_type(argname="argument budget_adjustment_period", value=budget_adjustment_period, expected_type=type_hints["budget_adjustment_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "budget_adjustment_period": budget_adjustment_period,
        }

    @builtins.property
    def budget_adjustment_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#budget_adjustment_period BudgetsBudget#budget_adjustment_period}.'''
        result = self._values.get("budget_adjustment_period")
        assert result is not None, "Required property 'budget_adjustment_period' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetAutoAdjustDataHistoricalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetAutoAdjustDataHistoricalOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetAutoAdjustDataHistoricalOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8829e7499be69874f2fb4264e0a23face7422d3a6cf5485f1bf4096c8afba78c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="lookbackAvailablePeriods")
    def lookback_available_periods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lookbackAvailablePeriods"))

    @builtins.property
    @jsii.member(jsii_name="budgetAdjustmentPeriodInput")
    def budget_adjustment_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "budgetAdjustmentPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="budgetAdjustmentPeriod")
    def budget_adjustment_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "budgetAdjustmentPeriod"))

    @budget_adjustment_period.setter
    def budget_adjustment_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6534b0008fa708f5d6a31b6fc27e00d1a9cfab57238e71b8bf1bc99aafc3d26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "budgetAdjustmentPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BudgetsBudgetAutoAdjustDataHistoricalOptions]:
        return typing.cast(typing.Optional[BudgetsBudgetAutoAdjustDataHistoricalOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetAutoAdjustDataHistoricalOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdb4cdc67fc001521a94e071e16df87740f01b0aa52b6f5a3355506473cbc51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BudgetsBudgetAutoAdjustDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetAutoAdjustDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f8c22e4d71da92dd4c10b71877ae5857ca32533326ee591dd4c88fbba6a7ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHistoricalOptions")
    def put_historical_options(self, *, budget_adjustment_period: jsii.Number) -> None:
        '''
        :param budget_adjustment_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#budget_adjustment_period BudgetsBudget#budget_adjustment_period}.
        '''
        value = BudgetsBudgetAutoAdjustDataHistoricalOptions(
            budget_adjustment_period=budget_adjustment_period
        )

        return typing.cast(None, jsii.invoke(self, "putHistoricalOptions", [value]))

    @jsii.member(jsii_name="resetHistoricalOptions")
    def reset_historical_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHistoricalOptions", []))

    @builtins.property
    @jsii.member(jsii_name="historicalOptions")
    def historical_options(
        self,
    ) -> BudgetsBudgetAutoAdjustDataHistoricalOptionsOutputReference:
        return typing.cast(BudgetsBudgetAutoAdjustDataHistoricalOptionsOutputReference, jsii.get(self, "historicalOptions"))

    @builtins.property
    @jsii.member(jsii_name="lastAutoAdjustTime")
    def last_auto_adjust_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastAutoAdjustTime"))

    @builtins.property
    @jsii.member(jsii_name="autoAdjustTypeInput")
    def auto_adjust_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoAdjustTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="historicalOptionsInput")
    def historical_options_input(
        self,
    ) -> typing.Optional[BudgetsBudgetAutoAdjustDataHistoricalOptions]:
        return typing.cast(typing.Optional[BudgetsBudgetAutoAdjustDataHistoricalOptions], jsii.get(self, "historicalOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoAdjustType")
    def auto_adjust_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoAdjustType"))

    @auto_adjust_type.setter
    def auto_adjust_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61834abc21fb1e048efdf7bd8ab6e980e91ce048696c1d42a517cacbb3ee6a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoAdjustType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BudgetsBudgetAutoAdjustData]:
        return typing.cast(typing.Optional[BudgetsBudgetAutoAdjustData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BudgetsBudgetAutoAdjustData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4efeca2508bf95a07f0cb3e30430f788a72ccf4e533f7a976ec461bed27e48ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "budget_type": "budgetType",
        "time_unit": "timeUnit",
        "account_id": "accountId",
        "auto_adjust_data": "autoAdjustData",
        "billing_view_arn": "billingViewArn",
        "cost_filter": "costFilter",
        "cost_types": "costTypes",
        "id": "id",
        "limit_amount": "limitAmount",
        "limit_unit": "limitUnit",
        "name": "name",
        "name_prefix": "namePrefix",
        "notification": "notification",
        "planned_limit": "plannedLimit",
        "tags": "tags",
        "tags_all": "tagsAll",
        "time_period_end": "timePeriodEnd",
        "time_period_start": "timePeriodStart",
    },
)
class BudgetsBudgetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        budget_type: builtins.str,
        time_unit: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        auto_adjust_data: typing.Optional[typing.Union[BudgetsBudgetAutoAdjustData, typing.Dict[builtins.str, typing.Any]]] = None,
        billing_view_arn: typing.Optional[builtins.str] = None,
        cost_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetCostFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cost_types: typing.Optional[typing.Union["BudgetsBudgetCostTypes", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        limit_amount: typing.Optional[builtins.str] = None,
        limit_unit: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        notification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetNotification", typing.Dict[builtins.str, typing.Any]]]]] = None,
        planned_limit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BudgetsBudgetPlannedLimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        time_period_end: typing.Optional[builtins.str] = None,
        time_period_start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param budget_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#budget_type BudgetsBudget#budget_type}.
        :param time_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_unit BudgetsBudget#time_unit}.
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#account_id BudgetsBudget#account_id}.
        :param auto_adjust_data: auto_adjust_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#auto_adjust_data BudgetsBudget#auto_adjust_data}
        :param billing_view_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#billing_view_arn BudgetsBudget#billing_view_arn}.
        :param cost_filter: cost_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#cost_filter BudgetsBudget#cost_filter}
        :param cost_types: cost_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#cost_types BudgetsBudget#cost_types}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#id BudgetsBudget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param limit_amount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#limit_amount BudgetsBudget#limit_amount}.
        :param limit_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#limit_unit BudgetsBudget#limit_unit}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name BudgetsBudget#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name_prefix BudgetsBudget#name_prefix}.
        :param notification: notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#notification BudgetsBudget#notification}
        :param planned_limit: planned_limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#planned_limit BudgetsBudget#planned_limit}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#tags BudgetsBudget#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#tags_all BudgetsBudget#tags_all}.
        :param time_period_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_period_end BudgetsBudget#time_period_end}.
        :param time_period_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_period_start BudgetsBudget#time_period_start}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auto_adjust_data, dict):
            auto_adjust_data = BudgetsBudgetAutoAdjustData(**auto_adjust_data)
        if isinstance(cost_types, dict):
            cost_types = BudgetsBudgetCostTypes(**cost_types)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9512b42f8024519b0596878e835b27f72449e6e26ab7ba149836dbf8f9a72d19)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument budget_type", value=budget_type, expected_type=type_hints["budget_type"])
            check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument auto_adjust_data", value=auto_adjust_data, expected_type=type_hints["auto_adjust_data"])
            check_type(argname="argument billing_view_arn", value=billing_view_arn, expected_type=type_hints["billing_view_arn"])
            check_type(argname="argument cost_filter", value=cost_filter, expected_type=type_hints["cost_filter"])
            check_type(argname="argument cost_types", value=cost_types, expected_type=type_hints["cost_types"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument limit_amount", value=limit_amount, expected_type=type_hints["limit_amount"])
            check_type(argname="argument limit_unit", value=limit_unit, expected_type=type_hints["limit_unit"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument notification", value=notification, expected_type=type_hints["notification"])
            check_type(argname="argument planned_limit", value=planned_limit, expected_type=type_hints["planned_limit"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument time_period_end", value=time_period_end, expected_type=type_hints["time_period_end"])
            check_type(argname="argument time_period_start", value=time_period_start, expected_type=type_hints["time_period_start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "budget_type": budget_type,
            "time_unit": time_unit,
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
        if auto_adjust_data is not None:
            self._values["auto_adjust_data"] = auto_adjust_data
        if billing_view_arn is not None:
            self._values["billing_view_arn"] = billing_view_arn
        if cost_filter is not None:
            self._values["cost_filter"] = cost_filter
        if cost_types is not None:
            self._values["cost_types"] = cost_types
        if id is not None:
            self._values["id"] = id
        if limit_amount is not None:
            self._values["limit_amount"] = limit_amount
        if limit_unit is not None:
            self._values["limit_unit"] = limit_unit
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if notification is not None:
            self._values["notification"] = notification
        if planned_limit is not None:
            self._values["planned_limit"] = planned_limit
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if time_period_end is not None:
            self._values["time_period_end"] = time_period_end
        if time_period_start is not None:
            self._values["time_period_start"] = time_period_start

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
    def budget_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#budget_type BudgetsBudget#budget_type}.'''
        result = self._values.get("budget_type")
        assert result is not None, "Required property 'budget_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_unit BudgetsBudget#time_unit}.'''
        result = self._values.get("time_unit")
        assert result is not None, "Required property 'time_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#account_id BudgetsBudget#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_adjust_data(self) -> typing.Optional[BudgetsBudgetAutoAdjustData]:
        '''auto_adjust_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#auto_adjust_data BudgetsBudget#auto_adjust_data}
        '''
        result = self._values.get("auto_adjust_data")
        return typing.cast(typing.Optional[BudgetsBudgetAutoAdjustData], result)

    @builtins.property
    def billing_view_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#billing_view_arn BudgetsBudget#billing_view_arn}.'''
        result = self._values.get("billing_view_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cost_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetCostFilter"]]]:
        '''cost_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#cost_filter BudgetsBudget#cost_filter}
        '''
        result = self._values.get("cost_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetCostFilter"]]], result)

    @builtins.property
    def cost_types(self) -> typing.Optional["BudgetsBudgetCostTypes"]:
        '''cost_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#cost_types BudgetsBudget#cost_types}
        '''
        result = self._values.get("cost_types")
        return typing.cast(typing.Optional["BudgetsBudgetCostTypes"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#id BudgetsBudget#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_amount(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#limit_amount BudgetsBudget#limit_amount}.'''
        result = self._values.get("limit_amount")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#limit_unit BudgetsBudget#limit_unit}.'''
        result = self._values.get("limit_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name BudgetsBudget#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name_prefix BudgetsBudget#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetNotification"]]]:
        '''notification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#notification BudgetsBudget#notification}
        '''
        result = self._values.get("notification")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetNotification"]]], result)

    @builtins.property
    def planned_limit(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetPlannedLimit"]]]:
        '''planned_limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#planned_limit BudgetsBudget#planned_limit}
        '''
        result = self._values.get("planned_limit")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BudgetsBudgetPlannedLimit"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#tags BudgetsBudget#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#tags_all BudgetsBudget#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def time_period_end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_period_end BudgetsBudget#time_period_end}.'''
        result = self._values.get("time_period_end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_period_start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#time_period_start BudgetsBudget#time_period_start}.'''
        result = self._values.get("time_period_start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetCostFilter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class BudgetsBudgetCostFilter:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name BudgetsBudget#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#values BudgetsBudget#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067902cb2904b6eb28907a79e613d62ea6a16ce8acbb99e3466465f10a05ffad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#name BudgetsBudget#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#values BudgetsBudget#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetCostFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetCostFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetCostFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11af638c8a4804752a1e727b07b7a6e026f89d68312529533f7abec115bd2152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BudgetsBudgetCostFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871e3854dff2865fa9e232587c81475c3e26576b9b97abf8e907276cb5d7e33f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BudgetsBudgetCostFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72606cb8f79f61338faa42a6592da9637f6b094414b9a4a340f6ca6ec3b14d58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb8e2106003248e09ecd0299f3c5aecae33101c5477f1dcc5c5f8bb2e877292f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__760f5aa6d17ff1c08dac082656a18e164f0485ed885874cefdfe541df9c51129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetCostFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetCostFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetCostFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef61ea6a95384b1f2d7757b5e965bbe0a872b20358968dfbe2f3f23932aa1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BudgetsBudgetCostFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetCostFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e486230479ba731ee132d5b1e3387ee1c7725738397c2f2638762132eb44f528)
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
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6d3d0574fddb63dfad5b08b15a609208977868fcd100e6156dedaedaa3a7d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66af87f59d88f533144d6ea4b37e7a3dc9b54108744479024a4be96ce962040c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetCostFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetCostFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetCostFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012bc92432a6ef4cc7773ee510974814f74f3de1c6b321c397f95f58ea6975c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetCostTypes",
    jsii_struct_bases=[],
    name_mapping={
        "include_credit": "includeCredit",
        "include_discount": "includeDiscount",
        "include_other_subscription": "includeOtherSubscription",
        "include_recurring": "includeRecurring",
        "include_refund": "includeRefund",
        "include_subscription": "includeSubscription",
        "include_support": "includeSupport",
        "include_tax": "includeTax",
        "include_upfront": "includeUpfront",
        "use_amortized": "useAmortized",
        "use_blended": "useBlended",
    },
)
class BudgetsBudgetCostTypes:
    def __init__(
        self,
        *,
        include_credit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_discount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_other_subscription: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_recurring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_refund: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_subscription: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_tax: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_upfront: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_amortized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_blended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param include_credit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_credit BudgetsBudget#include_credit}.
        :param include_discount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_discount BudgetsBudget#include_discount}.
        :param include_other_subscription: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_other_subscription BudgetsBudget#include_other_subscription}.
        :param include_recurring: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_recurring BudgetsBudget#include_recurring}.
        :param include_refund: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_refund BudgetsBudget#include_refund}.
        :param include_subscription: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_subscription BudgetsBudget#include_subscription}.
        :param include_support: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_support BudgetsBudget#include_support}.
        :param include_tax: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_tax BudgetsBudget#include_tax}.
        :param include_upfront: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_upfront BudgetsBudget#include_upfront}.
        :param use_amortized: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#use_amortized BudgetsBudget#use_amortized}.
        :param use_blended: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#use_blended BudgetsBudget#use_blended}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa5652375455474eb0aafd0ed3ccef32d8e747204b6b25d45efc5ca2f04f0ad)
            check_type(argname="argument include_credit", value=include_credit, expected_type=type_hints["include_credit"])
            check_type(argname="argument include_discount", value=include_discount, expected_type=type_hints["include_discount"])
            check_type(argname="argument include_other_subscription", value=include_other_subscription, expected_type=type_hints["include_other_subscription"])
            check_type(argname="argument include_recurring", value=include_recurring, expected_type=type_hints["include_recurring"])
            check_type(argname="argument include_refund", value=include_refund, expected_type=type_hints["include_refund"])
            check_type(argname="argument include_subscription", value=include_subscription, expected_type=type_hints["include_subscription"])
            check_type(argname="argument include_support", value=include_support, expected_type=type_hints["include_support"])
            check_type(argname="argument include_tax", value=include_tax, expected_type=type_hints["include_tax"])
            check_type(argname="argument include_upfront", value=include_upfront, expected_type=type_hints["include_upfront"])
            check_type(argname="argument use_amortized", value=use_amortized, expected_type=type_hints["use_amortized"])
            check_type(argname="argument use_blended", value=use_blended, expected_type=type_hints["use_blended"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_credit is not None:
            self._values["include_credit"] = include_credit
        if include_discount is not None:
            self._values["include_discount"] = include_discount
        if include_other_subscription is not None:
            self._values["include_other_subscription"] = include_other_subscription
        if include_recurring is not None:
            self._values["include_recurring"] = include_recurring
        if include_refund is not None:
            self._values["include_refund"] = include_refund
        if include_subscription is not None:
            self._values["include_subscription"] = include_subscription
        if include_support is not None:
            self._values["include_support"] = include_support
        if include_tax is not None:
            self._values["include_tax"] = include_tax
        if include_upfront is not None:
            self._values["include_upfront"] = include_upfront
        if use_amortized is not None:
            self._values["use_amortized"] = use_amortized
        if use_blended is not None:
            self._values["use_blended"] = use_blended

    @builtins.property
    def include_credit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_credit BudgetsBudget#include_credit}.'''
        result = self._values.get("include_credit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_discount(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_discount BudgetsBudget#include_discount}.'''
        result = self._values.get("include_discount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_other_subscription(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_other_subscription BudgetsBudget#include_other_subscription}.'''
        result = self._values.get("include_other_subscription")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_recurring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_recurring BudgetsBudget#include_recurring}.'''
        result = self._values.get("include_recurring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_refund(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_refund BudgetsBudget#include_refund}.'''
        result = self._values.get("include_refund")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_subscription(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_subscription BudgetsBudget#include_subscription}.'''
        result = self._values.get("include_subscription")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_support(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_support BudgetsBudget#include_support}.'''
        result = self._values.get("include_support")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_tax(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_tax BudgetsBudget#include_tax}.'''
        result = self._values.get("include_tax")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_upfront(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#include_upfront BudgetsBudget#include_upfront}.'''
        result = self._values.get("include_upfront")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_amortized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#use_amortized BudgetsBudget#use_amortized}.'''
        result = self._values.get("use_amortized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_blended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#use_blended BudgetsBudget#use_blended}.'''
        result = self._values.get("use_blended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetCostTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetCostTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetCostTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95bffd853788a04e7d9dfa9e7905542c0a09a4bb060b81e6f6f4e0859d30b7f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeCredit")
    def reset_include_credit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeCredit", []))

    @jsii.member(jsii_name="resetIncludeDiscount")
    def reset_include_discount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeDiscount", []))

    @jsii.member(jsii_name="resetIncludeOtherSubscription")
    def reset_include_other_subscription(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeOtherSubscription", []))

    @jsii.member(jsii_name="resetIncludeRecurring")
    def reset_include_recurring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRecurring", []))

    @jsii.member(jsii_name="resetIncludeRefund")
    def reset_include_refund(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRefund", []))

    @jsii.member(jsii_name="resetIncludeSubscription")
    def reset_include_subscription(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSubscription", []))

    @jsii.member(jsii_name="resetIncludeSupport")
    def reset_include_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSupport", []))

    @jsii.member(jsii_name="resetIncludeTax")
    def reset_include_tax(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTax", []))

    @jsii.member(jsii_name="resetIncludeUpfront")
    def reset_include_upfront(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeUpfront", []))

    @jsii.member(jsii_name="resetUseAmortized")
    def reset_use_amortized(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseAmortized", []))

    @jsii.member(jsii_name="resetUseBlended")
    def reset_use_blended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseBlended", []))

    @builtins.property
    @jsii.member(jsii_name="includeCreditInput")
    def include_credit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeCreditInput"))

    @builtins.property
    @jsii.member(jsii_name="includeDiscountInput")
    def include_discount_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeDiscountInput"))

    @builtins.property
    @jsii.member(jsii_name="includeOtherSubscriptionInput")
    def include_other_subscription_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeOtherSubscriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRecurringInput")
    def include_recurring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeRecurringInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRefundInput")
    def include_refund_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeRefundInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSubscriptionInput")
    def include_subscription_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSubscriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSupportInput")
    def include_support_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSupportInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTaxInput")
    def include_tax_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeTaxInput"))

    @builtins.property
    @jsii.member(jsii_name="includeUpfrontInput")
    def include_upfront_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeUpfrontInput"))

    @builtins.property
    @jsii.member(jsii_name="useAmortizedInput")
    def use_amortized_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAmortizedInput"))

    @builtins.property
    @jsii.member(jsii_name="useBlendedInput")
    def use_blended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useBlendedInput"))

    @builtins.property
    @jsii.member(jsii_name="includeCredit")
    def include_credit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeCredit"))

    @include_credit.setter
    def include_credit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e790f40c3035e449d7fd8ecdb2b64d021c19182eedc767d7197ab182a40f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeCredit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeDiscount")
    def include_discount(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeDiscount"))

    @include_discount.setter
    def include_discount(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674a7a31b056977555eb41101a3f73eb7f1f6bd024554134473ec8bd24f02dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeDiscount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeOtherSubscription")
    def include_other_subscription(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeOtherSubscription"))

    @include_other_subscription.setter
    def include_other_subscription(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f840e228ca0d0ddc2df7bdf1d9745740c5802094c96b9b3aab4642f6f2f7dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeOtherSubscription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRecurring")
    def include_recurring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeRecurring"))

    @include_recurring.setter
    def include_recurring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56977e67851475e36e6c50735d2459d5fc34a8a852bce55395d97dbe4f95b20a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRecurring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRefund")
    def include_refund(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeRefund"))

    @include_refund.setter
    def include_refund(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84803440b0f6cf8061bab0b328515d3b56e1fce5e6363a80e1a7771a239f5d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRefund", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSubscription")
    def include_subscription(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSubscription"))

    @include_subscription.setter
    def include_subscription(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e9093b71a1c72ce222b0523ebb80ced7166b8e2ea29d8b496d356e8fec8ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSubscription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSupport")
    def include_support(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSupport"))

    @include_support.setter
    def include_support(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4628e29ee81e459ea1a7aca78ccf628b59b331695832f9671d4ce964083908f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSupport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTax")
    def include_tax(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeTax"))

    @include_tax.setter
    def include_tax(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e756cd03fae89dc030537b2343776f59bea38a33fba52a5284cbe774d0fbfcba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeUpfront")
    def include_upfront(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeUpfront"))

    @include_upfront.setter
    def include_upfront(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d7a3d65b5a0fda41f5019716f2ed0deabef74bce94a7d9e434c6f742489314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeUpfront", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAmortized")
    def use_amortized(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useAmortized"))

    @use_amortized.setter
    def use_amortized(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3a1621f5e518095697c7f3d19a39dc379f819b26fdb216c94da90833bc092f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAmortized", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useBlended")
    def use_blended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useBlended"))

    @use_blended.setter
    def use_blended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16d3bba714eaec1c0fb040643b6e122cb309940f2bfd5179d960679f1c9404b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useBlended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BudgetsBudgetCostTypes]:
        return typing.cast(typing.Optional[BudgetsBudgetCostTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BudgetsBudgetCostTypes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317b78cafd9e7dbd8d4a8f6a56e4a31ac9826f9df54c71cbbe888ffc16f49fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetNotification",
    jsii_struct_bases=[],
    name_mapping={
        "comparison_operator": "comparisonOperator",
        "notification_type": "notificationType",
        "threshold": "threshold",
        "threshold_type": "thresholdType",
        "subscriber_email_addresses": "subscriberEmailAddresses",
        "subscriber_sns_topic_arns": "subscriberSnsTopicArns",
    },
)
class BudgetsBudgetNotification:
    def __init__(
        self,
        *,
        comparison_operator: builtins.str,
        notification_type: builtins.str,
        threshold: jsii.Number,
        threshold_type: builtins.str,
        subscriber_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        subscriber_sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparison_operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#comparison_operator BudgetsBudget#comparison_operator}.
        :param notification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#notification_type BudgetsBudget#notification_type}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#threshold BudgetsBudget#threshold}.
        :param threshold_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#threshold_type BudgetsBudget#threshold_type}.
        :param subscriber_email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#subscriber_email_addresses BudgetsBudget#subscriber_email_addresses}.
        :param subscriber_sns_topic_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#subscriber_sns_topic_arns BudgetsBudget#subscriber_sns_topic_arns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a896f53aa2959d65053a477c6347303c4837b94f733fbdcb5ec87497dfeef0)
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument threshold_type", value=threshold_type, expected_type=type_hints["threshold_type"])
            check_type(argname="argument subscriber_email_addresses", value=subscriber_email_addresses, expected_type=type_hints["subscriber_email_addresses"])
            check_type(argname="argument subscriber_sns_topic_arns", value=subscriber_sns_topic_arns, expected_type=type_hints["subscriber_sns_topic_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison_operator": comparison_operator,
            "notification_type": notification_type,
            "threshold": threshold,
            "threshold_type": threshold_type,
        }
        if subscriber_email_addresses is not None:
            self._values["subscriber_email_addresses"] = subscriber_email_addresses
        if subscriber_sns_topic_arns is not None:
            self._values["subscriber_sns_topic_arns"] = subscriber_sns_topic_arns

    @builtins.property
    def comparison_operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#comparison_operator BudgetsBudget#comparison_operator}.'''
        result = self._values.get("comparison_operator")
        assert result is not None, "Required property 'comparison_operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#notification_type BudgetsBudget#notification_type}.'''
        result = self._values.get("notification_type")
        assert result is not None, "Required property 'notification_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#threshold BudgetsBudget#threshold}.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def threshold_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#threshold_type BudgetsBudget#threshold_type}.'''
        result = self._values.get("threshold_type")
        assert result is not None, "Required property 'threshold_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscriber_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#subscriber_email_addresses BudgetsBudget#subscriber_email_addresses}.'''
        result = self._values.get("subscriber_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subscriber_sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#subscriber_sns_topic_arns BudgetsBudget#subscriber_sns_topic_arns}.'''
        result = self._values.get("subscriber_sns_topic_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetNotification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetNotificationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetNotificationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a39f32c7c76e5ef11bb721698bda43c66811a391aa2d22316281a9cd1d00fab4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BudgetsBudgetNotificationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b33fb6bbcac9980400f78dbe9676429186af169061710bb1782f858a6ce5f7f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BudgetsBudgetNotificationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59ce56a9ebbf573832fcbadcf26239cf1b9e76f4d5f82f7b25cb2b4f5cd1535)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1175d294e8bc0f3a190ab714eb2843122afe5ce5384973271f811fbf82dc034e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b931b7fd4ffdde20da74c479733485bd5eb4cbfbfe663939551dca4be61182b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetNotification]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetNotification]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetNotification]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ba54001cd96a0b0f8c83de05930ebf49b0df5a45e46edc57d234b043c988f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BudgetsBudgetNotificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetNotificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f33274e92e1f52c1edfb6bd6670fcaf12a3c0a0a5aa5314073e4402f8ee80c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubscriberEmailAddresses")
    def reset_subscriber_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriberEmailAddresses", []))

    @jsii.member(jsii_name="resetSubscriberSnsTopicArns")
    def reset_subscriber_sns_topic_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriberSnsTopicArns", []))

    @builtins.property
    @jsii.member(jsii_name="comparisonOperatorInput")
    def comparison_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationTypeInput")
    def notification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriberEmailAddressesInput")
    def subscriber_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subscriberEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriberSnsTopicArnsInput")
    def subscriber_sns_topic_arns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subscriberSnsTopicArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdTypeInput")
    def threshold_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparisonOperator"))

    @comparison_operator.setter
    def comparison_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fe4e3d1b546f474ac8c6927ddc5ba50c09b9b33448ab01dfc724314a49b5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparisonOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationType"))

    @notification_type.setter
    def notification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fc847d1a12bb006f6301478df389bf802e77fb460dd0b425c9bdf219541b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriberEmailAddresses")
    def subscriber_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subscriberEmailAddresses"))

    @subscriber_email_addresses.setter
    def subscriber_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4919f961e415ee1624211a31be0163ee63f4710ac6e97f7e1f4aa3583e9d9693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriberEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriberSnsTopicArns")
    def subscriber_sns_topic_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subscriberSnsTopicArns"))

    @subscriber_sns_topic_arns.setter
    def subscriber_sns_topic_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81c7d961121aa7ee23d5d40ca1ce702433a91a80301fe98ec9d6b2e8d1f2559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriberSnsTopicArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665618f39b7fdf3d800653a800fd41858114288a49eff25649fee588714b2d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdType"))

    @threshold_type.setter
    def threshold_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb27bf78d0109f0bd5061756ae289c4d43c9f7e8b78f0e1e9bdb01ffeb50b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetNotification]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetNotification]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetNotification]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb402d3f66b9a02b189a4056c5c66236c6bc91034537fd9ad04ad1bee403521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetPlannedLimit",
    jsii_struct_bases=[],
    name_mapping={"amount": "amount", "start_time": "startTime", "unit": "unit"},
)
class BudgetsBudgetPlannedLimit:
    def __init__(
        self,
        *,
        amount: builtins.str,
        start_time: builtins.str,
        unit: builtins.str,
    ) -> None:
        '''
        :param amount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#amount BudgetsBudget#amount}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#start_time BudgetsBudget#start_time}.
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#unit BudgetsBudget#unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f69d121370c60c7265649f8fb5b3d27a268c6f3c17d37cfb9854e53c9281496)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amount": amount,
            "start_time": start_time,
            "unit": unit,
        }

    @builtins.property
    def amount(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#amount BudgetsBudget#amount}.'''
        result = self._values.get("amount")
        assert result is not None, "Required property 'amount' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#start_time BudgetsBudget#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/budgets_budget#unit BudgetsBudget#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsBudgetPlannedLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BudgetsBudgetPlannedLimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetPlannedLimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e19883714c819ce7d2e0ee71e1b344e32243632d0b705c68b582cf4c35aae7e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BudgetsBudgetPlannedLimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd61fab11c5882ce8ed1c65037c4b6a2570c8bc0b14bf60d30f49766ce427b90)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BudgetsBudgetPlannedLimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106f72d4385321266f945739c28fd072e9f580783a8f0b43eab434b24109a0ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7ebe2b197a17175c960b83629a9f5592a7b57e1739302ec8e954d18997f1625)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77cc9094879caab033a6a9766f9239db0a7faddac5722c86fa866689a8b79fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetPlannedLimit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetPlannedLimit]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetPlannedLimit]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ffbca3b52d84bc867f2f0c8b191bddf4a219342f1e3395f29cd48242a85506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BudgetsBudgetPlannedLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.budgetsBudget.BudgetsBudgetPlannedLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f40bd2be5ece762a33db2de9294a60802bbf83a912f7d76863425195e6c7ac6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="amountInput")
    def amount_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amountInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="amount")
    def amount(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amount"))

    @amount.setter
    def amount(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1a964e79a05eeb8f4a31c70f85a3a2dfe51789cea6f19e49b731dc2db38f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe38b5a019057555f07a9b10cb4fb48e6789227c2ea2612e88ae3ad1fea4c0d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a37996bf45dc300f35c0d41c7fe01831a5387e45a5fa4c46ddc4ab12e5cb4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetPlannedLimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetPlannedLimit]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetPlannedLimit]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75345f6a9e63566d39f21aa65e99c7e8319d7bf8411ee706289c820506250d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BudgetsBudget",
    "BudgetsBudgetAutoAdjustData",
    "BudgetsBudgetAutoAdjustDataHistoricalOptions",
    "BudgetsBudgetAutoAdjustDataHistoricalOptionsOutputReference",
    "BudgetsBudgetAutoAdjustDataOutputReference",
    "BudgetsBudgetConfig",
    "BudgetsBudgetCostFilter",
    "BudgetsBudgetCostFilterList",
    "BudgetsBudgetCostFilterOutputReference",
    "BudgetsBudgetCostTypes",
    "BudgetsBudgetCostTypesOutputReference",
    "BudgetsBudgetNotification",
    "BudgetsBudgetNotificationList",
    "BudgetsBudgetNotificationOutputReference",
    "BudgetsBudgetPlannedLimit",
    "BudgetsBudgetPlannedLimitList",
    "BudgetsBudgetPlannedLimitOutputReference",
]

publication.publish()

def _typecheckingstub__76737ca33fc598975c9af917298840a9a3dae7ae89c8e21c49d6df52621ee629(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    budget_type: builtins.str,
    time_unit: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    auto_adjust_data: typing.Optional[typing.Union[BudgetsBudgetAutoAdjustData, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
    cost_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetCostFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cost_types: typing.Optional[typing.Union[BudgetsBudgetCostTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    limit_amount: typing.Optional[builtins.str] = None,
    limit_unit: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    notification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetNotification, typing.Dict[builtins.str, typing.Any]]]]] = None,
    planned_limit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetPlannedLimit, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    time_period_end: typing.Optional[builtins.str] = None,
    time_period_start: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__53a6c480fd0be4b86e8ca514da985515e5532fb88c8fca8eed6278de2aed6429(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f06341089f78ff988a122044eeeb601250760fb4824a80066c4a6d5664092f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetCostFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaa8adeb5bbefa30aaabfa06ce5161ad331d218407dca82a39edb36dfb9b3d1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetNotification, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a84a1be9bf0d1d2fd703292a428d3a5b855f00efd09eeafea74af295aa152d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetPlannedLimit, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15ef7362a1b4ee88090b0ce5b34f9c80b21b459d8d350f676f281ccf03fb0a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6543176334b8509d714f690eb78ed806c5bb8eb59675ab2e9a4cddc877ca61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459833eb52ac22cbf5c49e72ab3e64a813d7013855e20ec96f2291d538229590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f956ff886821d71349fcb826645aed0b2a1d1943d05938340217caa95d4ca0d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feca239b57be2b84ca570bdf77d06b697cdaac99bc549b9a63108964b20c24fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520ca7be74e31347b70efc6c827b7fe8b2b1a4dada5d758698ce0fa8c531862d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b8d5cfa6cc5239bacb9252f8ac63f336cb4bd278216348d5f5a1b90dde138b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af50a3ab536ca79153bf01e2c8d20de347355e60f272935458f37d189f94e2ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16711ce551710d1209d1175e4282ef7d60c2f836002ae0c5a80f3b3cc3e8cb56(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e219b2c0bfdefe532c5c6bfdefbeef6fec428314f75686ad6d704eab60e195(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d69601081ba3ec7ea08d28c68fb13af9c4e6b4dff11bee4dec3929c52f73a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f611651ed4ca9d92147fce08c1f857961f2bd2e161d2766a682f8208abcad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfd96ab9cb4301eb5223a2635bf114f81c64a69ab72a4c20785281a22ecf67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b9aa0f916ddcca9e02671f6e003215d9445086e4c84660cac834a7381c0b61(
    *,
    auto_adjust_type: builtins.str,
    historical_options: typing.Optional[typing.Union[BudgetsBudgetAutoAdjustDataHistoricalOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5883c1eef5d51bc7120c4feb15744d8a108c87a5e71c188d698b5ca56d86375(
    *,
    budget_adjustment_period: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8829e7499be69874f2fb4264e0a23face7422d3a6cf5485f1bf4096c8afba78c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6534b0008fa708f5d6a31b6fc27e00d1a9cfab57238e71b8bf1bc99aafc3d26c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdb4cdc67fc001521a94e071e16df87740f01b0aa52b6f5a3355506473cbc51(
    value: typing.Optional[BudgetsBudgetAutoAdjustDataHistoricalOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f8c22e4d71da92dd4c10b71877ae5857ca32533326ee591dd4c88fbba6a7ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61834abc21fb1e048efdf7bd8ab6e980e91ce048696c1d42a517cacbb3ee6a1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efeca2508bf95a07f0cb3e30430f788a72ccf4e533f7a976ec461bed27e48ba(
    value: typing.Optional[BudgetsBudgetAutoAdjustData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9512b42f8024519b0596878e835b27f72449e6e26ab7ba149836dbf8f9a72d19(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    budget_type: builtins.str,
    time_unit: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    auto_adjust_data: typing.Optional[typing.Union[BudgetsBudgetAutoAdjustData, typing.Dict[builtins.str, typing.Any]]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
    cost_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetCostFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cost_types: typing.Optional[typing.Union[BudgetsBudgetCostTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    limit_amount: typing.Optional[builtins.str] = None,
    limit_unit: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    notification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetNotification, typing.Dict[builtins.str, typing.Any]]]]] = None,
    planned_limit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BudgetsBudgetPlannedLimit, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    time_period_end: typing.Optional[builtins.str] = None,
    time_period_start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067902cb2904b6eb28907a79e613d62ea6a16ce8acbb99e3466465f10a05ffad(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11af638c8a4804752a1e727b07b7a6e026f89d68312529533f7abec115bd2152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871e3854dff2865fa9e232587c81475c3e26576b9b97abf8e907276cb5d7e33f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72606cb8f79f61338faa42a6592da9637f6b094414b9a4a340f6ca6ec3b14d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8e2106003248e09ecd0299f3c5aecae33101c5477f1dcc5c5f8bb2e877292f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760f5aa6d17ff1c08dac082656a18e164f0485ed885874cefdfe541df9c51129(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef61ea6a95384b1f2d7757b5e965bbe0a872b20358968dfbe2f3f23932aa1b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetCostFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e486230479ba731ee132d5b1e3387ee1c7725738397c2f2638762132eb44f528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6d3d0574fddb63dfad5b08b15a609208977868fcd100e6156dedaedaa3a7d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66af87f59d88f533144d6ea4b37e7a3dc9b54108744479024a4be96ce962040c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012bc92432a6ef4cc7773ee510974814f74f3de1c6b321c397f95f58ea6975c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetCostFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa5652375455474eb0aafd0ed3ccef32d8e747204b6b25d45efc5ca2f04f0ad(
    *,
    include_credit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_discount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_other_subscription: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_recurring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_refund: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_subscription: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_tax: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_upfront: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_amortized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_blended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95bffd853788a04e7d9dfa9e7905542c0a09a4bb060b81e6f6f4e0859d30b7f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e790f40c3035e449d7fd8ecdb2b64d021c19182eedc767d7197ab182a40f6a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674a7a31b056977555eb41101a3f73eb7f1f6bd024554134473ec8bd24f02dc7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f840e228ca0d0ddc2df7bdf1d9745740c5802094c96b9b3aab4642f6f2f7dfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56977e67851475e36e6c50735d2459d5fc34a8a852bce55395d97dbe4f95b20a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84803440b0f6cf8061bab0b328515d3b56e1fce5e6363a80e1a7771a239f5d4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e9093b71a1c72ce222b0523ebb80ced7166b8e2ea29d8b496d356e8fec8ee9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4628e29ee81e459ea1a7aca78ccf628b59b331695832f9671d4ce964083908f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e756cd03fae89dc030537b2343776f59bea38a33fba52a5284cbe774d0fbfcba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d7a3d65b5a0fda41f5019716f2ed0deabef74bce94a7d9e434c6f742489314(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3a1621f5e518095697c7f3d19a39dc379f819b26fdb216c94da90833bc092f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16d3bba714eaec1c0fb040643b6e122cb309940f2bfd5179d960679f1c9404b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317b78cafd9e7dbd8d4a8f6a56e4a31ac9826f9df54c71cbbe888ffc16f49fc2(
    value: typing.Optional[BudgetsBudgetCostTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a896f53aa2959d65053a477c6347303c4837b94f733fbdcb5ec87497dfeef0(
    *,
    comparison_operator: builtins.str,
    notification_type: builtins.str,
    threshold: jsii.Number,
    threshold_type: builtins.str,
    subscriber_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    subscriber_sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39f32c7c76e5ef11bb721698bda43c66811a391aa2d22316281a9cd1d00fab4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b33fb6bbcac9980400f78dbe9676429186af169061710bb1782f858a6ce5f7f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59ce56a9ebbf573832fcbadcf26239cf1b9e76f4d5f82f7b25cb2b4f5cd1535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1175d294e8bc0f3a190ab714eb2843122afe5ce5384973271f811fbf82dc034e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b931b7fd4ffdde20da74c479733485bd5eb4cbfbfe663939551dca4be61182b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ba54001cd96a0b0f8c83de05930ebf49b0df5a45e46edc57d234b043c988f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetNotification]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f33274e92e1f52c1edfb6bd6670fcaf12a3c0a0a5aa5314073e4402f8ee80c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fe4e3d1b546f474ac8c6927ddc5ba50c09b9b33448ab01dfc724314a49b5f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fc847d1a12bb006f6301478df389bf802e77fb460dd0b425c9bdf219541b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4919f961e415ee1624211a31be0163ee63f4710ac6e97f7e1f4aa3583e9d9693(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81c7d961121aa7ee23d5d40ca1ce702433a91a80301fe98ec9d6b2e8d1f2559(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665618f39b7fdf3d800653a800fd41858114288a49eff25649fee588714b2d17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb27bf78d0109f0bd5061756ae289c4d43c9f7e8b78f0e1e9bdb01ffeb50b32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb402d3f66b9a02b189a4056c5c66236c6bc91034537fd9ad04ad1bee403521(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetNotification]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f69d121370c60c7265649f8fb5b3d27a268c6f3c17d37cfb9854e53c9281496(
    *,
    amount: builtins.str,
    start_time: builtins.str,
    unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19883714c819ce7d2e0ee71e1b344e32243632d0b705c68b582cf4c35aae7e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd61fab11c5882ce8ed1c65037c4b6a2570c8bc0b14bf60d30f49766ce427b90(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106f72d4385321266f945739c28fd072e9f580783a8f0b43eab434b24109a0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ebe2b197a17175c960b83629a9f5592a7b57e1739302ec8e954d18997f1625(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cc9094879caab033a6a9766f9239db0a7faddac5722c86fa866689a8b79fc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ffbca3b52d84bc867f2f0c8b191bddf4a219342f1e3395f29cd48242a85506(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BudgetsBudgetPlannedLimit]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f40bd2be5ece762a33db2de9294a60802bbf83a912f7d76863425195e6c7ac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1a964e79a05eeb8f4a31c70f85a3a2dfe51789cea6f19e49b731dc2db38f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe38b5a019057555f07a9b10cb4fb48e6789227c2ea2612e88ae3ad1fea4c0d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a37996bf45dc300f35c0d41c7fe01831a5387e45a5fa4c46ddc4ab12e5cb4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75345f6a9e63566d39f21aa65e99c7e8319d7bf8411ee706289c820506250d27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BudgetsBudgetPlannedLimit]],
) -> None:
    """Type checking stubs"""
    pass
