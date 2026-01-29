r'''
# `aws_bedrock_guardrail`

Refer to the Terraform Registry for docs: [`aws_bedrock_guardrail`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail).
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


class BedrockGuardrail(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrail",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail aws_bedrock_guardrail}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        blocked_input_messaging: builtins.str,
        blocked_outputs_messaging: builtins.str,
        name: builtins.str,
        content_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContentPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        contextual_grounding_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContextualGroundingPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cross_region_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailCrossRegionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sensitive_information_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BedrockGuardrailTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topic_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        word_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailWordPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail aws_bedrock_guardrail} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param blocked_input_messaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#blocked_input_messaging BedrockGuardrail#blocked_input_messaging}.
        :param blocked_outputs_messaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#blocked_outputs_messaging BedrockGuardrail#blocked_outputs_messaging}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.
        :param content_policy_config: content_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#content_policy_config BedrockGuardrail#content_policy_config}
        :param contextual_grounding_policy_config: contextual_grounding_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#contextual_grounding_policy_config BedrockGuardrail#contextual_grounding_policy_config}
        :param cross_region_config: cross_region_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#cross_region_config BedrockGuardrail#cross_region_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#description BedrockGuardrail#description}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#kms_key_arn BedrockGuardrail#kms_key_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#region BedrockGuardrail#region}
        :param sensitive_information_policy_config: sensitive_information_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#sensitive_information_policy_config BedrockGuardrail#sensitive_information_policy_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tags BedrockGuardrail#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#timeouts BedrockGuardrail#timeouts}
        :param topic_policy_config: topic_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#topic_policy_config BedrockGuardrail#topic_policy_config}
        :param word_policy_config: word_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#word_policy_config BedrockGuardrail#word_policy_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89679a72b300b92734c8d2e4aec78dfd2b4ede2488d25427753f25c70c97d70a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BedrockGuardrailConfig(
            blocked_input_messaging=blocked_input_messaging,
            blocked_outputs_messaging=blocked_outputs_messaging,
            name=name,
            content_policy_config=content_policy_config,
            contextual_grounding_policy_config=contextual_grounding_policy_config,
            cross_region_config=cross_region_config,
            description=description,
            kms_key_arn=kms_key_arn,
            region=region,
            sensitive_information_policy_config=sensitive_information_policy_config,
            tags=tags,
            timeouts=timeouts,
            topic_policy_config=topic_policy_config,
            word_policy_config=word_policy_config,
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
        '''Generates CDKTF code for importing a BedrockGuardrail resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BedrockGuardrail to import.
        :param import_from_id: The id of the existing BedrockGuardrail that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BedrockGuardrail to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf15f6ce84a9a722232c465e06a98919853377be40c7d48190794b72a3c84c70)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContentPolicyConfig")
    def put_content_policy_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContentPolicyConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aec3f0b81ab68ed0a7cdb27e15aa252049bdf9b97946b0d93be9d8e84ecf8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContentPolicyConfig", [value]))

    @jsii.member(jsii_name="putContextualGroundingPolicyConfig")
    def put_contextual_grounding_policy_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContextualGroundingPolicyConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48797a4fecbb10af82b1856b4dca29869096c93ab07a2cb360f117ca84eccfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContextualGroundingPolicyConfig", [value]))

    @jsii.member(jsii_name="putCrossRegionConfig")
    def put_cross_region_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailCrossRegionConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8807dc1910475a7a2dd8018860175665fe0b5164b3d438e55e84f69c2e39dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCrossRegionConfig", [value]))

    @jsii.member(jsii_name="putSensitiveInformationPolicyConfig")
    def put_sensitive_information_policy_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d962950aa15b3a41c5a46051726ca72adbae87c03639b9feff409433672840e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSensitiveInformationPolicyConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#create BedrockGuardrail#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#delete BedrockGuardrail#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#update BedrockGuardrail#update}
        '''
        value = BedrockGuardrailTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTopicPolicyConfig")
    def put_topic_policy_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f1869e8588b0db501af561c56bc63b0ddc1bed511fda487ef174f63453db71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopicPolicyConfig", [value]))

    @jsii.member(jsii_name="putWordPolicyConfig")
    def put_word_policy_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailWordPolicyConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc71905690b0215d05f721776fb501a72ab438809e9b14907b417c99c193b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWordPolicyConfig", [value]))

    @jsii.member(jsii_name="resetContentPolicyConfig")
    def reset_content_policy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentPolicyConfig", []))

    @jsii.member(jsii_name="resetContextualGroundingPolicyConfig")
    def reset_contextual_grounding_policy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextualGroundingPolicyConfig", []))

    @jsii.member(jsii_name="resetCrossRegionConfig")
    def reset_cross_region_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRegionConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSensitiveInformationPolicyConfig")
    def reset_sensitive_information_policy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitiveInformationPolicyConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTopicPolicyConfig")
    def reset_topic_policy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicPolicyConfig", []))

    @jsii.member(jsii_name="resetWordPolicyConfig")
    def reset_word_policy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWordPolicyConfig", []))

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
    @jsii.member(jsii_name="contentPolicyConfig")
    def content_policy_config(self) -> "BedrockGuardrailContentPolicyConfigList":
        return typing.cast("BedrockGuardrailContentPolicyConfigList", jsii.get(self, "contentPolicyConfig"))

    @builtins.property
    @jsii.member(jsii_name="contextualGroundingPolicyConfig")
    def contextual_grounding_policy_config(
        self,
    ) -> "BedrockGuardrailContextualGroundingPolicyConfigList":
        return typing.cast("BedrockGuardrailContextualGroundingPolicyConfigList", jsii.get(self, "contextualGroundingPolicyConfig"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionConfig")
    def cross_region_config(self) -> "BedrockGuardrailCrossRegionConfigList":
        return typing.cast("BedrockGuardrailCrossRegionConfigList", jsii.get(self, "crossRegionConfig"))

    @builtins.property
    @jsii.member(jsii_name="guardrailArn")
    def guardrail_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guardrailArn"))

    @builtins.property
    @jsii.member(jsii_name="guardrailId")
    def guardrail_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guardrailId"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveInformationPolicyConfig")
    def sensitive_information_policy_config(
        self,
    ) -> "BedrockGuardrailSensitiveInformationPolicyConfigList":
        return typing.cast("BedrockGuardrailSensitiveInformationPolicyConfigList", jsii.get(self, "sensitiveInformationPolicyConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BedrockGuardrailTimeoutsOutputReference":
        return typing.cast("BedrockGuardrailTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="topicPolicyConfig")
    def topic_policy_config(self) -> "BedrockGuardrailTopicPolicyConfigList":
        return typing.cast("BedrockGuardrailTopicPolicyConfigList", jsii.get(self, "topicPolicyConfig"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="wordPolicyConfig")
    def word_policy_config(self) -> "BedrockGuardrailWordPolicyConfigList":
        return typing.cast("BedrockGuardrailWordPolicyConfigList", jsii.get(self, "wordPolicyConfig"))

    @builtins.property
    @jsii.member(jsii_name="blockedInputMessagingInput")
    def blocked_input_messaging_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockedInputMessagingInput"))

    @builtins.property
    @jsii.member(jsii_name="blockedOutputsMessagingInput")
    def blocked_outputs_messaging_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockedOutputsMessagingInput"))

    @builtins.property
    @jsii.member(jsii_name="contentPolicyConfigInput")
    def content_policy_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfig"]]], jsii.get(self, "contentPolicyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="contextualGroundingPolicyConfigInput")
    def contextual_grounding_policy_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContextualGroundingPolicyConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContextualGroundingPolicyConfig"]]], jsii.get(self, "contextualGroundingPolicyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionConfigInput")
    def cross_region_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailCrossRegionConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailCrossRegionConfig"]]], jsii.get(self, "crossRegionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveInformationPolicyConfigInput")
    def sensitive_information_policy_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfig"]]], jsii.get(self, "sensitiveInformationPolicyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BedrockGuardrailTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BedrockGuardrailTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicPolicyConfigInput")
    def topic_policy_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfig"]]], jsii.get(self, "topicPolicyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="wordPolicyConfigInput")
    def word_policy_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfig"]]], jsii.get(self, "wordPolicyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="blockedInputMessaging")
    def blocked_input_messaging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockedInputMessaging"))

    @blocked_input_messaging.setter
    def blocked_input_messaging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846272fb55b40e879aff759856b8ea6e3de1230cb8c9da05b684a14576ca3a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedInputMessaging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockedOutputsMessaging")
    def blocked_outputs_messaging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockedOutputsMessaging"))

    @blocked_outputs_messaging.setter
    def blocked_outputs_messaging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e41418248c163f6885c17f3f985cd0e5a358a2ebbc65d95a23c0b4d96aaeb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedOutputsMessaging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b7bacf5807e86b7afea7c8c7ae5f521953a38206b2d7794a77ab5c696b847e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71503680e5a32197d8a664ab2d7f32c403abae18f34d688e72fe43a972ccdc6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62304004a822227874b07faae546c388d289f249b8a8e82b790f55188e30e886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351189ac15f7a3a0694d4144b8e68bbb5dc12cfa8e1d3064ac4323dd0df85250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21e45ce0266cd6bcfcf1c7730d4b360b599838bc367d1bf6b7540eb68bb103f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "blocked_input_messaging": "blockedInputMessaging",
        "blocked_outputs_messaging": "blockedOutputsMessaging",
        "name": "name",
        "content_policy_config": "contentPolicyConfig",
        "contextual_grounding_policy_config": "contextualGroundingPolicyConfig",
        "cross_region_config": "crossRegionConfig",
        "description": "description",
        "kms_key_arn": "kmsKeyArn",
        "region": "region",
        "sensitive_information_policy_config": "sensitiveInformationPolicyConfig",
        "tags": "tags",
        "timeouts": "timeouts",
        "topic_policy_config": "topicPolicyConfig",
        "word_policy_config": "wordPolicyConfig",
    },
)
class BedrockGuardrailConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        blocked_input_messaging: builtins.str,
        blocked_outputs_messaging: builtins.str,
        name: builtins.str,
        content_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContentPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        contextual_grounding_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContextualGroundingPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cross_region_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailCrossRegionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sensitive_information_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BedrockGuardrailTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topic_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        word_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailWordPolicyConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param blocked_input_messaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#blocked_input_messaging BedrockGuardrail#blocked_input_messaging}.
        :param blocked_outputs_messaging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#blocked_outputs_messaging BedrockGuardrail#blocked_outputs_messaging}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.
        :param content_policy_config: content_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#content_policy_config BedrockGuardrail#content_policy_config}
        :param contextual_grounding_policy_config: contextual_grounding_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#contextual_grounding_policy_config BedrockGuardrail#contextual_grounding_policy_config}
        :param cross_region_config: cross_region_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#cross_region_config BedrockGuardrail#cross_region_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#description BedrockGuardrail#description}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#kms_key_arn BedrockGuardrail#kms_key_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#region BedrockGuardrail#region}
        :param sensitive_information_policy_config: sensitive_information_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#sensitive_information_policy_config BedrockGuardrail#sensitive_information_policy_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tags BedrockGuardrail#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#timeouts BedrockGuardrail#timeouts}
        :param topic_policy_config: topic_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#topic_policy_config BedrockGuardrail#topic_policy_config}
        :param word_policy_config: word_policy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#word_policy_config BedrockGuardrail#word_policy_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BedrockGuardrailTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e30826463460cd2647edc423fb15a8b83d4ac5dff3aaf26679822947a60695)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument blocked_input_messaging", value=blocked_input_messaging, expected_type=type_hints["blocked_input_messaging"])
            check_type(argname="argument blocked_outputs_messaging", value=blocked_outputs_messaging, expected_type=type_hints["blocked_outputs_messaging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument content_policy_config", value=content_policy_config, expected_type=type_hints["content_policy_config"])
            check_type(argname="argument contextual_grounding_policy_config", value=contextual_grounding_policy_config, expected_type=type_hints["contextual_grounding_policy_config"])
            check_type(argname="argument cross_region_config", value=cross_region_config, expected_type=type_hints["cross_region_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sensitive_information_policy_config", value=sensitive_information_policy_config, expected_type=type_hints["sensitive_information_policy_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument topic_policy_config", value=topic_policy_config, expected_type=type_hints["topic_policy_config"])
            check_type(argname="argument word_policy_config", value=word_policy_config, expected_type=type_hints["word_policy_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blocked_input_messaging": blocked_input_messaging,
            "blocked_outputs_messaging": blocked_outputs_messaging,
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
        if content_policy_config is not None:
            self._values["content_policy_config"] = content_policy_config
        if contextual_grounding_policy_config is not None:
            self._values["contextual_grounding_policy_config"] = contextual_grounding_policy_config
        if cross_region_config is not None:
            self._values["cross_region_config"] = cross_region_config
        if description is not None:
            self._values["description"] = description
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if region is not None:
            self._values["region"] = region
        if sensitive_information_policy_config is not None:
            self._values["sensitive_information_policy_config"] = sensitive_information_policy_config
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if topic_policy_config is not None:
            self._values["topic_policy_config"] = topic_policy_config
        if word_policy_config is not None:
            self._values["word_policy_config"] = word_policy_config

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
    def blocked_input_messaging(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#blocked_input_messaging BedrockGuardrail#blocked_input_messaging}.'''
        result = self._values.get("blocked_input_messaging")
        assert result is not None, "Required property 'blocked_input_messaging' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blocked_outputs_messaging(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#blocked_outputs_messaging BedrockGuardrail#blocked_outputs_messaging}.'''
        result = self._values.get("blocked_outputs_messaging")
        assert result is not None, "Required property 'blocked_outputs_messaging' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfig"]]]:
        '''content_policy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#content_policy_config BedrockGuardrail#content_policy_config}
        '''
        result = self._values.get("content_policy_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfig"]]], result)

    @builtins.property
    def contextual_grounding_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContextualGroundingPolicyConfig"]]]:
        '''contextual_grounding_policy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#contextual_grounding_policy_config BedrockGuardrail#contextual_grounding_policy_config}
        '''
        result = self._values.get("contextual_grounding_policy_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContextualGroundingPolicyConfig"]]], result)

    @builtins.property
    def cross_region_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailCrossRegionConfig"]]]:
        '''cross_region_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#cross_region_config BedrockGuardrail#cross_region_config}
        '''
        result = self._values.get("cross_region_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailCrossRegionConfig"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#description BedrockGuardrail#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#kms_key_arn BedrockGuardrail#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#region BedrockGuardrail#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitive_information_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfig"]]]:
        '''sensitive_information_policy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#sensitive_information_policy_config BedrockGuardrail#sensitive_information_policy_config}
        '''
        result = self._values.get("sensitive_information_policy_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfig"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tags BedrockGuardrail#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BedrockGuardrailTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#timeouts BedrockGuardrail#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BedrockGuardrailTimeouts"], result)

    @builtins.property
    def topic_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfig"]]]:
        '''topic_policy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#topic_policy_config BedrockGuardrail#topic_policy_config}
        '''
        result = self._values.get("topic_policy_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfig"]]], result)

    @builtins.property
    def word_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfig"]]]:
        '''word_policy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#word_policy_config BedrockGuardrail#word_policy_config}
        '''
        result = self._values.get("word_policy_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfig",
    jsii_struct_bases=[],
    name_mapping={"filters_config": "filtersConfig", "tier_config": "tierConfig"},
)
class BedrockGuardrailContentPolicyConfig:
    def __init__(
        self,
        *,
        filters_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContentPolicyConfigFiltersConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tier_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContentPolicyConfigTierConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filters_config: filters_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#filters_config BedrockGuardrail#filters_config}
        :param tier_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_config BedrockGuardrail#tier_config}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e51ee8244d3f560206d2bc0e4178c1c8d2b619509cf0d9feab76f761dae01c4)
            check_type(argname="argument filters_config", value=filters_config, expected_type=type_hints["filters_config"])
            check_type(argname="argument tier_config", value=tier_config, expected_type=type_hints["tier_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters_config is not None:
            self._values["filters_config"] = filters_config
        if tier_config is not None:
            self._values["tier_config"] = tier_config

    @builtins.property
    def filters_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfigFiltersConfig"]]]:
        '''filters_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#filters_config BedrockGuardrail#filters_config}
        '''
        result = self._values.get("filters_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfigFiltersConfig"]]], result)

    @builtins.property
    def tier_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfigTierConfig"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_config BedrockGuardrail#tier_config}.'''
        result = self._values.get("tier_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfigTierConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailContentPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigFiltersConfig",
    jsii_struct_bases=[],
    name_mapping={
        "input_strength": "inputStrength",
        "output_strength": "outputStrength",
        "type": "type",
        "input_action": "inputAction",
        "input_enabled": "inputEnabled",
        "input_modalities": "inputModalities",
        "output_action": "outputAction",
        "output_enabled": "outputEnabled",
        "output_modalities": "outputModalities",
    },
)
class BedrockGuardrailContentPolicyConfigFiltersConfig:
    def __init__(
        self,
        *,
        input_strength: builtins.str,
        output_strength: builtins.str,
        type: builtins.str,
        input_action: typing.Optional[builtins.str] = None,
        input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        input_modalities: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_action: typing.Optional[builtins.str] = None,
        output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_modalities: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param input_strength: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_strength BedrockGuardrail#input_strength}.
        :param output_strength: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_strength BedrockGuardrail#output_strength}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.
        :param input_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.
        :param input_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.
        :param input_modalities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_modalities BedrockGuardrail#input_modalities}.
        :param output_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.
        :param output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.
        :param output_modalities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_modalities BedrockGuardrail#output_modalities}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf6b79a6ae429d317ee4f075dd2fd8c39612817934f251da416ee4c8d93630d)
            check_type(argname="argument input_strength", value=input_strength, expected_type=type_hints["input_strength"])
            check_type(argname="argument output_strength", value=output_strength, expected_type=type_hints["output_strength"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument input_action", value=input_action, expected_type=type_hints["input_action"])
            check_type(argname="argument input_enabled", value=input_enabled, expected_type=type_hints["input_enabled"])
            check_type(argname="argument input_modalities", value=input_modalities, expected_type=type_hints["input_modalities"])
            check_type(argname="argument output_action", value=output_action, expected_type=type_hints["output_action"])
            check_type(argname="argument output_enabled", value=output_enabled, expected_type=type_hints["output_enabled"])
            check_type(argname="argument output_modalities", value=output_modalities, expected_type=type_hints["output_modalities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_strength": input_strength,
            "output_strength": output_strength,
            "type": type,
        }
        if input_action is not None:
            self._values["input_action"] = input_action
        if input_enabled is not None:
            self._values["input_enabled"] = input_enabled
        if input_modalities is not None:
            self._values["input_modalities"] = input_modalities
        if output_action is not None:
            self._values["output_action"] = output_action
        if output_enabled is not None:
            self._values["output_enabled"] = output_enabled
        if output_modalities is not None:
            self._values["output_modalities"] = output_modalities

    @builtins.property
    def input_strength(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_strength BedrockGuardrail#input_strength}.'''
        result = self._values.get("input_strength")
        assert result is not None, "Required property 'input_strength' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_strength(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_strength BedrockGuardrail#output_strength}.'''
        result = self._values.get("output_strength")
        assert result is not None, "Required property 'output_strength' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.'''
        result = self._values.get("input_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.'''
        result = self._values.get("input_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def input_modalities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_modalities BedrockGuardrail#input_modalities}.'''
        result = self._values.get("input_modalities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def output_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.'''
        result = self._values.get("output_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.'''
        result = self._values.get("output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_modalities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_modalities BedrockGuardrail#output_modalities}.'''
        result = self._values.get("output_modalities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailContentPolicyConfigFiltersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailContentPolicyConfigFiltersConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigFiltersConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16628221be8706b6bce78c5483b2aa55b3a659d1d97d4a60defcb54c0f2356ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailContentPolicyConfigFiltersConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73062407b32b33967ff1cb4c79887999a6dfbea7719b9f72bb0d3af367d038a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailContentPolicyConfigFiltersConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff3817e2512d0fe968a28e4cf27bc34bf7a7e32cff2f7a284b68f96e76ca62a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa94c27a8ff15a2705dd3c877adbdebcb9fc0512e823abd370027641c8a4d87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5563270c810def7ea1e88cda53acd0bcfdcbbe4a16f1a242576e827cb4fec777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigFiltersConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigFiltersConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigFiltersConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67c5c075f4294aa8242e9b8893110eb6ab0eed97c2c57b72bbe6ca0c0252afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContentPolicyConfigFiltersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigFiltersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cfe222aabd40543451b5c3ceb191024c37c64b850f7b68334c9097cdf4ee9a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInputAction")
    def reset_input_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputAction", []))

    @jsii.member(jsii_name="resetInputEnabled")
    def reset_input_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputEnabled", []))

    @jsii.member(jsii_name="resetInputModalities")
    def reset_input_modalities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputModalities", []))

    @jsii.member(jsii_name="resetOutputAction")
    def reset_output_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAction", []))

    @jsii.member(jsii_name="resetOutputEnabled")
    def reset_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEnabled", []))

    @jsii.member(jsii_name="resetOutputModalities")
    def reset_output_modalities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputModalities", []))

    @builtins.property
    @jsii.member(jsii_name="inputActionInput")
    def input_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputEnabledInput")
    def input_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="inputModalitiesInput")
    def input_modalities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputModalitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="inputStrengthInput")
    def input_strength_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputStrengthInput"))

    @builtins.property
    @jsii.member(jsii_name="outputActionInput")
    def output_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEnabledInput")
    def output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="outputModalitiesInput")
    def output_modalities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputModalitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="outputStrengthInput")
    def output_strength_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputStrengthInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputAction")
    def input_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputAction"))

    @input_action.setter
    def input_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9987815b3971648f02c52864a49e7c404a931c7f8b5b294b1fa31d50afbb795a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputEnabled")
    def input_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inputEnabled"))

    @input_enabled.setter
    def input_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d302c53f5ba4840bc53884131fefe290abcc61ce1370796e8e264af9d756aba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputModalities")
    def input_modalities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputModalities"))

    @input_modalities.setter
    def input_modalities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c27bc119560a85060fd562633c1ad9b8e9c1f9dba07a272ab9a53e0df86958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputModalities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputStrength")
    def input_strength(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputStrength"))

    @input_strength.setter
    def input_strength(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce5f970cede5bb7cb0c633f081c3b80d69f03dad89838fce86d92b0c4e8adb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputStrength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputAction")
    def output_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputAction"))

    @output_action.setter
    def output_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83be7642e6353f1d8de575b5a79dd7f1ba926472ebfbb24b44db6d45d7e3f497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEnabled")
    def output_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outputEnabled"))

    @output_enabled.setter
    def output_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396c523e895c761fd50762aae441cb9a2c92a8739710067c85b57ceb24d743e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputModalities")
    def output_modalities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outputModalities"))

    @output_modalities.setter
    def output_modalities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f97c34a347c1a5f6a79ced5813b11a06d180b4d25b2a10c5bd46784d9893be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputModalities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputStrength")
    def output_strength(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputStrength"))

    @output_strength.setter
    def output_strength(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78d51f6bc51a1f4087d9cde349ec5275adfee46ab011800206fec6b6d07ac80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputStrength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd47f1bda59f2759b8dab42ab7cdfe96eed854c473097f4ac093c05e5ba2f6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigFiltersConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigFiltersConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigFiltersConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c833aef8f413483e6f38a86f283c1d8ee4617f8f3823b124adb1bcb234597c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContentPolicyConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f04484d43274107ad11cce629dc8020449399f2c0695349c5e80fab6a54b6d56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailContentPolicyConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825cbc609657ee362cef15d87d340e8926719e014f431bf730236d709655b597)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailContentPolicyConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec0bdc0011cabaa9ee9710f34262132dedba3f0caf94562430eaf3152e4797a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62508f26b599d30d2963bb138b6edfc967d86f3972b3b093a0d459f14d947841)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc25978fe207121556f268b2715c5261f5d11328b6f3e40d7b79ac3f01ea3649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44478a3a8043cfc58d96ff80768f444f76f1c7ab9deb4a02d6e8808018d99e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContentPolicyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e70a332594eb4c17b6b67989efa0a7d5db20163d5bca448ff4ae22736c50d87b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFiltersConfig")
    def put_filters_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfigFiltersConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a617530fb0f4d5b407a757f1643652aa94fd9be472cd0febc2a0fe35ec5856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFiltersConfig", [value]))

    @jsii.member(jsii_name="putTierConfig")
    def put_tier_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContentPolicyConfigTierConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29cc5bcfa067b6d1432e12adddf2ed716091826d1b6c35b097c541d82e48bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTierConfig", [value]))

    @jsii.member(jsii_name="resetFiltersConfig")
    def reset_filters_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFiltersConfig", []))

    @jsii.member(jsii_name="resetTierConfig")
    def reset_tier_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierConfig", []))

    @builtins.property
    @jsii.member(jsii_name="filtersConfig")
    def filters_config(self) -> BedrockGuardrailContentPolicyConfigFiltersConfigList:
        return typing.cast(BedrockGuardrailContentPolicyConfigFiltersConfigList, jsii.get(self, "filtersConfig"))

    @builtins.property
    @jsii.member(jsii_name="tierConfig")
    def tier_config(self) -> "BedrockGuardrailContentPolicyConfigTierConfigList":
        return typing.cast("BedrockGuardrailContentPolicyConfigTierConfigList", jsii.get(self, "tierConfig"))

    @builtins.property
    @jsii.member(jsii_name="filtersConfigInput")
    def filters_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigFiltersConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigFiltersConfig]]], jsii.get(self, "filtersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tierConfigInput")
    def tier_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfigTierConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContentPolicyConfigTierConfig"]]], jsii.get(self, "tierConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bdd496d434c7b6e809d9f133613cdadb214e42b84f53e56a67131abd5ad988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigTierConfig",
    jsii_struct_bases=[],
    name_mapping={"tier_name": "tierName"},
)
class BedrockGuardrailContentPolicyConfigTierConfig:
    def __init__(self, *, tier_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param tier_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_name BedrockGuardrail#tier_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe06b6debce9a98b908e37159cf3e54cb07f393fe07954da6b862a91024052be)
            check_type(argname="argument tier_name", value=tier_name, expected_type=type_hints["tier_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tier_name is not None:
            self._values["tier_name"] = tier_name

    @builtins.property
    def tier_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_name BedrockGuardrail#tier_name}.'''
        result = self._values.get("tier_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailContentPolicyConfigTierConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailContentPolicyConfigTierConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigTierConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ccef2fc08d6597eadd49604dbb1a58e1a565302c2891578f914bbe70faaa9d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailContentPolicyConfigTierConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf63aa35b4f5817b9eff48ecb33616542a9055c13ba28198171c49422f88a4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailContentPolicyConfigTierConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a139ed6c0fd2a41ee74a9df71a0704012ce6113a3813c7f998b278e29dfab0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9c3a00fa4cced0fc26677091a2ee8dadb9e79a6eefbbb83cfb7a1f154005af1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b7164c23f52c8dcd9341541b63bf4fc8c1b9fe8f5df8ea29e197b53c7d3527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigTierConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigTierConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigTierConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a33517e324788a15653a98346311cb4a169108a16d96dc6fd158e07dfc12564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContentPolicyConfigTierConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContentPolicyConfigTierConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5d38903fe1d42a72d89c1598a38adfd9691625bd18b45c40df41c26ffb7eefc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTierName")
    def reset_tier_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierName", []))

    @builtins.property
    @jsii.member(jsii_name="tierNameInput")
    def tier_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tierName")
    def tier_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tierName"))

    @tier_name.setter
    def tier_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826e883fcd113879b09ce4a8db9ff2be7f74e4fec055a30768fe4b0ad0feeb24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigTierConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigTierConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigTierConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8b9ae20d0ab82e8500d91e4eaa804ce9c37c0d75772b179aa1f90ec1058c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContextualGroundingPolicyConfig",
    jsii_struct_bases=[],
    name_mapping={"filters_config": "filtersConfig"},
)
class BedrockGuardrailContextualGroundingPolicyConfig:
    def __init__(
        self,
        *,
        filters_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param filters_config: filters_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#filters_config BedrockGuardrail#filters_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fdfc4cc52636c238c9508c0528d12c6957327ec9f7977b9efe9b34caa6fc218)
            check_type(argname="argument filters_config", value=filters_config, expected_type=type_hints["filters_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters_config is not None:
            self._values["filters_config"] = filters_config

    @builtins.property
    def filters_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig"]]]:
        '''filters_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#filters_config BedrockGuardrail#filters_config}
        '''
        result = self._values.get("filters_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailContextualGroundingPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig",
    jsii_struct_bases=[],
    name_mapping={"threshold": "threshold", "type": "type"},
)
class BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig:
    def __init__(self, *, threshold: jsii.Number, type: builtins.str) -> None:
        '''
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#threshold BedrockGuardrail#threshold}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fee62eb6c0dc16b849fa560b4cec9e81f6349a3e87e1208e215cb4bf7c656e)
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "type": type,
        }

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#threshold BedrockGuardrail#threshold}.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a6f9cdc8ff20e786b87ff570930f73f69650921cc021f0609f4a403f848115)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56ad151a1175b587cbd4ad4637603da4fb4002985d970bddf5d1a1eeedc0180)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4280889888f68097d3dbeea8476fa73ec09dfed2500b37e7401f660152d8e85f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa7f57b4e26869a73050de2fc22d5a65215a7a9b8da4f27bfdad731dd39818f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18176b13b3c6ccd33c7fdc913583b410b03b0b8f13a12e237f0a9fdbe26e88c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec05ff9169cb906b0e77934aec24bbe7e3ad81ccd637fbc7ded5aa0181dda6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aa2fcb0aaa360464a8c18aea49a5113692905ed506345378eee300bc49c1b33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5095dae746987cff97e166aa6037a897c260b3098a9792138d47d0e94f95da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a7fdbe70284c707f6fba45ccc9112cffc251726ce2ec649be181c20b567c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b960be5bdbc3c37b2da88075acfd9ed2b21df3b994d0c6ad6af4656cb87d3f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContextualGroundingPolicyConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContextualGroundingPolicyConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__996129c3f3804958ed1ffee2997934cbf3f962b1a62461328dde7a5cc49a7a3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailContextualGroundingPolicyConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467eaf0b340c5fa520b9edbc42b66245ee6003d786d6934cdc3014be7e4727ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailContextualGroundingPolicyConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efeeacb4e9731f30008002d11f666d70abf64b44bef84f009e95ed570c3f6952)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcbd5387324f41d5abdbdf37773eb57ac5bad9c1f834899b6aaf8bf1ba58e2b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57ee50e485c3c807a4ace84f82c1bd391336eac180e74298f3f8161604ec9874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360551b773eeee384d8258e14d0340586995d9fb8dfca51cf19f8bdeadea46e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailContextualGroundingPolicyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailContextualGroundingPolicyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53ed0a7a83761f813a19c76000f226eeb830691a9bad9f9154b5bdd94cfa2627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFiltersConfig")
    def put_filters_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e4ba938d1ce6cac0614894b0b7262523c64c0c32853f75fdce3ba9f305e8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFiltersConfig", [value]))

    @jsii.member(jsii_name="resetFiltersConfig")
    def reset_filters_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFiltersConfig", []))

    @builtins.property
    @jsii.member(jsii_name="filtersConfig")
    def filters_config(
        self,
    ) -> BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigList:
        return typing.cast(BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigList, jsii.get(self, "filtersConfig"))

    @builtins.property
    @jsii.member(jsii_name="filtersConfigInput")
    def filters_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]], jsii.get(self, "filtersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c255d3a118beb356a8dc862f6d6ef043614472fdae1ed3a9bb68ad55c2e88864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailCrossRegionConfig",
    jsii_struct_bases=[],
    name_mapping={"guardrail_profile_identifier": "guardrailProfileIdentifier"},
)
class BedrockGuardrailCrossRegionConfig:
    def __init__(self, *, guardrail_profile_identifier: builtins.str) -> None:
        '''
        :param guardrail_profile_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#guardrail_profile_identifier BedrockGuardrail#guardrail_profile_identifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c613689de5c28dc5830543b881c28758178899c28600df402916104a7a07db4f)
            check_type(argname="argument guardrail_profile_identifier", value=guardrail_profile_identifier, expected_type=type_hints["guardrail_profile_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "guardrail_profile_identifier": guardrail_profile_identifier,
        }

    @builtins.property
    def guardrail_profile_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#guardrail_profile_identifier BedrockGuardrail#guardrail_profile_identifier}.'''
        result = self._values.get("guardrail_profile_identifier")
        assert result is not None, "Required property 'guardrail_profile_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailCrossRegionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailCrossRegionConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailCrossRegionConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c4a83feb5f6b509e322640866abca369e14e47fe52f3bd580c0898b6dcdd16b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailCrossRegionConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9dc623e52c5b3d56d534751f73bf56355c4e66f0cfab5d2ac6565d058fe3c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailCrossRegionConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e1575f3c98072c6d236998792e1b4165a9def252f75e5e095a9b2297babdf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb49a9a3c7c9c5eb72683db7cafdbee0f6834e7dd5d9f4378f3223dccf750790)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21b189d21b95577fbb1ee588f7bb5cfc90053f0a09dbb68fccdd5fafbb62079e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailCrossRegionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailCrossRegionConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailCrossRegionConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9589b7b099d3e2d1844318f646ee4a862093f9b3fb69de129aca85b684fba9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailCrossRegionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailCrossRegionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa2067481a0589348f9ed2d29b3e046a997d48f70275fff99fe4bd9787ddf9ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="guardrailProfileIdentifierInput")
    def guardrail_profile_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guardrailProfileIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="guardrailProfileIdentifier")
    def guardrail_profile_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guardrailProfileIdentifier"))

    @guardrail_profile_identifier.setter
    def guardrail_profile_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce94fd0329908f54296a01885615542eed4f868ca0c0af22f8864976bdc00cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailProfileIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailCrossRegionConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailCrossRegionConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailCrossRegionConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1d25c86d85f4c0564fd370d95a3155a7d1451f5080b22a346a67c1524b065e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "pii_entities_config": "piiEntitiesConfig",
        "regexes_config": "regexesConfig",
    },
)
class BedrockGuardrailSensitiveInformationPolicyConfig:
    def __init__(
        self,
        *,
        pii_entities_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        regexes_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param pii_entities_config: pii_entities_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#pii_entities_config BedrockGuardrail#pii_entities_config}
        :param regexes_config: regexes_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#regexes_config BedrockGuardrail#regexes_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1eb3e0d12fbf1c4314459c8ffae097fb71866b7039f312db18ba8ad496945e2)
            check_type(argname="argument pii_entities_config", value=pii_entities_config, expected_type=type_hints["pii_entities_config"])
            check_type(argname="argument regexes_config", value=regexes_config, expected_type=type_hints["regexes_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pii_entities_config is not None:
            self._values["pii_entities_config"] = pii_entities_config
        if regexes_config is not None:
            self._values["regexes_config"] = regexes_config

    @builtins.property
    def pii_entities_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig"]]]:
        '''pii_entities_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#pii_entities_config BedrockGuardrail#pii_entities_config}
        '''
        result = self._values.get("pii_entities_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig"]]], result)

    @builtins.property
    def regexes_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig"]]]:
        '''regexes_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#regexes_config BedrockGuardrail#regexes_config}
        '''
        result = self._values.get("regexes_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailSensitiveInformationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailSensitiveInformationPolicyConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c519368b7486e53391f3eee701cab4297f25c3108563a7f4b5ebb4c360352798)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailSensitiveInformationPolicyConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964276c1e6f060069073e48686aa3d1916f8905ee918c8aec5f6c730cd2bf676)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailSensitiveInformationPolicyConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264aa0c12850349bc588bdf7f02701b0f30a80849b22e97b606728f12e8eb653)
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
            type_hints = typing.get_type_hints(_typecheckingstub__451965510d8425597a31060321e746e5e838bfd55aacf7ad7eb5954d12678413)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a22659361686222185e037726d420d0f2155bf5b07167cd8091cd88c8c897bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295c3ff597d44bd1b83f1869ccbf430e477ccc783589d0c88c5c5ccc8ffb980b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailSensitiveInformationPolicyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c699ac68f49de79d978b0690fd99a614372c64bc448055d127550300dd5a1b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPiiEntitiesConfig")
    def put_pii_entities_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a4aeb51977fad0fdd93ce3a1e843fcdb6714d2595023fa283bde753ab63df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPiiEntitiesConfig", [value]))

    @jsii.member(jsii_name="putRegexesConfig")
    def put_regexes_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198cbca5b95022493458b6b98d42ca2a472f7127fbd68abdbdbda2725f0b89f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegexesConfig", [value]))

    @jsii.member(jsii_name="resetPiiEntitiesConfig")
    def reset_pii_entities_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiiEntitiesConfig", []))

    @jsii.member(jsii_name="resetRegexesConfig")
    def reset_regexes_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexesConfig", []))

    @builtins.property
    @jsii.member(jsii_name="piiEntitiesConfig")
    def pii_entities_config(
        self,
    ) -> "BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigList":
        return typing.cast("BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigList", jsii.get(self, "piiEntitiesConfig"))

    @builtins.property
    @jsii.member(jsii_name="regexesConfig")
    def regexes_config(
        self,
    ) -> "BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigList":
        return typing.cast("BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigList", jsii.get(self, "regexesConfig"))

    @builtins.property
    @jsii.member(jsii_name="piiEntitiesConfigInput")
    def pii_entities_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig"]]], jsii.get(self, "piiEntitiesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="regexesConfigInput")
    def regexes_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig"]]], jsii.get(self, "regexesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c41e9ad1f59e6c6da11af1d18e100d2c09855ed4e6a8b51870f7d71ebb78cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "type": "type",
        "input_action": "inputAction",
        "input_enabled": "inputEnabled",
        "output_action": "outputAction",
        "output_enabled": "outputEnabled",
    },
)
class BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig:
    def __init__(
        self,
        *,
        action: builtins.str,
        type: builtins.str,
        input_action: typing.Optional[builtins.str] = None,
        input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_action: typing.Optional[builtins.str] = None,
        output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#action BedrockGuardrail#action}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.
        :param input_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.
        :param input_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.
        :param output_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.
        :param output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da56630492f9ef68700d0ba9441758cdca9ae7ed98c79155a5e493d19e863a9)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument input_action", value=input_action, expected_type=type_hints["input_action"])
            check_type(argname="argument input_enabled", value=input_enabled, expected_type=type_hints["input_enabled"])
            check_type(argname="argument output_action", value=output_action, expected_type=type_hints["output_action"])
            check_type(argname="argument output_enabled", value=output_enabled, expected_type=type_hints["output_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "type": type,
        }
        if input_action is not None:
            self._values["input_action"] = input_action
        if input_enabled is not None:
            self._values["input_enabled"] = input_enabled
        if output_action is not None:
            self._values["output_action"] = output_action
        if output_enabled is not None:
            self._values["output_enabled"] = output_enabled

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#action BedrockGuardrail#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.'''
        result = self._values.get("input_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.'''
        result = self._values.get("input_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.'''
        result = self._values.get("output_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.'''
        result = self._values.get("output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__041bb0450767a551594d309d53b5f7bbb4d88c301ac2e1ebb0a263626cb9d5ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caebe61fb1f9c8db54ed2e5e7f1a54bb983e9c8782fc0ddff141128af6308f59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493e986c64d7faa06a2ee91c5e6663ed7c933e15de127a231d57cde4151389ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ce14c9820edccd6aa8d84d59fd07f3c9019a9c64a722a11a368541e4cf62e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bf926144c5cc3f1c22054671690bacb0ba0521e8e686f3775bc2afd63bc0b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9612a898fa0c44b3e59e617facce094f0408a63c64bd538b37459e1e387ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b65b8dc7d2fc39755e82e2cc99064b320740f0377f5f02b55c49bed955506dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInputAction")
    def reset_input_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputAction", []))

    @jsii.member(jsii_name="resetInputEnabled")
    def reset_input_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputEnabled", []))

    @jsii.member(jsii_name="resetOutputAction")
    def reset_output_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAction", []))

    @jsii.member(jsii_name="resetOutputEnabled")
    def reset_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputActionInput")
    def input_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputEnabledInput")
    def input_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="outputActionInput")
    def output_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEnabledInput")
    def output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26043917d564e069a393f0ef29a2cba9f9564dcaa0484747950069480a575c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputAction")
    def input_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputAction"))

    @input_action.setter
    def input_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2626d90ce3738700a5f8d923517a5ea04fac8f85ebe7a5e88725d1892780f4a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputEnabled")
    def input_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inputEnabled"))

    @input_enabled.setter
    def input_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170edf885459839fe8a1180a548f33ce96b716f48a3c972407b5a7697cbfb6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputAction")
    def output_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputAction"))

    @output_action.setter
    def output_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac56947f5016d876997c46742f811350adeaadec98fbce21c4e311ed4e94df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEnabled")
    def output_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outputEnabled"))

    @output_enabled.setter
    def output_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6899187f8fe8624f170c4728f46b94bf1b8b13b1a6e82768a146e8ac6b0173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077fd6b41e075877e1381f0c880da970900fe0dc727612e17ccb4252d07ad5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09af52b7ec760325db030592514ca40bcf0cc94b2af048ca9c5324ada9dcb83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "name": "name",
        "pattern": "pattern",
        "description": "description",
        "input_action": "inputAction",
        "input_enabled": "inputEnabled",
        "output_action": "outputAction",
        "output_enabled": "outputEnabled",
    },
)
class BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        pattern: builtins.str,
        description: typing.Optional[builtins.str] = None,
        input_action: typing.Optional[builtins.str] = None,
        input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_action: typing.Optional[builtins.str] = None,
        output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#action BedrockGuardrail#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#pattern BedrockGuardrail#pattern}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#description BedrockGuardrail#description}.
        :param input_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.
        :param input_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.
        :param output_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.
        :param output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c1dafa4c76334a24cf0f32f4b227a6d30a380904e564447429c13d80833b8d)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input_action", value=input_action, expected_type=type_hints["input_action"])
            check_type(argname="argument input_enabled", value=input_enabled, expected_type=type_hints["input_enabled"])
            check_type(argname="argument output_action", value=output_action, expected_type=type_hints["output_action"])
            check_type(argname="argument output_enabled", value=output_enabled, expected_type=type_hints["output_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
            "pattern": pattern,
        }
        if description is not None:
            self._values["description"] = description
        if input_action is not None:
            self._values["input_action"] = input_action
        if input_enabled is not None:
            self._values["input_enabled"] = input_enabled
        if output_action is not None:
            self._values["output_action"] = output_action
        if output_enabled is not None:
            self._values["output_enabled"] = output_enabled

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#action BedrockGuardrail#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#pattern BedrockGuardrail#pattern}.'''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#description BedrockGuardrail#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.'''
        result = self._values.get("input_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.'''
        result = self._values.get("input_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.'''
        result = self._values.get("output_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.'''
        result = self._values.get("output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adfe11a91002e7ae21ac7e153a090eee6598eedf2cd849602cbfdd24509c56e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e52f8edec39b7304fa34225962268e792b1b85f79130901fa195a076d13999)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130a07e6f53093f602df5badad8d791b329b4744ef3d2eba1299818ebb1faeab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7988d0178a1e6f7942d4b3f8cf9c129ed50a6e3cdaa4838575033e7944ac7ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0baf99be59c5bb33d065e2da9903602c44943de6cccccfa7a10561b513803f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e539d48d38767013346fc1745b9e960b4df59e20e5cb2496f74a4da4a159ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__439c7eb05166af73bfc2d993f7117959294cf6dbdc94b0b6dbb9b863ff2e044e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetInputAction")
    def reset_input_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputAction", []))

    @jsii.member(jsii_name="resetInputEnabled")
    def reset_input_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputEnabled", []))

    @jsii.member(jsii_name="resetOutputAction")
    def reset_output_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAction", []))

    @jsii.member(jsii_name="resetOutputEnabled")
    def reset_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputActionInput")
    def input_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputEnabledInput")
    def input_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputActionInput")
    def output_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEnabledInput")
    def output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94866cf9731ff12c5583eeacbb67747a13866fe1c9211e58d3c8f908889a1d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bffba49821c4cbfb1b6ad74317da919758ea0647a3ec316a0c1fdc01c548b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputAction")
    def input_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputAction"))

    @input_action.setter
    def input_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c19f1541147ccf580a1faba7102f899a2be5c03a6927f84cf7307b1dfaec630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputEnabled")
    def input_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inputEnabled"))

    @input_enabled.setter
    def input_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affdadfb76152c2b21f381db42021c3b9a5fae90cf4bfc5c42f41898ea535e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710b527d23b41cb4c8f2bccf7d06d6969775f0be8aed7d221957b9b3b31abc69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputAction")
    def output_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputAction"))

    @output_action.setter
    def output_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245cea5e4648727012d57498147eda62113b6a1ffe2fd525688ce87133b0d50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEnabled")
    def output_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outputEnabled"))

    @output_enabled.setter
    def output_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2058407bbae55570426d5f7f011d0f882a0693c8e6b946053d8c1a3dca8376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faed32b17a4cc2eb055b7f646283c0667dcdf2fe2a922fea844ef3016e2e8b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25a5032931e1360e6cae79845609e2bf6f2af21a2e8e643327af5342cabcc48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BedrockGuardrailTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#create BedrockGuardrail#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#delete BedrockGuardrail#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#update BedrockGuardrail#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ef06ab6926438b236f5e849554b0c858afac74b3483240763d0db8bb831ada)
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
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#create BedrockGuardrail#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#delete BedrockGuardrail#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#update BedrockGuardrail#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__511b4459d0aaea10804b5e17bf30729da46de3ce147de2f352b7dad49d25e6a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae61039c55332637d92770384cf7166737330aa20eb70fb563fb4118a495a204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0a7f5686482127837316d8afae3cca35ce5122aea5f362c4ca53bc5d50817c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34778932de0a2daf6796ca0b18b7e5e402fdb30c945c316709ae99ab518423cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd854ee6d1b5e1939548eb800484a235de0d11837d31ac800e3a5c4545409bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfig",
    jsii_struct_bases=[],
    name_mapping={"tier_config": "tierConfig", "topics_config": "topicsConfig"},
)
class BedrockGuardrailTopicPolicyConfig:
    def __init__(
        self,
        *,
        tier_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfigTierConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        topics_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfigTopicsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param tier_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_config BedrockGuardrail#tier_config}.
        :param topics_config: topics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#topics_config BedrockGuardrail#topics_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7fe74c3f55a36f518fb0c1c9596265216d505bf1e2ed0710e14f1222f198cf)
            check_type(argname="argument tier_config", value=tier_config, expected_type=type_hints["tier_config"])
            check_type(argname="argument topics_config", value=topics_config, expected_type=type_hints["topics_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tier_config is not None:
            self._values["tier_config"] = tier_config
        if topics_config is not None:
            self._values["topics_config"] = topics_config

    @builtins.property
    def tier_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTierConfig"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_config BedrockGuardrail#tier_config}.'''
        result = self._values.get("tier_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTierConfig"]]], result)

    @builtins.property
    def topics_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTopicsConfig"]]]:
        '''topics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#topics_config BedrockGuardrail#topics_config}
        '''
        result = self._values.get("topics_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTopicsConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailTopicPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailTopicPolicyConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d320399921d09ff5127f1b9a016c2b7d0414c296526dd03e7ad0f0bfc8d225aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailTopicPolicyConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fcea76c768411a707cc0d71950338e39d92282e12c2c23574687b2cbb035b74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailTopicPolicyConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9698837d2102b58964da34e0e2137f9dffbc65e0a67d66f06d5c91d5f2ed73c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6b8db5106ae20bf48e8c0dfccf18a5ec8e3588ae71530d23751acaa6a651f91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1173dadf685854cf6ce27264312173e69069edfebbb318db5f04118a544a1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b9a82464cac126738d819f4f992004d9fbcf0dccdbcbd93bb4fd8fd0aece0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailTopicPolicyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eb7034a93a91ae3a1e9c22413fe004b15d6ba6a69da00e756bebda5e84b5ac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTierConfig")
    def put_tier_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfigTierConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005ec7d34ad5b97c51558ce351375a8888078f455f45903de5f5b14e15939f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTierConfig", [value]))

    @jsii.member(jsii_name="putTopicsConfig")
    def put_topics_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailTopicPolicyConfigTopicsConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec208f000ae39c9b884d40ef72b033f50988aa1efbef1fb8af2c121b40b767d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopicsConfig", [value]))

    @jsii.member(jsii_name="resetTierConfig")
    def reset_tier_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierConfig", []))

    @jsii.member(jsii_name="resetTopicsConfig")
    def reset_topics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="tierConfig")
    def tier_config(self) -> "BedrockGuardrailTopicPolicyConfigTierConfigList":
        return typing.cast("BedrockGuardrailTopicPolicyConfigTierConfigList", jsii.get(self, "tierConfig"))

    @builtins.property
    @jsii.member(jsii_name="topicsConfig")
    def topics_config(self) -> "BedrockGuardrailTopicPolicyConfigTopicsConfigList":
        return typing.cast("BedrockGuardrailTopicPolicyConfigTopicsConfigList", jsii.get(self, "topicsConfig"))

    @builtins.property
    @jsii.member(jsii_name="tierConfigInput")
    def tier_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTierConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTierConfig"]]], jsii.get(self, "tierConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsConfigInput")
    def topics_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTopicsConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailTopicPolicyConfigTopicsConfig"]]], jsii.get(self, "topicsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b247f056b4e981c483a6cf55936686401ac758f7fea9ebbf6da783f6bc1863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigTierConfig",
    jsii_struct_bases=[],
    name_mapping={"tier_name": "tierName"},
)
class BedrockGuardrailTopicPolicyConfigTierConfig:
    def __init__(self, *, tier_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param tier_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_name BedrockGuardrail#tier_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a7cc31526b56c3300b6df69cbdfcdc654161bef9557055ec0b67a961a7d315)
            check_type(argname="argument tier_name", value=tier_name, expected_type=type_hints["tier_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tier_name is not None:
            self._values["tier_name"] = tier_name

    @builtins.property
    def tier_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#tier_name BedrockGuardrail#tier_name}.'''
        result = self._values.get("tier_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailTopicPolicyConfigTierConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailTopicPolicyConfigTierConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigTierConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ab9104e3e674086868d74fdafcad7441eab542903c0206610077755cc55665c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailTopicPolicyConfigTierConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4b8c734a58038cff8de4c6b9a122bee7e7fb6d9b8f44b4b8ff121db2fcc5b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailTopicPolicyConfigTierConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afc0c5c935a731a928304153054391dac110b13a0a34931891dbe3055df4d8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c30f37d7e0481712c49e90ca0081690e8e290c0bc38ae3491db0b19a4512c45a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5363a45c2123c859325bab70c220829c095d50f74903db9a9a8dad75d03ed2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTierConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTierConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTierConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6773850fb423721280020306ba1cea638b163b225cfa431d03e21b9ae3de8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailTopicPolicyConfigTierConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigTierConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4816eb1bf474aca349633c62c7bc9f2ee268115263a36aa0aaa46be29310ba6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTierName")
    def reset_tier_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierName", []))

    @builtins.property
    @jsii.member(jsii_name="tierNameInput")
    def tier_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tierName")
    def tier_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tierName"))

    @tier_name.setter
    def tier_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585d5b240134056905574760366a0235f224142bc05750c8ae8cf382085c021b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTierConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTierConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTierConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b985f3d1a8e74be2e57dc25ce4e052ab546edf4d66d7951289a92bb5f5c495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigTopicsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "name": "name",
        "type": "type",
        "examples": "examples",
    },
)
class BedrockGuardrailTopicPolicyConfigTopicsConfig:
    def __init__(
        self,
        *,
        definition: builtins.str,
        name: builtins.str,
        type: builtins.str,
        examples: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param definition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#definition BedrockGuardrail#definition}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.
        :param examples: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#examples BedrockGuardrail#examples}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b2fc4ae1bac6d0365c91385794653154534bb67adf8a3097e844e8bb764284)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument examples", value=examples, expected_type=type_hints["examples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "name": name,
            "type": type,
        }
        if examples is not None:
            self._values["examples"] = examples

    @builtins.property
    def definition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#definition BedrockGuardrail#definition}.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#name BedrockGuardrail#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def examples(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#examples BedrockGuardrail#examples}.'''
        result = self._values.get("examples")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailTopicPolicyConfigTopicsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailTopicPolicyConfigTopicsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigTopicsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfe332509536f4f9d31fc1ed9f8747d5da869389afd4fd3dc7e576f82c77dc48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailTopicPolicyConfigTopicsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420e75462fccfe1a6c18d11bf92ac3540447ed218342351871143157ce072290)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailTopicPolicyConfigTopicsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8804bfe558c558cc78b066dc396a90507f9a316bc17077c1e44651be1686f821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c26c63c9a25d1c14984f7a9842692f0c97beaa25ce4bf3cf5682d9eef015a85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b14bd2d5ca99c399f07c226af905ebe79707e32e2a578900681301a4c4511212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTopicsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTopicsConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTopicsConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c174c41785dfabf5792d458657b38bd9111c6a7eaabb36bfd785c559f8b7f772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailTopicPolicyConfigTopicsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailTopicPolicyConfigTopicsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0782c269eaf9d45f2f7250a98d39938c95ec09846d98664d65be14423d56906)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExamples")
    def reset_examples(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExamples", []))

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionInput"))

    @builtins.property
    @jsii.member(jsii_name="examplesInput")
    def examples_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "examplesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458e426d5ef089bc5189421f816367e2117af7d58fd9b6c0ad4698eb75278a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="examples")
    def examples(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "examples"))

    @examples.setter
    def examples(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18981e38ebe094587f61fc091833e0fdd81b83be453114fd0f616c052f0cb534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "examples", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524f9ad02b65ec26a7c243bf8a35430cb1f88703eacb6dad1e846024f79787fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69691b495bc54e280c13b9f3d2b4130c3c507b0a8ec5be3d26c6b85658acd713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTopicsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTopicsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTopicsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025f2ba17d3fd13c57a6b0424c214759af9a38cf9e5a84c7898d758e265c7462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "managed_word_lists_config": "managedWordListsConfig",
        "words_config": "wordsConfig",
    },
)
class BedrockGuardrailWordPolicyConfig:
    def __init__(
        self,
        *,
        managed_word_lists_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailWordPolicyConfigManagedWordListsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        words_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailWordPolicyConfigWordsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param managed_word_lists_config: managed_word_lists_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#managed_word_lists_config BedrockGuardrail#managed_word_lists_config}
        :param words_config: words_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#words_config BedrockGuardrail#words_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f049527ae3d535c660add7005907b3c53261ca6d8dddf30c58ac9bcc0b7de8b9)
            check_type(argname="argument managed_word_lists_config", value=managed_word_lists_config, expected_type=type_hints["managed_word_lists_config"])
            check_type(argname="argument words_config", value=words_config, expected_type=type_hints["words_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if managed_word_lists_config is not None:
            self._values["managed_word_lists_config"] = managed_word_lists_config
        if words_config is not None:
            self._values["words_config"] = words_config

    @builtins.property
    def managed_word_lists_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfigManagedWordListsConfig"]]]:
        '''managed_word_lists_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#managed_word_lists_config BedrockGuardrail#managed_word_lists_config}
        '''
        result = self._values.get("managed_word_lists_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfigManagedWordListsConfig"]]], result)

    @builtins.property
    def words_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfigWordsConfig"]]]:
        '''words_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#words_config BedrockGuardrail#words_config}
        '''
        result = self._values.get("words_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfigWordsConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailWordPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailWordPolicyConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc48bc76fe331bee24683fcb3dff2ca48016c6f6175d4150e9cab411d458720d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailWordPolicyConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8caf6328ab0952459313ed70a7a84c271eb0fe655750b2f36786eceada90be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailWordPolicyConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bcbbc7b3ff1cf5f3bf32f4fd0e3edba4b422ef97864e68a2a175134f29aa0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a87c9a311c85e88c2e753d4ebab4bb7c01b9bd548c7e7a9007b6f2a53950056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__869a520c92c062d70642f704e07d6aac741b3484112d5bf0a949f49b73a66227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3850ad28f4b4c0119bc5a2d0c780a70e00010f7d8463719c2827f60fc36e69d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigManagedWordListsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "input_action": "inputAction",
        "input_enabled": "inputEnabled",
        "output_action": "outputAction",
        "output_enabled": "outputEnabled",
    },
)
class BedrockGuardrailWordPolicyConfigManagedWordListsConfig:
    def __init__(
        self,
        *,
        type: builtins.str,
        input_action: typing.Optional[builtins.str] = None,
        input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_action: typing.Optional[builtins.str] = None,
        output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.
        :param input_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.
        :param input_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.
        :param output_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.
        :param output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaef8d0b58a9912fa5621f3d9cfb46eae6bd41884ebe251677ce491056de09b5)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument input_action", value=input_action, expected_type=type_hints["input_action"])
            check_type(argname="argument input_enabled", value=input_enabled, expected_type=type_hints["input_enabled"])
            check_type(argname="argument output_action", value=output_action, expected_type=type_hints["output_action"])
            check_type(argname="argument output_enabled", value=output_enabled, expected_type=type_hints["output_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if input_action is not None:
            self._values["input_action"] = input_action
        if input_enabled is not None:
            self._values["input_enabled"] = input_enabled
        if output_action is not None:
            self._values["output_action"] = output_action
        if output_enabled is not None:
            self._values["output_enabled"] = output_enabled

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#type BedrockGuardrail#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.'''
        result = self._values.get("input_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.'''
        result = self._values.get("input_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.'''
        result = self._values.get("output_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.'''
        result = self._values.get("output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailWordPolicyConfigManagedWordListsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailWordPolicyConfigManagedWordListsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigManagedWordListsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3361b68f5af75dcffaa53e75be587b776762a581291c202c7f64f131406a4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailWordPolicyConfigManagedWordListsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64796ca500eac2201a24a2158171446362d6070082a91fbc761ab01c37283348)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailWordPolicyConfigManagedWordListsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8790674a724dd7b01fef653c3fbd911337f20bea231d59b4dd1998f18943416b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18a50827a9d93f0d1100e289988e02a5bd4dba16e4372797fc4f64584d855f69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22b64b735389953190c3fd90d1bc93252330c1ba894a37a24550bb5d9e466d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029472f82792d5412be77f755244950de2d56416eb0cfe100af9697fd8344f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailWordPolicyConfigManagedWordListsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigManagedWordListsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3da6f59a4591a66659b9cf5582add0112735c2ced59112b34965b528b35a7ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInputAction")
    def reset_input_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputAction", []))

    @jsii.member(jsii_name="resetInputEnabled")
    def reset_input_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputEnabled", []))

    @jsii.member(jsii_name="resetOutputAction")
    def reset_output_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAction", []))

    @jsii.member(jsii_name="resetOutputEnabled")
    def reset_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="inputActionInput")
    def input_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputEnabledInput")
    def input_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="outputActionInput")
    def output_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEnabledInput")
    def output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputAction")
    def input_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputAction"))

    @input_action.setter
    def input_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e813d84ed867184769c3c579c781cc8d7a3e2efbaf2f3adcde956df938d358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputEnabled")
    def input_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inputEnabled"))

    @input_enabled.setter
    def input_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e586da31d1e8c6f443d777998dc9489f9148de40ae0786f1c390187156b503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputAction")
    def output_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputAction"))

    @output_action.setter
    def output_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7873ad763e6212bdf6f455004a5dfeed69acb9edb8cfbdd1a1a3139a386468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEnabled")
    def output_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outputEnabled"))

    @output_enabled.setter
    def output_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844eaec6a14d8ed36c294ddf9f1d5625844658fb2f8af741595eedf2d1ce671e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259b7203e0c0b6218c89567c9080cbbd8b34584385aacadd556528631cdcd183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigManagedWordListsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigManagedWordListsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4d1c30dfc0c88131462aa55fbff879b106fcfe131d87cbcb992dea95f0c51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailWordPolicyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5d849eaa684d93c8b53d0739ae1bf2a5f85943ee415e32c9b6a0faf04336d3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putManagedWordListsConfig")
    def put_managed_word_lists_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfigManagedWordListsConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2a29882db38481af24a1be720584954179f6726bf58599c2be247128017f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedWordListsConfig", [value]))

    @jsii.member(jsii_name="putWordsConfig")
    def put_words_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockGuardrailWordPolicyConfigWordsConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364e321d645e3f6fea9304bd591bd89b9ff37ae2859a9bd01e164aba6b5cc17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWordsConfig", [value]))

    @jsii.member(jsii_name="resetManagedWordListsConfig")
    def reset_managed_word_lists_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedWordListsConfig", []))

    @jsii.member(jsii_name="resetWordsConfig")
    def reset_words_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWordsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="managedWordListsConfig")
    def managed_word_lists_config(
        self,
    ) -> BedrockGuardrailWordPolicyConfigManagedWordListsConfigList:
        return typing.cast(BedrockGuardrailWordPolicyConfigManagedWordListsConfigList, jsii.get(self, "managedWordListsConfig"))

    @builtins.property
    @jsii.member(jsii_name="wordsConfig")
    def words_config(self) -> "BedrockGuardrailWordPolicyConfigWordsConfigList":
        return typing.cast("BedrockGuardrailWordPolicyConfigWordsConfigList", jsii.get(self, "wordsConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedWordListsConfigInput")
    def managed_word_lists_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]], jsii.get(self, "managedWordListsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="wordsConfigInput")
    def words_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfigWordsConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockGuardrailWordPolicyConfigWordsConfig"]]], jsii.get(self, "wordsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23233048635320e1c6d1ca4a7cec754fe8788f102e6a08b0ff153489398800e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigWordsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "text": "text",
        "input_action": "inputAction",
        "input_enabled": "inputEnabled",
        "output_action": "outputAction",
        "output_enabled": "outputEnabled",
    },
)
class BedrockGuardrailWordPolicyConfigWordsConfig:
    def __init__(
        self,
        *,
        text: builtins.str,
        input_action: typing.Optional[builtins.str] = None,
        input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_action: typing.Optional[builtins.str] = None,
        output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#text BedrockGuardrail#text}.
        :param input_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.
        :param input_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.
        :param output_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.
        :param output_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b83a25b9f4bd8ea8390eafdd285602cd9695043e7a955e961dbd9a41011de92)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument input_action", value=input_action, expected_type=type_hints["input_action"])
            check_type(argname="argument input_enabled", value=input_enabled, expected_type=type_hints["input_enabled"])
            check_type(argname="argument output_action", value=output_action, expected_type=type_hints["output_action"])
            check_type(argname="argument output_enabled", value=output_enabled, expected_type=type_hints["output_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }
        if input_action is not None:
            self._values["input_action"] = input_action
        if input_enabled is not None:
            self._values["input_enabled"] = input_enabled
        if output_action is not None:
            self._values["output_action"] = output_action
        if output_enabled is not None:
            self._values["output_enabled"] = output_enabled

    @builtins.property
    def text(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#text BedrockGuardrail#text}.'''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_action BedrockGuardrail#input_action}.'''
        result = self._values.get("input_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#input_enabled BedrockGuardrail#input_enabled}.'''
        result = self._values.get("input_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_action BedrockGuardrail#output_action}.'''
        result = self._values.get("output_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/bedrock_guardrail#output_enabled BedrockGuardrail#output_enabled}.'''
        result = self._values.get("output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockGuardrailWordPolicyConfigWordsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockGuardrailWordPolicyConfigWordsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigWordsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5865da6b4c573b973bfd69d5ba023a5e72e4b2b1efbfe4e85891f8b22a6d93a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockGuardrailWordPolicyConfigWordsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9d3b3792b4fc0f8de0cf6c233a412fb7f5f440db8ca296eb8d7884ecab09bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockGuardrailWordPolicyConfigWordsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8c22dbc16245dd11183c57ce173464edb27fe707da6ceb36d11a3d673e3f30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3624bb15613ccc832e0abb16c25a642d6f98b96d0bd3ba7432d5f2ad588000e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cac9d248dea85e8c84ba00c7e05c154c23aebd38b6d35059b9b5a84ff574314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigWordsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigWordsConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigWordsConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201ab631300edf6bfb366d9abca74e926df3cb2d3e1dcd2919ff35837c8018b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockGuardrailWordPolicyConfigWordsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.bedrockGuardrail.BedrockGuardrailWordPolicyConfigWordsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59c73d6977945819ee63b7f75b8f8566f53687d6d5f17c7dce8aa572ec22ecc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInputAction")
    def reset_input_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputAction", []))

    @jsii.member(jsii_name="resetInputEnabled")
    def reset_input_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputEnabled", []))

    @jsii.member(jsii_name="resetOutputAction")
    def reset_output_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAction", []))

    @jsii.member(jsii_name="resetOutputEnabled")
    def reset_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="inputActionInput")
    def input_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputEnabledInput")
    def input_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="outputActionInput")
    def output_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputActionInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEnabledInput")
    def output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outputEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="inputAction")
    def input_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputAction"))

    @input_action.setter
    def input_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1fb45be2f4ee8a236d1bd93b329bb3af4e096cf2946aad0e02cac9470b86bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputEnabled")
    def input_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inputEnabled"))

    @input_enabled.setter
    def input_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e34973fb8076ae0991705c2fcede8548a35471f5be398fd8167fe616279215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputAction")
    def output_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputAction"))

    @output_action.setter
    def output_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb18a3082ee5cd5b633f464b4e557bcd3fd03ad6454f712016dd9a6dc2a2080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEnabled")
    def output_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outputEnabled"))

    @output_enabled.setter
    def output_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14c916ac5a39a7a3818b2a2788f4f9de37472251c60321c64bdc751ed4c5c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd7e3626ffa504bd3d94211de33a0cb43f1fa727baa1bd3431d8802b298d123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigWordsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigWordsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigWordsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6da36cc643626b66bf938ed049ed4ce632258968bdfeef8a65709a879e6d436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BedrockGuardrail",
    "BedrockGuardrailConfig",
    "BedrockGuardrailContentPolicyConfig",
    "BedrockGuardrailContentPolicyConfigFiltersConfig",
    "BedrockGuardrailContentPolicyConfigFiltersConfigList",
    "BedrockGuardrailContentPolicyConfigFiltersConfigOutputReference",
    "BedrockGuardrailContentPolicyConfigList",
    "BedrockGuardrailContentPolicyConfigOutputReference",
    "BedrockGuardrailContentPolicyConfigTierConfig",
    "BedrockGuardrailContentPolicyConfigTierConfigList",
    "BedrockGuardrailContentPolicyConfigTierConfigOutputReference",
    "BedrockGuardrailContextualGroundingPolicyConfig",
    "BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig",
    "BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigList",
    "BedrockGuardrailContextualGroundingPolicyConfigFiltersConfigOutputReference",
    "BedrockGuardrailContextualGroundingPolicyConfigList",
    "BedrockGuardrailContextualGroundingPolicyConfigOutputReference",
    "BedrockGuardrailCrossRegionConfig",
    "BedrockGuardrailCrossRegionConfigList",
    "BedrockGuardrailCrossRegionConfigOutputReference",
    "BedrockGuardrailSensitiveInformationPolicyConfig",
    "BedrockGuardrailSensitiveInformationPolicyConfigList",
    "BedrockGuardrailSensitiveInformationPolicyConfigOutputReference",
    "BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig",
    "BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigList",
    "BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfigOutputReference",
    "BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig",
    "BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigList",
    "BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfigOutputReference",
    "BedrockGuardrailTimeouts",
    "BedrockGuardrailTimeoutsOutputReference",
    "BedrockGuardrailTopicPolicyConfig",
    "BedrockGuardrailTopicPolicyConfigList",
    "BedrockGuardrailTopicPolicyConfigOutputReference",
    "BedrockGuardrailTopicPolicyConfigTierConfig",
    "BedrockGuardrailTopicPolicyConfigTierConfigList",
    "BedrockGuardrailTopicPolicyConfigTierConfigOutputReference",
    "BedrockGuardrailTopicPolicyConfigTopicsConfig",
    "BedrockGuardrailTopicPolicyConfigTopicsConfigList",
    "BedrockGuardrailTopicPolicyConfigTopicsConfigOutputReference",
    "BedrockGuardrailWordPolicyConfig",
    "BedrockGuardrailWordPolicyConfigList",
    "BedrockGuardrailWordPolicyConfigManagedWordListsConfig",
    "BedrockGuardrailWordPolicyConfigManagedWordListsConfigList",
    "BedrockGuardrailWordPolicyConfigManagedWordListsConfigOutputReference",
    "BedrockGuardrailWordPolicyConfigOutputReference",
    "BedrockGuardrailWordPolicyConfigWordsConfig",
    "BedrockGuardrailWordPolicyConfigWordsConfigList",
    "BedrockGuardrailWordPolicyConfigWordsConfigOutputReference",
]

publication.publish()

def _typecheckingstub__89679a72b300b92734c8d2e4aec78dfd2b4ede2488d25427753f25c70c97d70a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    blocked_input_messaging: builtins.str,
    blocked_outputs_messaging: builtins.str,
    name: builtins.str,
    content_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    contextual_grounding_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContextualGroundingPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cross_region_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailCrossRegionConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sensitive_information_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BedrockGuardrailTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topic_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    word_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__cf15f6ce84a9a722232c465e06a98919853377be40c7d48190794b72a3c84c70(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aec3f0b81ab68ed0a7cdb27e15aa252049bdf9b97946b0d93be9d8e84ecf8c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48797a4fecbb10af82b1856b4dca29869096c93ab07a2cb360f117ca84eccfd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContextualGroundingPolicyConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8807dc1910475a7a2dd8018860175665fe0b5164b3d438e55e84f69c2e39dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailCrossRegionConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d962950aa15b3a41c5a46051726ca72adbae87c03639b9feff409433672840e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f1869e8588b0db501af561c56bc63b0ddc1bed511fda487ef174f63453db71(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc71905690b0215d05f721776fb501a72ab438809e9b14907b417c99c193b0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846272fb55b40e879aff759856b8ea6e3de1230cb8c9da05b684a14576ca3a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e41418248c163f6885c17f3f985cd0e5a358a2ebbc65d95a23c0b4d96aaeb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b7bacf5807e86b7afea7c8c7ae5f521953a38206b2d7794a77ab5c696b847e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71503680e5a32197d8a664ab2d7f32c403abae18f34d688e72fe43a972ccdc6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62304004a822227874b07faae546c388d289f249b8a8e82b790f55188e30e886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351189ac15f7a3a0694d4144b8e68bbb5dc12cfa8e1d3064ac4323dd0df85250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21e45ce0266cd6bcfcf1c7730d4b360b599838bc367d1bf6b7540eb68bb103f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e30826463460cd2647edc423fb15a8b83d4ac5dff3aaf26679822947a60695(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    blocked_input_messaging: builtins.str,
    blocked_outputs_messaging: builtins.str,
    name: builtins.str,
    content_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    contextual_grounding_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContextualGroundingPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cross_region_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailCrossRegionConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sensitive_information_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BedrockGuardrailTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topic_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    word_policy_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e51ee8244d3f560206d2bc0e4178c1c8d2b619509cf0d9feab76f761dae01c4(
    *,
    filters_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfigFiltersConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tier_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfigTierConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf6b79a6ae429d317ee4f075dd2fd8c39612817934f251da416ee4c8d93630d(
    *,
    input_strength: builtins.str,
    output_strength: builtins.str,
    type: builtins.str,
    input_action: typing.Optional[builtins.str] = None,
    input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    input_modalities: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_action: typing.Optional[builtins.str] = None,
    output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_modalities: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16628221be8706b6bce78c5483b2aa55b3a659d1d97d4a60defcb54c0f2356ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73062407b32b33967ff1cb4c79887999a6dfbea7719b9f72bb0d3af367d038a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff3817e2512d0fe968a28e4cf27bc34bf7a7e32cff2f7a284b68f96e76ca62a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa94c27a8ff15a2705dd3c877adbdebcb9fc0512e823abd370027641c8a4d87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5563270c810def7ea1e88cda53acd0bcfdcbbe4a16f1a242576e827cb4fec777(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67c5c075f4294aa8242e9b8893110eb6ab0eed97c2c57b72bbe6ca0c0252afa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigFiltersConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfe222aabd40543451b5c3ceb191024c37c64b850f7b68334c9097cdf4ee9a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9987815b3971648f02c52864a49e7c404a931c7f8b5b294b1fa31d50afbb795a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d302c53f5ba4840bc53884131fefe290abcc61ce1370796e8e264af9d756aba3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c27bc119560a85060fd562633c1ad9b8e9c1f9dba07a272ab9a53e0df86958(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce5f970cede5bb7cb0c633f081c3b80d69f03dad89838fce86d92b0c4e8adb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83be7642e6353f1d8de575b5a79dd7f1ba926472ebfbb24b44db6d45d7e3f497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396c523e895c761fd50762aae441cb9a2c92a8739710067c85b57ceb24d743e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f97c34a347c1a5f6a79ced5813b11a06d180b4d25b2a10c5bd46784d9893be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78d51f6bc51a1f4087d9cde349ec5275adfee46ab011800206fec6b6d07ac80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd47f1bda59f2759b8dab42ab7cdfe96eed854c473097f4ac093c05e5ba2f6bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c833aef8f413483e6f38a86f283c1d8ee4617f8f3823b124adb1bcb234597c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigFiltersConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04484d43274107ad11cce629dc8020449399f2c0695349c5e80fab6a54b6d56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825cbc609657ee362cef15d87d340e8926719e014f431bf730236d709655b597(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec0bdc0011cabaa9ee9710f34262132dedba3f0caf94562430eaf3152e4797a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62508f26b599d30d2963bb138b6edfc967d86f3972b3b093a0d459f14d947841(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc25978fe207121556f268b2715c5261f5d11328b6f3e40d7b79ac3f01ea3649(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44478a3a8043cfc58d96ff80768f444f76f1c7ab9deb4a02d6e8808018d99e95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70a332594eb4c17b6b67989efa0a7d5db20163d5bca448ff4ae22736c50d87b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a617530fb0f4d5b407a757f1643652aa94fd9be472cd0febc2a0fe35ec5856(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfigFiltersConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29cc5bcfa067b6d1432e12adddf2ed716091826d1b6c35b097c541d82e48bb4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContentPolicyConfigTierConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bdd496d434c7b6e809d9f133613cdadb214e42b84f53e56a67131abd5ad988(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe06b6debce9a98b908e37159cf3e54cb07f393fe07954da6b862a91024052be(
    *,
    tier_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccef2fc08d6597eadd49604dbb1a58e1a565302c2891578f914bbe70faaa9d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf63aa35b4f5817b9eff48ecb33616542a9055c13ba28198171c49422f88a4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a139ed6c0fd2a41ee74a9df71a0704012ce6113a3813c7f998b278e29dfab0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c3a00fa4cced0fc26677091a2ee8dadb9e79a6eefbbb83cfb7a1f154005af1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b7164c23f52c8dcd9341541b63bf4fc8c1b9fe8f5df8ea29e197b53c7d3527(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a33517e324788a15653a98346311cb4a169108a16d96dc6fd158e07dfc12564(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContentPolicyConfigTierConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d38903fe1d42a72d89c1598a38adfd9691625bd18b45c40df41c26ffb7eefc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826e883fcd113879b09ce4a8db9ff2be7f74e4fec055a30768fe4b0ad0feeb24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8b9ae20d0ab82e8500d91e4eaa804ce9c37c0d75772b179aa1f90ec1058c80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContentPolicyConfigTierConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdfc4cc52636c238c9508c0528d12c6957327ec9f7977b9efe9b34caa6fc218(
    *,
    filters_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fee62eb6c0dc16b849fa560b4cec9e81f6349a3e87e1208e215cb4bf7c656e(
    *,
    threshold: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a6f9cdc8ff20e786b87ff570930f73f69650921cc021f0609f4a403f848115(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56ad151a1175b587cbd4ad4637603da4fb4002985d970bddf5d1a1eeedc0180(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4280889888f68097d3dbeea8476fa73ec09dfed2500b37e7401f660152d8e85f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7f57b4e26869a73050de2fc22d5a65215a7a9b8da4f27bfdad731dd39818f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18176b13b3c6ccd33c7fdc913583b410b03b0b8f13a12e237f0a9fdbe26e88c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec05ff9169cb906b0e77934aec24bbe7e3ad81ccd637fbc7ded5aa0181dda6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa2fcb0aaa360464a8c18aea49a5113692905ed506345378eee300bc49c1b33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5095dae746987cff97e166aa6037a897c260b3098a9792138d47d0e94f95da3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a7fdbe70284c707f6fba45ccc9112cffc251726ce2ec649be181c20b567c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b960be5bdbc3c37b2da88075acfd9ed2b21df3b994d0c6ad6af4656cb87d3f9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996129c3f3804958ed1ffee2997934cbf3f962b1a62461328dde7a5cc49a7a3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467eaf0b340c5fa520b9edbc42b66245ee6003d786d6934cdc3014be7e4727ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efeeacb4e9731f30008002d11f666d70abf64b44bef84f009e95ed570c3f6952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbd5387324f41d5abdbdf37773eb57ac5bad9c1f834899b6aaf8bf1ba58e2b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ee50e485c3c807a4ace84f82c1bd391336eac180e74298f3f8161604ec9874(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360551b773eeee384d8258e14d0340586995d9fb8dfca51cf19f8bdeadea46e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailContextualGroundingPolicyConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ed0a7a83761f813a19c76000f226eeb830691a9bad9f9154b5bdd94cfa2627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e4ba938d1ce6cac0614894b0b7262523c64c0c32853f75fdce3ba9f305e8e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailContextualGroundingPolicyConfigFiltersConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c255d3a118beb356a8dc862f6d6ef043614472fdae1ed3a9bb68ad55c2e88864(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailContextualGroundingPolicyConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c613689de5c28dc5830543b881c28758178899c28600df402916104a7a07db4f(
    *,
    guardrail_profile_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4a83feb5f6b509e322640866abca369e14e47fe52f3bd580c0898b6dcdd16b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9dc623e52c5b3d56d534751f73bf56355c4e66f0cfab5d2ac6565d058fe3c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e1575f3c98072c6d236998792e1b4165a9def252f75e5e095a9b2297babdf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb49a9a3c7c9c5eb72683db7cafdbee0f6834e7dd5d9f4378f3223dccf750790(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b189d21b95577fbb1ee588f7bb5cfc90053f0a09dbb68fccdd5fafbb62079e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9589b7b099d3e2d1844318f646ee4a862093f9b3fb69de129aca85b684fba9dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailCrossRegionConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2067481a0589348f9ed2d29b3e046a997d48f70275fff99fe4bd9787ddf9ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce94fd0329908f54296a01885615542eed4f868ca0c0af22f8864976bdc00cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1d25c86d85f4c0564fd370d95a3155a7d1451f5080b22a346a67c1524b065e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailCrossRegionConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1eb3e0d12fbf1c4314459c8ffae097fb71866b7039f312db18ba8ad496945e2(
    *,
    pii_entities_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    regexes_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c519368b7486e53391f3eee701cab4297f25c3108563a7f4b5ebb4c360352798(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964276c1e6f060069073e48686aa3d1916f8905ee918c8aec5f6c730cd2bf676(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264aa0c12850349bc588bdf7f02701b0f30a80849b22e97b606728f12e8eb653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451965510d8425597a31060321e746e5e838bfd55aacf7ad7eb5954d12678413(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22659361686222185e037726d420d0f2155bf5b07167cd8091cd88c8c897bca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295c3ff597d44bd1b83f1869ccbf430e477ccc783589d0c88c5c5ccc8ffb980b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c699ac68f49de79d978b0690fd99a614372c64bc448055d127550300dd5a1b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a4aeb51977fad0fdd93ce3a1e843fcdb6714d2595023fa283bde753ab63df3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198cbca5b95022493458b6b98d42ca2a472f7127fbd68abdbdbda2725f0b89f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c41e9ad1f59e6c6da11af1d18e100d2c09855ed4e6a8b51870f7d71ebb78cc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da56630492f9ef68700d0ba9441758cdca9ae7ed98c79155a5e493d19e863a9(
    *,
    action: builtins.str,
    type: builtins.str,
    input_action: typing.Optional[builtins.str] = None,
    input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_action: typing.Optional[builtins.str] = None,
    output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041bb0450767a551594d309d53b5f7bbb4d88c301ac2e1ebb0a263626cb9d5ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caebe61fb1f9c8db54ed2e5e7f1a54bb983e9c8782fc0ddff141128af6308f59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493e986c64d7faa06a2ee91c5e6663ed7c933e15de127a231d57cde4151389ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ce14c9820edccd6aa8d84d59fd07f3c9019a9c64a722a11a368541e4cf62e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf926144c5cc3f1c22054671690bacb0ba0521e8e686f3775bc2afd63bc0b00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9612a898fa0c44b3e59e617facce094f0408a63c64bd538b37459e1e387ed3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b65b8dc7d2fc39755e82e2cc99064b320740f0377f5f02b55c49bed955506dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26043917d564e069a393f0ef29a2cba9f9564dcaa0484747950069480a575c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2626d90ce3738700a5f8d923517a5ea04fac8f85ebe7a5e88725d1892780f4a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170edf885459839fe8a1180a548f33ce96b716f48a3c972407b5a7697cbfb6f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac56947f5016d876997c46742f811350adeaadec98fbce21c4e311ed4e94df8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6899187f8fe8624f170c4728f46b94bf1b8b13b1a6e82768a146e8ac6b0173(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077fd6b41e075877e1381f0c880da970900fe0dc727612e17ccb4252d07ad5c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09af52b7ec760325db030592514ca40bcf0cc94b2af048ca9c5324ada9dcb83c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigPiiEntitiesConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c1dafa4c76334a24cf0f32f4b227a6d30a380904e564447429c13d80833b8d(
    *,
    action: builtins.str,
    name: builtins.str,
    pattern: builtins.str,
    description: typing.Optional[builtins.str] = None,
    input_action: typing.Optional[builtins.str] = None,
    input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_action: typing.Optional[builtins.str] = None,
    output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfe11a91002e7ae21ac7e153a090eee6598eedf2cd849602cbfdd24509c56e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e52f8edec39b7304fa34225962268e792b1b85f79130901fa195a076d13999(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130a07e6f53093f602df5badad8d791b329b4744ef3d2eba1299818ebb1faeab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7988d0178a1e6f7942d4b3f8cf9c129ed50a6e3cdaa4838575033e7944ac7ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baf99be59c5bb33d065e2da9903602c44943de6cccccfa7a10561b513803f6f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e539d48d38767013346fc1745b9e960b4df59e20e5cb2496f74a4da4a159ab0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439c7eb05166af73bfc2d993f7117959294cf6dbdc94b0b6dbb9b863ff2e044e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94866cf9731ff12c5583eeacbb67747a13866fe1c9211e58d3c8f908889a1d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bffba49821c4cbfb1b6ad74317da919758ea0647a3ec316a0c1fdc01c548b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c19f1541147ccf580a1faba7102f899a2be5c03a6927f84cf7307b1dfaec630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affdadfb76152c2b21f381db42021c3b9a5fae90cf4bfc5c42f41898ea535e3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710b527d23b41cb4c8f2bccf7d06d6969775f0be8aed7d221957b9b3b31abc69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245cea5e4648727012d57498147eda62113b6a1ffe2fd525688ce87133b0d50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2058407bbae55570426d5f7f011d0f882a0693c8e6b946053d8c1a3dca8376(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faed32b17a4cc2eb055b7f646283c0667dcdf2fe2a922fea844ef3016e2e8b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25a5032931e1360e6cae79845609e2bf6f2af21a2e8e643327af5342cabcc48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailSensitiveInformationPolicyConfigRegexesConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ef06ab6926438b236f5e849554b0c858afac74b3483240763d0db8bb831ada(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511b4459d0aaea10804b5e17bf30729da46de3ce147de2f352b7dad49d25e6a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae61039c55332637d92770384cf7166737330aa20eb70fb563fb4118a495a204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0a7f5686482127837316d8afae3cca35ce5122aea5f362c4ca53bc5d50817c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34778932de0a2daf6796ca0b18b7e5e402fdb30c945c316709ae99ab518423cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd854ee6d1b5e1939548eb800484a235de0d11837d31ac800e3a5c4545409bec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7fe74c3f55a36f518fb0c1c9596265216d505bf1e2ed0710e14f1222f198cf(
    *,
    tier_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfigTierConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    topics_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfigTopicsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d320399921d09ff5127f1b9a016c2b7d0414c296526dd03e7ad0f0bfc8d225aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcea76c768411a707cc0d71950338e39d92282e12c2c23574687b2cbb035b74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9698837d2102b58964da34e0e2137f9dffbc65e0a67d66f06d5c91d5f2ed73c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b8db5106ae20bf48e8c0dfccf18a5ec8e3588ae71530d23751acaa6a651f91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1173dadf685854cf6ce27264312173e69069edfebbb318db5f04118a544a1d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b9a82464cac126738d819f4f992004d9fbcf0dccdbcbd93bb4fd8fd0aece0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb7034a93a91ae3a1e9c22413fe004b15d6ba6a69da00e756bebda5e84b5ac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005ec7d34ad5b97c51558ce351375a8888078f455f45903de5f5b14e15939f40(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfigTierConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec208f000ae39c9b884d40ef72b033f50988aa1efbef1fb8af2c121b40b767d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailTopicPolicyConfigTopicsConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b247f056b4e981c483a6cf55936686401ac758f7fea9ebbf6da783f6bc1863(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a7cc31526b56c3300b6df69cbdfcdc654161bef9557055ec0b67a961a7d315(
    *,
    tier_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab9104e3e674086868d74fdafcad7441eab542903c0206610077755cc55665c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4b8c734a58038cff8de4c6b9a122bee7e7fb6d9b8f44b4b8ff121db2fcc5b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afc0c5c935a731a928304153054391dac110b13a0a34931891dbe3055df4d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30f37d7e0481712c49e90ca0081690e8e290c0bc38ae3491db0b19a4512c45a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5363a45c2123c859325bab70c220829c095d50f74903db9a9a8dad75d03ed2ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6773850fb423721280020306ba1cea638b163b225cfa431d03e21b9ae3de8ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTierConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4816eb1bf474aca349633c62c7bc9f2ee268115263a36aa0aaa46be29310ba6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585d5b240134056905574760366a0235f224142bc05750c8ae8cf382085c021b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b985f3d1a8e74be2e57dc25ce4e052ab546edf4d66d7951289a92bb5f5c495(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTierConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b2fc4ae1bac6d0365c91385794653154534bb67adf8a3097e844e8bb764284(
    *,
    definition: builtins.str,
    name: builtins.str,
    type: builtins.str,
    examples: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe332509536f4f9d31fc1ed9f8747d5da869389afd4fd3dc7e576f82c77dc48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420e75462fccfe1a6c18d11bf92ac3540447ed218342351871143157ce072290(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8804bfe558c558cc78b066dc396a90507f9a316bc17077c1e44651be1686f821(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c26c63c9a25d1c14984f7a9842692f0c97beaa25ce4bf3cf5682d9eef015a85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14bd2d5ca99c399f07c226af905ebe79707e32e2a578900681301a4c4511212(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c174c41785dfabf5792d458657b38bd9111c6a7eaabb36bfd785c559f8b7f772(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailTopicPolicyConfigTopicsConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0782c269eaf9d45f2f7250a98d39938c95ec09846d98664d65be14423d56906(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458e426d5ef089bc5189421f816367e2117af7d58fd9b6c0ad4698eb75278a46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18981e38ebe094587f61fc091833e0fdd81b83be453114fd0f616c052f0cb534(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524f9ad02b65ec26a7c243bf8a35430cb1f88703eacb6dad1e846024f79787fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69691b495bc54e280c13b9f3d2b4130c3c507b0a8ec5be3d26c6b85658acd713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025f2ba17d3fd13c57a6b0424c214759af9a38cf9e5a84c7898d758e265c7462(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailTopicPolicyConfigTopicsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f049527ae3d535c660add7005907b3c53261ca6d8dddf30c58ac9bcc0b7de8b9(
    *,
    managed_word_lists_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfigManagedWordListsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    words_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfigWordsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc48bc76fe331bee24683fcb3dff2ca48016c6f6175d4150e9cab411d458720d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8caf6328ab0952459313ed70a7a84c271eb0fe655750b2f36786eceada90be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bcbbc7b3ff1cf5f3bf32f4fd0e3edba4b422ef97864e68a2a175134f29aa0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a87c9a311c85e88c2e753d4ebab4bb7c01b9bd548c7e7a9007b6f2a53950056(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869a520c92c062d70642f704e07d6aac741b3484112d5bf0a949f49b73a66227(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3850ad28f4b4c0119bc5a2d0c780a70e00010f7d8463719c2827f60fc36e69d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaef8d0b58a9912fa5621f3d9cfb46eae6bd41884ebe251677ce491056de09b5(
    *,
    type: builtins.str,
    input_action: typing.Optional[builtins.str] = None,
    input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_action: typing.Optional[builtins.str] = None,
    output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3361b68f5af75dcffaa53e75be587b776762a581291c202c7f64f131406a4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64796ca500eac2201a24a2158171446362d6070082a91fbc761ab01c37283348(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8790674a724dd7b01fef653c3fbd911337f20bea231d59b4dd1998f18943416b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a50827a9d93f0d1100e289988e02a5bd4dba16e4372797fc4f64584d855f69(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b64b735389953190c3fd90d1bc93252330c1ba894a37a24550bb5d9e466d20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029472f82792d5412be77f755244950de2d56416eb0cfe100af9697fd8344f96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigManagedWordListsConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3da6f59a4591a66659b9cf5582add0112735c2ced59112b34965b528b35a7ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e813d84ed867184769c3c579c781cc8d7a3e2efbaf2f3adcde956df938d358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e586da31d1e8c6f443d777998dc9489f9148de40ae0786f1c390187156b503(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7873ad763e6212bdf6f455004a5dfeed69acb9edb8cfbdd1a1a3139a386468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844eaec6a14d8ed36c294ddf9f1d5625844658fb2f8af741595eedf2d1ce671e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259b7203e0c0b6218c89567c9080cbbd8b34584385aacadd556528631cdcd183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4d1c30dfc0c88131462aa55fbff879b106fcfe131d87cbcb992dea95f0c51a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigManagedWordListsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d849eaa684d93c8b53d0739ae1bf2a5f85943ee415e32c9b6a0faf04336d3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2a29882db38481af24a1be720584954179f6726bf58599c2be247128017f07(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfigManagedWordListsConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364e321d645e3f6fea9304bd591bd89b9ff37ae2859a9bd01e164aba6b5cc17a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockGuardrailWordPolicyConfigWordsConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23233048635320e1c6d1ca4a7cec754fe8788f102e6a08b0ff153489398800e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b83a25b9f4bd8ea8390eafdd285602cd9695043e7a955e961dbd9a41011de92(
    *,
    text: builtins.str,
    input_action: typing.Optional[builtins.str] = None,
    input_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_action: typing.Optional[builtins.str] = None,
    output_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5865da6b4c573b973bfd69d5ba023a5e72e4b2b1efbfe4e85891f8b22a6d93a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9d3b3792b4fc0f8de0cf6c233a412fb7f5f440db8ca296eb8d7884ecab09bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8c22dbc16245dd11183c57ce173464edb27fe707da6ceb36d11a3d673e3f30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3624bb15613ccc832e0abb16c25a642d6f98b96d0bd3ba7432d5f2ad588000e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cac9d248dea85e8c84ba00c7e05c154c23aebd38b6d35059b9b5a84ff574314(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201ab631300edf6bfb366d9abca74e926df3cb2d3e1dcd2919ff35837c8018b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockGuardrailWordPolicyConfigWordsConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c73d6977945819ee63b7f75b8f8566f53687d6d5f17c7dce8aa572ec22ecc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1fb45be2f4ee8a236d1bd93b329bb3af4e096cf2946aad0e02cac9470b86bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e34973fb8076ae0991705c2fcede8548a35471f5be398fd8167fe616279215(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb18a3082ee5cd5b633f464b4e557bcd3fd03ad6454f712016dd9a6dc2a2080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14c916ac5a39a7a3818b2a2788f4f9de37472251c60321c64bdc751ed4c5c90(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd7e3626ffa504bd3d94211de33a0cb43f1fa727baa1bd3431d8802b298d123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6da36cc643626b66bf938ed049ed4ce632258968bdfeef8a65709a879e6d436(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockGuardrailWordPolicyConfigWordsConfig]],
) -> None:
    """Type checking stubs"""
    pass
