r'''
# `aws_cognito_user_pool`

Refer to the Terraform Registry for docs: [`aws_cognito_user_pool`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool).
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


class CognitoUserPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool aws_cognito_user_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        account_recovery_setting: typing.Optional[typing.Union["CognitoUserPoolAccountRecoverySetting", typing.Dict[builtins.str, typing.Any]]] = None,
        admin_create_user_config: typing.Optional[typing.Union["CognitoUserPoolAdminCreateUserConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        alias_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_verified_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[builtins.str] = None,
        device_configuration: typing.Optional[typing.Union["CognitoUserPoolDeviceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        email_configuration: typing.Optional[typing.Union["CognitoUserPoolEmailConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        email_mfa_configuration: typing.Optional[typing.Union["CognitoUserPoolEmailMfaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        email_verification_message: typing.Optional[builtins.str] = None,
        email_verification_subject: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lambda_config: typing.Optional[typing.Union["CognitoUserPoolLambdaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mfa_configuration: typing.Optional[builtins.str] = None,
        password_policy: typing.Optional[typing.Union["CognitoUserPoolPasswordPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CognitoUserPoolSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sign_in_policy: typing.Optional[typing.Union["CognitoUserPoolSignInPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sms_authentication_message: typing.Optional[builtins.str] = None,
        sms_configuration: typing.Optional[typing.Union["CognitoUserPoolSmsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sms_verification_message: typing.Optional[builtins.str] = None,
        software_token_mfa_configuration: typing.Optional[typing.Union["CognitoUserPoolSoftwareTokenMfaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_attribute_update_settings: typing.Optional[typing.Union["CognitoUserPoolUserAttributeUpdateSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        username_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        username_configuration: typing.Optional[typing.Union["CognitoUserPoolUsernameConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_add_ons: typing.Optional[typing.Union["CognitoUserPoolUserPoolAddOns", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_tier: typing.Optional[builtins.str] = None,
        verification_message_template: typing.Optional[typing.Union["CognitoUserPoolVerificationMessageTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        web_authn_configuration: typing.Optional[typing.Union["CognitoUserPoolWebAuthnConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool aws_cognito_user_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.
        :param account_recovery_setting: account_recovery_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#account_recovery_setting CognitoUserPool#account_recovery_setting}
        :param admin_create_user_config: admin_create_user_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#admin_create_user_config CognitoUserPool#admin_create_user_config}
        :param alias_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#alias_attributes CognitoUserPool#alias_attributes}.
        :param auto_verified_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#auto_verified_attributes CognitoUserPool#auto_verified_attributes}.
        :param deletion_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#deletion_protection CognitoUserPool#deletion_protection}.
        :param device_configuration: device_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#device_configuration CognitoUserPool#device_configuration}
        :param email_configuration: email_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_configuration CognitoUserPool#email_configuration}
        :param email_mfa_configuration: email_mfa_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_mfa_configuration CognitoUserPool#email_mfa_configuration}
        :param email_verification_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_verification_message CognitoUserPool#email_verification_message}.
        :param email_verification_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_verification_subject CognitoUserPool#email_verification_subject}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#id CognitoUserPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lambda_config: lambda_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_config CognitoUserPool#lambda_config}
        :param mfa_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#mfa_configuration CognitoUserPool#mfa_configuration}.
        :param password_policy: password_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#password_policy CognitoUserPool#password_policy}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#region CognitoUserPool#region}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#schema CognitoUserPool#schema}
        :param sign_in_policy: sign_in_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sign_in_policy CognitoUserPool#sign_in_policy}
        :param sms_authentication_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_authentication_message CognitoUserPool#sms_authentication_message}.
        :param sms_configuration: sms_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_configuration CognitoUserPool#sms_configuration}
        :param sms_verification_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_verification_message CognitoUserPool#sms_verification_message}.
        :param software_token_mfa_configuration: software_token_mfa_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#software_token_mfa_configuration CognitoUserPool#software_token_mfa_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#tags CognitoUserPool#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#tags_all CognitoUserPool#tags_all}.
        :param user_attribute_update_settings: user_attribute_update_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_attribute_update_settings CognitoUserPool#user_attribute_update_settings}
        :param username_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#username_attributes CognitoUserPool#username_attributes}.
        :param username_configuration: username_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#username_configuration CognitoUserPool#username_configuration}
        :param user_pool_add_ons: user_pool_add_ons block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_pool_add_ons CognitoUserPool#user_pool_add_ons}
        :param user_pool_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_pool_tier CognitoUserPool#user_pool_tier}.
        :param verification_message_template: verification_message_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#verification_message_template CognitoUserPool#verification_message_template}
        :param web_authn_configuration: web_authn_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#web_authn_configuration CognitoUserPool#web_authn_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8872d50f4ab62e16f985b6573881f5ac556a0b0e5ae00333187a9276ac1eb0d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CognitoUserPoolConfig(
            name=name,
            account_recovery_setting=account_recovery_setting,
            admin_create_user_config=admin_create_user_config,
            alias_attributes=alias_attributes,
            auto_verified_attributes=auto_verified_attributes,
            deletion_protection=deletion_protection,
            device_configuration=device_configuration,
            email_configuration=email_configuration,
            email_mfa_configuration=email_mfa_configuration,
            email_verification_message=email_verification_message,
            email_verification_subject=email_verification_subject,
            id=id,
            lambda_config=lambda_config,
            mfa_configuration=mfa_configuration,
            password_policy=password_policy,
            region=region,
            schema=schema,
            sign_in_policy=sign_in_policy,
            sms_authentication_message=sms_authentication_message,
            sms_configuration=sms_configuration,
            sms_verification_message=sms_verification_message,
            software_token_mfa_configuration=software_token_mfa_configuration,
            tags=tags,
            tags_all=tags_all,
            user_attribute_update_settings=user_attribute_update_settings,
            username_attributes=username_attributes,
            username_configuration=username_configuration,
            user_pool_add_ons=user_pool_add_ons,
            user_pool_tier=user_pool_tier,
            verification_message_template=verification_message_template,
            web_authn_configuration=web_authn_configuration,
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
        '''Generates CDKTF code for importing a CognitoUserPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CognitoUserPool to import.
        :param import_from_id: The id of the existing CognitoUserPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CognitoUserPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1401e9d804e77e6f117726fe6753f19e9e59c35fb80630d8ac4d054f0c20f485)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountRecoverySetting")
    def put_account_recovery_setting(
        self,
        *,
        recovery_mechanism: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CognitoUserPoolAccountRecoverySettingRecoveryMechanism", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param recovery_mechanism: recovery_mechanism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#recovery_mechanism CognitoUserPool#recovery_mechanism}
        '''
        value = CognitoUserPoolAccountRecoverySetting(
            recovery_mechanism=recovery_mechanism
        )

        return typing.cast(None, jsii.invoke(self, "putAccountRecoverySetting", [value]))

    @jsii.member(jsii_name="putAdminCreateUserConfig")
    def put_admin_create_user_config(
        self,
        *,
        allow_admin_create_user_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        invite_message_template: typing.Optional[typing.Union["CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_admin_create_user_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#allow_admin_create_user_only CognitoUserPool#allow_admin_create_user_only}.
        :param invite_message_template: invite_message_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#invite_message_template CognitoUserPool#invite_message_template}
        '''
        value = CognitoUserPoolAdminCreateUserConfig(
            allow_admin_create_user_only=allow_admin_create_user_only,
            invite_message_template=invite_message_template,
        )

        return typing.cast(None, jsii.invoke(self, "putAdminCreateUserConfig", [value]))

    @jsii.member(jsii_name="putDeviceConfiguration")
    def put_device_configuration(
        self,
        *,
        challenge_required_on_new_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_only_remembered_on_user_prompt: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param challenge_required_on_new_device: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#challenge_required_on_new_device CognitoUserPool#challenge_required_on_new_device}.
        :param device_only_remembered_on_user_prompt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#device_only_remembered_on_user_prompt CognitoUserPool#device_only_remembered_on_user_prompt}.
        '''
        value = CognitoUserPoolDeviceConfiguration(
            challenge_required_on_new_device=challenge_required_on_new_device,
            device_only_remembered_on_user_prompt=device_only_remembered_on_user_prompt,
        )

        return typing.cast(None, jsii.invoke(self, "putDeviceConfiguration", [value]))

    @jsii.member(jsii_name="putEmailConfiguration")
    def put_email_configuration(
        self,
        *,
        configuration_set: typing.Optional[builtins.str] = None,
        email_sending_account: typing.Optional[builtins.str] = None,
        from_email_address: typing.Optional[builtins.str] = None,
        reply_to_email_address: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param configuration_set: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#configuration_set CognitoUserPool#configuration_set}.
        :param email_sending_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_sending_account CognitoUserPool#email_sending_account}.
        :param from_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#from_email_address CognitoUserPool#from_email_address}.
        :param reply_to_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#reply_to_email_address CognitoUserPool#reply_to_email_address}.
        :param source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#source_arn CognitoUserPool#source_arn}.
        '''
        value = CognitoUserPoolEmailConfiguration(
            configuration_set=configuration_set,
            email_sending_account=email_sending_account,
            from_email_address=from_email_address,
            reply_to_email_address=reply_to_email_address,
            source_arn=source_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putEmailConfiguration", [value]))

    @jsii.member(jsii_name="putEmailMfaConfiguration")
    def put_email_mfa_configuration(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#message CognitoUserPool#message}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#subject CognitoUserPool#subject}.
        '''
        value = CognitoUserPoolEmailMfaConfiguration(message=message, subject=subject)

        return typing.cast(None, jsii.invoke(self, "putEmailMfaConfiguration", [value]))

    @jsii.member(jsii_name="putLambdaConfig")
    def put_lambda_config(
        self,
        *,
        create_auth_challenge: typing.Optional[builtins.str] = None,
        custom_email_sender: typing.Optional[typing.Union["CognitoUserPoolLambdaConfigCustomEmailSender", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_message: typing.Optional[builtins.str] = None,
        custom_sms_sender: typing.Optional[typing.Union["CognitoUserPoolLambdaConfigCustomSmsSender", typing.Dict[builtins.str, typing.Any]]] = None,
        define_auth_challenge: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        post_authentication: typing.Optional[builtins.str] = None,
        post_confirmation: typing.Optional[builtins.str] = None,
        pre_authentication: typing.Optional[builtins.str] = None,
        pre_sign_up: typing.Optional[builtins.str] = None,
        pre_token_generation: typing.Optional[builtins.str] = None,
        pre_token_generation_config: typing.Optional[typing.Union["CognitoUserPoolLambdaConfigPreTokenGenerationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_migration: typing.Optional[builtins.str] = None,
        verify_auth_challenge_response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_auth_challenge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#create_auth_challenge CognitoUserPool#create_auth_challenge}.
        :param custom_email_sender: custom_email_sender block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_email_sender CognitoUserPool#custom_email_sender}
        :param custom_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_message CognitoUserPool#custom_message}.
        :param custom_sms_sender: custom_sms_sender block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_sms_sender CognitoUserPool#custom_sms_sender}
        :param define_auth_challenge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#define_auth_challenge CognitoUserPool#define_auth_challenge}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#kms_key_id CognitoUserPool#kms_key_id}.
        :param post_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#post_authentication CognitoUserPool#post_authentication}.
        :param post_confirmation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#post_confirmation CognitoUserPool#post_confirmation}.
        :param pre_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_authentication CognitoUserPool#pre_authentication}.
        :param pre_sign_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_sign_up CognitoUserPool#pre_sign_up}.
        :param pre_token_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_token_generation CognitoUserPool#pre_token_generation}.
        :param pre_token_generation_config: pre_token_generation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_token_generation_config CognitoUserPool#pre_token_generation_config}
        :param user_migration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_migration CognitoUserPool#user_migration}.
        :param verify_auth_challenge_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#verify_auth_challenge_response CognitoUserPool#verify_auth_challenge_response}.
        '''
        value = CognitoUserPoolLambdaConfig(
            create_auth_challenge=create_auth_challenge,
            custom_email_sender=custom_email_sender,
            custom_message=custom_message,
            custom_sms_sender=custom_sms_sender,
            define_auth_challenge=define_auth_challenge,
            kms_key_id=kms_key_id,
            post_authentication=post_authentication,
            post_confirmation=post_confirmation,
            pre_authentication=pre_authentication,
            pre_sign_up=pre_sign_up,
            pre_token_generation=pre_token_generation,
            pre_token_generation_config=pre_token_generation_config,
            user_migration=user_migration,
            verify_auth_challenge_response=verify_auth_challenge_response,
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaConfig", [value]))

    @jsii.member(jsii_name="putPasswordPolicy")
    def put_password_policy(
        self,
        *,
        minimum_length: typing.Optional[jsii.Number] = None,
        password_history_size: typing.Optional[jsii.Number] = None,
        require_lowercase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_numbers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_symbols: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_uppercase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        temporary_password_validity_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param minimum_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#minimum_length CognitoUserPool#minimum_length}.
        :param password_history_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#password_history_size CognitoUserPool#password_history_size}.
        :param require_lowercase: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_lowercase CognitoUserPool#require_lowercase}.
        :param require_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_numbers CognitoUserPool#require_numbers}.
        :param require_symbols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_symbols CognitoUserPool#require_symbols}.
        :param require_uppercase: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_uppercase CognitoUserPool#require_uppercase}.
        :param temporary_password_validity_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#temporary_password_validity_days CognitoUserPool#temporary_password_validity_days}.
        '''
        value = CognitoUserPoolPasswordPolicy(
            minimum_length=minimum_length,
            password_history_size=password_history_size,
            require_lowercase=require_lowercase,
            require_numbers=require_numbers,
            require_symbols=require_symbols,
            require_uppercase=require_uppercase,
            temporary_password_validity_days=temporary_password_validity_days,
        )

        return typing.cast(None, jsii.invoke(self, "putPasswordPolicy", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CognitoUserPoolSchema", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05766da8b9a1b2faefe9f4a6078fde5bf415303580305edb32539b965be61460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="putSignInPolicy")
    def put_sign_in_policy(
        self,
        *,
        allowed_first_auth_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_first_auth_factors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#allowed_first_auth_factors CognitoUserPool#allowed_first_auth_factors}.
        '''
        value = CognitoUserPoolSignInPolicy(
            allowed_first_auth_factors=allowed_first_auth_factors
        )

        return typing.cast(None, jsii.invoke(self, "putSignInPolicy", [value]))

    @jsii.member(jsii_name="putSmsConfiguration")
    def put_sms_configuration(
        self,
        *,
        external_id: builtins.str,
        sns_caller_arn: builtins.str,
        sns_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#external_id CognitoUserPool#external_id}.
        :param sns_caller_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sns_caller_arn CognitoUserPool#sns_caller_arn}.
        :param sns_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sns_region CognitoUserPool#sns_region}.
        '''
        value = CognitoUserPoolSmsConfiguration(
            external_id=external_id,
            sns_caller_arn=sns_caller_arn,
            sns_region=sns_region,
        )

        return typing.cast(None, jsii.invoke(self, "putSmsConfiguration", [value]))

    @jsii.member(jsii_name="putSoftwareTokenMfaConfiguration")
    def put_software_token_mfa_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#enabled CognitoUserPool#enabled}.
        '''
        value = CognitoUserPoolSoftwareTokenMfaConfiguration(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putSoftwareTokenMfaConfiguration", [value]))

    @jsii.member(jsii_name="putUserAttributeUpdateSettings")
    def put_user_attribute_update_settings(
        self,
        *,
        attributes_require_verification_before_update: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attributes_require_verification_before_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#attributes_require_verification_before_update CognitoUserPool#attributes_require_verification_before_update}.
        '''
        value = CognitoUserPoolUserAttributeUpdateSettings(
            attributes_require_verification_before_update=attributes_require_verification_before_update,
        )

        return typing.cast(None, jsii.invoke(self, "putUserAttributeUpdateSettings", [value]))

    @jsii.member(jsii_name="putUsernameConfiguration")
    def put_username_configuration(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param case_sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#case_sensitive CognitoUserPool#case_sensitive}.
        '''
        value = CognitoUserPoolUsernameConfiguration(case_sensitive=case_sensitive)

        return typing.cast(None, jsii.invoke(self, "putUsernameConfiguration", [value]))

    @jsii.member(jsii_name="putUserPoolAddOns")
    def put_user_pool_add_ons(
        self,
        *,
        advanced_security_mode: builtins.str,
        advanced_security_additional_flows: typing.Optional[typing.Union["CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_security_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#advanced_security_mode CognitoUserPool#advanced_security_mode}.
        :param advanced_security_additional_flows: advanced_security_additional_flows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#advanced_security_additional_flows CognitoUserPool#advanced_security_additional_flows}
        '''
        value = CognitoUserPoolUserPoolAddOns(
            advanced_security_mode=advanced_security_mode,
            advanced_security_additional_flows=advanced_security_additional_flows,
        )

        return typing.cast(None, jsii.invoke(self, "putUserPoolAddOns", [value]))

    @jsii.member(jsii_name="putVerificationMessageTemplate")
    def put_verification_message_template(
        self,
        *,
        default_email_option: typing.Optional[builtins.str] = None,
        email_message: typing.Optional[builtins.str] = None,
        email_message_by_link: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
        email_subject_by_link: typing.Optional[builtins.str] = None,
        sms_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_email_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#default_email_option CognitoUserPool#default_email_option}.
        :param email_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message CognitoUserPool#email_message}.
        :param email_message_by_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message_by_link CognitoUserPool#email_message_by_link}.
        :param email_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject CognitoUserPool#email_subject}.
        :param email_subject_by_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject_by_link CognitoUserPool#email_subject_by_link}.
        :param sms_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_message CognitoUserPool#sms_message}.
        '''
        value = CognitoUserPoolVerificationMessageTemplate(
            default_email_option=default_email_option,
            email_message=email_message,
            email_message_by_link=email_message_by_link,
            email_subject=email_subject,
            email_subject_by_link=email_subject_by_link,
            sms_message=sms_message,
        )

        return typing.cast(None, jsii.invoke(self, "putVerificationMessageTemplate", [value]))

    @jsii.member(jsii_name="putWebAuthnConfiguration")
    def put_web_authn_configuration(
        self,
        *,
        relying_party_id: typing.Optional[builtins.str] = None,
        user_verification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relying_party_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#relying_party_id CognitoUserPool#relying_party_id}.
        :param user_verification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_verification CognitoUserPool#user_verification}.
        '''
        value = CognitoUserPoolWebAuthnConfiguration(
            relying_party_id=relying_party_id, user_verification=user_verification
        )

        return typing.cast(None, jsii.invoke(self, "putWebAuthnConfiguration", [value]))

    @jsii.member(jsii_name="resetAccountRecoverySetting")
    def reset_account_recovery_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountRecoverySetting", []))

    @jsii.member(jsii_name="resetAdminCreateUserConfig")
    def reset_admin_create_user_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminCreateUserConfig", []))

    @jsii.member(jsii_name="resetAliasAttributes")
    def reset_alias_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliasAttributes", []))

    @jsii.member(jsii_name="resetAutoVerifiedAttributes")
    def reset_auto_verified_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoVerifiedAttributes", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDeviceConfiguration")
    def reset_device_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceConfiguration", []))

    @jsii.member(jsii_name="resetEmailConfiguration")
    def reset_email_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailConfiguration", []))

    @jsii.member(jsii_name="resetEmailMfaConfiguration")
    def reset_email_mfa_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailMfaConfiguration", []))

    @jsii.member(jsii_name="resetEmailVerificationMessage")
    def reset_email_verification_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailVerificationMessage", []))

    @jsii.member(jsii_name="resetEmailVerificationSubject")
    def reset_email_verification_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailVerificationSubject", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLambdaConfig")
    def reset_lambda_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaConfig", []))

    @jsii.member(jsii_name="resetMfaConfiguration")
    def reset_mfa_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaConfiguration", []))

    @jsii.member(jsii_name="resetPasswordPolicy")
    def reset_password_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordPolicy", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetSignInPolicy")
    def reset_sign_in_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInPolicy", []))

    @jsii.member(jsii_name="resetSmsAuthenticationMessage")
    def reset_sms_authentication_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsAuthenticationMessage", []))

    @jsii.member(jsii_name="resetSmsConfiguration")
    def reset_sms_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsConfiguration", []))

    @jsii.member(jsii_name="resetSmsVerificationMessage")
    def reset_sms_verification_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsVerificationMessage", []))

    @jsii.member(jsii_name="resetSoftwareTokenMfaConfiguration")
    def reset_software_token_mfa_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareTokenMfaConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetUserAttributeUpdateSettings")
    def reset_user_attribute_update_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAttributeUpdateSettings", []))

    @jsii.member(jsii_name="resetUsernameAttributes")
    def reset_username_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameAttributes", []))

    @jsii.member(jsii_name="resetUsernameConfiguration")
    def reset_username_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameConfiguration", []))

    @jsii.member(jsii_name="resetUserPoolAddOns")
    def reset_user_pool_add_ons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPoolAddOns", []))

    @jsii.member(jsii_name="resetUserPoolTier")
    def reset_user_pool_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPoolTier", []))

    @jsii.member(jsii_name="resetVerificationMessageTemplate")
    def reset_verification_message_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationMessageTemplate", []))

    @jsii.member(jsii_name="resetWebAuthnConfiguration")
    def reset_web_authn_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebAuthnConfiguration", []))

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
    @jsii.member(jsii_name="accountRecoverySetting")
    def account_recovery_setting(
        self,
    ) -> "CognitoUserPoolAccountRecoverySettingOutputReference":
        return typing.cast("CognitoUserPoolAccountRecoverySettingOutputReference", jsii.get(self, "accountRecoverySetting"))

    @builtins.property
    @jsii.member(jsii_name="adminCreateUserConfig")
    def admin_create_user_config(
        self,
    ) -> "CognitoUserPoolAdminCreateUserConfigOutputReference":
        return typing.cast("CognitoUserPoolAdminCreateUserConfigOutputReference", jsii.get(self, "adminCreateUserConfig"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomain"))

    @builtins.property
    @jsii.member(jsii_name="deviceConfiguration")
    def device_configuration(
        self,
    ) -> "CognitoUserPoolDeviceConfigurationOutputReference":
        return typing.cast("CognitoUserPoolDeviceConfigurationOutputReference", jsii.get(self, "deviceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="emailConfiguration")
    def email_configuration(self) -> "CognitoUserPoolEmailConfigurationOutputReference":
        return typing.cast("CognitoUserPoolEmailConfigurationOutputReference", jsii.get(self, "emailConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="emailMfaConfiguration")
    def email_mfa_configuration(
        self,
    ) -> "CognitoUserPoolEmailMfaConfigurationOutputReference":
        return typing.cast("CognitoUserPoolEmailMfaConfigurationOutputReference", jsii.get(self, "emailMfaConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="estimatedNumberOfUsers")
    def estimated_number_of_users(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "estimatedNumberOfUsers"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(self) -> "CognitoUserPoolLambdaConfigOutputReference":
        return typing.cast("CognitoUserPoolLambdaConfigOutputReference", jsii.get(self, "lambdaConfig"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedDate")
    def last_modified_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedDate"))

    @builtins.property
    @jsii.member(jsii_name="passwordPolicy")
    def password_policy(self) -> "CognitoUserPoolPasswordPolicyOutputReference":
        return typing.cast("CognitoUserPoolPasswordPolicyOutputReference", jsii.get(self, "passwordPolicy"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "CognitoUserPoolSchemaList":
        return typing.cast("CognitoUserPoolSchemaList", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="signInPolicy")
    def sign_in_policy(self) -> "CognitoUserPoolSignInPolicyOutputReference":
        return typing.cast("CognitoUserPoolSignInPolicyOutputReference", jsii.get(self, "signInPolicy"))

    @builtins.property
    @jsii.member(jsii_name="smsConfiguration")
    def sms_configuration(self) -> "CognitoUserPoolSmsConfigurationOutputReference":
        return typing.cast("CognitoUserPoolSmsConfigurationOutputReference", jsii.get(self, "smsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="softwareTokenMfaConfiguration")
    def software_token_mfa_configuration(
        self,
    ) -> "CognitoUserPoolSoftwareTokenMfaConfigurationOutputReference":
        return typing.cast("CognitoUserPoolSoftwareTokenMfaConfigurationOutputReference", jsii.get(self, "softwareTokenMfaConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="userAttributeUpdateSettings")
    def user_attribute_update_settings(
        self,
    ) -> "CognitoUserPoolUserAttributeUpdateSettingsOutputReference":
        return typing.cast("CognitoUserPoolUserAttributeUpdateSettingsOutputReference", jsii.get(self, "userAttributeUpdateSettings"))

    @builtins.property
    @jsii.member(jsii_name="usernameConfiguration")
    def username_configuration(
        self,
    ) -> "CognitoUserPoolUsernameConfigurationOutputReference":
        return typing.cast("CognitoUserPoolUsernameConfigurationOutputReference", jsii.get(self, "usernameConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="userPoolAddOns")
    def user_pool_add_ons(self) -> "CognitoUserPoolUserPoolAddOnsOutputReference":
        return typing.cast("CognitoUserPoolUserPoolAddOnsOutputReference", jsii.get(self, "userPoolAddOns"))

    @builtins.property
    @jsii.member(jsii_name="verificationMessageTemplate")
    def verification_message_template(
        self,
    ) -> "CognitoUserPoolVerificationMessageTemplateOutputReference":
        return typing.cast("CognitoUserPoolVerificationMessageTemplateOutputReference", jsii.get(self, "verificationMessageTemplate"))

    @builtins.property
    @jsii.member(jsii_name="webAuthnConfiguration")
    def web_authn_configuration(
        self,
    ) -> "CognitoUserPoolWebAuthnConfigurationOutputReference":
        return typing.cast("CognitoUserPoolWebAuthnConfigurationOutputReference", jsii.get(self, "webAuthnConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accountRecoverySettingInput")
    def account_recovery_setting_input(
        self,
    ) -> typing.Optional["CognitoUserPoolAccountRecoverySetting"]:
        return typing.cast(typing.Optional["CognitoUserPoolAccountRecoverySetting"], jsii.get(self, "accountRecoverySettingInput"))

    @builtins.property
    @jsii.member(jsii_name="adminCreateUserConfigInput")
    def admin_create_user_config_input(
        self,
    ) -> typing.Optional["CognitoUserPoolAdminCreateUserConfig"]:
        return typing.cast(typing.Optional["CognitoUserPoolAdminCreateUserConfig"], jsii.get(self, "adminCreateUserConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasAttributesInput")
    def alias_attributes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aliasAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoVerifiedAttributesInput")
    def auto_verified_attributes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoVerifiedAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceConfigurationInput")
    def device_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolDeviceConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolDeviceConfiguration"], jsii.get(self, "deviceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="emailConfigurationInput")
    def email_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolEmailConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolEmailConfiguration"], jsii.get(self, "emailConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="emailMfaConfigurationInput")
    def email_mfa_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolEmailMfaConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolEmailMfaConfiguration"], jsii.get(self, "emailMfaConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="emailVerificationMessageInput")
    def email_verification_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailVerificationMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="emailVerificationSubjectInput")
    def email_verification_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailVerificationSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfigInput")
    def lambda_config_input(self) -> typing.Optional["CognitoUserPoolLambdaConfig"]:
        return typing.cast(typing.Optional["CognitoUserPoolLambdaConfig"], jsii.get(self, "lambdaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaConfigurationInput")
    def mfa_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mfaConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordPolicyInput")
    def password_policy_input(self) -> typing.Optional["CognitoUserPoolPasswordPolicy"]:
        return typing.cast(typing.Optional["CognitoUserPoolPasswordPolicy"], jsii.get(self, "passwordPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolSchema"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolSchema"]]], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="signInPolicyInput")
    def sign_in_policy_input(self) -> typing.Optional["CognitoUserPoolSignInPolicy"]:
        return typing.cast(typing.Optional["CognitoUserPoolSignInPolicy"], jsii.get(self, "signInPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="smsAuthenticationMessageInput")
    def sms_authentication_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smsAuthenticationMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="smsConfigurationInput")
    def sms_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolSmsConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolSmsConfiguration"], jsii.get(self, "smsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="smsVerificationMessageInput")
    def sms_verification_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smsVerificationMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareTokenMfaConfigurationInput")
    def software_token_mfa_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolSoftwareTokenMfaConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolSoftwareTokenMfaConfiguration"], jsii.get(self, "softwareTokenMfaConfigurationInput"))

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
    @jsii.member(jsii_name="userAttributeUpdateSettingsInput")
    def user_attribute_update_settings_input(
        self,
    ) -> typing.Optional["CognitoUserPoolUserAttributeUpdateSettings"]:
        return typing.cast(typing.Optional["CognitoUserPoolUserAttributeUpdateSettings"], jsii.get(self, "userAttributeUpdateSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameAttributesInput")
    def username_attributes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usernameAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameConfigurationInput")
    def username_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolUsernameConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolUsernameConfiguration"], jsii.get(self, "usernameConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolAddOnsInput")
    def user_pool_add_ons_input(
        self,
    ) -> typing.Optional["CognitoUserPoolUserPoolAddOns"]:
        return typing.cast(typing.Optional["CognitoUserPoolUserPoolAddOns"], jsii.get(self, "userPoolAddOnsInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolTierInput")
    def user_pool_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolTierInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationMessageTemplateInput")
    def verification_message_template_input(
        self,
    ) -> typing.Optional["CognitoUserPoolVerificationMessageTemplate"]:
        return typing.cast(typing.Optional["CognitoUserPoolVerificationMessageTemplate"], jsii.get(self, "verificationMessageTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="webAuthnConfigurationInput")
    def web_authn_configuration_input(
        self,
    ) -> typing.Optional["CognitoUserPoolWebAuthnConfiguration"]:
        return typing.cast(typing.Optional["CognitoUserPoolWebAuthnConfiguration"], jsii.get(self, "webAuthnConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasAttributes")
    def alias_attributes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aliasAttributes"))

    @alias_attributes.setter
    def alias_attributes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35eda83e750e892aed12a4a60a8a6054443ff4c17dc4c7525be5473208eda4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aliasAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoVerifiedAttributes")
    def auto_verified_attributes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "autoVerifiedAttributes"))

    @auto_verified_attributes.setter
    def auto_verified_attributes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6e50f4430aa2db407907a8038d5099045323251eeb3daa905c0066e54bf4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoVerifiedAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db6753e5585a8149b0d00e3b4f78120a272159bb7aa4a741a24b97b445cce05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailVerificationMessage")
    def email_verification_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailVerificationMessage"))

    @email_verification_message.setter
    def email_verification_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c0fe43457a68e7d56aa0c87ba0cbb95f68f3a7cdb15222df1ef4c69cb28c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailVerificationMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailVerificationSubject")
    def email_verification_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailVerificationSubject"))

    @email_verification_subject.setter
    def email_verification_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2194bb2c68fa7fcc89d76d003fefe1889e78bedd41c3059f121d0428b218d11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailVerificationSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46963528b276aab05cd6c46191aa8868cddd2b86f4e565b1c6a6c7a5bdfb6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mfaConfiguration")
    def mfa_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mfaConfiguration"))

    @mfa_configuration.setter
    def mfa_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36d57b85a35c2470155897f4506c5721f7fa4f623ae86c82935d32b401bdfdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mfaConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1410a7051cbb3b4a3d62f5b82b76576d07f86eb296dbbc3e78db8b4318012e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3df8d82df8f6fc041af8976ac0de53ffe371383db79fe28315a49965e547f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smsAuthenticationMessage")
    def sms_authentication_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smsAuthenticationMessage"))

    @sms_authentication_message.setter
    def sms_authentication_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95889b943c68eb1da10ad13ee44acd16f0b333ed89306c45456b3f6f5bf19128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smsAuthenticationMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smsVerificationMessage")
    def sms_verification_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smsVerificationMessage"))

    @sms_verification_message.setter
    def sms_verification_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06927ad91bad9f4bce31833eb353c6064b0394c61ae01f691943b2aa67ec55c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smsVerificationMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88402dd2924097c4c41582f73b468d8a30a1b3da75142038c6e6144173cf4e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f3826b5b5e68e6487364afb1b7665bb76c23e97404e75a6433158f9d557163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usernameAttributes")
    def username_attributes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usernameAttributes"))

    @username_attributes.setter
    def username_attributes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9377aba987382ab50a6cb2e4443c307e3459bd81a14fcdc1d21cb12d8313ac17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolTier")
    def user_pool_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolTier"))

    @user_pool_tier.setter
    def user_pool_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511f73aae65892fc0bb42482da5028f2a7955d6ee61efdd04ab4ef6a42d67730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolTier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAccountRecoverySetting",
    jsii_struct_bases=[],
    name_mapping={"recovery_mechanism": "recoveryMechanism"},
)
class CognitoUserPoolAccountRecoverySetting:
    def __init__(
        self,
        *,
        recovery_mechanism: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CognitoUserPoolAccountRecoverySettingRecoveryMechanism", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param recovery_mechanism: recovery_mechanism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#recovery_mechanism CognitoUserPool#recovery_mechanism}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdce3ed1b0953e1f407f7b8c3bff7b911cf91156683b5edc1342b78a0c91e0ed)
            check_type(argname="argument recovery_mechanism", value=recovery_mechanism, expected_type=type_hints["recovery_mechanism"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recovery_mechanism is not None:
            self._values["recovery_mechanism"] = recovery_mechanism

    @builtins.property
    def recovery_mechanism(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolAccountRecoverySettingRecoveryMechanism"]]]:
        '''recovery_mechanism block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#recovery_mechanism CognitoUserPool#recovery_mechanism}
        '''
        result = self._values.get("recovery_mechanism")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolAccountRecoverySettingRecoveryMechanism"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolAccountRecoverySetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolAccountRecoverySettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAccountRecoverySettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b5008d0ce83af1839c1fcb983dabdd9ff5d14b62cba1b1d5a1ef30959d17b40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecoveryMechanism")
    def put_recovery_mechanism(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CognitoUserPoolAccountRecoverySettingRecoveryMechanism", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afea38f94d9021003e1ecb231e88d57d8c58829e2ecf2d1bab3bcd24696565c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecoveryMechanism", [value]))

    @jsii.member(jsii_name="resetRecoveryMechanism")
    def reset_recovery_mechanism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryMechanism", []))

    @builtins.property
    @jsii.member(jsii_name="recoveryMechanism")
    def recovery_mechanism(
        self,
    ) -> "CognitoUserPoolAccountRecoverySettingRecoveryMechanismList":
        return typing.cast("CognitoUserPoolAccountRecoverySettingRecoveryMechanismList", jsii.get(self, "recoveryMechanism"))

    @builtins.property
    @jsii.member(jsii_name="recoveryMechanismInput")
    def recovery_mechanism_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolAccountRecoverySettingRecoveryMechanism"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolAccountRecoverySettingRecoveryMechanism"]]], jsii.get(self, "recoveryMechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolAccountRecoverySetting]:
        return typing.cast(typing.Optional[CognitoUserPoolAccountRecoverySetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolAccountRecoverySetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63deb84336cd99c87e17a845255c8cea7d5b68bd4e8e646d51614d59a9c00fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAccountRecoverySettingRecoveryMechanism",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "priority": "priority"},
)
class CognitoUserPoolAccountRecoverySettingRecoveryMechanism:
    def __init__(self, *, name: builtins.str, priority: jsii.Number) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#priority CognitoUserPool#priority}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8928ec841be3ef008727f3ae2ce29aab59d57da11097a50ca58ad43f223d19ab)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "priority": priority,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#priority CognitoUserPool#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolAccountRecoverySettingRecoveryMechanism(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolAccountRecoverySettingRecoveryMechanismList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAccountRecoverySettingRecoveryMechanismList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d539329a1bd3fe7595b4c8b0931a34ebc5969387a889d3e22bee52e62ab37293)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CognitoUserPoolAccountRecoverySettingRecoveryMechanismOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050acd11e1e1b2b816647bbfaef0e816b3eda268ef6ae53dd7797e29db19478d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CognitoUserPoolAccountRecoverySettingRecoveryMechanismOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73fe69656931b54a74bc6cca047f9259b5ed20a93670aff806eb2ba03f79a9f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d11be7c57011b09627210f78688da5eb319a92b8db9ae74324ce7c0f2ae3bbd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81c6821a76cdeeecb0cf3a7ca68041f207ccaccd5a6134de858ad932412e11e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolAccountRecoverySettingRecoveryMechanism]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolAccountRecoverySettingRecoveryMechanism]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolAccountRecoverySettingRecoveryMechanism]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b4dcc37d49d0cb410e7047744ccb61aeae76db82386c44dbc65364c62b9301b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoUserPoolAccountRecoverySettingRecoveryMechanismOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAccountRecoverySettingRecoveryMechanismOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae5288c016cbdc22757ad8a87cf598c425ba41654d4ec31aa40b6ca66f067814)
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
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa506396680e39fae1a1d5db0e168ef4652084d02bb73ba69fa680b1bfc1e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3261d811c880effff9480cd53fd504b79ef41331d191793e941b6de9908d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolAccountRecoverySettingRecoveryMechanism]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolAccountRecoverySettingRecoveryMechanism]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolAccountRecoverySettingRecoveryMechanism]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c238679ed69ce3c4bdad99cb9e4f3f812e780186611fd0cef5ccad2e5c7e480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAdminCreateUserConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allow_admin_create_user_only": "allowAdminCreateUserOnly",
        "invite_message_template": "inviteMessageTemplate",
    },
)
class CognitoUserPoolAdminCreateUserConfig:
    def __init__(
        self,
        *,
        allow_admin_create_user_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        invite_message_template: typing.Optional[typing.Union["CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_admin_create_user_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#allow_admin_create_user_only CognitoUserPool#allow_admin_create_user_only}.
        :param invite_message_template: invite_message_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#invite_message_template CognitoUserPool#invite_message_template}
        '''
        if isinstance(invite_message_template, dict):
            invite_message_template = CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate(**invite_message_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea17fcaa62d2b73fe80a62a087697b614e3d8dc22a0823e9424f7222fe87541d)
            check_type(argname="argument allow_admin_create_user_only", value=allow_admin_create_user_only, expected_type=type_hints["allow_admin_create_user_only"])
            check_type(argname="argument invite_message_template", value=invite_message_template, expected_type=type_hints["invite_message_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_admin_create_user_only is not None:
            self._values["allow_admin_create_user_only"] = allow_admin_create_user_only
        if invite_message_template is not None:
            self._values["invite_message_template"] = invite_message_template

    @builtins.property
    def allow_admin_create_user_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#allow_admin_create_user_only CognitoUserPool#allow_admin_create_user_only}.'''
        result = self._values.get("allow_admin_create_user_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def invite_message_template(
        self,
    ) -> typing.Optional["CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate"]:
        '''invite_message_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#invite_message_template CognitoUserPool#invite_message_template}
        '''
        result = self._values.get("invite_message_template")
        return typing.cast(typing.Optional["CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolAdminCreateUserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "email_message": "emailMessage",
        "email_subject": "emailSubject",
        "sms_message": "smsMessage",
    },
)
class CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate:
    def __init__(
        self,
        *,
        email_message: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
        sms_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message CognitoUserPool#email_message}.
        :param email_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject CognitoUserPool#email_subject}.
        :param sms_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_message CognitoUserPool#sms_message}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1df1cc8c4d026285fe9b0dad3a281ac06e8d250dc2be8e1048a2da7ba16a03)
            check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
            check_type(argname="argument email_subject", value=email_subject, expected_type=type_hints["email_subject"])
            check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email_message is not None:
            self._values["email_message"] = email_message
        if email_subject is not None:
            self._values["email_subject"] = email_subject
        if sms_message is not None:
            self._values["sms_message"] = sms_message

    @builtins.property
    def email_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message CognitoUserPool#email_message}.'''
        result = self._values.get("email_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject CognitoUserPool#email_subject}.'''
        result = self._values.get("email_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sms_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_message CognitoUserPool#sms_message}.'''
        result = self._values.get("sms_message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolAdminCreateUserConfigInviteMessageTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAdminCreateUserConfigInviteMessageTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d3571efe6343d500b04f0c9630eea52ae24722cb7e05d6f0b088f32822ef240)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmailMessage")
    def reset_email_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailMessage", []))

    @jsii.member(jsii_name="resetEmailSubject")
    def reset_email_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailSubject", []))

    @jsii.member(jsii_name="resetSmsMessage")
    def reset_sms_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsMessage", []))

    @builtins.property
    @jsii.member(jsii_name="emailMessageInput")
    def email_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="emailSubjectInput")
    def email_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="smsMessageInput")
    def sms_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smsMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="emailMessage")
    def email_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailMessage"))

    @email_message.setter
    def email_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62ab26e3b76a0a2a7aa05a7e363216736fab1c7974456c0ffec8184433d982a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailSubject")
    def email_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailSubject"))

    @email_subject.setter
    def email_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e237bf52d8655b9ad88fce0ef8b8e6ddb6bddf2b78160cce2766cc29d428f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smsMessage")
    def sms_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smsMessage"))

    @sms_message.setter
    def sms_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711b9e8dbbb2b39713c79aedab488b81fd8988af979730a9d15fd07f93bf46a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smsMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate]:
        return typing.cast(typing.Optional[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e8b08dbe32597c57c67595e46287ed1db61cf05690dd9dfd69a3114baae217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoUserPoolAdminCreateUserConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolAdminCreateUserConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b2390d13f3edbd3452cc7fcb4461664c190a36833c2e887a1d20affe39f9200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInviteMessageTemplate")
    def put_invite_message_template(
        self,
        *,
        email_message: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
        sms_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message CognitoUserPool#email_message}.
        :param email_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject CognitoUserPool#email_subject}.
        :param sms_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_message CognitoUserPool#sms_message}.
        '''
        value = CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate(
            email_message=email_message,
            email_subject=email_subject,
            sms_message=sms_message,
        )

        return typing.cast(None, jsii.invoke(self, "putInviteMessageTemplate", [value]))

    @jsii.member(jsii_name="resetAllowAdminCreateUserOnly")
    def reset_allow_admin_create_user_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAdminCreateUserOnly", []))

    @jsii.member(jsii_name="resetInviteMessageTemplate")
    def reset_invite_message_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInviteMessageTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="inviteMessageTemplate")
    def invite_message_template(
        self,
    ) -> CognitoUserPoolAdminCreateUserConfigInviteMessageTemplateOutputReference:
        return typing.cast(CognitoUserPoolAdminCreateUserConfigInviteMessageTemplateOutputReference, jsii.get(self, "inviteMessageTemplate"))

    @builtins.property
    @jsii.member(jsii_name="allowAdminCreateUserOnlyInput")
    def allow_admin_create_user_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAdminCreateUserOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="inviteMessageTemplateInput")
    def invite_message_template_input(
        self,
    ) -> typing.Optional[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate]:
        return typing.cast(typing.Optional[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate], jsii.get(self, "inviteMessageTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAdminCreateUserOnly")
    def allow_admin_create_user_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAdminCreateUserOnly"))

    @allow_admin_create_user_only.setter
    def allow_admin_create_user_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa56595440716b9016521ed96f1e3283635303bd047d71cff93ebfa346dac06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAdminCreateUserOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolAdminCreateUserConfig]:
        return typing.cast(typing.Optional[CognitoUserPoolAdminCreateUserConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolAdminCreateUserConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be63cf7143187151c094fca4cefa042c466f8b0aa23311f32941ecac1cbd0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolConfig",
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
        "account_recovery_setting": "accountRecoverySetting",
        "admin_create_user_config": "adminCreateUserConfig",
        "alias_attributes": "aliasAttributes",
        "auto_verified_attributes": "autoVerifiedAttributes",
        "deletion_protection": "deletionProtection",
        "device_configuration": "deviceConfiguration",
        "email_configuration": "emailConfiguration",
        "email_mfa_configuration": "emailMfaConfiguration",
        "email_verification_message": "emailVerificationMessage",
        "email_verification_subject": "emailVerificationSubject",
        "id": "id",
        "lambda_config": "lambdaConfig",
        "mfa_configuration": "mfaConfiguration",
        "password_policy": "passwordPolicy",
        "region": "region",
        "schema": "schema",
        "sign_in_policy": "signInPolicy",
        "sms_authentication_message": "smsAuthenticationMessage",
        "sms_configuration": "smsConfiguration",
        "sms_verification_message": "smsVerificationMessage",
        "software_token_mfa_configuration": "softwareTokenMfaConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "user_attribute_update_settings": "userAttributeUpdateSettings",
        "username_attributes": "usernameAttributes",
        "username_configuration": "usernameConfiguration",
        "user_pool_add_ons": "userPoolAddOns",
        "user_pool_tier": "userPoolTier",
        "verification_message_template": "verificationMessageTemplate",
        "web_authn_configuration": "webAuthnConfiguration",
    },
)
class CognitoUserPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_recovery_setting: typing.Optional[typing.Union[CognitoUserPoolAccountRecoverySetting, typing.Dict[builtins.str, typing.Any]]] = None,
        admin_create_user_config: typing.Optional[typing.Union[CognitoUserPoolAdminCreateUserConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        alias_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_verified_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[builtins.str] = None,
        device_configuration: typing.Optional[typing.Union["CognitoUserPoolDeviceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        email_configuration: typing.Optional[typing.Union["CognitoUserPoolEmailConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        email_mfa_configuration: typing.Optional[typing.Union["CognitoUserPoolEmailMfaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        email_verification_message: typing.Optional[builtins.str] = None,
        email_verification_subject: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lambda_config: typing.Optional[typing.Union["CognitoUserPoolLambdaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mfa_configuration: typing.Optional[builtins.str] = None,
        password_policy: typing.Optional[typing.Union["CognitoUserPoolPasswordPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CognitoUserPoolSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sign_in_policy: typing.Optional[typing.Union["CognitoUserPoolSignInPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sms_authentication_message: typing.Optional[builtins.str] = None,
        sms_configuration: typing.Optional[typing.Union["CognitoUserPoolSmsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sms_verification_message: typing.Optional[builtins.str] = None,
        software_token_mfa_configuration: typing.Optional[typing.Union["CognitoUserPoolSoftwareTokenMfaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_attribute_update_settings: typing.Optional[typing.Union["CognitoUserPoolUserAttributeUpdateSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        username_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        username_configuration: typing.Optional[typing.Union["CognitoUserPoolUsernameConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_add_ons: typing.Optional[typing.Union["CognitoUserPoolUserPoolAddOns", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_tier: typing.Optional[builtins.str] = None,
        verification_message_template: typing.Optional[typing.Union["CognitoUserPoolVerificationMessageTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        web_authn_configuration: typing.Optional[typing.Union["CognitoUserPoolWebAuthnConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.
        :param account_recovery_setting: account_recovery_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#account_recovery_setting CognitoUserPool#account_recovery_setting}
        :param admin_create_user_config: admin_create_user_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#admin_create_user_config CognitoUserPool#admin_create_user_config}
        :param alias_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#alias_attributes CognitoUserPool#alias_attributes}.
        :param auto_verified_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#auto_verified_attributes CognitoUserPool#auto_verified_attributes}.
        :param deletion_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#deletion_protection CognitoUserPool#deletion_protection}.
        :param device_configuration: device_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#device_configuration CognitoUserPool#device_configuration}
        :param email_configuration: email_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_configuration CognitoUserPool#email_configuration}
        :param email_mfa_configuration: email_mfa_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_mfa_configuration CognitoUserPool#email_mfa_configuration}
        :param email_verification_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_verification_message CognitoUserPool#email_verification_message}.
        :param email_verification_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_verification_subject CognitoUserPool#email_verification_subject}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#id CognitoUserPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lambda_config: lambda_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_config CognitoUserPool#lambda_config}
        :param mfa_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#mfa_configuration CognitoUserPool#mfa_configuration}.
        :param password_policy: password_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#password_policy CognitoUserPool#password_policy}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#region CognitoUserPool#region}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#schema CognitoUserPool#schema}
        :param sign_in_policy: sign_in_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sign_in_policy CognitoUserPool#sign_in_policy}
        :param sms_authentication_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_authentication_message CognitoUserPool#sms_authentication_message}.
        :param sms_configuration: sms_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_configuration CognitoUserPool#sms_configuration}
        :param sms_verification_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_verification_message CognitoUserPool#sms_verification_message}.
        :param software_token_mfa_configuration: software_token_mfa_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#software_token_mfa_configuration CognitoUserPool#software_token_mfa_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#tags CognitoUserPool#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#tags_all CognitoUserPool#tags_all}.
        :param user_attribute_update_settings: user_attribute_update_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_attribute_update_settings CognitoUserPool#user_attribute_update_settings}
        :param username_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#username_attributes CognitoUserPool#username_attributes}.
        :param username_configuration: username_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#username_configuration CognitoUserPool#username_configuration}
        :param user_pool_add_ons: user_pool_add_ons block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_pool_add_ons CognitoUserPool#user_pool_add_ons}
        :param user_pool_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_pool_tier CognitoUserPool#user_pool_tier}.
        :param verification_message_template: verification_message_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#verification_message_template CognitoUserPool#verification_message_template}
        :param web_authn_configuration: web_authn_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#web_authn_configuration CognitoUserPool#web_authn_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(account_recovery_setting, dict):
            account_recovery_setting = CognitoUserPoolAccountRecoverySetting(**account_recovery_setting)
        if isinstance(admin_create_user_config, dict):
            admin_create_user_config = CognitoUserPoolAdminCreateUserConfig(**admin_create_user_config)
        if isinstance(device_configuration, dict):
            device_configuration = CognitoUserPoolDeviceConfiguration(**device_configuration)
        if isinstance(email_configuration, dict):
            email_configuration = CognitoUserPoolEmailConfiguration(**email_configuration)
        if isinstance(email_mfa_configuration, dict):
            email_mfa_configuration = CognitoUserPoolEmailMfaConfiguration(**email_mfa_configuration)
        if isinstance(lambda_config, dict):
            lambda_config = CognitoUserPoolLambdaConfig(**lambda_config)
        if isinstance(password_policy, dict):
            password_policy = CognitoUserPoolPasswordPolicy(**password_policy)
        if isinstance(sign_in_policy, dict):
            sign_in_policy = CognitoUserPoolSignInPolicy(**sign_in_policy)
        if isinstance(sms_configuration, dict):
            sms_configuration = CognitoUserPoolSmsConfiguration(**sms_configuration)
        if isinstance(software_token_mfa_configuration, dict):
            software_token_mfa_configuration = CognitoUserPoolSoftwareTokenMfaConfiguration(**software_token_mfa_configuration)
        if isinstance(user_attribute_update_settings, dict):
            user_attribute_update_settings = CognitoUserPoolUserAttributeUpdateSettings(**user_attribute_update_settings)
        if isinstance(username_configuration, dict):
            username_configuration = CognitoUserPoolUsernameConfiguration(**username_configuration)
        if isinstance(user_pool_add_ons, dict):
            user_pool_add_ons = CognitoUserPoolUserPoolAddOns(**user_pool_add_ons)
        if isinstance(verification_message_template, dict):
            verification_message_template = CognitoUserPoolVerificationMessageTemplate(**verification_message_template)
        if isinstance(web_authn_configuration, dict):
            web_authn_configuration = CognitoUserPoolWebAuthnConfiguration(**web_authn_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a868aa72412a31fbec88aa66ae13517046726a0401d5b2c61a9daa22c941797c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_recovery_setting", value=account_recovery_setting, expected_type=type_hints["account_recovery_setting"])
            check_type(argname="argument admin_create_user_config", value=admin_create_user_config, expected_type=type_hints["admin_create_user_config"])
            check_type(argname="argument alias_attributes", value=alias_attributes, expected_type=type_hints["alias_attributes"])
            check_type(argname="argument auto_verified_attributes", value=auto_verified_attributes, expected_type=type_hints["auto_verified_attributes"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument device_configuration", value=device_configuration, expected_type=type_hints["device_configuration"])
            check_type(argname="argument email_configuration", value=email_configuration, expected_type=type_hints["email_configuration"])
            check_type(argname="argument email_mfa_configuration", value=email_mfa_configuration, expected_type=type_hints["email_mfa_configuration"])
            check_type(argname="argument email_verification_message", value=email_verification_message, expected_type=type_hints["email_verification_message"])
            check_type(argname="argument email_verification_subject", value=email_verification_subject, expected_type=type_hints["email_verification_subject"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            check_type(argname="argument mfa_configuration", value=mfa_configuration, expected_type=type_hints["mfa_configuration"])
            check_type(argname="argument password_policy", value=password_policy, expected_type=type_hints["password_policy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument sign_in_policy", value=sign_in_policy, expected_type=type_hints["sign_in_policy"])
            check_type(argname="argument sms_authentication_message", value=sms_authentication_message, expected_type=type_hints["sms_authentication_message"])
            check_type(argname="argument sms_configuration", value=sms_configuration, expected_type=type_hints["sms_configuration"])
            check_type(argname="argument sms_verification_message", value=sms_verification_message, expected_type=type_hints["sms_verification_message"])
            check_type(argname="argument software_token_mfa_configuration", value=software_token_mfa_configuration, expected_type=type_hints["software_token_mfa_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument user_attribute_update_settings", value=user_attribute_update_settings, expected_type=type_hints["user_attribute_update_settings"])
            check_type(argname="argument username_attributes", value=username_attributes, expected_type=type_hints["username_attributes"])
            check_type(argname="argument username_configuration", value=username_configuration, expected_type=type_hints["username_configuration"])
            check_type(argname="argument user_pool_add_ons", value=user_pool_add_ons, expected_type=type_hints["user_pool_add_ons"])
            check_type(argname="argument user_pool_tier", value=user_pool_tier, expected_type=type_hints["user_pool_tier"])
            check_type(argname="argument verification_message_template", value=verification_message_template, expected_type=type_hints["verification_message_template"])
            check_type(argname="argument web_authn_configuration", value=web_authn_configuration, expected_type=type_hints["web_authn_configuration"])
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
        if account_recovery_setting is not None:
            self._values["account_recovery_setting"] = account_recovery_setting
        if admin_create_user_config is not None:
            self._values["admin_create_user_config"] = admin_create_user_config
        if alias_attributes is not None:
            self._values["alias_attributes"] = alias_attributes
        if auto_verified_attributes is not None:
            self._values["auto_verified_attributes"] = auto_verified_attributes
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if device_configuration is not None:
            self._values["device_configuration"] = device_configuration
        if email_configuration is not None:
            self._values["email_configuration"] = email_configuration
        if email_mfa_configuration is not None:
            self._values["email_mfa_configuration"] = email_mfa_configuration
        if email_verification_message is not None:
            self._values["email_verification_message"] = email_verification_message
        if email_verification_subject is not None:
            self._values["email_verification_subject"] = email_verification_subject
        if id is not None:
            self._values["id"] = id
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if mfa_configuration is not None:
            self._values["mfa_configuration"] = mfa_configuration
        if password_policy is not None:
            self._values["password_policy"] = password_policy
        if region is not None:
            self._values["region"] = region
        if schema is not None:
            self._values["schema"] = schema
        if sign_in_policy is not None:
            self._values["sign_in_policy"] = sign_in_policy
        if sms_authentication_message is not None:
            self._values["sms_authentication_message"] = sms_authentication_message
        if sms_configuration is not None:
            self._values["sms_configuration"] = sms_configuration
        if sms_verification_message is not None:
            self._values["sms_verification_message"] = sms_verification_message
        if software_token_mfa_configuration is not None:
            self._values["software_token_mfa_configuration"] = software_token_mfa_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if user_attribute_update_settings is not None:
            self._values["user_attribute_update_settings"] = user_attribute_update_settings
        if username_attributes is not None:
            self._values["username_attributes"] = username_attributes
        if username_configuration is not None:
            self._values["username_configuration"] = username_configuration
        if user_pool_add_ons is not None:
            self._values["user_pool_add_ons"] = user_pool_add_ons
        if user_pool_tier is not None:
            self._values["user_pool_tier"] = user_pool_tier
        if verification_message_template is not None:
            self._values["verification_message_template"] = verification_message_template
        if web_authn_configuration is not None:
            self._values["web_authn_configuration"] = web_authn_configuration

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_recovery_setting(
        self,
    ) -> typing.Optional[CognitoUserPoolAccountRecoverySetting]:
        '''account_recovery_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#account_recovery_setting CognitoUserPool#account_recovery_setting}
        '''
        result = self._values.get("account_recovery_setting")
        return typing.cast(typing.Optional[CognitoUserPoolAccountRecoverySetting], result)

    @builtins.property
    def admin_create_user_config(
        self,
    ) -> typing.Optional[CognitoUserPoolAdminCreateUserConfig]:
        '''admin_create_user_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#admin_create_user_config CognitoUserPool#admin_create_user_config}
        '''
        result = self._values.get("admin_create_user_config")
        return typing.cast(typing.Optional[CognitoUserPoolAdminCreateUserConfig], result)

    @builtins.property
    def alias_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#alias_attributes CognitoUserPool#alias_attributes}.'''
        result = self._values.get("alias_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_verified_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#auto_verified_attributes CognitoUserPool#auto_verified_attributes}.'''
        result = self._values.get("auto_verified_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#deletion_protection CognitoUserPool#deletion_protection}.'''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_configuration(
        self,
    ) -> typing.Optional["CognitoUserPoolDeviceConfiguration"]:
        '''device_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#device_configuration CognitoUserPool#device_configuration}
        '''
        result = self._values.get("device_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolDeviceConfiguration"], result)

    @builtins.property
    def email_configuration(
        self,
    ) -> typing.Optional["CognitoUserPoolEmailConfiguration"]:
        '''email_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_configuration CognitoUserPool#email_configuration}
        '''
        result = self._values.get("email_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolEmailConfiguration"], result)

    @builtins.property
    def email_mfa_configuration(
        self,
    ) -> typing.Optional["CognitoUserPoolEmailMfaConfiguration"]:
        '''email_mfa_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_mfa_configuration CognitoUserPool#email_mfa_configuration}
        '''
        result = self._values.get("email_mfa_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolEmailMfaConfiguration"], result)

    @builtins.property
    def email_verification_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_verification_message CognitoUserPool#email_verification_message}.'''
        result = self._values.get("email_verification_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_verification_subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_verification_subject CognitoUserPool#email_verification_subject}.'''
        result = self._values.get("email_verification_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#id CognitoUserPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_config(self) -> typing.Optional["CognitoUserPoolLambdaConfig"]:
        '''lambda_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_config CognitoUserPool#lambda_config}
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional["CognitoUserPoolLambdaConfig"], result)

    @builtins.property
    def mfa_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#mfa_configuration CognitoUserPool#mfa_configuration}.'''
        result = self._values.get("mfa_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_policy(self) -> typing.Optional["CognitoUserPoolPasswordPolicy"]:
        '''password_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#password_policy CognitoUserPool#password_policy}
        '''
        result = self._values.get("password_policy")
        return typing.cast(typing.Optional["CognitoUserPoolPasswordPolicy"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#region CognitoUserPool#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolSchema"]]]:
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#schema CognitoUserPool#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CognitoUserPoolSchema"]]], result)

    @builtins.property
    def sign_in_policy(self) -> typing.Optional["CognitoUserPoolSignInPolicy"]:
        '''sign_in_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sign_in_policy CognitoUserPool#sign_in_policy}
        '''
        result = self._values.get("sign_in_policy")
        return typing.cast(typing.Optional["CognitoUserPoolSignInPolicy"], result)

    @builtins.property
    def sms_authentication_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_authentication_message CognitoUserPool#sms_authentication_message}.'''
        result = self._values.get("sms_authentication_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sms_configuration(self) -> typing.Optional["CognitoUserPoolSmsConfiguration"]:
        '''sms_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_configuration CognitoUserPool#sms_configuration}
        '''
        result = self._values.get("sms_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolSmsConfiguration"], result)

    @builtins.property
    def sms_verification_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_verification_message CognitoUserPool#sms_verification_message}.'''
        result = self._values.get("sms_verification_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_token_mfa_configuration(
        self,
    ) -> typing.Optional["CognitoUserPoolSoftwareTokenMfaConfiguration"]:
        '''software_token_mfa_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#software_token_mfa_configuration CognitoUserPool#software_token_mfa_configuration}
        '''
        result = self._values.get("software_token_mfa_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolSoftwareTokenMfaConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#tags CognitoUserPool#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#tags_all CognitoUserPool#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user_attribute_update_settings(
        self,
    ) -> typing.Optional["CognitoUserPoolUserAttributeUpdateSettings"]:
        '''user_attribute_update_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_attribute_update_settings CognitoUserPool#user_attribute_update_settings}
        '''
        result = self._values.get("user_attribute_update_settings")
        return typing.cast(typing.Optional["CognitoUserPoolUserAttributeUpdateSettings"], result)

    @builtins.property
    def username_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#username_attributes CognitoUserPool#username_attributes}.'''
        result = self._values.get("username_attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username_configuration(
        self,
    ) -> typing.Optional["CognitoUserPoolUsernameConfiguration"]:
        '''username_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#username_configuration CognitoUserPool#username_configuration}
        '''
        result = self._values.get("username_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolUsernameConfiguration"], result)

    @builtins.property
    def user_pool_add_ons(self) -> typing.Optional["CognitoUserPoolUserPoolAddOns"]:
        '''user_pool_add_ons block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_pool_add_ons CognitoUserPool#user_pool_add_ons}
        '''
        result = self._values.get("user_pool_add_ons")
        return typing.cast(typing.Optional["CognitoUserPoolUserPoolAddOns"], result)

    @builtins.property
    def user_pool_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_pool_tier CognitoUserPool#user_pool_tier}.'''
        result = self._values.get("user_pool_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verification_message_template(
        self,
    ) -> typing.Optional["CognitoUserPoolVerificationMessageTemplate"]:
        '''verification_message_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#verification_message_template CognitoUserPool#verification_message_template}
        '''
        result = self._values.get("verification_message_template")
        return typing.cast(typing.Optional["CognitoUserPoolVerificationMessageTemplate"], result)

    @builtins.property
    def web_authn_configuration(
        self,
    ) -> typing.Optional["CognitoUserPoolWebAuthnConfiguration"]:
        '''web_authn_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#web_authn_configuration CognitoUserPool#web_authn_configuration}
        '''
        result = self._values.get("web_authn_configuration")
        return typing.cast(typing.Optional["CognitoUserPoolWebAuthnConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolDeviceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "challenge_required_on_new_device": "challengeRequiredOnNewDevice",
        "device_only_remembered_on_user_prompt": "deviceOnlyRememberedOnUserPrompt",
    },
)
class CognitoUserPoolDeviceConfiguration:
    def __init__(
        self,
        *,
        challenge_required_on_new_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_only_remembered_on_user_prompt: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param challenge_required_on_new_device: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#challenge_required_on_new_device CognitoUserPool#challenge_required_on_new_device}.
        :param device_only_remembered_on_user_prompt: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#device_only_remembered_on_user_prompt CognitoUserPool#device_only_remembered_on_user_prompt}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038225e22036b1b3e2653fbc0f1e10a2d66604953c8f50c95052f554a0b456ba)
            check_type(argname="argument challenge_required_on_new_device", value=challenge_required_on_new_device, expected_type=type_hints["challenge_required_on_new_device"])
            check_type(argname="argument device_only_remembered_on_user_prompt", value=device_only_remembered_on_user_prompt, expected_type=type_hints["device_only_remembered_on_user_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if challenge_required_on_new_device is not None:
            self._values["challenge_required_on_new_device"] = challenge_required_on_new_device
        if device_only_remembered_on_user_prompt is not None:
            self._values["device_only_remembered_on_user_prompt"] = device_only_remembered_on_user_prompt

    @builtins.property
    def challenge_required_on_new_device(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#challenge_required_on_new_device CognitoUserPool#challenge_required_on_new_device}.'''
        result = self._values.get("challenge_required_on_new_device")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def device_only_remembered_on_user_prompt(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#device_only_remembered_on_user_prompt CognitoUserPool#device_only_remembered_on_user_prompt}.'''
        result = self._values.get("device_only_remembered_on_user_prompt")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolDeviceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolDeviceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolDeviceConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d08fe8f92d2259e9a3224bcc8c65dcba60431cad6063ea6083fe56f53d9d987b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChallengeRequiredOnNewDevice")
    def reset_challenge_required_on_new_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChallengeRequiredOnNewDevice", []))

    @jsii.member(jsii_name="resetDeviceOnlyRememberedOnUserPrompt")
    def reset_device_only_remembered_on_user_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceOnlyRememberedOnUserPrompt", []))

    @builtins.property
    @jsii.member(jsii_name="challengeRequiredOnNewDeviceInput")
    def challenge_required_on_new_device_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "challengeRequiredOnNewDeviceInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceOnlyRememberedOnUserPromptInput")
    def device_only_remembered_on_user_prompt_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deviceOnlyRememberedOnUserPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="challengeRequiredOnNewDevice")
    def challenge_required_on_new_device(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "challengeRequiredOnNewDevice"))

    @challenge_required_on_new_device.setter
    def challenge_required_on_new_device(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7875426dd1d30b7b4697fd10593778624e25fb03328f14bee13c1aa4af1245c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "challengeRequiredOnNewDevice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceOnlyRememberedOnUserPrompt")
    def device_only_remembered_on_user_prompt(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deviceOnlyRememberedOnUserPrompt"))

    @device_only_remembered_on_user_prompt.setter
    def device_only_remembered_on_user_prompt(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db70f8e76153ce365f56f3ad1ea9f90d60dbb2b26ff018d66f5fabfd0b10da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceOnlyRememberedOnUserPrompt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolDeviceConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolDeviceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolDeviceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6828cacb3d671be9b565bfa11715b12afc6a14ee62f3f3fd89c72b15ce9d7e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolEmailConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_set": "configurationSet",
        "email_sending_account": "emailSendingAccount",
        "from_email_address": "fromEmailAddress",
        "reply_to_email_address": "replyToEmailAddress",
        "source_arn": "sourceArn",
    },
)
class CognitoUserPoolEmailConfiguration:
    def __init__(
        self,
        *,
        configuration_set: typing.Optional[builtins.str] = None,
        email_sending_account: typing.Optional[builtins.str] = None,
        from_email_address: typing.Optional[builtins.str] = None,
        reply_to_email_address: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param configuration_set: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#configuration_set CognitoUserPool#configuration_set}.
        :param email_sending_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_sending_account CognitoUserPool#email_sending_account}.
        :param from_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#from_email_address CognitoUserPool#from_email_address}.
        :param reply_to_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#reply_to_email_address CognitoUserPool#reply_to_email_address}.
        :param source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#source_arn CognitoUserPool#source_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e46f6ef87a1a4d79ac90e481a9af37fd093e1c663cfa7f440d669739e4618d0)
            check_type(argname="argument configuration_set", value=configuration_set, expected_type=type_hints["configuration_set"])
            check_type(argname="argument email_sending_account", value=email_sending_account, expected_type=type_hints["email_sending_account"])
            check_type(argname="argument from_email_address", value=from_email_address, expected_type=type_hints["from_email_address"])
            check_type(argname="argument reply_to_email_address", value=reply_to_email_address, expected_type=type_hints["reply_to_email_address"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_set is not None:
            self._values["configuration_set"] = configuration_set
        if email_sending_account is not None:
            self._values["email_sending_account"] = email_sending_account
        if from_email_address is not None:
            self._values["from_email_address"] = from_email_address
        if reply_to_email_address is not None:
            self._values["reply_to_email_address"] = reply_to_email_address
        if source_arn is not None:
            self._values["source_arn"] = source_arn

    @builtins.property
    def configuration_set(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#configuration_set CognitoUserPool#configuration_set}.'''
        result = self._values.get("configuration_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_sending_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_sending_account CognitoUserPool#email_sending_account}.'''
        result = self._values.get("email_sending_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#from_email_address CognitoUserPool#from_email_address}.'''
        result = self._values.get("from_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reply_to_email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#reply_to_email_address CognitoUserPool#reply_to_email_address}.'''
        result = self._values.get("reply_to_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#source_arn CognitoUserPool#source_arn}.'''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolEmailConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolEmailConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolEmailConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b517a3d8ec077750c7aaf16db66d445177c3ef99008ab52e71fabe10d09230ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfigurationSet")
    def reset_configuration_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigurationSet", []))

    @jsii.member(jsii_name="resetEmailSendingAccount")
    def reset_email_sending_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailSendingAccount", []))

    @jsii.member(jsii_name="resetFromEmailAddress")
    def reset_from_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromEmailAddress", []))

    @jsii.member(jsii_name="resetReplyToEmailAddress")
    def reset_reply_to_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplyToEmailAddress", []))

    @jsii.member(jsii_name="resetSourceArn")
    def reset_source_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceArn", []))

    @builtins.property
    @jsii.member(jsii_name="configurationSetInput")
    def configuration_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationSetInput"))

    @builtins.property
    @jsii.member(jsii_name="emailSendingAccountInput")
    def email_sending_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailSendingAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="fromEmailAddressInput")
    def from_email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromEmailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="replyToEmailAddressInput")
    def reply_to_email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replyToEmailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceArnInput")
    def source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationSet")
    def configuration_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationSet"))

    @configuration_set.setter
    def configuration_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd9a8a19e904d77fed7306968b37ee053803bf2d008bf13ae446e3645a5e3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailSendingAccount")
    def email_sending_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailSendingAccount"))

    @email_sending_account.setter
    def email_sending_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31b7f3d521474bc28bec01bb669d0a6ea307ede0edf18c6cf79d09de2f77316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailSendingAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fromEmailAddress")
    def from_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromEmailAddress"))

    @from_email_address.setter
    def from_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3729b49d3795aa2acb80589c036e007083cfffbf177a66a0d0d9fcac22ba05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromEmailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replyToEmailAddress")
    def reply_to_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replyToEmailAddress"))

    @reply_to_email_address.setter
    def reply_to_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e7bf55fa18b4a5a8faf64090d3989ab25add6ede84a8608df6ddbb83616947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replyToEmailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290d94ea9eb2ada2fcf7cd15ff4061fc1cc76da26710955e88e89358264933c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolEmailConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolEmailConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolEmailConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2ec708c45c1f1e4dec62b6d5a959799785101fc9bd28e09df3ead8ba7e75d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolEmailMfaConfiguration",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "subject": "subject"},
)
class CognitoUserPoolEmailMfaConfiguration:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#message CognitoUserPool#message}.
        :param subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#subject CognitoUserPool#subject}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b23416bbce4591c8bbf56547aa67f2aa695a2ba91267ff0301646522a8c223)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#message CognitoUserPool#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#subject CognitoUserPool#subject}.'''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolEmailMfaConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolEmailMfaConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolEmailMfaConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcc61590ff37fd760de7adb4c7a60099d50ab14e3c53822e4bf9e582fe52f691)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4d7aa280824df4107c3e69fb4b27a0a1e93075534cb3cb3be6eb34eb53fc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0990cfa6050bdab8542f30ca1ff4e18b1fc6c616bb27ae1ab65a2d59b2ea28af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolEmailMfaConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolEmailMfaConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolEmailMfaConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6790a45977fc7d62e34b88019e0b8161d1b700b4c461b8e324c9834052b20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfig",
    jsii_struct_bases=[],
    name_mapping={
        "create_auth_challenge": "createAuthChallenge",
        "custom_email_sender": "customEmailSender",
        "custom_message": "customMessage",
        "custom_sms_sender": "customSmsSender",
        "define_auth_challenge": "defineAuthChallenge",
        "kms_key_id": "kmsKeyId",
        "post_authentication": "postAuthentication",
        "post_confirmation": "postConfirmation",
        "pre_authentication": "preAuthentication",
        "pre_sign_up": "preSignUp",
        "pre_token_generation": "preTokenGeneration",
        "pre_token_generation_config": "preTokenGenerationConfig",
        "user_migration": "userMigration",
        "verify_auth_challenge_response": "verifyAuthChallengeResponse",
    },
)
class CognitoUserPoolLambdaConfig:
    def __init__(
        self,
        *,
        create_auth_challenge: typing.Optional[builtins.str] = None,
        custom_email_sender: typing.Optional[typing.Union["CognitoUserPoolLambdaConfigCustomEmailSender", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_message: typing.Optional[builtins.str] = None,
        custom_sms_sender: typing.Optional[typing.Union["CognitoUserPoolLambdaConfigCustomSmsSender", typing.Dict[builtins.str, typing.Any]]] = None,
        define_auth_challenge: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        post_authentication: typing.Optional[builtins.str] = None,
        post_confirmation: typing.Optional[builtins.str] = None,
        pre_authentication: typing.Optional[builtins.str] = None,
        pre_sign_up: typing.Optional[builtins.str] = None,
        pre_token_generation: typing.Optional[builtins.str] = None,
        pre_token_generation_config: typing.Optional[typing.Union["CognitoUserPoolLambdaConfigPreTokenGenerationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_migration: typing.Optional[builtins.str] = None,
        verify_auth_challenge_response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_auth_challenge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#create_auth_challenge CognitoUserPool#create_auth_challenge}.
        :param custom_email_sender: custom_email_sender block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_email_sender CognitoUserPool#custom_email_sender}
        :param custom_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_message CognitoUserPool#custom_message}.
        :param custom_sms_sender: custom_sms_sender block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_sms_sender CognitoUserPool#custom_sms_sender}
        :param define_auth_challenge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#define_auth_challenge CognitoUserPool#define_auth_challenge}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#kms_key_id CognitoUserPool#kms_key_id}.
        :param post_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#post_authentication CognitoUserPool#post_authentication}.
        :param post_confirmation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#post_confirmation CognitoUserPool#post_confirmation}.
        :param pre_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_authentication CognitoUserPool#pre_authentication}.
        :param pre_sign_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_sign_up CognitoUserPool#pre_sign_up}.
        :param pre_token_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_token_generation CognitoUserPool#pre_token_generation}.
        :param pre_token_generation_config: pre_token_generation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_token_generation_config CognitoUserPool#pre_token_generation_config}
        :param user_migration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_migration CognitoUserPool#user_migration}.
        :param verify_auth_challenge_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#verify_auth_challenge_response CognitoUserPool#verify_auth_challenge_response}.
        '''
        if isinstance(custom_email_sender, dict):
            custom_email_sender = CognitoUserPoolLambdaConfigCustomEmailSender(**custom_email_sender)
        if isinstance(custom_sms_sender, dict):
            custom_sms_sender = CognitoUserPoolLambdaConfigCustomSmsSender(**custom_sms_sender)
        if isinstance(pre_token_generation_config, dict):
            pre_token_generation_config = CognitoUserPoolLambdaConfigPreTokenGenerationConfig(**pre_token_generation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668acb7eb5e07f5b965d50a16ee29f7e922060ca574534a61d63780b2e08343d)
            check_type(argname="argument create_auth_challenge", value=create_auth_challenge, expected_type=type_hints["create_auth_challenge"])
            check_type(argname="argument custom_email_sender", value=custom_email_sender, expected_type=type_hints["custom_email_sender"])
            check_type(argname="argument custom_message", value=custom_message, expected_type=type_hints["custom_message"])
            check_type(argname="argument custom_sms_sender", value=custom_sms_sender, expected_type=type_hints["custom_sms_sender"])
            check_type(argname="argument define_auth_challenge", value=define_auth_challenge, expected_type=type_hints["define_auth_challenge"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument post_authentication", value=post_authentication, expected_type=type_hints["post_authentication"])
            check_type(argname="argument post_confirmation", value=post_confirmation, expected_type=type_hints["post_confirmation"])
            check_type(argname="argument pre_authentication", value=pre_authentication, expected_type=type_hints["pre_authentication"])
            check_type(argname="argument pre_sign_up", value=pre_sign_up, expected_type=type_hints["pre_sign_up"])
            check_type(argname="argument pre_token_generation", value=pre_token_generation, expected_type=type_hints["pre_token_generation"])
            check_type(argname="argument pre_token_generation_config", value=pre_token_generation_config, expected_type=type_hints["pre_token_generation_config"])
            check_type(argname="argument user_migration", value=user_migration, expected_type=type_hints["user_migration"])
            check_type(argname="argument verify_auth_challenge_response", value=verify_auth_challenge_response, expected_type=type_hints["verify_auth_challenge_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_auth_challenge is not None:
            self._values["create_auth_challenge"] = create_auth_challenge
        if custom_email_sender is not None:
            self._values["custom_email_sender"] = custom_email_sender
        if custom_message is not None:
            self._values["custom_message"] = custom_message
        if custom_sms_sender is not None:
            self._values["custom_sms_sender"] = custom_sms_sender
        if define_auth_challenge is not None:
            self._values["define_auth_challenge"] = define_auth_challenge
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if post_authentication is not None:
            self._values["post_authentication"] = post_authentication
        if post_confirmation is not None:
            self._values["post_confirmation"] = post_confirmation
        if pre_authentication is not None:
            self._values["pre_authentication"] = pre_authentication
        if pre_sign_up is not None:
            self._values["pre_sign_up"] = pre_sign_up
        if pre_token_generation is not None:
            self._values["pre_token_generation"] = pre_token_generation
        if pre_token_generation_config is not None:
            self._values["pre_token_generation_config"] = pre_token_generation_config
        if user_migration is not None:
            self._values["user_migration"] = user_migration
        if verify_auth_challenge_response is not None:
            self._values["verify_auth_challenge_response"] = verify_auth_challenge_response

    @builtins.property
    def create_auth_challenge(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#create_auth_challenge CognitoUserPool#create_auth_challenge}.'''
        result = self._values.get("create_auth_challenge")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_email_sender(
        self,
    ) -> typing.Optional["CognitoUserPoolLambdaConfigCustomEmailSender"]:
        '''custom_email_sender block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_email_sender CognitoUserPool#custom_email_sender}
        '''
        result = self._values.get("custom_email_sender")
        return typing.cast(typing.Optional["CognitoUserPoolLambdaConfigCustomEmailSender"], result)

    @builtins.property
    def custom_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_message CognitoUserPool#custom_message}.'''
        result = self._values.get("custom_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_sms_sender(
        self,
    ) -> typing.Optional["CognitoUserPoolLambdaConfigCustomSmsSender"]:
        '''custom_sms_sender block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_sms_sender CognitoUserPool#custom_sms_sender}
        '''
        result = self._values.get("custom_sms_sender")
        return typing.cast(typing.Optional["CognitoUserPoolLambdaConfigCustomSmsSender"], result)

    @builtins.property
    def define_auth_challenge(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#define_auth_challenge CognitoUserPool#define_auth_challenge}.'''
        result = self._values.get("define_auth_challenge")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#kms_key_id CognitoUserPool#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_authentication(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#post_authentication CognitoUserPool#post_authentication}.'''
        result = self._values.get("post_authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_confirmation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#post_confirmation CognitoUserPool#post_confirmation}.'''
        result = self._values.get("post_confirmation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_authentication(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_authentication CognitoUserPool#pre_authentication}.'''
        result = self._values.get("pre_authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_sign_up(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_sign_up CognitoUserPool#pre_sign_up}.'''
        result = self._values.get("pre_sign_up")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_token_generation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_token_generation CognitoUserPool#pre_token_generation}.'''
        result = self._values.get("pre_token_generation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_token_generation_config(
        self,
    ) -> typing.Optional["CognitoUserPoolLambdaConfigPreTokenGenerationConfig"]:
        '''pre_token_generation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#pre_token_generation_config CognitoUserPool#pre_token_generation_config}
        '''
        result = self._values.get("pre_token_generation_config")
        return typing.cast(typing.Optional["CognitoUserPoolLambdaConfigPreTokenGenerationConfig"], result)

    @builtins.property
    def user_migration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_migration CognitoUserPool#user_migration}.'''
        result = self._values.get("user_migration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_auth_challenge_response(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#verify_auth_challenge_response CognitoUserPool#verify_auth_challenge_response}.'''
        result = self._values.get("verify_auth_challenge_response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolLambdaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigCustomEmailSender",
    jsii_struct_bases=[],
    name_mapping={"lambda_arn": "lambdaArn", "lambda_version": "lambdaVersion"},
)
class CognitoUserPoolLambdaConfigCustomEmailSender:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        lambda_version: builtins.str,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.
        :param lambda_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ff3f4731fd10b0753a24c785e16c45db565e2c2ddfa564b873623de4277a32)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument lambda_version", value=lambda_version, expected_type=type_hints["lambda_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "lambda_version": lambda_version,
        }

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.'''
        result = self._values.get("lambda_version")
        assert result is not None, "Required property 'lambda_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolLambdaConfigCustomEmailSender(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolLambdaConfigCustomEmailSenderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigCustomEmailSenderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8444a0cfcbcb9aeab68508356c8312a525985a21cc88e94b64b0f821da769ead)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaVersionInput")
    def lambda_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bc85444a8c645ddc6ff4027f8532be2ec9433781dd954294a6d4fb471ef21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaVersion")
    def lambda_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaVersion"))

    @lambda_version.setter
    def lambda_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04819a67abe91a7988a216b0402958f05ff983f70f16da72890fef42995ad44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolLambdaConfigCustomEmailSender]:
        return typing.cast(typing.Optional[CognitoUserPoolLambdaConfigCustomEmailSender], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolLambdaConfigCustomEmailSender],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9f6c105a8a1d8f725f2218e91fc30df3e141fe50a4b5729697e8a1e6b17dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigCustomSmsSender",
    jsii_struct_bases=[],
    name_mapping={"lambda_arn": "lambdaArn", "lambda_version": "lambdaVersion"},
)
class CognitoUserPoolLambdaConfigCustomSmsSender:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        lambda_version: builtins.str,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.
        :param lambda_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d83acf85af820d2231daebe78f7f77d3d362c6f830648a482c5d9280f360042)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument lambda_version", value=lambda_version, expected_type=type_hints["lambda_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "lambda_version": lambda_version,
        }

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.'''
        result = self._values.get("lambda_version")
        assert result is not None, "Required property 'lambda_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolLambdaConfigCustomSmsSender(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolLambdaConfigCustomSmsSenderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigCustomSmsSenderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81adec252b7a5b3a9e40b34b940e5f0264c7630667832f5398a8e48774c5a21a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaVersionInput")
    def lambda_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd9002c835aa805436fcbfbe570fc50f33c4c591ec4f042417feb225d6e7228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaVersion")
    def lambda_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaVersion"))

    @lambda_version.setter
    def lambda_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0907623f3dba649d70afe96632201b79642bf5398817e92fc553c90da9afe90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolLambdaConfigCustomSmsSender]:
        return typing.cast(typing.Optional[CognitoUserPoolLambdaConfigCustomSmsSender], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolLambdaConfigCustomSmsSender],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde587a29bfd8341dc5cf0c4e8658b7fb3701a2f56122f27ee1927a5d8137a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoUserPoolLambdaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f737d212b2d5001fd75cc6fa7e3cd81ac6630c2f262d3d1ee5dc130ea26b21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomEmailSender")
    def put_custom_email_sender(
        self,
        *,
        lambda_arn: builtins.str,
        lambda_version: builtins.str,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.
        :param lambda_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.
        '''
        value = CognitoUserPoolLambdaConfigCustomEmailSender(
            lambda_arn=lambda_arn, lambda_version=lambda_version
        )

        return typing.cast(None, jsii.invoke(self, "putCustomEmailSender", [value]))

    @jsii.member(jsii_name="putCustomSmsSender")
    def put_custom_sms_sender(
        self,
        *,
        lambda_arn: builtins.str,
        lambda_version: builtins.str,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.
        :param lambda_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.
        '''
        value = CognitoUserPoolLambdaConfigCustomSmsSender(
            lambda_arn=lambda_arn, lambda_version=lambda_version
        )

        return typing.cast(None, jsii.invoke(self, "putCustomSmsSender", [value]))

    @jsii.member(jsii_name="putPreTokenGenerationConfig")
    def put_pre_token_generation_config(
        self,
        *,
        lambda_arn: builtins.str,
        lambda_version: builtins.str,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.
        :param lambda_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.
        '''
        value = CognitoUserPoolLambdaConfigPreTokenGenerationConfig(
            lambda_arn=lambda_arn, lambda_version=lambda_version
        )

        return typing.cast(None, jsii.invoke(self, "putPreTokenGenerationConfig", [value]))

    @jsii.member(jsii_name="resetCreateAuthChallenge")
    def reset_create_auth_challenge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAuthChallenge", []))

    @jsii.member(jsii_name="resetCustomEmailSender")
    def reset_custom_email_sender(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEmailSender", []))

    @jsii.member(jsii_name="resetCustomMessage")
    def reset_custom_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMessage", []))

    @jsii.member(jsii_name="resetCustomSmsSender")
    def reset_custom_sms_sender(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSmsSender", []))

    @jsii.member(jsii_name="resetDefineAuthChallenge")
    def reset_define_auth_challenge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefineAuthChallenge", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetPostAuthentication")
    def reset_post_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostAuthentication", []))

    @jsii.member(jsii_name="resetPostConfirmation")
    def reset_post_confirmation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostConfirmation", []))

    @jsii.member(jsii_name="resetPreAuthentication")
    def reset_pre_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreAuthentication", []))

    @jsii.member(jsii_name="resetPreSignUp")
    def reset_pre_sign_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreSignUp", []))

    @jsii.member(jsii_name="resetPreTokenGeneration")
    def reset_pre_token_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreTokenGeneration", []))

    @jsii.member(jsii_name="resetPreTokenGenerationConfig")
    def reset_pre_token_generation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreTokenGenerationConfig", []))

    @jsii.member(jsii_name="resetUserMigration")
    def reset_user_migration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserMigration", []))

    @jsii.member(jsii_name="resetVerifyAuthChallengeResponse")
    def reset_verify_auth_challenge_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyAuthChallengeResponse", []))

    @builtins.property
    @jsii.member(jsii_name="customEmailSender")
    def custom_email_sender(
        self,
    ) -> CognitoUserPoolLambdaConfigCustomEmailSenderOutputReference:
        return typing.cast(CognitoUserPoolLambdaConfigCustomEmailSenderOutputReference, jsii.get(self, "customEmailSender"))

    @builtins.property
    @jsii.member(jsii_name="customSmsSender")
    def custom_sms_sender(
        self,
    ) -> CognitoUserPoolLambdaConfigCustomSmsSenderOutputReference:
        return typing.cast(CognitoUserPoolLambdaConfigCustomSmsSenderOutputReference, jsii.get(self, "customSmsSender"))

    @builtins.property
    @jsii.member(jsii_name="preTokenGenerationConfig")
    def pre_token_generation_config(
        self,
    ) -> "CognitoUserPoolLambdaConfigPreTokenGenerationConfigOutputReference":
        return typing.cast("CognitoUserPoolLambdaConfigPreTokenGenerationConfigOutputReference", jsii.get(self, "preTokenGenerationConfig"))

    @builtins.property
    @jsii.member(jsii_name="createAuthChallengeInput")
    def create_auth_challenge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createAuthChallengeInput"))

    @builtins.property
    @jsii.member(jsii_name="customEmailSenderInput")
    def custom_email_sender_input(
        self,
    ) -> typing.Optional[CognitoUserPoolLambdaConfigCustomEmailSender]:
        return typing.cast(typing.Optional[CognitoUserPoolLambdaConfigCustomEmailSender], jsii.get(self, "customEmailSenderInput"))

    @builtins.property
    @jsii.member(jsii_name="customMessageInput")
    def custom_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="customSmsSenderInput")
    def custom_sms_sender_input(
        self,
    ) -> typing.Optional[CognitoUserPoolLambdaConfigCustomSmsSender]:
        return typing.cast(typing.Optional[CognitoUserPoolLambdaConfigCustomSmsSender], jsii.get(self, "customSmsSenderInput"))

    @builtins.property
    @jsii.member(jsii_name="defineAuthChallengeInput")
    def define_auth_challenge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defineAuthChallengeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="postAuthenticationInput")
    def post_authentication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="postConfirmationInput")
    def post_confirmation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postConfirmationInput"))

    @builtins.property
    @jsii.member(jsii_name="preAuthenticationInput")
    def pre_authentication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="preSignUpInput")
    def pre_sign_up_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preSignUpInput"))

    @builtins.property
    @jsii.member(jsii_name="preTokenGenerationConfigInput")
    def pre_token_generation_config_input(
        self,
    ) -> typing.Optional["CognitoUserPoolLambdaConfigPreTokenGenerationConfig"]:
        return typing.cast(typing.Optional["CognitoUserPoolLambdaConfigPreTokenGenerationConfig"], jsii.get(self, "preTokenGenerationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="preTokenGenerationInput")
    def pre_token_generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preTokenGenerationInput"))

    @builtins.property
    @jsii.member(jsii_name="userMigrationInput")
    def user_migration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userMigrationInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyAuthChallengeResponseInput")
    def verify_auth_challenge_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verifyAuthChallengeResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="createAuthChallenge")
    def create_auth_challenge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAuthChallenge"))

    @create_auth_challenge.setter
    def create_auth_challenge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedab9c41db5f7cd63eec3d26bfb33163224b63ff93799ccf049404400e8fffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAuthChallenge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customMessage")
    def custom_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customMessage"))

    @custom_message.setter
    def custom_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5495cf8535a7cd7a444974c3628232f53974026161e3b1205e60b40b62746ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defineAuthChallenge")
    def define_auth_challenge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defineAuthChallenge"))

    @define_auth_challenge.setter
    def define_auth_challenge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288ecc3e848c1493f63632dec3e6d54bad3fe452f5cc767ec0cadd9c226a43a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defineAuthChallenge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfc396c8b46ba5f4dc8bf8e8dbf687099b54f06a2caecef6a947b2fba065166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postAuthentication")
    def post_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postAuthentication"))

    @post_authentication.setter
    def post_authentication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb0e8913a029e8916a51026459a703958ddb72bb0fc05c560a350bf505e08e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postConfirmation")
    def post_confirmation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postConfirmation"))

    @post_confirmation.setter
    def post_confirmation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfcfadc3a87ecf317ea17c1392845a68a019b91ef1e0074a0dc8ed9a60f4c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postConfirmation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preAuthentication")
    def pre_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preAuthentication"))

    @pre_authentication.setter
    def pre_authentication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77186cccf33eef4558802168f25a9ec3d498026b249efd7e7018d66581f0551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preSignUp")
    def pre_sign_up(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preSignUp"))

    @pre_sign_up.setter
    def pre_sign_up(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a2d2ee74660017949e2d21172fa7629071c0c3eb98cd8bac90fff7bf7f906c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preSignUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preTokenGeneration")
    def pre_token_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preTokenGeneration"))

    @pre_token_generation.setter
    def pre_token_generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68dcf081de741a8d6798ccf79cd6e18ff49043d771a9eb71173f1af0db4d63e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preTokenGeneration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userMigration")
    def user_migration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userMigration"))

    @user_migration.setter
    def user_migration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd7e7070f4e163d5e7e0ce9827f49c3a5f3382b32a33735273faa004fc9872e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userMigration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifyAuthChallengeResponse")
    def verify_auth_challenge_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verifyAuthChallengeResponse"))

    @verify_auth_challenge_response.setter
    def verify_auth_challenge_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a3c54f03c77fb1671d68766a4e1aa0f0a013068d9d591b74e6330bbfbc77ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyAuthChallengeResponse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolLambdaConfig]:
        return typing.cast(typing.Optional[CognitoUserPoolLambdaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolLambdaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd53d4fa3adf45f8a3b251156a8e3d93dfa7212506604cef3bdf919479ed7f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigPreTokenGenerationConfig",
    jsii_struct_bases=[],
    name_mapping={"lambda_arn": "lambdaArn", "lambda_version": "lambdaVersion"},
)
class CognitoUserPoolLambdaConfigPreTokenGenerationConfig:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        lambda_version: builtins.str,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.
        :param lambda_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcfff89af6b040567caf36a7bb46a51baa33e0393f91a89909debf7e915d23c)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument lambda_version", value=lambda_version, expected_type=type_hints["lambda_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "lambda_version": lambda_version,
        }

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_arn CognitoUserPool#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#lambda_version CognitoUserPool#lambda_version}.'''
        result = self._values.get("lambda_version")
        assert result is not None, "Required property 'lambda_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolLambdaConfigPreTokenGenerationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolLambdaConfigPreTokenGenerationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolLambdaConfigPreTokenGenerationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb1acd990c3595be9bb14927a439e0c2ea5f281568307741cb824043757bdeaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaVersionInput")
    def lambda_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519979e234a5869bbf1dfda58fe2e33f0fdc72386761352b8fddfa0ec7b1a4c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaVersion")
    def lambda_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaVersion"))

    @lambda_version.setter
    def lambda_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7eb803910af59879354209ced3a66e71981c2f57563f74c9a86d9257eb8e9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolLambdaConfigPreTokenGenerationConfig]:
        return typing.cast(typing.Optional[CognitoUserPoolLambdaConfigPreTokenGenerationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolLambdaConfigPreTokenGenerationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5cc67024120d581f457a94e5a49588ae5045082d537ef0772482f856830b954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolPasswordPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "minimum_length": "minimumLength",
        "password_history_size": "passwordHistorySize",
        "require_lowercase": "requireLowercase",
        "require_numbers": "requireNumbers",
        "require_symbols": "requireSymbols",
        "require_uppercase": "requireUppercase",
        "temporary_password_validity_days": "temporaryPasswordValidityDays",
    },
)
class CognitoUserPoolPasswordPolicy:
    def __init__(
        self,
        *,
        minimum_length: typing.Optional[jsii.Number] = None,
        password_history_size: typing.Optional[jsii.Number] = None,
        require_lowercase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_numbers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_symbols: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_uppercase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        temporary_password_validity_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param minimum_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#minimum_length CognitoUserPool#minimum_length}.
        :param password_history_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#password_history_size CognitoUserPool#password_history_size}.
        :param require_lowercase: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_lowercase CognitoUserPool#require_lowercase}.
        :param require_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_numbers CognitoUserPool#require_numbers}.
        :param require_symbols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_symbols CognitoUserPool#require_symbols}.
        :param require_uppercase: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_uppercase CognitoUserPool#require_uppercase}.
        :param temporary_password_validity_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#temporary_password_validity_days CognitoUserPool#temporary_password_validity_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5474c2606df3645d4b1f4b09577b47ed8ccf69eeb31096fd25c8f00ab2c5e9)
            check_type(argname="argument minimum_length", value=minimum_length, expected_type=type_hints["minimum_length"])
            check_type(argname="argument password_history_size", value=password_history_size, expected_type=type_hints["password_history_size"])
            check_type(argname="argument require_lowercase", value=require_lowercase, expected_type=type_hints["require_lowercase"])
            check_type(argname="argument require_numbers", value=require_numbers, expected_type=type_hints["require_numbers"])
            check_type(argname="argument require_symbols", value=require_symbols, expected_type=type_hints["require_symbols"])
            check_type(argname="argument require_uppercase", value=require_uppercase, expected_type=type_hints["require_uppercase"])
            check_type(argname="argument temporary_password_validity_days", value=temporary_password_validity_days, expected_type=type_hints["temporary_password_validity_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minimum_length is not None:
            self._values["minimum_length"] = minimum_length
        if password_history_size is not None:
            self._values["password_history_size"] = password_history_size
        if require_lowercase is not None:
            self._values["require_lowercase"] = require_lowercase
        if require_numbers is not None:
            self._values["require_numbers"] = require_numbers
        if require_symbols is not None:
            self._values["require_symbols"] = require_symbols
        if require_uppercase is not None:
            self._values["require_uppercase"] = require_uppercase
        if temporary_password_validity_days is not None:
            self._values["temporary_password_validity_days"] = temporary_password_validity_days

    @builtins.property
    def minimum_length(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#minimum_length CognitoUserPool#minimum_length}.'''
        result = self._values.get("minimum_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_history_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#password_history_size CognitoUserPool#password_history_size}.'''
        result = self._values.get("password_history_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_lowercase(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_lowercase CognitoUserPool#require_lowercase}.'''
        result = self._values.get("require_lowercase")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_numbers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_numbers CognitoUserPool#require_numbers}.'''
        result = self._values.get("require_numbers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_symbols(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_symbols CognitoUserPool#require_symbols}.'''
        result = self._values.get("require_symbols")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_uppercase(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#require_uppercase CognitoUserPool#require_uppercase}.'''
        result = self._values.get("require_uppercase")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def temporary_password_validity_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#temporary_password_validity_days CognitoUserPool#temporary_password_validity_days}.'''
        result = self._values.get("temporary_password_validity_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolPasswordPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolPasswordPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolPasswordPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c4ed2cddca5201211903fbafa0c8b80dd0ad18f33387a7e0435ccc2aeea39bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinimumLength")
    def reset_minimum_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumLength", []))

    @jsii.member(jsii_name="resetPasswordHistorySize")
    def reset_password_history_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordHistorySize", []))

    @jsii.member(jsii_name="resetRequireLowercase")
    def reset_require_lowercase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireLowercase", []))

    @jsii.member(jsii_name="resetRequireNumbers")
    def reset_require_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireNumbers", []))

    @jsii.member(jsii_name="resetRequireSymbols")
    def reset_require_symbols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireSymbols", []))

    @jsii.member(jsii_name="resetRequireUppercase")
    def reset_require_uppercase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireUppercase", []))

    @jsii.member(jsii_name="resetTemporaryPasswordValidityDays")
    def reset_temporary_password_validity_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemporaryPasswordValidityDays", []))

    @builtins.property
    @jsii.member(jsii_name="minimumLengthInput")
    def minimum_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordHistorySizeInput")
    def password_history_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordHistorySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="requireLowercaseInput")
    def require_lowercase_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireLowercaseInput"))

    @builtins.property
    @jsii.member(jsii_name="requireNumbersInput")
    def require_numbers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="requireSymbolsInput")
    def require_symbols_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireSymbolsInput"))

    @builtins.property
    @jsii.member(jsii_name="requireUppercaseInput")
    def require_uppercase_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireUppercaseInput"))

    @builtins.property
    @jsii.member(jsii_name="temporaryPasswordValidityDaysInput")
    def temporary_password_validity_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "temporaryPasswordValidityDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumLength")
    def minimum_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumLength"))

    @minimum_length.setter
    def minimum_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8aa5c4c62dc389d09bc30b4e472ef95ef69aac9658076b3dcb4bc927ec3cda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordHistorySize")
    def password_history_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordHistorySize"))

    @password_history_size.setter
    def password_history_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b402d03080f4778e32cf7f79f0263815c0b046cd6b44fbec18da45737161489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordHistorySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireLowercase")
    def require_lowercase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireLowercase"))

    @require_lowercase.setter
    def require_lowercase(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5a83bf9b84b148f9b7cae7b5be6ea94059c409c8f2efa1eea69d552229321a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireLowercase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireNumbers")
    def require_numbers(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireNumbers"))

    @require_numbers.setter
    def require_numbers(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496cebbff9fee0ebeefe3cdebb5c7fe3130271e0f8598f4d6155eb1abf780b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireSymbols")
    def require_symbols(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireSymbols"))

    @require_symbols.setter
    def require_symbols(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e75aa600685737d48cb18f61fe7068cf58db34fe1bce8a38447cf2ae17dbf35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireSymbols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireUppercase")
    def require_uppercase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireUppercase"))

    @require_uppercase.setter
    def require_uppercase(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332752b9620a9a919ea6056392e826ca5e35c2c95fc06b7a477432a39dc4319a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireUppercase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temporaryPasswordValidityDays")
    def temporary_password_validity_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "temporaryPasswordValidityDays"))

    @temporary_password_validity_days.setter
    def temporary_password_validity_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc959d6c9b7177cf57590c9ca7e16d1942ff5215fd96007f89831980c2e841c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temporaryPasswordValidityDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolPasswordPolicy]:
        return typing.cast(typing.Optional[CognitoUserPoolPasswordPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolPasswordPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0031baa28841a3c22babeed3c88c2099043106f8de4ca0d64fc9419d1ce482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchema",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_data_type": "attributeDataType",
        "name": "name",
        "developer_only_attribute": "developerOnlyAttribute",
        "mutable": "mutable",
        "number_attribute_constraints": "numberAttributeConstraints",
        "required": "required",
        "string_attribute_constraints": "stringAttributeConstraints",
    },
)
class CognitoUserPoolSchema:
    def __init__(
        self,
        *,
        attribute_data_type: builtins.str,
        name: builtins.str,
        developer_only_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        number_attribute_constraints: typing.Optional[typing.Union["CognitoUserPoolSchemaNumberAttributeConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        string_attribute_constraints: typing.Optional[typing.Union["CognitoUserPoolSchemaStringAttributeConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param attribute_data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#attribute_data_type CognitoUserPool#attribute_data_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.
        :param developer_only_attribute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#developer_only_attribute CognitoUserPool#developer_only_attribute}.
        :param mutable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#mutable CognitoUserPool#mutable}.
        :param number_attribute_constraints: number_attribute_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#number_attribute_constraints CognitoUserPool#number_attribute_constraints}
        :param required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#required CognitoUserPool#required}.
        :param string_attribute_constraints: string_attribute_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#string_attribute_constraints CognitoUserPool#string_attribute_constraints}
        '''
        if isinstance(number_attribute_constraints, dict):
            number_attribute_constraints = CognitoUserPoolSchemaNumberAttributeConstraints(**number_attribute_constraints)
        if isinstance(string_attribute_constraints, dict):
            string_attribute_constraints = CognitoUserPoolSchemaStringAttributeConstraints(**string_attribute_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9753d2c4b4d6e595c79a8db36a1870432ba418548868e6393c71a8f8c23c7c46)
            check_type(argname="argument attribute_data_type", value=attribute_data_type, expected_type=type_hints["attribute_data_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument developer_only_attribute", value=developer_only_attribute, expected_type=type_hints["developer_only_attribute"])
            check_type(argname="argument mutable", value=mutable, expected_type=type_hints["mutable"])
            check_type(argname="argument number_attribute_constraints", value=number_attribute_constraints, expected_type=type_hints["number_attribute_constraints"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument string_attribute_constraints", value=string_attribute_constraints, expected_type=type_hints["string_attribute_constraints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute_data_type": attribute_data_type,
            "name": name,
        }
        if developer_only_attribute is not None:
            self._values["developer_only_attribute"] = developer_only_attribute
        if mutable is not None:
            self._values["mutable"] = mutable
        if number_attribute_constraints is not None:
            self._values["number_attribute_constraints"] = number_attribute_constraints
        if required is not None:
            self._values["required"] = required
        if string_attribute_constraints is not None:
            self._values["string_attribute_constraints"] = string_attribute_constraints

    @builtins.property
    def attribute_data_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#attribute_data_type CognitoUserPool#attribute_data_type}.'''
        result = self._values.get("attribute_data_type")
        assert result is not None, "Required property 'attribute_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#name CognitoUserPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def developer_only_attribute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#developer_only_attribute CognitoUserPool#developer_only_attribute}.'''
        result = self._values.get("developer_only_attribute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mutable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#mutable CognitoUserPool#mutable}.'''
        result = self._values.get("mutable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def number_attribute_constraints(
        self,
    ) -> typing.Optional["CognitoUserPoolSchemaNumberAttributeConstraints"]:
        '''number_attribute_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#number_attribute_constraints CognitoUserPool#number_attribute_constraints}
        '''
        result = self._values.get("number_attribute_constraints")
        return typing.cast(typing.Optional["CognitoUserPoolSchemaNumberAttributeConstraints"], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#required CognitoUserPool#required}.'''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def string_attribute_constraints(
        self,
    ) -> typing.Optional["CognitoUserPoolSchemaStringAttributeConstraints"]:
        '''string_attribute_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#string_attribute_constraints CognitoUserPool#string_attribute_constraints}
        '''
        result = self._values.get("string_attribute_constraints")
        return typing.cast(typing.Optional["CognitoUserPoolSchemaStringAttributeConstraints"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolSchemaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchemaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__387fd2f7fc34311692d8a14ab80de91ac05aab272483d373ddbfa2405179ad5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CognitoUserPoolSchemaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527ad0da4d40995ebd468ce634652c34c9e3601a19ae27a111575bffd5b4fc62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CognitoUserPoolSchemaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d0e5dc90340c6a31cd7aa1dfb8f1c07930e6bda4f3c56fb3e1862c90150a79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7ecac03578e224c1fe03f5de740ad09ede82717e68bf376106a57af7514fc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__293db56195c7a37c0e294d9202d3e5f703c173d294ba0f71f99b1e4ea08cc306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolSchema]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolSchema]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671f458042a4d89ed33082f30d965e482e5b38a7f8338c9e83f814385c91de11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchemaNumberAttributeConstraints",
    jsii_struct_bases=[],
    name_mapping={"max_value": "maxValue", "min_value": "minValue"},
)
class CognitoUserPoolSchemaNumberAttributeConstraints:
    def __init__(
        self,
        *,
        max_value: typing.Optional[builtins.str] = None,
        min_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#max_value CognitoUserPool#max_value}.
        :param min_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#min_value CognitoUserPool#min_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32d36d8328006032a1389001b857bd524f5874522fe4351684e390e2a523579)
            check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
            check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_value is not None:
            self._values["max_value"] = max_value
        if min_value is not None:
            self._values["min_value"] = min_value

    @builtins.property
    def max_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#max_value CognitoUserPool#max_value}.'''
        result = self._values.get("max_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#min_value CognitoUserPool#min_value}.'''
        result = self._values.get("min_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolSchemaNumberAttributeConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolSchemaNumberAttributeConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchemaNumberAttributeConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12125e68559fb65e41fbb4ce8e4f4df26bfbc3fd6fdb30611aab2c53a4365e38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxValue")
    def reset_max_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxValue", []))

    @jsii.member(jsii_name="resetMinValue")
    def reset_min_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinValue", []))

    @builtins.property
    @jsii.member(jsii_name="maxValueInput")
    def max_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxValueInput"))

    @builtins.property
    @jsii.member(jsii_name="minValueInput")
    def min_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minValueInput"))

    @builtins.property
    @jsii.member(jsii_name="maxValue")
    def max_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxValue"))

    @max_value.setter
    def max_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76fff08a2db82903038f8dc8664b69648ad8776dfb0f800279ffc7d37253d0c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minValue")
    def min_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minValue"))

    @min_value.setter
    def min_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de587eb8066379dc9035de8d360acefecc4d09a2d92449d7b50857b0c2bdcd2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolSchemaNumberAttributeConstraints]:
        return typing.cast(typing.Optional[CognitoUserPoolSchemaNumberAttributeConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolSchemaNumberAttributeConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c594b66e7a620d5e1b70078454418463cd92fe36fe3ca7f806b997dee8057662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoUserPoolSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8054f77b4efee5c18c00a042b22de36a02c2f0fb3a6465d9501b6f4168c966)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNumberAttributeConstraints")
    def put_number_attribute_constraints(
        self,
        *,
        max_value: typing.Optional[builtins.str] = None,
        min_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#max_value CognitoUserPool#max_value}.
        :param min_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#min_value CognitoUserPool#min_value}.
        '''
        value = CognitoUserPoolSchemaNumberAttributeConstraints(
            max_value=max_value, min_value=min_value
        )

        return typing.cast(None, jsii.invoke(self, "putNumberAttributeConstraints", [value]))

    @jsii.member(jsii_name="putStringAttributeConstraints")
    def put_string_attribute_constraints(
        self,
        *,
        max_length: typing.Optional[builtins.str] = None,
        min_length: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#max_length CognitoUserPool#max_length}.
        :param min_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#min_length CognitoUserPool#min_length}.
        '''
        value = CognitoUserPoolSchemaStringAttributeConstraints(
            max_length=max_length, min_length=min_length
        )

        return typing.cast(None, jsii.invoke(self, "putStringAttributeConstraints", [value]))

    @jsii.member(jsii_name="resetDeveloperOnlyAttribute")
    def reset_developer_only_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperOnlyAttribute", []))

    @jsii.member(jsii_name="resetMutable")
    def reset_mutable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMutable", []))

    @jsii.member(jsii_name="resetNumberAttributeConstraints")
    def reset_number_attribute_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberAttributeConstraints", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetStringAttributeConstraints")
    def reset_string_attribute_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringAttributeConstraints", []))

    @builtins.property
    @jsii.member(jsii_name="numberAttributeConstraints")
    def number_attribute_constraints(
        self,
    ) -> CognitoUserPoolSchemaNumberAttributeConstraintsOutputReference:
        return typing.cast(CognitoUserPoolSchemaNumberAttributeConstraintsOutputReference, jsii.get(self, "numberAttributeConstraints"))

    @builtins.property
    @jsii.member(jsii_name="stringAttributeConstraints")
    def string_attribute_constraints(
        self,
    ) -> "CognitoUserPoolSchemaStringAttributeConstraintsOutputReference":
        return typing.cast("CognitoUserPoolSchemaStringAttributeConstraintsOutputReference", jsii.get(self, "stringAttributeConstraints"))

    @builtins.property
    @jsii.member(jsii_name="attributeDataTypeInput")
    def attribute_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeDataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="developerOnlyAttributeInput")
    def developer_only_attribute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "developerOnlyAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="mutableInput")
    def mutable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mutableInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="numberAttributeConstraintsInput")
    def number_attribute_constraints_input(
        self,
    ) -> typing.Optional[CognitoUserPoolSchemaNumberAttributeConstraints]:
        return typing.cast(typing.Optional[CognitoUserPoolSchemaNumberAttributeConstraints], jsii.get(self, "numberAttributeConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="stringAttributeConstraintsInput")
    def string_attribute_constraints_input(
        self,
    ) -> typing.Optional["CognitoUserPoolSchemaStringAttributeConstraints"]:
        return typing.cast(typing.Optional["CognitoUserPoolSchemaStringAttributeConstraints"], jsii.get(self, "stringAttributeConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeDataType")
    def attribute_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeDataType"))

    @attribute_data_type.setter
    def attribute_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706e293a458d4165dd4e0921d9d8891c5cf81388c5fce1e3ebe445a285876b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerOnlyAttribute")
    def developer_only_attribute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "developerOnlyAttribute"))

    @developer_only_attribute.setter
    def developer_only_attribute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbbbf7ae7a2899f27503e6b1c39c431d0fe627e205749daffeeb0297b14962a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerOnlyAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mutable")
    def mutable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mutable"))

    @mutable.setter
    def mutable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f55912451a2736dd088bf2df62d83c57ae8f13781a73070e1b0fedcd0f23e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mutable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171a223f34df91cae8c6089a57465a79285b0cec93950693f34e0315e96d5302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698f166e52580250785905ef175f2b5493292000e241b1650fdd105aaa86804f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b0a304408f9fbfbb1e01fd2be9af465ee978e3480fc1f516681b8e60dcec64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchemaStringAttributeConstraints",
    jsii_struct_bases=[],
    name_mapping={"max_length": "maxLength", "min_length": "minLength"},
)
class CognitoUserPoolSchemaStringAttributeConstraints:
    def __init__(
        self,
        *,
        max_length: typing.Optional[builtins.str] = None,
        min_length: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#max_length CognitoUserPool#max_length}.
        :param min_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#min_length CognitoUserPool#min_length}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117f050d7ca69a59e43c48bd791fa85d73d9dc53bdabd1416f6f83e634c94025)
            check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_length is not None:
            self._values["max_length"] = max_length
        if min_length is not None:
            self._values["min_length"] = min_length

    @builtins.property
    def max_length(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#max_length CognitoUserPool#max_length}.'''
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_length(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#min_length CognitoUserPool#min_length}.'''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolSchemaStringAttributeConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolSchemaStringAttributeConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSchemaStringAttributeConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42424a4003480fbe3fe2cff014b8e6e0d83aeb2511079591bedc78394d89fc17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxLength")
    def reset_max_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLength", []))

    @jsii.member(jsii_name="resetMinLength")
    def reset_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLength", []))

    @builtins.property
    @jsii.member(jsii_name="maxLengthInput")
    def max_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="minLengthInput")
    def min_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLength")
    def max_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxLength"))

    @max_length.setter
    def max_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4196fc7be63861aefbe5ba8c4d9a521f38b7829389bf7a5f14c1b51da1e9be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5873a24f11a950b8e4230d14be5439861976c20fbc8bcdd688f1b8a43baaa3c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolSchemaStringAttributeConstraints]:
        return typing.cast(typing.Optional[CognitoUserPoolSchemaStringAttributeConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolSchemaStringAttributeConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb1125954b386fbbdbdb9263d29bff63edaeb6049324d66387c94053d18a9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSignInPolicy",
    jsii_struct_bases=[],
    name_mapping={"allowed_first_auth_factors": "allowedFirstAuthFactors"},
)
class CognitoUserPoolSignInPolicy:
    def __init__(
        self,
        *,
        allowed_first_auth_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_first_auth_factors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#allowed_first_auth_factors CognitoUserPool#allowed_first_auth_factors}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fb2425e2b9654fbe93c45b5583aa2c4b10c46411022cc4549e46def5b29e07)
            check_type(argname="argument allowed_first_auth_factors", value=allowed_first_auth_factors, expected_type=type_hints["allowed_first_auth_factors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_first_auth_factors is not None:
            self._values["allowed_first_auth_factors"] = allowed_first_auth_factors

    @builtins.property
    def allowed_first_auth_factors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#allowed_first_auth_factors CognitoUserPool#allowed_first_auth_factors}.'''
        result = self._values.get("allowed_first_auth_factors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolSignInPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolSignInPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSignInPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c1d371672b86715af9976665984e1d9dd5211a47d132e19307d6a1ba4c8d1a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedFirstAuthFactors")
    def reset_allowed_first_auth_factors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedFirstAuthFactors", []))

    @builtins.property
    @jsii.member(jsii_name="allowedFirstAuthFactorsInput")
    def allowed_first_auth_factors_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedFirstAuthFactorsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedFirstAuthFactors")
    def allowed_first_auth_factors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedFirstAuthFactors"))

    @allowed_first_auth_factors.setter
    def allowed_first_auth_factors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9f96df1d1b6742bf4445ad2529df07defe5273a908494fa33206943fb64f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedFirstAuthFactors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolSignInPolicy]:
        return typing.cast(typing.Optional[CognitoUserPoolSignInPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolSignInPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff73600fb3011151ddca40894077f54429d923187718feff5f0b84a5f79c101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSmsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "external_id": "externalId",
        "sns_caller_arn": "snsCallerArn",
        "sns_region": "snsRegion",
    },
)
class CognitoUserPoolSmsConfiguration:
    def __init__(
        self,
        *,
        external_id: builtins.str,
        sns_caller_arn: builtins.str,
        sns_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#external_id CognitoUserPool#external_id}.
        :param sns_caller_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sns_caller_arn CognitoUserPool#sns_caller_arn}.
        :param sns_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sns_region CognitoUserPool#sns_region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e97872fdfeac02cd4e90d1f54617e8205dcc1daca930ceb0697ce78267b1fa0)
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument sns_caller_arn", value=sns_caller_arn, expected_type=type_hints["sns_caller_arn"])
            check_type(argname="argument sns_region", value=sns_region, expected_type=type_hints["sns_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "external_id": external_id,
            "sns_caller_arn": sns_caller_arn,
        }
        if sns_region is not None:
            self._values["sns_region"] = sns_region

    @builtins.property
    def external_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#external_id CognitoUserPool#external_id}.'''
        result = self._values.get("external_id")
        assert result is not None, "Required property 'external_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sns_caller_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sns_caller_arn CognitoUserPool#sns_caller_arn}.'''
        result = self._values.get("sns_caller_arn")
        assert result is not None, "Required property 'sns_caller_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sns_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sns_region CognitoUserPool#sns_region}.'''
        result = self._values.get("sns_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolSmsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolSmsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSmsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b7d542912e2c7cb4f7f7d7c3735aa5b9117989c86419355e0fdab4e84ce8c32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSnsRegion")
    def reset_sns_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnsRegion", []))

    @builtins.property
    @jsii.member(jsii_name="externalIdInput")
    def external_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="snsCallerArnInput")
    def sns_caller_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snsCallerArnInput"))

    @builtins.property
    @jsii.member(jsii_name="snsRegionInput")
    def sns_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @external_id.setter
    def external_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a448bd4decce6d30cd8f525b5871856c7da8aa1b272a9fabd29b368c1adc5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snsCallerArn")
    def sns_caller_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snsCallerArn"))

    @sns_caller_arn.setter
    def sns_caller_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd68f29ebbd55e1576a25260cb749719b068ff130c62c6babd8e978ff899ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsCallerArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snsRegion")
    def sns_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snsRegion"))

    @sns_region.setter
    def sns_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167ff9987ea74b7e000c590f4e2fb168c640adf6a0acc66048292d17772d78dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolSmsConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolSmsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolSmsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25124069f57933a99dc6d489912d5756cee403bf0af50425a1ac20b7efabb0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSoftwareTokenMfaConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CognitoUserPoolSoftwareTokenMfaConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#enabled CognitoUserPool#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43673c87f798a2991fdf2edcd70b5aebe4177c52c9eb00b4bfaec77c4cb89778)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#enabled CognitoUserPool#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolSoftwareTokenMfaConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolSoftwareTokenMfaConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolSoftwareTokenMfaConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a21fd61c4c6989a0ea9b3ba85904068d168e6fb2854f064c6674417418c8713)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990e997d7c12e5190224415556218406f1bbea8f87f59f9fd2cacb5c2dd23f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolSoftwareTokenMfaConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolSoftwareTokenMfaConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolSoftwareTokenMfaConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32b09287fa5ce42f74ba7f83895f11bc7b63c1fe6911052cfd1fb4514b1f43a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUserAttributeUpdateSettings",
    jsii_struct_bases=[],
    name_mapping={
        "attributes_require_verification_before_update": "attributesRequireVerificationBeforeUpdate",
    },
)
class CognitoUserPoolUserAttributeUpdateSettings:
    def __init__(
        self,
        *,
        attributes_require_verification_before_update: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attributes_require_verification_before_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#attributes_require_verification_before_update CognitoUserPool#attributes_require_verification_before_update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61819ae735392d0b227b6e3024d33247546143116064ad397fd11aa9e968ead8)
            check_type(argname="argument attributes_require_verification_before_update", value=attributes_require_verification_before_update, expected_type=type_hints["attributes_require_verification_before_update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attributes_require_verification_before_update": attributes_require_verification_before_update,
        }

    @builtins.property
    def attributes_require_verification_before_update(
        self,
    ) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#attributes_require_verification_before_update CognitoUserPool#attributes_require_verification_before_update}.'''
        result = self._values.get("attributes_require_verification_before_update")
        assert result is not None, "Required property 'attributes_require_verification_before_update' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolUserAttributeUpdateSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolUserAttributeUpdateSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUserAttributeUpdateSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57fcab2e5c6be0fa0de9285e8d27fb194670aa4d74a442a48298873245a70405)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="attributesRequireVerificationBeforeUpdateInput")
    def attributes_require_verification_before_update_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "attributesRequireVerificationBeforeUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesRequireVerificationBeforeUpdate")
    def attributes_require_verification_before_update(
        self,
    ) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attributesRequireVerificationBeforeUpdate"))

    @attributes_require_verification_before_update.setter
    def attributes_require_verification_before_update(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0cee101edea7fff6063548c05ebaecbbdc32c95ce01168c719bc3af91dbafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesRequireVerificationBeforeUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolUserAttributeUpdateSettings]:
        return typing.cast(typing.Optional[CognitoUserPoolUserAttributeUpdateSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolUserAttributeUpdateSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28363d71e9312a26505f23addd5b5e93f919923f167dcbe6185d558228ce1e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUserPoolAddOns",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_security_mode": "advancedSecurityMode",
        "advanced_security_additional_flows": "advancedSecurityAdditionalFlows",
    },
)
class CognitoUserPoolUserPoolAddOns:
    def __init__(
        self,
        *,
        advanced_security_mode: builtins.str,
        advanced_security_additional_flows: typing.Optional[typing.Union["CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_security_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#advanced_security_mode CognitoUserPool#advanced_security_mode}.
        :param advanced_security_additional_flows: advanced_security_additional_flows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#advanced_security_additional_flows CognitoUserPool#advanced_security_additional_flows}
        '''
        if isinstance(advanced_security_additional_flows, dict):
            advanced_security_additional_flows = CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows(**advanced_security_additional_flows)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21bd072d96fc217f6d469063a020cceed2be834bdf83ed99e5e701f61f56bdb)
            check_type(argname="argument advanced_security_mode", value=advanced_security_mode, expected_type=type_hints["advanced_security_mode"])
            check_type(argname="argument advanced_security_additional_flows", value=advanced_security_additional_flows, expected_type=type_hints["advanced_security_additional_flows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "advanced_security_mode": advanced_security_mode,
        }
        if advanced_security_additional_flows is not None:
            self._values["advanced_security_additional_flows"] = advanced_security_additional_flows

    @builtins.property
    def advanced_security_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#advanced_security_mode CognitoUserPool#advanced_security_mode}.'''
        result = self._values.get("advanced_security_mode")
        assert result is not None, "Required property 'advanced_security_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_security_additional_flows(
        self,
    ) -> typing.Optional["CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows"]:
        '''advanced_security_additional_flows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#advanced_security_additional_flows CognitoUserPool#advanced_security_additional_flows}
        '''
        result = self._values.get("advanced_security_additional_flows")
        return typing.cast(typing.Optional["CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolUserPoolAddOns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows",
    jsii_struct_bases=[],
    name_mapping={"custom_auth_mode": "customAuthMode"},
)
class CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows:
    def __init__(
        self,
        *,
        custom_auth_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_auth_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_auth_mode CognitoUserPool#custom_auth_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd031c6b82e9df0f6602df01623115ad39488f48219e1b7f67f3727ecb18c49)
            check_type(argname="argument custom_auth_mode", value=custom_auth_mode, expected_type=type_hints["custom_auth_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_auth_mode is not None:
            self._values["custom_auth_mode"] = custom_auth_mode

    @builtins.property
    def custom_auth_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_auth_mode CognitoUserPool#custom_auth_mode}.'''
        result = self._values.get("custom_auth_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fa21669158caed5158ab2cf33c36d4c47230b23a1ad20a6388e5470b69bc8a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomAuthMode")
    def reset_custom_auth_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAuthMode", []))

    @builtins.property
    @jsii.member(jsii_name="customAuthModeInput")
    def custom_auth_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customAuthModeInput"))

    @builtins.property
    @jsii.member(jsii_name="customAuthMode")
    def custom_auth_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customAuthMode"))

    @custom_auth_mode.setter
    def custom_auth_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a74876ff268aaaf977bb0ae1badbcb6a10b9187ef13da26ec7bffa759ae0792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAuthMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows]:
        return typing.cast(typing.Optional[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b6adfc20a96471e5142e1993436067b742d8ffacab11a984e3f3a8368b17f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CognitoUserPoolUserPoolAddOnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUserPoolAddOnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34408c7075e950ef7d87e304676cf7288f0c3050f3cc956e5f6254642152011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedSecurityAdditionalFlows")
    def put_advanced_security_additional_flows(
        self,
        *,
        custom_auth_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_auth_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#custom_auth_mode CognitoUserPool#custom_auth_mode}.
        '''
        value = CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows(
            custom_auth_mode=custom_auth_mode
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSecurityAdditionalFlows", [value]))

    @jsii.member(jsii_name="resetAdvancedSecurityAdditionalFlows")
    def reset_advanced_security_additional_flows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSecurityAdditionalFlows", []))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityAdditionalFlows")
    def advanced_security_additional_flows(
        self,
    ) -> CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlowsOutputReference:
        return typing.cast(CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlowsOutputReference, jsii.get(self, "advancedSecurityAdditionalFlows"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityAdditionalFlowsInput")
    def advanced_security_additional_flows_input(
        self,
    ) -> typing.Optional[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows]:
        return typing.cast(typing.Optional[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows], jsii.get(self, "advancedSecurityAdditionalFlowsInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityModeInput")
    def advanced_security_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "advancedSecurityModeInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityMode")
    def advanced_security_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "advancedSecurityMode"))

    @advanced_security_mode.setter
    def advanced_security_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df295b085415f4f294948433cf6de6f3a43f013ff286f40e5879790faec27382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedSecurityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolUserPoolAddOns]:
        return typing.cast(typing.Optional[CognitoUserPoolUserPoolAddOns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolUserPoolAddOns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16ddf37ee439df947f71ce552ed3ab236312e5ace78e8198870e6cb042d6396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUsernameConfiguration",
    jsii_struct_bases=[],
    name_mapping={"case_sensitive": "caseSensitive"},
)
class CognitoUserPoolUsernameConfiguration:
    def __init__(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param case_sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#case_sensitive CognitoUserPool#case_sensitive}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee23b3be485c6835535b556af2d764afb5c148efd7a562156e0d192b77a08b7)
            check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if case_sensitive is not None:
            self._values["case_sensitive"] = case_sensitive

    @builtins.property
    def case_sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#case_sensitive CognitoUserPool#case_sensitive}.'''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolUsernameConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolUsernameConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolUsernameConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a934ccdaba3c5d2769945468a87e29d4cb928c1eeb9f18e3cca87175abc263)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaseSensitive")
    def reset_case_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseSensitive", []))

    @builtins.property
    @jsii.member(jsii_name="caseSensitiveInput")
    def case_sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseSensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="caseSensitive")
    def case_sensitive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseSensitive"))

    @case_sensitive.setter
    def case_sensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0143e98d0b763d8ca1b7717b8e7bfaeb95ff04c32447e3dc49c13504850b6ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseSensitive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolUsernameConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolUsernameConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolUsernameConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4dc108f5e8c5a979208fec47fee0e57914b419b5f5f4e6669b123da4d3db51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolVerificationMessageTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "default_email_option": "defaultEmailOption",
        "email_message": "emailMessage",
        "email_message_by_link": "emailMessageByLink",
        "email_subject": "emailSubject",
        "email_subject_by_link": "emailSubjectByLink",
        "sms_message": "smsMessage",
    },
)
class CognitoUserPoolVerificationMessageTemplate:
    def __init__(
        self,
        *,
        default_email_option: typing.Optional[builtins.str] = None,
        email_message: typing.Optional[builtins.str] = None,
        email_message_by_link: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
        email_subject_by_link: typing.Optional[builtins.str] = None,
        sms_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_email_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#default_email_option CognitoUserPool#default_email_option}.
        :param email_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message CognitoUserPool#email_message}.
        :param email_message_by_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message_by_link CognitoUserPool#email_message_by_link}.
        :param email_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject CognitoUserPool#email_subject}.
        :param email_subject_by_link: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject_by_link CognitoUserPool#email_subject_by_link}.
        :param sms_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_message CognitoUserPool#sms_message}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e763b067160fac805fe8caa4b03877f1c9891b4d2448172c0529375c90386131)
            check_type(argname="argument default_email_option", value=default_email_option, expected_type=type_hints["default_email_option"])
            check_type(argname="argument email_message", value=email_message, expected_type=type_hints["email_message"])
            check_type(argname="argument email_message_by_link", value=email_message_by_link, expected_type=type_hints["email_message_by_link"])
            check_type(argname="argument email_subject", value=email_subject, expected_type=type_hints["email_subject"])
            check_type(argname="argument email_subject_by_link", value=email_subject_by_link, expected_type=type_hints["email_subject_by_link"])
            check_type(argname="argument sms_message", value=sms_message, expected_type=type_hints["sms_message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_email_option is not None:
            self._values["default_email_option"] = default_email_option
        if email_message is not None:
            self._values["email_message"] = email_message
        if email_message_by_link is not None:
            self._values["email_message_by_link"] = email_message_by_link
        if email_subject is not None:
            self._values["email_subject"] = email_subject
        if email_subject_by_link is not None:
            self._values["email_subject_by_link"] = email_subject_by_link
        if sms_message is not None:
            self._values["sms_message"] = sms_message

    @builtins.property
    def default_email_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#default_email_option CognitoUserPool#default_email_option}.'''
        result = self._values.get("default_email_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message CognitoUserPool#email_message}.'''
        result = self._values.get("email_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_message_by_link(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_message_by_link CognitoUserPool#email_message_by_link}.'''
        result = self._values.get("email_message_by_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject CognitoUserPool#email_subject}.'''
        result = self._values.get("email_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_subject_by_link(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#email_subject_by_link CognitoUserPool#email_subject_by_link}.'''
        result = self._values.get("email_subject_by_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sms_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#sms_message CognitoUserPool#sms_message}.'''
        result = self._values.get("sms_message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolVerificationMessageTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolVerificationMessageTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolVerificationMessageTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__685f25441304ccbe1c88a059cb875bd458f146b262870092b2da3eb03ea745a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultEmailOption")
    def reset_default_email_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultEmailOption", []))

    @jsii.member(jsii_name="resetEmailMessage")
    def reset_email_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailMessage", []))

    @jsii.member(jsii_name="resetEmailMessageByLink")
    def reset_email_message_by_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailMessageByLink", []))

    @jsii.member(jsii_name="resetEmailSubject")
    def reset_email_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailSubject", []))

    @jsii.member(jsii_name="resetEmailSubjectByLink")
    def reset_email_subject_by_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailSubjectByLink", []))

    @jsii.member(jsii_name="resetSmsMessage")
    def reset_sms_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsMessage", []))

    @builtins.property
    @jsii.member(jsii_name="defaultEmailOptionInput")
    def default_email_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultEmailOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailMessageByLinkInput")
    def email_message_by_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailMessageByLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="emailMessageInput")
    def email_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="emailSubjectByLinkInput")
    def email_subject_by_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailSubjectByLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="emailSubjectInput")
    def email_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="smsMessageInput")
    def sms_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smsMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultEmailOption")
    def default_email_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultEmailOption"))

    @default_email_option.setter
    def default_email_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd88ddbbde9e9bb8aea9a9ee5f7c84eaf5165d39e85d58e4cf1f5215c6340c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultEmailOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailMessage")
    def email_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailMessage"))

    @email_message.setter
    def email_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661b5a4df3e54a6092393aded5e980512bb1c4f7d082d535900da5b7a896d537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailMessageByLink")
    def email_message_by_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailMessageByLink"))

    @email_message_by_link.setter
    def email_message_by_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3da72730070e9ad780d438e8f258a14f5e760eab82acb841ba4b6eb61b115d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailMessageByLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailSubject")
    def email_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailSubject"))

    @email_subject.setter
    def email_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b611ee45ddfe70529c0b8f8d99ace1c1e142460303141d073215bab53ad3a88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailSubjectByLink")
    def email_subject_by_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailSubjectByLink"))

    @email_subject_by_link.setter
    def email_subject_by_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9dd61b84129efc3c70d2bc67079e623616cf0668e99242803ab6f95f8a1ae7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailSubjectByLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smsMessage")
    def sms_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smsMessage"))

    @sms_message.setter
    def sms_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3f859a6ca224692bc1e5346f851fe0f3d18decb88ebd864174480abe0a7901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smsMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CognitoUserPoolVerificationMessageTemplate]:
        return typing.cast(typing.Optional[CognitoUserPoolVerificationMessageTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolVerificationMessageTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e02aef994b2b2b24ca6dded16d43c02ae0eb95d110948278b3318d6c28565d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolWebAuthnConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "relying_party_id": "relyingPartyId",
        "user_verification": "userVerification",
    },
)
class CognitoUserPoolWebAuthnConfiguration:
    def __init__(
        self,
        *,
        relying_party_id: typing.Optional[builtins.str] = None,
        user_verification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relying_party_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#relying_party_id CognitoUserPool#relying_party_id}.
        :param user_verification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_verification CognitoUserPool#user_verification}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c012667b4eebb56bff595bad7453f8417900b7286dd9f9b43d1a981c709ff6fa)
            check_type(argname="argument relying_party_id", value=relying_party_id, expected_type=type_hints["relying_party_id"])
            check_type(argname="argument user_verification", value=user_verification, expected_type=type_hints["user_verification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if relying_party_id is not None:
            self._values["relying_party_id"] = relying_party_id
        if user_verification is not None:
            self._values["user_verification"] = user_verification

    @builtins.property
    def relying_party_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#relying_party_id CognitoUserPool#relying_party_id}.'''
        result = self._values.get("relying_party_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_verification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cognito_user_pool#user_verification CognitoUserPool#user_verification}.'''
        result = self._values.get("user_verification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoUserPoolWebAuthnConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitoUserPoolWebAuthnConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cognitoUserPool.CognitoUserPoolWebAuthnConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce049caa349cc4c01efc3ad059282c7443c8b3c4d8e6048d7008cdaf03c0fee6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRelyingPartyId")
    def reset_relying_party_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelyingPartyId", []))

    @jsii.member(jsii_name="resetUserVerification")
    def reset_user_verification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserVerification", []))

    @builtins.property
    @jsii.member(jsii_name="relyingPartyIdInput")
    def relying_party_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relyingPartyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userVerificationInput")
    def user_verification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userVerificationInput"))

    @builtins.property
    @jsii.member(jsii_name="relyingPartyId")
    def relying_party_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relyingPartyId"))

    @relying_party_id.setter
    def relying_party_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba3914e81517cb06c27f7499fa4c3854eba33f542642a8af7bf9920595facc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relyingPartyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userVerification")
    def user_verification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userVerification"))

    @user_verification.setter
    def user_verification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15783652361a95fe468e7cc44bcd369c64ddcc5146ac8804c61cd5ae99d05b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userVerification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitoUserPoolWebAuthnConfiguration]:
        return typing.cast(typing.Optional[CognitoUserPoolWebAuthnConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CognitoUserPoolWebAuthnConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ee7f5c04005688c7c3dc216abc61b1907a15918448e18d311fa9e85c228d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CognitoUserPool",
    "CognitoUserPoolAccountRecoverySetting",
    "CognitoUserPoolAccountRecoverySettingOutputReference",
    "CognitoUserPoolAccountRecoverySettingRecoveryMechanism",
    "CognitoUserPoolAccountRecoverySettingRecoveryMechanismList",
    "CognitoUserPoolAccountRecoverySettingRecoveryMechanismOutputReference",
    "CognitoUserPoolAdminCreateUserConfig",
    "CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate",
    "CognitoUserPoolAdminCreateUserConfigInviteMessageTemplateOutputReference",
    "CognitoUserPoolAdminCreateUserConfigOutputReference",
    "CognitoUserPoolConfig",
    "CognitoUserPoolDeviceConfiguration",
    "CognitoUserPoolDeviceConfigurationOutputReference",
    "CognitoUserPoolEmailConfiguration",
    "CognitoUserPoolEmailConfigurationOutputReference",
    "CognitoUserPoolEmailMfaConfiguration",
    "CognitoUserPoolEmailMfaConfigurationOutputReference",
    "CognitoUserPoolLambdaConfig",
    "CognitoUserPoolLambdaConfigCustomEmailSender",
    "CognitoUserPoolLambdaConfigCustomEmailSenderOutputReference",
    "CognitoUserPoolLambdaConfigCustomSmsSender",
    "CognitoUserPoolLambdaConfigCustomSmsSenderOutputReference",
    "CognitoUserPoolLambdaConfigOutputReference",
    "CognitoUserPoolLambdaConfigPreTokenGenerationConfig",
    "CognitoUserPoolLambdaConfigPreTokenGenerationConfigOutputReference",
    "CognitoUserPoolPasswordPolicy",
    "CognitoUserPoolPasswordPolicyOutputReference",
    "CognitoUserPoolSchema",
    "CognitoUserPoolSchemaList",
    "CognitoUserPoolSchemaNumberAttributeConstraints",
    "CognitoUserPoolSchemaNumberAttributeConstraintsOutputReference",
    "CognitoUserPoolSchemaOutputReference",
    "CognitoUserPoolSchemaStringAttributeConstraints",
    "CognitoUserPoolSchemaStringAttributeConstraintsOutputReference",
    "CognitoUserPoolSignInPolicy",
    "CognitoUserPoolSignInPolicyOutputReference",
    "CognitoUserPoolSmsConfiguration",
    "CognitoUserPoolSmsConfigurationOutputReference",
    "CognitoUserPoolSoftwareTokenMfaConfiguration",
    "CognitoUserPoolSoftwareTokenMfaConfigurationOutputReference",
    "CognitoUserPoolUserAttributeUpdateSettings",
    "CognitoUserPoolUserAttributeUpdateSettingsOutputReference",
    "CognitoUserPoolUserPoolAddOns",
    "CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows",
    "CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlowsOutputReference",
    "CognitoUserPoolUserPoolAddOnsOutputReference",
    "CognitoUserPoolUsernameConfiguration",
    "CognitoUserPoolUsernameConfigurationOutputReference",
    "CognitoUserPoolVerificationMessageTemplate",
    "CognitoUserPoolVerificationMessageTemplateOutputReference",
    "CognitoUserPoolWebAuthnConfiguration",
    "CognitoUserPoolWebAuthnConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__8872d50f4ab62e16f985b6573881f5ac556a0b0e5ae00333187a9276ac1eb0d4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    account_recovery_setting: typing.Optional[typing.Union[CognitoUserPoolAccountRecoverySetting, typing.Dict[builtins.str, typing.Any]]] = None,
    admin_create_user_config: typing.Optional[typing.Union[CognitoUserPoolAdminCreateUserConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    alias_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_verified_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[builtins.str] = None,
    device_configuration: typing.Optional[typing.Union[CognitoUserPoolDeviceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    email_configuration: typing.Optional[typing.Union[CognitoUserPoolEmailConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    email_mfa_configuration: typing.Optional[typing.Union[CognitoUserPoolEmailMfaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    email_verification_message: typing.Optional[builtins.str] = None,
    email_verification_subject: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lambda_config: typing.Optional[typing.Union[CognitoUserPoolLambdaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mfa_configuration: typing.Optional[builtins.str] = None,
    password_policy: typing.Optional[typing.Union[CognitoUserPoolPasswordPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CognitoUserPoolSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sign_in_policy: typing.Optional[typing.Union[CognitoUserPoolSignInPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sms_authentication_message: typing.Optional[builtins.str] = None,
    sms_configuration: typing.Optional[typing.Union[CognitoUserPoolSmsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sms_verification_message: typing.Optional[builtins.str] = None,
    software_token_mfa_configuration: typing.Optional[typing.Union[CognitoUserPoolSoftwareTokenMfaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_attribute_update_settings: typing.Optional[typing.Union[CognitoUserPoolUserAttributeUpdateSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    username_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    username_configuration: typing.Optional[typing.Union[CognitoUserPoolUsernameConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_add_ons: typing.Optional[typing.Union[CognitoUserPoolUserPoolAddOns, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_tier: typing.Optional[builtins.str] = None,
    verification_message_template: typing.Optional[typing.Union[CognitoUserPoolVerificationMessageTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    web_authn_configuration: typing.Optional[typing.Union[CognitoUserPoolWebAuthnConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1401e9d804e77e6f117726fe6753f19e9e59c35fb80630d8ac4d054f0c20f485(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05766da8b9a1b2faefe9f4a6078fde5bf415303580305edb32539b965be61460(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CognitoUserPoolSchema, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35eda83e750e892aed12a4a60a8a6054443ff4c17dc4c7525be5473208eda4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6e50f4430aa2db407907a8038d5099045323251eeb3daa905c0066e54bf4f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db6753e5585a8149b0d00e3b4f78120a272159bb7aa4a741a24b97b445cce05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c0fe43457a68e7d56aa0c87ba0cbb95f68f3a7cdb15222df1ef4c69cb28c56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2194bb2c68fa7fcc89d76d003fefe1889e78bedd41c3059f121d0428b218d11c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46963528b276aab05cd6c46191aa8868cddd2b86f4e565b1c6a6c7a5bdfb6c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36d57b85a35c2470155897f4506c5721f7fa4f623ae86c82935d32b401bdfdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1410a7051cbb3b4a3d62f5b82b76576d07f86eb296dbbc3e78db8b4318012e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3df8d82df8f6fc041af8976ac0de53ffe371383db79fe28315a49965e547f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95889b943c68eb1da10ad13ee44acd16f0b333ed89306c45456b3f6f5bf19128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06927ad91bad9f4bce31833eb353c6064b0394c61ae01f691943b2aa67ec55c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88402dd2924097c4c41582f73b468d8a30a1b3da75142038c6e6144173cf4e50(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f3826b5b5e68e6487364afb1b7665bb76c23e97404e75a6433158f9d557163(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9377aba987382ab50a6cb2e4443c307e3459bd81a14fcdc1d21cb12d8313ac17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511f73aae65892fc0bb42482da5028f2a7955d6ee61efdd04ab4ef6a42d67730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdce3ed1b0953e1f407f7b8c3bff7b911cf91156683b5edc1342b78a0c91e0ed(
    *,
    recovery_mechanism: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CognitoUserPoolAccountRecoverySettingRecoveryMechanism, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5008d0ce83af1839c1fcb983dabdd9ff5d14b62cba1b1d5a1ef30959d17b40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afea38f94d9021003e1ecb231e88d57d8c58829e2ecf2d1bab3bcd24696565c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CognitoUserPoolAccountRecoverySettingRecoveryMechanism, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63deb84336cd99c87e17a845255c8cea7d5b68bd4e8e646d51614d59a9c00fd7(
    value: typing.Optional[CognitoUserPoolAccountRecoverySetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8928ec841be3ef008727f3ae2ce29aab59d57da11097a50ca58ad43f223d19ab(
    *,
    name: builtins.str,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d539329a1bd3fe7595b4c8b0931a34ebc5969387a889d3e22bee52e62ab37293(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050acd11e1e1b2b816647bbfaef0e816b3eda268ef6ae53dd7797e29db19478d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fe69656931b54a74bc6cca047f9259b5ed20a93670aff806eb2ba03f79a9f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11be7c57011b09627210f78688da5eb319a92b8db9ae74324ce7c0f2ae3bbd9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c6821a76cdeeecb0cf3a7ca68041f207ccaccd5a6134de858ad932412e11e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4dcc37d49d0cb410e7047744ccb61aeae76db82386c44dbc65364c62b9301b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolAccountRecoverySettingRecoveryMechanism]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5288c016cbdc22757ad8a87cf598c425ba41654d4ec31aa40b6ca66f067814(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa506396680e39fae1a1d5db0e168ef4652084d02bb73ba69fa680b1bfc1e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3261d811c880effff9480cd53fd504b79ef41331d191793e941b6de9908d44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c238679ed69ce3c4bdad99cb9e4f3f812e780186611fd0cef5ccad2e5c7e480(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolAccountRecoverySettingRecoveryMechanism]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea17fcaa62d2b73fe80a62a087697b614e3d8dc22a0823e9424f7222fe87541d(
    *,
    allow_admin_create_user_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    invite_message_template: typing.Optional[typing.Union[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1df1cc8c4d026285fe9b0dad3a281ac06e8d250dc2be8e1048a2da7ba16a03(
    *,
    email_message: typing.Optional[builtins.str] = None,
    email_subject: typing.Optional[builtins.str] = None,
    sms_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3571efe6343d500b04f0c9630eea52ae24722cb7e05d6f0b088f32822ef240(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62ab26e3b76a0a2a7aa05a7e363216736fab1c7974456c0ffec8184433d982a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e237bf52d8655b9ad88fce0ef8b8e6ddb6bddf2b78160cce2766cc29d428f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711b9e8dbbb2b39713c79aedab488b81fd8988af979730a9d15fd07f93bf46a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e8b08dbe32597c57c67595e46287ed1db61cf05690dd9dfd69a3114baae217(
    value: typing.Optional[CognitoUserPoolAdminCreateUserConfigInviteMessageTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2390d13f3edbd3452cc7fcb4461664c190a36833c2e887a1d20affe39f9200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa56595440716b9016521ed96f1e3283635303bd047d71cff93ebfa346dac06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be63cf7143187151c094fca4cefa042c466f8b0aa23311f32941ecac1cbd0ff(
    value: typing.Optional[CognitoUserPoolAdminCreateUserConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a868aa72412a31fbec88aa66ae13517046726a0401d5b2c61a9daa22c941797c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    account_recovery_setting: typing.Optional[typing.Union[CognitoUserPoolAccountRecoverySetting, typing.Dict[builtins.str, typing.Any]]] = None,
    admin_create_user_config: typing.Optional[typing.Union[CognitoUserPoolAdminCreateUserConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    alias_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_verified_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[builtins.str] = None,
    device_configuration: typing.Optional[typing.Union[CognitoUserPoolDeviceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    email_configuration: typing.Optional[typing.Union[CognitoUserPoolEmailConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    email_mfa_configuration: typing.Optional[typing.Union[CognitoUserPoolEmailMfaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    email_verification_message: typing.Optional[builtins.str] = None,
    email_verification_subject: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lambda_config: typing.Optional[typing.Union[CognitoUserPoolLambdaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mfa_configuration: typing.Optional[builtins.str] = None,
    password_policy: typing.Optional[typing.Union[CognitoUserPoolPasswordPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CognitoUserPoolSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sign_in_policy: typing.Optional[typing.Union[CognitoUserPoolSignInPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sms_authentication_message: typing.Optional[builtins.str] = None,
    sms_configuration: typing.Optional[typing.Union[CognitoUserPoolSmsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sms_verification_message: typing.Optional[builtins.str] = None,
    software_token_mfa_configuration: typing.Optional[typing.Union[CognitoUserPoolSoftwareTokenMfaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_attribute_update_settings: typing.Optional[typing.Union[CognitoUserPoolUserAttributeUpdateSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    username_attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    username_configuration: typing.Optional[typing.Union[CognitoUserPoolUsernameConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_add_ons: typing.Optional[typing.Union[CognitoUserPoolUserPoolAddOns, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_tier: typing.Optional[builtins.str] = None,
    verification_message_template: typing.Optional[typing.Union[CognitoUserPoolVerificationMessageTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    web_authn_configuration: typing.Optional[typing.Union[CognitoUserPoolWebAuthnConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038225e22036b1b3e2653fbc0f1e10a2d66604953c8f50c95052f554a0b456ba(
    *,
    challenge_required_on_new_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_only_remembered_on_user_prompt: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08fe8f92d2259e9a3224bcc8c65dcba60431cad6063ea6083fe56f53d9d987b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7875426dd1d30b7b4697fd10593778624e25fb03328f14bee13c1aa4af1245c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db70f8e76153ce365f56f3ad1ea9f90d60dbb2b26ff018d66f5fabfd0b10da8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6828cacb3d671be9b565bfa11715b12afc6a14ee62f3f3fd89c72b15ce9d7e86(
    value: typing.Optional[CognitoUserPoolDeviceConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e46f6ef87a1a4d79ac90e481a9af37fd093e1c663cfa7f440d669739e4618d0(
    *,
    configuration_set: typing.Optional[builtins.str] = None,
    email_sending_account: typing.Optional[builtins.str] = None,
    from_email_address: typing.Optional[builtins.str] = None,
    reply_to_email_address: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b517a3d8ec077750c7aaf16db66d445177c3ef99008ab52e71fabe10d09230ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd9a8a19e904d77fed7306968b37ee053803bf2d008bf13ae446e3645a5e3f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31b7f3d521474bc28bec01bb669d0a6ea307ede0edf18c6cf79d09de2f77316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3729b49d3795aa2acb80589c036e007083cfffbf177a66a0d0d9fcac22ba05a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e7bf55fa18b4a5a8faf64090d3989ab25add6ede84a8608df6ddbb83616947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290d94ea9eb2ada2fcf7cd15ff4061fc1cc76da26710955e88e89358264933c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2ec708c45c1f1e4dec62b6d5a959799785101fc9bd28e09df3ead8ba7e75d7(
    value: typing.Optional[CognitoUserPoolEmailConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b23416bbce4591c8bbf56547aa67f2aa695a2ba91267ff0301646522a8c223(
    *,
    message: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc61590ff37fd760de7adb4c7a60099d50ab14e3c53822e4bf9e582fe52f691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4d7aa280824df4107c3e69fb4b27a0a1e93075534cb3cb3be6eb34eb53fc10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0990cfa6050bdab8542f30ca1ff4e18b1fc6c616bb27ae1ab65a2d59b2ea28af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6790a45977fc7d62e34b88019e0b8161d1b700b4c461b8e324c9834052b20d(
    value: typing.Optional[CognitoUserPoolEmailMfaConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668acb7eb5e07f5b965d50a16ee29f7e922060ca574534a61d63780b2e08343d(
    *,
    create_auth_challenge: typing.Optional[builtins.str] = None,
    custom_email_sender: typing.Optional[typing.Union[CognitoUserPoolLambdaConfigCustomEmailSender, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_message: typing.Optional[builtins.str] = None,
    custom_sms_sender: typing.Optional[typing.Union[CognitoUserPoolLambdaConfigCustomSmsSender, typing.Dict[builtins.str, typing.Any]]] = None,
    define_auth_challenge: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    post_authentication: typing.Optional[builtins.str] = None,
    post_confirmation: typing.Optional[builtins.str] = None,
    pre_authentication: typing.Optional[builtins.str] = None,
    pre_sign_up: typing.Optional[builtins.str] = None,
    pre_token_generation: typing.Optional[builtins.str] = None,
    pre_token_generation_config: typing.Optional[typing.Union[CognitoUserPoolLambdaConfigPreTokenGenerationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_migration: typing.Optional[builtins.str] = None,
    verify_auth_challenge_response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ff3f4731fd10b0753a24c785e16c45db565e2c2ddfa564b873623de4277a32(
    *,
    lambda_arn: builtins.str,
    lambda_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8444a0cfcbcb9aeab68508356c8312a525985a21cc88e94b64b0f821da769ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bc85444a8c645ddc6ff4027f8532be2ec9433781dd954294a6d4fb471ef21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04819a67abe91a7988a216b0402958f05ff983f70f16da72890fef42995ad44b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9f6c105a8a1d8f725f2218e91fc30df3e141fe50a4b5729697e8a1e6b17dbd(
    value: typing.Optional[CognitoUserPoolLambdaConfigCustomEmailSender],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d83acf85af820d2231daebe78f7f77d3d362c6f830648a482c5d9280f360042(
    *,
    lambda_arn: builtins.str,
    lambda_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81adec252b7a5b3a9e40b34b940e5f0264c7630667832f5398a8e48774c5a21a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd9002c835aa805436fcbfbe570fc50f33c4c591ec4f042417feb225d6e7228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0907623f3dba649d70afe96632201b79642bf5398817e92fc553c90da9afe90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde587a29bfd8341dc5cf0c4e8658b7fb3701a2f56122f27ee1927a5d8137a82(
    value: typing.Optional[CognitoUserPoolLambdaConfigCustomSmsSender],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f737d212b2d5001fd75cc6fa7e3cd81ac6630c2f262d3d1ee5dc130ea26b21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedab9c41db5f7cd63eec3d26bfb33163224b63ff93799ccf049404400e8fffd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5495cf8535a7cd7a444974c3628232f53974026161e3b1205e60b40b62746ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288ecc3e848c1493f63632dec3e6d54bad3fe452f5cc767ec0cadd9c226a43a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfc396c8b46ba5f4dc8bf8e8dbf687099b54f06a2caecef6a947b2fba065166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb0e8913a029e8916a51026459a703958ddb72bb0fc05c560a350bf505e08e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfcfadc3a87ecf317ea17c1392845a68a019b91ef1e0074a0dc8ed9a60f4c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77186cccf33eef4558802168f25a9ec3d498026b249efd7e7018d66581f0551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a2d2ee74660017949e2d21172fa7629071c0c3eb98cd8bac90fff7bf7f906c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68dcf081de741a8d6798ccf79cd6e18ff49043d771a9eb71173f1af0db4d63e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd7e7070f4e163d5e7e0ce9827f49c3a5f3382b32a33735273faa004fc9872e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a3c54f03c77fb1671d68766a4e1aa0f0a013068d9d591b74e6330bbfbc77ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd53d4fa3adf45f8a3b251156a8e3d93dfa7212506604cef3bdf919479ed7f44(
    value: typing.Optional[CognitoUserPoolLambdaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcfff89af6b040567caf36a7bb46a51baa33e0393f91a89909debf7e915d23c(
    *,
    lambda_arn: builtins.str,
    lambda_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1acd990c3595be9bb14927a439e0c2ea5f281568307741cb824043757bdeaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519979e234a5869bbf1dfda58fe2e33f0fdc72386761352b8fddfa0ec7b1a4c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7eb803910af59879354209ced3a66e71981c2f57563f74c9a86d9257eb8e9cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cc67024120d581f457a94e5a49588ae5045082d537ef0772482f856830b954(
    value: typing.Optional[CognitoUserPoolLambdaConfigPreTokenGenerationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5474c2606df3645d4b1f4b09577b47ed8ccf69eeb31096fd25c8f00ab2c5e9(
    *,
    minimum_length: typing.Optional[jsii.Number] = None,
    password_history_size: typing.Optional[jsii.Number] = None,
    require_lowercase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_numbers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_symbols: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_uppercase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    temporary_password_validity_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4ed2cddca5201211903fbafa0c8b80dd0ad18f33387a7e0435ccc2aeea39bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8aa5c4c62dc389d09bc30b4e472ef95ef69aac9658076b3dcb4bc927ec3cda2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b402d03080f4778e32cf7f79f0263815c0b046cd6b44fbec18da45737161489(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5a83bf9b84b148f9b7cae7b5be6ea94059c409c8f2efa1eea69d552229321a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496cebbff9fee0ebeefe3cdebb5c7fe3130271e0f8598f4d6155eb1abf780b3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e75aa600685737d48cb18f61fe7068cf58db34fe1bce8a38447cf2ae17dbf35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332752b9620a9a919ea6056392e826ca5e35c2c95fc06b7a477432a39dc4319a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc959d6c9b7177cf57590c9ca7e16d1942ff5215fd96007f89831980c2e841c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0031baa28841a3c22babeed3c88c2099043106f8de4ca0d64fc9419d1ce482(
    value: typing.Optional[CognitoUserPoolPasswordPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9753d2c4b4d6e595c79a8db36a1870432ba418548868e6393c71a8f8c23c7c46(
    *,
    attribute_data_type: builtins.str,
    name: builtins.str,
    developer_only_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    number_attribute_constraints: typing.Optional[typing.Union[CognitoUserPoolSchemaNumberAttributeConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    string_attribute_constraints: typing.Optional[typing.Union[CognitoUserPoolSchemaStringAttributeConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387fd2f7fc34311692d8a14ab80de91ac05aab272483d373ddbfa2405179ad5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527ad0da4d40995ebd468ce634652c34c9e3601a19ae27a111575bffd5b4fc62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d0e5dc90340c6a31cd7aa1dfb8f1c07930e6bda4f3c56fb3e1862c90150a79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7ecac03578e224c1fe03f5de740ad09ede82717e68bf376106a57af7514fc2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293db56195c7a37c0e294d9202d3e5f703c173d294ba0f71f99b1e4ea08cc306(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671f458042a4d89ed33082f30d965e482e5b38a7f8338c9e83f814385c91de11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CognitoUserPoolSchema]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32d36d8328006032a1389001b857bd524f5874522fe4351684e390e2a523579(
    *,
    max_value: typing.Optional[builtins.str] = None,
    min_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12125e68559fb65e41fbb4ce8e4f4df26bfbc3fd6fdb30611aab2c53a4365e38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fff08a2db82903038f8dc8664b69648ad8776dfb0f800279ffc7d37253d0c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de587eb8066379dc9035de8d360acefecc4d09a2d92449d7b50857b0c2bdcd2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c594b66e7a620d5e1b70078454418463cd92fe36fe3ca7f806b997dee8057662(
    value: typing.Optional[CognitoUserPoolSchemaNumberAttributeConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8054f77b4efee5c18c00a042b22de36a02c2f0fb3a6465d9501b6f4168c966(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706e293a458d4165dd4e0921d9d8891c5cf81388c5fce1e3ebe445a285876b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbbbf7ae7a2899f27503e6b1c39c431d0fe627e205749daffeeb0297b14962a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f55912451a2736dd088bf2df62d83c57ae8f13781a73070e1b0fedcd0f23e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171a223f34df91cae8c6089a57465a79285b0cec93950693f34e0315e96d5302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698f166e52580250785905ef175f2b5493292000e241b1650fdd105aaa86804f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b0a304408f9fbfbb1e01fd2be9af465ee978e3480fc1f516681b8e60dcec64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CognitoUserPoolSchema]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117f050d7ca69a59e43c48bd791fa85d73d9dc53bdabd1416f6f83e634c94025(
    *,
    max_length: typing.Optional[builtins.str] = None,
    min_length: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42424a4003480fbe3fe2cff014b8e6e0d83aeb2511079591bedc78394d89fc17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4196fc7be63861aefbe5ba8c4d9a521f38b7829389bf7a5f14c1b51da1e9be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5873a24f11a950b8e4230d14be5439861976c20fbc8bcdd688f1b8a43baaa3c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb1125954b386fbbdbdb9263d29bff63edaeb6049324d66387c94053d18a9bd(
    value: typing.Optional[CognitoUserPoolSchemaStringAttributeConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fb2425e2b9654fbe93c45b5583aa2c4b10c46411022cc4549e46def5b29e07(
    *,
    allowed_first_auth_factors: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1d371672b86715af9976665984e1d9dd5211a47d132e19307d6a1ba4c8d1a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9f96df1d1b6742bf4445ad2529df07defe5273a908494fa33206943fb64f7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff73600fb3011151ddca40894077f54429d923187718feff5f0b84a5f79c101(
    value: typing.Optional[CognitoUserPoolSignInPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e97872fdfeac02cd4e90d1f54617e8205dcc1daca930ceb0697ce78267b1fa0(
    *,
    external_id: builtins.str,
    sns_caller_arn: builtins.str,
    sns_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7d542912e2c7cb4f7f7d7c3735aa5b9117989c86419355e0fdab4e84ce8c32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a448bd4decce6d30cd8f525b5871856c7da8aa1b272a9fabd29b368c1adc5b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd68f29ebbd55e1576a25260cb749719b068ff130c62c6babd8e978ff899ff0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167ff9987ea74b7e000c590f4e2fb168c640adf6a0acc66048292d17772d78dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25124069f57933a99dc6d489912d5756cee403bf0af50425a1ac20b7efabb0c5(
    value: typing.Optional[CognitoUserPoolSmsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43673c87f798a2991fdf2edcd70b5aebe4177c52c9eb00b4bfaec77c4cb89778(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a21fd61c4c6989a0ea9b3ba85904068d168e6fb2854f064c6674417418c8713(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990e997d7c12e5190224415556218406f1bbea8f87f59f9fd2cacb5c2dd23f0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32b09287fa5ce42f74ba7f83895f11bc7b63c1fe6911052cfd1fb4514b1f43a(
    value: typing.Optional[CognitoUserPoolSoftwareTokenMfaConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61819ae735392d0b227b6e3024d33247546143116064ad397fd11aa9e968ead8(
    *,
    attributes_require_verification_before_update: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fcab2e5c6be0fa0de9285e8d27fb194670aa4d74a442a48298873245a70405(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0cee101edea7fff6063548c05ebaecbbdc32c95ce01168c719bc3af91dbafb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28363d71e9312a26505f23addd5b5e93f919923f167dcbe6185d558228ce1e97(
    value: typing.Optional[CognitoUserPoolUserAttributeUpdateSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21bd072d96fc217f6d469063a020cceed2be834bdf83ed99e5e701f61f56bdb(
    *,
    advanced_security_mode: builtins.str,
    advanced_security_additional_flows: typing.Optional[typing.Union[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd031c6b82e9df0f6602df01623115ad39488f48219e1b7f67f3727ecb18c49(
    *,
    custom_auth_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa21669158caed5158ab2cf33c36d4c47230b23a1ad20a6388e5470b69bc8a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a74876ff268aaaf977bb0ae1badbcb6a10b9187ef13da26ec7bffa759ae0792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b6adfc20a96471e5142e1993436067b742d8ffacab11a984e3f3a8368b17f3(
    value: typing.Optional[CognitoUserPoolUserPoolAddOnsAdvancedSecurityAdditionalFlows],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34408c7075e950ef7d87e304676cf7288f0c3050f3cc956e5f6254642152011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df295b085415f4f294948433cf6de6f3a43f013ff286f40e5879790faec27382(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16ddf37ee439df947f71ce552ed3ab236312e5ace78e8198870e6cb042d6396(
    value: typing.Optional[CognitoUserPoolUserPoolAddOns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee23b3be485c6835535b556af2d764afb5c148efd7a562156e0d192b77a08b7(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a934ccdaba3c5d2769945468a87e29d4cb928c1eeb9f18e3cca87175abc263(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0143e98d0b763d8ca1b7717b8e7bfaeb95ff04c32447e3dc49c13504850b6ee8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4dc108f5e8c5a979208fec47fee0e57914b419b5f5f4e6669b123da4d3db51(
    value: typing.Optional[CognitoUserPoolUsernameConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e763b067160fac805fe8caa4b03877f1c9891b4d2448172c0529375c90386131(
    *,
    default_email_option: typing.Optional[builtins.str] = None,
    email_message: typing.Optional[builtins.str] = None,
    email_message_by_link: typing.Optional[builtins.str] = None,
    email_subject: typing.Optional[builtins.str] = None,
    email_subject_by_link: typing.Optional[builtins.str] = None,
    sms_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685f25441304ccbe1c88a059cb875bd458f146b262870092b2da3eb03ea745a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd88ddbbde9e9bb8aea9a9ee5f7c84eaf5165d39e85d58e4cf1f5215c6340c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661b5a4df3e54a6092393aded5e980512bb1c4f7d082d535900da5b7a896d537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3da72730070e9ad780d438e8f258a14f5e760eab82acb841ba4b6eb61b115d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b611ee45ddfe70529c0b8f8d99ace1c1e142460303141d073215bab53ad3a88d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9dd61b84129efc3c70d2bc67079e623616cf0668e99242803ab6f95f8a1ae7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3f859a6ca224692bc1e5346f851fe0f3d18decb88ebd864174480abe0a7901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e02aef994b2b2b24ca6dded16d43c02ae0eb95d110948278b3318d6c28565d(
    value: typing.Optional[CognitoUserPoolVerificationMessageTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c012667b4eebb56bff595bad7453f8417900b7286dd9f9b43d1a981c709ff6fa(
    *,
    relying_party_id: typing.Optional[builtins.str] = None,
    user_verification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce049caa349cc4c01efc3ad059282c7443c8b3c4d8e6048d7008cdaf03c0fee6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba3914e81517cb06c27f7499fa4c3854eba33f542642a8af7bf9920595facc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15783652361a95fe468e7cc44bcd369c64ddcc5146ac8804c61cd5ae99d05b35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ee7f5c04005688c7c3dc216abc61b1907a15918448e18d311fa9e85c228d5c(
    value: typing.Optional[CognitoUserPoolWebAuthnConfiguration],
) -> None:
    """Type checking stubs"""
    pass
