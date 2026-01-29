r'''
# `aws_wafv2_web_acl`

Refer to the Terraform Registry for docs: [`aws_wafv2_web_acl`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl).
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


class Wafv2WebAcl(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAcl",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl aws_wafv2_web_acl}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_action: typing.Union["Wafv2WebAclDefaultAction", typing.Dict[builtins.str, typing.Any]],
        scope: builtins.str,
        visibility_config: typing.Union["Wafv2WebAclVisibilityConfig", typing.Dict[builtins.str, typing.Any]],
        association_config: typing.Optional[typing.Union["Wafv2WebAclAssociationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        captcha_config: typing.Optional[typing.Union["Wafv2WebAclCaptchaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        challenge_config: typing.Optional[typing.Union["Wafv2WebAclChallengeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_response_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclCustomResponseBody", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_protection_config: typing.Optional[typing.Union["Wafv2WebAclDataProtectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rule_json: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        token_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl aws_wafv2_web_acl} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_action: default_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_action Wafv2WebAcl#default_action}
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#scope Wafv2WebAcl#scope}.
        :param visibility_config: visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#visibility_config Wafv2WebAcl#visibility_config}
        :param association_config: association_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#association_config Wafv2WebAcl#association_config}
        :param captcha_config: captcha_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha_config Wafv2WebAcl#captcha_config}
        :param challenge_config: challenge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge_config Wafv2WebAcl#challenge_config}
        :param custom_response_body: custom_response_body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body Wafv2WebAcl#custom_response_body}
        :param data_protection_config: data_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#data_protection_config Wafv2WebAcl#data_protection_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#description Wafv2WebAcl#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#id Wafv2WebAcl#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name_prefix Wafv2WebAcl#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#region Wafv2WebAcl#region}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule Wafv2WebAcl#rule}
        :param rule_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule_json Wafv2WebAcl#rule_json}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#tags Wafv2WebAcl#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#tags_all Wafv2WebAcl#tags_all}.
        :param token_domains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#token_domains Wafv2WebAcl#token_domains}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bacca56f499a3b02a462d08c7425e86ca2a1d18130ab2dfa652dc54570230a1)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Wafv2WebAclConfig(
            default_action=default_action,
            scope=scope,
            visibility_config=visibility_config,
            association_config=association_config,
            captcha_config=captcha_config,
            challenge_config=challenge_config,
            custom_response_body=custom_response_body,
            data_protection_config=data_protection_config,
            description=description,
            id=id,
            name=name,
            name_prefix=name_prefix,
            region=region,
            rule=rule,
            rule_json=rule_json,
            tags=tags,
            tags_all=tags_all,
            token_domains=token_domains,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Wafv2WebAcl resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Wafv2WebAcl to import.
        :param import_from_id: The id of the existing Wafv2WebAcl that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Wafv2WebAcl to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a81b401034dc40dbee996e70f5400d3788286f1f937812e94430e0b64f26e73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAssociationConfig")
    def put_association_config(
        self,
        *,
        request_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclAssociationConfigRequestBody", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_body: request_body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#request_body Wafv2WebAcl#request_body}
        '''
        value = Wafv2WebAclAssociationConfig(request_body=request_body)

        return typing.cast(None, jsii.invoke(self, "putAssociationConfig", [value]))

    @jsii.member(jsii_name="putCaptchaConfig")
    def put_captcha_config(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union["Wafv2WebAclCaptchaConfigImmunityTimeProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        value = Wafv2WebAclCaptchaConfig(immunity_time_property=immunity_time_property)

        return typing.cast(None, jsii.invoke(self, "putCaptchaConfig", [value]))

    @jsii.member(jsii_name="putChallengeConfig")
    def put_challenge_config(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union["Wafv2WebAclChallengeConfigImmunityTimeProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        value = Wafv2WebAclChallengeConfig(
            immunity_time_property=immunity_time_property
        )

        return typing.cast(None, jsii.invoke(self, "putChallengeConfig", [value]))

    @jsii.member(jsii_name="putCustomResponseBody")
    def put_custom_response_body(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclCustomResponseBody", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47cf5a1579be5ffd95f2e234d8cc9055e7add822abc72b98308b0328234b6648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomResponseBody", [value]))

    @jsii.member(jsii_name="putDataProtectionConfig")
    def put_data_protection_config(
        self,
        *,
        data_protection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclDataProtectionConfigDataProtection", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_protection: data_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#data_protection Wafv2WebAcl#data_protection}
        '''
        value = Wafv2WebAclDataProtectionConfig(data_protection=data_protection)

        return typing.cast(None, jsii.invoke(self, "putDataProtectionConfig", [value]))

    @jsii.member(jsii_name="putDefaultAction")
    def put_default_action(
        self,
        *,
        allow: typing.Optional[typing.Union["Wafv2WebAclDefaultActionAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        block: typing.Optional[typing.Union["Wafv2WebAclDefaultActionBlock", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#allow Wafv2WebAcl#allow}
        :param block: block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#block Wafv2WebAcl#block}
        '''
        value = Wafv2WebAclDefaultAction(allow=allow, block=block)

        return typing.cast(None, jsii.invoke(self, "putDefaultAction", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081577810311b70bac1d78bef696c9da63c42b77c34d1e8af2baeb08e4a64c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="putVisibilityConfig")
    def put_visibility_config(
        self,
        *,
        cloudwatch_metrics_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        metric_name: builtins.str,
        sampled_requests_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param cloudwatch_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudwatch_metrics_enabled Wafv2WebAcl#cloudwatch_metrics_enabled}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#metric_name Wafv2WebAcl#metric_name}.
        :param sampled_requests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#sampled_requests_enabled Wafv2WebAcl#sampled_requests_enabled}.
        '''
        value = Wafv2WebAclVisibilityConfig(
            cloudwatch_metrics_enabled=cloudwatch_metrics_enabled,
            metric_name=metric_name,
            sampled_requests_enabled=sampled_requests_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putVisibilityConfig", [value]))

    @jsii.member(jsii_name="resetAssociationConfig")
    def reset_association_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssociationConfig", []))

    @jsii.member(jsii_name="resetCaptchaConfig")
    def reset_captcha_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptchaConfig", []))

    @jsii.member(jsii_name="resetChallengeConfig")
    def reset_challenge_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChallengeConfig", []))

    @jsii.member(jsii_name="resetCustomResponseBody")
    def reset_custom_response_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomResponseBody", []))

    @jsii.member(jsii_name="resetDataProtectionConfig")
    def reset_data_protection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @jsii.member(jsii_name="resetRuleJson")
    def reset_rule_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleJson", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTokenDomains")
    def reset_token_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenDomains", []))

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
    @jsii.member(jsii_name="applicationIntegrationUrl")
    def application_integration_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationIntegrationUrl"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="associationConfig")
    def association_config(self) -> "Wafv2WebAclAssociationConfigOutputReference":
        return typing.cast("Wafv2WebAclAssociationConfigOutputReference", jsii.get(self, "associationConfig"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="captchaConfig")
    def captcha_config(self) -> "Wafv2WebAclCaptchaConfigOutputReference":
        return typing.cast("Wafv2WebAclCaptchaConfigOutputReference", jsii.get(self, "captchaConfig"))

    @builtins.property
    @jsii.member(jsii_name="challengeConfig")
    def challenge_config(self) -> "Wafv2WebAclChallengeConfigOutputReference":
        return typing.cast("Wafv2WebAclChallengeConfigOutputReference", jsii.get(self, "challengeConfig"))

    @builtins.property
    @jsii.member(jsii_name="customResponseBody")
    def custom_response_body(self) -> "Wafv2WebAclCustomResponseBodyList":
        return typing.cast("Wafv2WebAclCustomResponseBodyList", jsii.get(self, "customResponseBody"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionConfig")
    def data_protection_config(
        self,
    ) -> "Wafv2WebAclDataProtectionConfigOutputReference":
        return typing.cast("Wafv2WebAclDataProtectionConfigOutputReference", jsii.get(self, "dataProtectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> "Wafv2WebAclDefaultActionOutputReference":
        return typing.cast("Wafv2WebAclDefaultActionOutputReference", jsii.get(self, "defaultAction"))

    @builtins.property
    @jsii.member(jsii_name="lockToken")
    def lock_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockToken"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "Wafv2WebAclRuleList":
        return typing.cast("Wafv2WebAclRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="visibilityConfig")
    def visibility_config(self) -> "Wafv2WebAclVisibilityConfigOutputReference":
        return typing.cast("Wafv2WebAclVisibilityConfigOutputReference", jsii.get(self, "visibilityConfig"))

    @builtins.property
    @jsii.member(jsii_name="associationConfigInput")
    def association_config_input(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfig"]:
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfig"], jsii.get(self, "associationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="captchaConfigInput")
    def captcha_config_input(self) -> typing.Optional["Wafv2WebAclCaptchaConfig"]:
        return typing.cast(typing.Optional["Wafv2WebAclCaptchaConfig"], jsii.get(self, "captchaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="challengeConfigInput")
    def challenge_config_input(self) -> typing.Optional["Wafv2WebAclChallengeConfig"]:
        return typing.cast(typing.Optional["Wafv2WebAclChallengeConfig"], jsii.get(self, "challengeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="customResponseBodyInput")
    def custom_response_body_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclCustomResponseBody"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclCustomResponseBody"]]], jsii.get(self, "customResponseBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionConfigInput")
    def data_protection_config_input(
        self,
    ) -> typing.Optional["Wafv2WebAclDataProtectionConfig"]:
        return typing.cast(typing.Optional["Wafv2WebAclDataProtectionConfig"], jsii.get(self, "dataProtectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(self) -> typing.Optional["Wafv2WebAclDefaultAction"]:
        return typing.cast(typing.Optional["Wafv2WebAclDefaultAction"], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleJsonInput")
    def rule_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

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
    @jsii.member(jsii_name="tokenDomainsInput")
    def token_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tokenDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityConfigInput")
    def visibility_config_input(self) -> typing.Optional["Wafv2WebAclVisibilityConfig"]:
        return typing.cast(typing.Optional["Wafv2WebAclVisibilityConfig"], jsii.get(self, "visibilityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff8fff4c6cfc097b72fd73d04f8d4079902c9eef77f61a627d4ff86a68fdb78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91089f6846d95ff0e30dd4eec5bca7b19be4af16b67e38ed595a7f0d70dc9f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7422278a77bfd4531787f5245bed804040d17fc819cef9466781e756bcc52c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db691fdb5330309f7cada4fc3fda210067157ec85462a997d85f5e7c70f9618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16a72f98e88ac1b1c0816249ecd28a973c35e1a850ebdb68c07aef761562c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleJson")
    def rule_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleJson"))

    @rule_json.setter
    def rule_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f1c55a8f32c0bc3675da8a7fe81585829c9ecb68b68d9c4b31545c31f8cb14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2fea4fe4c0644389030626a30b30099479fbad7cadbe4d2fe14556e5db609af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a11b455a6991d9122285238ba53327f45e4c643a3771e01a6cc5f8459e757a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d542a8413b07779725989a7cd2fcd8bfee61a02ecb8c117d4615644929110b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenDomains")
    def token_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tokenDomains"))

    @token_domains.setter
    def token_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f5ce624caaa75da5cd5f1c6f49d5af5ed9605fee61746d4ca312bc7e6b5690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenDomains", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfig",
    jsii_struct_bases=[],
    name_mapping={"request_body": "requestBody"},
)
class Wafv2WebAclAssociationConfig:
    def __init__(
        self,
        *,
        request_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclAssociationConfigRequestBody", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_body: request_body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#request_body Wafv2WebAcl#request_body}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322032451ba34136f93e37446edfc3f61eec3f74b20866b889bf7df4ce07dd79)
            check_type(argname="argument request_body", value=request_body, expected_type=type_hints["request_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_body is not None:
            self._values["request_body"] = request_body

    @builtins.property
    def request_body(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclAssociationConfigRequestBody"]]]:
        '''request_body block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#request_body Wafv2WebAcl#request_body}
        '''
        result = self._values.get("request_body")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclAssociationConfigRequestBody"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclAssociationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ea0f0ff26a99ecdaad62456cf4d539efbbc4de0d2aa2133dd94e4d9d0838118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestBody")
    def put_request_body(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclAssociationConfigRequestBody", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28c224cb04d9ebc1a0736f394ee726b2155bf6af3328cd1d2bda1d74603660e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestBody", [value]))

    @jsii.member(jsii_name="resetRequestBody")
    def reset_request_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBody", []))

    @builtins.property
    @jsii.member(jsii_name="requestBody")
    def request_body(self) -> "Wafv2WebAclAssociationConfigRequestBodyList":
        return typing.cast("Wafv2WebAclAssociationConfigRequestBodyList", jsii.get(self, "requestBody"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyInput")
    def request_body_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclAssociationConfigRequestBody"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclAssociationConfigRequestBody"]]], jsii.get(self, "requestBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclAssociationConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclAssociationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30674cb5d8d06ce8c7d6ef3292927c56ddad7741fe7f02249ba7e4fc1f70849c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBody",
    jsii_struct_bases=[],
    name_mapping={
        "api_gateway": "apiGateway",
        "app_runner_service": "appRunnerService",
        "cloudfront": "cloudfront",
        "cognito_user_pool": "cognitoUserPool",
        "verified_access_instance": "verifiedAccessInstance",
    },
)
class Wafv2WebAclAssociationConfigRequestBody:
    def __init__(
        self,
        *,
        api_gateway: typing.Optional[typing.Union["Wafv2WebAclAssociationConfigRequestBodyApiGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        app_runner_service: typing.Optional[typing.Union["Wafv2WebAclAssociationConfigRequestBodyAppRunnerService", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudfront: typing.Optional[typing.Union["Wafv2WebAclAssociationConfigRequestBodyCloudfront", typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_user_pool: typing.Optional[typing.Union["Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool", typing.Dict[builtins.str, typing.Any]]] = None,
        verified_access_instance: typing.Optional[typing.Union["Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_gateway: api_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#api_gateway Wafv2WebAcl#api_gateway}
        :param app_runner_service: app_runner_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#app_runner_service Wafv2WebAcl#app_runner_service}
        :param cloudfront: cloudfront block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudfront Wafv2WebAcl#cloudfront}
        :param cognito_user_pool: cognito_user_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cognito_user_pool Wafv2WebAcl#cognito_user_pool}
        :param verified_access_instance: verified_access_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#verified_access_instance Wafv2WebAcl#verified_access_instance}
        '''
        if isinstance(api_gateway, dict):
            api_gateway = Wafv2WebAclAssociationConfigRequestBodyApiGateway(**api_gateway)
        if isinstance(app_runner_service, dict):
            app_runner_service = Wafv2WebAclAssociationConfigRequestBodyAppRunnerService(**app_runner_service)
        if isinstance(cloudfront, dict):
            cloudfront = Wafv2WebAclAssociationConfigRequestBodyCloudfront(**cloudfront)
        if isinstance(cognito_user_pool, dict):
            cognito_user_pool = Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool(**cognito_user_pool)
        if isinstance(verified_access_instance, dict):
            verified_access_instance = Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance(**verified_access_instance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae5234493a4916c5a0415725c89c83d10a585a830e61aab5746999a5f4860cd)
            check_type(argname="argument api_gateway", value=api_gateway, expected_type=type_hints["api_gateway"])
            check_type(argname="argument app_runner_service", value=app_runner_service, expected_type=type_hints["app_runner_service"])
            check_type(argname="argument cloudfront", value=cloudfront, expected_type=type_hints["cloudfront"])
            check_type(argname="argument cognito_user_pool", value=cognito_user_pool, expected_type=type_hints["cognito_user_pool"])
            check_type(argname="argument verified_access_instance", value=verified_access_instance, expected_type=type_hints["verified_access_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_gateway is not None:
            self._values["api_gateway"] = api_gateway
        if app_runner_service is not None:
            self._values["app_runner_service"] = app_runner_service
        if cloudfront is not None:
            self._values["cloudfront"] = cloudfront
        if cognito_user_pool is not None:
            self._values["cognito_user_pool"] = cognito_user_pool
        if verified_access_instance is not None:
            self._values["verified_access_instance"] = verified_access_instance

    @builtins.property
    def api_gateway(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfigRequestBodyApiGateway"]:
        '''api_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#api_gateway Wafv2WebAcl#api_gateway}
        '''
        result = self._values.get("api_gateway")
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfigRequestBodyApiGateway"], result)

    @builtins.property
    def app_runner_service(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfigRequestBodyAppRunnerService"]:
        '''app_runner_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#app_runner_service Wafv2WebAcl#app_runner_service}
        '''
        result = self._values.get("app_runner_service")
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfigRequestBodyAppRunnerService"], result)

    @builtins.property
    def cloudfront(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfigRequestBodyCloudfront"]:
        '''cloudfront block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudfront Wafv2WebAcl#cloudfront}
        '''
        result = self._values.get("cloudfront")
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfigRequestBodyCloudfront"], result)

    @builtins.property
    def cognito_user_pool(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool"]:
        '''cognito_user_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cognito_user_pool Wafv2WebAcl#cognito_user_pool}
        '''
        result = self._values.get("cognito_user_pool")
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool"], result)

    @builtins.property
    def verified_access_instance(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance"]:
        '''verified_access_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#verified_access_instance Wafv2WebAcl#verified_access_instance}
        '''
        result = self._values.get("verified_access_instance")
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfigRequestBody(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyApiGateway",
    jsii_struct_bases=[],
    name_mapping={"default_size_inspection_limit": "defaultSizeInspectionLimit"},
)
class Wafv2WebAclAssociationConfigRequestBodyApiGateway:
    def __init__(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cede49b91fe34ff280d2f00ac3d67fa56e59af46ed88e6a2f9d547bb2c724a5)
            check_type(argname="argument default_size_inspection_limit", value=default_size_inspection_limit, expected_type=type_hints["default_size_inspection_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_size_inspection_limit": default_size_inspection_limit,
        }

    @builtins.property
    def default_size_inspection_limit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.'''
        result = self._values.get("default_size_inspection_limit")
        assert result is not None, "Required property 'default_size_inspection_limit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfigRequestBodyApiGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclAssociationConfigRequestBodyApiGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyApiGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e55b83884c0d4c51d698bd7522b999e2d1e2cfe4e78be59b3fa908c1f04c83e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimitInput")
    def default_size_inspection_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSizeInspectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimit")
    def default_size_inspection_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSizeInspectionLimit"))

    @default_size_inspection_limit.setter
    def default_size_inspection_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390562097734a7d8153e3559c8534e1b2b3a287cb391895f3e1b8284f6c5d3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSizeInspectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyApiGateway]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyApiGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyApiGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b32e2d7e99c793b0105a0eb98ad1462643d42beceb6c4182eece377effa61ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyAppRunnerService",
    jsii_struct_bases=[],
    name_mapping={"default_size_inspection_limit": "defaultSizeInspectionLimit"},
)
class Wafv2WebAclAssociationConfigRequestBodyAppRunnerService:
    def __init__(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005cbd452d37e35930a328bcc9c44a18c8a8e29d9cb711e78c24727f027e251c)
            check_type(argname="argument default_size_inspection_limit", value=default_size_inspection_limit, expected_type=type_hints["default_size_inspection_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_size_inspection_limit": default_size_inspection_limit,
        }

    @builtins.property
    def default_size_inspection_limit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.'''
        result = self._values.get("default_size_inspection_limit")
        assert result is not None, "Required property 'default_size_inspection_limit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfigRequestBodyAppRunnerService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclAssociationConfigRequestBodyAppRunnerServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyAppRunnerServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6a47ef939ab81e1265cb62d27fae1c2b90db6a763e6a2c1e8bf37836bd1529)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimitInput")
    def default_size_inspection_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSizeInspectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimit")
    def default_size_inspection_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSizeInspectionLimit"))

    @default_size_inspection_limit.setter
    def default_size_inspection_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14db49bceaf9d0a812251658e368ba75f2bb87513fbeb5728fe17f18e73f567f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSizeInspectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd91c6f3997ae1fd790f372561819bbd89509eed8290039fe026bcbd3d0bda1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyCloudfront",
    jsii_struct_bases=[],
    name_mapping={"default_size_inspection_limit": "defaultSizeInspectionLimit"},
)
class Wafv2WebAclAssociationConfigRequestBodyCloudfront:
    def __init__(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dff72cfd6927f2124e3cf14aaf0849958ac9448abd3a80f451b47af5181acf4)
            check_type(argname="argument default_size_inspection_limit", value=default_size_inspection_limit, expected_type=type_hints["default_size_inspection_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_size_inspection_limit": default_size_inspection_limit,
        }

    @builtins.property
    def default_size_inspection_limit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.'''
        result = self._values.get("default_size_inspection_limit")
        assert result is not None, "Required property 'default_size_inspection_limit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfigRequestBodyCloudfront(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclAssociationConfigRequestBodyCloudfrontOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyCloudfrontOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2641af708c61bd86bf9866ad6e6b4c42553105f957f129fb982118496173d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimitInput")
    def default_size_inspection_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSizeInspectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimit")
    def default_size_inspection_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSizeInspectionLimit"))

    @default_size_inspection_limit.setter
    def default_size_inspection_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a80882b6f4a3cc61aaf028f4e1e7824dc26095630c16ee068a4bf94b70c614b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSizeInspectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCloudfront]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCloudfront], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCloudfront],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bab7578bb083a1acf526c69428b0c30f41f2ddbea309df1c601a29b068a5012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool",
    jsii_struct_bases=[],
    name_mapping={"default_size_inspection_limit": "defaultSizeInspectionLimit"},
)
class Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool:
    def __init__(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bdefe2663fdbf7085e967f3ff44fee5ffd3146e2893185ba1f48aef563f92b)
            check_type(argname="argument default_size_inspection_limit", value=default_size_inspection_limit, expected_type=type_hints["default_size_inspection_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_size_inspection_limit": default_size_inspection_limit,
        }

    @builtins.property
    def default_size_inspection_limit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.'''
        result = self._values.get("default_size_inspection_limit")
        assert result is not None, "Required property 'default_size_inspection_limit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclAssociationConfigRequestBodyCognitoUserPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyCognitoUserPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2256294d89f43f1915dcb8bd6654e4916533bcc59139fbba84dada4bd03bdee3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimitInput")
    def default_size_inspection_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSizeInspectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimit")
    def default_size_inspection_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSizeInspectionLimit"))

    @default_size_inspection_limit.setter
    def default_size_inspection_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86371d247fd6751ebb1e5a1ecab439ac99d28d976c90c848cdfab170b6d401d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSizeInspectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd81a1d822654f24db60e7628cd3a66c7c373d09dd471ea10f10f6e7a7a3677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclAssociationConfigRequestBodyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef5224b0cacd6e857f694ee54c21c38e5bd88dd02a73f4027df6f93fd456f2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclAssociationConfigRequestBodyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48dbf522efa54ba4676fb00a7f01fe8791e284580a9b57967e60035226b361b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclAssociationConfigRequestBodyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd435df5f048b49e1a12ab71eecafd6363a7dbffc83ad0ec432948adb39a5ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a91cbdb8f3ecfe8c4589376d74c811e01687a7faffdd7a8376a1930f54236e36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e49b339a40e4a2b41e7059371feae97f941318d28ff12df2e7cbd6591b1a8b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclAssociationConfigRequestBody]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclAssociationConfigRequestBody]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclAssociationConfigRequestBody]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13fa06d764e58f7fd98568f1f68fc16b247186e01232b0c75a3ac0566c125fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclAssociationConfigRequestBodyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffe0cee958b53943ff663d61a94dc4178785e3e07821bf4acfcae5ba00c2ae8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putApiGateway")
    def put_api_gateway(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        value = Wafv2WebAclAssociationConfigRequestBodyApiGateway(
            default_size_inspection_limit=default_size_inspection_limit
        )

        return typing.cast(None, jsii.invoke(self, "putApiGateway", [value]))

    @jsii.member(jsii_name="putAppRunnerService")
    def put_app_runner_service(
        self,
        *,
        default_size_inspection_limit: builtins.str,
    ) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        value = Wafv2WebAclAssociationConfigRequestBodyAppRunnerService(
            default_size_inspection_limit=default_size_inspection_limit
        )

        return typing.cast(None, jsii.invoke(self, "putAppRunnerService", [value]))

    @jsii.member(jsii_name="putCloudfront")
    def put_cloudfront(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        value = Wafv2WebAclAssociationConfigRequestBodyCloudfront(
            default_size_inspection_limit=default_size_inspection_limit
        )

        return typing.cast(None, jsii.invoke(self, "putCloudfront", [value]))

    @jsii.member(jsii_name="putCognitoUserPool")
    def put_cognito_user_pool(
        self,
        *,
        default_size_inspection_limit: builtins.str,
    ) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        value = Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool(
            default_size_inspection_limit=default_size_inspection_limit
        )

        return typing.cast(None, jsii.invoke(self, "putCognitoUserPool", [value]))

    @jsii.member(jsii_name="putVerifiedAccessInstance")
    def put_verified_access_instance(
        self,
        *,
        default_size_inspection_limit: builtins.str,
    ) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        value = Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance(
            default_size_inspection_limit=default_size_inspection_limit
        )

        return typing.cast(None, jsii.invoke(self, "putVerifiedAccessInstance", [value]))

    @jsii.member(jsii_name="resetApiGateway")
    def reset_api_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiGateway", []))

    @jsii.member(jsii_name="resetAppRunnerService")
    def reset_app_runner_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppRunnerService", []))

    @jsii.member(jsii_name="resetCloudfront")
    def reset_cloudfront(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudfront", []))

    @jsii.member(jsii_name="resetCognitoUserPool")
    def reset_cognito_user_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCognitoUserPool", []))

    @jsii.member(jsii_name="resetVerifiedAccessInstance")
    def reset_verified_access_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifiedAccessInstance", []))

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(
        self,
    ) -> Wafv2WebAclAssociationConfigRequestBodyApiGatewayOutputReference:
        return typing.cast(Wafv2WebAclAssociationConfigRequestBodyApiGatewayOutputReference, jsii.get(self, "apiGateway"))

    @builtins.property
    @jsii.member(jsii_name="appRunnerService")
    def app_runner_service(
        self,
    ) -> Wafv2WebAclAssociationConfigRequestBodyAppRunnerServiceOutputReference:
        return typing.cast(Wafv2WebAclAssociationConfigRequestBodyAppRunnerServiceOutputReference, jsii.get(self, "appRunnerService"))

    @builtins.property
    @jsii.member(jsii_name="cloudfront")
    def cloudfront(
        self,
    ) -> Wafv2WebAclAssociationConfigRequestBodyCloudfrontOutputReference:
        return typing.cast(Wafv2WebAclAssociationConfigRequestBodyCloudfrontOutputReference, jsii.get(self, "cloudfront"))

    @builtins.property
    @jsii.member(jsii_name="cognitoUserPool")
    def cognito_user_pool(
        self,
    ) -> Wafv2WebAclAssociationConfigRequestBodyCognitoUserPoolOutputReference:
        return typing.cast(Wafv2WebAclAssociationConfigRequestBodyCognitoUserPoolOutputReference, jsii.get(self, "cognitoUserPool"))

    @builtins.property
    @jsii.member(jsii_name="verifiedAccessInstance")
    def verified_access_instance(
        self,
    ) -> "Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstanceOutputReference":
        return typing.cast("Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstanceOutputReference", jsii.get(self, "verifiedAccessInstance"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayInput")
    def api_gateway_input(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyApiGateway]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyApiGateway], jsii.get(self, "apiGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="appRunnerServiceInput")
    def app_runner_service_input(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService], jsii.get(self, "appRunnerServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontInput")
    def cloudfront_input(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCloudfront]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCloudfront], jsii.get(self, "cloudfrontInput"))

    @builtins.property
    @jsii.member(jsii_name="cognitoUserPoolInput")
    def cognito_user_pool_input(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool], jsii.get(self, "cognitoUserPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="verifiedAccessInstanceInput")
    def verified_access_instance_input(
        self,
    ) -> typing.Optional["Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance"]:
        return typing.cast(typing.Optional["Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance"], jsii.get(self, "verifiedAccessInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclAssociationConfigRequestBody]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclAssociationConfigRequestBody]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclAssociationConfigRequestBody]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b523954de00db1d7ecbfd0f1a5d52669d85a939683cf3718b22594b605c4bab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance",
    jsii_struct_bases=[],
    name_mapping={"default_size_inspection_limit": "defaultSizeInspectionLimit"},
)
class Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance:
    def __init__(self, *, default_size_inspection_limit: builtins.str) -> None:
        '''
        :param default_size_inspection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7793a8b35253bb545e577df8a6b1ccc1877ea0b6960361df4d5b63f81b6221cc)
            check_type(argname="argument default_size_inspection_limit", value=default_size_inspection_limit, expected_type=type_hints["default_size_inspection_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_size_inspection_limit": default_size_inspection_limit,
        }

    @builtins.property
    def default_size_inspection_limit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_size_inspection_limit Wafv2WebAcl#default_size_inspection_limit}.'''
        result = self._values.get("default_size_inspection_limit")
        assert result is not None, "Required property 'default_size_inspection_limit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94fe3cb56a43249e687a9ca2dcaf1905a987b31ab083738fc902aab4cc334a59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimitInput")
    def default_size_inspection_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSizeInspectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSizeInspectionLimit")
    def default_size_inspection_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSizeInspectionLimit"))

    @default_size_inspection_limit.setter
    def default_size_inspection_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22f0058056c3c6f1cc1323f97b1fc4491cedc16fc888684b22e0e45d409dd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSizeInspectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance]:
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8296bd993604d102ad080336d785752cac21698031299d32d8cd254f13dfe5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCaptchaConfig",
    jsii_struct_bases=[],
    name_mapping={"immunity_time_property": "immunityTimeProperty"},
)
class Wafv2WebAclCaptchaConfig:
    def __init__(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union["Wafv2WebAclCaptchaConfigImmunityTimeProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        if isinstance(immunity_time_property, dict):
            immunity_time_property = Wafv2WebAclCaptchaConfigImmunityTimeProperty(**immunity_time_property)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6fa2aca8a649ddec07b8f109edf9fab9b97e4bfb5bf45f8dacd28e9557b2fc5)
            check_type(argname="argument immunity_time_property", value=immunity_time_property, expected_type=type_hints["immunity_time_property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time_property is not None:
            self._values["immunity_time_property"] = immunity_time_property

    @builtins.property
    def immunity_time_property(
        self,
    ) -> typing.Optional["Wafv2WebAclCaptchaConfigImmunityTimeProperty"]:
        '''immunity_time_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        result = self._values.get("immunity_time_property")
        return typing.cast(typing.Optional["Wafv2WebAclCaptchaConfigImmunityTimeProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclCaptchaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCaptchaConfigImmunityTimeProperty",
    jsii_struct_bases=[],
    name_mapping={"immunity_time": "immunityTime"},
)
class Wafv2WebAclCaptchaConfigImmunityTimeProperty:
    def __init__(self, *, immunity_time: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2312ffdaff3cb0e15d7cece12802b900e647b78c10471f8f35af418b157cb20)
            check_type(argname="argument immunity_time", value=immunity_time, expected_type=type_hints["immunity_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time is not None:
            self._values["immunity_time"] = immunity_time

    @builtins.property
    def immunity_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.'''
        result = self._values.get("immunity_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclCaptchaConfigImmunityTimeProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclCaptchaConfigImmunityTimePropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCaptchaConfigImmunityTimePropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec84a1817c92c2063e6c33791b4ed4adf1329ff99520034690d73af7ef51ae79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmunityTime")
    def reset_immunity_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTime", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeInput")
    def immunity_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "immunityTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="immunityTime")
    def immunity_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "immunityTime"))

    @immunity_time.setter
    def immunity_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69374857f420f836759e5f142109e6c75cb0ad0b0b1dcf3e31f477776cc3300c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immunityTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclCaptchaConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclCaptchaConfigImmunityTimeProperty], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclCaptchaConfigImmunityTimeProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4be9cf5023b21efc442cbc6fa3059923dd4f183b88d21b0b08b8abd3d69ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclCaptchaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCaptchaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf5a65c896b1f75270291ea52862f2d913d49f47184f78c3aae0acdf449e79c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImmunityTimeProperty")
    def put_immunity_time_property(
        self,
        *,
        immunity_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        value = Wafv2WebAclCaptchaConfigImmunityTimeProperty(
            immunity_time=immunity_time
        )

        return typing.cast(None, jsii.invoke(self, "putImmunityTimeProperty", [value]))

    @jsii.member(jsii_name="resetImmunityTimeProperty")
    def reset_immunity_time_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTimeProperty", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeProperty")
    def immunity_time_property(
        self,
    ) -> Wafv2WebAclCaptchaConfigImmunityTimePropertyOutputReference:
        return typing.cast(Wafv2WebAclCaptchaConfigImmunityTimePropertyOutputReference, jsii.get(self, "immunityTimeProperty"))

    @builtins.property
    @jsii.member(jsii_name="immunityTimePropertyInput")
    def immunity_time_property_input(
        self,
    ) -> typing.Optional[Wafv2WebAclCaptchaConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclCaptchaConfigImmunityTimeProperty], jsii.get(self, "immunityTimePropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclCaptchaConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclCaptchaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[Wafv2WebAclCaptchaConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30099605ca6e815a3bd5c21f3bc613d70d6aa24409c48d1fb0d5b27918481696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclChallengeConfig",
    jsii_struct_bases=[],
    name_mapping={"immunity_time_property": "immunityTimeProperty"},
)
class Wafv2WebAclChallengeConfig:
    def __init__(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union["Wafv2WebAclChallengeConfigImmunityTimeProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        if isinstance(immunity_time_property, dict):
            immunity_time_property = Wafv2WebAclChallengeConfigImmunityTimeProperty(**immunity_time_property)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e115cfd7f532bfeaf17db65b3163e0feb0726d18aa69cd60763f3736104050a5)
            check_type(argname="argument immunity_time_property", value=immunity_time_property, expected_type=type_hints["immunity_time_property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time_property is not None:
            self._values["immunity_time_property"] = immunity_time_property

    @builtins.property
    def immunity_time_property(
        self,
    ) -> typing.Optional["Wafv2WebAclChallengeConfigImmunityTimeProperty"]:
        '''immunity_time_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        result = self._values.get("immunity_time_property")
        return typing.cast(typing.Optional["Wafv2WebAclChallengeConfigImmunityTimeProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclChallengeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclChallengeConfigImmunityTimeProperty",
    jsii_struct_bases=[],
    name_mapping={"immunity_time": "immunityTime"},
)
class Wafv2WebAclChallengeConfigImmunityTimeProperty:
    def __init__(self, *, immunity_time: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66aec466fffaa0498619c21a0c2caeb27003a35b72e62a8fb449ee065d7f522)
            check_type(argname="argument immunity_time", value=immunity_time, expected_type=type_hints["immunity_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time is not None:
            self._values["immunity_time"] = immunity_time

    @builtins.property
    def immunity_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.'''
        result = self._values.get("immunity_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclChallengeConfigImmunityTimeProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclChallengeConfigImmunityTimePropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclChallengeConfigImmunityTimePropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7828eac20930715f584d1905be89c8320db6e4db3b67a3dd2872e21a85a23722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmunityTime")
    def reset_immunity_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTime", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeInput")
    def immunity_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "immunityTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="immunityTime")
    def immunity_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "immunityTime"))

    @immunity_time.setter
    def immunity_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e93083f8add2611f72b2a0510dfa03ba4f724c00a4ecf4e7cef242c5554f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immunityTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclChallengeConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclChallengeConfigImmunityTimeProperty], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclChallengeConfigImmunityTimeProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1be32e56ab96666238e9f85866674f53c0c1cbbfa5acb026ca34ed5576f75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclChallengeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclChallengeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__892eaef0c626af19b78ecc8e5fe26da10a34271e2971e8326b824a225528b89d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImmunityTimeProperty")
    def put_immunity_time_property(
        self,
        *,
        immunity_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        value = Wafv2WebAclChallengeConfigImmunityTimeProperty(
            immunity_time=immunity_time
        )

        return typing.cast(None, jsii.invoke(self, "putImmunityTimeProperty", [value]))

    @jsii.member(jsii_name="resetImmunityTimeProperty")
    def reset_immunity_time_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTimeProperty", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeProperty")
    def immunity_time_property(
        self,
    ) -> Wafv2WebAclChallengeConfigImmunityTimePropertyOutputReference:
        return typing.cast(Wafv2WebAclChallengeConfigImmunityTimePropertyOutputReference, jsii.get(self, "immunityTimeProperty"))

    @builtins.property
    @jsii.member(jsii_name="immunityTimePropertyInput")
    def immunity_time_property_input(
        self,
    ) -> typing.Optional[Wafv2WebAclChallengeConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclChallengeConfigImmunityTimeProperty], jsii.get(self, "immunityTimePropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclChallengeConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclChallengeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclChallengeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdc8d221c7ed210b7b50860a6ab2256caae59ea88bac18c735c218bf1d4573e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_action": "defaultAction",
        "scope": "scope",
        "visibility_config": "visibilityConfig",
        "association_config": "associationConfig",
        "captcha_config": "captchaConfig",
        "challenge_config": "challengeConfig",
        "custom_response_body": "customResponseBody",
        "data_protection_config": "dataProtectionConfig",
        "description": "description",
        "id": "id",
        "name": "name",
        "name_prefix": "namePrefix",
        "region": "region",
        "rule": "rule",
        "rule_json": "ruleJson",
        "tags": "tags",
        "tags_all": "tagsAll",
        "token_domains": "tokenDomains",
    },
)
class Wafv2WebAclConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_action: typing.Union["Wafv2WebAclDefaultAction", typing.Dict[builtins.str, typing.Any]],
        scope: builtins.str,
        visibility_config: typing.Union["Wafv2WebAclVisibilityConfig", typing.Dict[builtins.str, typing.Any]],
        association_config: typing.Optional[typing.Union[Wafv2WebAclAssociationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        captcha_config: typing.Optional[typing.Union[Wafv2WebAclCaptchaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        challenge_config: typing.Optional[typing.Union[Wafv2WebAclChallengeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_response_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclCustomResponseBody", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_protection_config: typing.Optional[typing.Union["Wafv2WebAclDataProtectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rule_json: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        token_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_action: default_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_action Wafv2WebAcl#default_action}
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#scope Wafv2WebAcl#scope}.
        :param visibility_config: visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#visibility_config Wafv2WebAcl#visibility_config}
        :param association_config: association_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#association_config Wafv2WebAcl#association_config}
        :param captcha_config: captcha_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha_config Wafv2WebAcl#captcha_config}
        :param challenge_config: challenge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge_config Wafv2WebAcl#challenge_config}
        :param custom_response_body: custom_response_body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body Wafv2WebAcl#custom_response_body}
        :param data_protection_config: data_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#data_protection_config Wafv2WebAcl#data_protection_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#description Wafv2WebAcl#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#id Wafv2WebAcl#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name_prefix Wafv2WebAcl#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#region Wafv2WebAcl#region}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule Wafv2WebAcl#rule}
        :param rule_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule_json Wafv2WebAcl#rule_json}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#tags Wafv2WebAcl#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#tags_all Wafv2WebAcl#tags_all}.
        :param token_domains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#token_domains Wafv2WebAcl#token_domains}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_action, dict):
            default_action = Wafv2WebAclDefaultAction(**default_action)
        if isinstance(visibility_config, dict):
            visibility_config = Wafv2WebAclVisibilityConfig(**visibility_config)
        if isinstance(association_config, dict):
            association_config = Wafv2WebAclAssociationConfig(**association_config)
        if isinstance(captcha_config, dict):
            captcha_config = Wafv2WebAclCaptchaConfig(**captcha_config)
        if isinstance(challenge_config, dict):
            challenge_config = Wafv2WebAclChallengeConfig(**challenge_config)
        if isinstance(data_protection_config, dict):
            data_protection_config = Wafv2WebAclDataProtectionConfig(**data_protection_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22005b7e448d418414d12f019356401f53a352182e1385bba3ce90d7b97ce91)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument visibility_config", value=visibility_config, expected_type=type_hints["visibility_config"])
            check_type(argname="argument association_config", value=association_config, expected_type=type_hints["association_config"])
            check_type(argname="argument captcha_config", value=captcha_config, expected_type=type_hints["captcha_config"])
            check_type(argname="argument challenge_config", value=challenge_config, expected_type=type_hints["challenge_config"])
            check_type(argname="argument custom_response_body", value=custom_response_body, expected_type=type_hints["custom_response_body"])
            check_type(argname="argument data_protection_config", value=data_protection_config, expected_type=type_hints["data_protection_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_json", value=rule_json, expected_type=type_hints["rule_json"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument token_domains", value=token_domains, expected_type=type_hints["token_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "scope": scope,
            "visibility_config": visibility_config,
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
        if association_config is not None:
            self._values["association_config"] = association_config
        if captcha_config is not None:
            self._values["captcha_config"] = captcha_config
        if challenge_config is not None:
            self._values["challenge_config"] = challenge_config
        if custom_response_body is not None:
            self._values["custom_response_body"] = custom_response_body
        if data_protection_config is not None:
            self._values["data_protection_config"] = data_protection_config
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if region is not None:
            self._values["region"] = region
        if rule is not None:
            self._values["rule"] = rule
        if rule_json is not None:
            self._values["rule_json"] = rule_json
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if token_domains is not None:
            self._values["token_domains"] = token_domains

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
    def default_action(self) -> "Wafv2WebAclDefaultAction":
        '''default_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#default_action Wafv2WebAcl#default_action}
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast("Wafv2WebAclDefaultAction", result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#scope Wafv2WebAcl#scope}.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def visibility_config(self) -> "Wafv2WebAclVisibilityConfig":
        '''visibility_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#visibility_config Wafv2WebAcl#visibility_config}
        '''
        result = self._values.get("visibility_config")
        assert result is not None, "Required property 'visibility_config' is missing"
        return typing.cast("Wafv2WebAclVisibilityConfig", result)

    @builtins.property
    def association_config(self) -> typing.Optional[Wafv2WebAclAssociationConfig]:
        '''association_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#association_config Wafv2WebAcl#association_config}
        '''
        result = self._values.get("association_config")
        return typing.cast(typing.Optional[Wafv2WebAclAssociationConfig], result)

    @builtins.property
    def captcha_config(self) -> typing.Optional[Wafv2WebAclCaptchaConfig]:
        '''captcha_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha_config Wafv2WebAcl#captcha_config}
        '''
        result = self._values.get("captcha_config")
        return typing.cast(typing.Optional[Wafv2WebAclCaptchaConfig], result)

    @builtins.property
    def challenge_config(self) -> typing.Optional[Wafv2WebAclChallengeConfig]:
        '''challenge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge_config Wafv2WebAcl#challenge_config}
        '''
        result = self._values.get("challenge_config")
        return typing.cast(typing.Optional[Wafv2WebAclChallengeConfig], result)

    @builtins.property
    def custom_response_body(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclCustomResponseBody"]]]:
        '''custom_response_body block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body Wafv2WebAcl#custom_response_body}
        '''
        result = self._values.get("custom_response_body")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclCustomResponseBody"]]], result)

    @builtins.property
    def data_protection_config(
        self,
    ) -> typing.Optional["Wafv2WebAclDataProtectionConfig"]:
        '''data_protection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#data_protection_config Wafv2WebAcl#data_protection_config}
        '''
        result = self._values.get("data_protection_config")
        return typing.cast(typing.Optional["Wafv2WebAclDataProtectionConfig"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#description Wafv2WebAcl#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#id Wafv2WebAcl#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name_prefix Wafv2WebAcl#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#region Wafv2WebAcl#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule Wafv2WebAcl#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRule"]]], result)

    @builtins.property
    def rule_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule_json Wafv2WebAcl#rule_json}.'''
        result = self._values.get("rule_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#tags Wafv2WebAcl#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#tags_all Wafv2WebAcl#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def token_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#token_domains Wafv2WebAcl#token_domains}.'''
        result = self._values.get("token_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCustomResponseBody",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "content_type": "contentType", "key": "key"},
)
class Wafv2WebAclCustomResponseBody:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: builtins.str,
        key: builtins.str,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#content Wafv2WebAcl#content}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#content_type Wafv2WebAcl#content_type}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#key Wafv2WebAcl#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27031c2bbace2dbc7e68ca55f928a415dd19df0141062319262db824065cfedf)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "content_type": content_type,
            "key": key,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#content Wafv2WebAcl#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#content_type Wafv2WebAcl#content_type}.'''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#key Wafv2WebAcl#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclCustomResponseBody(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclCustomResponseBodyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCustomResponseBodyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75d0e599d5588c7247a00fc559fae9d4eaae958dbb2f16ff3a3432105706ecdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "Wafv2WebAclCustomResponseBodyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47322b1b1540f42cd572573bbb3b9b07d589d6b7242758678620e3cf7d7d17a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclCustomResponseBodyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7666c167522d45e6f7764eeb81527e01ac901177d4d65fd1873378d6ef6049eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a9e07ad9edecc9929f5912dcc53bb2a918821ffa27ace7026466bc04e3cf15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__721f74eb2d25f839a2836e2f09329d774cd54f9e3be4df6918f638fb75f82f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclCustomResponseBody]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclCustomResponseBody]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclCustomResponseBody]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0921c44b654ddcbbf7a78a96e9253da3aff86fa9b8a8a468866ed122c104e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclCustomResponseBodyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclCustomResponseBodyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d3e873a142452de1effcdeab5243f4a697466e77774bfc7a469c8a9a4cca8b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e866926df9b4ce5a6bdb1bb0b846425f7e4ae1884566dd3ce087f4083a2fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebcb086313c8387fed11fcd0307459f8dfe18f9c8b98b8edc120bca513aaf3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0dac2077c65e8926b4957a3a74d346ee3ad00ba0292641af1a89c337fee144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclCustomResponseBody]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclCustomResponseBody]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclCustomResponseBody]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4990e95360f7159ecbc93f9bb59aea39a8f23890f637398d18130c676d1548cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfig",
    jsii_struct_bases=[],
    name_mapping={"data_protection": "dataProtection"},
)
class Wafv2WebAclDataProtectionConfig:
    def __init__(
        self,
        *,
        data_protection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclDataProtectionConfigDataProtection", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_protection: data_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#data_protection Wafv2WebAcl#data_protection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65536503bea380ff2aed83e16147551d1b1facde9b07868366899254bea55817)
            check_type(argname="argument data_protection", value=data_protection, expected_type=type_hints["data_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_protection is not None:
            self._values["data_protection"] = data_protection

    @builtins.property
    def data_protection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDataProtectionConfigDataProtection"]]]:
        '''data_protection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#data_protection Wafv2WebAcl#data_protection}
        '''
        result = self._values.get("data_protection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDataProtectionConfigDataProtection"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDataProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfigDataProtection",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "field": "field",
        "exclude_rate_based_details": "excludeRateBasedDetails",
        "exclude_rule_match_details": "excludeRuleMatchDetails",
    },
)
class Wafv2WebAclDataProtectionConfigDataProtection:
    def __init__(
        self,
        *,
        action: builtins.str,
        field: typing.Union["Wafv2WebAclDataProtectionConfigDataProtectionField", typing.Dict[builtins.str, typing.Any]],
        exclude_rate_based_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_rule_match_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#action Wafv2WebAcl#action}.
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field Wafv2WebAcl#field}
        :param exclude_rate_based_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#exclude_rate_based_details Wafv2WebAcl#exclude_rate_based_details}.
        :param exclude_rule_match_details: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#exclude_rule_match_details Wafv2WebAcl#exclude_rule_match_details}.
        '''
        if isinstance(field, dict):
            field = Wafv2WebAclDataProtectionConfigDataProtectionField(**field)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce46cda844236ff719951f5b0d75d668e8fdb8f0d8d38d88cba03ec357bb5f49)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument exclude_rate_based_details", value=exclude_rate_based_details, expected_type=type_hints["exclude_rate_based_details"])
            check_type(argname="argument exclude_rule_match_details", value=exclude_rule_match_details, expected_type=type_hints["exclude_rule_match_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "field": field,
        }
        if exclude_rate_based_details is not None:
            self._values["exclude_rate_based_details"] = exclude_rate_based_details
        if exclude_rule_match_details is not None:
            self._values["exclude_rule_match_details"] = exclude_rule_match_details

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#action Wafv2WebAcl#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field(self) -> "Wafv2WebAclDataProtectionConfigDataProtectionField":
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field Wafv2WebAcl#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast("Wafv2WebAclDataProtectionConfigDataProtectionField", result)

    @builtins.property
    def exclude_rate_based_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#exclude_rate_based_details Wafv2WebAcl#exclude_rate_based_details}.'''
        result = self._values.get("exclude_rate_based_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_rule_match_details(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#exclude_rule_match_details Wafv2WebAcl#exclude_rule_match_details}.'''
        result = self._values.get("exclude_rule_match_details")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDataProtectionConfigDataProtection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfigDataProtectionField",
    jsii_struct_bases=[],
    name_mapping={"field_type": "fieldType", "field_keys": "fieldKeys"},
)
class Wafv2WebAclDataProtectionConfigDataProtectionField:
    def __init__(
        self,
        *,
        field_type: builtins.str,
        field_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param field_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field_type Wafv2WebAcl#field_type}.
        :param field_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field_keys Wafv2WebAcl#field_keys}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82f1840ef69d637b4e3a7a063d4cdbb828ac1d21b9055a4f4200f1aa779e482)
            check_type(argname="argument field_type", value=field_type, expected_type=type_hints["field_type"])
            check_type(argname="argument field_keys", value=field_keys, expected_type=type_hints["field_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_type": field_type,
        }
        if field_keys is not None:
            self._values["field_keys"] = field_keys

    @builtins.property
    def field_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field_type Wafv2WebAcl#field_type}.'''
        result = self._values.get("field_type")
        assert result is not None, "Required property 'field_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field_keys Wafv2WebAcl#field_keys}.'''
        result = self._values.get("field_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDataProtectionConfigDataProtectionField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclDataProtectionConfigDataProtectionFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfigDataProtectionFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3210d5f51a5528ec15c7dd4d290159eb5400420cc92ffd46c0e3fda9486b57af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFieldKeys")
    def reset_field_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldKeys", []))

    @builtins.property
    @jsii.member(jsii_name="fieldKeysInput")
    def field_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fieldKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldTypeInput")
    def field_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldKeys")
    def field_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fieldKeys"))

    @field_keys.setter
    def field_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562190e77b0c6889c594c85337726641e9d360c1dee1f52361815d3986e209f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldType")
    def field_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldType"))

    @field_type.setter
    def field_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f90940fe02febae6fc052734d2f89f0113dc2276aea1505fc72af93be2d3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclDataProtectionConfigDataProtectionField]:
        return typing.cast(typing.Optional[Wafv2WebAclDataProtectionConfigDataProtectionField], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclDataProtectionConfigDataProtectionField],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5859b8b682f3c4ccbeba73940e55d63b4181cef7d9e833ee963c159b0c67f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDataProtectionConfigDataProtectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfigDataProtectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66c5297f38a3a2118239c74a84733d8f5f0cd2e39e59ff2c1b98287ce273aa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclDataProtectionConfigDataProtectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd59f8b8b46aaf019252458824b2dee6a529cc6dd890d0d7567fe0098e18df9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclDataProtectionConfigDataProtectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c208f341d962cdb173a0c42ebc813d6edf044bcbf32bdf0b26c8040cbc683c7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d7bf67a39fe682085c700c05af8598fac6b207815c2ccd559ca70d9d09e6995)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e9e438f958be9d5c76ed1915f5d335cb652df13ad9b5b93f9c3ee4e8652df5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDataProtectionConfigDataProtection]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDataProtectionConfigDataProtection]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDataProtectionConfigDataProtection]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47bc084278c559df7fb8e987b4e71ab00c08efa487b66f3466d16373df92b5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDataProtectionConfigDataProtectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfigDataProtectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e13d6d54b5bf066b58d949494f559737c31652e2df2bef6ae05baac3561626b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putField")
    def put_field(
        self,
        *,
        field_type: builtins.str,
        field_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param field_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field_type Wafv2WebAcl#field_type}.
        :param field_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#field_keys Wafv2WebAcl#field_keys}.
        '''
        value = Wafv2WebAclDataProtectionConfigDataProtectionField(
            field_type=field_type, field_keys=field_keys
        )

        return typing.cast(None, jsii.invoke(self, "putField", [value]))

    @jsii.member(jsii_name="resetExcludeRateBasedDetails")
    def reset_exclude_rate_based_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeRateBasedDetails", []))

    @jsii.member(jsii_name="resetExcludeRuleMatchDetails")
    def reset_exclude_rule_match_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeRuleMatchDetails", []))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(
        self,
    ) -> Wafv2WebAclDataProtectionConfigDataProtectionFieldOutputReference:
        return typing.cast(Wafv2WebAclDataProtectionConfigDataProtectionFieldOutputReference, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeRateBasedDetailsInput")
    def exclude_rate_based_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeRateBasedDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeRuleMatchDetailsInput")
    def exclude_rule_match_details_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeRuleMatchDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[Wafv2WebAclDataProtectionConfigDataProtectionField]:
        return typing.cast(typing.Optional[Wafv2WebAclDataProtectionConfigDataProtectionField], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b7a403199b5de9ce16c1ba74cae791e27a825952b2f9291344fab3a757827f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeRateBasedDetails")
    def exclude_rate_based_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeRateBasedDetails"))

    @exclude_rate_based_details.setter
    def exclude_rate_based_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5307d63de19a8eae6be6f28daee6af012ee3f012960fe3f2442b9a9e841f3e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeRateBasedDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeRuleMatchDetails")
    def exclude_rule_match_details(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeRuleMatchDetails"))

    @exclude_rule_match_details.setter
    def exclude_rule_match_details(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a24fad030424084b072a0c5e6cee9a3ccbe8275542801af1576469c8c77d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeRuleMatchDetails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDataProtectionConfigDataProtection]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDataProtectionConfigDataProtection]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDataProtectionConfigDataProtection]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f0132970950a8363c6a43dbf86b2cde8b0ffff20dd9acc81d3b16149d0091c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDataProtectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDataProtectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c30b8eeb5038f87faad9a0aa8c8a34cafbc238204f71fae416d72db138ece2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataProtection")
    def put_data_protection(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDataProtectionConfigDataProtection, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a6a39d84713a8880a06c800922f08dd40b577fcf94c4462710c2edb5657939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataProtection", [value]))

    @jsii.member(jsii_name="resetDataProtection")
    def reset_data_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtection", []))

    @builtins.property
    @jsii.member(jsii_name="dataProtection")
    def data_protection(self) -> Wafv2WebAclDataProtectionConfigDataProtectionList:
        return typing.cast(Wafv2WebAclDataProtectionConfigDataProtectionList, jsii.get(self, "dataProtection"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionInput")
    def data_protection_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDataProtectionConfigDataProtection]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDataProtectionConfigDataProtection]]], jsii.get(self, "dataProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclDataProtectionConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclDataProtectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclDataProtectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eff751257c2bb55e4a295add897e9b0bbb4e1b02610aec3141292e66fedb031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultAction",
    jsii_struct_bases=[],
    name_mapping={"allow": "allow", "block": "block"},
)
class Wafv2WebAclDefaultAction:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union["Wafv2WebAclDefaultActionAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        block: typing.Optional[typing.Union["Wafv2WebAclDefaultActionBlock", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#allow Wafv2WebAcl#allow}
        :param block: block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#block Wafv2WebAcl#block}
        '''
        if isinstance(allow, dict):
            allow = Wafv2WebAclDefaultActionAllow(**allow)
        if isinstance(block, dict):
            block = Wafv2WebAclDefaultActionBlock(**block)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4a58b7a138a69876a24d6b0ff3770c1d0b7cda15e70b072707781f01c7126c)
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument block", value=block, expected_type=type_hints["block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow is not None:
            self._values["allow"] = allow
        if block is not None:
            self._values["block"] = block

    @builtins.property
    def allow(self) -> typing.Optional["Wafv2WebAclDefaultActionAllow"]:
        '''allow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#allow Wafv2WebAcl#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional["Wafv2WebAclDefaultActionAllow"], result)

    @builtins.property
    def block(self) -> typing.Optional["Wafv2WebAclDefaultActionBlock"]:
        '''block block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#block Wafv2WebAcl#block}
        '''
        result = self._values.get("block")
        return typing.cast(typing.Optional["Wafv2WebAclDefaultActionBlock"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllow",
    jsii_struct_bases=[],
    name_mapping={"custom_request_handling": "customRequestHandling"},
)
class Wafv2WebAclDefaultActionAllow:
    def __init__(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union["Wafv2WebAclDefaultActionAllowCustomRequestHandling", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        if isinstance(custom_request_handling, dict):
            custom_request_handling = Wafv2WebAclDefaultActionAllowCustomRequestHandling(**custom_request_handling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af86cfc41cc8ef145d6041671d5594b3d4f622728a8192d52933f8e41df48291)
            check_type(argname="argument custom_request_handling", value=custom_request_handling, expected_type=type_hints["custom_request_handling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_request_handling is not None:
            self._values["custom_request_handling"] = custom_request_handling

    @builtins.property
    def custom_request_handling(
        self,
    ) -> typing.Optional["Wafv2WebAclDefaultActionAllowCustomRequestHandling"]:
        '''custom_request_handling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        result = self._values.get("custom_request_handling")
        return typing.cast(typing.Optional["Wafv2WebAclDefaultActionAllowCustomRequestHandling"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultActionAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllowCustomRequestHandling",
    jsii_struct_bases=[],
    name_mapping={"insert_header": "insertHeader"},
)
class Wafv2WebAclDefaultActionAllowCustomRequestHandling:
    def __init__(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bf2a7dc57bff17a290ad6de2a5e1c2a40fa52c433b432ee2e589016554692b)
            check_type(argname="argument insert_header", value=insert_header, expected_type=type_hints["insert_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insert_header": insert_header,
        }

    @builtins.property
    def insert_header(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader"]]:
        '''insert_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        result = self._values.get("insert_header")
        assert result is not None, "Required property 'insert_header' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultActionAllowCustomRequestHandling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cd4756099f26c0ae026786b0bc9637bca6e82b0bda1594aa7e270904d217f6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2e1b764dc4228642a05f8afa0569854d42e91049b52d80d966c0afc0862c26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50abf5f9366698fde0ca6ec52f9e5880b4f390968b2888a69c9efd0b9cf8abe7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b265618589b584f7922ab5f08ac4426610ae96e9d15fb237149ebd951816af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24d11c348495aac2d67da831170bea9f8274f34923c2a2b5c87b97ddf56817ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96108dfda3c1087f91f7bc676da2582b7e2d7546dcb0d451f1916336a72fc823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eedd661be75b2988bdbc723e5466506eed8d23511218032926506d6242d8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__056821d4665a3e16bcf5cb505c8c683ca65a79e85eea48db036903ef20872ad1)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055e58f9316452609b9140ea1145a17f034ff88e92b797e4748fe950f6a0548d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73cdb3fe6a3e25a707a395f2a1eae384303ab309e6a82df23fc234bffb246be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3b0aa992ab75a4820b4212c2edacb36a9eabc58f5a7822550b52583415daa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDefaultActionAllowCustomRequestHandlingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllowCustomRequestHandlingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e19e1b66b0583a254e845638cea52b0398266a40ad2fa29031b0204a85c2b8f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInsertHeader")
    def put_insert_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a2268f0faf31826ba7b2c8cfb4b8f9b3066df06d415304b8cf7ee87b88ebd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInsertHeader", [value]))

    @builtins.property
    @jsii.member(jsii_name="insertHeader")
    def insert_header(
        self,
    ) -> Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderList:
        return typing.cast(Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderList, jsii.get(self, "insertHeader"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaderInput")
    def insert_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]], jsii.get(self, "insertHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclDefaultActionAllowCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionAllowCustomRequestHandling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclDefaultActionAllowCustomRequestHandling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47934563bc7ba2c96634ffa1b4386c7cc9e48f847d6b86da1c55854c4a7d6400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDefaultActionAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb2c3e20b51d160d575a8955846a368fe67037757c6ba770bcb753027d053123)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRequestHandling")
    def put_custom_request_handling(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        value = Wafv2WebAclDefaultActionAllowCustomRequestHandling(
            insert_header=insert_header
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRequestHandling", [value]))

    @jsii.member(jsii_name="resetCustomRequestHandling")
    def reset_custom_request_handling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRequestHandling", []))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandling")
    def custom_request_handling(
        self,
    ) -> Wafv2WebAclDefaultActionAllowCustomRequestHandlingOutputReference:
        return typing.cast(Wafv2WebAclDefaultActionAllowCustomRequestHandlingOutputReference, jsii.get(self, "customRequestHandling"))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandlingInput")
    def custom_request_handling_input(
        self,
    ) -> typing.Optional[Wafv2WebAclDefaultActionAllowCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionAllowCustomRequestHandling], jsii.get(self, "customRequestHandlingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclDefaultActionAllow]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionAllow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclDefaultActionAllow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4c1c41a9222c42870e598607635b019b4943b09e73f66d6bd48126681af6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlock",
    jsii_struct_bases=[],
    name_mapping={"custom_response": "customResponse"},
)
class Wafv2WebAclDefaultActionBlock:
    def __init__(
        self,
        *,
        custom_response: typing.Optional[typing.Union["Wafv2WebAclDefaultActionBlockCustomResponse", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_response: custom_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response Wafv2WebAcl#custom_response}
        '''
        if isinstance(custom_response, dict):
            custom_response = Wafv2WebAclDefaultActionBlockCustomResponse(**custom_response)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9077ac5ca0858b9bf08a98ab163b9d861cd5d6484340c2d214d7f56cefe75685)
            check_type(argname="argument custom_response", value=custom_response, expected_type=type_hints["custom_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_response is not None:
            self._values["custom_response"] = custom_response

    @builtins.property
    def custom_response(
        self,
    ) -> typing.Optional["Wafv2WebAclDefaultActionBlockCustomResponse"]:
        '''custom_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response Wafv2WebAcl#custom_response}
        '''
        result = self._values.get("custom_response")
        return typing.cast(typing.Optional["Wafv2WebAclDefaultActionBlockCustomResponse"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultActionBlock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlockCustomResponse",
    jsii_struct_bases=[],
    name_mapping={
        "response_code": "responseCode",
        "custom_response_body_key": "customResponseBodyKey",
        "response_header": "responseHeader",
    },
)
class Wafv2WebAclDefaultActionBlockCustomResponse:
    def __init__(
        self,
        *,
        response_code: jsii.Number,
        custom_response_body_key: typing.Optional[builtins.str] = None,
        response_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param response_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_code Wafv2WebAcl#response_code}.
        :param custom_response_body_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body_key Wafv2WebAcl#custom_response_body_key}.
        :param response_header: response_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_header Wafv2WebAcl#response_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccee0ab071048e311df083a47fc200282e3fa3f23fb79068d9a58c38e59f40f)
            check_type(argname="argument response_code", value=response_code, expected_type=type_hints["response_code"])
            check_type(argname="argument custom_response_body_key", value=custom_response_body_key, expected_type=type_hints["custom_response_body_key"])
            check_type(argname="argument response_header", value=response_header, expected_type=type_hints["response_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "response_code": response_code,
        }
        if custom_response_body_key is not None:
            self._values["custom_response_body_key"] = custom_response_body_key
        if response_header is not None:
            self._values["response_header"] = response_header

    @builtins.property
    def response_code(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_code Wafv2WebAcl#response_code}.'''
        result = self._values.get("response_code")
        assert result is not None, "Required property 'response_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def custom_response_body_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body_key Wafv2WebAcl#custom_response_body_key}.'''
        result = self._values.get("custom_response_body_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader"]]]:
        '''response_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_header Wafv2WebAcl#response_header}
        '''
        result = self._values.get("response_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultActionBlockCustomResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclDefaultActionBlockCustomResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlockCustomResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41be0f86f99286111bdce5504d1dd1751da69c8ef8e5dae4ee8926420d7bd7e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putResponseHeader")
    def put_response_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1190509cc63121d434f17e4ba92e78c025e51650c96863b440b82b86b29108f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeader", [value]))

    @jsii.member(jsii_name="resetCustomResponseBodyKey")
    def reset_custom_response_body_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomResponseBodyKey", []))

    @jsii.member(jsii_name="resetResponseHeader")
    def reset_response_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeader", []))

    @builtins.property
    @jsii.member(jsii_name="responseHeader")
    def response_header(
        self,
    ) -> "Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderList":
        return typing.cast("Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderList", jsii.get(self, "responseHeader"))

    @builtins.property
    @jsii.member(jsii_name="customResponseBodyKeyInput")
    def custom_response_body_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customResponseBodyKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCodeInput")
    def response_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "responseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderInput")
    def response_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader"]]], jsii.get(self, "responseHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="customResponseBodyKey")
    def custom_response_body_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customResponseBodyKey"))

    @custom_response_body_key.setter
    def custom_response_body_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671d78b83c516966ea3b9c6b6c2c9f44df0e13f6358a2b1c005cd5f065150db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customResponseBodyKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64eb204549ef3d4430c18b59ef76e3583299ef8cedb1af8c870f4e120e048cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclDefaultActionBlockCustomResponse]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionBlockCustomResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclDefaultActionBlockCustomResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c5a3f2c5ecd6afbc41d3c833cbd2e4c4a34effef9cc2020686b657f923ce62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df48ca27128d53ad157a7713ad567078d8ad9599916ad6a43708c70ca459397f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52b4a786248ebf167165aad5edfc866d09ef7b966664df3db32dc01b2e313220)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176228f720436728fcf8ac96be11b265e2bdc8054d4dca2fd64ef20d3eba9583)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7d9f50ba3d40952e4021ed60f552ff9eff394e2700e7d8c1e8c935f355247c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13a9022e2a8fe15e3102051ad81c3f2ed9cbb7adf87ed39feee0ab8844cfe16a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b79ea437b76d99d683e3efbe9a2ff3f68cda8765648ed2b7774565d853900c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf5ef509fe8731c5f932ac975f76a5aad10bc90a6189f2829e4830bff95af52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a59fa116648e776d0d1bf28734d3cfacb3b5529d479422d2dc26b3a63e14c8)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79183a152dcff2e5dddf7d46a26553e9bba11e6eaa4ede0ae208c1e6b43049ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf3dc7fd0a1f6b36db979a74d2d0aa0ea1aaf799cd18cceb75eb599bc653b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd85cef8ec9d535aaa13a50f657171c9998c6903369ed99f5737ff946c3b9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDefaultActionBlockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionBlockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f448e6d4151e5673f276513ba0f97ddd43d14004c06435da363b6f0fa5a7ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomResponse")
    def put_custom_response(
        self,
        *,
        response_code: jsii.Number,
        custom_response_body_key: typing.Optional[builtins.str] = None,
        response_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param response_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_code Wafv2WebAcl#response_code}.
        :param custom_response_body_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body_key Wafv2WebAcl#custom_response_body_key}.
        :param response_header: response_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_header Wafv2WebAcl#response_header}
        '''
        value = Wafv2WebAclDefaultActionBlockCustomResponse(
            response_code=response_code,
            custom_response_body_key=custom_response_body_key,
            response_header=response_header,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomResponse", [value]))

    @jsii.member(jsii_name="resetCustomResponse")
    def reset_custom_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomResponse", []))

    @builtins.property
    @jsii.member(jsii_name="customResponse")
    def custom_response(
        self,
    ) -> Wafv2WebAclDefaultActionBlockCustomResponseOutputReference:
        return typing.cast(Wafv2WebAclDefaultActionBlockCustomResponseOutputReference, jsii.get(self, "customResponse"))

    @builtins.property
    @jsii.member(jsii_name="customResponseInput")
    def custom_response_input(
        self,
    ) -> typing.Optional[Wafv2WebAclDefaultActionBlockCustomResponse]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionBlockCustomResponse], jsii.get(self, "customResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclDefaultActionBlock]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionBlock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclDefaultActionBlock],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a926c7eafb04fd976961c7d1a72f81c3bf8338ca2ffd002bf5baa26d7a30c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclDefaultActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclDefaultActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32f843f9ea13b95ae863333fa142d908111a02a2461d0cc72284efce5ff3aa3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllow")
    def put_allow(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclDefaultActionAllowCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        value = Wafv2WebAclDefaultActionAllow(
            custom_request_handling=custom_request_handling
        )

        return typing.cast(None, jsii.invoke(self, "putAllow", [value]))

    @jsii.member(jsii_name="putBlock")
    def put_block(
        self,
        *,
        custom_response: typing.Optional[typing.Union[Wafv2WebAclDefaultActionBlockCustomResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_response: custom_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response Wafv2WebAcl#custom_response}
        '''
        value = Wafv2WebAclDefaultActionBlock(custom_response=custom_response)

        return typing.cast(None, jsii.invoke(self, "putBlock", [value]))

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetBlock")
    def reset_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlock", []))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> Wafv2WebAclDefaultActionAllowOutputReference:
        return typing.cast(Wafv2WebAclDefaultActionAllowOutputReference, jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="block")
    def block(self) -> Wafv2WebAclDefaultActionBlockOutputReference:
        return typing.cast(Wafv2WebAclDefaultActionBlockOutputReference, jsii.get(self, "block"))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(self) -> typing.Optional[Wafv2WebAclDefaultActionAllow]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionAllow], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="blockInput")
    def block_input(self) -> typing.Optional[Wafv2WebAclDefaultActionBlock]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultActionBlock], jsii.get(self, "blockInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclDefaultAction]:
        return typing.cast(typing.Optional[Wafv2WebAclDefaultAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[Wafv2WebAclDefaultAction]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1760e3c1c722ed4248d318089816e56d0c55fc9d1ba1fd067fed734c142a11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRule",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "priority": "priority",
        "visibility_config": "visibilityConfig",
        "action": "action",
        "captcha_config": "captchaConfig",
        "challenge_config": "challengeConfig",
        "override_action": "overrideAction",
        "rule_label": "ruleLabel",
        "statement": "statement",
    },
)
class Wafv2WebAclRule:
    def __init__(
        self,
        *,
        name: builtins.str,
        priority: jsii.Number,
        visibility_config: typing.Union["Wafv2WebAclRuleVisibilityConfig", typing.Dict[builtins.str, typing.Any]],
        action: typing.Optional[typing.Union["Wafv2WebAclRuleAction", typing.Dict[builtins.str, typing.Any]]] = None,
        captcha_config: typing.Optional[typing.Union["Wafv2WebAclRuleCaptchaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        challenge_config: typing.Optional[typing.Union["Wafv2WebAclRuleChallengeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        override_action: typing.Optional[typing.Union["Wafv2WebAclRuleOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleRuleLabel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        statement: typing.Any = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#priority Wafv2WebAcl#priority}.
        :param visibility_config: visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#visibility_config Wafv2WebAcl#visibility_config}
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#action Wafv2WebAcl#action}
        :param captcha_config: captcha_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha_config Wafv2WebAcl#captcha_config}
        :param challenge_config: challenge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge_config Wafv2WebAcl#challenge_config}
        :param override_action: override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#override_action Wafv2WebAcl#override_action}
        :param rule_label: rule_label block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule_label Wafv2WebAcl#rule_label}
        :param statement: statement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#statement Wafv2WebAcl#statement}
        '''
        if isinstance(visibility_config, dict):
            visibility_config = Wafv2WebAclRuleVisibilityConfig(**visibility_config)
        if isinstance(action, dict):
            action = Wafv2WebAclRuleAction(**action)
        if isinstance(captcha_config, dict):
            captcha_config = Wafv2WebAclRuleCaptchaConfig(**captcha_config)
        if isinstance(challenge_config, dict):
            challenge_config = Wafv2WebAclRuleChallengeConfig(**challenge_config)
        if isinstance(override_action, dict):
            override_action = Wafv2WebAclRuleOverrideAction(**override_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fe2b8063ea5f2d7c3585567705a86d100364548cee1202715ca67038f73c8f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument visibility_config", value=visibility_config, expected_type=type_hints["visibility_config"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument captcha_config", value=captcha_config, expected_type=type_hints["captcha_config"])
            check_type(argname="argument challenge_config", value=challenge_config, expected_type=type_hints["challenge_config"])
            check_type(argname="argument override_action", value=override_action, expected_type=type_hints["override_action"])
            check_type(argname="argument rule_label", value=rule_label, expected_type=type_hints["rule_label"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "priority": priority,
            "visibility_config": visibility_config,
        }
        if action is not None:
            self._values["action"] = action
        if captcha_config is not None:
            self._values["captcha_config"] = captcha_config
        if challenge_config is not None:
            self._values["challenge_config"] = challenge_config
        if override_action is not None:
            self._values["override_action"] = override_action
        if rule_label is not None:
            self._values["rule_label"] = rule_label
        if statement is not None:
            self._values["statement"] = statement

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#priority Wafv2WebAcl#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def visibility_config(self) -> "Wafv2WebAclRuleVisibilityConfig":
        '''visibility_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#visibility_config Wafv2WebAcl#visibility_config}
        '''
        result = self._values.get("visibility_config")
        assert result is not None, "Required property 'visibility_config' is missing"
        return typing.cast("Wafv2WebAclRuleVisibilityConfig", result)

    @builtins.property
    def action(self) -> typing.Optional["Wafv2WebAclRuleAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#action Wafv2WebAcl#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["Wafv2WebAclRuleAction"], result)

    @builtins.property
    def captcha_config(self) -> typing.Optional["Wafv2WebAclRuleCaptchaConfig"]:
        '''captcha_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha_config Wafv2WebAcl#captcha_config}
        '''
        result = self._values.get("captcha_config")
        return typing.cast(typing.Optional["Wafv2WebAclRuleCaptchaConfig"], result)

    @builtins.property
    def challenge_config(self) -> typing.Optional["Wafv2WebAclRuleChallengeConfig"]:
        '''challenge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge_config Wafv2WebAcl#challenge_config}
        '''
        result = self._values.get("challenge_config")
        return typing.cast(typing.Optional["Wafv2WebAclRuleChallengeConfig"], result)

    @builtins.property
    def override_action(self) -> typing.Optional["Wafv2WebAclRuleOverrideAction"]:
        '''override_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#override_action Wafv2WebAcl#override_action}
        '''
        result = self._values.get("override_action")
        return typing.cast(typing.Optional["Wafv2WebAclRuleOverrideAction"], result)

    @builtins.property
    def rule_label(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleRuleLabel"]]]:
        '''rule_label block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#rule_label Wafv2WebAcl#rule_label}
        '''
        result = self._values.get("rule_label")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleRuleLabel"]]], result)

    @builtins.property
    def statement(self) -> typing.Any:
        '''statement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#statement Wafv2WebAcl#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleAction",
    jsii_struct_bases=[],
    name_mapping={
        "allow": "allow",
        "block": "block",
        "captcha": "captcha",
        "challenge": "challenge",
        "count": "count",
    },
)
class Wafv2WebAclRuleAction:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union["Wafv2WebAclRuleActionAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        block: typing.Optional[typing.Union["Wafv2WebAclRuleActionBlock", typing.Dict[builtins.str, typing.Any]]] = None,
        captcha: typing.Optional[typing.Union["Wafv2WebAclRuleActionCaptcha", typing.Dict[builtins.str, typing.Any]]] = None,
        challenge: typing.Optional[typing.Union["Wafv2WebAclRuleActionChallenge", typing.Dict[builtins.str, typing.Any]]] = None,
        count: typing.Optional[typing.Union["Wafv2WebAclRuleActionCount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#allow Wafv2WebAcl#allow}
        :param block: block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#block Wafv2WebAcl#block}
        :param captcha: captcha block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha Wafv2WebAcl#captcha}
        :param challenge: challenge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge Wafv2WebAcl#challenge}
        :param count: count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#count Wafv2WebAcl#count}
        '''
        if isinstance(allow, dict):
            allow = Wafv2WebAclRuleActionAllow(**allow)
        if isinstance(block, dict):
            block = Wafv2WebAclRuleActionBlock(**block)
        if isinstance(captcha, dict):
            captcha = Wafv2WebAclRuleActionCaptcha(**captcha)
        if isinstance(challenge, dict):
            challenge = Wafv2WebAclRuleActionChallenge(**challenge)
        if isinstance(count, dict):
            count = Wafv2WebAclRuleActionCount(**count)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89721362d6d591d68d8ff0b68aeca965263bac4a908015f996997d24bb253f53)
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument block", value=block, expected_type=type_hints["block"])
            check_type(argname="argument captcha", value=captcha, expected_type=type_hints["captcha"])
            check_type(argname="argument challenge", value=challenge, expected_type=type_hints["challenge"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow is not None:
            self._values["allow"] = allow
        if block is not None:
            self._values["block"] = block
        if captcha is not None:
            self._values["captcha"] = captcha
        if challenge is not None:
            self._values["challenge"] = challenge
        if count is not None:
            self._values["count"] = count

    @builtins.property
    def allow(self) -> typing.Optional["Wafv2WebAclRuleActionAllow"]:
        '''allow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#allow Wafv2WebAcl#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionAllow"], result)

    @builtins.property
    def block(self) -> typing.Optional["Wafv2WebAclRuleActionBlock"]:
        '''block block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#block Wafv2WebAcl#block}
        '''
        result = self._values.get("block")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionBlock"], result)

    @builtins.property
    def captcha(self) -> typing.Optional["Wafv2WebAclRuleActionCaptcha"]:
        '''captcha block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha Wafv2WebAcl#captcha}
        '''
        result = self._values.get("captcha")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionCaptcha"], result)

    @builtins.property
    def challenge(self) -> typing.Optional["Wafv2WebAclRuleActionChallenge"]:
        '''challenge block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge Wafv2WebAcl#challenge}
        '''
        result = self._values.get("challenge")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionChallenge"], result)

    @builtins.property
    def count(self) -> typing.Optional["Wafv2WebAclRuleActionCount"]:
        '''count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#count Wafv2WebAcl#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionCount"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllow",
    jsii_struct_bases=[],
    name_mapping={"custom_request_handling": "customRequestHandling"},
)
class Wafv2WebAclRuleActionAllow:
    def __init__(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union["Wafv2WebAclRuleActionAllowCustomRequestHandling", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        if isinstance(custom_request_handling, dict):
            custom_request_handling = Wafv2WebAclRuleActionAllowCustomRequestHandling(**custom_request_handling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5cc2fc7cbcfbbfe97ae25f7b501a04189b75d4e9fa3d92f36d1c8726d22824)
            check_type(argname="argument custom_request_handling", value=custom_request_handling, expected_type=type_hints["custom_request_handling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_request_handling is not None:
            self._values["custom_request_handling"] = custom_request_handling

    @builtins.property
    def custom_request_handling(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleActionAllowCustomRequestHandling"]:
        '''custom_request_handling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        result = self._values.get("custom_request_handling")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionAllowCustomRequestHandling"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllowCustomRequestHandling",
    jsii_struct_bases=[],
    name_mapping={"insert_header": "insertHeader"},
)
class Wafv2WebAclRuleActionAllowCustomRequestHandling:
    def __init__(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee4329a8d53bf4a9d4eab6affc8cf1be53c7019a80b55ba5b0f494bbe69acb9)
            check_type(argname="argument insert_header", value=insert_header, expected_type=type_hints["insert_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insert_header": insert_header,
        }

    @builtins.property
    def insert_header(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader"]]:
        '''insert_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        result = self._values.get("insert_header")
        assert result is not None, "Required property 'insert_header' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionAllowCustomRequestHandling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c79db5986ce2b026bfefc5a00516737006bfcd864cdc617e6d3427cf160cd0a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__566297cb25407a21410a4ea34b72a5aaaaea8ae4a8db7ebcfed75d111f89892a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e8ab5401ef71d4d9473c082e6d617f14964a7e50b7bd51631f78d0cea494de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e92317a0e0f4c4551796b62df4705f15a8ec5678c9b33a6f0c3209e77be442)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a31a8c0016ddd74f8189320f3e7a7d88ba297644596f30869d9a1b86320ad1a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a5eb6de56f4a437271ce3aa21c2321c2bb31f228965cd6915b709477c2d8e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ac2601961d2bd0b7296d4b288ced3c54f730019fb13f5bd333d0e46027e5ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d8e53b99e5ec759091b847b7c4e58d39ba2ff50323020dd0076dfd50c72025d)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05935057e53dbe336f44ed5f1b1a169f8df19a4df078b38add94b877a24b1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdbd48ce2a769e3ecabf076f3bd938762f7e88ee2d109106ada04485d3ec50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123e751c630edb4be6735aa02389ae50474e730321c3f67b5d367a92daa86040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionAllowCustomRequestHandlingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllowCustomRequestHandlingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb0945e5c95998737f2e89ace96b17510549afa5f26cdfe3a350af6104d64a52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInsertHeader")
    def put_insert_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e22700d0a93db74337a660ed266f4d2637728ed326ebc15ca3d1129a07a927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInsertHeader", [value]))

    @builtins.property
    @jsii.member(jsii_name="insertHeader")
    def insert_header(
        self,
    ) -> Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderList:
        return typing.cast(Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderList, jsii.get(self, "insertHeader"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaderInput")
    def insert_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]], jsii.get(self, "insertHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionAllowCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionAllowCustomRequestHandling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionAllowCustomRequestHandling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54227397dd44db8d64eef809b7c9c3d01df20104736c32db91a70938c9481ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__536306b6380dbd8413dbd10779be9514f5d8ba7b699d6bf69e46cd7e92e2a20a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRequestHandling")
    def put_custom_request_handling(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        value = Wafv2WebAclRuleActionAllowCustomRequestHandling(
            insert_header=insert_header
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRequestHandling", [value]))

    @jsii.member(jsii_name="resetCustomRequestHandling")
    def reset_custom_request_handling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRequestHandling", []))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandling")
    def custom_request_handling(
        self,
    ) -> Wafv2WebAclRuleActionAllowCustomRequestHandlingOutputReference:
        return typing.cast(Wafv2WebAclRuleActionAllowCustomRequestHandlingOutputReference, jsii.get(self, "customRequestHandling"))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandlingInput")
    def custom_request_handling_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionAllowCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionAllowCustomRequestHandling], jsii.get(self, "customRequestHandlingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleActionAllow]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionAllow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionAllow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d771952097d71104cef5b969b247bdf7141b25249b30cb9b6ac3ab3546e8f2a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlock",
    jsii_struct_bases=[],
    name_mapping={"custom_response": "customResponse"},
)
class Wafv2WebAclRuleActionBlock:
    def __init__(
        self,
        *,
        custom_response: typing.Optional[typing.Union["Wafv2WebAclRuleActionBlockCustomResponse", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_response: custom_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response Wafv2WebAcl#custom_response}
        '''
        if isinstance(custom_response, dict):
            custom_response = Wafv2WebAclRuleActionBlockCustomResponse(**custom_response)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f458f2a2f01072567fc6273e9e503884397f77d6689be6af3f294b16cf6ef397)
            check_type(argname="argument custom_response", value=custom_response, expected_type=type_hints["custom_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_response is not None:
            self._values["custom_response"] = custom_response

    @builtins.property
    def custom_response(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleActionBlockCustomResponse"]:
        '''custom_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response Wafv2WebAcl#custom_response}
        '''
        result = self._values.get("custom_response")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionBlockCustomResponse"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionBlock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlockCustomResponse",
    jsii_struct_bases=[],
    name_mapping={
        "response_code": "responseCode",
        "custom_response_body_key": "customResponseBodyKey",
        "response_header": "responseHeader",
    },
)
class Wafv2WebAclRuleActionBlockCustomResponse:
    def __init__(
        self,
        *,
        response_code: jsii.Number,
        custom_response_body_key: typing.Optional[builtins.str] = None,
        response_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleActionBlockCustomResponseResponseHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param response_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_code Wafv2WebAcl#response_code}.
        :param custom_response_body_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body_key Wafv2WebAcl#custom_response_body_key}.
        :param response_header: response_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_header Wafv2WebAcl#response_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98c39088889cf991f3c1cf14fc6b3010743e0e98238ead317acbc869fbcce96)
            check_type(argname="argument response_code", value=response_code, expected_type=type_hints["response_code"])
            check_type(argname="argument custom_response_body_key", value=custom_response_body_key, expected_type=type_hints["custom_response_body_key"])
            check_type(argname="argument response_header", value=response_header, expected_type=type_hints["response_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "response_code": response_code,
        }
        if custom_response_body_key is not None:
            self._values["custom_response_body_key"] = custom_response_body_key
        if response_header is not None:
            self._values["response_header"] = response_header

    @builtins.property
    def response_code(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_code Wafv2WebAcl#response_code}.'''
        result = self._values.get("response_code")
        assert result is not None, "Required property 'response_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def custom_response_body_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body_key Wafv2WebAcl#custom_response_body_key}.'''
        result = self._values.get("custom_response_body_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionBlockCustomResponseResponseHeader"]]]:
        '''response_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_header Wafv2WebAcl#response_header}
        '''
        result = self._values.get("response_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionBlockCustomResponseResponseHeader"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionBlockCustomResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleActionBlockCustomResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlockCustomResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4098b617c595c91483d8bb456a3c3fb523c1c127cc51bbe367f84dd09dfa8cbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putResponseHeader")
    def put_response_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleActionBlockCustomResponseResponseHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b52fc09347e0f7d85ce3e66190a73c3c3beba0029f0a458c5c20ef24cd4de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeader", [value]))

    @jsii.member(jsii_name="resetCustomResponseBodyKey")
    def reset_custom_response_body_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomResponseBodyKey", []))

    @jsii.member(jsii_name="resetResponseHeader")
    def reset_response_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeader", []))

    @builtins.property
    @jsii.member(jsii_name="responseHeader")
    def response_header(
        self,
    ) -> "Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderList":
        return typing.cast("Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderList", jsii.get(self, "responseHeader"))

    @builtins.property
    @jsii.member(jsii_name="customResponseBodyKeyInput")
    def custom_response_body_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customResponseBodyKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCodeInput")
    def response_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "responseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderInput")
    def response_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionBlockCustomResponseResponseHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionBlockCustomResponseResponseHeader"]]], jsii.get(self, "responseHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="customResponseBodyKey")
    def custom_response_body_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customResponseBodyKey"))

    @custom_response_body_key.setter
    def custom_response_body_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903ce2aba843ad33024de13915f42ec3fb2c7c4803fc5a7b82920743f06a3bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customResponseBodyKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fb6da3c39e3d1d7c27eb7e4638a87fc75d37683b56b6c7a63dc9214e06c415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionBlockCustomResponse]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionBlockCustomResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionBlockCustomResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c970bfc1d7aaaf7ec0e04d5460bf55a8fed99060fdd0eff8b8aa8fdf8b63cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlockCustomResponseResponseHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclRuleActionBlockCustomResponseResponseHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4e9e926f3c80f3c9422e8c727c1b2383be0fbdbf60fbada4cf1a8412583cf7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionBlockCustomResponseResponseHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec937daf27159b3d0ddb913333720ad7af069a66ace9385f65f232481e2f014)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61105db2742fc304dcb444167141ecf2a77beee689033c86c94dcd05b7627d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8322fa545d19c462429d02249fc87efe0a7b0133cb61c884008a179f89a03897)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dc3d51e168d9c3b99dc0b8aa5488a8fdee8c1c630f400addc8e023961ab0d38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39293f59b712940b9e26179842aac8231b040c3d8967e4bf711e1891df7f66de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b943083a8a6052f5988d646a3dfff9e1d4cea725f6550dc8cb3b567b3792dd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a2196c183061ea846ee56bf1893d4d870ea0a10f98336f6289cdcafaa4b87d)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe479518a432cd296d00233657d4cca4e6e291903c539691c0ef6dde7b1020d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d9b53be249b0ccfc2b86a3d47605365cc10ae0b7236fe5a49e6732af8d1952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147bb6195249a443560bbec1ca8ebb1c5c411342c1fa2bd9ce95605ed4e1056b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionBlockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionBlockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77a5cba1f2f68cbc67c36be3c6b47aece966d279a46f475545e537de7d641dd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomResponse")
    def put_custom_response(
        self,
        *,
        response_code: jsii.Number,
        custom_response_body_key: typing.Optional[builtins.str] = None,
        response_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param response_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_code Wafv2WebAcl#response_code}.
        :param custom_response_body_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response_body_key Wafv2WebAcl#custom_response_body_key}.
        :param response_header: response_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#response_header Wafv2WebAcl#response_header}
        '''
        value = Wafv2WebAclRuleActionBlockCustomResponse(
            response_code=response_code,
            custom_response_body_key=custom_response_body_key,
            response_header=response_header,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomResponse", [value]))

    @jsii.member(jsii_name="resetCustomResponse")
    def reset_custom_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomResponse", []))

    @builtins.property
    @jsii.member(jsii_name="customResponse")
    def custom_response(
        self,
    ) -> Wafv2WebAclRuleActionBlockCustomResponseOutputReference:
        return typing.cast(Wafv2WebAclRuleActionBlockCustomResponseOutputReference, jsii.get(self, "customResponse"))

    @builtins.property
    @jsii.member(jsii_name="customResponseInput")
    def custom_response_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionBlockCustomResponse]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionBlockCustomResponse], jsii.get(self, "customResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleActionBlock]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionBlock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionBlock],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856ed8b300603e9f6968f627fa2a094141c29ed291d35a98de111f64220b0286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptcha",
    jsii_struct_bases=[],
    name_mapping={"custom_request_handling": "customRequestHandling"},
)
class Wafv2WebAclRuleActionCaptcha:
    def __init__(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union["Wafv2WebAclRuleActionCaptchaCustomRequestHandling", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        if isinstance(custom_request_handling, dict):
            custom_request_handling = Wafv2WebAclRuleActionCaptchaCustomRequestHandling(**custom_request_handling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271475f47888c6045fbee335616c8f0c18965c49729e10f449ca5ac42adbae2b)
            check_type(argname="argument custom_request_handling", value=custom_request_handling, expected_type=type_hints["custom_request_handling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_request_handling is not None:
            self._values["custom_request_handling"] = custom_request_handling

    @builtins.property
    def custom_request_handling(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleActionCaptchaCustomRequestHandling"]:
        '''custom_request_handling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        result = self._values.get("custom_request_handling")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionCaptchaCustomRequestHandling"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionCaptcha(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptchaCustomRequestHandling",
    jsii_struct_bases=[],
    name_mapping={"insert_header": "insertHeader"},
)
class Wafv2WebAclRuleActionCaptchaCustomRequestHandling:
    def __init__(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b706967092b79dafe1837be0d391f981d7b628314cb8fa76981b92c823b99d)
            check_type(argname="argument insert_header", value=insert_header, expected_type=type_hints["insert_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insert_header": insert_header,
        }

    @builtins.property
    def insert_header(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader"]]:
        '''insert_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        result = self._values.get("insert_header")
        assert result is not None, "Required property 'insert_header' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionCaptchaCustomRequestHandling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d951557f40bdb6d5080cd74a7665de0a6ff1b6e2b2955f6911608a8b834368f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79081d342625849893aa2380e9e07db0c615795225eab0c5dd8af5568101338)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299cdc2eb48b549ee0d833e04c1b096db358ca31857107cb8f8764ba64a22393)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c116f1b35d547269a5f25af233f4b0e86101093fd7b4ce9b14153e1d3eb08eac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d18e0a864d831bccbb82ea8fcf9798fdca0684d80a4df582fe4d4e736158e18a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__383d25da294ee9e4d29d77e5ea6f463b34cc7051ef782de66bc146557e13d7e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4b78d48ad77298798cd6ec461c3f887c9301f6ce9eab2fd5baea55f723c280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__156645f1f2dad445da1ceb0348574c85dbc605c4722c520dcd7750ed7c75be79)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f784758953371a13a8f81a8c78274f8ca9f206742eab5a01f324a90e32f913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49167a91cf93a3a7b1858618e7eb1f889fd0a56f0842001549a09cde7bda6218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200aeec50ed624a442bd810eac1945bb474fdd8e31915f351d1bc7a3c83af046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionCaptchaCustomRequestHandlingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptchaCustomRequestHandlingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__935c72b02c573fc40efe9a4df4c19ead64086c05f88d97d53a74a1fae1094825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInsertHeader")
    def put_insert_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ae18b76bac6aeb55f4e5ac982bb1efe6917be8ff54958136065a240e0be09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInsertHeader", [value]))

    @builtins.property
    @jsii.member(jsii_name="insertHeader")
    def insert_header(
        self,
    ) -> Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderList:
        return typing.cast(Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderList, jsii.get(self, "insertHeader"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaderInput")
    def insert_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]], jsii.get(self, "insertHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionCaptchaCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCaptchaCustomRequestHandling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionCaptchaCustomRequestHandling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2503777da66375c813b0d4def8084ab8132d83d09afad17f6134fe2873fd62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionCaptchaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCaptchaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__376443ad441882123fccbfb375d73331dabd389e2ef317e4341b4bc4b1196418)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRequestHandling")
    def put_custom_request_handling(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        value = Wafv2WebAclRuleActionCaptchaCustomRequestHandling(
            insert_header=insert_header
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRequestHandling", [value]))

    @jsii.member(jsii_name="resetCustomRequestHandling")
    def reset_custom_request_handling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRequestHandling", []))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandling")
    def custom_request_handling(
        self,
    ) -> Wafv2WebAclRuleActionCaptchaCustomRequestHandlingOutputReference:
        return typing.cast(Wafv2WebAclRuleActionCaptchaCustomRequestHandlingOutputReference, jsii.get(self, "customRequestHandling"))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandlingInput")
    def custom_request_handling_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionCaptchaCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCaptchaCustomRequestHandling], jsii.get(self, "customRequestHandlingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleActionCaptcha]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCaptcha], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionCaptcha],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67810f2752b373cdd0cd9b701b3363816ca16131cae47920b00ba28d19ace581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallenge",
    jsii_struct_bases=[],
    name_mapping={"custom_request_handling": "customRequestHandling"},
)
class Wafv2WebAclRuleActionChallenge:
    def __init__(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union["Wafv2WebAclRuleActionChallengeCustomRequestHandling", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        if isinstance(custom_request_handling, dict):
            custom_request_handling = Wafv2WebAclRuleActionChallengeCustomRequestHandling(**custom_request_handling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5593fc33b2dfcaa0a0e5ebb288641cdb3826f59371b1182a78a524a716a781f5)
            check_type(argname="argument custom_request_handling", value=custom_request_handling, expected_type=type_hints["custom_request_handling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_request_handling is not None:
            self._values["custom_request_handling"] = custom_request_handling

    @builtins.property
    def custom_request_handling(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleActionChallengeCustomRequestHandling"]:
        '''custom_request_handling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        result = self._values.get("custom_request_handling")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionChallengeCustomRequestHandling"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionChallenge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallengeCustomRequestHandling",
    jsii_struct_bases=[],
    name_mapping={"insert_header": "insertHeader"},
)
class Wafv2WebAclRuleActionChallengeCustomRequestHandling:
    def __init__(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54b52ff882bd2bf164aa568da5f33abd839b52074676badb620d980b4c68da7)
            check_type(argname="argument insert_header", value=insert_header, expected_type=type_hints["insert_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insert_header": insert_header,
        }

    @builtins.property
    def insert_header(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader"]]:
        '''insert_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        result = self._values.get("insert_header")
        assert result is not None, "Required property 'insert_header' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionChallengeCustomRequestHandling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcbf20391e08eceb9bc521bf6f2a6211cf886e4f51decfeb79b3e0a7c57ef83)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d53a6f1e42c31ad9ab7ac4970b0b7fc06ca3f6c0524093fa4665e144bb45920)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81e99592e5d77fb51d02747d523f3bc79f8a641e1b656156e0a2454fefeaaff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c970cf6470b6a4b4328b7033d4997d5f7c9992f388f4fed0d7d4d4162b06c32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76240f39e86a19cf6ce126d54f904df77be940fe2bfabdb46d2894c56becc485)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e27e8114af3b71813097dfcc8a8e66fe8f30228004272fc9cd2120a4869744e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3956fb61a59897f07a0e84cc0699eabe643a849d908c2879c6cdcfdde13b7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad3e57e5c52e7ccefe94cb13b30e04f0ffacb2c1fa37fe14c46adb2538e6d48b)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12dd9ea70a029ea9978537d069ea39ac7423d9a528f005c73345309988491d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1397f8eaecc0281cd473bbc7d58fb1c2b64bbc0d1050c01f25856439cc4ca80e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d81deade3d9cd2a3984892c9f8c2d119bf5d3d1d3a5174679c2e8ac3e87e260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionChallengeCustomRequestHandlingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallengeCustomRequestHandlingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f55a760b1ae07d6ac53cb5023a295702916ba0a028957f862cbde021c313734)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInsertHeader")
    def put_insert_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b007473458038182ddcffe8542e2f766ced5f8d33204f61912b8023fb63710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInsertHeader", [value]))

    @builtins.property
    @jsii.member(jsii_name="insertHeader")
    def insert_header(
        self,
    ) -> Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderList:
        return typing.cast(Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderList, jsii.get(self, "insertHeader"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaderInput")
    def insert_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]], jsii.get(self, "insertHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionChallengeCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionChallengeCustomRequestHandling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionChallengeCustomRequestHandling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7069ee6acce60eec74fc41b7ea1ea4285ad77774395ab4e3138df4c6bc6aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionChallengeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionChallengeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32cdc57849fc47ee7066468ed10cfc8b1e677d9cd9c4e0dd25f121e479ff4e8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRequestHandling")
    def put_custom_request_handling(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        value = Wafv2WebAclRuleActionChallengeCustomRequestHandling(
            insert_header=insert_header
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRequestHandling", [value]))

    @jsii.member(jsii_name="resetCustomRequestHandling")
    def reset_custom_request_handling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRequestHandling", []))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandling")
    def custom_request_handling(
        self,
    ) -> Wafv2WebAclRuleActionChallengeCustomRequestHandlingOutputReference:
        return typing.cast(Wafv2WebAclRuleActionChallengeCustomRequestHandlingOutputReference, jsii.get(self, "customRequestHandling"))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandlingInput")
    def custom_request_handling_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionChallengeCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionChallengeCustomRequestHandling], jsii.get(self, "customRequestHandlingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleActionChallenge]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionChallenge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionChallenge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364c66f7ab235c255f6ee6b5821e74744a738cede14ca64b661416fc276236d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCount",
    jsii_struct_bases=[],
    name_mapping={"custom_request_handling": "customRequestHandling"},
)
class Wafv2WebAclRuleActionCount:
    def __init__(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union["Wafv2WebAclRuleActionCountCustomRequestHandling", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        if isinstance(custom_request_handling, dict):
            custom_request_handling = Wafv2WebAclRuleActionCountCustomRequestHandling(**custom_request_handling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3115f3af8ecad5b45b4175dd14e03a5c19a09eb48d933cdb81436a4114fb825e)
            check_type(argname="argument custom_request_handling", value=custom_request_handling, expected_type=type_hints["custom_request_handling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_request_handling is not None:
            self._values["custom_request_handling"] = custom_request_handling

    @builtins.property
    def custom_request_handling(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleActionCountCustomRequestHandling"]:
        '''custom_request_handling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        result = self._values.get("custom_request_handling")
        return typing.cast(typing.Optional["Wafv2WebAclRuleActionCountCustomRequestHandling"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCountCustomRequestHandling",
    jsii_struct_bases=[],
    name_mapping={"insert_header": "insertHeader"},
)
class Wafv2WebAclRuleActionCountCustomRequestHandling:
    def __init__(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b24362410a16116021578d3396ee57de3a64c5b0e5b0fff5439aff24efb3c7f)
            check_type(argname="argument insert_header", value=insert_header, expected_type=type_hints["insert_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insert_header": insert_header,
        }

    @builtins.property
    def insert_header(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader"]]:
        '''insert_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        result = self._values.get("insert_header")
        assert result is not None, "Required property 'insert_header' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionCountCustomRequestHandling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ad86827405d5009c80cb4628ed61e3b926aa56c783ba246f22fc6b6de6b637)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#value Wafv2WebAcl#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__908e3d2cb2e950b6fcd152951ead5807cf7a55daa6b4fae1ee0de62b06fb7022)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605656f5184e87dca1e947843adbe1046f17f4e2b95950c3da8119e614084142)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c095dddf3abab740798d68b03c48eeb64934d2a069c6733009f25eb8368bc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b99c12178963879f0ddb9434aaa609c9f2dbc60cf47fd5a3572841a240f453a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d102e0a97009e7ca9cda9d1e5bd055e82657863ab74b130959db83228351c426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718ef5fe68224f45dd59a229bdafacf7f6d5252f2c826ae55f4815ace66f10f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02defd4cf711189763f688362eebc8eac03c3f06dd78aa440cf3deb3c3952547)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f235829d2534d09d945e0f5a022a1d461d29be90c70db96992234ee7238095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42b3205b84260af663155970aa000d0ff03e5188401d38704583ad1d0084609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e84c1988c498b53855fbb29811a9757f6b60eb491dcfe25023d645f8a33154b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionCountCustomRequestHandlingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCountCustomRequestHandlingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f20b0d10806631d4842ae6002f50178cd10ae0df150cc730d599df77f5670ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInsertHeader")
    def put_insert_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb147591911bc164821517c6ce04c57b88eb7f67eede27029e40ccfe92222dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInsertHeader", [value]))

    @builtins.property
    @jsii.member(jsii_name="insertHeader")
    def insert_header(
        self,
    ) -> Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderList:
        return typing.cast(Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderList, jsii.get(self, "insertHeader"))

    @builtins.property
    @jsii.member(jsii_name="insertHeaderInput")
    def insert_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]], jsii.get(self, "insertHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionCountCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCountCustomRequestHandling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionCountCustomRequestHandling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fa7c8167aa0a86a9dba76f7472633961559cb993688e9134df65688b4d5c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64badc41138ad03158869d9ded08b33bbd425826771fc6f901463363c1f8ae91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRequestHandling")
    def put_custom_request_handling(
        self,
        *,
        insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param insert_header: insert_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#insert_header Wafv2WebAcl#insert_header}
        '''
        value = Wafv2WebAclRuleActionCountCustomRequestHandling(
            insert_header=insert_header
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRequestHandling", [value]))

    @jsii.member(jsii_name="resetCustomRequestHandling")
    def reset_custom_request_handling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRequestHandling", []))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandling")
    def custom_request_handling(
        self,
    ) -> Wafv2WebAclRuleActionCountCustomRequestHandlingOutputReference:
        return typing.cast(Wafv2WebAclRuleActionCountCustomRequestHandlingOutputReference, jsii.get(self, "customRequestHandling"))

    @builtins.property
    @jsii.member(jsii_name="customRequestHandlingInput")
    def custom_request_handling_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleActionCountCustomRequestHandling]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCountCustomRequestHandling], jsii.get(self, "customRequestHandlingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleActionCount]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleActionCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ce0b3433719ccb6f487804350a01b2a40ac0723b822064648cfe4dc88ce6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf273dc1cda317eeaf1d79e89efaa6ebd26d0044bcc8fdbf87186bdb3cd94e01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllow")
    def put_allow(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionAllowCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        value = Wafv2WebAclRuleActionAllow(
            custom_request_handling=custom_request_handling
        )

        return typing.cast(None, jsii.invoke(self, "putAllow", [value]))

    @jsii.member(jsii_name="putBlock")
    def put_block(
        self,
        *,
        custom_response: typing.Optional[typing.Union[Wafv2WebAclRuleActionBlockCustomResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_response: custom_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_response Wafv2WebAcl#custom_response}
        '''
        value = Wafv2WebAclRuleActionBlock(custom_response=custom_response)

        return typing.cast(None, jsii.invoke(self, "putBlock", [value]))

    @jsii.member(jsii_name="putCaptcha")
    def put_captcha(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionCaptchaCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        value = Wafv2WebAclRuleActionCaptcha(
            custom_request_handling=custom_request_handling
        )

        return typing.cast(None, jsii.invoke(self, "putCaptcha", [value]))

    @jsii.member(jsii_name="putChallenge")
    def put_challenge(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionChallengeCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        value = Wafv2WebAclRuleActionChallenge(
            custom_request_handling=custom_request_handling
        )

        return typing.cast(None, jsii.invoke(self, "putChallenge", [value]))

    @jsii.member(jsii_name="putCount")
    def put_count(
        self,
        *,
        custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionCountCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_request_handling: custom_request_handling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#custom_request_handling Wafv2WebAcl#custom_request_handling}
        '''
        value = Wafv2WebAclRuleActionCount(
            custom_request_handling=custom_request_handling
        )

        return typing.cast(None, jsii.invoke(self, "putCount", [value]))

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetBlock")
    def reset_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlock", []))

    @jsii.member(jsii_name="resetCaptcha")
    def reset_captcha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptcha", []))

    @jsii.member(jsii_name="resetChallenge")
    def reset_challenge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChallenge", []))

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> Wafv2WebAclRuleActionAllowOutputReference:
        return typing.cast(Wafv2WebAclRuleActionAllowOutputReference, jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="block")
    def block(self) -> Wafv2WebAclRuleActionBlockOutputReference:
        return typing.cast(Wafv2WebAclRuleActionBlockOutputReference, jsii.get(self, "block"))

    @builtins.property
    @jsii.member(jsii_name="captcha")
    def captcha(self) -> Wafv2WebAclRuleActionCaptchaOutputReference:
        return typing.cast(Wafv2WebAclRuleActionCaptchaOutputReference, jsii.get(self, "captcha"))

    @builtins.property
    @jsii.member(jsii_name="challenge")
    def challenge(self) -> Wafv2WebAclRuleActionChallengeOutputReference:
        return typing.cast(Wafv2WebAclRuleActionChallengeOutputReference, jsii.get(self, "challenge"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> Wafv2WebAclRuleActionCountOutputReference:
        return typing.cast(Wafv2WebAclRuleActionCountOutputReference, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(self) -> typing.Optional[Wafv2WebAclRuleActionAllow]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionAllow], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="blockInput")
    def block_input(self) -> typing.Optional[Wafv2WebAclRuleActionBlock]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionBlock], jsii.get(self, "blockInput"))

    @builtins.property
    @jsii.member(jsii_name="captchaInput")
    def captcha_input(self) -> typing.Optional[Wafv2WebAclRuleActionCaptcha]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCaptcha], jsii.get(self, "captchaInput"))

    @builtins.property
    @jsii.member(jsii_name="challengeInput")
    def challenge_input(self) -> typing.Optional[Wafv2WebAclRuleActionChallenge]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionChallenge], jsii.get(self, "challengeInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[Wafv2WebAclRuleActionCount]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleActionCount], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleAction]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[Wafv2WebAclRuleAction]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282b503640bca96ca2244dcd27a3140a66d28e13826505903a38a4145ca8edcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleCaptchaConfig",
    jsii_struct_bases=[],
    name_mapping={"immunity_time_property": "immunityTimeProperty"},
)
class Wafv2WebAclRuleCaptchaConfig:
    def __init__(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union["Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        if isinstance(immunity_time_property, dict):
            immunity_time_property = Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty(**immunity_time_property)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04597b66260a0965657d273288c439afeb708cca00e939185585e3040f19be21)
            check_type(argname="argument immunity_time_property", value=immunity_time_property, expected_type=type_hints["immunity_time_property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time_property is not None:
            self._values["immunity_time_property"] = immunity_time_property

    @builtins.property
    def immunity_time_property(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty"]:
        '''immunity_time_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        result = self._values.get("immunity_time_property")
        return typing.cast(typing.Optional["Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleCaptchaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty",
    jsii_struct_bases=[],
    name_mapping={"immunity_time": "immunityTime"},
)
class Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty:
    def __init__(self, *, immunity_time: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a15dc9c5165382d2892a55f4ab456c9e310b3c7c579a5fe4345f0d54fd70b5)
            check_type(argname="argument immunity_time", value=immunity_time, expected_type=type_hints["immunity_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time is not None:
            self._values["immunity_time"] = immunity_time

    @builtins.property
    def immunity_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.'''
        result = self._values.get("immunity_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleCaptchaConfigImmunityTimePropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleCaptchaConfigImmunityTimePropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c5183ae55fd5c48e8c312130599b81ef59b4c64b25e8e333d2e19e1d6cf878)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmunityTime")
    def reset_immunity_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTime", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeInput")
    def immunity_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "immunityTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="immunityTime")
    def immunity_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "immunityTime"))

    @immunity_time.setter
    def immunity_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942c3dd5ef3410d54efbe6f5743cf36e1dadb6d1c0d5b466bbaf558ea7035e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immunityTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7350ddb2b3fbf929042aae5a77ac451a5c68b6888fa7e79ffae4c75e6f0009e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleCaptchaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleCaptchaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d813952abb0ccaadb802860a449a20d091aca909e6c1cae5ed7ea0d40eee972c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImmunityTimeProperty")
    def put_immunity_time_property(
        self,
        *,
        immunity_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        value = Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty(
            immunity_time=immunity_time
        )

        return typing.cast(None, jsii.invoke(self, "putImmunityTimeProperty", [value]))

    @jsii.member(jsii_name="resetImmunityTimeProperty")
    def reset_immunity_time_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTimeProperty", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeProperty")
    def immunity_time_property(
        self,
    ) -> Wafv2WebAclRuleCaptchaConfigImmunityTimePropertyOutputReference:
        return typing.cast(Wafv2WebAclRuleCaptchaConfigImmunityTimePropertyOutputReference, jsii.get(self, "immunityTimeProperty"))

    @builtins.property
    @jsii.member(jsii_name="immunityTimePropertyInput")
    def immunity_time_property_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty], jsii.get(self, "immunityTimePropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleCaptchaConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleCaptchaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleCaptchaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f336c71d13119b6a8d413c61acff69b1b54a07cf027fbd667157592950dd378f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleChallengeConfig",
    jsii_struct_bases=[],
    name_mapping={"immunity_time_property": "immunityTimeProperty"},
)
class Wafv2WebAclRuleChallengeConfig:
    def __init__(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union["Wafv2WebAclRuleChallengeConfigImmunityTimeProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        if isinstance(immunity_time_property, dict):
            immunity_time_property = Wafv2WebAclRuleChallengeConfigImmunityTimeProperty(**immunity_time_property)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdc0b3a2c3e5401fb7ed8dfd3a144a73566890bba0990fe1a9e51badc1ecf98)
            check_type(argname="argument immunity_time_property", value=immunity_time_property, expected_type=type_hints["immunity_time_property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time_property is not None:
            self._values["immunity_time_property"] = immunity_time_property

    @builtins.property
    def immunity_time_property(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleChallengeConfigImmunityTimeProperty"]:
        '''immunity_time_property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        result = self._values.get("immunity_time_property")
        return typing.cast(typing.Optional["Wafv2WebAclRuleChallengeConfigImmunityTimeProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleChallengeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleChallengeConfigImmunityTimeProperty",
    jsii_struct_bases=[],
    name_mapping={"immunity_time": "immunityTime"},
)
class Wafv2WebAclRuleChallengeConfigImmunityTimeProperty:
    def __init__(self, *, immunity_time: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47ee6b57e4d7f61351c4dbf4d99074493522d081a6f11f1440a6275852f956a)
            check_type(argname="argument immunity_time", value=immunity_time, expected_type=type_hints["immunity_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immunity_time is not None:
            self._values["immunity_time"] = immunity_time

    @builtins.property
    def immunity_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.'''
        result = self._values.get("immunity_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleChallengeConfigImmunityTimeProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleChallengeConfigImmunityTimePropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleChallengeConfigImmunityTimePropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e1ce759158a36ac79b1ab8da48a63aa7b461c08c9b074a6108fe4fa5939320e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmunityTime")
    def reset_immunity_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTime", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeInput")
    def immunity_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "immunityTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="immunityTime")
    def immunity_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "immunityTime"))

    @immunity_time.setter
    def immunity_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ad9578415c71639136990d7d636cd7b020281eb295f95022c07cb0c4507499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immunityTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aea1414fbb8775a50deac05e307423dae0805d47d59ec26dad86d54118e8404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleChallengeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleChallengeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bb058c116afb58284b95297cb8a78ee44544fd132547e42149b13663ca12975)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImmunityTimeProperty")
    def put_immunity_time_property(
        self,
        *,
        immunity_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param immunity_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time Wafv2WebAcl#immunity_time}.
        '''
        value = Wafv2WebAclRuleChallengeConfigImmunityTimeProperty(
            immunity_time=immunity_time
        )

        return typing.cast(None, jsii.invoke(self, "putImmunityTimeProperty", [value]))

    @jsii.member(jsii_name="resetImmunityTimeProperty")
    def reset_immunity_time_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmunityTimeProperty", []))

    @builtins.property
    @jsii.member(jsii_name="immunityTimeProperty")
    def immunity_time_property(
        self,
    ) -> Wafv2WebAclRuleChallengeConfigImmunityTimePropertyOutputReference:
        return typing.cast(Wafv2WebAclRuleChallengeConfigImmunityTimePropertyOutputReference, jsii.get(self, "immunityTimeProperty"))

    @builtins.property
    @jsii.member(jsii_name="immunityTimePropertyInput")
    def immunity_time_property_input(
        self,
    ) -> typing.Optional[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty], jsii.get(self, "immunityTimePropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleChallengeConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleChallengeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleChallengeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c74fc926f7f8851f97b025113aaa27abb9b47cebdb19a826a9838cde8b357fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a63e8753d69e2aacfb8ce31e3ea796383b3b9ac1084dbfdeab3f49bf597a667)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "Wafv2WebAclRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0462143547db82c66042c3947d3eb350e8096c9024ccbff4090d3e7d69209991)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f11bd445a617843ead82c289cec7bbc1e9a6e906d9aef0fb124f5bfd5c3bdd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cbbd0a13ed95d7e72edbddbe40a9ba848e1cb0cc80265f9c5c0ef7295a6f2ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24f60126725e10d8a1bc1c9fd03c153bed475330603241f7069697a61dfc27bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf8038a4c83c071023157c0c4448c7e304fe04fc0c51a1e26ca2e8f160e083a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45dbff4d6e22a1915a7d3f1e4e349591dfeb5aef93db65fd833af27b00b1f892)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        allow: typing.Optional[typing.Union[Wafv2WebAclRuleActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
        block: typing.Optional[typing.Union[Wafv2WebAclRuleActionBlock, typing.Dict[builtins.str, typing.Any]]] = None,
        captcha: typing.Optional[typing.Union[Wafv2WebAclRuleActionCaptcha, typing.Dict[builtins.str, typing.Any]]] = None,
        challenge: typing.Optional[typing.Union[Wafv2WebAclRuleActionChallenge, typing.Dict[builtins.str, typing.Any]]] = None,
        count: typing.Optional[typing.Union[Wafv2WebAclRuleActionCount, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#allow Wafv2WebAcl#allow}
        :param block: block block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#block Wafv2WebAcl#block}
        :param captcha: captcha block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#captcha Wafv2WebAcl#captcha}
        :param challenge: challenge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#challenge Wafv2WebAcl#challenge}
        :param count: count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#count Wafv2WebAcl#count}
        '''
        value = Wafv2WebAclRuleAction(
            allow=allow, block=block, captcha=captcha, challenge=challenge, count=count
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putCaptchaConfig")
    def put_captcha_config(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        value = Wafv2WebAclRuleCaptchaConfig(
            immunity_time_property=immunity_time_property
        )

        return typing.cast(None, jsii.invoke(self, "putCaptchaConfig", [value]))

    @jsii.member(jsii_name="putChallengeConfig")
    def put_challenge_config(
        self,
        *,
        immunity_time_property: typing.Optional[typing.Union[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param immunity_time_property: immunity_time_property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#immunity_time_property Wafv2WebAcl#immunity_time_property}
        '''
        value = Wafv2WebAclRuleChallengeConfig(
            immunity_time_property=immunity_time_property
        )

        return typing.cast(None, jsii.invoke(self, "putChallengeConfig", [value]))

    @jsii.member(jsii_name="putOverrideAction")
    def put_override_action(
        self,
        *,
        count: typing.Optional[typing.Union["Wafv2WebAclRuleOverrideActionCount", typing.Dict[builtins.str, typing.Any]]] = None,
        none: typing.Optional[typing.Union["Wafv2WebAclRuleOverrideActionNone", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#count Wafv2WebAcl#count}
        :param none: none block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#none Wafv2WebAcl#none}
        '''
        value = Wafv2WebAclRuleOverrideAction(count=count, none=none)

        return typing.cast(None, jsii.invoke(self, "putOverrideAction", [value]))

    @jsii.member(jsii_name="putRuleLabel")
    def put_rule_label(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclRuleRuleLabel", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937fe0182bb7eef5e5d45153cd133f93e520b59aa96af30613da6bcc9883968b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuleLabel", [value]))

    @jsii.member(jsii_name="putVisibilityConfig")
    def put_visibility_config(
        self,
        *,
        cloudwatch_metrics_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        metric_name: builtins.str,
        sampled_requests_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param cloudwatch_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudwatch_metrics_enabled Wafv2WebAcl#cloudwatch_metrics_enabled}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#metric_name Wafv2WebAcl#metric_name}.
        :param sampled_requests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#sampled_requests_enabled Wafv2WebAcl#sampled_requests_enabled}.
        '''
        value = Wafv2WebAclRuleVisibilityConfig(
            cloudwatch_metrics_enabled=cloudwatch_metrics_enabled,
            metric_name=metric_name,
            sampled_requests_enabled=sampled_requests_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putVisibilityConfig", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetCaptchaConfig")
    def reset_captcha_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptchaConfig", []))

    @jsii.member(jsii_name="resetChallengeConfig")
    def reset_challenge_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChallengeConfig", []))

    @jsii.member(jsii_name="resetOverrideAction")
    def reset_override_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideAction", []))

    @jsii.member(jsii_name="resetRuleLabel")
    def reset_rule_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleLabel", []))

    @jsii.member(jsii_name="resetStatement")
    def reset_statement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatement", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> Wafv2WebAclRuleActionOutputReference:
        return typing.cast(Wafv2WebAclRuleActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="captchaConfig")
    def captcha_config(self) -> Wafv2WebAclRuleCaptchaConfigOutputReference:
        return typing.cast(Wafv2WebAclRuleCaptchaConfigOutputReference, jsii.get(self, "captchaConfig"))

    @builtins.property
    @jsii.member(jsii_name="challengeConfig")
    def challenge_config(self) -> Wafv2WebAclRuleChallengeConfigOutputReference:
        return typing.cast(Wafv2WebAclRuleChallengeConfigOutputReference, jsii.get(self, "challengeConfig"))

    @builtins.property
    @jsii.member(jsii_name="overrideAction")
    def override_action(self) -> "Wafv2WebAclRuleOverrideActionOutputReference":
        return typing.cast("Wafv2WebAclRuleOverrideActionOutputReference", jsii.get(self, "overrideAction"))

    @builtins.property
    @jsii.member(jsii_name="ruleLabel")
    def rule_label(self) -> "Wafv2WebAclRuleRuleLabelList":
        return typing.cast("Wafv2WebAclRuleRuleLabelList", jsii.get(self, "ruleLabel"))

    @builtins.property
    @jsii.member(jsii_name="statementInput")
    def statement_input(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "statementInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityConfig")
    def visibility_config(self) -> "Wafv2WebAclRuleVisibilityConfigOutputReference":
        return typing.cast("Wafv2WebAclRuleVisibilityConfigOutputReference", jsii.get(self, "visibilityConfig"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[Wafv2WebAclRuleAction]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="captchaConfigInput")
    def captcha_config_input(self) -> typing.Optional[Wafv2WebAclRuleCaptchaConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleCaptchaConfig], jsii.get(self, "captchaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="challengeConfigInput")
    def challenge_config_input(self) -> typing.Optional[Wafv2WebAclRuleChallengeConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleChallengeConfig], jsii.get(self, "challengeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideActionInput")
    def override_action_input(self) -> typing.Optional["Wafv2WebAclRuleOverrideAction"]:
        return typing.cast(typing.Optional["Wafv2WebAclRuleOverrideAction"], jsii.get(self, "overrideActionInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleLabelInput")
    def rule_label_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleRuleLabel"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclRuleRuleLabel"]]], jsii.get(self, "ruleLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityConfigInput")
    def visibility_config_input(
        self,
    ) -> typing.Optional["Wafv2WebAclRuleVisibilityConfig"]:
        return typing.cast(typing.Optional["Wafv2WebAclRuleVisibilityConfig"], jsii.get(self, "visibilityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9128c3a9051ce94f639bd98acedb0242d0b4ee4da9bf9da4fcf1a291722f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7285d4a6d12adf1272b60bd32c8b44cfe0365919bc2b9ad8dc9ed14097a86aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c176be72d5bb069415049dce9755aab2d6d6369d601698a3bf88f460ffda912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa9768eb949386c353397fbe15b3162f9c8d8f8f32a4d2a05647693c1d14969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOverrideAction",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "none": "none"},
)
class Wafv2WebAclRuleOverrideAction:
    def __init__(
        self,
        *,
        count: typing.Optional[typing.Union["Wafv2WebAclRuleOverrideActionCount", typing.Dict[builtins.str, typing.Any]]] = None,
        none: typing.Optional[typing.Union["Wafv2WebAclRuleOverrideActionNone", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#count Wafv2WebAcl#count}
        :param none: none block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#none Wafv2WebAcl#none}
        '''
        if isinstance(count, dict):
            count = Wafv2WebAclRuleOverrideActionCount(**count)
        if isinstance(none, dict):
            none = Wafv2WebAclRuleOverrideActionNone(**none)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1d4f05d13811d3d6390860c51ca3218bbabca4bde76aa6a4ffb576ed96acc4)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument none", value=none, expected_type=type_hints["none"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if none is not None:
            self._values["none"] = none

    @builtins.property
    def count(self) -> typing.Optional["Wafv2WebAclRuleOverrideActionCount"]:
        '''count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#count Wafv2WebAcl#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional["Wafv2WebAclRuleOverrideActionCount"], result)

    @builtins.property
    def none(self) -> typing.Optional["Wafv2WebAclRuleOverrideActionNone"]:
        '''none block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#none Wafv2WebAcl#none}
        '''
        result = self._values.get("none")
        return typing.cast(typing.Optional["Wafv2WebAclRuleOverrideActionNone"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleOverrideAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOverrideActionCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclRuleOverrideActionCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleOverrideActionCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleOverrideActionCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOverrideActionCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b53d64b98948dced8d92f7b4274f23b8c647c62b23c8d861603f40a68ef136c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleOverrideActionCount]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleOverrideActionCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleOverrideActionCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35864858c1829b77c7177d787271fe482a742e33ddd5597424e89c39cb083e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOverrideActionNone",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclRuleOverrideActionNone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleOverrideActionNone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleOverrideActionNoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOverrideActionNoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__120e271cae5e4e085cead380307141b76b47e66167e155e8728a03eaf5ca2c15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleOverrideActionNone]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleOverrideActionNone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleOverrideActionNone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd762a3ff78fc969f8fe4aa69dbeb83cb9a7d2bca558b767dd6ebb4006016e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleOverrideActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleOverrideActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7fb5d0ed6b23894bdcc8a73f0a3abe93c12739b8081d519c53ca5630252e2aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCount")
    def put_count(self) -> None:
        value = Wafv2WebAclRuleOverrideActionCount()

        return typing.cast(None, jsii.invoke(self, "putCount", [value]))

    @jsii.member(jsii_name="putNone")
    def put_none(self) -> None:
        value = Wafv2WebAclRuleOverrideActionNone()

        return typing.cast(None, jsii.invoke(self, "putNone", [value]))

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetNone")
    def reset_none(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNone", []))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> Wafv2WebAclRuleOverrideActionCountOutputReference:
        return typing.cast(Wafv2WebAclRuleOverrideActionCountOutputReference, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="none")
    def none(self) -> Wafv2WebAclRuleOverrideActionNoneOutputReference:
        return typing.cast(Wafv2WebAclRuleOverrideActionNoneOutputReference, jsii.get(self, "none"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[Wafv2WebAclRuleOverrideActionCount]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleOverrideActionCount], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="noneInput")
    def none_input(self) -> typing.Optional[Wafv2WebAclRuleOverrideActionNone]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleOverrideActionNone], jsii.get(self, "noneInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleOverrideAction]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleOverrideAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleOverrideAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bcfaf2e5320cd9185bd28b337904489876ecc723c33211b1b738e4ffb1062f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleRuleLabel",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class Wafv2WebAclRuleRuleLabel:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2906a084030046f665e326c207883eeed18790cb800663455913d0bab04b7b9d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#name Wafv2WebAcl#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleRuleLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleRuleLabelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleRuleLabelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1fa00a17e8eeac9ddc1a334ed7d91f598c2f53b4546a276fe1c0f6cfa052be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "Wafv2WebAclRuleRuleLabelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b8f52e6be1579ed5c2bd747932a7a0f73eac1437d922d9278b1b47c0800a24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclRuleRuleLabelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5f7c3adaa4ff8d4170aa8e56275c7342cf3fbbad45442428972746c5a91790)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53abcbac0d068ac9b0de6c552a223e9fcfc879f36b5f8e46510734cea42c358f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e5f95c0d27dce14257b25aaf5865800bbce861452ad6941d6d25e6912635d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleRuleLabel]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleRuleLabel]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleRuleLabel]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8cb16fd6d9364d865c6f65d86a1cfefadf03084858ab1a24b7a503d7b51ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclRuleRuleLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleRuleLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ebb78d7104238f4cb257942814925a59490eb13a301a9f34f6e527b615abd35)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a0557ca19ff9ffa316bbd6c5ea02107161687c38d221982b1a2bdcee440aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleRuleLabel]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleRuleLabel]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleRuleLabel]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ffb031513ce5d4271e6bbe106f7c673d0a21e7dba951ad2d0ffb550b43a6ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleVisibilityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_metrics_enabled": "cloudwatchMetricsEnabled",
        "metric_name": "metricName",
        "sampled_requests_enabled": "sampledRequestsEnabled",
    },
)
class Wafv2WebAclRuleVisibilityConfig:
    def __init__(
        self,
        *,
        cloudwatch_metrics_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        metric_name: builtins.str,
        sampled_requests_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param cloudwatch_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudwatch_metrics_enabled Wafv2WebAcl#cloudwatch_metrics_enabled}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#metric_name Wafv2WebAcl#metric_name}.
        :param sampled_requests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#sampled_requests_enabled Wafv2WebAcl#sampled_requests_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dcff26991aa8a3b61a74813e163b210838da6a92b4e1d88efc0cafb6dbfad1)
            check_type(argname="argument cloudwatch_metrics_enabled", value=cloudwatch_metrics_enabled, expected_type=type_hints["cloudwatch_metrics_enabled"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument sampled_requests_enabled", value=sampled_requests_enabled, expected_type=type_hints["sampled_requests_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudwatch_metrics_enabled": cloudwatch_metrics_enabled,
            "metric_name": metric_name,
            "sampled_requests_enabled": sampled_requests_enabled,
        }

    @builtins.property
    def cloudwatch_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudwatch_metrics_enabled Wafv2WebAcl#cloudwatch_metrics_enabled}.'''
        result = self._values.get("cloudwatch_metrics_enabled")
        assert result is not None, "Required property 'cloudwatch_metrics_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#metric_name Wafv2WebAcl#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sampled_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#sampled_requests_enabled Wafv2WebAcl#sampled_requests_enabled}.'''
        result = self._values.get("sampled_requests_enabled")
        assert result is not None, "Required property 'sampled_requests_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclRuleVisibilityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclRuleVisibilityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclRuleVisibilityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1bf83f5d6e403e961cb64335cc5e32e99b5b8cf34a8fa5c984645653b0372aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricsEnabledInput")
    def cloudwatch_metrics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudwatchMetricsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sampledRequestsEnabledInput")
    def sampled_requests_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sampledRequestsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricsEnabled")
    def cloudwatch_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cloudwatchMetricsEnabled"))

    @cloudwatch_metrics_enabled.setter
    def cloudwatch_metrics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c864e9c088fd4edbae2ba21a5f4e96c92529d3bc2bac33e819277e86a80840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchMetricsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995ad7e1c6d5d2956285f05c8d9e6f6e7e821fa4ae1ac1ab6cf7c817e8f7316a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampledRequestsEnabled")
    def sampled_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sampledRequestsEnabled"))

    @sampled_requests_enabled.setter
    def sampled_requests_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d501ae8826460352d42ff1b09ddb0833fb78158c7c935cace342e4e077fb9f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampledRequestsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclRuleVisibilityConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclRuleVisibilityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclRuleVisibilityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efb4f5ae5625414608d8b1b8f3ff43b193123d03d2cec960126e370ddc5baed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclVisibilityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_metrics_enabled": "cloudwatchMetricsEnabled",
        "metric_name": "metricName",
        "sampled_requests_enabled": "sampledRequestsEnabled",
    },
)
class Wafv2WebAclVisibilityConfig:
    def __init__(
        self,
        *,
        cloudwatch_metrics_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        metric_name: builtins.str,
        sampled_requests_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param cloudwatch_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudwatch_metrics_enabled Wafv2WebAcl#cloudwatch_metrics_enabled}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#metric_name Wafv2WebAcl#metric_name}.
        :param sampled_requests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#sampled_requests_enabled Wafv2WebAcl#sampled_requests_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae273d2b29feb830a63ebcad84dde341ca21b54859741e999fa490626cc4ada8)
            check_type(argname="argument cloudwatch_metrics_enabled", value=cloudwatch_metrics_enabled, expected_type=type_hints["cloudwatch_metrics_enabled"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument sampled_requests_enabled", value=sampled_requests_enabled, expected_type=type_hints["sampled_requests_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudwatch_metrics_enabled": cloudwatch_metrics_enabled,
            "metric_name": metric_name,
            "sampled_requests_enabled": sampled_requests_enabled,
        }

    @builtins.property
    def cloudwatch_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#cloudwatch_metrics_enabled Wafv2WebAcl#cloudwatch_metrics_enabled}.'''
        result = self._values.get("cloudwatch_metrics_enabled")
        assert result is not None, "Required property 'cloudwatch_metrics_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#metric_name Wafv2WebAcl#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sampled_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl#sampled_requests_enabled Wafv2WebAcl#sampled_requests_enabled}.'''
        result = self._values.get("sampled_requests_enabled")
        assert result is not None, "Required property 'sampled_requests_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclVisibilityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclVisibilityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAcl.Wafv2WebAclVisibilityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c677fdb201627c4ade6d94f172f08f391401901f87bdd51b8526f0cbf168a44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricsEnabledInput")
    def cloudwatch_metrics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudwatchMetricsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sampledRequestsEnabledInput")
    def sampled_requests_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sampledRequestsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricsEnabled")
    def cloudwatch_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cloudwatchMetricsEnabled"))

    @cloudwatch_metrics_enabled.setter
    def cloudwatch_metrics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e061e7830e08caaa980312268ca20f2f2b99c4cd1212038b2f5e23bec1ca0503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchMetricsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa75186d17efa0b0b19c090f9b0606140ac561e7aaf2cfdbd877f044ffad203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampledRequestsEnabled")
    def sampled_requests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sampledRequestsEnabled"))

    @sampled_requests_enabled.setter
    def sampled_requests_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240e07cfe7c2e00c399587ac7e659b0198bd58206524f44c54ad5cac9fa6dc70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampledRequestsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Wafv2WebAclVisibilityConfig]:
        return typing.cast(typing.Optional[Wafv2WebAclVisibilityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclVisibilityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545229753b7262b15e285354f02f72dfcf483bdeecce4816048e8d218f367705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Wafv2WebAcl",
    "Wafv2WebAclAssociationConfig",
    "Wafv2WebAclAssociationConfigOutputReference",
    "Wafv2WebAclAssociationConfigRequestBody",
    "Wafv2WebAclAssociationConfigRequestBodyApiGateway",
    "Wafv2WebAclAssociationConfigRequestBodyApiGatewayOutputReference",
    "Wafv2WebAclAssociationConfigRequestBodyAppRunnerService",
    "Wafv2WebAclAssociationConfigRequestBodyAppRunnerServiceOutputReference",
    "Wafv2WebAclAssociationConfigRequestBodyCloudfront",
    "Wafv2WebAclAssociationConfigRequestBodyCloudfrontOutputReference",
    "Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool",
    "Wafv2WebAclAssociationConfigRequestBodyCognitoUserPoolOutputReference",
    "Wafv2WebAclAssociationConfigRequestBodyList",
    "Wafv2WebAclAssociationConfigRequestBodyOutputReference",
    "Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance",
    "Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstanceOutputReference",
    "Wafv2WebAclCaptchaConfig",
    "Wafv2WebAclCaptchaConfigImmunityTimeProperty",
    "Wafv2WebAclCaptchaConfigImmunityTimePropertyOutputReference",
    "Wafv2WebAclCaptchaConfigOutputReference",
    "Wafv2WebAclChallengeConfig",
    "Wafv2WebAclChallengeConfigImmunityTimeProperty",
    "Wafv2WebAclChallengeConfigImmunityTimePropertyOutputReference",
    "Wafv2WebAclChallengeConfigOutputReference",
    "Wafv2WebAclConfig",
    "Wafv2WebAclCustomResponseBody",
    "Wafv2WebAclCustomResponseBodyList",
    "Wafv2WebAclCustomResponseBodyOutputReference",
    "Wafv2WebAclDataProtectionConfig",
    "Wafv2WebAclDataProtectionConfigDataProtection",
    "Wafv2WebAclDataProtectionConfigDataProtectionField",
    "Wafv2WebAclDataProtectionConfigDataProtectionFieldOutputReference",
    "Wafv2WebAclDataProtectionConfigDataProtectionList",
    "Wafv2WebAclDataProtectionConfigDataProtectionOutputReference",
    "Wafv2WebAclDataProtectionConfigOutputReference",
    "Wafv2WebAclDefaultAction",
    "Wafv2WebAclDefaultActionAllow",
    "Wafv2WebAclDefaultActionAllowCustomRequestHandling",
    "Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader",
    "Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderList",
    "Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeaderOutputReference",
    "Wafv2WebAclDefaultActionAllowCustomRequestHandlingOutputReference",
    "Wafv2WebAclDefaultActionAllowOutputReference",
    "Wafv2WebAclDefaultActionBlock",
    "Wafv2WebAclDefaultActionBlockCustomResponse",
    "Wafv2WebAclDefaultActionBlockCustomResponseOutputReference",
    "Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader",
    "Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderList",
    "Wafv2WebAclDefaultActionBlockCustomResponseResponseHeaderOutputReference",
    "Wafv2WebAclDefaultActionBlockOutputReference",
    "Wafv2WebAclDefaultActionOutputReference",
    "Wafv2WebAclRule",
    "Wafv2WebAclRuleAction",
    "Wafv2WebAclRuleActionAllow",
    "Wafv2WebAclRuleActionAllowCustomRequestHandling",
    "Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader",
    "Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderList",
    "Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeaderOutputReference",
    "Wafv2WebAclRuleActionAllowCustomRequestHandlingOutputReference",
    "Wafv2WebAclRuleActionAllowOutputReference",
    "Wafv2WebAclRuleActionBlock",
    "Wafv2WebAclRuleActionBlockCustomResponse",
    "Wafv2WebAclRuleActionBlockCustomResponseOutputReference",
    "Wafv2WebAclRuleActionBlockCustomResponseResponseHeader",
    "Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderList",
    "Wafv2WebAclRuleActionBlockCustomResponseResponseHeaderOutputReference",
    "Wafv2WebAclRuleActionBlockOutputReference",
    "Wafv2WebAclRuleActionCaptcha",
    "Wafv2WebAclRuleActionCaptchaCustomRequestHandling",
    "Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader",
    "Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderList",
    "Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeaderOutputReference",
    "Wafv2WebAclRuleActionCaptchaCustomRequestHandlingOutputReference",
    "Wafv2WebAclRuleActionCaptchaOutputReference",
    "Wafv2WebAclRuleActionChallenge",
    "Wafv2WebAclRuleActionChallengeCustomRequestHandling",
    "Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader",
    "Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderList",
    "Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeaderOutputReference",
    "Wafv2WebAclRuleActionChallengeCustomRequestHandlingOutputReference",
    "Wafv2WebAclRuleActionChallengeOutputReference",
    "Wafv2WebAclRuleActionCount",
    "Wafv2WebAclRuleActionCountCustomRequestHandling",
    "Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader",
    "Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderList",
    "Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeaderOutputReference",
    "Wafv2WebAclRuleActionCountCustomRequestHandlingOutputReference",
    "Wafv2WebAclRuleActionCountOutputReference",
    "Wafv2WebAclRuleActionOutputReference",
    "Wafv2WebAclRuleCaptchaConfig",
    "Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty",
    "Wafv2WebAclRuleCaptchaConfigImmunityTimePropertyOutputReference",
    "Wafv2WebAclRuleCaptchaConfigOutputReference",
    "Wafv2WebAclRuleChallengeConfig",
    "Wafv2WebAclRuleChallengeConfigImmunityTimeProperty",
    "Wafv2WebAclRuleChallengeConfigImmunityTimePropertyOutputReference",
    "Wafv2WebAclRuleChallengeConfigOutputReference",
    "Wafv2WebAclRuleList",
    "Wafv2WebAclRuleOutputReference",
    "Wafv2WebAclRuleOverrideAction",
    "Wafv2WebAclRuleOverrideActionCount",
    "Wafv2WebAclRuleOverrideActionCountOutputReference",
    "Wafv2WebAclRuleOverrideActionNone",
    "Wafv2WebAclRuleOverrideActionNoneOutputReference",
    "Wafv2WebAclRuleOverrideActionOutputReference",
    "Wafv2WebAclRuleRuleLabel",
    "Wafv2WebAclRuleRuleLabelList",
    "Wafv2WebAclRuleRuleLabelOutputReference",
    "Wafv2WebAclRuleVisibilityConfig",
    "Wafv2WebAclRuleVisibilityConfigOutputReference",
    "Wafv2WebAclVisibilityConfig",
    "Wafv2WebAclVisibilityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__0bacca56f499a3b02a462d08c7425e86ca2a1d18130ab2dfa652dc54570230a1(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_action: typing.Union[Wafv2WebAclDefaultAction, typing.Dict[builtins.str, typing.Any]],
    scope: builtins.str,
    visibility_config: typing.Union[Wafv2WebAclVisibilityConfig, typing.Dict[builtins.str, typing.Any]],
    association_config: typing.Optional[typing.Union[Wafv2WebAclAssociationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    captcha_config: typing.Optional[typing.Union[Wafv2WebAclCaptchaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    challenge_config: typing.Optional[typing.Union[Wafv2WebAclChallengeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_response_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclCustomResponseBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_protection_config: typing.Optional[typing.Union[Wafv2WebAclDataProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule_json: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    token_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__4a81b401034dc40dbee996e70f5400d3788286f1f937812e94430e0b64f26e73(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cf5a1579be5ffd95f2e234d8cc9055e7add822abc72b98308b0328234b6648(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclCustomResponseBody, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081577810311b70bac1d78bef696c9da63c42b77c34d1e8af2baeb08e4a64c42(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff8fff4c6cfc097b72fd73d04f8d4079902c9eef77f61a627d4ff86a68fdb78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91089f6846d95ff0e30dd4eec5bca7b19be4af16b67e38ed595a7f0d70dc9f0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7422278a77bfd4531787f5245bed804040d17fc819cef9466781e756bcc52c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db691fdb5330309f7cada4fc3fda210067157ec85462a997d85f5e7c70f9618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16a72f98e88ac1b1c0816249ecd28a973c35e1a850ebdb68c07aef761562c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f1c55a8f32c0bc3675da8a7fe81585829c9ecb68b68d9c4b31545c31f8cb14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fea4fe4c0644389030626a30b30099479fbad7cadbe4d2fe14556e5db609af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a11b455a6991d9122285238ba53327f45e4c643a3771e01a6cc5f8459e757a7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d542a8413b07779725989a7cd2fcd8bfee61a02ecb8c117d4615644929110b0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f5ce624caaa75da5cd5f1c6f49d5af5ed9605fee61746d4ca312bc7e6b5690(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322032451ba34136f93e37446edfc3f61eec3f74b20866b889bf7df4ce07dd79(
    *,
    request_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclAssociationConfigRequestBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea0f0ff26a99ecdaad62456cf4d539efbbc4de0d2aa2133dd94e4d9d0838118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28c224cb04d9ebc1a0736f394ee726b2155bf6af3328cd1d2bda1d74603660e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclAssociationConfigRequestBody, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30674cb5d8d06ce8c7d6ef3292927c56ddad7741fe7f02249ba7e4fc1f70849c(
    value: typing.Optional[Wafv2WebAclAssociationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae5234493a4916c5a0415725c89c83d10a585a830e61aab5746999a5f4860cd(
    *,
    api_gateway: typing.Optional[typing.Union[Wafv2WebAclAssociationConfigRequestBodyApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    app_runner_service: typing.Optional[typing.Union[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudfront: typing.Optional[typing.Union[Wafv2WebAclAssociationConfigRequestBodyCloudfront, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_user_pool: typing.Optional[typing.Union[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool, typing.Dict[builtins.str, typing.Any]]] = None,
    verified_access_instance: typing.Optional[typing.Union[Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cede49b91fe34ff280d2f00ac3d67fa56e59af46ed88e6a2f9d547bb2c724a5(
    *,
    default_size_inspection_limit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e55b83884c0d4c51d698bd7522b999e2d1e2cfe4e78be59b3fa908c1f04c83e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390562097734a7d8153e3559c8534e1b2b3a287cb391895f3e1b8284f6c5d3a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b32e2d7e99c793b0105a0eb98ad1462643d42beceb6c4182eece377effa61ae(
    value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyApiGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005cbd452d37e35930a328bcc9c44a18c8a8e29d9cb711e78c24727f027e251c(
    *,
    default_size_inspection_limit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6a47ef939ab81e1265cb62d27fae1c2b90db6a763e6a2c1e8bf37836bd1529(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14db49bceaf9d0a812251658e368ba75f2bb87513fbeb5728fe17f18e73f567f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd91c6f3997ae1fd790f372561819bbd89509eed8290039fe026bcbd3d0bda1c(
    value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyAppRunnerService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dff72cfd6927f2124e3cf14aaf0849958ac9448abd3a80f451b47af5181acf4(
    *,
    default_size_inspection_limit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2641af708c61bd86bf9866ad6e6b4c42553105f957f129fb982118496173d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a80882b6f4a3cc61aaf028f4e1e7824dc26095630c16ee068a4bf94b70c614b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bab7578bb083a1acf526c69428b0c30f41f2ddbea309df1c601a29b068a5012(
    value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCloudfront],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bdefe2663fdbf7085e967f3ff44fee5ffd3146e2893185ba1f48aef563f92b(
    *,
    default_size_inspection_limit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2256294d89f43f1915dcb8bd6654e4916533bcc59139fbba84dada4bd03bdee3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86371d247fd6751ebb1e5a1ecab439ac99d28d976c90c848cdfab170b6d401d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd81a1d822654f24db60e7628cd3a66c7c373d09dd471ea10f10f6e7a7a3677(
    value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyCognitoUserPool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef5224b0cacd6e857f694ee54c21c38e5bd88dd02a73f4027df6f93fd456f2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dbf522efa54ba4676fb00a7f01fe8791e284580a9b57967e60035226b361b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd435df5f048b49e1a12ab71eecafd6363a7dbffc83ad0ec432948adb39a5ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91cbdb8f3ecfe8c4589376d74c811e01687a7faffdd7a8376a1930f54236e36(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e49b339a40e4a2b41e7059371feae97f941318d28ff12df2e7cbd6591b1a8b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13fa06d764e58f7fd98568f1f68fc16b247186e01232b0c75a3ac0566c125fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclAssociationConfigRequestBody]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe0cee958b53943ff663d61a94dc4178785e3e07821bf4acfcae5ba00c2ae8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b523954de00db1d7ecbfd0f1a5d52669d85a939683cf3718b22594b605c4bab4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclAssociationConfigRequestBody]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7793a8b35253bb545e577df8a6b1ccc1877ea0b6960361df4d5b63f81b6221cc(
    *,
    default_size_inspection_limit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fe3cb56a43249e687a9ca2dcaf1905a987b31ab083738fc902aab4cc334a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22f0058056c3c6f1cc1323f97b1fc4491cedc16fc888684b22e0e45d409dd45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8296bd993604d102ad080336d785752cac21698031299d32d8cd254f13dfe5f(
    value: typing.Optional[Wafv2WebAclAssociationConfigRequestBodyVerifiedAccessInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fa2aca8a649ddec07b8f109edf9fab9b97e4bfb5bf45f8dacd28e9557b2fc5(
    *,
    immunity_time_property: typing.Optional[typing.Union[Wafv2WebAclCaptchaConfigImmunityTimeProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2312ffdaff3cb0e15d7cece12802b900e647b78c10471f8f35af418b157cb20(
    *,
    immunity_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec84a1817c92c2063e6c33791b4ed4adf1329ff99520034690d73af7ef51ae79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69374857f420f836759e5f142109e6c75cb0ad0b0b1dcf3e31f477776cc3300c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4be9cf5023b21efc442cbc6fa3059923dd4f183b88d21b0b08b8abd3d69ce7(
    value: typing.Optional[Wafv2WebAclCaptchaConfigImmunityTimeProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf5a65c896b1f75270291ea52862f2d913d49f47184f78c3aae0acdf449e79c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30099605ca6e815a3bd5c21f3bc613d70d6aa24409c48d1fb0d5b27918481696(
    value: typing.Optional[Wafv2WebAclCaptchaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e115cfd7f532bfeaf17db65b3163e0feb0726d18aa69cd60763f3736104050a5(
    *,
    immunity_time_property: typing.Optional[typing.Union[Wafv2WebAclChallengeConfigImmunityTimeProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66aec466fffaa0498619c21a0c2caeb27003a35b72e62a8fb449ee065d7f522(
    *,
    immunity_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7828eac20930715f584d1905be89c8320db6e4db3b67a3dd2872e21a85a23722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e93083f8add2611f72b2a0510dfa03ba4f724c00a4ecf4e7cef242c5554f7a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1be32e56ab96666238e9f85866674f53c0c1cbbfa5acb026ca34ed5576f75b(
    value: typing.Optional[Wafv2WebAclChallengeConfigImmunityTimeProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892eaef0c626af19b78ecc8e5fe26da10a34271e2971e8326b824a225528b89d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdc8d221c7ed210b7b50860a6ab2256caae59ea88bac18c735c218bf1d4573e(
    value: typing.Optional[Wafv2WebAclChallengeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22005b7e448d418414d12f019356401f53a352182e1385bba3ce90d7b97ce91(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_action: typing.Union[Wafv2WebAclDefaultAction, typing.Dict[builtins.str, typing.Any]],
    scope: builtins.str,
    visibility_config: typing.Union[Wafv2WebAclVisibilityConfig, typing.Dict[builtins.str, typing.Any]],
    association_config: typing.Optional[typing.Union[Wafv2WebAclAssociationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    captcha_config: typing.Optional[typing.Union[Wafv2WebAclCaptchaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    challenge_config: typing.Optional[typing.Union[Wafv2WebAclChallengeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_response_body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclCustomResponseBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_protection_config: typing.Optional[typing.Union[Wafv2WebAclDataProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule_json: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    token_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27031c2bbace2dbc7e68ca55f928a415dd19df0141062319262db824065cfedf(
    *,
    content: builtins.str,
    content_type: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d0e599d5588c7247a00fc559fae9d4eaae958dbb2f16ff3a3432105706ecdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47322b1b1540f42cd572573bbb3b9b07d589d6b7242758678620e3cf7d7d17a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7666c167522d45e6f7764eeb81527e01ac901177d4d65fd1873378d6ef6049eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a9e07ad9edecc9929f5912dcc53bb2a918821ffa27ace7026466bc04e3cf15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721f74eb2d25f839a2836e2f09329d774cd54f9e3be4df6918f638fb75f82f4e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0921c44b654ddcbbf7a78a96e9253da3aff86fa9b8a8a468866ed122c104e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclCustomResponseBody]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3e873a142452de1effcdeab5243f4a697466e77774bfc7a469c8a9a4cca8b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e866926df9b4ce5a6bdb1bb0b846425f7e4ae1884566dd3ce087f4083a2fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebcb086313c8387fed11fcd0307459f8dfe18f9c8b98b8edc120bca513aaf3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0dac2077c65e8926b4957a3a74d346ee3ad00ba0292641af1a89c337fee144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4990e95360f7159ecbc93f9bb59aea39a8f23890f637398d18130c676d1548cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclCustomResponseBody]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65536503bea380ff2aed83e16147551d1b1facde9b07868366899254bea55817(
    *,
    data_protection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDataProtectionConfigDataProtection, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce46cda844236ff719951f5b0d75d668e8fdb8f0d8d38d88cba03ec357bb5f49(
    *,
    action: builtins.str,
    field: typing.Union[Wafv2WebAclDataProtectionConfigDataProtectionField, typing.Dict[builtins.str, typing.Any]],
    exclude_rate_based_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_rule_match_details: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82f1840ef69d637b4e3a7a063d4cdbb828ac1d21b9055a4f4200f1aa779e482(
    *,
    field_type: builtins.str,
    field_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3210d5f51a5528ec15c7dd4d290159eb5400420cc92ffd46c0e3fda9486b57af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562190e77b0c6889c594c85337726641e9d360c1dee1f52361815d3986e209f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f90940fe02febae6fc052734d2f89f0113dc2276aea1505fc72af93be2d3d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5859b8b682f3c4ccbeba73940e55d63b4181cef7d9e833ee963c159b0c67f6c(
    value: typing.Optional[Wafv2WebAclDataProtectionConfigDataProtectionField],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66c5297f38a3a2118239c74a84733d8f5f0cd2e39e59ff2c1b98287ce273aa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd59f8b8b46aaf019252458824b2dee6a529cc6dd890d0d7567fe0098e18df9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c208f341d962cdb173a0c42ebc813d6edf044bcbf32bdf0b26c8040cbc683c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7bf67a39fe682085c700c05af8598fac6b207815c2ccd559ca70d9d09e6995(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9e438f958be9d5c76ed1915f5d335cb652df13ad9b5b93f9c3ee4e8652df5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bc084278c559df7fb8e987b4e71ab00c08efa487b66f3466d16373df92b5e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDataProtectionConfigDataProtection]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e13d6d54b5bf066b58d949494f559737c31652e2df2bef6ae05baac3561626b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b7a403199b5de9ce16c1ba74cae791e27a825952b2f9291344fab3a757827f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5307d63de19a8eae6be6f28daee6af012ee3f012960fe3f2442b9a9e841f3e8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a24fad030424084b072a0c5e6cee9a3ccbe8275542801af1576469c8c77d85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f0132970950a8363c6a43dbf86b2cde8b0ffff20dd9acc81d3b16149d0091c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDataProtectionConfigDataProtection]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c30b8eeb5038f87faad9a0aa8c8a34cafbc238204f71fae416d72db138ece2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a6a39d84713a8880a06c800922f08dd40b577fcf94c4462710c2edb5657939(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDataProtectionConfigDataProtection, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eff751257c2bb55e4a295add897e9b0bbb4e1b02610aec3141292e66fedb031(
    value: typing.Optional[Wafv2WebAclDataProtectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4a58b7a138a69876a24d6b0ff3770c1d0b7cda15e70b072707781f01c7126c(
    *,
    allow: typing.Optional[typing.Union[Wafv2WebAclDefaultActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    block: typing.Optional[typing.Union[Wafv2WebAclDefaultActionBlock, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af86cfc41cc8ef145d6041671d5594b3d4f622728a8192d52933f8e41df48291(
    *,
    custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclDefaultActionAllowCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bf2a7dc57bff17a290ad6de2a5e1c2a40fa52c433b432ee2e589016554692b(
    *,
    insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cd4756099f26c0ae026786b0bc9637bca6e82b0bda1594aa7e270904d217f6(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2e1b764dc4228642a05f8afa0569854d42e91049b52d80d966c0afc0862c26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50abf5f9366698fde0ca6ec52f9e5880b4f390968b2888a69c9efd0b9cf8abe7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b265618589b584f7922ab5f08ac4426610ae96e9d15fb237149ebd951816af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d11c348495aac2d67da831170bea9f8274f34923c2a2b5c87b97ddf56817ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96108dfda3c1087f91f7bc676da2582b7e2d7546dcb0d451f1916336a72fc823(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eedd661be75b2988bdbc723e5466506eed8d23511218032926506d6242d8a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056821d4665a3e16bcf5cb505c8c683ca65a79e85eea48db036903ef20872ad1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055e58f9316452609b9140ea1145a17f034ff88e92b797e4748fe950f6a0548d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73cdb3fe6a3e25a707a395f2a1eae384303ab309e6a82df23fc234bffb246be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3b0aa992ab75a4820b4212c2edacb36a9eabc58f5a7822550b52583415daa0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19e1b66b0583a254e845638cea52b0398266a40ad2fa29031b0204a85c2b8f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a2268f0faf31826ba7b2c8cfb4b8f9b3066df06d415304b8cf7ee87b88ebd3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47934563bc7ba2c96634ffa1b4386c7cc9e48f847d6b86da1c55854c4a7d6400(
    value: typing.Optional[Wafv2WebAclDefaultActionAllowCustomRequestHandling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2c3e20b51d160d575a8955846a368fe67037757c6ba770bcb753027d053123(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4c1c41a9222c42870e598607635b019b4943b09e73f66d6bd48126681af6b1(
    value: typing.Optional[Wafv2WebAclDefaultActionAllow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9077ac5ca0858b9bf08a98ab163b9d861cd5d6484340c2d214d7f56cefe75685(
    *,
    custom_response: typing.Optional[typing.Union[Wafv2WebAclDefaultActionBlockCustomResponse, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccee0ab071048e311df083a47fc200282e3fa3f23fb79068d9a58c38e59f40f(
    *,
    response_code: jsii.Number,
    custom_response_body_key: typing.Optional[builtins.str] = None,
    response_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41be0f86f99286111bdce5504d1dd1751da69c8ef8e5dae4ee8926420d7bd7e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1190509cc63121d434f17e4ba92e78c025e51650c96863b440b82b86b29108f4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671d78b83c516966ea3b9c6b6c2c9f44df0e13f6358a2b1c005cd5f065150db6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64eb204549ef3d4430c18b59ef76e3583299ef8cedb1af8c870f4e120e048cf4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c5a3f2c5ecd6afbc41d3c833cbd2e4c4a34effef9cc2020686b657f923ce62(
    value: typing.Optional[Wafv2WebAclDefaultActionBlockCustomResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df48ca27128d53ad157a7713ad567078d8ad9599916ad6a43708c70ca459397f(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b4a786248ebf167165aad5edfc866d09ef7b966664df3db32dc01b2e313220(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176228f720436728fcf8ac96be11b265e2bdc8054d4dca2fd64ef20d3eba9583(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7d9f50ba3d40952e4021ed60f552ff9eff394e2700e7d8c1e8c935f355247c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a9022e2a8fe15e3102051ad81c3f2ed9cbb7adf87ed39feee0ab8844cfe16a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79ea437b76d99d683e3efbe9a2ff3f68cda8765648ed2b7774565d853900c65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf5ef509fe8731c5f932ac975f76a5aad10bc90a6189f2829e4830bff95af52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a59fa116648e776d0d1bf28734d3cfacb3b5529d479422d2dc26b3a63e14c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79183a152dcff2e5dddf7d46a26553e9bba11e6eaa4ede0ae208c1e6b43049ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf3dc7fd0a1f6b36db979a74d2d0aa0ea1aaf799cd18cceb75eb599bc653b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd85cef8ec9d535aaa13a50f657171c9998c6903369ed99f5737ff946c3b9c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclDefaultActionBlockCustomResponseResponseHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f448e6d4151e5673f276513ba0f97ddd43d14004c06435da363b6f0fa5a7ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a926c7eafb04fd976961c7d1a72f81c3bf8338ca2ffd002bf5baa26d7a30c9(
    value: typing.Optional[Wafv2WebAclDefaultActionBlock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f843f9ea13b95ae863333fa142d908111a02a2461d0cc72284efce5ff3aa3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1760e3c1c722ed4248d318089816e56d0c55fc9d1ba1fd067fed734c142a11b(
    value: typing.Optional[Wafv2WebAclDefaultAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fe2b8063ea5f2d7c3585567705a86d100364548cee1202715ca67038f73c8f(
    *,
    name: builtins.str,
    priority: jsii.Number,
    visibility_config: typing.Union[Wafv2WebAclRuleVisibilityConfig, typing.Dict[builtins.str, typing.Any]],
    action: typing.Optional[typing.Union[Wafv2WebAclRuleAction, typing.Dict[builtins.str, typing.Any]]] = None,
    captcha_config: typing.Optional[typing.Union[Wafv2WebAclRuleCaptchaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    challenge_config: typing.Optional[typing.Union[Wafv2WebAclRuleChallengeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    override_action: typing.Optional[typing.Union[Wafv2WebAclRuleOverrideAction, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleRuleLabel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    statement: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89721362d6d591d68d8ff0b68aeca965263bac4a908015f996997d24bb253f53(
    *,
    allow: typing.Optional[typing.Union[Wafv2WebAclRuleActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    block: typing.Optional[typing.Union[Wafv2WebAclRuleActionBlock, typing.Dict[builtins.str, typing.Any]]] = None,
    captcha: typing.Optional[typing.Union[Wafv2WebAclRuleActionCaptcha, typing.Dict[builtins.str, typing.Any]]] = None,
    challenge: typing.Optional[typing.Union[Wafv2WebAclRuleActionChallenge, typing.Dict[builtins.str, typing.Any]]] = None,
    count: typing.Optional[typing.Union[Wafv2WebAclRuleActionCount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5cc2fc7cbcfbbfe97ae25f7b501a04189b75d4e9fa3d92f36d1c8726d22824(
    *,
    custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionAllowCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee4329a8d53bf4a9d4eab6affc8cf1be53c7019a80b55ba5b0f494bbe69acb9(
    *,
    insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c79db5986ce2b026bfefc5a00516737006bfcd864cdc617e6d3427cf160cd0a(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566297cb25407a21410a4ea34b72a5aaaaea8ae4a8db7ebcfed75d111f89892a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e8ab5401ef71d4d9473c082e6d617f14964a7e50b7bd51631f78d0cea494de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e92317a0e0f4c4551796b62df4705f15a8ec5678c9b33a6f0c3209e77be442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31a8c0016ddd74f8189320f3e7a7d88ba297644596f30869d9a1b86320ad1a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5eb6de56f4a437271ce3aa21c2321c2bb31f228965cd6915b709477c2d8e82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ac2601961d2bd0b7296d4b288ced3c54f730019fb13f5bd333d0e46027e5ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8e53b99e5ec759091b847b7c4e58d39ba2ff50323020dd0076dfd50c72025d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05935057e53dbe336f44ed5f1b1a169f8df19a4df078b38add94b877a24b1b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdbd48ce2a769e3ecabf076f3bd938762f7e88ee2d109106ada04485d3ec50c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123e751c630edb4be6735aa02389ae50474e730321c3f67b5d367a92daa86040(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0945e5c95998737f2e89ace96b17510549afa5f26cdfe3a350af6104d64a52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e22700d0a93db74337a660ed266f4d2637728ed326ebc15ca3d1129a07a927(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionAllowCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54227397dd44db8d64eef809b7c9c3d01df20104736c32db91a70938c9481ed7(
    value: typing.Optional[Wafv2WebAclRuleActionAllowCustomRequestHandling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536306b6380dbd8413dbd10779be9514f5d8ba7b699d6bf69e46cd7e92e2a20a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d771952097d71104cef5b969b247bdf7141b25249b30cb9b6ac3ab3546e8f2a4(
    value: typing.Optional[Wafv2WebAclRuleActionAllow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f458f2a2f01072567fc6273e9e503884397f77d6689be6af3f294b16cf6ef397(
    *,
    custom_response: typing.Optional[typing.Union[Wafv2WebAclRuleActionBlockCustomResponse, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98c39088889cf991f3c1cf14fc6b3010743e0e98238ead317acbc869fbcce96(
    *,
    response_code: jsii.Number,
    custom_response_body_key: typing.Optional[builtins.str] = None,
    response_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4098b617c595c91483d8bb456a3c3fb523c1c127cc51bbe367f84dd09dfa8cbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b52fc09347e0f7d85ce3e66190a73c3c3beba0029f0a458c5c20ef24cd4de2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903ce2aba843ad33024de13915f42ec3fb2c7c4803fc5a7b82920743f06a3bd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fb6da3c39e3d1d7c27eb7e4638a87fc75d37683b56b6c7a63dc9214e06c415(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c970bfc1d7aaaf7ec0e04d5460bf55a8fed99060fdd0eff8b8aa8fdf8b63cf(
    value: typing.Optional[Wafv2WebAclRuleActionBlockCustomResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4e9e926f3c80f3c9422e8c727c1b2383be0fbdbf60fbada4cf1a8412583cf7(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec937daf27159b3d0ddb913333720ad7af069a66ace9385f65f232481e2f014(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61105db2742fc304dcb444167141ecf2a77beee689033c86c94dcd05b7627d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8322fa545d19c462429d02249fc87efe0a7b0133cb61c884008a179f89a03897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc3d51e168d9c3b99dc0b8aa5488a8fdee8c1c630f400addc8e023961ab0d38(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39293f59b712940b9e26179842aac8231b040c3d8967e4bf711e1891df7f66de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b943083a8a6052f5988d646a3dfff9e1d4cea725f6550dc8cb3b567b3792dd31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a2196c183061ea846ee56bf1893d4d870ea0a10f98336f6289cdcafaa4b87d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe479518a432cd296d00233657d4cca4e6e291903c539691c0ef6dde7b1020d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d9b53be249b0ccfc2b86a3d47605365cc10ae0b7236fe5a49e6732af8d1952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147bb6195249a443560bbec1ca8ebb1c5c411342c1fa2bd9ce95605ed4e1056b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionBlockCustomResponseResponseHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a5cba1f2f68cbc67c36be3c6b47aece966d279a46f475545e537de7d641dd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856ed8b300603e9f6968f627fa2a094141c29ed291d35a98de111f64220b0286(
    value: typing.Optional[Wafv2WebAclRuleActionBlock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271475f47888c6045fbee335616c8f0c18965c49729e10f449ca5ac42adbae2b(
    *,
    custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionCaptchaCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b706967092b79dafe1837be0d391f981d7b628314cb8fa76981b92c823b99d(
    *,
    insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d951557f40bdb6d5080cd74a7665de0a6ff1b6e2b2955f6911608a8b834368f(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79081d342625849893aa2380e9e07db0c615795225eab0c5dd8af5568101338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299cdc2eb48b549ee0d833e04c1b096db358ca31857107cb8f8764ba64a22393(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c116f1b35d547269a5f25af233f4b0e86101093fd7b4ce9b14153e1d3eb08eac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18e0a864d831bccbb82ea8fcf9798fdca0684d80a4df582fe4d4e736158e18a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383d25da294ee9e4d29d77e5ea6f463b34cc7051ef782de66bc146557e13d7e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4b78d48ad77298798cd6ec461c3f887c9301f6ce9eab2fd5baea55f723c280(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156645f1f2dad445da1ceb0348574c85dbc605c4722c520dcd7750ed7c75be79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f784758953371a13a8f81a8c78274f8ca9f206742eab5a01f324a90e32f913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49167a91cf93a3a7b1858618e7eb1f889fd0a56f0842001549a09cde7bda6218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200aeec50ed624a442bd810eac1945bb474fdd8e31915f351d1bc7a3c83af046(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935c72b02c573fc40efe9a4df4c19ead64086c05f88d97d53a74a1fae1094825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ae18b76bac6aeb55f4e5ac982bb1efe6917be8ff54958136065a240e0be09d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCaptchaCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2503777da66375c813b0d4def8084ab8132d83d09afad17f6134fe2873fd62(
    value: typing.Optional[Wafv2WebAclRuleActionCaptchaCustomRequestHandling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376443ad441882123fccbfb375d73331dabd389e2ef317e4341b4bc4b1196418(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67810f2752b373cdd0cd9b701b3363816ca16131cae47920b00ba28d19ace581(
    value: typing.Optional[Wafv2WebAclRuleActionCaptcha],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5593fc33b2dfcaa0a0e5ebb288641cdb3826f59371b1182a78a524a716a781f5(
    *,
    custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionChallengeCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54b52ff882bd2bf164aa568da5f33abd839b52074676badb620d980b4c68da7(
    *,
    insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcbf20391e08eceb9bc521bf6f2a6211cf886e4f51decfeb79b3e0a7c57ef83(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d53a6f1e42c31ad9ab7ac4970b0b7fc06ca3f6c0524093fa4665e144bb45920(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81e99592e5d77fb51d02747d523f3bc79f8a641e1b656156e0a2454fefeaaff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c970cf6470b6a4b4328b7033d4997d5f7c9992f388f4fed0d7d4d4162b06c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76240f39e86a19cf6ce126d54f904df77be940fe2bfabdb46d2894c56becc485(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27e8114af3b71813097dfcc8a8e66fe8f30228004272fc9cd2120a4869744e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3956fb61a59897f07a0e84cc0699eabe643a849d908c2879c6cdcfdde13b7a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3e57e5c52e7ccefe94cb13b30e04f0ffacb2c1fa37fe14c46adb2538e6d48b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12dd9ea70a029ea9978537d069ea39ac7423d9a528f005c73345309988491d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1397f8eaecc0281cd473bbc7d58fb1c2b64bbc0d1050c01f25856439cc4ca80e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d81deade3d9cd2a3984892c9f8c2d119bf5d3d1d3a5174679c2e8ac3e87e260(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f55a760b1ae07d6ac53cb5023a295702916ba0a028957f862cbde021c313734(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b007473458038182ddcffe8542e2f766ced5f8d33204f61912b8023fb63710(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionChallengeCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7069ee6acce60eec74fc41b7ea1ea4285ad77774395ab4e3138df4c6bc6aad(
    value: typing.Optional[Wafv2WebAclRuleActionChallengeCustomRequestHandling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cdc57849fc47ee7066468ed10cfc8b1e677d9cd9c4e0dd25f121e479ff4e8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364c66f7ab235c255f6ee6b5821e74744a738cede14ca64b661416fc276236d2(
    value: typing.Optional[Wafv2WebAclRuleActionChallenge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3115f3af8ecad5b45b4175dd14e03a5c19a09eb48d933cdb81436a4114fb825e(
    *,
    custom_request_handling: typing.Optional[typing.Union[Wafv2WebAclRuleActionCountCustomRequestHandling, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b24362410a16116021578d3396ee57de3a64c5b0e5b0fff5439aff24efb3c7f(
    *,
    insert_header: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ad86827405d5009c80cb4628ed61e3b926aa56c783ba246f22fc6b6de6b637(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908e3d2cb2e950b6fcd152951ead5807cf7a55daa6b4fae1ee0de62b06fb7022(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605656f5184e87dca1e947843adbe1046f17f4e2b95950c3da8119e614084142(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c095dddf3abab740798d68b03c48eeb64934d2a069c6733009f25eb8368bc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99c12178963879f0ddb9434aaa609c9f2dbc60cf47fd5a3572841a240f453a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d102e0a97009e7ca9cda9d1e5bd055e82657863ab74b130959db83228351c426(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718ef5fe68224f45dd59a229bdafacf7f6d5252f2c826ae55f4815ace66f10f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02defd4cf711189763f688362eebc8eac03c3f06dd78aa440cf3deb3c3952547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f235829d2534d09d945e0f5a022a1d461d29be90c70db96992234ee7238095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42b3205b84260af663155970aa000d0ff03e5188401d38704583ad1d0084609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e84c1988c498b53855fbb29811a9757f6b60eb491dcfe25023d645f8a33154b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f20b0d10806631d4842ae6002f50178cd10ae0df150cc730d599df77f5670ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb147591911bc164821517c6ce04c57b88eb7f67eede27029e40ccfe92222dc4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleActionCountCustomRequestHandlingInsertHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fa7c8167aa0a86a9dba76f7472633961559cb993688e9134df65688b4d5c52(
    value: typing.Optional[Wafv2WebAclRuleActionCountCustomRequestHandling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64badc41138ad03158869d9ded08b33bbd425826771fc6f901463363c1f8ae91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ce0b3433719ccb6f487804350a01b2a40ac0723b822064648cfe4dc88ce6ae(
    value: typing.Optional[Wafv2WebAclRuleActionCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf273dc1cda317eeaf1d79e89efaa6ebd26d0044bcc8fdbf87186bdb3cd94e01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282b503640bca96ca2244dcd27a3140a66d28e13826505903a38a4145ca8edcc(
    value: typing.Optional[Wafv2WebAclRuleAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04597b66260a0965657d273288c439afeb708cca00e939185585e3040f19be21(
    *,
    immunity_time_property: typing.Optional[typing.Union[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a15dc9c5165382d2892a55f4ab456c9e310b3c7c579a5fe4345f0d54fd70b5(
    *,
    immunity_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c5183ae55fd5c48e8c312130599b81ef59b4c64b25e8e333d2e19e1d6cf878(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942c3dd5ef3410d54efbe6f5743cf36e1dadb6d1c0d5b466bbaf558ea7035e07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7350ddb2b3fbf929042aae5a77ac451a5c68b6888fa7e79ffae4c75e6f0009e3(
    value: typing.Optional[Wafv2WebAclRuleCaptchaConfigImmunityTimeProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d813952abb0ccaadb802860a449a20d091aca909e6c1cae5ed7ea0d40eee972c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f336c71d13119b6a8d413c61acff69b1b54a07cf027fbd667157592950dd378f(
    value: typing.Optional[Wafv2WebAclRuleCaptchaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdc0b3a2c3e5401fb7ed8dfd3a144a73566890bba0990fe1a9e51badc1ecf98(
    *,
    immunity_time_property: typing.Optional[typing.Union[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47ee6b57e4d7f61351c4dbf4d99074493522d081a6f11f1440a6275852f956a(
    *,
    immunity_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1ce759158a36ac79b1ab8da48a63aa7b461c08c9b074a6108fe4fa5939320e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ad9578415c71639136990d7d636cd7b020281eb295f95022c07cb0c4507499(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aea1414fbb8775a50deac05e307423dae0805d47d59ec26dad86d54118e8404(
    value: typing.Optional[Wafv2WebAclRuleChallengeConfigImmunityTimeProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb058c116afb58284b95297cb8a78ee44544fd132547e42149b13663ca12975(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c74fc926f7f8851f97b025113aaa27abb9b47cebdb19a826a9838cde8b357fb(
    value: typing.Optional[Wafv2WebAclRuleChallengeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a63e8753d69e2aacfb8ce31e3ea796383b3b9ac1084dbfdeab3f49bf597a667(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0462143547db82c66042c3947d3eb350e8096c9024ccbff4090d3e7d69209991(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f11bd445a617843ead82c289cec7bbc1e9a6e906d9aef0fb124f5bfd5c3bdd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbbd0a13ed95d7e72edbddbe40a9ba848e1cb0cc80265f9c5c0ef7295a6f2ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f60126725e10d8a1bc1c9fd03c153bed475330603241f7069697a61dfc27bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf8038a4c83c071023157c0c4448c7e304fe04fc0c51a1e26ca2e8f160e083a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dbff4d6e22a1915a7d3f1e4e349591dfeb5aef93db65fd833af27b00b1f892(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937fe0182bb7eef5e5d45153cd133f93e520b59aa96af30613da6bcc9883968b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclRuleRuleLabel, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9128c3a9051ce94f639bd98acedb0242d0b4ee4da9bf9da4fcf1a291722f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7285d4a6d12adf1272b60bd32c8b44cfe0365919bc2b9ad8dc9ed14097a86aa1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c176be72d5bb069415049dce9755aab2d6d6369d601698a3bf88f460ffda912(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa9768eb949386c353397fbe15b3162f9c8d8f8f32a4d2a05647693c1d14969(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1d4f05d13811d3d6390860c51ca3218bbabca4bde76aa6a4ffb576ed96acc4(
    *,
    count: typing.Optional[typing.Union[Wafv2WebAclRuleOverrideActionCount, typing.Dict[builtins.str, typing.Any]]] = None,
    none: typing.Optional[typing.Union[Wafv2WebAclRuleOverrideActionNone, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53d64b98948dced8d92f7b4274f23b8c647c62b23c8d861603f40a68ef136c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35864858c1829b77c7177d787271fe482a742e33ddd5597424e89c39cb083e1b(
    value: typing.Optional[Wafv2WebAclRuleOverrideActionCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120e271cae5e4e085cead380307141b76b47e66167e155e8728a03eaf5ca2c15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd762a3ff78fc969f8fe4aa69dbeb83cb9a7d2bca558b767dd6ebb4006016e2c(
    value: typing.Optional[Wafv2WebAclRuleOverrideActionNone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fb5d0ed6b23894bdcc8a73f0a3abe93c12739b8081d519c53ca5630252e2aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bcfaf2e5320cd9185bd28b337904489876ecc723c33211b1b738e4ffb1062f(
    value: typing.Optional[Wafv2WebAclRuleOverrideAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2906a084030046f665e326c207883eeed18790cb800663455913d0bab04b7b9d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1fa00a17e8eeac9ddc1a334ed7d91f598c2f53b4546a276fe1c0f6cfa052be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b8f52e6be1579ed5c2bd747932a7a0f73eac1437d922d9278b1b47c0800a24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5f7c3adaa4ff8d4170aa8e56275c7342cf3fbbad45442428972746c5a91790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53abcbac0d068ac9b0de6c552a223e9fcfc879f36b5f8e46510734cea42c358f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5f95c0d27dce14257b25aaf5865800bbce861452ad6941d6d25e6912635d88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8cb16fd6d9364d865c6f65d86a1cfefadf03084858ab1a24b7a503d7b51ffa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclRuleRuleLabel]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebb78d7104238f4cb257942814925a59490eb13a301a9f34f6e527b615abd35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a0557ca19ff9ffa316bbd6c5ea02107161687c38d221982b1a2bdcee440aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffb031513ce5d4271e6bbe106f7c673d0a21e7dba951ad2d0ffb550b43a6ae4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclRuleRuleLabel]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dcff26991aa8a3b61a74813e163b210838da6a92b4e1d88efc0cafb6dbfad1(
    *,
    cloudwatch_metrics_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    metric_name: builtins.str,
    sampled_requests_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bf83f5d6e403e961cb64335cc5e32e99b5b8cf34a8fa5c984645653b0372aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c864e9c088fd4edbae2ba21a5f4e96c92529d3bc2bac33e819277e86a80840(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995ad7e1c6d5d2956285f05c8d9e6f6e7e821fa4ae1ac1ab6cf7c817e8f7316a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d501ae8826460352d42ff1b09ddb0833fb78158c7c935cace342e4e077fb9f96(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efb4f5ae5625414608d8b1b8f3ff43b193123d03d2cec960126e370ddc5baed(
    value: typing.Optional[Wafv2WebAclRuleVisibilityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae273d2b29feb830a63ebcad84dde341ca21b54859741e999fa490626cc4ada8(
    *,
    cloudwatch_metrics_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    metric_name: builtins.str,
    sampled_requests_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c677fdb201627c4ade6d94f172f08f391401901f87bdd51b8526f0cbf168a44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e061e7830e08caaa980312268ca20f2f2b99c4cd1212038b2f5e23bec1ca0503(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa75186d17efa0b0b19c090f9b0606140ac561e7aaf2cfdbd877f044ffad203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240e07cfe7c2e00c399587ac7e659b0198bd58206524f44c54ad5cac9fa6dc70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545229753b7262b15e285354f02f72dfcf483bdeecce4816048e8d218f367705(
    value: typing.Optional[Wafv2WebAclVisibilityConfig],
) -> None:
    """Type checking stubs"""
    pass
