r'''
# `aws_cognito_risk_configuration`

Refer to the Terraform Registry for docs: [`aws_cognito_risk_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration).
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


class CognitoRiskConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration aws_cognito_risk_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        user_pool_id: builtins.str,
        account_takeover_risk_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        risk_exception_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationRiskExceptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration aws_cognito_risk_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#user_pool_id CognitoRiskConfiguration#user_pool_id}.
        :param account_takeover_risk_configuration: account_takeover_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#account_takeover_risk_configuration CognitoRiskConfiguration#account_takeover_risk_configuration}
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#client_id CognitoRiskConfiguration#client_id}.
        :param compromised_credentials_risk_configuration: compromised_credentials_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#compromised_credentials_risk_configuration CognitoRiskConfiguration#compromised_credentials_risk_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#id CognitoRiskConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#region CognitoRiskConfiguration#region}
        :param risk_exception_configuration: risk_exception_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#risk_exception_configuration CognitoRiskConfiguration#risk_exception_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32aeb79b4c0182f82de7e0b9408250a384aebac1a9a1890d3648eb468a9f2306)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CognitoRiskConfigurationConfig(
            user_pool_id=user_pool_id,
            account_takeover_risk_configuration=account_takeover_risk_configuration,
            client_id=client_id,
            compromised_credentials_risk_configuration=compromised_credentials_risk_configuration,
            id=id,
            region=region,
            risk_exception_configuration=risk_exception_configuration,
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
        '''Generates CDKTF code for importing a CognitoRiskConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CognitoRiskConfiguration to import.
        :param import_from_id: The id of the existing CognitoRiskConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CognitoRiskConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33db9c84aa70fe32991602860a6f43ad1b7fce149c15876c8e20646cebcccb1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountTakeoverRiskConfiguration")
    def put_account_takeover_risk_configuration(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        notify_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param notify_configuration: notify_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify_configuration CognitoRiskConfiguration#notify_configuration}
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfiguration(
            actions=actions, notify_configuration=notify_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putAccountTakeoverRiskConfiguration", [value]))

    @jsii.member(jsii_name="putCompromisedCredentialsRiskConfiguration")
    def put_compromised_credentials_risk_configuration(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param event_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_filter CognitoRiskConfiguration#event_filter}.
        '''
        value = CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration(
            actions=actions, event_filter=event_filter
        )

        return typing.cast(None, jsii.invoke(self, "putCompromisedCredentialsRiskConfiguration", [value]))

    @jsii.member(jsii_name="putRiskExceptionConfiguration")
    def put_risk_exception_configuration(
        self,
        *,
        blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blocked_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#blocked_ip_range_list CognitoRiskConfiguration#blocked_ip_range_list}.
        :param skipped_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#skipped_ip_range_list CognitoRiskConfiguration#skipped_ip_range_list}.
        '''
        value = CognitoRiskConfigurationRiskExceptionConfiguration(
            blocked_ip_range_list=blocked_ip_range_list,
            skipped_ip_range_list=skipped_ip_range_list,
        )

        return typing.cast(None, jsii.invoke(self, "putRiskExceptionConfiguration", [value]))

    @jsii.member(jsii_name="resetAccountTakeoverRiskConfiguration")
    def reset_account_takeover_risk_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountTakeoverRiskConfiguration", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetCompromisedCredentialsRiskConfiguration")
    def reset_compromised_credentials_risk_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompromisedCredentialsRiskConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRiskExceptionConfiguration")
    def reset_risk_exception_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRiskExceptionConfiguration", []))

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
    @jsii.member(jsii_name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(
        self,
    ) -> "CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference":
        return typing.cast("CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference", jsii.get(self, "accountTakeoverRiskConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(
        self,
    ) -> "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference":
        return typing.cast("CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference", jsii.get(self, "compromisedCredentialsRiskConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="riskExceptionConfiguration")
    def risk_exception_configuration(
        self,
    ) -> "CognitoRiskConfigurationRiskExceptionConfigurationOutputReference":
        return typing.cast("CognitoRiskConfigurationRiskExceptionConfigurationOutputReference", jsii.get(self, "riskExceptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accountTakeoverRiskConfigurationInput")
    def account_takeover_risk_configuration_input(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfiguration"]:
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfiguration"], jsii.get(self, "accountTakeoverRiskConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="compromisedCredentialsRiskConfigurationInput")
    def compromised_credentials_risk_configuration_input(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration"]:
        return typing.cast(typing.Optional["CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration"], jsii.get(self, "compromisedCredentialsRiskConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="riskExceptionConfigurationInput")
    def risk_exception_configuration_input(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"]:
        return typing.cast(typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"], jsii.get(self, "riskExceptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolIdInput")
    def user_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833400308e4726e619a8ab4b47810125884bd176f592423dbb988fbaadf38fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688622402d0b420bf0019a0143fee423cbd957707d703435df63d04d04b7716c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5427afd1bc90f91abd6908b47106e31280509ae5b066fd877e52647b0633d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolId"))

    @user_pool_id.setter
    def user_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8438c87e5c1ddb8ea8ea351f4f69e55e81b7271d3b17201f59f54d8da51a460b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfiguration",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "notify_configuration": "notifyConfiguration"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfiguration:
    def __init__(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        notify_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param notify_configuration: notify_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify_configuration CognitoRiskConfiguration#notify_configuration}
        '''
        if isinstance(actions, dict):
            actions = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions(**actions)
        if isinstance(notify_configuration, dict):
            notify_configuration = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration(**notify_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c949ea89a8515611b2cf722d46957dbd23e2776734e785cf3232284c0efaa6)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument notify_configuration", value=notify_configuration, expected_type=type_hints["notify_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }
        if notify_configuration is not None:
            self._values["notify_configuration"] = notify_configuration

    @builtins.property
    def actions(
        self,
    ) -> "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions", result)

    @builtins.property
    def notify_configuration(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration"]:
        '''notify_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify_configuration CognitoRiskConfiguration#notify_configuration}
        '''
        result = self._values.get("notify_configuration")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions",
    jsii_struct_bases=[],
    name_mapping={
        "high_action": "highAction",
        "low_action": "lowAction",
        "medium_action": "mediumAction",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions:
    def __init__(
        self,
        *,
        high_action: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction", typing.Dict[builtins.str, typing.Any]]] = None,
        low_action: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction", typing.Dict[builtins.str, typing.Any]]] = None,
        medium_action: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param high_action: high_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#high_action CognitoRiskConfiguration#high_action}
        :param low_action: low_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#low_action CognitoRiskConfiguration#low_action}
        :param medium_action: medium_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#medium_action CognitoRiskConfiguration#medium_action}
        '''
        if isinstance(high_action, dict):
            high_action = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction(**high_action)
        if isinstance(low_action, dict):
            low_action = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction(**low_action)
        if isinstance(medium_action, dict):
            medium_action = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction(**medium_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e78c5eaa3912318c797d73c08cc9fce92045ea13a6f287643e1ed65a8add488)
            check_type(argname="argument high_action", value=high_action, expected_type=type_hints["high_action"])
            check_type(argname="argument low_action", value=low_action, expected_type=type_hints["low_action"])
            check_type(argname="argument medium_action", value=medium_action, expected_type=type_hints["medium_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if high_action is not None:
            self._values["high_action"] = high_action
        if low_action is not None:
            self._values["low_action"] = low_action
        if medium_action is not None:
            self._values["medium_action"] = medium_action

    @builtins.property
    def high_action(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction"]:
        '''high_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#high_action CognitoRiskConfiguration#high_action}
        '''
        result = self._values.get("high_action")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction"], result)

    @builtins.property
    def low_action(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction"]:
        '''low_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#low_action CognitoRiskConfiguration#low_action}
        '''
        result = self._values.get("low_action")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction"], result)

    @builtins.property
    def medium_action(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction"]:
        '''medium_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#medium_action CognitoRiskConfiguration#medium_action}
        '''
        result = self._values.get("medium_action")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction", "notify": "notify"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction:
    def __init__(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d108a1d78579ffc499a204421e4997dcce064a9be1212dd2c6cf948dfb458049)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
            "notify": notify,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.'''
        result = self._values.get("notify")
        assert result is not None, "Required property 'notify' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d09a7822f5e73b83629cb8e76c5d39458dac20d7afc22efd7662b5ed8058990e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyInput")
    def notify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac06f05e39ddccff2b2315af7fb8fcda5b5bddccdf9e63893e0fbfe2fde666dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notify")
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notify"))

    @notify.setter
    def notify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739009ddea305bbea5c4d419f29c4a477ca066bfad1920c8cc1ff513af3efb7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc8ea8a47adeda67e757776c4bc56309336b78894cb959c4acdd56be4f8ad0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction", "notify": "notify"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction:
    def __init__(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8fe1f0602be4ceef06a79a5cca8cf543f4c975331df9106cda78c0c9b48ad7)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
            "notify": notify,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.'''
        result = self._values.get("notify")
        assert result is not None, "Required property 'notify' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb81c71761766077aab008a881a29ab999f3783fe56bfa2ba677e56f3db8e7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyInput")
    def notify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bc05f7e4d9f6079a217f95b6b31cc38c6e9f01173559c61101486c6f4152d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notify")
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notify"))

    @notify.setter
    def notify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a63e16dab3823ad77dfc9effe0e3df8223912697922459e831753880321cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a602ededb6337b948f7d4a52c09a2b47e8aa74d0b7077568d63855471cf7b7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction", "notify": "notify"},
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction:
    def __init__(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c04db688d47d24e17f85a07c3b5a89715a4208f70df28cfb28657ee2b28e82)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
            "notify": notify,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.'''
        result = self._values.get("notify")
        assert result is not None, "Required property 'notify' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a9b667486a89225b5217b90dc28e4f005cdd6af4ef7144aa96da96817426493)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyInput")
    def notify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65661be92a48fd870cee1c4de13d81b1910f67fa7e9c607e3d8445382dcd138d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notify")
    def notify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notify"))

    @notify.setter
    def notify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38004666bd64fd0ef04820bb97e21fc4190d7469816f2807bf112502c2af86a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28917b8978b2c8273d74611908cfdb3aad9b426e3d65432073e6a8b502088dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55cbfc21fe07b8e6510c3c569fd47ef3c0d67c814ace4a0b9894c9f648b6a1b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHighAction")
    def put_high_action(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction(
            event_action=event_action, notify=notify
        )

        return typing.cast(None, jsii.invoke(self, "putHighAction", [value]))

    @jsii.member(jsii_name="putLowAction")
    def put_low_action(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction(
            event_action=event_action, notify=notify
        )

        return typing.cast(None, jsii.invoke(self, "putLowAction", [value]))

    @jsii.member(jsii_name="putMediumAction")
    def put_medium_action(
        self,
        *,
        event_action: builtins.str,
        notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        :param notify: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#notify CognitoRiskConfiguration#notify}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction(
            event_action=event_action, notify=notify
        )

        return typing.cast(None, jsii.invoke(self, "putMediumAction", [value]))

    @jsii.member(jsii_name="resetHighAction")
    def reset_high_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighAction", []))

    @jsii.member(jsii_name="resetLowAction")
    def reset_low_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLowAction", []))

    @jsii.member(jsii_name="resetMediumAction")
    def reset_medium_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMediumAction", []))

    @builtins.property
    @jsii.member(jsii_name="highAction")
    def high_action(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference, jsii.get(self, "highAction"))

    @builtins.property
    @jsii.member(jsii_name="lowAction")
    def low_action(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference, jsii.get(self, "lowAction"))

    @builtins.property
    @jsii.member(jsii_name="mediumAction")
    def medium_action(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference, jsii.get(self, "mediumAction"))

    @builtins.property
    @jsii.member(jsii_name="highActionInput")
    def high_action_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction], jsii.get(self, "highActionInput"))

    @builtins.property
    @jsii.member(jsii_name="lowActionInput")
    def low_action_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction], jsii.get(self, "lowActionInput"))

    @builtins.property
    @jsii.member(jsii_name="mediumActionInput")
    def medium_action_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction], jsii.get(self, "mediumActionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cb773067dda8d81165886bf23ddf584029b62a59607da96a5fca95f1fe9766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "source_arn": "sourceArn",
        "block_email": "blockEmail",
        "from_": "from",
        "mfa_email": "mfaEmail",
        "no_action_email": "noActionEmail",
        "reply_to": "replyTo",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration:
    def __init__(
        self,
        *,
        source_arn: builtins.str,
        block_email: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        from_: typing.Optional[builtins.str] = None,
        mfa_email: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        no_action_email: typing.Optional[typing.Union["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        reply_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#source_arn CognitoRiskConfiguration#source_arn}.
        :param block_email: block_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#block_email CognitoRiskConfiguration#block_email}
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#from CognitoRiskConfiguration#from}.
        :param mfa_email: mfa_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#mfa_email CognitoRiskConfiguration#mfa_email}
        :param no_action_email: no_action_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#no_action_email CognitoRiskConfiguration#no_action_email}
        :param reply_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#reply_to CognitoRiskConfiguration#reply_to}.
        '''
        if isinstance(block_email, dict):
            block_email = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail(**block_email)
        if isinstance(mfa_email, dict):
            mfa_email = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail(**mfa_email)
        if isinstance(no_action_email, dict):
            no_action_email = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail(**no_action_email)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77f0554507a4691bdf46529722bc17fab012dc548fcec2970cf2b2821972b47)
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument block_email", value=block_email, expected_type=type_hints["block_email"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument mfa_email", value=mfa_email, expected_type=type_hints["mfa_email"])
            check_type(argname="argument no_action_email", value=no_action_email, expected_type=type_hints["no_action_email"])
            check_type(argname="argument reply_to", value=reply_to, expected_type=type_hints["reply_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_arn": source_arn,
        }
        if block_email is not None:
            self._values["block_email"] = block_email
        if from_ is not None:
            self._values["from_"] = from_
        if mfa_email is not None:
            self._values["mfa_email"] = mfa_email
        if no_action_email is not None:
            self._values["no_action_email"] = no_action_email
        if reply_to is not None:
            self._values["reply_to"] = reply_to

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#source_arn CognitoRiskConfiguration#source_arn}.'''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_email(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail"]:
        '''block_email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#block_email CognitoRiskConfiguration#block_email}
        '''
        result = self._values.get("block_email")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail"], result)

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#from CognitoRiskConfiguration#from}.'''
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mfa_email(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail"]:
        '''mfa_email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#mfa_email CognitoRiskConfiguration#mfa_email}
        '''
        result = self._values.get("mfa_email")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail"], result)

    @builtins.property
    def no_action_email(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail"]:
        '''no_action_email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#no_action_email CognitoRiskConfiguration#no_action_email}
        '''
        result = self._values.get("no_action_email")
        return typing.cast(typing.Optional["CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail"], result)

    @builtins.property
    def reply_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#reply_to CognitoRiskConfiguration#reply_to}.'''
        result = self._values.get("reply_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail",
    jsii_struct_bases=[],
    name_mapping={
        "html_body": "htmlBody",
        "subject": "subject",
        "text_body": "textBody",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail:
    def __init__(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a37894bfbe9b95980d29706b8da034f5b518579531fea4097a8f9d630ed6baf)
            check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_body": html_body,
            "subject": subject,
            "text_body": text_body,
        }

    @builtins.property
    def html_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.'''
        result = self._values.get("html_body")
        assert result is not None, "Required property 'html_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.'''
        result = self._values.get("text_body")
        assert result is not None, "Required property 'text_body' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f96b8fcd62749e5687659dd38252e206c1fedfd7ff9c0b02005dcabb667efc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="htmlBodyInput")
    def html_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="textBodyInput")
    def text_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlBody")
    def html_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlBody"))

    @html_body.setter
    def html_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddee3583ef41d53f64b755176ef1833b5d773c728d89166668aeb21658a07c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71a6f9a1b7d9e45829711e6afcbe687e9fa041f40bcbf34e3b111fd11b9424f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textBody")
    def text_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textBody"))

    @text_body.setter
    def text_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813779e557548512a9fb635976e996808922487eb1afe7aa19f4c104839175e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dda5782065ae784588cf4d926e34b4b0c72c02bc97c26005d9d3dda012b1f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail",
    jsii_struct_bases=[],
    name_mapping={
        "html_body": "htmlBody",
        "subject": "subject",
        "text_body": "textBody",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail:
    def __init__(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3470e9e66d0b8100ce0177d4d7f8e373b5fe81ef184b072510754f74b7cb5cbd)
            check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_body": html_body,
            "subject": subject,
            "text_body": text_body,
        }

    @builtins.property
    def html_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.'''
        result = self._values.get("html_body")
        assert result is not None, "Required property 'html_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.'''
        result = self._values.get("text_body")
        assert result is not None, "Required property 'text_body' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b668e99c3af393f214745e07aa3baab4ea2b9e5a208df3c00ba9d4956f18abf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="htmlBodyInput")
    def html_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="textBodyInput")
    def text_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlBody")
    def html_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlBody"))

    @html_body.setter
    def html_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277f022e3cce17e17a4c407c5fd7a6fd3a01c4384ad9cdf294214c9b80833434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159742fade0ff8702fe0a715bad30d7a72209d1e5122776d56c4ccae669932b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textBody")
    def text_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textBody"))

    @text_body.setter
    def text_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e09e0f5f5116716f3ff89d6633f59a3301c0a463fd1750465292f3975f2d61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21afc8d3dc4d6f654a8f3c55e1f981811a1f0d2ad4df68c1397e700d8e9445b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail",
    jsii_struct_bases=[],
    name_mapping={
        "html_body": "htmlBody",
        "subject": "subject",
        "text_body": "textBody",
    },
)
class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail:
    def __init__(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bdfda7f1eb88529707a619ae9ee2068979fd3f6e4c4fe2cd0ef99ec22222c50)
            check_type(argname="argument html_body", value=html_body, expected_type=type_hints["html_body"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument text_body", value=text_body, expected_type=type_hints["text_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_body": html_body,
            "subject": subject,
            "text_body": text_body,
        }

    @builtins.property
    def html_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.'''
        result = self._values.get("html_body")
        assert result is not None, "Required property 'html_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_body(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.'''
        result = self._values.get("text_body")
        assert result is not None, "Required property 'text_body' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dff052bf7c2e0a0d64fcaa6cc2bb40a04454af324d56c121df8d311c74c3022)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="htmlBodyInput")
    def html_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="textBodyInput")
    def text_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlBody")
    def html_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlBody"))

    @html_body.setter
    def html_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df475b8731407284bc5792e6d468f367fcaa5e16cfe58a6e332b841f8f161166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30e963730935b1e1b474fc77505880132f7b88ebe87fdcd0c65866243299e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textBody")
    def text_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textBody"))

    @text_body.setter
    def text_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007bcd92958632358514723457c3cc58c87568cb2128abe49c89f24e6bc244b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39911bc0e61ca23f377c258e25c32e72dde7ee4740cfccf672949df0598c7302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78a8c6558ab4e9097eedd8dbcaf3117d0f17024f0fee0cb692916cbbe54d375c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBlockEmail")
    def put_block_email(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail(
            html_body=html_body, subject=subject, text_body=text_body
        )

        return typing.cast(None, jsii.invoke(self, "putBlockEmail", [value]))

    @jsii.member(jsii_name="putMfaEmail")
    def put_mfa_email(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail(
            html_body=html_body, subject=subject, text_body=text_body
        )

        return typing.cast(None, jsii.invoke(self, "putMfaEmail", [value]))

    @jsii.member(jsii_name="putNoActionEmail")
    def put_no_action_email(
        self,
        *,
        html_body: builtins.str,
        subject: builtins.str,
        text_body: builtins.str,
    ) -> None:
        '''
        :param html_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#html_body CognitoRiskConfiguration#html_body}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#subject CognitoRiskConfiguration#subject}.
        :param text_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#text_body CognitoRiskConfiguration#text_body}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail(
            html_body=html_body, subject=subject, text_body=text_body
        )

        return typing.cast(None, jsii.invoke(self, "putNoActionEmail", [value]))

    @jsii.member(jsii_name="resetBlockEmail")
    def reset_block_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockEmail", []))

    @jsii.member(jsii_name="resetFrom")
    def reset_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrom", []))

    @jsii.member(jsii_name="resetMfaEmail")
    def reset_mfa_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaEmail", []))

    @jsii.member(jsii_name="resetNoActionEmail")
    def reset_no_action_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoActionEmail", []))

    @jsii.member(jsii_name="resetReplyTo")
    def reset_reply_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplyTo", []))

    @builtins.property
    @jsii.member(jsii_name="blockEmail")
    def block_email(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference, jsii.get(self, "blockEmail"))

    @builtins.property
    @jsii.member(jsii_name="mfaEmail")
    def mfa_email(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference, jsii.get(self, "mfaEmail"))

    @builtins.property
    @jsii.member(jsii_name="noActionEmail")
    def no_action_email(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference, jsii.get(self, "noActionEmail"))

    @builtins.property
    @jsii.member(jsii_name="blockEmailInput")
    def block_email_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail], jsii.get(self, "blockEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaEmailInput")
    def mfa_email_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail], jsii.get(self, "mfaEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="noActionEmailInput")
    def no_action_email_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail], jsii.get(self, "noActionEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="replyToInput")
    def reply_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replyToInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceArnInput")
    def source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b8011188c52f10e25af4b981e3aa0459ae5ddc7a0f3577a9194efceeaadc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replyTo")
    def reply_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replyTo"))

    @reply_to.setter
    def reply_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33b2966a3f1f7bfc44f934654070e9451b294a4d954942e4644402fef278f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replyTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7992bb152a844db93e4275e7eef0b875be2abc18efd06b60b9acfd6d2cac1dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52539502ed0c474cfdceef771105964a6aea1518b75f43ba9bdc82195cf4bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3311123cfdd275e7f620bbb6134cb67255137716876caa813c106df72ddad5d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        high_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction, typing.Dict[builtins.str, typing.Any]]] = None,
        low_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction, typing.Dict[builtins.str, typing.Any]]] = None,
        medium_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param high_action: high_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#high_action CognitoRiskConfiguration#high_action}
        :param low_action: low_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#low_action CognitoRiskConfiguration#low_action}
        :param medium_action: medium_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#medium_action CognitoRiskConfiguration#medium_action}
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions(
            high_action=high_action, low_action=low_action, medium_action=medium_action
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putNotifyConfiguration")
    def put_notify_configuration(
        self,
        *,
        source_arn: builtins.str,
        block_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail, typing.Dict[builtins.str, typing.Any]]] = None,
        from_: typing.Optional[builtins.str] = None,
        mfa_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail, typing.Dict[builtins.str, typing.Any]]] = None,
        no_action_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail, typing.Dict[builtins.str, typing.Any]]] = None,
        reply_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#source_arn CognitoRiskConfiguration#source_arn}.
        :param block_email: block_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#block_email CognitoRiskConfiguration#block_email}
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#from CognitoRiskConfiguration#from}.
        :param mfa_email: mfa_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#mfa_email CognitoRiskConfiguration#mfa_email}
        :param no_action_email: no_action_email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#no_action_email CognitoRiskConfiguration#no_action_email}
        :param reply_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#reply_to CognitoRiskConfiguration#reply_to}.
        '''
        value = CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration(
            source_arn=source_arn,
            block_email=block_email,
            from_=from_,
            mfa_email=mfa_email,
            no_action_email=no_action_email,
            reply_to=reply_to,
        )

        return typing.cast(None, jsii.invoke(self, "putNotifyConfiguration", [value]))

    @jsii.member(jsii_name="resetNotifyConfiguration")
    def reset_notify_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="notifyConfiguration")
    def notify_configuration(
        self,
    ) -> CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference:
        return typing.cast(CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference, jsii.get(self, "notifyConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyConfigurationInput")
    def notify_configuration_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration], jsii.get(self, "notifyConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2bcc0a658be1e60cf09854814c7602fe83ccb71c55121ce654c5b59f10d616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "event_filter": "eventFilter"},
)
class CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration:
    def __init__(
        self,
        *,
        actions: typing.Union["CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions", typing.Dict[builtins.str, typing.Any]],
        event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        :param event_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_filter CognitoRiskConfiguration#event_filter}.
        '''
        if isinstance(actions, dict):
            actions = CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d7c7a9c2848d44f3d67c771950339ee4f64098489ef823b4b0a3713e75e652)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }
        if event_filter is not None:
            self._values["event_filter"] = event_filter

    @builtins.property
    def actions(
        self,
    ) -> "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#actions CognitoRiskConfiguration#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions", result)

    @builtins.property
    def event_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_filter CognitoRiskConfiguration#event_filter}.'''
        result = self._values.get("event_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions",
    jsii_struct_bases=[],
    name_mapping={"event_action": "eventAction"},
)
class CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions:
    def __init__(self, *, event_action: builtins.str) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556f14acd138f8b5b78940d0df3c8ef235cb9c2dcf0623a32db6e37928aa5e26)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_action": event_action,
        }

    @builtins.property
    def event_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.'''
        result = self._values.get("event_action")
        assert result is not None, "Required property 'event_action' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c455b85e6285ee990e23b6340a6637c51dc58076369d8517cf161fb365aa2a7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bb308eafeb49bb50405142cd9545aca6ed463d0828480f1014a7ee75188779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2315afd2a1acd172f46754633d2dd8a3117039502beed1b101f6a0ef7f01bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92167e11dce0a44d8a7fc6b24e4e7c59559c7282bb9c5942fffa31c79c52b72e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(self, *, event_action: builtins.str) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#event_action CognitoRiskConfiguration#event_action}.
        '''
        value = CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions(
            event_action=event_action
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="resetEventFilter")
    def reset_event_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventFilter", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference:
        return typing.cast(CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventFilterInput")
    def event_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="eventFilter")
    def event_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventFilter"))

    @event_filter.setter
    def event_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0dd9408809992b6fb492123ad5a8cbde7395b0a70099cdc32565fe265d9e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba8f18f6fadcfd172d3399cdf56c5f32acfe306530ba72b87082197176ad200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "user_pool_id": "userPoolId",
        "account_takeover_risk_configuration": "accountTakeoverRiskConfiguration",
        "client_id": "clientId",
        "compromised_credentials_risk_configuration": "compromisedCredentialsRiskConfiguration",
        "id": "id",
        "region": "region",
        "risk_exception_configuration": "riskExceptionConfiguration",
    },
)
class CognitoRiskConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        user_pool_id: builtins.str,
        account_takeover_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        client_id: typing.Optional[builtins.str] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        risk_exception_configuration: typing.Optional[typing.Union["CognitoRiskConfigurationRiskExceptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#user_pool_id CognitoRiskConfiguration#user_pool_id}.
        :param account_takeover_risk_configuration: account_takeover_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#account_takeover_risk_configuration CognitoRiskConfiguration#account_takeover_risk_configuration}
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#client_id CognitoRiskConfiguration#client_id}.
        :param compromised_credentials_risk_configuration: compromised_credentials_risk_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#compromised_credentials_risk_configuration CognitoRiskConfiguration#compromised_credentials_risk_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#id CognitoRiskConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#region CognitoRiskConfiguration#region}
        :param risk_exception_configuration: risk_exception_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#risk_exception_configuration CognitoRiskConfiguration#risk_exception_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(account_takeover_risk_configuration, dict):
            account_takeover_risk_configuration = CognitoRiskConfigurationAccountTakeoverRiskConfiguration(**account_takeover_risk_configuration)
        if isinstance(compromised_credentials_risk_configuration, dict):
            compromised_credentials_risk_configuration = CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration(**compromised_credentials_risk_configuration)
        if isinstance(risk_exception_configuration, dict):
            risk_exception_configuration = CognitoRiskConfigurationRiskExceptionConfiguration(**risk_exception_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92ef194413ea584e48272b65e794ee2861d0a6ad79b8f22939949f1840eaaad)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument account_takeover_risk_configuration", value=account_takeover_risk_configuration, expected_type=type_hints["account_takeover_risk_configuration"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument compromised_credentials_risk_configuration", value=compromised_credentials_risk_configuration, expected_type=type_hints["compromised_credentials_risk_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument risk_exception_configuration", value=risk_exception_configuration, expected_type=type_hints["risk_exception_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool_id": user_pool_id,
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
        if account_takeover_risk_configuration is not None:
            self._values["account_takeover_risk_configuration"] = account_takeover_risk_configuration
        if client_id is not None:
            self._values["client_id"] = client_id
        if compromised_credentials_risk_configuration is not None:
            self._values["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if risk_exception_configuration is not None:
            self._values["risk_exception_configuration"] = risk_exception_configuration

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
    def user_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#user_pool_id CognitoRiskConfiguration#user_pool_id}.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_takeover_risk_configuration(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration]:
        '''account_takeover_risk_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#account_takeover_risk_configuration CognitoRiskConfiguration#account_takeover_risk_configuration}
        '''
        result = self._values.get("account_takeover_risk_configuration")
        return typing.cast(typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#client_id CognitoRiskConfiguration#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compromised_credentials_risk_configuration(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration]:
        '''compromised_credentials_risk_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#compromised_credentials_risk_configuration CognitoRiskConfiguration#compromised_credentials_risk_configuration}
        '''
        result = self._values.get("compromised_credentials_risk_configuration")
        return typing.cast(typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#id CognitoRiskConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#region CognitoRiskConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def risk_exception_configuration(
        self,
    ) -> typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"]:
        '''risk_exception_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#risk_exception_configuration CognitoRiskConfiguration#risk_exception_configuration}
        '''
        result = self._values.get("risk_exception_configuration")
        return typing.cast(typing.Optional["CognitoRiskConfigurationRiskExceptionConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationRiskExceptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "blocked_ip_range_list": "blockedIpRangeList",
        "skipped_ip_range_list": "skippedIpRangeList",
    },
)
class CognitoRiskConfigurationRiskExceptionConfiguration:
    def __init__(
        self,
        *,
        blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blocked_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#blocked_ip_range_list CognitoRiskConfiguration#blocked_ip_range_list}.
        :param skipped_ip_range_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#skipped_ip_range_list CognitoRiskConfiguration#skipped_ip_range_list}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a42f6c25dcf97ab0b19aefe4dcf6dee9d9b24e29deab8fdfae1a84205c4257c)
            check_type(argname="argument blocked_ip_range_list", value=blocked_ip_range_list, expected_type=type_hints["blocked_ip_range_list"])
            check_type(argname="argument skipped_ip_range_list", value=skipped_ip_range_list, expected_type=type_hints["skipped_ip_range_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if blocked_ip_range_list is not None:
            self._values["blocked_ip_range_list"] = blocked_ip_range_list
        if skipped_ip_range_list is not None:
            self._values["skipped_ip_range_list"] = skipped_ip_range_list

    @builtins.property
    def blocked_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#blocked_ip_range_list CognitoRiskConfiguration#blocked_ip_range_list}.'''
        result = self._values.get("blocked_ip_range_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skipped_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_risk_configuration#skipped_ip_range_list CognitoRiskConfiguration#skipped_ip_range_list}.'''
        result = self._values.get("skipped_ip_range_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoRiskConfigurationRiskExceptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoRiskConfigurationRiskExceptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoRiskConfiguration.CognitoRiskConfigurationRiskExceptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ea0b6a56cda2420a733e035b91163f4a08c2b6f42c715782367eb9bf507b1ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBlockedIpRangeList")
    def reset_blocked_ip_range_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockedIpRangeList", []))

    @jsii.member(jsii_name="resetSkippedIpRangeList")
    def reset_skipped_ip_range_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkippedIpRangeList", []))

    @builtins.property
    @jsii.member(jsii_name="blockedIpRangeListInput")
    def blocked_ip_range_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blockedIpRangeListInput"))

    @builtins.property
    @jsii.member(jsii_name="skippedIpRangeListInput")
    def skipped_ip_range_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "skippedIpRangeListInput"))

    @builtins.property
    @jsii.member(jsii_name="blockedIpRangeList")
    def blocked_ip_range_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blockedIpRangeList"))

    @blocked_ip_range_list.setter
    def blocked_ip_range_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70de62f84b64939a7f95b58e5934277c2da68d50cef18330c20205c548cf832f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedIpRangeList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skippedIpRangeList")
    def skipped_ip_range_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "skippedIpRangeList"))

    @skipped_ip_range_list.setter
    def skipped_ip_range_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0b26628b6356953cdd278ed025a073919460ee84d55495f59155120a2e91c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skippedIpRangeList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration]:
        return typing.cast(typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb18166c57d88b13dcfb4c36e8a45022afdafcde274d8cdb5296ad9ad47f7948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CognitoRiskConfiguration",
    "CognitoRiskConfigurationAccountTakeoverRiskConfiguration",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighActionOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowActionOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumActionOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmailOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmailOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmailOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationOutputReference",
    "CognitoRiskConfigurationAccountTakeoverRiskConfigurationOutputReference",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActionsOutputReference",
    "CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationOutputReference",
    "CognitoRiskConfigurationConfig",
    "CognitoRiskConfigurationRiskExceptionConfiguration",
    "CognitoRiskConfigurationRiskExceptionConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__32aeb79b4c0182f82de7e0b9408250a384aebac1a9a1890d3648eb468a9f2306(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    user_pool_id: builtins.str,
    account_takeover_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    compromised_credentials_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    risk_exception_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationRiskExceptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__33db9c84aa70fe32991602860a6f43ad1b7fce149c15876c8e20646cebcccb1f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833400308e4726e619a8ab4b47810125884bd176f592423dbb988fbaadf38fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688622402d0b420bf0019a0143fee423cbd957707d703435df63d04d04b7716c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5427afd1bc90f91abd6908b47106e31280509ae5b066fd877e52647b0633d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8438c87e5c1ddb8ea8ea351f4f69e55e81b7271d3b17201f59f54d8da51a460b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c949ea89a8515611b2cf722d46957dbd23e2776734e785cf3232284c0efaa6(
    *,
    actions: typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions, typing.Dict[builtins.str, typing.Any]],
    notify_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e78c5eaa3912318c797d73c08cc9fce92045ea13a6f287643e1ed65a8add488(
    *,
    high_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction, typing.Dict[builtins.str, typing.Any]]] = None,
    low_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction, typing.Dict[builtins.str, typing.Any]]] = None,
    medium_action: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d108a1d78579ffc499a204421e4997dcce064a9be1212dd2c6cf948dfb458049(
    *,
    event_action: builtins.str,
    notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09a7822f5e73b83629cb8e76c5d39458dac20d7afc22efd7662b5ed8058990e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac06f05e39ddccff2b2315af7fb8fcda5b5bddccdf9e63893e0fbfe2fde666dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739009ddea305bbea5c4d419f29c4a477ca066bfad1920c8cc1ff513af3efb7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc8ea8a47adeda67e757776c4bc56309336b78894cb959c4acdd56be4f8ad0c(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsHighAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8fe1f0602be4ceef06a79a5cca8cf543f4c975331df9106cda78c0c9b48ad7(
    *,
    event_action: builtins.str,
    notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb81c71761766077aab008a881a29ab999f3783fe56bfa2ba677e56f3db8e7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bc05f7e4d9f6079a217f95b6b31cc38c6e9f01173559c61101486c6f4152d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a63e16dab3823ad77dfc9effe0e3df8223912697922459e831753880321cf1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a602ededb6337b948f7d4a52c09a2b47e8aa74d0b7077568d63855471cf7b7f5(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsLowAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c04db688d47d24e17f85a07c3b5a89715a4208f70df28cfb28657ee2b28e82(
    *,
    event_action: builtins.str,
    notify: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9b667486a89225b5217b90dc28e4f005cdd6af4ef7144aa96da96817426493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65661be92a48fd870cee1c4de13d81b1910f67fa7e9c607e3d8445382dcd138d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38004666bd64fd0ef04820bb97e21fc4190d7469816f2807bf112502c2af86a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28917b8978b2c8273d74611908cfdb3aad9b426e3d65432073e6a8b502088dfa(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActionsMediumAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cbfc21fe07b8e6510c3c569fd47ef3c0d67c814ace4a0b9894c9f648b6a1b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cb773067dda8d81165886bf23ddf584029b62a59607da96a5fca95f1fe9766(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77f0554507a4691bdf46529722bc17fab012dc548fcec2970cf2b2821972b47(
    *,
    source_arn: builtins.str,
    block_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    from_: typing.Optional[builtins.str] = None,
    mfa_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    no_action_email: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    reply_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a37894bfbe9b95980d29706b8da034f5b518579531fea4097a8f9d630ed6baf(
    *,
    html_body: builtins.str,
    subject: builtins.str,
    text_body: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f96b8fcd62749e5687659dd38252e206c1fedfd7ff9c0b02005dcabb667efc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddee3583ef41d53f64b755176ef1833b5d773c728d89166668aeb21658a07c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71a6f9a1b7d9e45829711e6afcbe687e9fa041f40bcbf34e3b111fd11b9424f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813779e557548512a9fb635976e996808922487eb1afe7aa19f4c104839175e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dda5782065ae784588cf4d926e34b4b0c72c02bc97c26005d9d3dda012b1f08(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationBlockEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3470e9e66d0b8100ce0177d4d7f8e373b5fe81ef184b072510754f74b7cb5cbd(
    *,
    html_body: builtins.str,
    subject: builtins.str,
    text_body: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b668e99c3af393f214745e07aa3baab4ea2b9e5a208df3c00ba9d4956f18abf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277f022e3cce17e17a4c407c5fd7a6fd3a01c4384ad9cdf294214c9b80833434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159742fade0ff8702fe0a715bad30d7a72209d1e5122776d56c4ccae669932b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e09e0f5f5116716f3ff89d6633f59a3301c0a463fd1750465292f3975f2d61d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21afc8d3dc4d6f654a8f3c55e1f981811a1f0d2ad4df68c1397e700d8e9445b5(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationMfaEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdfda7f1eb88529707a619ae9ee2068979fd3f6e4c4fe2cd0ef99ec22222c50(
    *,
    html_body: builtins.str,
    subject: builtins.str,
    text_body: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dff052bf7c2e0a0d64fcaa6cc2bb40a04454af324d56c121df8d311c74c3022(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df475b8731407284bc5792e6d468f367fcaa5e16cfe58a6e332b841f8f161166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30e963730935b1e1b474fc77505880132f7b88ebe87fdcd0c65866243299e59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007bcd92958632358514723457c3cc58c87568cb2128abe49c89f24e6bc244b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39911bc0e61ca23f377c258e25c32e72dde7ee4740cfccf672949df0598c7302(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfigurationNoActionEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a8c6558ab4e9097eedd8dbcaf3117d0f17024f0fee0cb692916cbbe54d375c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b8011188c52f10e25af4b981e3aa0459ae5ddc7a0f3577a9194efceeaadc56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33b2966a3f1f7bfc44f934654070e9451b294a4d954942e4644402fef278f48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7992bb152a844db93e4275e7eef0b875be2abc18efd06b60b9acfd6d2cac1dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52539502ed0c474cfdceef771105964a6aea1518b75f43ba9bdc82195cf4bd8(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfigurationNotifyConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3311123cfdd275e7f620bbb6134cb67255137716876caa813c106df72ddad5d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2bcc0a658be1e60cf09854814c7602fe83ccb71c55121ce654c5b59f10d616(
    value: typing.Optional[CognitoRiskConfigurationAccountTakeoverRiskConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d7c7a9c2848d44f3d67c771950339ee4f64098489ef823b4b0a3713e75e652(
    *,
    actions: typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions, typing.Dict[builtins.str, typing.Any]],
    event_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556f14acd138f8b5b78940d0df3c8ef235cb9c2dcf0623a32db6e37928aa5e26(
    *,
    event_action: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c455b85e6285ee990e23b6340a6637c51dc58076369d8517cf161fb365aa2a7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bb308eafeb49bb50405142cd9545aca6ed463d0828480f1014a7ee75188779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2315afd2a1acd172f46754633d2dd8a3117039502beed1b101f6a0ef7f01bc7(
    value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfigurationActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92167e11dce0a44d8a7fc6b24e4e7c59559c7282bb9c5942fffa31c79c52b72e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0dd9408809992b6fb492123ad5a8cbde7395b0a70099cdc32565fe265d9e55(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba8f18f6fadcfd172d3399cdf56c5f32acfe306530ba72b87082197176ad200(
    value: typing.Optional[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92ef194413ea584e48272b65e794ee2861d0a6ad79b8f22939949f1840eaaad(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_pool_id: builtins.str,
    account_takeover_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationAccountTakeoverRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    client_id: typing.Optional[builtins.str] = None,
    compromised_credentials_risk_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationCompromisedCredentialsRiskConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    risk_exception_configuration: typing.Optional[typing.Union[CognitoRiskConfigurationRiskExceptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a42f6c25dcf97ab0b19aefe4dcf6dee9d9b24e29deab8fdfae1a84205c4257c(
    *,
    blocked_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    skipped_ip_range_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea0b6a56cda2420a733e035b91163f4a08c2b6f42c715782367eb9bf507b1ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70de62f84b64939a7f95b58e5934277c2da68d50cef18330c20205c548cf832f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0b26628b6356953cdd278ed025a073919460ee84d55495f59155120a2e91c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb18166c57d88b13dcfb4c36e8a45022afdafcde274d8cdb5296ad9ad47f7948(
    value: typing.Optional[CognitoRiskConfigurationRiskExceptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass
